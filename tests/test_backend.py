"""Backend + data-integrity test suite for AWS Atlas Pro.

Covers: every API endpoint, the 94-service dataset (no dup ids, no missing or
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


def test_services_count_is_94():
    r = client.get("/api/v1/services")
    assert r.status_code == 200
    assert len(r.json()) == 94


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


def test_categories_total_matches():
    d = client.get("/api/v1/categories").json()
    assert d["total"] == 94
    assert sum(d["categories"].values()) == 94


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

TEST_UID = "test-user-001"


def test_db_status_ok():
    r = client.get("/api/v1/db")
    assert r.status_code == 200
    body = r.json()
    assert body["driver"] == "sqlite"
    assert "persistent" in body and "ephemeral" in body


def test_user_state_default_empty():
    r = client.get("/api/v1/user-state", params={"user_id": TEST_UID})
    assert r.status_code == 200
    assert r.json() == {"user_id": TEST_UID, "learned": [], "quiz_best": 0}


def test_user_state_roundtrip():
    payload = {"user_id": TEST_UID, "learned": ["ec2", "s3", "lambda"], "quiz_best": 8}
    r = client.put("/api/v1/user-state", json=payload)
    assert r.status_code == 200
    assert r.json() == payload
    got = client.get("/api/v1/user-state", params={"user_id": TEST_UID}).json()
    assert got == payload
    # cleanup
    client.delete("/api/v1/user-state", params={"user_id": TEST_UID})


def test_user_state_overwrite():
    a = {"user_id": TEST_UID, "learned": ["ec2"], "quiz_best": 3}
    b = {"user_id": TEST_UID, "learned": ["ec2", "rds"], "quiz_best": 5}
    client.put("/api/v1/user-state", json=a)
    client.put("/api/v1/user-state", json=b)
    got = client.get("/api/v1/user-state", params={"user_id": TEST_UID}).json()
    assert got == b
    client.delete("/api/v1/user-state", params={"user_id": TEST_UID})


def test_user_state_delete():
    client.put("/api/v1/user-state", json={"user_id": TEST_UID, "learned": ["ec2"], "quiz_best": 1})
    r = client.delete("/api/v1/user-state", params={"user_id": TEST_UID})
    assert r.status_code == 200
    assert r.json()["deleted"] is True
    r = client.delete("/api/v1/user-state", params={"user_id": TEST_UID})
    assert r.json()["deleted"] is False


def test_user_state_requires_user_id():
    assert client.get("/api/v1/user-state").status_code == 422
    assert client.put("/api/v1/user-state", json={"learned": ["ec2"], "quiz_best": 1}).status_code == 422


def test_user_state_learned_only_valid_service_ids():
    """Learned entries that aren't real service ids must be rejected client-side, but the
    API stays safe: it stores strings only (no code execution, no injection)."""
    r = client.put("/api/v1/user-state", json={"user_id": TEST_UID, "learned": ["</script>"], "quiz_best": 0})
    assert r.status_code == 200
    assert r.json()["learned"] == ["</script>"]
    client.delete("/api/v1/user-state", params={"user_id": TEST_UID})
