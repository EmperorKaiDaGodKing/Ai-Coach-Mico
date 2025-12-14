# Minimal gating module (example)
import json
import time
from pathlib import Path

CONFIG_PATH = "nsfw_config.yaml"

def load_config():
    import yaml
    return yaml.safe_load(Path(CONFIG_PATH).read_text())

def is_owner(username, cfg):
    return username in cfg["private_adult_mode"].get("owner_usernames", [])

def activate_private_mode(username):
    cfg = load_config()
    if not cfg["private_adult_mode"].get("enabled", False):
        return False, "Private Adult Mode is disabled in config."
    if not is_owner(username, cfg):
        return False, "Only repository owners can activate Private Adult Mode."
    # Here you would show disclaimer and require explicit confirmation in UI/CLI
    log_activation(username)
    return True, "Private Adult Mode activated for session."

def log_activation(username):
    cfg = load_config()
    path = Path(cfg["private_adult_mode"]["audit_log_path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"user": username, "time": int(time.time())}

