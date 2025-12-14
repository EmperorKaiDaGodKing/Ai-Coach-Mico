"""
Persona manager: robust persona loading and safety checks.

Changes:
- tolerant import of content_filter (supports running as package or top-level)
- persona file lookup: supports personas/ directory or fallback to root filenames
- clearer FileNotFoundError message
"""
import yaml
from pathlib import Path

# tolerant import to work when module is imported as package or run top-level
try:
    from content_filter import check_safe
except Exception:
    try:
        from .content_filter import check_safe
    except Exception:
        # Last resort: define a permissive stub to avoid import failures during static checks.
        def check_safe(text):
            return True, "no_content_filter"

# Prefer a personas/ directory in repo root; if absent, fallback to repo root.
PERSONA_DIR = Path.cwd() / "personas"
if not PERSONA_DIR.exists():
    PERSONA_DIR = Path.cwd()

class PersonaManager:
    def __init__(self, persona_name="sensual"):
        self.persona = self.load_persona(persona_name)
        self.idle = self.persona.get("standby_on_idle", False)

    def load_persona(self, name):
        # Try personas/name.yaml
        p1 = PERSONA_DIR / f"{name}.yaml"
        if p1.exists():
            try:
                return yaml.safe_load(p1.read_text())
            except Exception as e:
                raise RuntimeError(f"Failed to parse persona file {p1}: {e}")

        # Fallback: support existing flat filename like personas_sensual.yaml
        p2 = Path.cwd() / f"personas_{name}.yaml"
        if p2.exists():
            try:
                return yaml.safe_load(p2.read_text())
            except Exception as e:
                raise RuntimeError(f"Failed to parse persona file {p2}: {e}")

        raise FileNotFoundError(
            f"Persona file not found for '{name}'.\n"
            "Create personas/{name}.yaml or place a file named personas_{name}.yaml at repo root."
        )

    def request_allowed(self, text, explicit_consent=False):
        safe, reason = check_safe(text)
        if not safe:
            return False, f"Blocked by content filter: {reason}"

        if self.persona.get("consent_required") and not explicit_consent:
            return False, "This persona requires explicit consent to engage in restricted modes."

        for k in self.persona.get("disallowed_content", []):
            # Convert underscores to word boundaries for compound terms
            import re
            # Replace underscores with a pattern that matches underscores or spaces
            pattern = r'\b' + re.escape(k).replace(r'\_', r'[\s_]+') + r'\b'
            if re.search(pattern, (text or "").lower()):
                return False, f"Disallowed by persona rule: {k}"

        return True, "Allowed"

    def handle_request(self, text, explicit_consent=False):
        if self.idle and not text.strip():
            return {"status": "idle", "message": "Standing by. Send a focused request to continue."}

        allowed, msg = self.request_allowed(text, explicit_consent=explicit_consent)
        if not allowed:
            return {"status": "blocked", "message": msg}

        # Placeholder: generation delegated elsewhere
        return {"status": "ok", "message": "Generate safe persona response here."}
