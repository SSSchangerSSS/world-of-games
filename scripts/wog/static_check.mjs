// Static cross-check in Node: evaluate WOG_LOGIC per game, verify L.<fn> usages
// in the rendered UI and engine-function usage vs engines actually embedded.
import fs from 'fs';
import path from 'path';

const root = process.argv[2] || '/home/z/my-project/pages-site';
const gamesDir = path.join(root, 'games');
const slugs = fs.readdirSync(gamesDir).filter(s =>
  fs.statSync(path.join(gamesDir, s)).isDirectory());

const ENGINE_FNS = {
  common: ['ce', 'fa', 'shuffle', 'rint', 'pick', 'clamp', 'toast', 'hud', 'ovl', 'bestOf', 'storeBest'],
  card: ['makeDeck', 'isRed', 'suitOf', 'rankShort', 'rankFa', 'cardEl', 'cardStack'],
  arcade: ['makeCanvas', 'keyState', 'bindPad', 'rafStep'],
  word: ['normFa', 'faKb'],
};
const ENGINE_MARK = {
  card: 'var SUITS=', arcade: 'function makeCanvas', word: 'var FA_LETTERS=',
};

let problems = 0;
for (const slug of slugs) {
  const file = path.join(gamesDir, slug, 'index.html');
  let html;
  try { html = fs.readFileSync(file, 'utf8'); } catch { continue; }
  const errs = [];
  // extract whole script
  const sm = html.match(/<script>\n([\s\S]*?)<\/script>/);
  if (!sm) { console.log('---', slug, ':: no inline script'); problems++; continue; }
  const script = sm[1];
  // split logic vs ui
  const li = script.indexOf('/*WOG_LOGIC_START*/');
  const le = script.indexOf('/*WOG_LOGIC_END*/');
  const uiStart = script.indexOf('var L = WOG_LOGIC;');
  if (li < 0 || le < 0 || uiStart < 0) { console.log('---', slug, ':: markers missing'); problems++; continue; }
  const logic = script.slice(li + 20, le);
  const ui = script.slice(uiStart + 'var L = WOG_LOGIC;'.length);

  // engines present
  const engines = ['common'];
  for (const [e, mark] of Object.entries(ENGINE_MARK)) if (script.includes(mark)) engines.push(e);

  // evaluate logic
  let keys = null, evalErr = null;
  try {
    const fn = new Function('store',
      logic + '\n;return typeof WOG_LOGIC==="undefined"?null:(typeof WOG_LOGIC==="function"?WOG_LOGIC:WOG_LOGIC);')({});
    const W = fn;
    keys = W ? Object.keys(typeof W === 'function' ? W() || {} : W) : null;
  } catch (e) { evalErr = e.message; }
  if (evalErr) {
    errs.push('LOGIC EVAL: ' + evalErr.slice(0, 150));
  } else if (!keys) {
    errs.push('WOG_LOGIC missing (maybe IIFE returning fn)');
  }

  // L.<fn> usages
  const usedL = new Set();
  for (const m of ui.matchAll(/\bL\.([A-Za-z_$][\w$]*)/g)) usedL.add(m[1]);
  if (keys) {
    // IIFE WOG_LOGIC that returns a function: treat keys of returned obj if fn
    const miss = [...usedL].filter(k => !keys.includes(k));
    if (miss.length) errs.push('L.' + miss.join(', L.') + ' used but not exported');
  }

  // engine fn usage
  for (const [e, fns] of Object.entries(ENGINE_FNS)) {
    if (engines.includes(e)) continue;
    for (const fnName of fns) {
      if (new RegExp('(?<![.\\w])' + fnName + '\\s*\\(').test(ui)) {
        errs.push('uses ' + fnName + '() without ' + e + ' engine');
        break;
      }
    }
  }

  if (errs.length) {
    problems++;
    console.log('---', slug);
    errs.forEach(e => console.log('    ', e));
  }
}
console.log('NODE STATIC CHECK: %s problems across %d games', problems, slugs.length);
process.exit(problems ? 1 : 0);
