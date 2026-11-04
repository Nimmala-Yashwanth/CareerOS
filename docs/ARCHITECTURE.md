# System architecture

## Components

1. **React/Vite frontend** (`frontend/src/main.jsx`, `style.css`) renders login, job tracking, analytics, resume upload and feedback. Vite proxies `/api` to FastAPI at port 8000.
2. **FastAPI service** (`app/main.py`) implements REST endpoints and orchestrates SQLAlchemy, resume processing, matching and Ollama calls.
3. **SQLAlchemy models** (`app/models.py`) define users, job applications and user skills. SQLite is the local default; PostgreSQL is supported through configuration and Docker Compose.
4. **Security** (`app/security.py`) handles password hashing and JWT authentication. Protected routes obtain the current user and enforce record ownership.
5. **Matching engine** (`app/matching.py`) uses regular expressions over a fixed catalog. `score = round(100 * matched / detected)` if any job skills are detected; otherwise score is null.
6. **PDF extraction** (`pypdf` in `app/main.py`) reads text PDFs into memory and extracts detected skills. Files over 2 MB or 12 pages are rejected.
7. **Ollama** (`POST /api/ai/feedback`) sends structured job description and skill lists to the local `llama3.2:3b` model via `/api/chat` at `127.0.0.1:11434`.

## Data flow: resume comparison

```text
Upload PDF + job description
 -> POST /api/resume/compare (JWT required)
 -> PDF validation and text extraction
 -> detect resume skill phrases
 -> detect job description skill phrases
 -> compute matched, missing and keyword coverage
 -> return structured JSON
 -> optional POST /api/ai/feedback
 -> Ollama response displayed in UI
```

## Data model

- `User`: id, email, password hash, created timestamp
- `Application`: id, user_id, company, role, status, location, job URL, description, notes, timestamps
- `Skill`: id, user_id, name; unique per user/name

One user owns many applications and skills. Uploaded resumes are not persisted.

## Trust boundaries and limitations

The browser is untrusted; protected API endpoints require bearer tokens. Job descriptions are untrusted input to the LLM; system instructions request that embedded instructions be ignored, but this is not a formal guarantee. AI outputs must be verified. This is a local development architecture; production deployment requires additional security review and service orchestration.
