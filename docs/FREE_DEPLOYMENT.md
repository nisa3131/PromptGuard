# Render cloud demo deployment

The portfolio demo uses a single Docker image containing FastAPI and the React build. The local Docker Compose setup remains separate.

## Render configuration

| Setting | Value |
|---|---|
| Source | https://github.com/nisa3131/PromptGuard |
| Runtime | Docker |
| Branch | main |
| Root directory | Repository root (leave blank) |
| Instance type | Free, when available |
| Dockerfile path | ./Dockerfile.cloud |
| Docker build context | . |
| Docker command | Leave blank |
| Health check path | /api/v1/health |

Choose only a free instance and review the current [Render free service limits](https://render.com/docs/free). Do not activate paid resources.

## Secrets

Set PROMPTGUARD_API_KEY to at least 32 random characters in Render's Environment section. Enter that private administrator key in the dashboard. Create scoped, revocable integration keys when demonstrating API access.

Never put secret values in source control, screenshots, documentation or a public demo link.

## Verify after deploy

1. Open the public service URL displayed in the Render dashboard.
2. Open /api/v1/health and /docs on the same origin.
3. Analyze a benign prompt and a synthetic instruction override, then refresh analytics. Verify that the response reports model_available=true.
4. The cloud image trains the baseline during build. Model training depends on public dataset availability; do not claim an accuracy figure without actual evaluation results.
5. If the application sleeps, reopen it before an interview and allow it to start. Free service storage is ephemeral: database records, accounts and uploaded documents may reset.

## Interview use

Open the public dashboard in a browser, use synthetic inputs, and keep secrets private. See [the interview guide](INTERVIEW_GUIDE.md). This is a portfolio prototype, not a production service or a comprehensive security guarantee.
