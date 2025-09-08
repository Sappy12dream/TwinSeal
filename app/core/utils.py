# app/core/utils.py
import secrets
from pathlib import Path

def generate_random_filename(ext: str = "") -> str:
    name = secrets.token_hex(16)
    if ext:
        name += f".{ext.lstrip('.')}"
    return name

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
