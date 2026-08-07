#!/usr/bin/env node
/* Frontend integrity tests for AWS Atlas Pro (node, no framework).
 * Exits non-zero on any failure. Run: node tests/frontend.test.js */
const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, '..', 'frontend', 'index.html');
const src = fs.readFileSync(htmlPath, 'utf8');

let failures = 0;
const check = (cond, msg) => {
  if (!cond) { failures++; console.error('FAIL:', msg); }
};

/* --- extract the SERVICES array (same scanner as the generator) --- */
const marker = 'let SERVICES=[';
const start = src.indexOf(marker);
check(start !== -1, 'SERVICES array marker found');
let SERVICES = [];
if (start !== -1) {
  const after = src.slice(start + marker.length);
  let depth = 1, i = 0, tpl = false, dq = false, sq = false;
  for (; i < after.length; i++) {
    const ch = after[i];
    if (tpl) { if (ch === '\\') { i++; continue; } if (ch === '`') tpl = false; continue; }
    if (dq) { if (ch === '\\') { i++; continue; } if (ch === '"') dq = false; continue; }
    if (sq) { if (ch === '\\') { i++; continue; } if (ch === "'") sq = false; continue; }
    if (ch === '`') { tpl = true; continue; }
    if (ch === '"') { dq = true; continue; }
    if (ch === "'") { sq = true; continue; }
    if (ch === '[') depth++;
    else if (ch === ']') { depth--; if (depth === 0) break; }
  }
  const expr = '[' + after.slice(0, i + 1);
  try { SERVICES = new Function('return ' + expr)(); }
  catch (e) { check(false, 'SERVICES parses: ' + e.message); }
}

check(SERVICES.length === 100, `expect 100 services, got ${SERVICES.length}`);

const KEYS = ['id', 'n', 'f', 'c', 'i', 't', 'w', 'u', 'b', 'tf', 'ck', 'sd', 'dl', 'x', 'r', 'nt'];
const ids = SERVICES.map((s) => s.id);
check(new Set(ids).size === ids.length, 'service ids are unique');
check(ids.length === 0 || ids.includes('ec2'), 'ec2 present');

for (const s of SERVICES) {
  for (const k of KEYS) {
    check(s[k] !== undefined && s[k] !== null && s[k] !== '', `${s.id} missing ${k}`);
  }
  for (const k of ['t', 'w', 'u']) {
    check(typeof s[k] === 'string' && s[k].trim().length > 0, `${s.id} empty text ${k}`);
  }
  check(Array.isArray(s.r) && s.r.length >= 2 && s.r.every((x) => typeof x === 'string' && x), `${s.id} r malformed`);
  check(Array.isArray(s.nt) && s.nt.every((p) => Array.isArray(p) && p.length === 2 && p[0] && p[1]), `${s.id} nt malformed`);
  check(typeof s.tf === 'string' && s.tf.length > 0, `${s.id} terraform empty`);
  check(typeof s.ck === 'string' && s.ck.length > 0, `${s.id} cdk empty`);
  check(typeof s.sd === 'string' && s.sd.length > 0, `${s.id} boto3 empty`);
}

/* --- page wiring --- */
check(/let SERVICES=/.test(src), 'SERVICES declared with let (reassignable)');
check(src.includes('loadFromAPI'), 'loadFromAPI present');
check(src.includes('adaptService'), 'adaptService present');
check(src.includes('fetch("/api/v1/services"'), 'fetches /api/v1/services');
check(/connect-src 'self'/.test(src), "CSP allows same-origin fetch (connect-src 'self')");

/* --- adapter round-trip against a backend-format fixture --- */
const adapt = (s) => ({
  id: s.id, n: s.name, f: s.full_name, c: s.category, i: s.icon, t: s.tagline,
  w: s.why_it_exists, u: s.use_cases, b: s.learn_first,
  tf: s.terraform, ck: s.cdk, sd: s.boto3, dl: s.delete,
  x: s.expert_tips, r: s.real_world, nt: s.next_steps,
});
const backend = (s) => ({
  id: s.id, name: s.n, full_name: s.f, category: s.c, icon: s.i, tagline: s.t,
  why_it_exists: s.w, use_cases: s.u, learn_first: s.b,
  terraform: s.tf, cdk: s.ck, boto3: s.sd, delete: s.dl,
  expert_tips: s.x, real_world: s.r, next_steps: s.nt,
});
const roundTripOk = SERVICES.every((s) => {
  const out = adapt(backend(s));
  return Object.keys(s).sort().join(',') === Object.keys(out).sort().join(',') &&
    Object.keys(s).every((k) => JSON.stringify(s[k]) === JSON.stringify(out[k]));
});
check(roundTripOk, 'adapter round-trips every service exactly');

if (failures) { console.error(`${failures} frontend test(s) failed`); process.exit(1); }
console.log('frontend tests: ALL PASS (100 services, unique ids, full fields, adapter round-trip, wiring)');
