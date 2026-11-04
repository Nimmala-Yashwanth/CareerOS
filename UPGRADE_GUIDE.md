# CareerOS v2 upgrade guide

## What changed
- Refreshed the existing responsive dashboard and added application-stage bar charts.
- Added authenticated PDF resume parsing and job-description gap analysis.
- Added input limits and in-memory PDF processing; uploaded files are not saved.
- Fixed the empty-status filter error in the original frontend.
- Preserved the existing database models and API routes; no database migration is required.

**Important:** This version does **not** use an LLM, semantic embeddings, React, or Next.js. The resume matcher is transparent keyword matching. It does not estimate a real ATS score. Scanned PDFs require OCR and are not supported.

## Upgrade your existing Mac project
1. Stop Uvicorn with Control+C.
2. Back up your existing `careeros_pro` folder, especially its SQLite database and `.env` file.
3. Copy the new `app/main.py`, `static/index.html`, `requirements.txt` and `tests/test_resume.py` into the matching paths of your existing project. Do not delete your existing database.
4. Activate your Python 3.11 venv and run `python -m pip install -r requirements-dev.txt`.
5. Run `python -m pytest -q`.
6. Run `uvicorn app.main:app --reload` and open http://127.0.0.1:8000.

## Fresh install
`python3.11 -m venv .venv && source .venv/bin/activate`
`python -m pip install -r requirements-dev.txt`
`python -m pytest -q`
`uvicorn app.main:app --reload`

For resume comparisons, choose a PDF and paste a job description (20+ characters). Without a job description, the app only extracts resume skills.
