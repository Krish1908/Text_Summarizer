#!/usr/bin/env python3
"""
FastAPI backend for Text Summarizer.
Simple, fast, and production-ready.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import uvicorn
import requests
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from pathlib import Path
import logging

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("text-summarizer")

app = FastAPI(title="Text Summarizer API", version="1.0.0")

# Mount static files for the new UI
app.mount("/static", StaticFiles(directory="."), name="static")

# Disable caching for static files during development
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

app.add_middleware(NoCacheMiddleware)

logger.info("Text Summarizer API initialized")


# Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Application Limits
MAX_WORDS = 3000


class AppError(Exception):
    """Base class for all application-specific exceptions."""
    pass


class ValidationError(AppError):
    """Raised for invalid client input."""
    pass


class PayloadTooLargeError(AppError):
    """Raised when the request exceeds application limits."""
    pass


class AuthenticationError(AppError):
    """Raised when provider authentication fails."""
    pass


class RateLimitError(AppError):
    """Raised when the provider rate limit is exceeded."""
    pass


class ProviderUnavailableError(AppError):
    """Raised when the configured provider is unavailable."""
    pass


class ConfigurationError(AppError):
    """Raised when application configuration is invalid."""
    pass

class SummarizeRequest(BaseModel):
    text: str
    summary_type: str = "concise"
    language: str = "auto"
    method: str = "groq"  # "groq" or "ollama"
    temperature: float = 0.0


class SummarizeResponse(BaseModel):
    success: bool
    summary: str
    stats: dict
    timestamp: str



def get_api_key():
    """Get API key from environment variable"""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ConfigurationError("GROQ_API_KEY environment variable not set!")
    return api_key



def validate_text(text: str) -> str:
    """Validate input text"""
    if not text or not text.strip():
        raise ValidationError("Text cannot be empty")
    
    text = text.strip()
    word_count = len(text.split())

    if word_count > MAX_WORDS: # Enforce maximum input word limit
        logger.warning(
            "Input validation failed: word count (%d) exceeds the maximum allowed limit (%d).",
            word_count,
            MAX_WORDS,
        )

        raise PayloadTooLargeError(
            f"Text too long ({word_count} words). Please reduce it to under {MAX_WORDS} words."
        )

    return text


def build_prompt(text: str, summary_type: str, language: str) -> str:
    """Build the prompt for the LLM"""
    prompt = f"Summarize the following text in a {summary_type} manner:\n\n{text}\n\n"
    
    if summary_type == 'bullet':
        prompt += "Please provide the summary as bullet points."
    elif summary_type == 'keypoints':
        prompt += "Please extract the key points and main ideas."
    elif summary_type == 'detailed':
        prompt += "Please provide a detailed summary covering all important aspects."
    else:
        prompt += "Please provide a concise summary."
    
    if language != 'auto' and language != 'en':
        language_names = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 
            'de': 'German', 'it': 'Italian'
        }
        lang_name = language_names.get(language, language)
        prompt += f"\n\nPlease respond in {lang_name}."
    
    return prompt


def call_groq_api(prompt: str, model: str, temperature: float, api_key: str) -> str:
    """Call the Groq API using LangChain"""
    try:
        # Initialize LangChain Groq client
        llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=1000
        )
        
        # Create message and invoke model
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        
        return response.content
        
    except Exception as e:
        error = str(e).lower()

        if "authentication" in error or "invalid api key" in error:
            raise AuthenticationError("Invalid Groq API key.") from e

        if "rate_limit" in error or "rate limit" in error:
            raise RateLimitError("Groq API rate limit exceeded.") from e

        raise

def call_ollama_api(prompt: str, temperature: float) -> str:
    """Call the Ollama API using LangChain"""
    try:
        # Initialize LangChain Ollama client with hardcoded model
        llm = ChatOllama(
            model="phi3",  # Hardcoded model as requested
            temperature=temperature,
            max_tokens=1000
        )
        
        # Create message and invoke model
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        
        return response.content
        
    except Exception as e:
        error = str(e).lower()

        if "connection refused" in error:
            raise ProviderUnavailableError(
                "Ollama is not running or not reachable."
            ) from e

        if "failed to connect" in error:
            raise ProviderUnavailableError(
                "Ollama is not running or not reachable."
            ) from e

        raise

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main HTML page"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    """Summarize text using either Groq API or Ollama"""
    logger.info("Summary request received | provider=%s | summary_type=%s", request.method, request.summary_type,)
    try:
        # Validate input
        text = validate_text(request.text)
        
        # Build prompt
        prompt = build_prompt(text, request.summary_type, request.language)
        
        # Route to appropriate API based on method
        if request.method == "ollama":
            # Call Ollama API
            summary = call_ollama_api(prompt, request.temperature)
        else:
            # Default to Groq API
            api_key = get_api_key()
            summary = call_groq_api(prompt, "llama-3.1-8b-instant", request.temperature, api_key)
        
        # Calculate statistics
        original_words = len(text.split())
        summary_words = len(summary.split())
        reduction_ratio = ((original_words - summary_words) / original_words) * 100 if original_words > 0 else 0
        
        logger.info(
            "Summary generated successfully | provider=%s | original_words=%d | summary_words=%d | reduction=%.1f%%",
            request.method,
            original_words,
            summary_words,
            reduction_ratio,
        )

        return SummarizeResponse(
            success=True,
            summary=summary,
            stats={
                'original_words': original_words,
                'summary_words': summary_words,
                'reduction_percentage': round(reduction_ratio, 1)
            },
            timestamp=datetime.now().isoformat()
        )
        
    except ValidationError as e:
        logger.warning("Validation failed: %s", e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except PayloadTooLargeError as e:
        logger.warning("Payload too large: %s", e)
        raise HTTPException(
            status_code=413,
            detail=str(e),
        )
    
    except AuthenticationError as e:
        logger.warning("Authentication failed: %s", e)
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

    except RateLimitError as e:
        logger.warning("Rate limit exceeded: %s", e)
        raise HTTPException(
            status_code=429,
            detail=str(e),
        )

    except ProviderUnavailableError as e:
        logger.error("Provider unavailable: %s", e)
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )

    except ConfigurationError as e:
        logger.error("Configuration error: %s", e)
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    
    except Exception:
        logger.exception("Unhandled exception while processing summary request")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred.",
        )

@app.get("/api/methods")
async def get_methods():
    """Get available methods"""
    methods = [
        {
            'value': 'groq',
            'label': 'Groq API',
            'description': 'Cloud-based API with fast response times'
        },
        {
            'value': 'ollama',
            'label': 'Local Ollama',
            'description': 'Local AI processing, no internet required'
        }
    ]
    
    return {"success": True, "methods": methods}


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    # Check for API key
    if not os.getenv('GROQ_API_KEY'):
        logger.warning(
            "GROQ_API_KEY environment variable is not set. "
            "Please configure it before starting the application."
        )
    
    # Run the server
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info("Starting Text Summarizer API server on port %d", port)

    logger.info("Debug mode: %s", debug)

    logger.info(
        "API endpoint available at http://localhost:%d/api/summarize",
        port
    )

    logger.info(
        "Swagger UI available at http://localhost:%d/docs",
        port
    )
    
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)