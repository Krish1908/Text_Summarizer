# 🤖 AI Text Summarizer

A fast, modern web-based text summarization tool powered by **Groq API** and **LangChain**, served through a **FastAPI** backend with a clean, responsive frontend.

---

## 🚀 Features

- **Instant Summarization** — Powered by Groq's LLaMA 3.1 8B model for fast, accurate results
- **4 Summary Formats** — Concise, Detailed, Bullet Points, or Key Points
- **Live Word & Character Count** — Real-time stats as you type
- **Clipboard Support** — Paste directly from clipboard with one click
- **File Upload** — Load `.txt`, `.doc`, `.docx`, or `.pdf` files directly
- **Copy & Download** — Export your summary to clipboard or as a `.txt` file
- **Token Limit Guard** — Warns you if text exceeds the 3000-word API limit before sending
- **Reduction Stats** — Shows word count and % reduction after every summary
- **Responsive Design** — Works on desktop, tablet, and mobile
- **Keyboard Shortcuts** — `Ctrl+Enter` to summarize, `Ctrl+K` to clear

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| AI / LLM | Groq API via LangChain |
| Model | `llama-3.1-8b-instant` |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Config | python-dotenv (`.env` file) |

---

## 📁 Project Structure

```
Text_Summarizer/
├── main.py               # FastAPI backend — API routes, LLM calls
├── index.html            # Frontend — main UI
├── styles.css            # Frontend — styling
├── script.js             # Frontend — button logic, API calls, animations
├── image-1.jpg           # Favicon / logo image
├── .env                  # API key
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- Groq API key — [Get yours free at console.groq.com](https://console.groq.com/)

### 1. Clone the repository
```bash
git clone <repository-url>
cd Text_Summarizer
```

### 2. Create and activate a virtual environment
```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your-actual-groq-api-key-here
```

---

## ▶️ Running the App

```bash
uvicorn main:app --reload --port 8000
```

Then open your browser and go to:
```
http://localhost:8000
```

The API documentation (Swagger UI) is available at:
```
http://localhost:8000/docs
```

---

## 🎯 How to Use

1. Open `http://localhost:8000` in your browser
2. Paste your text into the input box — or use the **Paste**, **Upload**, or **Clear** buttons
3. Select a summary format from the dropdown: `Concise`, `Detailed`, `Bullet Points`, or `Key Points`
4. Click **Generate Summary**
5. View the summary, then **Copy** or **Download** it

> ⚠️ Keep input under **3000 words** to stay within the free Groq API token limits.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main HTML page |
| `POST` | `/api/summarize` | Summarizes submitted text |
| `GET` | `/api/models` | Returns available LLM models |
| `GET` | `/api/health` | Health check |

---

## ⚙️ Configuration

All configuration is handled via the `.env` file:

```env
# Required
GROQ_API_KEY=your-actual-groq-api-key-here

# Optional
PORT=8000
DEBUG=False
```

---

## 🧠 Available Models

| Model | Speed | Quality | Use Case |
|---|---|---|---|
| `llama-3.1-8b-instant` | ⚡ Fast | Good | Default — everyday summarization |
| `llama-3.3-70b-versatile` | 🐢 Slower | Best | Long, complex documents |

> The default model is `llama-3.1-8b-instant`. To use a different model, update the `model` field in your API request.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + Enter` | Generate Summary |
| `Ctrl + K` | Clear all text |
| `Ctrl + V` | Paste from clipboard |

---


## 🐛 Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `500 Internal Server Error` on load | Wrong file path in `main.py` | Ensure `index.html` is in the same directory as `main.py` |
| `GROQ_API_KEY not set` warning | `.env` file missing or wrong path | Create `.env` in the root directory next to `main.py` |
| `413 / rate_limit_exceeded` error | Text too long for free tier | Reduce input to under 3000 words |
| Buttons not working | JS crash on load | Check browser console for errors |
| Static files not loading (CSS/JS) | Wrong static directory in `main.py` | Ensure `StaticFiles(directory=".")` in `main.py` |

---

## 📋 Requirements

```
fastapi==0.115.0
uvicorn[standard]==0.38.0
python-dotenv==1.1.1
pydantic==2.11.5
langchain-core==1.0.0
langchain-groq==1.0.0
requests==2.32.5
```

---