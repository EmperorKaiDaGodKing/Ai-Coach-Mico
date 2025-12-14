"""
Simple persona manager: loads persona, enforces standby and content rules.
Integrate content_filter.check(request_text) to block explicit requests.
"""

import yaml
from pathlib import Path
from .content_filter import check_safe  # implement classifier + regex list

PERSONA_DIR = Path(__file__).parent.parent / "personas"

class PersonaManager:
    def __init__(self, persona_name="sensual"):
        self.persona = self.load_persona(persona_name)
        self.idle = self.persona.get("standby_on_idle", False)

    def load_persona(self, name):
        p = PERSONA_DIR / f"{name}.yaml"
        return yaml.safe_load(p.read_text())

    def request_allowed(self, text, explicit_consent=False):
        # First: run safety check (classifier + blacklist)
        safe, reason = check_safe(text)
        if not safe:
            return False, f"Blocked by content filter: {reason}"

        # If persona requires consent for restricted modes, ensure explicit_consent
        if self.persona.get("consent_required") and not explicit_consent:
            return False, "This persona requires explicit consent to engage in restricted modes."

        # Enforce disallowed keywords from persona metadata (additional layer)
        for k in self.persona.get("disallowed_content", []):
            if k in text.lower():
                return False, f"Disallowed by persona rule: {k}"

        return True, "Allowed"

    def handle_request(self, text, explicit_consent=False):
        # Standby behavior
        if self.idle and not text.strip():
            return {"status":"idle","message":"Standing by. Send a focused request to continue."}

        allowed, msg = self.request_allowed(text, explicit_consent=explicit_consent)
        if not allowed:
            return {"status":"blocked","message":msg}

        # Delegate to response generator (placeholder)
        # Ensure generator is constrained to allowed_content categories
        return {"status":"ok","message":"Generate safe persona response here."}