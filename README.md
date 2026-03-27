# 🎓 Lecture AI: Automated Lecture Understanding & Note Generation

A production-level system designed to turn audio lectures (MP3/WAV) into highly structured, academic-grade notes using OpenAI Whisper and advanced LLMs.

---

## 🚀 Key Features

*   **Speech-to-Text**: High-accuracy transcription using OpenAI Whisper.
*   **Transcript Cleaning**: Automatically removes filler words (uh, um, you know) and fixes formatting.
*   **Academic Summarization**: Generates deep, structured notes with key concepts, definitions, and logical flow.
*   **Dual-Model Backend**: Supports both OpenAI (GPT-4o-mini) for premium quality and HuggingFace (BART-Large-CNN) for local offline use.
*   **User-Friendly Dashboard**: Minimalist modern UI for file uploading, editing transcripts, and downloading notes.
*   **Automation-Ready**: Optional n8n workflow for seamless integration with other tools.

---

## 📁 Project Structure

```text
lecture-ai-project/
├── backend/
│   ├── main.py             # FastAPI entry point
│   ├── services/
│   │   ├── whisper_service.py # Audio transcription logic
│   │   └── nlp_service.py     # AI Note generation logic
│   ├── utils/
│   │   └── text_processor.py  # Text cleaning & filler removal
│   └── models/             # Local model storage (if needed)
├── frontend/
│   ├── index.html          # Modern UI
│   ├── style.css           # Custom styling
│   └── script.js           # Frontend logic & API calls
├── data/
│   ├── uploads/            # Temporary storage for audio files
│   └── outputs/            # Storage for generated transcripts/notes
├── n8n/
│   └── workflow.json       # n8n automation template
├── notebooks/              # Exploration scripts (optional)
├── requirements.txt        # Full dependencies list
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Prerequisities

*   Python 3.9+
*   FFmpeg (Required for audio processing):
    *   **Windows**: `choco install ffmpeg` or download binaries from `ffmpeg.org`.
    *   **MacOS**: `brew install ffmpeg`
    *   **Linux**: `sudo apt install ffmpeg`

### 2. Backend Setup

1.  Navigate to the `backend/` directory.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  *(Optional)* Create a `.env` file for OpenAI quality:
    ```env
    OPENAI_API_KEY=your_key_here
    ```
4.  Run the backend server:
    ```bash
    python main.py
    ```
    The API will be available at `http://localhost:8000`.

### 3. Frontend Setup

1.  Simply open `frontend/index.html` in any modern browser.
2.  Alternatively, use a Live Server (VS Code) to avoid CORS issues.

---

## 🧪 Testing & Usage

### Method A: Browser UI (Recommended)
1.  Open `index.html`.
2.  Upload an audio lecture (WAV/MP3).
3.  Click **"Transcribe Audio"**.
4.  Review the transcript, then click **"Generate Academic Notes"**.
5.  **Download** your structured notes.

### Method B: API (cURL)
Transcribe an audio file:
```bash
curl -F "file=@lecture.mp3" http://localhost:8000/transcribe
```

Generate notes from text:
```bash
curl -d "text=Lectures about quantum..." http://localhost:8000/generate-notes
```

---

## 🤖 NLP Output Format

The system strictly enforces this structured academic format:

📘 **Title**: [Generated Topic Title]

📌 **Key Points**:
1.  **[Concept Title]**: [Deep academic explanation of the concept...]
2.  **[Relationship]**: [How this relates to previous theories...]
3.  ...

---

## ✨ Future Improvements

*   **Multi-language support**: Whisper already supports it; just enable it in `whisper_service.py`.
*   **Vector Database (RAG)**: Store notes in Pinecone/Chroma for semantic search across all your lectures.
*   **Speaker Diarization**: Identify who is speaking (Lecturer vs. Student).
*   **Topic Clusters**: Automatically categorize lectures into subjects (Math, History, etc.).

---

## 📝 License
MIT License. Built for Education & Open Science.
