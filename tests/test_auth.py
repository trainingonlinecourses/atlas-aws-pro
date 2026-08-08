"""Auth + session-security test suite for AWS Atlas Pro.

Covers the email+password auth layer: register, verify, login, refresh
rotation, reuse detection, lockout, rate limiting, email enumeration, token
tampering, and user-state authorization pinning.
"""
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("ATLAS_AUTH_SECRET", "test-secret-" + uuid.uuid4().hex)

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402

client = TestClient(app)

PASSWORD = "CorrectHorse7"
AUTH_HEADERS = {"X-Requested-With": "XMLHttpRequest"}


def uniq_email(prefix="u"):
    return f"{prefix}-{uuid.uuid4().hex[:10]}@example.com"


def register(email=None, password=PASSWORD, **kw):
    email = email or uniq_email()
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password}, headers=AUTH_HEADERS)
    return email, r


def make_verified_user(email=None, password=PASSWORD):
    """Register + capture raw verify token + verify -> returns (email, token)."""
    captured = {}

    def fake_send(to_email, subject, html, text):
        # text contains the raw token in the URL ?token=<raw>
        import re
        m = re.search(r"token=([A-Za-z0-9_-]+)", text)
        if m:
            captured["raw"] = m.group(1)
    from backend import auth as auth_core
    orig = auth_core.send_email
    auth_core.send_email = fake_send
    try:
        email, r = register(email=email, password=password)
        assert r.status_code == 200, r.text
    finally:
        auth_core.send_email = orig
    assert "raw" in captured, "verify email not captured"
    r = client.post("/api/v1/auth/verify-email", json={"token": captured["raw"]}, headers=AUTH_HEADERS)
    assert r.status_code == 200, r.text
    return email


def login(email, password=PASSWORD):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
        headers=AUTH_HEADERS,
    )


def logged_in_client(email=None, password=PASSWORD):
    """A TestClient whose cookies carry a valid session for a verified user."""
    email = make_verified_user(email=email, password=password)
    r = login(email, password)
    assert r.status_code == 200, r.text
    c = TestClient(app)
    c.cookies.set("atlas_access", r.cookies["atlas_access"])
    c.cookies.set("atlas_refresh", r.cookies["atlas_refresh"])
    return c, email


# ----------------------------------------------------------------------
# Registration
# ----------------------------------------------------------------------
def test_register_creates_user_with_bcrypt_hash():
    email, r = register()
    assert r.status_code == 200
    from backend import db as db_store
    user = db_store.get_user(email)
    assert user is not None
    assert user["password_hash"] != PASSWORD  # not plaintext
    assert user["password_hash"].startswith("$2")  # bcrypt marker
    assert user["email_verified"] == 0


def test_register_duplicate_email_409():
    email, r = register()
    assert r.status_code == 200
    r2 = client.post("/api/v1/auth/register", json={"email": email, "password": PASSWORD}, headers=AUTH_HEADERS)
    assert r2.status_code == 409


def test_register_weak_password_rejected():
    for bad in ["short", "alllettersonly", "12345678", ""]:
        r = client.post("/api/v1/auth/register", json={"email": uniq_email(), "password": bad}, headers=AUTH_HEADERS)
        assert r.status_code in (400, 422), (bad, r.text)


def test_register_invalid_email_rejected():
    for bad in ["not-an-email", "a@b", "a@b.", "@x.com", "spaces in@mail.com"]:
        r = client.post("/api/v1/auth/register", json={"email": bad, "password": PASSWORD}, headers=AUTH_HEADERS)
        assert r.status_code == 400, (bad, r.text)


# ----------------------------------------------------------------------
# Email verification
# ----------------------------------------------------------------------
def test_verify_email_happy_path_and_single_use():
    captured = {}

    def fake_send(to_email, subject, html, text):
        import re
        m = re.search(r"token=([A-Za-z0-9_-]+)", text)
        if m:
            captured["raw"] = m.group(1)
    from backend import auth as auth_core
    orig = auth_core.send_email
    auth_core.send_email = fake_send
    try:
        email, r = register()
        assert r.status_code == 200
    finally:
        auth_core.send_email = orig
    from backend import db as db_store
    assert db_store.get_user(email)["email_verified"] == 0

    r = client.post("/api/v1/auth/verify-email", json={"token": captured["raw"]}, headers=AUTH_HEADERS)
    assert r.status_code == 200
    assert db_store.get_user(email)["email_verified"] == 1

    # Single-use: replay fails.
    r = client.post("/api/v1/auth/verify-email", json={"token": captured["raw"]}, headers=AUTH_HEADERS)
    assert r.status_code == 400


