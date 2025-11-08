# encryption_utils.py
import os
import struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_SIZE = 12  # recommended for AESGCM
FNAME_LEN_FIELD = ">H"  # 2 bytes unsigned short big-endian (max filename 65535 bytes)

def generate_key() -> bytes:
    """Return 32-byte (256-bit) key suitable for AES-256-GCM."""
    return os.urandom(32)

def load_key_from_env(env_var: str = "FILE_ENCRYPTION_KEY") -> bytes:
    """
    Load key from environment variable (base64 or hex recommended).
    For simplicity here we accept raw bytes stored via files or hex string.
    We'll accept hex string if length matches.
    """
    key = os.environ.get(env_var)
    if not key:
        raise RuntimeError(f"Environment variable {env_var} not set. Generate and set a 32-byte key.")
    # try hex decode
    try:
        # if user provides hex
        if len(key) == 64:  # 32 bytes hex
            return bytes.fromhex(key)
    except Exception:
        pass
    # if the key was stored raw (not recommended) then decode as utf-8 bytes (warning)
    b = key.encode('utf-8')
    if len(b) == 32:
        return b
    raise RuntimeError(f"{env_var} must be a 32-byte key (provide as 64 hex chars for safety).")

def encrypt_bytes(plaintext: bytes, key: bytes, filename: str) -> bytes:
    """
    Return the bytes we will write to disk:
    nonce (12 bytes) + filename_len(2 bytes) + filename_utf8 + ciphertext
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    fname_bytes = filename.encode('utf-8')
    if len(fname_bytes) > 65535:
        raise ValueError("Filename too long.")
    header = nonce + struct.pack(FNAME_LEN_FIELD, len(fname_bytes)) + fname_bytes
    return header + ciphertext

def decrypt_bytes(data: bytes, key: bytes) -> (bytes, str):
    """
    Parse the stored format and return (plaintext_bytes, original_filename)
    """
    if len(data) < NONCE_SIZE + 2:
        raise ValueError("Encrypted data too short or corrupted.")
    nonce = data[:NONCE_SIZE]
    pos = NONCE_SIZE
    fname_len = struct.unpack(FNAME_LEN_FIELD, data[pos:pos+2])[0]
    pos += 2
    fname_bytes = data[pos:pos+fname_len]
    pos += fname_len
    ciphertext = data[pos:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext, fname_bytes.decode('utf-8')

def encrypt_file(input_path: str, output_path: str, key: bytes, original_filename: str = None):
    """
    Read input_path bytes, encrypt and write to output_path using header format.
    If original_filename not provided, the basename of input_path is used.
    """
    if original_filename is None:
        original_filename = os.path.basename(input_path)
    with open(input_path, "rb") as f:
        data = f.read()
    out = encrypt_bytes(data, key, original_filename)
    with open(output_path, "wb") as f:
        f.write(out)

def decrypt_file_to_bytes(encrypted_path: str, key: bytes) -> (bytes, str):
    """Return (plaintext_bytes, original_filename) for the encrypted file."""
    with open(encrypted_path, "rb") as f:
        data = f.read()
    return decrypt_bytes(data, key)