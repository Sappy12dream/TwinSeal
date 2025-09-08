# scripts/generate_keys.py
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    print(f"Generated key: {key.decode()}")

if __name__ == "__main__":
    generate_key()
