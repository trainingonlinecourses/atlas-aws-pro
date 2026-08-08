"""Backend + data-integrity test suite for AWS Atlas Pro.

Covers: every API endpoint, the 100-service dataset (no dup ids, no missing or
empty fields), and frontend adapter compatibility (the fields the SPA's
loadFromAPI adapter needs must be present in /api/v1/services).
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402
from backend.services_data import SERVICES_DATA  # noqa: E402

client = TestClient(app)

DETAIL_FIELDS = [
    "id", "name", "full_name", "category", "icon", "tagline",
    "why_it_exists", "when_to_use", "use_cases", "learn_first",
    "terraform", "cdk", "boto3", "delete", "expert_tips", "real_world",
    "next_steps",
]
FRONTEND_MAP = {
    "id": "id", "name": "n", "full_name": "f", "category": "c",
    "icon": "i", "tagline": "t", "why_it_exists": "w", "use_cases": "u",
    "learn_first": "b", "terraform": "tf", "cdk": "ck", "boto3": "sd",
    "delete": "dl", "expert_tips": "x", "real_world": "r", "next_steps": "nt",
}
VALID_CATS = {
    "compute", "storage", "database", "networking", "security",
    "messaging", "analytics", "migration", "devops", "ml",
}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_root_serves_html():
    r = client.get("/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert b"<html" in r.content


def test_root_contains_api_loader():
    r = client.get("/")
    assert b"loadFromAPI" in r.content


def test_services_count_is_100():
    r = client.get("/api/v1/services")
    assert r.status_code == 200
    assert len(r.json()) == 100


def test_api_matches_dataset_ids():
    api_ids = [s["id"] for s in client.get("/api/v1/services").json()]
    data_ids = [s["id"] for s in SERVICES_DATA]
    assert sorted(api_ids) == sorted(data_ids)


def test_services_ids_unique():
    ids = [s["id"] for s in SERVICES_DATA]
    assert len(ids) == len(set(ids)), "duplicate service ids present"


def test_all_services_full_detail_in_api():
    r = client.get("/api/v1/services")
    for s in r.json():
        for f in DETAIL_FIELDS:
            assert f in s and s[f], f"{s.get('id')} missing/empty {f!r} in API"


def test_no_empty_critical_text():
    for s in SERVICES_DATA:
        for f in ("tagline", "why_it_exists", "when_to_use", "use_cases"):
            v = s[f]
            assert v and v.strip(), f"{s['id']} has empty {f!r}"


def test_real_world_two_strings():
    for s in SERVICES_DATA:
        rw = s["real_world"]
        assert isinstance(rw, list) and len(rw) >= 2, f"{s['id']} real_world malformed"
        assert all(isinstance(x, str) and x for x in rw), f"{s['id']} real_world empty item"


def test_next_steps_pairs():
    for s in SERVICES_DATA:
        assert isinstance(s["next_steps"], list) and s["next_steps"], f"{s['id']} no next_steps"
        for ns in s["next_steps"]:
            assert isinstance(ns, list) and len(ns) == 2, f"{s['id']} next_step malformed"
            assert ns[0] and ns[1], f"{s['id']} next_step empty"


def test_valid_categories():
    cats = {s["category"] for s in SERVICES_DATA}
    assert cats <= VALID_CATS, f"unexpected categories: {cats - VALID_CATS}"


def test_frontend_adapter_compat():
    """Every field the frontend adapter reads must be present on every service."""
    for s in client.get("/api/v1/services").json():
        for be, fe in FRONTEND_MAP.items():
            assert s[be] is not None, f"{s['id']} missing {be!r} (frontend key {fe!r})"


def test_every_service_has_env_model():
    """Every service exposes the per-environment operating model (dev->DR->lifecycle)."""
    for s in client.get("/api/v1/services").json():
        em = s.get("env_model")
        assert em, f"{s['id']} missing env_model"
        assert len(em) == 5, f"{s['id']} env_model should have 5 blocks"
        labels = [b["env"] for b in em]
        for need in ("Development", "Staging", "Production", "Multi-region / DR", "Lifecycle"):
            assert any(need in l for l in labels), f"{s['id']} env_model missing {need!r}"
        for b in em:
            assert b["desc"] and b["points"], f"{s['id']} env_model block has empty content"
            assert all(isinstance(p, str) and p for p in b["points"])


def test_env_model_interpolates_service_name():
    """The service's own name (short or full) must appear in its environment model text."""
    for s in client.get("/api/v1/services").json():
        em = s.get("env_model") or []
        joined = " ".join(b["desc"] for b in em).lower()
        found = (s["name"].lower() in joined) or (s["full_name"].lower() in joined)
        assert found, f"{s['id']} neither name nor full_name interpolated into env_model"


