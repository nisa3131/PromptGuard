import hashlib
import hmac
import os
from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str | None = Header(default=None)) -> str:
    configured = os.getenv("PROMPTGUARD_API_KEY", "")
    if not configured:
        raise HTTPException(status_code=503, detail="API key is not configured")
    if not x_api_key or not hmac.compare_digest(
        hashlib.sha256(x_api_key.encode()).digest(),
        hashlib.sha256(configured.encode()).digest(),
    ):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return "default"
