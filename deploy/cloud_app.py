import os
from fastapi.staticfiles import StaticFiles
from app.main import app

if len(os.getenv("PROMPTGUARD_API_KEY", "")) < 32:
    raise RuntimeError("Configure PROMPTGUARD_API_KEY before starting the cloud demo")
app.mount("/", StaticFiles(directory="/srv/static", html=True), name="dashboard")
