# 📝 Automated Content Summarizer

A powerful and flexible text summarization tool built with LangChain, Groq API, and Streamlit that provides concise summaries of long articles and documents.

## 🚀 Features

- **Multiple Deployment Options:** Choose between local Ollama models or cloud-based Groq API
- **Fast Processing:** Instant summarization with real-time results
- **Clean Interface:** User-friendly Streamlit web application with responsive design
- **Console Support:** Command-line versions for direct usage and automation
- **Secure Configuration:** Environment variable support for API keys and sensitive data
- **Whitespace Handling:** Properly processes and cleans text formatting
- **Error Handling:** Robust error management with user-friendly messages

## 🛠️ Technologies Used

- **LangChain:** Framework for building LLM applications with powerful prompt management
- **Groq API:** High-performance cloud-based LLM inference for fast results
- **Ollama:** Local LLM deployment for offline and privacy-focused usage
- **Streamlit:** Modern web framework for building interactive data applications
- **Python:** Core programming language with extensive ecosystem support

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (for cloud models) - [Get yours here](https://console.groq.com/)
- Ollama (for local models) - [Install from ollama.ai](https://ollama.ai/)

### Quick Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Text_Summarizer
```
2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv/Scripts/activate

# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables:**
```bash
# Copy the environment template
cp .env.example .env
# Edit .env with your actual API key
```

## 🎯 Usage

### Web Interface (Recommended)

**Option 1: Local Ollama Model**
```bash
streamlit run Text_Summarizer_04.py
```

**Option 2: Groq Cloud API**
```bash
streamlit run Text_Summarizer_02.py
```

### Command Line Interface

**Option 1: Local Ollama Model**
```bash
python Text_Summarizer_03.py
```

**Option 2: Groq Cloud API**
```bash
python Text_Summarizer_01.py
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with your configuration:
```env
# Required for Groq API usage
GROQ_API_KEY=your-actual-groq-api-key-here

# Optional: Customize model names
GROQ_MODEL=llama-3.1-70b-versatile
OLLAMA_MODEL=llama3

# Optional: Temperature settings
GROQ_TEMPERATURE=0
```

### Streamlit Secrets (Alternative)
Create `.streamlit/secrets.toml` for Streamlit Cloud deployment:
```toml
[groq]
api_key = "your-actual-groq-api-key-here"
```

## 📁 Project Structure

```
Text_Summarizer/
├── Text_Summarizer_01.py      # Console app with Groq API
├── Text_Summarizer_02.py      # Web app with Groq API  
├── Text_Summarizer_03.py      # Console app with local Ollama
├── Text_Summarizer_04.py      # Web app with local Ollama
├── requirements.txt           # Exact library versions
├── .env                       # Environment variables (not committed)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── .streamlit/
    └── secrets.toml          # Streamlit secrets template
```

## 🔧 Model Options

### Groq Cloud Models (Fast, requires API key)
- `llama-3.3-70b-versatile` - Most powerful, detailed summaries
- `llama-3.1-8b-instant` - Fast, good for quick summaries

### Local Ollama Models (Offline, privacy-focused)
- `llama3` - Good general-purpose model
- `llama3:70b` - More powerful local option
- `mistral` - Alternative model option

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
