#!/usr/bin/env python3
"""Generate markdown documentation for AWS Atlas Pro.

Run from the repo root:
    .venv/Scripts/python.exe scripts/gen_docs.py

Outputs:
    docs/README.md            index + category breakdown
    docs/services/<id>.md     one page per service (full detail + code)
    docs/industry-issues.md   real-world scenarios & industry failure modes
    docs/api.md               API reference (derived from FastAPI routes)
    docs/PRIVACY.md           privacy & data-storage model
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from services_data import SERVICES_DATA  # noqa: E402

from env_model import for_service  # noqa: E402

DOCS = ROOT / "docs"
SVC_DIR = DOCS / "services"
SVC_DIR.mkdir(parents=True, exist_ok=True)

CAT_NAMES = {
    "compute": "Compute",
    "storage": "Storage",
    "database": "Database",
    "networking": "Networking & Delivery",
    "security": "Security, Identity & Compliance",
    "messaging": "Application Integration",
    "analytics": "Analytics",
    "migration": "Migration & Transfer",
    "devops": "Management & Governance",
    "ml": "Machine Learning & AI",
}


def md_code(lang, code):
    return f"```{lang}\n{code.rstrip()}\n```\n"


def service_md(s):
    lines = []
    lines.append(f"# {s['icon']} {s['full_name']} (`{s['id']}`)")
    lines.append("")
    lines.append(f"> {s['tagline']}")
    lines.append("")
    lines.append(f"- **Category:** {CAT_NAMES.get(s['category'], s['category'])}")
    lines.append(f"- **Service id:** `{s['id']}`")
    if s.get("ai_enabled"):
        lines.append("- **AI-enabled:** yes")
    lines.append("")
    lines.append("## Why it exists")
    lines.append(s["why_it_exists"])
    lines.append("")
    lines.append("## When to use it")
    lines.append(s["when_to_use"])
    lines.append("")
    lines.append("## Learn first")
    lines.append("")
    for item in s["learn_first"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Terraform")
    lines.append(md_code("hcl", s["terraform"]))
    lines.append("## AWS CDK")
    lines.append(md_code("ts", s["cdk"]))
    lines.append("## Boto3 (Python)")
    lines.append(md_code("python", s["boto3"]))
    lines.append("## Delete / teardown")
    lines.append(md_code("python", s["delete"]))
    lines.append("## Expert tips")
    lines.append("")
    for tip in s["expert_tips"]:
        lines.append(f"- {tip}")
    lines.append("")
    rw = s["real_world"]
    if isinstance(rw, list) and len(rw) >= 2:
        lines.append("## Real-world example")
        lines.append("")
        lines.append(f"**{rw[0]}** — {rw[1]}")
        lines.append("")
    lines.append("## Operating across environments")
    lines.append("")
    lines.append("The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.")
    lines.append("")
    for block in for_service(s):
        lines.append(f"### {block['icon']} {block['env']}")
        lines.append("")
        lines.append(block["desc"])
        lines.append("")
        for point in block["points"]:
            lines.append(f"- {point}")
        lines.append("")
    lines.append("## Next steps")
    lines.append("")
    for name, desc in s["next_steps"]:
        slug = name.lower().replace(" ", "-").replace("/", "-")
        lines.append(f"- **{name}** ({desc}) — see `{slug}`")
    lines.append("")
    return "\n".join(lines)


def index_md():
    lines = []
    lines.append("# AWS Atlas Pro — Service Documentation")
    lines.append("")
    lines.append(f"**{len(SERVICES_DATA)} AWS services**, each with a full reference page: tagline, why-it-exists, when-to-use, learning checklist, Terraform / CDK / Boto3 / delete code, expert tips, a real-world example, the environment operating model (Dev → Staging → Production → DR → Lifecycle), and next-step links.")
    lines.append("")
    lines.append("- [API reference](api.md)")
    lines.append("- [Real-world industry scenarios & failure modes](industry-issues.md)")
    lines.append("- [Privacy & data model](PRIVACY.md)")
    lines.append("")
    by_cat = {}
    for s in SERVICES_DATA:
        by_cat.setdefault(s["category"], []).append(s)
    for cat in sorted(by_cat):
        services = sorted(by_cat[cat], key=lambda x: x["id"])
        lines.append(f"## {CAT_NAMES.get(cat, cat)} ({len(services)})")
        lines.append("")
        for s in services:
            lines.append(f"- [{s['icon']} {s['full_name']} (`{s['id']}`)](services/{s['id']}.md) — {s['tagline']}")
        lines.append("")
    return "\n".join(lines)


def industry_md():
    from industry_issues import INDUSTRY_ISSUES, CATEGORY_ISSUES

    lines = []
    lines.append("# Real-World Industry Scenarios & Issues")
    lines.append("")
    lines.append("Production incidents, the failure mode behind each, the industry-standard fix, and the alert that would have caught it first. Per-service teaching reference — each entry doubles as an interview answer.")
    lines.append("")
    lines.append(f"**{len(INDUSTRY_ISSUES)} scenarios** across compute, storage, database, networking, security, messaging, data, and ML.")
    lines.append("")
    lines.append("## Scenarios by service")
    lines.append("")
    for s in sorted(INDUSTRY_ISSUES, key=lambda x: x["service_id"]):
        lines.append(f"### {s['service_name']} (`{s['service_id']}`)")
        lines.append("")
        lines.append(f"- **Category:** {CAT_NAMES.get(s['category'], s['category'])}")
        lines.append(f"- **Scenario:** {s['scenario']}")
        lines.append(f"- **The industry issue:** {s['issue']}")
        if s.get("impact"):
            lines.append(f"- **Impact:** {s['impact']}")
        lines.append(f"- **The standard fix:** {s['fix']}")
        lines.append(f"- **Alerts:** {', '.join(s['alerts'])}")
        lines.append(f"- **Tags:** {', '.join(s['tags'])}")
        lines.append("")
    lines.append("## Per-pillar failure modes")
    lines.append("")
    lines.append("The recurring, industry-standard pitfalls every team should design against.")
    lines.append("")
    for c in CATEGORY_ISSUES:
        lines.append(f"### {c['category']} — {c['pillar']}")
        lines.append("")
        for i in c["issues"]:
            lines.append(f"- **{i['title']}** — {i['detail']}")
        lines.append("")
    return "\n".join(lines)


def api_md(app):
    lines = []
    lines.append("# AWS Atlas Pro — API Reference")
    lines.append("")
    lines.append(f"Base URL: `https://atlas-aws-pro.vercel.app` (or `http://localhost:8000` locally).")
    lines.append("")
    lines.append("## Endpoints")
    lines.append("")
    lines.append("| Method | Path | Description |")
    lines.append("|--------|------|-------------|")
    routes = []
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)
        if not path or not methods:
            continue
        endpoint = getattr(route, "endpoint", None)
        doc = (getattr(endpoint, "__doc__", None) or "").strip().split("\n")[0]
        for m in sorted(methods - {"HEAD", "OPTIONS"}):
            routes.append((m, path, doc))
    for m, path, doc in sorted(routes, key=lambda r: (r[0], r[1])):
        lines.append(f"| {m} | `{path}` | {doc} |")
    lines.append("")
    lines.append("## Data path (privacy)")
    lines.append("")
    lines.append("The browser NEVER talks to the database. It calls the API; the backend reads/writes the private SQLite store and returns JSON. See [PRIVACY.md](PRIVACY.md).")
    lines.append("")
    return "\n".join(lines)


def privacy_md():
    return """# Privacy & Data Model