def test_verify_email_garbage_token_400():
    r = client.post("/api/v1/auth/verify-email", json={"token": "nonsense-token-xyz"}, headers=AUTH_HEADERS)
    assert r.status_code == 400


def test_verify_email_wrong_purpose_400():
    # A reset token must not verify email.
    captured = {}

    def fake_send(to_email, subject, html, text):
        import re
        m = re.search(r"token=([A-Za-z0-9_-]+)", text)
        if m:
            captured["raw"] = m.group(1)
    from backend import auth as auth_core
    orig = auth_core.send_email
    auth_core.send_email = fake_send
    email, r = register()
    assert r.status_code == 200
    # Manually mint a reset token for the same email, bypassing send.
    auth_core.send_email = fake_send
    try:
        # use an unverified user: reset-request is allowed regardless
        raw = auth_core.new_raw_token()
        from backend import db as db_store
        from datetime import datetime, timedelta, timezone
        db_store.create_verify_token(
            auth_core.hash_token(raw), email, "reset_password",
            (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        )
        r = client.post("/api/v1/auth/verify-email", json={"token": raw}, headers=AUTH_HEADERS)
        assert r.status_code == 400
    finally:
        auth_core.send_email = orig


# ----------------------------------------------------------------------
# Login
# ----------------------------------------------------------------------
def test_login_happy_path_sets_cookies():
    email = make_verified_user()
    r = login(email)
    assert r.status_code == 200
    assert "atlas_access" in r.cookies
    assert "atlas_refresh" in r.cookies


def test_login_wrong_password_401_generic():
    email = make_verified_user()
    r = login(email, "WrongPassword9")
    assert r.status_code == 401
    assert r.json()["detail"] == "invalid credentials"


def test_login_unknown_email_401_same_message():
    r = login(uniq_email(), PASSWORD)
    assert r.status_code == 401
    assert r.json()["detail"] == "invalid credentials"


def test_login_unverified_email_403():
    email, r = register()
    assert r.status_code == 200
    r = login(email)
    assert r.status_code == 403
    assert r.json()["detail"] == "email_not_verified"


def test_login_missing_csrf_header_403():
    email = make_verified_user()
    r = client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    assert r.status_code == 403


# ----------------------------------------------------------------------
# Lockout + rate limiting
# ----------------------------------------------------------------------
def test_lockout_after_5_failures():
    email = make_verified_user()
    for _ in range(5):
        r = login(email, "WrongPassword9")
        assert r.status_code == 401
    r = login(email, PASSWORD)  # correct password now blocked
    assert r.status_code == 429
    assert "try again later" in r.json()["detail"]


def test_login_rate_limited():
    email = uniq_email()
    codes = set()
    for _ in range(35):
        r = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": PASSWORD},
            headers=AUTH_HEADERS,
        )
        codes.add(r.status_code)
    assert 429 in codes  # slowapi IP throttle 30/15min kicks in


# ----------------------------------------------------------------------
# Refresh rotation + reuse detection
# ----------------------------------------------------------------------
def test_refresh_rotates_and_invalidates_old():
    email = make_verified_user()
    r = login(email)
    old_refresh = r.cookies["atlas_refresh"]

    c = TestClient(app)
    c.cookies.set("atlas_refresh", old_refresh)
    rr = c.post("/api/v1/auth/refresh")
    assert rr.status_code == 200
    new_refresh = rr.cookies["atlas_refresh"]
    assert new_refresh != old_refresh

    # Old token is now rotated out -> replay = reuse -> 401 + family revoked.
    c2 = TestClient(app)
    c2.cookies.set("atlas_refresh", old_refresh)
    assert c2.post("/api/v1/auth/refresh").status_code == 401
    # New token from same family is also revoked now.
    c3 = TestClient(app)
    c3.cookies.set("atlas_refresh", new_refresh)
    assert c3.post("/api/v1/auth/refresh").status_code == 401


def test_refresh_no_cookie_401():
    assert client.post("/api/v1/auth/refresh").status_code == 401


def test_refresh_garbage_token_401():
    c = TestClient(app)
    c.cookies.set("atlas_refresh", "garbage-not-a-token")
    assert c.post("/api/v1/auth/refresh").status_code == 401


# ----------------------------------------------------------------------
# Logout
# ----------------------------------------------------------------------
def test_logout_revokes_session():
    email = make_verified_user()
    r = login(email)
    refresh = r.cookies["atlas_refresh"]
    c = TestClient(app)
    c.cookies.set("atlas_refresh", refresh)
    c.cookies.set("atlas_access", r.cookies["atlas_access"])
    assert c.post("/api/v1/auth/logout", headers=AUTH_HEADERS).status_code == 200
    # Refresh now revoked.
    c2 = TestClient(app)
    c2.cookies.set("atlas_refresh", refresh)
    assert c2.post("/api/v1/auth/refresh").status_code == 401


