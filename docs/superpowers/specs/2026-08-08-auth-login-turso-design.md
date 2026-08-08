# AWS Atlas Pro — Auth Login + Turso-Backed Progress Tracking

**Date**: 2026-08-08
**Status**: Approved (design), in implementation

## Goal

Add real authentication so users can log in and track progress (learned services, quiz best) tied to a verified identity. All auth + progress data stored durably in Turso (already wired via `ATLAS_DB_URL`).

## Decisions (user-confirmed)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth method | Email + password | Chosen by user over OTP/social |
| Email delivery | Resend (free 100/day) | Works on Vercel, provider-agnostic wrapper |
| Progress mapping | Email = user_id | Backward compatible, no migration |
| UI scope | Full integration | Login modal + progress view + auto-prompt on save |
| Token transport | httpOnly SameSite cookies | JS never sees tokens → XSS can't steal |
| Refresh | Rotation + reuse detection | Replay of old refresh token revokes family |

## Architecture

```
frontend/index.html
   fetch + credentials:"include"
   ▼
POST /api/v1/auth/register|verify-email|login|logout|refresh|reset-password
   ▼
backend/auth.py
   ├─ bcrypt verify (cost 12)
   ├─ JWT sign/verify (HS256, ATLAS_AUTH_SECRET)
   ├─ refresh rotation + reuse detection
   ├─ email verify/reset tokens (single-use, SHA-256 hashed)
   └─ rate limiting (slowapi)
   ▼
backend/db.py → Turso
   └─ users, refresh_tokens, verify_tokens, user_state
```

## Data model (new Turso tables)

```sql
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    email_verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS refresh_tokens (
    token_hash TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    family TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS verify_tokens (
    token_hash TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    purpose TEXT NOT NULL,            -- 'verify_email' | 'reset_password'
    expires_at TEXT NOT NULL,
    used INTEGER NOT NULL DEFAULT 0
);
```

`user_state` unchanged. `user_id` = email.

## API endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/v1/auth/register` | public | Create account, send verify email |
| POST | `/api/v1/auth/verify-email` | public | Verify email via single-use token |
| POST | `/api/v1/auth/login` | public | bcrypt check, set cookies |
| POST | `/api/v1/auth/logout` | refresh cookie | Revoke session, clear cookies |
| POST | `/api/v1/auth/refresh` | refresh cookie | Rotate refresh token + reuse detection |
| POST | `/api/v1/auth/reset-password` | public | Email reset link |
| POST | `/api/v1/auth/reset-password/confirm` | public | Set new password, revoke sessions |
| GET | `/api/v1/auth/me` | access cookie | Current user profile |

Protected routes: existing `/api/v1/user-state` GET/PUT/DELETE require valid access cookie; `user_id` must equal authenticated email (server ignores client-supplied user_id when logged in).

## Security properties

- Passwords: bcrypt, cost 12 (explicit), never plaintext.
- Access token: JWT HS256, 15 min, stateless (no DB hit), signed with `ATLAS_AUTH_SECRET`.
- Refresh token: 256-bit random, 7 days, stored SHA-256 hashed. Rotated every refresh. Reuse of a rotated token → revoke entire family.
- Verify/reset tokens: single-use, 24h expiry, hashed at rest.
- Cookies: `HttpOnly; Secure; SameSite=Lax; Path=/`. Secure disabled when `VERCEL=0` local http for tests.
- CSRF: SameSite=Lax + `X-Requested-With: XMLHttpRequest` required on mutating auth routes.
- Rate limiting (slowapi): login 5/15min per IP+email, register 5/hour/IP, refresh 30/min/IP, reset-request 3/hour/email, verify 10/10min/IP.
- Lockout: after 5 failed logins for email+IP → 15 min block (error before bcrypt).
- Generic errors: "invalid credentials" for both unknown email + wrong password (no user enumeration).
- No stack traces in responses. JSON errors only.

## Env vars (Vercel + local, never committed)

- `ATLAS_AUTH_SECRET` (32+ byte random; JWT + token signing)
- `RESEND_API_KEY` (optional: console-fallback email when absent)
- `RESEND_FROM` (sender, default `AWS Atlas Pro <onboarding@resend.dev>`)
- Existing: `ATLAS_DB_URL`, `ATLAS_DB_AUTH_TOKEN`

## Error handling

- Duplicate email register → 409.
- Unverified email login → 403 `email_not_verified` (with resend option).
- Unknown email on login → 401 generic.
- Expired/used/revoked token → 401.
- DB unavailable → 503 storage unavailable (existing pattern).

## Testing plan

