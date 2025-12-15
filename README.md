# AI-Agent

A multi-modal AI assistant implemented in Python. This repository combines chat, memory, document Q&A, web scraping, vector search (FAISS), and voice I/O, and includes both CLI and Streamlit UI components.

This README was written from the repository layout and commit history. It documents features, installation guidance, usage examples, configuration, and troubleshooting to help you get started.

---

## Table of Contents

- Project overview
- Features
- Repository structure
- Requirements
- Quickstart
- Configuration / environment variables
- Usage examples
  - CLI chat
  - Streamlit UI (chat + voice UI)
  - Voice assistant (microphone + TTS)
  - Web scraping + FAISS retrieval
  - PDF/document reader (summarize + Q&A)
- How it works (architecture & data flow)
- Troubleshooting & tips
- Suggested improvements
- Contributing
- License

---

## Project overview

AI-Agent is a modular Python toolkit that provides:
- Conversational AI with memory and prompt templates.
- CLI and Streamlit-based UI for interactive chat.
- Voice assistant supporting speech recognition (STT) and text-to-speech (TTS).
- Web scraping pipeline with vector indexing (FAISS) for retrieval-augmented generation (RAG).
- Document (PDF) ingestion, summarization, and Q&A.

The project is flexible: it can use local or hosted LLMs (commit history references a model update to `llama3.2:1b`) and uses FAISS for vector retrieval.

---

## Features

- Interactive chat agent with memory (short/long term context).
- CLI chatbot mode for terminal-based use.
- Streamlit UI to run a web interface for chat and voice.
- Voice assistant:
  - Microphone input (speech-to-text).
  - TTS output with engine reinitialization and error handling.
- Web scraper to fetch webpages and turn content into retrievable chunks.
- FAISS vector store integration for semantic search and RAG.
- Document reader that:
  - Parses PDFs
  - Performs chunking & embedding
  - Offers summarization and Q&A capabilities

---

## Repository structure

(Descriptions based on file names and commit history)

- `basic_ai_agent.py`  
  Main chat agent core (prompt templates, memory, LLM integration). Entrypoint for the conversational logic.

- `ai_voice_assistant.py`  
  Voice assistant backend: STT, TTS, input/output handling, and memory integration.

- `ai_voice_assistant_ui.py`  
  Streamlit-based UI for the voice assistant (and possibly chat UI). Designed to run with `streamlit run`.

- `ai_web_scraper.py`  
  Web scraping utilities to fetch and parse webpages into text chunks.

- `ai_web_scraper_faiss.py`  
  Web scraping + FAISS indexing pipeline (embedding creation, index persistence, retrieval).

- `ai_document_reader.py`  
  PDF/document ingestion, chunking, summarization, and Q&A capabilities.

- `README.md`  
  This file.

Note: Add `requirements.txt`, `.env.example`, Dockerfiles, or CI configs as needed.

---

## Requirements

- Python 3.9+ (3.10+ recommended)
- Recommended system resources:
  - For hosted LLM usage: any modern machine with network access.
  - For local LLMs (e.g., large llama-style models): GPU with enough VRAM or a proper inference runtime.
- Typical Python libraries used by this project (create `requirements.txt` from these as appropriate):
  - langchain
  - transformers
  - sentence-transformers
  - faiss-cpu (or faiss-gpu)
  - streamlit
  - requests
  - beautifulsoup4
  - pdfplumber or PyMuPDF (fitz) or PyPDF2
  - speech_recognition
  - pyttsx3 or gTTS
  - pyaudio or sounddevice
  - python-dotenv
  - tqdm

Install dependencies (example):
```bash
python -m pip install -r requirements.txt
```
If `requirements.txt` is not present, create it and include the packages above with pinned versions.

---

## Quickstart

1. Clone the repo:
```bash
git clone https://github.com/Nirasha20/AI-Agent.git
cd AI-Agent
```

2. Create & activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file to hold configuration (see Configuration section).

5. Run the component you want:
- CLI chat (example):
  ```bash
  python basic_ai_agent.py
  ```
- Streamlit UI:
  ```bash
  streamlit run ai_voice_assistant_ui.py
  ```
- Voice assistant:
  ```bash
  python ai_voice_assistant.py
  ```
- Web scraper + FAISS pipeline:
  ```bash
  python ai_web_scraper_faiss.py --url "https://example.com"
  ```
- Document reader:
  ```bash
  python ai_document_reader.py --pdf path/to/document.pdf
  ```

Commands above assume these scripts expose a runnable CLI; if not, inspect each script for entry points and adapt commands.

