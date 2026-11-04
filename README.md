# CareerOS — AI-Powered Job Application Tracker

**React + Vite | FastAPI | SQLAlchemy + SQLite | Ollama + Llama 3.2**

CareerOS is a local-first, full-stack portfolio application for tracking job applications, reviewing pipeline analytics, extracting text from PDF resumes, comparing explicitly mentioned technical skills with job descriptions, and requesting optional AI-generated feedback from a local LLM.

> **Status:** Working local prototype. The skill score is **keyword coverage, not an ATS score**. LLM feedback can be inaccurate. Do not claim a deployed production service or measured accuracy.

## Features

- Account registration and login with hashed passwords and JWT bearer tokens
- User-scoped application CRUD, search, status filters and pagination
- Application pipeline statistics and CSV export
- User-managed skill profile and transparent keyword matching
- PDF resume extraction (text PDFs; maximum 2 MB and 12 pages)
- Resume-to-job comparison and local AI feedback through Ollama
- OpenAPI documentation at `/docs`, automated backend tests and migration scaffolding

## Architecture

```text
Browser (React/Vite, :5173)
      | /api proxy
      v
FastAPI REST API (:8000)
      |--- SQLAlchemy ---> SQLite (local development)
      |--- pypdf + matching.py ---> skill comparison
      `--- HTTP /api/chat ---> Ollama (:11434) ---> llama3.2:3b
```

## Requirements

- macOS/Linux or compatible environment
- Python 3.11+ (tested by the project owner with Python 3.11)
- Node.js and npm
- Ollama and enough memory/disk space for `llama3.2:3b`

## Quick start — macOS (three terminal windows)

Clone or download the repository and open its root folder. Run the following **once**:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cd frontend && npm install && cd ..
ollama pull llama3.2:3b
```

If `python3.11` is missing on a Homebrew Mac, install it using `brew install python@3.11`. Install Node with `brew install node` and Ollama with `brew install ollama` if necessary.

**Terminal 1 — Ollama** (skip `ollama serve` if the Ollama app/service is already running):

```bash
ollama serve
```

**Terminal 2 — FastAPI**, from the project root:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 — React**, from the project root:

```bash
cd frontend
npm run dev
```

Open **http://127.0.0.1:5173**. The backend API documentation is at **http://127.0.0.1:8000/docs**. Register an account (password minimum 10 characters) or sign in to an existing one.

> The local model is optional for all features except AI feedback. Ollama runs separately from FastAPI and Vite. Never run two copies of `ollama serve` on the same port.

## Tests

```bash
source .venv/bin/activate
python -m pytest -q
python -m compileall -q app
cd frontend && npm run build
```

The repository includes backend tests; this package was prepared from the project source, not validated on your specific Mac. Re-run tests before publishing.

## Project structure

```text
app/                 FastAPI routes, auth, ORM, validation and keyword matcher
frontend/            React/Vite UI and CSS
static/              Earlier plain-HTML frontend (legacy)
tests/               pytest tests
migrations/          Alembic migration setup
.github/workflows/   CI configuration
docs/                Architecture, development, API, troubleshooting, report
requirements*.txt    Python dependencies
Dockerfile           Backend container recipe
docker-compose.yml   PostgreSQL/backend development stack
.env.example         Example environment settings
```

## Important limitations

- The skill matcher checks explicit phrases in a fixed catalog. It does not understand synonyms, assess proficiency, or distinguish required from preferred skills reliably.
- LLM advice is generated from job description and matched/missing skill lists, **not from the full resume text**; it may contradict the matcher.
- Resume uploads are processed in memory, not stored as PDF files.
- Text-only PDF extraction does not OCR scanned resumes.
- Docker Compose covers the backend/database; the React dev server and local Ollama are separate. The Ollama endpoint is local and not automatically available inside Docker.
- This is a development prototype, not a security-hardened production service.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Development process](docs/DEVELOPMENT.md)
- [API reference](docs/API_REFERENCE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Project report (PDF)](docs/PROJECT_REPORT.pdf)

## Security and privacy

Do not commit `.env`, SQLite databases, virtual environments, `node_modules`, private resumes, or API secrets. Use a strong `JWT_SECRET` outside local testing. See `.gitignore`.

## Future work

Refactor the React UI into reusable components; improve contextual skill extraction and required/preferred classification; validate AI feedback against deterministic matches; add frontend tests, security hardening, and a reproducible production deployment.
