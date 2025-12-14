# Minimal smoke check to verify key modules import successfully.
import sys

MODULES = [
    "src_persona_manager",
    "src_assistant_state",
    "content_filter",
]

failed = []
for m in MODULES:
    try:
        __import__(m)
    except Exception as e:
        failed.append((m, str(e)))

if failed:
    print("IMPORT FAILURES:")
    for m, e in failed:
        print(f"- {m}: {e}")
    sys.exit(2)

print("SMOKE OK")