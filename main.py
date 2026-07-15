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


def get_api_key():
    """Get API key from environment variable"""
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set!")
    return api_key


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


def validate_text(text: str) -> str:
    """Validate input text"""
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    if len(text) > 50000:  # Limit text length
        logger.warning("Input validation failed: text length (%d characters) exceeds the maximum allowed limit (50000).", len(text),)
        raise ValueError("Text too long. Please limit to 50,000 characters or less")
    
    return text.strip()


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
        raise Exception(f"LangChain API call failed: {str(e)}")


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
        raise Exception(f"Ollama API call failed: {str(e)}")


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
        
    except ValueError as e:
        logger.warning("Validation failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except requests.exceptions.RequestException as e:
        logger.error("External API request failed: %s", e)
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except Exception as e:
        logger.exception("Unhandled exception while processing summary request")
        error_msg = str(e)
        if 'rate_limit_exceeded' in error_msg or '413' in error_msg:
            raise HTTPException(status_code=429, detail="Your text is too large. Please shorten it to under 4000 words and try again.")
        elif 'Ollama API call failed' in error_msg:
            raise HTTPException(status_code=503, detail="Ollama is not running or not accessible. Please ensure Ollama is installed and running on localhost:11434.")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {error_msg}")
    

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