## Where the data lives

- **Service catalog** (100 services): code-defined in `backend/services_data.py`, served over the API. No database involved.
- **User progress** (learned services, quiz best score): private **SQLite** database, `backend/db.py`. The frontend only ever calls the API — it never touches the DB.

## Data path

```
Browser (frontend)  --GET/PUT /api/v1/user-state-->  FastAPI backend  --sqlite-->  DB file
        ^                                                            |
        +-------------------- JSON response --------------------------+
```

## Privacy guarantees

- The DB file is **never served** to clients and is **gitignored** (`*.db`, `data/`).
- **No credentials in the repo.** The only knob is `ATLAS_DB_PATH` (an env var), set via `ATLAS_DB_PATH=/path/to/atlas.db`.
- `.env`, `CLAUDE.md`, `.claude/`, `config/`, and DB files are excluded from GitHub.
- Deleting your data: `DELETE /api/v1/user-state?user_id=<id>` wipes a row; the user_id is generated client-side and stored in the browser's localStorage.

## Serverless note (Vercel)

Vercel serverless filesystems are ephemeral. On Vercel the SQLite store falls back to **in-memory** so every endpoint keeps working, but data does not persist across cold starts. For durable persistence, use **Turso/libSQL** — the API layer and schema do not change.

## Making it durable with Turso (recommended)

1. Create a database: `turso db create atlas-pro`
2. Get your URL + token: `turso db show atlas-pro --url` and `turso db tokens create atlas-pro`
3. Set the env vars on the host (Vercel: *Settings → Environment Variables*):
   - `ATLAS_DB_URL` = `libsql://<db>.turso.io`
   - `ATLAS_DB_AUTH_TOKEN` = the token from step 2

When `ATLAS_DB_URL` is set, `backend/db.py` uses the `libsql_client` driver (a drop-in `sqlite3` replacement) so the schema and queries are identical. Without it, the app runs on local SQLite (or in-memory on serverless).

> **Tokens are secret.** Set them as environment variables on the host only — never in the repo. Neither `ATLAS_DB_URL` nor `ATLAS_DB_AUTH_TOKEN` is committed.
"""


def main():
    from fastapi import FastAPI

    count = len(SERVICES_DATA)
    written = 0
    for s in SERVICES_DATA:
        (SVC_DIR / f"{s['id']}.md").write_text(service_md(s), encoding="utf-8")
        written += 1

    (DOCS / "README.md").write_text(index_md(), encoding="utf-8")
    (DOCS / "industry-issues.md").write_text(industry_md(), encoding="utf-8")
    (DOCS / "PRIVACY.md").write_text(privacy_md(), encoding="utf-8")

    sys.path.insert(0, str(ROOT))
    from backend.main import app  # noqa: E402
    (DOCS / "api.md").write_text(api_md(app), encoding="utf-8")

    print(f"docs written: {written} service pages + README.md + industry-issues.md + api.md + PRIVACY.md")
    print(f"total services documented: {count}")


if __name__ == "__main__":
    main()
