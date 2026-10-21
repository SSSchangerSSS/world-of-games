// Node harness: runs pure-logic unit tests for every game in the manifest.
// Usage: node test_logic.mjs <dir-or-path-with-tests-manifest.json>
import fs from 'fs';

const dir = process.argv[2] || '.';
const mfPath = dir.endsWith('.json') ? dir : dir + '/tests-manifest.json';
const manifest = JSON.parse(fs.readFileSync(mfPath, 'utf8'));

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const T = {
  ok(c, m) { if (!c) throw new Error(m || 'assert failed'); },
  eq(a, b, m) {
    const ja = JSON.stringify(a), jb = JSON.stringify(b);
    if (ja !== jb) throw new Error((m || 'eq') + ' → ' + ja + ' !== ' + jb);
  },
  approx(a, b, e, m) {
    if (Math.abs(a - b) > (e || 1e-9)) throw new Error((m || 'approx') + ': ' + a + ' ~ ' + b);
  },
  throws(f, m) { let t = 0; try { f(); } catch (e) { t = 1; } if (!t) throw new Error(m || 'expected throw'); },
  near(a, b, d, m) { if (Math.abs(a - b) > d) throw new Error((m || 'near') + ': |' + a + '-' + b + '|>' + d); },
};

let P = 0, F = 0; const fails = [];
for (const g of manifest) {
  if (!g.tests || !g.tests.length) continue;
  let L = null;
  try {
    L = new Function('store', (g.enginesJs || '') + '\n' + g.logic + '\n;return typeof WOG_LOGIC==="undefined"?null:WOG_LOGIC;')({});
    if (!L) throw new Error('WOG_LOGIC not defined');
  } catch (e) {
    F += g.tests.length; fails.push(g.slug + ' › LOADING LOGIC :: ' + e.message); continue;
  }
  for (const t of g.tests) {
    try {
      const fn = new Function('T', 'L', 'rng', t.js);
      fn(T, L, mulberry32(g.seed || 12345));
      P++;
    } catch (e) {
      F++; fails.push(g.slug + ' › ' + t.name + ' :: ' + e.message);
    }
  }
}
console.log('LOGIC TESTS: pass=' + P + ' fail=' + F + (F ? '\n' + fails.slice(0, 60).join('\n') : ''));
process.exit(F ? 1 : 0);
