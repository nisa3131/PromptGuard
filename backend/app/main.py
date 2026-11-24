import hashlib
import secrets
import time
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.detector import detect
from app.security import verify_api_key, verify_admin, digest
from app.storage import connection

app = FastAPI(title="PromptGuard", version="0.2.0")

class AnalyzeRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "service": "promptguard"}

@app.post("/api/v1/analyze")
def analyze(payload: AnalyzeRequest, _: str = Depends(verify_api_key)):
    started = time.perf_counter()
    result = detect(payload.prompt)
    elapsed = round((time.perf_counter() - started) * 1000, 2)
    with connection() as db:
        db.execute(
            "INSERT INTO requests (prompt_hash,status,threat_type,latency_ms) VALUES (?,?,?,?)",
            (hashlib.sha256(payload.prompt.encode()).hexdigest(),
             result["status"], result["threat_type"], elapsed)
        )
    return {**result, "latency_ms": elapsed}

@app.get("/api/v1/analytics")
def analytics(_: str = Depends(verify_admin)):
    with connection() as db:
        total, blocked, average = db.execute(
            "SELECT COUNT(*), COALESCE(SUM(status='BLOCKED'),0), COALESCE(AVG(latency_ms),0) FROM requests"
        ).fetchone()
        distribution = db.execute(
            "SELECT threat_type, COUNT(*) FROM requests GROUP BY threat_type"
        ).fetchall()
        recent = db.execute(
            "SELECT id,created_at,status,threat_type,latency_ms FROM requests ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return {"total_requests": total, "blocked_percent": round(100 * blocked / total, 2) if total else 0,
            "average_latency_ms": round(average, 2),
            "threat_distribution": [{"name": name, "value": count} for name,count in distribution],
            "recent_logs": [{"id": i, "created_at": t, "status": s, "threat_type": th, "latency_ms": ms} for i,t,s,th,ms in recent]}

class KeyRequest(BaseModel):
    label: str = Field(min_length=1, max_length=100)

@app.post("/api/v1/api-keys", status_code=201)
def create_key(payload: KeyRequest, _: str = Depends(verify_admin)):
    key = "pg_" + secrets.token_urlsafe(32)
    with connection() as db:
        key_id = db.execute("INSERT INTO api_keys(label,key_hash) VALUES(?,?)",
                            (payload.label, digest(key))).lastrowid
    return {"id":key_id, "label":payload.label, "api_key":key}

@app.get("/api/v1/api-keys")
def list_keys(_: str = Depends(verify_admin)):
    with connection() as db:
        rows = db.execute("SELECT id,label,created_at,revoked FROM api_keys ORDER BY id DESC").fetchall()
    return [{"id":i,"label":label,"created_at":created,"revoked":bool(revoked)} for i,label,created,revoked in rows]

@app.delete("/api/v1/api-keys/{key_id}")
def revoke_key(key_id: int, _: str = Depends(verify_admin)):
    with connection() as db:
        cursor = db.execute("UPDATE api_keys SET revoked=1 WHERE id=?", (key_id,))
        if not cursor.rowcount:
            raise HTTPException(404,"Key not found")
    return {"revoked":True}
