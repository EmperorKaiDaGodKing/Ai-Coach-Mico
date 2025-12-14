"""
Lightweight content filter for Ai-Coach-Mico.

Provides check_safe(text) -> (bool, reason). Uses a small blacklist (regex)
and optionally calls an external moderation endpoint if configured in
nsfw_config.yaml. External calls are optional and fail-safe.

Dependencies: pyyaml (only to read config). Uses 'requests' only if available.
"""
import re
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

# Compact blacklist of explicit/sexual terms (kept conservative and obvious).
BLACKLIST = [
    "sex", "sexual", "porn", "pornography", "fuck", "fucking", "cock", "dick",
    "cum", "orgasm", "masturbat", "anal", "oral", "hardcore", "bdsm", "pornographic",
    "explicit", "penetrat", "strip", "escort"
]
BLACKLIST_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in BLACKLIST) + r")\b", re.IGNORECASE)

def _load_config():
    cfg_path = Path.cwd() / "nsfw_config.yaml"
    if not cfg_path.exists() or yaml is None:
        return {}
    try:
        return yaml.safe_load(cfg_path.read_text())
    except Exception:
        return {}

def _call_moderation(endpoint: str, text: str):
    # Optional external moderation call; returns (allowed:bool, reason:str)
    try:
        import requests
    except Exception:
        return True, "requests unavailable; skipping moderation"

    try:
        payload = {"text": text}
        resp = requests.post(endpoint, json=payload, timeout=3)
        if resp.status_code != 200:
            return True, f"moderation_unavailable_status:{resp.status_code}"
        data = resp.json()
        # Expecting a JSON response with something like {"allow": true/false, "reason": "..."}
        if isinstance(data, dict):
            allow = data.get("allow", True)
            reason = data.get("reason", "external_moderation")
            return bool(allow), reason
        return True, "unexpected_moderation_response"
    except Exception as e:
        return True, f"moderation_error:{e}"

def check_safe(text: str):
    """
    Return (allowed: bool, reason: str).
    - If blacklist matched -> (False, 'blacklist: <term>')
    - Else, if moderation endpoint configured -> query it (optional)
    - Else -> (True, 'ok')
    """
    if not text:
        return True, "ok"

    # Check blacklist
    m = BLACKLIST_RE.search(text)
    if m:
        return False, f"blacklist:{m.group(0)}"

    # Optional external moderation
    cfg = _load_config()
    endpoint = (
        cfg.get("private_adult_mode", {}) or {}
    ).get("moderation_endpoint")
    if endpoint:
        allowed, reason = _call_moderation(endpoint, text)
        if not allowed:
            return False, f"external_moderation:{reason}"

    return True, "ok"