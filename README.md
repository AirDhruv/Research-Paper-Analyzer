# 📄 Research Paper Analyzer

A powerful AI-powered tool that automatically analyzes and summarizes academic research papers. Upload a PDF and get a structured, comprehensive summary powered by Google's Gemini AI.

## ✨ Features

- **PDF Text Extraction**: Automatically extracts text from research paper PDFs using PyPDF2
- **Intelligent Chunking**: Splits large documents into manageable chunks with configurable overlap for context preservation
- **AI-Powered Summarization**: Leverages Google Gemini Flash for fast, accurate summaries
- **Structured Output**: Generates summaries with consistent sections:
  - Overview
  - Problem Statement
  - Methodology
  - Key Findings
  - Conclusion
- **Progressive Processing**: Handles large papers by summarizing chunks individually and then merging them
- **User-Friendly Interface**: Clean Streamlit-based web interface
- **Download Summaries**: Export generated summaries as text files
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Research-Paper-Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   MAX_CHUNK_TOKENS=3000
   CHUNK_OVERLAP=200
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   
   Open your browser and navigate to `http://localhost:8501`

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Create a `.env` file** with your API key (see above)

2. **Run with Docker Compose**
   ```bash
   docker-compose up
   ```

3. **Access the application** at `http://localhost:8501`

### Using Docker Directly

```bash
# Build the image
docker build -t research-paper-analyzer .

# Run the container
docker run -p 8501:8501 --env-file .env research-paper-analyzer
```

## 📖 Usage

1. **Upload a PDF**: Click the upload button and select your research paper (PDF format)
2. **View Extracted Text**: Expand the "View Extracted Text Chunks" section to see how the paper was split
3. **Generate Summary**: Click the "Generate Summary" button to start the AI analysis
4. **Review Results**: Read the structured summary with all key sections
5. **Download**: Use the download button to save the summary as a text file

## 🏗️ Project Structure

```
Research-Paper-Analyzer/
├── app.py              # Main Streamlit application
├── ai_client.py        # Google Gemini API client
├── pdf_utils.py        # PDF text extraction and chunking utilities
├── prompts.py          # AI prompt templates
├── ui_helpers.py       # UI utility functions
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .env                # Environment variables (create this)
├── tests/              # Unit tests
│   ├── test_pdf_utils.py
│   └── test_prompts.py
└── scripts/            # Utility scripts
```

## 🔧 Configuration

Configure the application by setting environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Required |
| `MAX_CHUNK_TOKENS` | Maximum words per chunk | 3000 |
| `CHUNK_OVERLAP` | Overlapping words between chunks | 200 |

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyPDF2
- **AI Model**: Google Gemini Flash (latest)
- **API Client**: Requests
- **Testing**: Pytest
- **Containerization**: Docker

## 📝 How It Works

1. **Text Extraction**: The app extracts text from uploaded PDFs using PyPDF2
2. **Chunking**: Large documents are split into chunks with configurable size and overlap
3. **Individual Summarization**: Each chunk is sent to Gemini AI with a structured prompt
4. **Merging**: Individual summaries are combined and re-summarized for coherence
5. **Display**: The final summary is presented in a clean, readable format

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Known Issues & Limitations

- Scanned PDFs without OCR may not extract text properly
- Very large PDFs (100+ pages) may take several minutes to process
- Summary quality depends on the source paper's clarity and structure

## 💡 Future Enhancements

- [ ] Support for multiple AI models (Claude, GPT-4, etc.)
- [ ] Citation extraction and formatting
- [ ] Figure and table analysis
- [ ] Multi-language support
- [ ] Batch processing for multiple papers
- [ ] Export to various formats (PDF, Word, Markdown)

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for researchers and students**