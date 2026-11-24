# PromptGuard

An ML-assisted prompt injection detection API and monitoring dashboard. Built with FastAPI, scikit-learn, SQLite, React/TypeScript, Recharts and Docker.

## Windows quick start

Open PowerShell in the cloned repository. Docker Desktop must be running.

```powershell
git pull
docker run --rm -v "${PWD}:/project" -w /project python:3.12-slim sh -c "pip install -r ml/requirements.txt && python ml/train.py"
if (!(Test-Path .env)) {
    $key = [guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N")
    "PROMPTGUARD_API_KEY=$key" | Set-Content -Encoding ascii .env
}
docker compose up --build
```

Dashboard: http://localhost:3001
API docs: http://localhost:8001/docs

In a separate PowerShell tab in this directory, copy the admin key privately:

```powershell
((Get-Content .env | Where-Object { $_ -like 'PROMPTGUARD_API_KEY=*' }) -replace '^PROMPTGUARD_API_KEY=','') | Set-Clipboard
```

Paste into the dashboard. Do not share the key or commit .env.

## Features

TF-IDF and logistic regression trained on deepset/prompt-injections, rule-assisted detection, latency analytics, and administrator endpoints for creating, listing and revoking hashed API keys. Use X-API-Key for authenticated requests. Admin-only operations require the original environment key.

## Limitations

Binary classifier and heuristic threat labels are not a guarantee of protection. Missing models fail closed. Rule decisions do not claim calibrated confidence. Logs store hashes instead of plaintext prompts; hashes are not anonymization. Evaluate the actual saved model and independently test new attacks before production use. Load only trusted joblib artifacts. Public deployment requires additional security hardening.
