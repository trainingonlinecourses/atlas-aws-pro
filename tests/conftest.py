"""Shared pytest fixtures for the AWS Atlas Pro test suites.

Rate limits and login-lockout counters are module-level state shared by every
test client; without a reset between tests the slowapi buckets fill up and
later tests 429 spuriously. Autouse fixture clears both after each test.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cheap bcrypt for the test suite; production keeps cost 12 via Vercel env.
os.environ.setdefault("ATLAS_BCRYPT_COST", "4")

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_rate_and_lockout_state():
    yield
    # slowapi limiter storage (register/login/refresh/reset buckets)
    from backend.main import app

    try:
        app.state.limiter.reset()
    except Exception:
        pass
    # login lockout tracker (module-level dict in auth.py)
    from backend import auth as auth_core

    auth_core._FAILS.clear()
    # TestClient persists cookies across requests — drop them so a session
    # logged in by one test doesn't leak into a later "requires auth" test.
    import importlib
    from fastapi.testclient import TestClient

    for modname in ("test_auth", "test_backend", "frontend.test"):
        try:
            mod = importlib.import_module(modname)
        except Exception:
            continue
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, TestClient):
                obj.cookies.clear()