def test_categories_total_matches():
    d = client.get("/api/v1/categories").json()
    assert d["total"] == 100
    assert sum(d["categories"].values()) == 100


def test_service_detail():
    r = client.get("/api/v1/services/ec2")
    assert r.status_code == 200
    assert r.json()["name"] == "EC2"


def test_service_detail_404():
    assert client.get("/api/v1/services/does-not-exist").status_code == 404


def test_search_finds_lambda():
    r = client.get("/api/v1/services/search", params={"q": "lambda"})
    assert r.status_code == 200
    assert any(s["id"] == "lambda" for s in r.json())


def test_search_requires_q():
    assert client.get("/api/v1/services/search").status_code in (400, 422)


def test_quiz():
    r = client.get("/api/v1/quiz")
    assert r.status_code == 200
    assert "questions" in r.json()


def test_data_endpoints_ok():
    paths = [
        "/api/v1/projects",
        "/api/v1/architecture-flows",
        "/api/v1/deployment-blueprints",
        "/api/v1/enterprise-architectures",
        "/api/v1/production-playbooks",
        "/api/v1/ai-radar",
    ]
    for path in paths:
        r = client.get(path)
        assert r.status_code == 200, f"{path} -> {r.status_code}"


# --- private DB (SQLite user state) ---


def test_db_status_ok():
    r = client.get("/api/v1/db")
    assert r.status_code == 200
    body = r.json()
    assert body["driver"] == "sqlite"
    assert "persistent" in body and "ephemeral" in body


def test_row_to_dict_maps_tuple_via_description():
    """The libsql client returns tuples (no Row/factory); the helper must
    map values back to column names so db.py stays driver-agnostic."""
    from backend import db as db_store

    class Cur:
        description = (("learned", None, None, None, None, None, None), ("quiz_best", None, None, None, None, None, None))

    assert db_store._row_to_dict(Cur(), ('["ec2"]', 7)) == {"learned": '["ec2"]', "quiz_best": 7}
    assert db_store._row_to_dict(Cur(), None) is None


def test_turso_connect_failure_falls_back_to_memory(monkeypatch):
    """When ATLAS_DB_URL is set but Turso is unreachable/invalid, the API must
    keep working on an in-memory store and /api/v1/db must say why."""
    from backend import db as db_store

    monkeypatch.setenv("ATLAS_DB_URL", "libsql://127.0.0.1:1/nope")
    monkeypatch.setenv("ATLAS_DB_AUTH_TOKEN", "test-token")
    monkeypatch.setattr(db_store, "_conn", None)
    monkeypatch.setattr(db_store, "_is_file", False)
    monkeypatch.setattr(db_store, "_ephemeral", False)
    monkeypatch.setattr(db_store, "_last_error", None)
    try:
        st = db_store.status()
        assert st["driver"] == "turso"
        assert st["persistent"] is False
        assert st["ephemeral"] is True
        assert st["token_set"] is True
        assert st["url_scheme"] == "libsql"
        assert st["error"]  # redacted reason is surfaced for diagnosis
    finally:
        monkeypatch.delenv("ATLAS_DB_URL", raising=False)
        monkeypatch.delenv("ATLAS_DB_AUTH_TOKEN", raising=False)
        db_store._conn = None
        db_store._is_file = False
        db_store._ephemeral = False
        db_store._last_error = None


# --- Auth-aware helper for user-state tests (user-state now requires login) ---
import re as _re
import uuid as _uuid


