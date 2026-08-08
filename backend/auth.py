"""
AWS Atlas Pro - Authentication core.

Production-grade email+password auth over Turso persistence.

Security properties
-------------------
- Passwords: bcrypt, cost 12 (explicit). Never plaintext, never logged.
- Access token: JWT HS256, 15 min, stateless (no DB hit on verify).
- Refresh token: 256-bit random, 7 days, stored SHA-256 hashed. Rotated on
  every refresh. Reuse detection: replaying a rotated-out token revokes the
  entire session family.
- Verify / reset tokens: single-use, 24h expiry, hashed at rest.
- Tokens ride in httpOnly, Secure, SameSite=Lax cookies so JS never sees them
  (XSS cannot exfiltrate a session).
- Login is rate-limited (slowapi in main.py) and lockout after N failures.

Env vars
--------
  ATLAS_AUTH_SECRET  32+ byte random secret (JWT + token hashing). Required.
  RESEND_API_KEY     Resend key for email. Absent -> dev console fallback.
  RESEND_FROM        Sender address (default AWS Atlas Pro <onboarding@resend.dev>).
"""
import hashlib
import hmac
import logging
import os
import secrets
import threading
import time
from datetime import datetime, timedelta, timezone

logger = logging.getLogger("atlas.auth")

# Login lockout tracker: email+IP -> [fail_timestamps]. In-memory (per
# serverless instance); slowapi adds cross-instance rate limiting in main.py.
_FAILS = {}
_LOCK = threading.Lock()


def _login_key(email: str, ip: str) -> str:
    return f"{email.lower()}|{ip}"


def _is_locked_out(email: str, ip: str) -> bool:
    now = time.time()
    with _LOCK:
        fails = _FAILS.get(_login_key(email, ip), [])
        fails = [t for t in fails if now - t < LOCKOUT_SECONDS]
        _FAILS[_login_key(email, ip)] = fails
        return len(fails) >= MAX_LOGIN_ATTEMPTS


def record_failed_login(email: str, ip: str) -> None:
    with _LOCK:
        key = _login_key(email, ip)
        fails = _FAILS.setdefault(key, [])
        now = time.time()
        fails.append(now)
        _FAILS[key] = [t for t in fails if now - t < LOCKOUT_SECONDS]


def clear_login_failures(email: str, ip: str) -> None:
    with _LOCK:
        _FAILS.pop(_login_key(email, ip), None)


# Same import strategy as backend/main.py — resolves to one module instance
# regardless of whether the app runs as `main` or `backend.main`.
try:
    import db as db_store
except ImportError:
    from backend import db as db_store

ACCESS_TOKEN_TTL_MIN = 15
REFRESH_TOKEN_TTL_DAYS = 7
VERIFY_TOKEN_TTL_HOURS = 24
# Cost overrideable for tests (ATLAS_BCRYPT_COST=4) — production keeps 12.
BCRYPT_COST = int(os.getenv("ATLAS_BCRYPT_COST", "12"))
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_SECONDS = 15 * 60

_COOKIE_NAME_ACCESS = "atlas_access"
_COOKIE_NAME_REFRESH = "atlas_refresh"
JWT_ALG = "HS256"


