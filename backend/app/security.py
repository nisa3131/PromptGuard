import hashlib
import hmac
import os
from fastapi import Header, HTTPException
from app.storage import connection

def digest(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

def verify_admin(x_api_key: str | None = Header(default=None)) -> str:
    configured = os.getenv("PROMPTGUARD_API_KEY", "")
    if not configured:
        raise HTTPException(503, "API key is not configured")
    if not x_api_key or not hmac.compare_digest(digest(x_api_key), digest(configured)):
        raise HTTPException(401, "Admin key required")
    return "admin"

def verify_api_key(x_api_key: str | None = Header(default=None)) -> str:
    if not x_api_key:
        raise HTTPException(401, "Invalid API key")
    configured = os.getenv("PROMPTGUARD_API_KEY", "")
    if configured and hmac.compare_digest(digest(x_api_key), digest(configured)):
        return "admin"
    with connection() as db:
        row = db.execute("SELECT id FROM api_keys WHERE key_hash=? AND revoked=0",
                         (digest(x_api_key),)).fetchone()
    if row is None:
        raise HTTPException(401, "Invalid API key")
    return str(row[0])