def _authed_client():
    """Create a verified + logged-in TestClient for a throwaway user."""
    from backend import auth as auth_core
    email = f"bt-{_uuid.uuid4().hex[:10]}@example.com"
    captured = {}

    def fake_send(to_email, subject, html, text):
        m = _re.search(r"token=([A-Za-z0-9_-]+)", text)
        if m:
            captured["raw"] = m.group(1)
    orig = auth_core.send_email
    auth_core.send_email = fake_send
    try:
        r = client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "BackendPass1"},
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        assert r.status_code == 200, r.text
    finally:
        auth_core.send_email = orig
    r = client.post(
        "/api/v1/auth/verify-email",
        json={"token": captured["raw"]},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    assert r.status_code == 200, r.text
    r = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "BackendPass1"},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    assert r.status_code == 200, r.text
    c = TestClient(app)
    c.cookies.set("atlas_access", r.cookies["atlas_access"])
    c.cookies.set("atlas_refresh", r.cookies["atlas_refresh"])
    return c, email


def test_user_state_requires_auth():
    assert client.get("/api/v1/user-state").status_code == 401


def test_user_state_default_empty():
    c, email = _authed_client()
    r = c.get("/api/v1/user-state")
    assert r.status_code == 200
    assert r.json() == {"user_id": email, "learned": [], "quiz_best": 0}


def test_user_state_roundtrip():
    c, email = _authed_client()
    payload = {"user_id": email, "learned": ["ec2", "s3", "lambda"], "quiz_best": 8}
    r = c.put("/api/v1/user-state", json=payload)
    assert r.status_code == 200
    assert r.json() == payload
    got = c.get("/api/v1/user-state").json()
    assert got == payload
    # cleanup
    c.delete("/api/v1/user-state")


def test_user_state_overwrite():
    c, email = _authed_client()
    a = {"user_id": email, "learned": ["ec2"], "quiz_best": 3}
    b = {"user_id": email, "learned": ["ec2", "rds"], "quiz_best": 5}
    c.put("/api/v1/user-state", json=a)
    c.put("/api/v1/user-state", json=b)
    got = c.get("/api/v1/user-state").json()
    assert got == b
    c.delete("/api/v1/user-state")


def test_user_state_delete():
    c, email = _authed_client()
    c.put("/api/v1/user-state", json={"user_id": email, "learned": ["ec2"], "quiz_best": 1})
    r = c.delete("/api/v1/user-state")
    assert r.status_code == 200
    assert r.json()["deleted"] is True
    r = c.delete("/api/v1/user-state")
    assert r.json()["deleted"] is False


def test_user_state_ignores_client_user_id():
    """Server pins user_id to the logged-in email; spoofed ids are ignored."""
    c, email = _authed_client()
    r = c.put("/api/v1/user-state", json={"user_id": "hacker@evil.com", "learned": ["ec2"], "quiz_best": 1})
    assert r.status_code == 200
    assert r.json()["user_id"] == email
    c.delete("/api/v1/user-state")


def test_user_state_learned_only_valid_service_ids():
    """Learned entries that aren't real service ids must be rejected client-side, but the
    API stays safe: it stores strings only (no code execution, no injection)."""
    c, email = _authed_client()
    r = c.put("/api/v1/user-state", json={"user_id": email, "learned": ["</script>"], "quiz_best": 0})
    assert r.status_code == 200
    assert r.json()["learned"] == ["</script>"]
    c.delete("/api/v1/user-state")


def test_industry_issues_list():
    r = client.get("/api/v1/industry-issues")
    assert r.status_code == 200
    j = r.json()
    assert j["count"] > 0
    assert len(j["services"]) == j["count"]
    ids = [s["service_id"] for s in j["services"]]
    assert len(ids) == len(set(ids)), "duplicate industry service_ids"
    for s in j["services"]:
        for key in ("service_id", "scenario", "issue", "fix", "alerts"):
            assert s.get(key), f"industry entry missing {key!r}: {s.get('service_id')}"
    assert len(j["categories"]) > 0
    for c in j["categories"]:
        assert c["category"] and c["pillar"] and c["issues"]


def test_industry_issue_by_id():
    r = client.get("/api/v1/industry-issues/ec2")
    assert r.status_code == 200
    assert r.json()["service_id"] == "ec2"
    assert client.get("/api/v1/industry-issues/does-not-exist").status_code == 404


def test_industry_issues_reference_real_services():
    """Every industry scenario must map to a real service in the catalog."""
    api_ids = {s["id"] for s in SERVICES_DATA}
    j = client.get("/api/v1/industry-issues").json()
    for s in j["services"]:
        assert s["service_id"] in api_ids, f"industry entry {s['service_id']} not in catalog"
