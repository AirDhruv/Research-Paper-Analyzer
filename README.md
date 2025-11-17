
# 📘 Research Paper Analyzer  
**AI‑Powered Tool for Automated Research Insight Extraction**

This project is an end‑to‑end implementation of an AI‑driven research paper analysis system.  
It extracts text from PDF research papers, preprocesses the content, breaks it into manageable chunks, and uses an LLM (Google Gemini or any pluggable model) to generate structured academic summaries.

---

# 🚀 Key Features

### 🔍 **PDF Processing**
- Upload any research paper in `.pdf` format.
- Extract text using **PyPDF2** (supports multi‑page, multi‑column text PDFs).
- Preprocess text to remove noise and prepare for summarization.

### 🧠 **AI Summarization**
- Uses Google Gemini (or other LLMs by swapping the client module).
- Produces structured JSON summaries with:
  - Title  
  - Domain  
  - Problem Statement  
  - Methods  
  - Results  
  - Strengths & Weaknesses  
  - Citations  
  - Keywords  

### 🧩 **Chunk‑Based Processing**
- Handles papers that exceed LLM token limits.
- Splits extracted text into overlapping chunks.
- Summaries for each chunk are merged into a final comprehensive output.

### 🖥️ **Streamlit Web App**
- Clean and interactive UI.
- Real‑time progress indicators.
- Summary display and downloadable text output.
- Runs fully locally or in Docker.

### 🛡️ **Security**
- `.env` for API keys  
- Git‑safe configuration  
- No user data stored  

### ⚙️ **Modular Architecture**
- Easy to swap AI providers (OpenAI, Gemini, Groq, etc.)
- Extendable for OCR, RAG, multi‑PDF analysis.

---

# 📂 Project Structure

```
research-paper-analyzer/
├── README.md
├── requirements.txt
├── .env.example
├── app.py
├── pdf_utils.py
├── ai_client.py
├── prompts.py
├── ui_helpers.py
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
├── tests/
│   ├── test_pdf_utils.py
│   └── test_prompts.py
└── scripts/
    └── run_local.sh
```

---

# 🛠️ Installation & Setup

## 1️⃣ Clone the Project
```
git clone https://github.com/AirDhruv/research-paper-analyzer.git
cd research-paper-analyzer
```

## 2️⃣ Create Virtual Environment
```
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
.venv\Scripts\activate        # Windows
```

## 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

## 4️⃣ Configure API Keys
Copy `.env.example` → `.env`
```
GOOGLE_API_KEY="your_api_key_here"
MAX_CHUNK_TOKENS=3000
CHUNK_OVERLAP=200
```

(You may substitute OpenAI keys if you modify `ai_client.py`.)

---

# ▶️ Running the Application

## Run Locally
```
streamlit run app.py
```

Then open the browser at:
```
http://localhost:8501
```

---

# 🐳 Docker Deployment

## Build Image
```
docker build -t rpa:latest .
```

## Run Container
```
docker run -p 8501:8501 --env-file .env rpa:latest
```

---

# 🧪 Testing

```
pytest -q
```

Includes unit tests for:
- PDF text extraction
- Chunking logic
- Prompt formatting

---

# 🧠 Architecture Overview

## 1️⃣ **Frontend (Streamlit)**
- File upload widget
- Progress bar during API processing
- Summary display area
- Download button for results

## 2️⃣ **Backend Logic**
### `pdf_utils.py`
- Extracts all text from PDF (per‑page extraction)
- Cleans and merges text
- Splits into word‑based chunks

### `ai_client.py`
- Provides a unified interface for LLMs
- Currently supports Google Gemini:
  - Initializes client
  - Sends prompt
  - Receives text completion

### `prompts.py`
- Stores structured prompt templates
- Ensures consistent summarization output

### `ui_helpers.py`
- Streamlit components for:
  - Result rendering
  - Download button

## 3️⃣ **Chunking Strategy**
Chunking mitigates token limit problems:
- Splits text into windows of ~3000 words
- Adds 200‑word overlap to preserve context

Final summary = Gemini summary over merged chunk summaries.

---

# 📊 Performance

| Component | Average Time |
|----------|---------------|
| PDF extraction | 1–3 seconds |
| Chunk creation | Instant |
| Summarization (Gemini) | 15–90 seconds per chunk |
| Final merge summary | 10–30 seconds |

Performance depends on API latency + model speed.

---

# 🧩 Extending the System

## 🔮 Short‑Term Enhancements
- Add export as PDF, DOCX, MD
- Add keyword highlighting
- Add citations extraction using regex + LLM

## 🚀 Medium‑Term Enhancements
- Integrate OCR:
  - `pytesseract`
  - PDF-to-image conversion
- Add semantic search over uploaded PDFs
- Store summaries in a local database (SQLite/Postgres)

## 🌐 Long‑Term Enhancements
- RAG pipeline (ChromaDB, Pinecone)
- Compare multiple research papers
- Topic clustering and visualization
- Fine‑tune custom academic summarization model

---

# ❓ FAQ

### **1. Does this support scanned PDFs?**  
Not by default — needs OCR. (Can be added.)

### **2. Does the app store my data?**  
No. Everything is processed in memory.

### **3. Can I use OpenAI instead of Gemini?**  
Yes — modify only `ai_client.py`.

### **4. Does it work offline?**  
No — requires LLM inference.

---

# 🤝 Contributing

Pull requests are welcome!  
If adding new features, follow conventional commit styles and update tests.

---

# 📝 License

MIT License.  
Feel free to use, modify, and distribute.

---

# 🙌 Acknowledgements

- Google Generative AI  
- PyPDF2  
- Streamlit Community  
- OpenAI Documentation  
- University Project Guidance  

---

If you want:
✅ A downloadable ZIP  
✅ A more detailed Deployment Guide  
✅ A version using **OpenAI GPT‑4.1**  
Just tell me!
