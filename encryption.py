from cryptography.fernet import Fernet
import os

KEY_FILE = "nayana.key"

def get_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    with open(KEY_FILE, 'rb') as f:
        return f.read()

def encrypt_data(data: str) -> bytes:
    return Fernet(get_key()).encrypt(data.encode())

def decrypt_data(data: bytes) -> str:
    return Fernet(get_key()).decrypt(data).decode()