---

## Configuration / environment variables

Create a `.env` (or export env vars) with values used by the code. Typical variables to include:

- Model & API keys
  - OPENAI_API_KEY=your_openai_key_here
  - HUGGINGFACE_API_KEY=your_hf_key_here
  - LLAMA_ENDPOINT=grpc_or_http_endpoint_for_llama_if_used
  - LLM_PROVIDER=provider_name_or_local_flag

- Embeddings & vector store
  - EMBEDDINGS_MODEL_NAME=sentence-transformers/...
  - FAISS_INDEX_PATH=./faiss_index.index

- Other
  - PERSIST_DIR=./data
  - LOG_LEVEL=info

Note: Check the source files for exact variable names the code expects (search `os.getenv(` or `.env` usage).

---

## Usage examples

The repository includes several runnable scripts. Example usage patterns follow; adjust to the actual CLI flags and function names in the source.

CLI chat (basic):
```bash
python basic_ai_agent.py --mode cli --memory enabled
```

Streamlit UI (chat + voice):
```bash
streamlit run ai_voice_assistant_ui.py
# Then open the Streamlit URL shown in the terminal (usually http://localhost:8501)
```

Voice assistant (microphone input & TTS output):
```bash
python ai_voice_assistant.py --listen --speak
```

Web scraping + FAISS index:
```bash
python ai_web_scraper_faiss.py --url "https://example.com" --index ./faiss_index
# Use subsequent script to query index for Q&A
```

Document reader (PDF):
```bash
python ai_document_reader.py --pdf path/to/doc.pdf --action summarize
python ai_document_reader.py --pdf path/to/doc.pdf --action qa --question "What is the main idea?"
```

Replace flags above with the actual flags used in each file. Inspect each script top-level help or code for exact usage.

---

## How it works (architecture & data flow)

1. Input
   - Text via CLI or Streamlit UI
   - Voice via microphone (converted to text via STT)
   - Documents (PDFs) or web pages for ingestion

2. Ingestion & preprocessing
   - Text is normalized and chunked into manageable segments
   - PDFs/webpages are parsed and converted to text
   - Chunks are embedded using an embeddings model

3. Storage / retrieval
   - Embeddings are stored in a FAISS vector index (local)
   - For a query, similar chunks are retrieved by nearest-neighbor search

4. Prompt composition
   - Retrieval results are injected into a prompt template with memory/context
   - The assembled prompt is sent to the LLM

5. Output
   - LLM text response is returned to the user
   - If voice enabled, response is converted to audio via TTS

---

## Troubleshooting & tips

- Audio device issues:
  - Ensure microphone drivers are installed and accessible.
  - On Windows, installing `PyAudio` may require prebuilt wheels or use `sounddevice`.
  - If STT fails or is noisy, increase `pause_threshold` or use platform-specific enhancements.

- TTS issues:
  - `pyttsx3` works offline but may require platform-specific backends; `gTTS` requires network access.
  - Reinitialize the TTS engine on errors (the repository includes improved error handling for this).

- FAISS:
  - Use `faiss-cpu` for CPU-only setups; `faiss-gpu` for GPU acceleration.
  - Save & load indices using the configured `FAISS_INDEX_PATH` or persistence directory.

- Local LLMs:
  - Large models require GPU and specialized runtimes. If using hosted models or APIs, set endpoint and API keys accordingly.

- Missing requirements:
  - If a `requirements.txt` is not present, create one using `pip freeze` after installing working versions of dependencies.

---

## Suggested improvements

- Add `requirements.txt` or `pyproject.toml` with pinned dependency versions.
- Add `.env.example` with all configuration keys shown.
- Provide sample config files for selecting between local vs hosted LLMs.
- Add clear CLI help messages for each script (using `argparse` or `click`).
- Add unit tests for ingestion, embedding, FAISS indexing, and TTS.
- Add a Dockerfile to standardize runtime environment.
- Add a more detailed README section with screenshots of the Streamlit UI.

---

## Contributing

Contributions are welcome. Suggested workflow:
1. Fork the repo and create a feature branch.
2. Add tests and documentation for your changes.
3. Open a pull request describing your changes.

Please include a short description of your change and reference any relevant issues.

---

## License

No license is specified in the repository metadata. If you are the repository owner, consider adding an OSI-approved license (e.g., MIT, Apache-2.0) to clarify usage rights.

---

## Acknowledgements

This project leverages common open-source building blocks for RAG systems, speech, document parsing, and UI. If you reuse any third-party models or libraries, please follow their licensing and attribution requirements.