# ----------------------------------------------------------------------
# Password hashing
# ----------------------------------------------------------------------
def hash_password(password: str) -> str:
    """bcrypt hash with explicit cost 12. Password must be <= 72 bytes
    (bcrypt truncates silently; our request models already cap length)."""
    import bcrypt
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=BCRYPT_COST)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Constant-time bcrypt check; returns False for any failure."""
    import bcrypt
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


_DUMMY_HASH = None
def _dummy_verify() -> None:
    """Burn comparable time when email is unknown so timing can't enumerate.

    Must be exactly ONE bcrypt checkpw (same cost as a real verify_password).
    Doing hashpw+checkpw here would be ~2x the real work and turn into a
    *reverse* timing oracle (unknown email slower than known).
    """
    global _DUMMY_HASH
    import bcrypt
    if _DUMMY_HASH is None:
        # Precompute once at the login cost so steady-state is a single checkpw.
        _DUMMY_HASH = bcrypt.hashpw(b"dummy-password-0", bcrypt.gensalt(rounds=BCRYPT_COST))
    try:
        bcrypt.checkpw(b"dummy-password-0", _DUMMY_HASH)
    except Exception:
        pass


# ----------------------------------------------------------------------
# Token primitives
# ----------------------------------------------------------------------
_MIN_SECRET_LEN = 32

def _auth_secret() -> bytes:
    """JWT + token-hash secret. Must exist and be strong: a short value makes
    HS256 offline-brute-forceable and lets an attacker forge tokens."""
    secret = os.getenv("ATLAS_AUTH_SECRET", "")
    if len(secret) < _MIN_SECRET_LEN:
        raise RuntimeError(
            f"ATLAS_AUTH_SECRET must be at least {_MIN_SECRET_LEN} chars (got {len(secret)})"
        )
    return secret.encode()


def hash_token(raw: str) -> str:
    """SHA-256 hash a token for at-rest storage (HMAC-keyed)."""
    return hmac.new(_auth_secret(), raw.encode(), hashlib.sha256).hexdigest()


def new_raw_token() -> str:
    """Cryptographically secure 256-bit URL-safe token."""
    return secrets.token_urlsafe(32)


def create_access_token(email: str) -> str:
    """Short-lived JWT access token (stateless, HS256)."""
    from jose import jwt
    now = datetime.now(timezone.utc)
    claims = {
        "sub": email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_TTL_MIN)).timestamp()),
        "type": "access",
    }
    return jwt.encode(claims, _auth_secret(), algorithm=JWT_ALG)


def verify_access_token(token: str):
    """Verify JWT; return email or None."""
    from jose import jwt
    from jose.exceptions import JWTError
    try:
        claims = jwt.decode(token, _auth_secret(), algorithms=[JWT_ALG])
        if claims.get("type") != "access":
            return None
        return claims.get("sub")
    except JWTError:
        return None


# ----------------------------------------------------------------------
# Cookies
# ----------------------------------------------------------------------
def cookie_secure() -> bool:
    """Secure flag off on local http (Vercel sets VERCEL=1 in prod)."""
    return os.getenv("VERCEL", "0") == "1"


def _set_auth_cookies(response, access_token: str, refresh_token: str, max_age: int):
    common = {"path": "/", "httponly": True, "samesite": "lax", "secure": cookie_secure()}
    response.set_cookie(_COOKIE_NAME_ACCESS, access_token, max_age=ACCESS_TOKEN_TTL_MIN * 60, **common)
    response.set_cookie(_COOKIE_NAME_REFRESH, refresh_token, max_age=max_age, **common)


def _clear_auth_cookies(response):
    common = {"path": "/", "httponly": True, "samesite": "lax", "secure": cookie_secure()}
    response.delete_cookie(_COOKIE_NAME_ACCESS, **common)
    response.delete_cookie(_COOKIE_NAME_REFRESH, **common)


def access_cookie_name() -> str:
    return _COOKIE_NAME_ACCESS


def refresh_cookie_name() -> str:
    return _COOKIE_NAME_REFRESH


# ----------------------------------------------------------------------
# Email (Resend with dev-console fallback)
# ----------------------------------------------------------------------
def _send_resend(to_email: str, subject: str, html: str, text: str) -> bool:
    import json as _json
    import urllib.request as _urllib
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        return False
    payload = _json.dumps({
        "from": os.getenv("RESEND_FROM", "AWS Atlas Pro <onboarding@resend.dev>"),
        "to": [to_email],
        "subject": subject,
        "html": html,
        "text": text,
    }).encode()
    req = _urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with _urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except Exception as exc:
        logger.warning("resend email failed to %s: %r", to_email, exc)
        return False


def send_email(to_email: str, subject: str, html: str, text: str) -> None:
    """Send via Resend; fall back to console log (dev) when no API key."""
    if _send_resend(to_email, subject, html, text):
        return
    # Dev fallback: surface the message locally instead of silently dropping.
    print(f"[DEV EMAIL] to={to_email} subject={subject!r}\n{text}", flush=True)


def send_verify_email(email: str, token: str) -> None:
    text = (
        f"Welcome to AWS Atlas Pro!\n\n"
        f"Verify your email to save progress:\n"
        f"{os.getenv('APP_BASE_URL', 'https://atlas-aws-pro.vercel.app')}/verify-email?token={token}\n\n"
        f"Link expires in 24 hours."
    )
    html = text.replace("\n", "<br>")
    send_email(email, "Verify your email — AWS Atlas Pro", html, text)


def send_reset_email(email: str, token: str) -> None:
    text = (
        f"Password reset request for your AWS Atlas Pro account.\n\n"
        f"Reset your password:\n"
        f"{os.getenv('APP_BASE_URL', 'https://atlas-aws-pro.vercel.app')}/reset-password?token={token}\n\n"
        f"Link expires in 24 hours. If you didn't request this, ignore it."
    )
    html = text.replace("\n", "<br>")
    send_email(email, "Reset your password — AWS Atlas Pro", html, text)


# ----------------------------------------------------------------------
# Session helpers (refresh rotation + reuse detection)
# ----------------------------------------------------------------------
def issue_session(email: str, response) -> None:
    """Create a fresh refresh token family + access token on login."""
    raw = new_raw_token()
    family = new_raw_token()
    db_store.create_refresh_token(
        hash_token(raw), email, family,
        (datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_TTL_DAYS)).isoformat(),
    )
    access = create_access_token(email)
    _set_auth_cookies(response, access, raw, REFRESH_TOKEN_TTL_DAYS * 24 * 3600)


def refresh_session(raw_token: str, response) -> bool:
    """Rotate a refresh token. Returns True on success.

    If the presented token is a rotated-out (used) one, we treat it as token
    theft and revoke the whole family (reuse detection).
    """
    tok_hash = hash_token(raw_token)
    row = db_store.get_refresh_token(tok_hash)
    if row is None:
        return False
    if row["revoked"]:
        # Reuse detection: this token was already rotated out. Replay of a
        # rotated token = token theft signal -> revoke the whole family.
        db_store.revoke_refresh_family(row["family"])
        return False
    expires = datetime.fromisoformat(row["expires_at"])
    if expires < datetime.now(timezone.utc):
        return False
    # Rotate: old token becomes used (revoked), new token same family.
    db_store.revoke_refresh_token(tok_hash)
    new_raw = new_raw_token()
    db_store.create_refresh_token(
        hash_token(new_raw), row["email"], row["family"],
        (datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_TTL_DAYS)).isoformat(),
    )
    access = create_access_token(row["email"])
    _set_auth_cookies(response, access, new_raw, REFRESH_TOKEN_TTL_DAYS * 24 * 3600)
    return True


def revoke_session(raw_token: str) -> None:
    tok_hash = hash_token(raw_token)
    row = db_store.get_refresh_token(tok_hash)
    if row is not None:
        db_store.revoke_refresh_family(row["family"])
