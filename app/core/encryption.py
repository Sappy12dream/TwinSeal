# app/core/encryption.py
from cryptography.fernet import Fernet
from pathlib import Path

# Generate a new key (store per user securely)
def generate_key() -> bytes:
    return Fernet.generate_key()

# Encrypt file bytes
def encrypt_file(file_bytes: bytes, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(file_bytes)

# Decrypt file bytes
def decrypt_file(file_bytes: bytes, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.decrypt(file_bytes)

# Save encrypted file to disk
def save_encrypted_file(file_bytes: bytes, filename: str, storage_path: str) -> str:
    Path(storage_path).mkdir(parents=True, exist_ok=True)
    filepath = Path(storage_path) / filename
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    return str(filepath)

# Load encrypted file from disk
def load_encrypted_file(filename: str, storage_path: str) -> bytes:
    filepath = Path(storage_path) / filename
    with open(filepath, "rb") as f:
        return f.read()
