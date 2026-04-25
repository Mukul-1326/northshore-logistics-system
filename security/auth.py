from database.db_connection import open_link, fetch_cursor
from security.encryption import make_hash, verify_hash
from datetime import datetime


# ================= ADD USER =================
def add_user(name, password, role):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        hashed_pass = make_hash(password)

        cur.execute("""
        INSERT INTO sys_users (usr_name, usr_pass, usr_role)
        VALUES (?, ?, ?)
        """, (name, hashed_pass, role))

        conn.commit()

    except Exception:
        pass  # avoid duplicate crash

    finally:
        conn.close()


# ================= LOGIN =================
def login_user(name, password):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        SELECT * FROM sys_users WHERE usr_name = ?
        """, (name,))

        user = cur.fetchone()

        if user and verify_hash(password, user["usr_pass"]):
            return user

        return None

    finally:
        conn.close()


# ================= ROLE CHECK =================
def check_role(user, allowed_roles):
    if not user:
        return False

    return user["usr_role"] in allowed_roles


# ================= LOG ACTION =================
def log_action(user_id, action_text):
    conn = open_link()
    try:
        cur = fetch_cursor(conn)

        cur.execute("""
        INSERT INTO audit_trail (usr_id, action, log_time)
        VALUES (?, ?, ?)
        """, (
            user_id,
            action_text,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

    finally:
        conn.close()


# ================= MASK SENSITIVE DATA =================
def mask_sensitive(data):
    if not data:
        return ""

    if len(data) <= 4:
        return "*" * len(data)

    return data[:2] + "*" * (len(data) - 4) + data[-2:]


# ================= SIMPLE ENCRYPTION =================
def simple_encrypt(text):
    if not text:
        return ""

    return "".join(chr(ord(c) + 2) for c in text)


def simple_decrypt(text):
    if not text:
        return ""

    return "".join(chr(ord(c) - 2) for c in text)