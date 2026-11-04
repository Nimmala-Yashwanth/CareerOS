# API reference

All `/api/*` endpoints except register and login require a JWT bearer token.

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Create account; returns access token |
| POST | `/api/auth/login` | Authenticate; returns access token |
| GET | `/api/me` | Current account |
| POST | `/api/applications` | Create application |
| GET | `/api/applications` | List; `status`, `search`, `limit`, `offset` |
| GET | `/api/applications/{id}` | Get one owned application |
| PATCH | `/api/applications/{id}` | Update owned application |
| DELETE | `/api/applications/{id}` | Delete owned application |
| GET | `/api/analytics` | Pipeline counts and metrics |
| GET | `/api/skills` | List user skills |
| PUT | `/api/skills` | Replace user skills |
| POST | `/api/match` | Match saved skills to job description |
| GET | `/api/export.csv` | Download CSV |
| POST | `/api/resume/analyze` | Multipart PDF `file` |
| POST | `/api/resume/compare` | Multipart `file` and `job_description` |
| POST | `/api/ai/feedback` | Local Ollama feedback from description + skill lists |
| GET | `/health` | Health check |

## Example: authentication

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.com","password":"a-long-test-password"}'
```

Use the returned `access_token` in `Authorization: Bearer <token>` for protected calls. Do not commit real tokens.

## Example: AI request body

```json
{
  "job_description": "Seeking Python and Docker experience for a backend role.",
  "matched": ["python"],
  "missing": ["docker"]
}
```

Returns a `feedback` string and `method`. Requires Ollama to be running with the configured model. For exact schemas, validation and live examples, use **http://127.0.0.1:8000/docs**.
