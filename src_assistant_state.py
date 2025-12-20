# Minimal assistant state manager (v2 starter)
# - Stores profile, timezone, short & long memory to data/memory.json
# - Provides timezone-aware now() and simple mode logic

import json
import logging
from pathlib import Path
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:
    # Fallback to pytz for Python < 3.9
    try:
        from pytz.exceptions import UnknownTimeZoneError as ZoneInfoNotFoundError
    except (ImportError, AttributeError):
        # Older pytz versions may not have UnknownTimeZoneError
        ZoneInfoNotFoundError = KeyError
    # For Python < 3.9, ensure 'pytz' is installed (add 'pytz; python_version < "3.9"' to requirements.txt)
    from pytz import timezone as ZoneInfo  # fallback if needed

logger = logging.getLogger(__name__)

DATA_DIR = Path.cwd() / "data"
MEMORY_FILE = DATA_DIR / "memory.json"

def _new_memory_bank():
    return {"engagement": {}, "journal": []}

DEFAULT_STATE = {
    "user_profile": {
        "username": "User",
        "timezone": "America/Los_Angeles",
        "preferences": { "default_mode": "concise", "daily_window": "08:00-22:00" }
    },
    "short_term": [],
    "long_term": [],
    "memory_bank": _new_memory_bank()
}

MAX_JOURNAL_ENTRIES = 200

class AssistantState:
    def __init__(self, memory_path=MEMORY_FILE):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.memory_path.exists():
            self._write(DEFAULT_STATE)
        self.state = self._read()
        self._ensure_structure()
        self.mode = self.state["user_profile"]["preferences"].get("default_mode", "concise")
        self.standby = True  # when True, assistant waits after responding

    def _read(self):
        with open(self.memory_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, obj):
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

    def _ensure_list_field(self, name):
        if name not in self.state or not isinstance(self.state[name], list):
            self.state[name] = []
            return True
        return False

    def _ensure_structure(self):
        changed = False
        profile = self.state.setdefault("user_profile", {})
        if "username" not in profile:
            profile["username"] = DEFAULT_STATE["user_profile"]["username"]
            changed = True
        if "timezone" not in profile:
            profile["timezone"] = DEFAULT_STATE["user_profile"]["timezone"]
            changed = True

        prefs = profile.setdefault("preferences", {})
        if "default_mode" not in prefs:
            prefs["default_mode"] = DEFAULT_STATE["user_profile"]["preferences"]["default_mode"]
            changed = True
        if "daily_window" not in prefs:
            prefs["daily_window"] = DEFAULT_STATE["user_profile"]["preferences"]["daily_window"]
            changed = True

        if self._ensure_list_field("short_term"):
            changed = True
        if self._ensure_list_field("long_term"):
            changed = True

        pre_bank = self.state.get("memory_bank")
        bank_missing = pre_bank is None
        engagement_missing = bank_missing or "engagement" not in pre_bank
        journal_missing = bank_missing or "journal" not in pre_bank
        self._ensure_memory_bank()
        if bank_missing or engagement_missing or journal_missing:
            changed = True

        if changed:
            self._write(self.state)

    def _ensure_memory_bank(self):
        bank = self.state.setdefault("memory_bank", _new_memory_bank())
        bank.setdefault("engagement", {})
        bank.setdefault("journal", [])
        return bank

    def save(self):
        self.state["user_profile"]["preferences"]["default_mode"] = self.mode
        self._write(self.state)

    def get_now(self):
        tzname = self.state["user_profile"].get("timezone", "America/Los_Angeles")
        try:
            tz = ZoneInfo(tzname)
        except ZoneInfoNotFoundError as e:
            logger.warning(
                "Invalid timezone '%s': %s. Falling back to UTC.",
                tzname, e
            )
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

    # --- Memory bank helpers -------------------------------------------------
    def update_engagement_profile(self, mood=None, style=None, flow=None, instructions=None):
        """
        Store user-guided engagement settings that steer responses.
        - mood: how you want the assistant to match your energy (str)
        - style: tone or delivery preference, e.g., "supportive" (str)
        - flow: pacing/structure hints, e.g., "check in, then suggest next step" (str)
        - instructions: guardrails or cues; str or list of strings, stored as list
        """
        bank = self._ensure_memory_bank()
        engagement = bank["engagement"]
        if mood is not None:
            engagement["mood"] = mood
        if style is not None:
            engagement["style"] = style
        if flow is not None:
            engagement["flow"] = flow
        if instructions is not None:
            if isinstance(instructions, str):
                engagement["instructions"] = [instructions]
            else:
                engagement["instructions"] = list(instructions)
        engagement["last_updated"] = self.get_now().isoformat()
        self.save()
        return engagement

    def get_engagement_profile(self):
        bank = self._ensure_memory_bank()
        return bank["engagement"]

    def log_moment(self, note, mood=None, tags=None, share_with_chat=False):
        """
        Log a journal entry tied to the current or provided mood.
        `share_with_chat=True` marks it as safe to surface inside chat context.
        - note: free-form text for the entry
        - mood: optional override for this entry
        - tags: optional list of short labels to group or search later
        - share_with_chat: whether this entry can be used in chat context
        """
        bank = self._ensure_memory_bank()
        engagement = bank["engagement"]
        if tags is None:
            normalized_tags = []
        elif isinstance(tags, str):
            normalized_tags = [tags]
        else:
            normalized_tags = list(tags)
        entry = {
            "time": self.get_now().isoformat(),
            "note": note,
            "mood": mood or engagement.get("mood"),
            "tags": normalized_tags,
            "share_with_chat": bool(share_with_chat),
        }
        bank["journal"].append(entry)
        if len(bank["journal"]) > MAX_JOURNAL_ENTRIES:
            bank["journal"] = bank["journal"][-MAX_JOURNAL_ENTRIES:]
        self.save()
        return entry

    def recall_journal(self, limit=20, shared_only=False):
        """Return the most recent journal entries (dicts with time/note/mood/tags/share flag).
        Set shared_only=True to return only entries marked shareable."""
        bank = self._ensure_memory_bank()
        entries = bank["journal"]
        if shared_only:
            entries = [e for e in entries if e.get("share_with_chat")]
        if limit is not None:
            entries = entries[-limit:]
        return entries

# Example usage:
# state = AssistantState()
# print(state.get_now().strftime("%H:%M %Z"))
# state.push_short("User asked for plan.")
