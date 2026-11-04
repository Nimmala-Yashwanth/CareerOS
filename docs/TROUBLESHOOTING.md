# Troubleshooting — macOS

**`zsh: command not found: npm`**: Install Node.js with `brew install node`; confirm `node -v` and `npm -v`. Run `npm install` **inside `frontend/`**.

**`zsh: command not found: python`**: Activate the virtual environment with `source .venv/bin/activate` from the repository root, then use `python`. Alternatively use `python3.11`.

**`could not connect to ollama server`**: In a separate terminal run `ollama serve` (unless the Ollama app/service is already running). Check `curl http://127.0.0.1:11434/api/tags`.

**Model missing**: Run `ollama pull llama3.2:3b`; then test `ollama run llama3.2:3b` and exit with `/bye`.

**`503` from `/api/ai/feedback`**: Ollama is stopped, the model is missing, or the request timed out. Keep the model service running and check backend logs.

**`409 Conflict` on registration**: The email already exists; use login instead.

**`401 Unauthorized`**: Log in again and ensure the bearer token is sent.

**`422` for PDF**: Use a non-encrypted text PDF, max 2 MB and 12 pages; scanned documents need OCR not currently included.

**Vite cannot reach backend**: Start FastAPI on port 8000 and React on port 5173 in separate terminals. Check `http://127.0.0.1:8000/health`.

**Port already in use**: Stop the other service with Control+C or check running processes. Do not start duplicate Ollama servers.

**AI contradicts matched skills**: This is a known model reliability issue. Trust the deterministic keyword list over unsupported AI assertions and verify all advice.