**Unit (pytest, `tests/test_auth.py`)**:
1. Register → user in DB, password bcrypt-hashed (not plaintext).
2. Verify email happy path (token single-use; second use → 400).
3. Expired verify token → 400.
4. Login happy path → cookies set.
5. Wrong password → 401 generic (same message as unknown email).
6. Unverified email login → 403.
7. Refresh rotation: old token invalid after refresh.
8. Reuse detection: replay old refresh token → family revoked, new token invalid.
9. Logout → refresh token revoked, cookies cleared.
10. Reset flow: request → confirm → old password fails, new works, sessions revoked.
11. Lockout after 5 failed logins → 429.
12. Rate limit exceeded → 429.
13. Access token expired → 401; forged/tampered token → 401.
14. `user-state` write when logged in → server pins user_id to email (client spoof fails).
15. Weak password rejected (short / no digit).

**Frontend (browser-sim)**: modal open, register, login, progress save auto-prompt, logout.

**Pen-test pass (redhat-style)**:
- Brute-force login → lockout.
- Refresh token replay → family revoked.
- Tampered JWT (flip alg, change email) → rejected.
- Cookie flags present (HttpOnly/Secure/SameSite).
- User enumeration: unknown email vs wrong password same response.
- Timing: unknown email short-circuits before bcrypt? → equalize with dummy bcrypt.
- Open redirect in email links → none (tokens only, no URL params).
- SQL injection via email/token params → parameterized queries only.
- Token in response body → never (cookie only).

## Pen-test results (2026-08-08, redhat pass — all checks green)

**Vulnerabilities found and fixed**:

1. **Timing oracle (email enumeration)** — `_dummy_verify()` did `hashpw` **+** `checkpw`
   (2× the bcrypt work of a real `verify_password`), so an unknown email responded ~2×
   *slower* than a known one — a reverse timing oracle. Fixed: `_dummy_verify` now does a
   single `checkpw` against a precomputed cost-12 hash, matching real login cost. Live
   timing check: unknown 4.1ms vs known 2.5ms (cost 4 test env; equal within noise).
2. **Open CORS in production** — `DEBUG` defaulted to `"true"`, so `allow_origins=["*"]`
   + `allow_credentials=True` shipped. Starlette reflects any origin, letting a hostile
   page read authed responses. Fixed: `DEBUG` defaults to `false`, `ATLAS_ORIGINS` env
   allow-list (default `https://atlas-aws-pro.vercel.app`, + localhost in DEBUG). Verified:
   evil origin gets no ACAO header; real origin allowed.
3. **Unbounded `learned` list** — authed user could PUT a 10k-element list (Turso storage
   abuse). Fixed: `UserState.learned` capped at 300 items, each id ≤ 64 chars → 422. Live:
   400-item list → 422, normal 2-item save works.
4. **Weak `ATLAS_AUTH_SECRET`** — no length check; a short secret makes HS256 JWT
   offline-brute-forceable. Fixed: `_auth_secret()` raises unless ≥ 32 chars.

**Frontend gap fixed**:
5. **No silent session refresh** — access token is 15-min TTL but the frontend never called
   `/api/v1/auth/refresh`, so long sessions silently lost progress saving after 15 min.
   Fixed: `apiFetch()` wrapper refreshes once on 401 and retries (single in-flight guard).

**Checked and confirmed safe (no action needed)**:
- Refresh rotation + reuse detection (replay of rotated token revokes whole family).
- Cookie flags: HttpOnly, Secure (prod via VERCEL=1), SameSite=Lax.
- CSRF: SameSite=Lax + `X-Requested-With` required on state-changing POSTs (login/logout);
  refresh doesn't need it (no cookie-bearing cross-site POST can send the cookie).
- Login lockout keyed email+IP (5/15min), slowapi IP throttle 30/15min.
- Generic errors: unknown email == wrong password == `invalid credentials`.
- Register duplicate → 409; reset request → generic message, no enumeration.
- Verify/reset tokens: single-use, purpose-scoped (`verify_email` vs `reset_password`),
  24h expiry, HMAC-hashed at rest.
- Password reset revokes all sessions for that user.
- SQLi: all queries parameterized (`?` placeholders).
- Tokens never in response bodies — httpOnly cookies only.
- `user_id` server-pinned to logged-in email (client spoof ignored).
- Register/verify/reset rate-limited; login lockout can't be used to DoS a victim (keyed
  to attacker's IP too).

**Full battery (31 live checks)**: register → verify (replay→400) → login (403 unverified,
403 no-CSRF, 401 generic, 401 wrong-pwd) → cookies → me → user-state PUT/GET pinned →
refresh rotation → old-refresh replay 401 + family revoked → lockout after 5 → 429 →
reset request generic → confirm → old pwd fails / new works → reset token replay 400 →
forged access 401 → logout revokes refresh → input caps 422.
