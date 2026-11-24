import os
import re
from functools import lru_cache
from pathlib import Path
import joblib

PATTERNS = [
    ("instruction_override", re.compile(r"ignore (all )?(previous|prior|above) instructions", re.I)),
    ("prompt_extraction", re.compile(r"(reveal|print|show).{0,30}(system prompt|developer instructions)", re.I)),
    ("guardrail_bypass", re.compile(r"(bypass|override).{0,30}(safety|guardrails|restrictions)", re.I)),
]

@lru_cache
def load_model():
    path = Path(os.getenv("PROMPTGUARD_MODEL_PATH", "/srv/models/promptguard_baseline.joblib"))
    if not path.exists():
        return None
    return joblib.load(path)

def detect(prompt: str) -> dict:
    model = load_model()
    matches = [name for name, pattern in PATTERNS if pattern.search(prompt)]
    if model is None:
        return {"status": "BLOCKED", "confidence_score": None,
                "threat_type": matches[0] if matches else "model_unavailable",
                "model_available": False, "matched_rules": matches, "decision_source": "rule" if matches else "fail_closed"}
    probability = float(model.predict_proba([prompt])[0][list(model.classes_).index(1)])
    blocked = bool(matches) or probability >= float(os.getenv("BLOCK_THRESHOLD", "0.7"))
    return {"status": "BLOCKED" if blocked else "SAFE",
            "confidence_score": None if matches else round(probability if blocked else 1-probability,4),
            "injection_probability": round(probability,4),
            "threat_type": matches[0] if matches else ("Prompt Injection" if blocked else "Benign"),
            "model_available": True, "matched_rules": matches,
            "decision_source": "rule" if matches else "model"}
