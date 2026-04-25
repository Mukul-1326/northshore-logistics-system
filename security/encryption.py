import hashlib
import secrets


def make_hash(raw_text):
    """Create secure salted hash."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((raw_text + salt).encode()).hexdigest()
    return f"{hashed}:{salt}"


def verify_hash(input_text, stored_value):
    """Verify input against stored hash."""
    try:
        hashed, salt = stored_value.split(":")
        check_hash = hashlib.sha256((input_text + salt).encode()).hexdigest()
        return check_hash == hashed
    except Exception:
        return False


# NEW (FOR DATA ENCRYPTION REQUIREMENT)
def encrypt_text(text):
    """Simple reversible encryption (for storage fields like address)."""
    return ''.join(chr(ord(c) + 3) for c in text)


def decrypt_text(text):
    """Reverse encryption."""
    return ''.join(chr(ord(c) - 3) for c in text)

# COMPATIBILITY FIX
simple_encrypt = encrypt_text
simple_decrypt = decrypt_text