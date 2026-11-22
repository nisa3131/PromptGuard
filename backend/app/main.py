import hashlib
import time
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from app.detector import detect
from app.security import verify_api_key
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
def analytics(_: str = Depends(verify_api_key)):
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
