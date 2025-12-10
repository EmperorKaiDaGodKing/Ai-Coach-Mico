# Minimal assistant state manager (v2 starter)
# - Stores profile, timezone, short & long memory to data/memory.json
# - Provides timezone-aware now() and simple mode logic

import json
from pathlib import Path
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # For Python < 3.9, ensure 'pytz' is installed (add 'pytz; python_version < "3.9"' to requirements.txt)
    from pytz import timezone as ZoneInfo  # fallback if needed

DATA_DIR = Path.cwd() / "data"
MEMORY_FILE = DATA_DIR / "memory.json"

DEFAULT_STATE = {
    "user_profile": {
        "username": "User",
        "timezone": "America/Los_Angeles",
        "preferences": { "default_mode": "concise", "daily_window": "08:00-22:00" }
    },
    "short_term": [],
    "long_term": []
}

class AssistantState:
    def __init__(self, memory_path=MEMORY_FILE):
        self.memory_path = Path(memory_path)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not self.memory_path.exists():
            self._write(DEFAULT_STATE)
        self.state = self._read()
        self.mode = self.state["user_profile"]["preferences"].get("default_mode", "concise")
        self.standby = True  # when True, assistant waits after responding

    def _read(self):
        with open(self.memory_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, obj):
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

    def save(self):
        self.state["user_profile"]["preferences"]["default_mode"] = self.mode
        self._write(self.state)

    def get_now(self):
        tzname = self.state["user_profile"].get("timezone", "America/Los_Angeles")
        try:
            tz = ZoneInfo(tzname)
        except Exception:
            tz = timezone.utc
        return datetime.now(tz)

    def push_short(self, entry):
        self.state.setdefault("short_term", []).append({
            "time": self.get_now().isoformat(),
            "entry": entry
        })
        # keep only last N (configurable; default 50)
        self.state["short_term"] = self.state["short_term"][-50:]
        self.save()

    def push_long(self, item):
        self.state.setdefault("long_term", []).append(item)
        self.save()

    def recall_short(self, limit=10):
        return self.state.get("short_term", [])[-limit:]

    def recall_long(self, query=None):
        # simple: return all if no query; query is a substring match
        long = self.state.get("long_term", []) or []
        if not query:
            return long
        return [x for x in long if query.lower() in json.dumps(x).lower()]

    def set_mode(self, mode):
        self.mode = mode
        self.save()

    def should_expand(self, explicit_request=False):
        # Basic decision: expand if user asked for details or mode set to 'instructional'
        if explicit_request or self.mode == "instructional":
            return True
        return False

# Example usage:
# state = AssistantState()
# print(state.get_now().strftime("%H:%M %Z"))
# state.push_short("User asked for plan.")