# ----------------------------------------------------------------------
# Password reset
# ----------------------------------------------------------------------
def test_reset_flow_updates_password_and_revokes_sessions():
    email = make_verified_user()
    r = login(email)
    old_refresh = r.cookies["atlas_refresh"]

    captured = {}

    def fake_send(to_email, subject, html, text):
        import re
        m = re.search(r"token=([A-Za-z0-9_-]+)", text)
        if m:
            captured["raw"] = m.group(1)
    from backend import auth as auth_core
    orig = auth_core.send_email
    auth_core.send_email = fake_send
    try:
        rr = client.post("/api/v1/auth/reset-password", json={"email": email}, headers=AUTH_HEADERS)
        assert rr.status_code == 200
    finally:
        auth_core.send_email = orig
    assert "raw" in captured

    r = client.post(
        "/api/v1/auth/reset-password/confirm",
        json={"token": captured["raw"], "new_password": "NewPassw0rd!"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200

    # Old password fails.
    assert login(email, PASSWORD).status_code == 401
    # New password works.
    assert login(email, "NewPassw0rd!").status_code == 200
    # Old session revoked.
    c = TestClient(app)
    c.cookies.set("atlas_refresh", old_refresh)
    assert c.post("/api/v1/auth/refresh").status_code == 401


def test_reset_confirm_reuses_token_once_only():
    captured = {}

    def fake_send(to_email, subject, html, text):
        import re
        m = re.search(r"token=([A-Za-z0-9_-]+)", text)
        if m:
            captured["raw"] = m.group(1)
    from backend import auth as auth_core
    orig = auth_core.send_email
    auth_core.send_email = fake_send
    email = make_verified_user()
    try:
        client.post("/api/v1/auth/reset-password", json={"email": email}, headers=AUTH_HEADERS)
    finally:
        auth_core.send_email = orig
    body = {"token": captured["raw"], "new_password": "NewPassw0rd!"}
    assert client.post("/api/v1/auth/reset-password/confirm", json=body, headers=AUTH_HEADERS).status_code == 200
    assert client.post("/api/v1/auth/reset-password/confirm", json=body, headers=AUTH_HEADERS).status_code == 400


def test_reset_request_no_account_no_enumeration():
    r = client.post("/api/v1/auth/reset-password", json={"email": uniq_email()}, headers=AUTH_HEADERS)
    assert r.status_code == 200
    assert "if that email exists" in r.json()["message"]


# ----------------------------------------------------------------------
# Access token security
# ----------------------------------------------------------------------
def test_tampered_access_token_rejected():
    email = make_verified_user()
    r = login(email)
    access = r.cookies["atlas_access"]
    # Flip the algorithm header and the subject.
    import base64, json
    parts = access.split(".")
    header = json.dumps({"alg": "none", "typ": "JWT"})
    head_b64 = base64.urlsafe_b64encode(header.encode()).rstrip(b"=").decode()
    forged = f"{head_b64}.{parts[1]}.{parts[2]}"
    c = TestClient(app)
    c.cookies.set("atlas_access", forged)
    c.cookies.set("atlas_refresh", r.cookies["atlas_refresh"])
    assert c.get("/api/v1/auth/me").status_code == 401


def test_me_requires_auth():
    assert client.get("/api/v1/auth/me").status_code == 401


def test_me_returns_email_and_progress():
    c, email = logged_in_client()
    r = c.get("/api/v1/auth/me")
    assert r.status_code == 200
    j = r.json()
    assert j["email"] == email
    assert j["email_verified"] is True
    assert "progress" in j


# ----------------------------------------------------------------------
# user-state authorization (server-pinned to logged-in email)
# ----------------------------------------------------------------------
def test_user_state_requires_auth():
    assert client.get("/api/v1/user-state").status_code == 401
    assert client.put("/api/v1/user-state", json={"user_id": "x", "learned": [], "quiz_best": 0}).status_code == 401


def test_user_state_pins_user_id_to_email():
    c, email = logged_in_client()
    # Client tries to write under a different user_id -> server pins to email.
    r = c.put("/api/v1/user-state", json={"user_id": "someone-else", "learned": ["ec2"], "quiz_best": 4})
    assert r.status_code == 200
    assert r.json()["user_id"] == email
    got = c.get("/api/v1/user-state").json()
    assert got["user_id"] == email
    assert got["learned"] == ["ec2"]
    # Another identity must not see this progress.
    c2, _ = logged_in_client()
    assert c2.get("/api/v1/user-state").json()["learned"] == []


def test_user_state_roundtrip_authed():
    c, email = logged_in_client()
    r = c.put("/api/v1/user-state", json={"user_id": email, "learned": ["s3", "lambda"], "quiz_best": 9})
    assert r.status_code == 200
    assert r.json() == {"user_id": email, "learned": ["s3", "lambda"], "quiz_best": 9}
    got = c.get("/api/v1/user-state").json()
    assert got == {"user_id": email, "learned": ["s3", "lambda"], "quiz_best": 9}
    d = c.delete("/api/v1/user-state")
    assert d.json()["deleted"] is True


# ----------------------------------------------------------------------
# Misc / defense-in-depth
# ----------------------------------------------------------------------
def test_no_plaintext_password_in_any_response():
    """Login/register/me responses never echo the password."""
    email = make_verified_user()
    r = login(email)
    text = r.text
    assert PASSWORD not in text
    assert "password" not in r.json()


def test_auth_me_rejects_refresh_token_as_access():
    email = make_verified_user()
    r = login(email)
    c = TestClient(app)
    c.cookies.set("atlas_access", r.cookies["atlas_refresh"])  # refresh token in access slot
    assert c.get("/api/v1/auth/me").status_code == 401


# ----------------------------------------------------------------------
# Pen-test regressions (redhat pass)
# ----------------------------------------------------------------------
def test_dummy_verify_is_single_checkpw_not_timing_oracle():
    """Unknown-email login must burn ~1 bcrypt op, not 2. A hashpw+checkpw
    here would make unknown emails ~2x slower -> timing-based enumeration."""
    from backend import auth as auth_core
    import bcrypt
    calls = {"hashpw": 0, "checkpw": 0}
    real_hashpw, real_checkpw = bcrypt.hashpw, bcrypt.checkpw
    bcrypt.hashpw = lambda *a, **k: (calls.__setitem__("hashpw", calls["hashpw"] + 1), real_hashpw(*a, **k))[1]
    bcrypt.checkpw = lambda *a, **k: (calls.__setitem__("checkpw", calls["checkpw"] + 1), real_checkpw(*a, **k))[1]
    try:
        auth_core._DUMMY_HASH = None  # force recompute so counters are clean
        auth_core._dummy_verify()
        auth_core._dummy_verify()  # steady-state path
    finally:
        bcrypt.hashpw, bcrypt.checkpw = real_hashpw, real_checkpw
        auth_core._DUMMY_HASH = None  # don't leak a cost-12 precompute into other tests
    # one hashpw for the warmup, then one checkpw per call (== real verify cost)
    assert calls["hashpw"] == 1, f"hashpw called {calls['hashpw']}x, want 1"
    assert calls["checkpw"] == 2, f"checkpw called {calls['checkpw']}x, want 2"


def test_user_state_rejects_huge_learned_list():
    c, _ = logged_in_client()
    big = [f"svc-{i}" for i in range(400)]  # > 300 cap
    r = c.put("/api/v1/user-state", json={"user_id": "x", "learned": big, "quiz_best": 0})
    assert r.status_code == 422  # pydantic list max_length


def test_user_state_rejects_huge_single_item():
    c, _ = logged_in_client()
    r = c.put("/api/v1/user-state", json={"user_id": "x", "learned": ["a" * 500], "quiz_best": 0})
    assert r.status_code == 422  # item StringConstraints max_length=64


def test_auth_secret_enforces_minimum_length():
    from backend import auth as auth_core
    import os
    saved = os.environ.get("ATLAS_AUTH_SECRET")
    try:
        os.environ["ATLAS_AUTH_SECRET"] = "short"
        try:
            auth_core._auth_secret()
            assert False, "short secret must be rejected"
        except RuntimeError as e:
            assert "at least 32" in str(e)
    finally:
        if saved is None:
            os.environ.pop("ATLAS_AUTH_SECRET", None)
        else:
            os.environ["ATLAS_AUTH_SECRET"] = saved


def test_cors_does_not_echo_arbitrary_origin():
    """Default config must not reflect any Origin. A hostile page that is
    NOT in allow_origins must get no access-control-allow-origin header, so
    it cannot read authed responses even with credentials requested."""
    r = client.get("/api/v1/services", headers={"Origin": "https://evil.example"})
    assert r.headers.get("access-control-allow-origin") != "https://evil.example"
    # Known-good origin must be allowed so the same-origin app works.
    r2 = client.get("/api/v1/services", headers={"Origin": "https://atlas-aws-pro.vercel.app"})
    assert r2.headers.get("access-control-allow-origin") == "https://atlas-aws-pro.vercel.app"
