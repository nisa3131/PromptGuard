import os
import re
from functools import lru_cache
from pathlib import Path
import joblib

PATTERNS = [
    re.compile(r"ignore (all )?(previous|prior|above) instructions", re.I),
    re.compile(r"(reveal|print|show).{0,30}(system prompt|developer instructions)", re.I),
    re.compile(r"(bypass|override).{0,30}(safety|guardrails|restrictions)", re.I),
]

@lru_cache
def load_model():
    path = Path(os.getenv("PROMPTGUARD_MODEL_PATH", "/srv/models/promptguard_baseline.joblib"))
    if not path.exists():
        return None
    # Load only the model artifact produced by our trusted training workflow.
    return joblib.load(path)

def detect(prompt: str) -> dict:
    model = load_model()
    matches = [pattern.pattern for pattern in PATTERNS if pattern.search(prompt)]
    if model is None:
        return {"status": "BLOCKED" if matches else "SAFE",
                "confidence_score": None,
                "threat_type": "Prompt Injection" if matches else "Unknown",
                "model_available": False,
                "matched_rules": matches}
    probability = float(model.predict_proba([prompt])[0][1])
    blocked = bool(matches) or probability >= float(os.getenv("BLOCK_THRESHOLD", "0.7"))
    return {"status": "BLOCKED" if blocked else "SAFE",
            "confidence_score": round(probability if blocked else 1 - probability, 4),
            "threat_type": "Prompt Injection" if blocked else "Benign",
            "model_available": True,
            "matched_rules": matches}
