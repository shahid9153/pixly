<div align="center">
<h1>
Pixly - Your AI Gaming Assistant 🎮
</h1>
</div>

Pixly is a desktop gaming assistant that combines AI chat with automated, privacy-friendly screenshot capture and a game-specific Retrieval-Augmented Generation (RAG) knowledge base. Pixly detects what game you’re playing, retrieves relevant, curated knowledge (wikis, user-supplied YouTube descriptions, and forum posts) via a local vector database, and grounds Gemini responses on those sources.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)

- [What Pixly Does](#what-pixly-does)
- [Architecture Overview](#architecture-overview)
  - [1) UI Overlay (`overlay.py`)](#1-ui-overlay-overlaypy)
  - [2) Backend API (`backend/`)](#2-backend-api-backend)
  - [3) AI \& RAG Layer](#3-ai--rag-layer)
- [Knowledge Base \& Data Flow](#knowledge-base--data-flow)
- [Game Detection](#game-detection)
- [API Surface (Selected)](#api-surface-selected)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [How Components Work Together](#how-components-work-together)
- [Security \& Privacy](#security--privacy)
- [Pixly Quick Start Guide](#pixly-quick-start-guide)
  - [📋 Prerequisites](#-prerequisites)
  - [Manual Setup](#manual-setup)
- [License](#license)
- [Acknowledgments](#acknowledgments)




## What Pixly Does

- Intelligent, game-focused chat using Google Gemini with a “Game Expert” system prompt
- Contextual help based on your active game (process detection and/or user message)
- Optional screenshot-powered context for visual analysis
- RAG pipeline over per-game CSV knowledge with local vector search (Chroma)
- Modern desktop overlay for chatting, settings, and screenshot gallery

## Architecture Overview

Pixly is organized into three main layers: UI Overlay, Backend API, and AI/RAG services, all running locally.

### 1) UI Overlay (`overlay.py`)
- CustomTkinter-based floating overlay, always-on-top, draggable
- Chat window with typing indicator and styled messages (user vs assistant)
- Settings window to manage screenshot capture and set the Google API key (persisted to `.env` via backend)
- Screenshot gallery with View and Delete actions

### 2) Backend API (`backend/`)
- FastAPI server exposes HTTP endpoints on 127.0.0.1:8000
- Responsibilities:
  - Route chat requests to Gemini
  - Manage screenshots (start/stop capture, list, view, delete)
  - Detect current game (process + manual keywords)
  - Manage per-game knowledge ingestion and vectorization
  - Provide vector search and knowledge stats
  - Manage API key configuration (.env persistence + live reconfigure)

Key modules:
- `backend/backend.py`: API endpoints and routing
- `backend/chatbot.py`: Gemini client configuration, runtime reconfigure, and chat logic (with RAG context injection)
- `backend/screenshot.py`: Encrypted screenshot capture and storage; database operations; delete support
- `backend/game_detection.py`: Game detection via running processes, recent screenshots, and user message keywords
- `backend/knowledge_manager.py`: CSV ingestion and text extraction (wiki + forum; YouTube entries use user-provided description)
- `backend/vector_service.py`: Chroma persistent client, collection management, chunking, embeddings, and semantic queries

### 3) AI & RAG Layer
- Model: `Google Gemini 2.5 Flash Lite` for responses
- System prompt (`PROMPTS.txt`) defines "Game Expert" persona and instructs grounding answers in retrieved snippets (WIKI / YOUTUBE / FORUM) with URLs
- Vector DB: `Chroma` (persistent on disk in `vector_db/`)
- Embeddings: sentence-transformers by default (configurable); text is chunked and embedded per content piece
- Retrieval: top-k relevant chunks by cosine similarity; included as context in the prompt

## Knowledge Base & Data Flow

Pixly’s knowledge is curated per game via CSV files that live in `games_info/`. The CSV schema is simple and contributor-friendly:

```
wiki,wiki_desc,youtube,yt_desc,forum,forum_desc
```

- **wiki**: URL to a relevant wiki page; Pixly extracts textual content
- **wiki_desc**: Contributor-provided description of the wiki URL
- **youtube**: URL to a relevant video; Pixly does not auto-transcribe; it uses the contributor-provided description
- **yt_desc**: Contributor-provided description of the YouTube URL
- **forum**: URL to a relevant forum/thread; Pixly extracts textual content
- **forum_desc**: Contributor-provided description of the forum URL

Processing pipeline per game:
1. Load CSV for the game (e.g., `games_info/minecraft.csv`)
2. Extract text from wiki and forum URLs; keep YouTube descriptions as-is
3. Clean and chunk text into manageable segments (e.g., ~512 tokens)
4. Generate embeddings for each chunk and persist into Chroma collections
5. On chat, detect game and run a semantic search to retrieve top snippets, then ground Gemini’s response on those

Vector DB collections are organized by game and source type, e.g. `minecraft_wiki`, `minecraft_youtube`, `minecraft_forum`.

## Game Detection

Pixly uses a layered strategy to infer the current game:
- **Process Detection**: Scans running processes for known executables
- **Screenshot Context**: Uses recent screenshot metadata (app/window) when available
- **Manual Override**: Detects game mentions in the user’s message (e.g., “I’m playing Minecraft”)

The detection result is passed into the RAG layer to scope retrieval to the active game’s knowledge base.

## API Surface (Selected)

- `POST /chat`: Chat with Gemini; auto-detects game; augments prompt with retrieved snippets
- `POST /screenshots/start?interval=30`: Start periodic capture
- `POST /screenshots/stop`: Stop capture
- `GET /screenshots/recent?limit=10&application=...`: List recent screenshots (metadata)
- `GET /screenshots/{id}`: Fetch a screenshot’s image data (base64)
- `DELETE /screenshots/{id}`: Delete a screenshot entry
- `POST /games/detect`: Detect current game (optionally pass message for keyword hints)
- `GET /games/list`: Enumerate detection-supported games, CSV-available games, and games with vectors
- `GET /games/{game}/knowledge/validate`: Validate CSV schema
- `POST /games/{game}/knowledge/process`: Ingest CSV and build vectors in Chroma
- `POST /games/{game}/knowledge/search`: Vector search within a game (query, content_types, limit)
- `GET /games/{game}/knowledge/stats`: Document counts per source type
- `GET /settings/api-key`: Report whether the Gemini API key is configured (masked preview)
- `POST /settings/api-key`: Persist API key to `.env` and live-reconfigure the chatbot

## Project Structure

```
Hacktober Fest/
├── backend/
│   ├── __init__.py               # FastAPI app initialization
│   ├── backend.py                # API endpoints and routing
│   ├── chatbot.py                # Gemini integration, RAG-aware chat, runtime reconfigure
│   ├── screenshot.py             # Encrypted screenshot capture, DB ops, delete support
│   ├── game_detection.py         # Process/message/screenshot-based game detection
│   ├── knowledge_manager.py      # CSV ingestion and content extraction (wiki/forum)
│   └── vector_service.py         # Chroma collections, embeddings, and search
├── overlay.py                    # CustomTkinter overlay (chat, settings, screenshot viewer)
├── games_info/                   # Per-game CSVs (e.g., minecraft.csv)
├── vector_db/                    # Chroma persistent storage
├── PROMPTS.txt                   # System persona + RAG grounding instructions
├── test_system.py                # Local API test harness
├── run.py                        # Backend server launcher
├── pyproject.toml                # Dependencies and metadata
├── screenshots.db                # Encrypted screenshot database (auto-created)
├── screenshot_key.key            # Encryption key (auto-generated)
└── README.md                     # Project documentation
```

## Technology Stack

- **UI/Frontend**: CustomTkinter (modern theming and widgets for Python GUIs)
- **API/Backend**: FastAPI (async Python web framework) + Uvicorn (ASGI server)
- **AI**: Google Gemini 2.5 Flash Lite via `google-generativeai`
- **RAG**: Chroma (persistent local vector DB) + sentence-transformers (embeddings)
- **Data**: CSV-based per-game knowledge; SQLite for screenshots; Fernet for encryption
- **System**: psutil + pywin32 for Windows process/window info; Pillow for imaging

Notes:
- The embedding model is configurable; by default we use a sentence-transformers model suitable for local inference. The system can be switched to a different embedder (e.g., Mistral embeddings) with minor changes in `vector_service.py`.
- The persona and grounding behavior are controlled by `PROMPTS.txt` so Gemini cites sources from retrieved snippets and focuses answers on gaming topics.

## How Components Work Together

1. The overlay sends chat requests to the backend.
2. The backend detects the current game and queries Chroma for relevant snippets (wiki, YouTube description, forum).
3. Retrieved snippets are added to the prompt to ground Gemini’s response.
4. If a screenshot is provided, it’s included as a multimodal input to Gemini for visual context.
5. The overlay displays a typing indicator while waiting and distinguishes user vs assistant messages for readability.

## Security & Privacy

- Local-first design: screenshots, vectors, and CSVs are stored on your machine
- Encrypted screenshot blobs at rest using Fernet (AES)
- API key managed locally via the settings UI and `.env` persistence
- No telemetry or external data collection

## Pixly Quick Start Guide 


### 📋 Prerequisites
<div>

<table>
<tr>
<td align="center" width="25%">

**🐍 Python 3.11+**
```bash
python --version
```

</td>
<td align="center" width="25%">

**🪟 Windows 10/11**
```bash
node --version
```

</td>
<td align="center" width="25%">

**⚡ uv Package Manager**

```bash
pip install uv
```
</td>

<td align="center" width="25%">

**🔧 Git**
```bash
git --version
```

</td>
</tr>
</table>
</div>

### Manual Setup 
1. Clone the repository : 
```bash 
git clone https://github.com/BrataBuilds/hacktoberfest
cd hacktoberfest
```
2. Install uv package manager 
```bash 
pip install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```
3. Install dependencies 
```bash
uv sync
```
4. Set up environment variables : 
   1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   2. Create a new API key
   3. Add to `.env`:
```bash
GEMINI_API_KEY=your_gemini_key_here
```

1. Make a folder called `vector_db`

2. Start the application, Create two powershell terminals 

Terminal 1 - Start Backend:
```bash
uv run run.py
```
EWait for the backend to start then in Terminal 2 - Start Frontend:
```bash 
uv run overlay.py
```

## License

MIT License — see [LICENSE](LICENSE).

## Acknowledgments

- Google Gemini for AI capabilities
- CustomTkinter for modern GUI components
- FastAPI for a robust backend framework
- The Hacktoberfest community for open-source collaboration