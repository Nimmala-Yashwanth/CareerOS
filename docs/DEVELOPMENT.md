# Development process — how CareerOS was built

## Phase 1 — Core full-stack application

Built a FastAPI backend with SQLAlchemy models for users, applications and skills; implemented registration, login, JWT-protected application CRUD, pagination/filtering, pipeline analytics and CSV export. Created a plain HTML/CSS/JavaScript interface under `static/`. Added pytest tests, Alembic migrations, GitHub Actions and Docker-related configuration.

## Phase 2 — Resume intelligence

Added `pypdf`-based extraction for text PDFs and two endpoints: `/api/resume/analyze` and `/api/resume/compare`. Implemented explainable regex keyword matching against a fixed skill catalog. Added upload restrictions and clear statements that keyword coverage is not an ATS prediction.

## Phase 3 — React frontend and optional generative AI

Added a React/Vite dashboard, visualizations and frontend flows for resume analysis and feedback. An optional AI feedback endpoint was initially designed for an external API; the locally used project was then upgraded to use Ollama.

## Phase 4 — Free local inference

Installed Ollama on an Apple Silicon Mac, downloaded `llama3.2:3b`, and changed `/api/ai/feedback` to call Ollama's local HTTP API. Kept the model server separate from FastAPI and Vite. The user's terminal logs showed HTTP 200 responses for login, analytics, PDF analysis, resume comparison, CSV export and AI feedback.

## Engineering choices and tradeoffs

- **SQLite** simplifies local development; PostgreSQL is available for a more realistic database deployment.
- **JWT** keeps authenticated requests stateless, but a production system needs further controls such as rate limiting and token revocation.
- **Regex skill matching** is explainable and testable, but it misses semantic equivalence and context.
- **Local LLM** avoids paid inference fees and sends feedback inputs to a local service, but consumes memory and may hallucinate.
- **pypdf** avoids external document services, but cannot read image-only PDFs without OCR.
- **Single-file React UI** enabled quick iteration but should be refactored for maintainability.

## Evidence and known defect

Observed user logs: `/api/auth/login`, `/api/me`, `/api/skills`, `/api/analytics`, `/api/applications`, `/api/export.csv`, `/api/resume/analyze`, `/api/resume/compare` and `/api/ai/feedback` returned HTTP 200. An HTTP 409 for repeated registration is expected when the account exists. The local model once described React and TypeScript as missing even though deterministic matching marked them present. This inconsistency is a known limitation, not a verified matching success.

## Next iterations

Extract React components; add integration/E2E tests; validate AI responses against structured matches; add richer matching; improve documentation screenshots and deployment; test accessibility and security.
