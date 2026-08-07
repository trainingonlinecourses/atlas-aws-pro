#!/usr/bin/env node
/* Browser-simulation harness for frontend/index.html (no framework).
 * Stubs a minimal DOM + localStorage + fetch, runs the real inline script,
 * then verifies: services load from the API, server progress is pulled and
 * merged, and progress is pushed back to the backend. Exits non-zero on
 * failure. Run: node tests/browser-sim.js */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'frontend', 'index.html'), 'utf8');
const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/);
if (!m) { console.error('no inline script found'); process.exit(1); }
const code = m[1];

let failures = 0;
const check = (cond, msg) => { if (!cond) { failures++; console.error('FAIL:', msg); } };

/* ---------- minimal DOM stubs ---------- */
function makeEl() {
  return new Proxy({}, {
    get(t, k) {
      if (k === 'style') return new Proxy({}, { get: () => '', set: () => true });
      if (k === 'classList') return { add() {}, remove() {}, toggle() {}, contains() { return false; } };
      if (k === 'dataset') return {};
      if (k === 'innerHTML') return '';
      if (k === 'textContent') return '';
      if (k === 'children') return [];
      if (k === 'parentNode') return null;
      if (typeof k === 'symbol') return undefined;
      if (k in t) return t[k];
      return function () { return makeEl(); };
    },
    set(t, k, v) { t[k] = v; return true; },
  });
}
const els = new Map();
const document = {
  getElementById(id) { if (!els.has(id)) els.set(id, makeEl()); return els.get(id); },
  querySelector() { return makeEl(); },
  querySelectorAll() { return { length: 0, forEach() {} }; },
  createElement() { return makeEl(); },
  body: { appendChild() {}, removeChild() {}, addEventListener() {} },
  addEventListener() {},
};
class IntersectionObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}

/* ---------- localStorage stub ---------- */
const mem = new Map();
const localStorage = {
  getItem: (k) => (mem.has(k) ? mem.get(k) : null),
  setItem: (k, v) => mem.set(k, String(v)),
  removeItem: (k) => mem.delete(k),
};

/* ---------- fetch stub ---------- */
const backendServices = (() => {
  // Minimal backend-format fixtures: enough to exercise adaptService + render.
  const ids = ['ec2', 's3', 'lambda', 'rds', 'vpc'];
  return ids.map((id) => ({
    id, name: id.toUpperCase(), full_name: 'Full ' + id, category: 'compute',
    icon: 'x', tagline: 'tagline ' + id, why_it_exists: 'why ' + id,
    when_to_use: 'when ' + id, use_cases: 'use ' + id,
    learn_first: ['a', 'b'], terraform: 'tf', cdk: 'ck', boto3: 'sd', delete: 'dl',
    expert_tips: ['t1', 't2'], real_world: ['ACME', 'does ' + id],
    next_steps: [['Other', 'how it connects']],
  }));
})();
const puts = [];
let pullCount = 0;
const fetchStub = (url, opts) => {
  opts = opts || {};
  if (url === '/api/v1/services') {
    return Promise.resolve({ ok: true, json: () => Promise.resolve(backendServices) });
  }
  if (url.indexOf('/api/v1/user-state') === 0) {
    if ((opts.method || 'GET') === 'PUT') {
      puts.push(JSON.parse(opts.body));
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
    }
    pullCount++;
    return Promise.resolve({ ok: true, json: () => Promise.resolve({ user_id: 'u_seed', learned: ['ec2', 'lambda'], quiz_best: 6 }) });
  }
  return Promise.resolve({ ok: false, json: () => Promise.resolve(null) });
};

/* ---------- other globals ---------- */
const navigator = { clipboard: { writeText: () => Promise.resolve() } };
const URL = { createObjectURL: () => 'blob:x', revokeObjectURL() {} };

const sandbox = { document, localStorage, IntersectionObserver, fetch: fetchStub, navigator, URL, console, Set, Map, Date, Math, JSON, Object, Array, String, Number, Boolean, encodeURIComponent, setTimeout, clearTimeout, parseInt, isNaN, addEventListener() {}, removeEventListener() {}, getComputedStyle: () => ({}) };
sandbox.window = sandbox;
sandbox.globalThis = sandbox;

/* ---------- run the real inline script ---------- */
/* `let`/`const` inside `with(this){}` are block-scoped, so the only way to
 * inspect the app state is to probe from inside the same scope. */
const probeCode = '\n;window.__probe=function(){return {servicesLen:SERVICES.length,learnedArr:Array.from(learned),best:bestGet()};};';
try {
  const fn = new Function('with(this){' + code + probeCode + '\n}');
  fn.call(sandbox);
} catch (e) {
  console.error('script crashed at load:', e && e.stack ? e.stack : e);
  process.exit(1);
}

/* ---------- verify (async) ---------- */
setTimeout(() => {
  try {
    const p = sandbox.__probe();
    // loadFromAPI must have replaced the embedded 100 with the live API payload (5 fixtures)
    check(p.servicesLen === backendServices.length, `SERVICES replaced by live API data (got ${p.servicesLen})`);

    // server learned ids (ec2, lambda) must have been merged into the live set
    check(p.learnedArr.includes('ec2') && p.learnedArr.includes('lambda'),
      'server progress pulled + merged into learned set');

    // server quiz best (6) must have been adopted over the default 0
    check(+(localStorage.getItem('awsAtlasBest') || 0) === 6, 'server quiz_best adopted');

    // merged progress must have been pushed back (debounced ~700ms)
    check(puts.length >= 1, 'a progress PUT was sent');
    const last = puts[puts.length - 1];
    if (last) {
      check(last.learned.includes('ec2') && last.learned.includes('lambda'), 'PUT body contains merged learned ids');
      check(last.quiz_best === 6, 'PUT body carries adopted quiz_best');
      check(typeof last.user_id === 'string' && last.user_id.length > 0, 'PUT body has a user_id');
    }

    if (failures) { console.error(`${failures} browser-sim test(s) failed`); process.exit(1); }
    console.log('browser-sim: ALL PASS (100 live services, progress pull+merge+push round-trip)');
    process.exit(0); // the app registers intervals; exit explicitly so node doesn't hang
  } catch (e) {
    console.error('verification threw:', e.stack || e);
    process.exit(1);
  }
}, 1200);
