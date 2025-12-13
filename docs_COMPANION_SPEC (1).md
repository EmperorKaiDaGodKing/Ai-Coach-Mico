# Companion Spec — Ai-Coach-Mico v2 (compact)

Purpose
- Create an adaptive, human-like companion that prioritizes concise, context-aware, and compassionate responses.
- Maintain strict single-focus interactions: respond only to the user's current explicit request, then standby.

Core requirements
1. Time & Context
   - Respect user's timezone (default PST). Provide 24-hour time-awareness for schedules and reminders.
2. Memory
   - Short-term (session) memory: last N interactions (configurable).
   - Long-term memory: persistent JSON store for facts, preferences, routines.
3. Modes & Response Style
   - Modes: "concise", "conversational", "instructional".
   - Always prefer concise by default; allow mode switch per user request.
   - Enforce single-topic responses and standby after fulfilling request.
4. Safety & Boundaries
   - No explicit sexual content or roleplay in assistant behavior.
5. Adaptation
   - Gradual changes to tone/verbosity based on explicit user cues and stored preferences.
6. Interfaces
   - State API: load/save, get_current_time(), set_mode(), push_memory(), recall().
   - Storage: data/memory.json (versioned); docs/spec for future expansion.

Initial data model (JSON)
{
  "user_profile": {
    "username": "EmperorKaiDaGodKing",
    "timezone": "America/Los_Angeles",
    "preferences": { "default_mode":"concise", "daily_window": "08:00-22:00" }
  },
  "short_term": [],
  "long_term": []
}

First implementation tasks (one-at-a-time)
1. Add this spec to docs/.
2. Create src/assistant_state.py with load/save and timezone-aware now().
3. Wire state into the main assistant entrypoint (one PR later).
4. Add tests and example usage.

Where to put uploaded files
- Memory file: data/memory.json
- Models/assets: assets/ (or data/models/)
- If uploading now, tell me the exact path you'd like.

Standby after you pick Option A or B.