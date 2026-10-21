# -*- coding: utf-8 -*-
"""AG-B3 - 4 luck games (lcr, rps, slots, wheel) as ONE batch per mini-kit contract."""
from lib_mini import G

# ==================================================================== lcr
LCR_LOGIC = r"""
var WOG_LOGIC = (function () {
  var PLAYERS = 3;
  var FACES = ['L', 'C', 'R', '.', '.', '.'];
  function roll3(rng) {
    var r = rng || Math.random, out = [], i;
    for (i = 0; i < 3; i++) out.push(FACES[Math.floor(r() * 6)]);
    return out;
  }
  function nextAlive(st, from) {
    var i = from, k;
    for (k = 0; k < PLAYERS; k++) {
      i = (i + 1) % PLAYERS;
      if (st.chips[i] > 0) return i;
    }
    return from;
  }
  function initial() { return { chips: [3, 3, 3], pot: 0, turn: 0, rolls: 0, last: null }; }
  function applyRoll(st, roller, rng) {
    var dice = roll3(rng);
    var passes = { left: 0, center: 0, right: 0, keep: 0 };
    var left = (roller + PLAYERS - 1) % PLAYERS;
    var right = (roller + 1) % PLAYERS;
    var i, d;
    for (i = 0; i < dice.length; i++) {
      d = dice[i];
      if (d === 'L' && st.chips[roller] > 0) { st.chips[roller]--; st.chips[left]++; passes.left++; }
      else if (d === 'R' && st.chips[roller] > 0) { st.chips[roller]--; st.chips[right]++; passes.right++; }
      else if (d === 'C' && st.chips[roller] > 0) { st.chips[roller]--; st.pot++; passes.center++; }
      else { passes.keep++; }
    }
    st.rolls++;
    st.last = { roller: roller, dice: dice };
    st.turn = nextAlive(st, roller);
    return { dice: dice, passes: passes, extra: null };
  }
  function holders(st) { var n = 0, i; for (i = 0; i < PLAYERS; i++) { if (st.chips[i] > 0) n++; } return n; }
  function isOver(st) { return holders(st) === 1; }
  function winner(st) { var i; for (i = 0; i < PLAYERS; i++) { if (st.chips[i] > 0) return i; } return -1; }
  return { PLAYERS: PLAYERS, FACES: FACES, initial: initial, roll3: roll3, nextAlive: nextAlive, applyRoll: applyRoll, holders: holders, isOver: isOver, winner: winner };
})();
"""

LCR_UI = r"""
var st = L.initial();
var timer = null;
var NAMES = ['شما', 'ربات ۱', 'ربات ۲'];
function faceFa(f) { return f === 'L' ? 'چ' : (f === 'C' ? 'و' : (f === 'R' ? 'ر' : '•')); }
function dots(n) { var s = '', i; for (i = 0; i < n; i++) s += '<i class="chip"></i>'; return n ? s : '<span class="zero">—</span>'; }
function diceHtml() {
  var s = '', k;
  if (!st.last) return '';
  for (k = 0; k < st.last.dice.length; k++) s += '<div class="die">' + faceFa(st.last.dice[k]) + '</div>';
  return '<div class="dicewrap"><span class="dlabel">تاس ' + NAMES[st.last.roller] + ':</span>' + s + '</div>';
}
function render(msg) {
  var over = L.isOver(st), h = '<div class="pot">دیگ وسط: <b>' + fa(st.pot) + '</b> چیپ</div><div class="row">';
  var i;
  for (i = 0; i < L.PLAYERS; i++) {
    h += '<div class="pcard' + (i === 0 ? ' me' : '') + (!over && st.turn === i ? ' active' : '') + '"><div class="pname">' + NAMES[i] + '</div><div class="chips">' + dots(st.chips[i]) + '</div><div class="pnum">' + fa(st.chips[i]) + ' چیپ</div></div>';
  }
  h += '</div>' + diceHtml();
  h += '<div class="btns"><button id="roll" class="btn primary" data-smoke' + (!over && st.turn === 0 ? '' : ' disabled') + '>پرتاب تاس</button><button id="new" class="btn" data-smoke>بازی جدید</button></div>';
  if (msg) h += '<div class="msg">' + msg + '</div>';
  $('#app').innerHTML = h;
  $('#roll').onclick = humanRoll;
  $('#new').onclick = newGame;
  hud('دیگ: ' + fa(st.pot) + ' · چیپ تو: ' + fa(st.chips[0]));
}
function humanRoll() { if (!L.isOver(st) && st.turn === 0) play(0); }
function play(roller) {
  var res = L.applyRoll(st, roller);
  render('تاس ' + NAMES[roller] + ': ' + res.dice.map(faceFa).join(' '));
  if (L.isOver(st)) endGame(L.winner(st));
  else if (st.turn !== 0) timer = setTimeout(aiStep, 750);
}
function aiStep() { if (!L.isOver(st) && st.turn !== 0) play(st.turn); }
function endGame(w) {
  if (w === 0) store.set('wog-lcr-wins', String(parseInt(store.get('wog-lcr-wins') || '0', 10) + 1));
  ovl(w === 0 ? 'بردی!' : 'باختی!', NAMES[w] + ' صاحب همهٔ چیپ‌ها شد: ' + fa(st.chips[w] + st.pot) + ' چیپ (دیگ: ' + fa(st.pot) + ')', 'بازی جدید', newGame);
}
function newGame() { if (timer) { clearTimeout(timer); timer = null; } st = L.initial(); render('بازی جدید؛ شروع با تو'); }
$('#hint').textContent = 'روی نوبتت ۳ تاس بریز: چ یک چیپ به بازیکن چپ، ر به راست و و به دیگ می‌دهد؛ نقطه یعنی چیپ می‌ماند. بازیکن بی‌چیپ رد می‌شود و آخرین نفرِ دارای چیپ، دیگ را می‌بَرد.';
render('');
"""

LCR_CSS = r"""
.pot{text-align:center;font-size:18px;margin:8px 0;color:#d9a441}
.row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.pcard{background:#14203a;border:1px solid #2c3f6b;border-radius:12px;padding:10px 12px;min-width:96px;text-align:center;opacity:.55}
.pcard.active{opacity:1;border-color:#d9a441;box-shadow:0 0 10px rgba(217,164,65,.35)}
.pcard.me .pname{color:#3fb8af}
.pname{font-weight:700;margin-bottom:6px}
.chips{min-height:20px;line-height:20px}
.chip{display:inline-block;width:12px;height:12px;border-radius:50%;background:#d9a441;margin:0 1px;border:1px solid #8a6a25}
.zero{color:#5a6c94}
.pnum{font-size:12px;color:#9fb0d8;margin-top:4px}
.dicewrap{display:flex;gap:8px;align-items:center;justify-content:center;margin:12px 0;flex-wrap:wrap}
.dlabel{color:#9fb0d8}
.die{width:46px;height:46px;border-radius:10px;background:#22345c;border:2px solid #d9a441;color:#fff;font-size:20px;font-weight:700;display:flex;align-items:center;justify-content:center}
.btns{display:flex;gap:10px;justify-content:center;margin:12px 0;flex-wrap:wrap}
.btn{min-height:44px;padding:10px 22px;font-size:16px;border-radius:10px;background:#1b2b4d;color:#e8edf7;border:1px solid #2c3f6b;cursor:pointer;touch-action:manipulation}
.btn.primary{background:#d9a441;color:#14203a;font-weight:700}
.btn:disabled{opacity:.45;cursor:default}
.msg{text-align:center;color:#67b98a;min-height:22px;margin-top:6px}
"""

LCR_TESTS = [
("حفظ چیپ‌ها در ۱۰۰۰ پرتاب", r"""
var st = L.initial(), done = 0, i, r;
function mr(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}}
for (i = 0; i < 1000; i++) {
  if (L.isOver(st)) st = L.initial();
  r = st.turn;
  T.ok(st.chips[r] > 0, 'roller holds a chip');
  L.applyRoll(st, r, mr(1000 + i));
  T.eq(st.chips[0] + st.chips[1] + st.chips[2] + st.pot, 9, 'chip conservation');
  T.ok(st.chips[r] >= 0, 'no negative chips');
  if (!L.isOver(st)) T.ok(st.chips[st.turn] > 0, 'empty player skipped in rotation');
  done++;
}
T.eq(done, 1000, '1000 rolls executed');
"""),
("رد شدن بازیکن بدون چیپ", r"""
function stub(v){return function(){return v}}
var st = { chips: [0, 2, 1], pot: 6, turn: 2, rolls: 0, last: null };
var res = L.applyRoll(st, 2, stub(0.2));
T.eq(res.passes.center, 1, 'single chip to pot');
T.eq(st.chips[2], 0, 'roller emptied');
T.eq(st.pot, 7, 'pot grew by one');
T.eq(st.chips[1], 2, 'middle untouched');
T.eq(st.turn, 1, 'empty player 0 skipped, turn to player 1');
T.eq(st.chips[0] + st.chips[1] + st.chips[2] + st.pot, 9, 'conservation');
"""),
("سقف پاس چیپ به اندازهٔ دارایی", r"""
function stub(v){return function(){return v}}
var st = { chips: [1, 3, 3], pot: 2, turn: 0, rolls: 0, last: null };
var res = L.applyRoll(st, 0, stub(0.2));
T.eq(res.passes.center, 1, 'capped at held chips');
T.eq(st.chips[0], 0, 'emptied not negative');
T.eq(st.pot, 3, 'pot +1 only');
T.eq(res.passes.keep, 2, 'rest kept');
T.eq(st.chips[0] + st.chips[1] + st.chips[2] + st.pot, 9, 'conservation');
T.eq(st.turn, 1, 'next alive player');
"""),
("اعتبار تاس‌ها و وجوه", r"""
var seen = { L: 0, C: 0, R: 0, '.': 0 }, i, j, d;
T.eq(L.FACES.length, 6, 'six faces');
T.eq(L.FACES.filter(function (f) { return f === '.'; }).length, 3, 'three dot faces');
T.eq(L.FACES.filter(function (f) { return f === 'L'; }).length, 1, 'one L face');
for (i = 0; i < 500; i++) {
  d = L.roll3(rng);
  T.eq(d.length, 3, '3 dice');
  for (j = 0; j < 3; j++) { T.ok(d[j] === 'L' || d[j] === 'C' || d[j] === 'R' || d[j] === '.', 'valid face'); seen[d[j]]++; }
}
T.ok(seen['.'] > seen.L * 2, 'dots dominate');
"""),
("پایان بازی روی ۳۰ بذر و برندهٔ کل ۹", r"""
function mr(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}}
var s, i, w, others, count = 0;
for (s = 1; s <= 30; s++) {
  var st = L.initial(), r = mr(s * 7919 + 13), n = 0;
  while (!L.isOver(st) && n < 3000) { L.applyRoll(st, st.turn, r); n++; }
  T.ok(L.isOver(st), 'terminated seed ' + s);
  T.ok(n < 3000, 'under roll cap seed ' + s + ' rolls=' + n);
  w = L.winner(st);
  T.ok(w >= 0 && w < 3, 'winner index seed ' + s);
  T.eq(st.chips[w] + st.pot, 9, 'winner takes all nine seed ' + s);
  others = 0;
  for (i = 0; i < 3; i++) { if (i !== w) others += st.chips[i]; }
  T.eq(others, 0, 'losers empty seed ' + s);
  T.ok(st.chips[w] > 0, 'winner holds chips seed ' + s);
  count++;
}
T.eq(count, 30, 'all seeds simulated');
"""),
("شکل نتیجه و بدون دور اضافه", r"""
function stub(v){return function(){return v}}
var st = L.initial();
var res = L.applyRoll(st, 0, stub(0.99));
T.eq(res.passes.keep, 3, 'three keeps');
T.eq(res.extra, null, 'no extra roll');
T.eq(res.passes.left + res.passes.center + res.passes.right, 0, 'nothing moved');
T.eq(st.turn, 1, 'turn advanced');
T.eq(st.rolls, 1, 'roll counted');
T.ok(st.last && st.last.roller === 0 && st.last.dice.length === 3, 'last roll recorded');
"""),
]

# ==================================================================== rps
RPS_LOGIC = r"""
var WOG_LOGIC = (function () {
  var MOVES = ['s', 'p', 'sc'];
  var BEATS = { s: 'sc', sc: 'p', p: 's' };
  function counter(move) { for (var k in BEATS) { if (BEATS[k] === move) return k; } return null; }
  function aiPick(history, rng) {
    var r = rng || Math.random, counts = { s: 0, p: 0, sc: 0 }, i, best = null, bestN = 0;
    for (i = 0; i < history.length; i++) { if (counts[history[i]] !== undefined) counts[history[i]]++; }
    for (i = 0; i < MOVES.length; i++) { if (counts[MOVES[i]] > bestN) { bestN = counts[MOVES[i]]; best = MOVES[i]; } }
    if (bestN <= 0 || r() < 0.2) return MOVES[Math.floor(r() * 3)];
    return counter(best);
  }
  function judge(a, b) { if (a === b) return 0; return BEATS[a] === b ? 1 : -1; }
  function matchOver(sa, sb) { return sa >= 3 || sb >= 3; }
  return { MOVES: MOVES, BEATS: BEATS, counter: counter, aiPick: aiPick, judge: judge, matchOver: matchOver };
})();
"""

RPS_UI = r"""
var sa = 0, sb = 0, hist = [], trail = [], done = false, lastMe = null, lastAi = null;
var MOVE_FA = { s: 'سنگ', p: 'کاغذ', sc: 'قیچی' };
function render(msg) {
  var h = '<div class="score"><div class="side"><span>شما</span><b>' + fa(sa) + '</b></div><div class="mid">تا ۳ برد</div><div class="side ai"><span>ربات</span><b>' + fa(sb) + '</b></div></div>';
  var t = '', i, from = Math.max(0, trail.length - 15);
  for (i = from; i < trail.length; i++) t += '<span class="dot ' + trail[i] + '"></span>';
  h += '<div class="trail">' + (t || '<span class="mut">هنوز دستی بازی نشده</span>') + '</div>';
  h += '<div class="faceoff"><div>تو: <b>' + (lastMe ? MOVE_FA[lastMe] : '—') + '</b></div><div class="mut">مقابل</div><div>ربات: <b>' + (lastAi ? MOVE_FA[lastAi] : '—') + '</b></div></div>';
  h += '<div class="btns">';
  for (i = 0; i < L.MOVES.length; i++) h += '<button id="mv' + i + '" class="btn primary"' + (i === 0 ? ' data-smoke' : '') + (done ? ' disabled' : '') + '>' + MOVE_FA[L.MOVES[i]] + '</button>';
  h += '<button id="new" class="btn" data-smoke>بازی جدید</button></div>';
  if (msg) h += '<div class="msg">' + msg + '</div>';
  $('#app').innerHTML = h;
  for (i = 0; i < L.MOVES.length; i++) {
    (function (idx) { $('#mv' + idx).onclick = function () { play(L.MOVES[idx]); }; })(i);
  }
  $('#new').onclick = newGame;
}
function play(m) {
  if (done) return;
  var ai = L.aiPick(hist), j = L.judge(m, ai);
  hist.push(m);
  lastMe = m; lastAi = ai;
  if (j === 1) { sa++; trail.push('w'); } else if (j === -1) { sb++; trail.push('l'); } else { trail.push('d'); }
  render(MOVE_FA[m] + ' در برابر ' + MOVE_FA[ai] + ' — ' + (j === 1 ? 'برد این دست!' : (j === -1 ? 'باخت این دست' : 'مساوی')));
  hud('تو ' + fa(sa) + ' – ' + fa(sb) + ' ربات');
  if (L.matchOver(sa, sb)) {
    done = true;
    if (sa > sb) store.set('wog-rps-wins', String(parseInt(store.get('wog-rps-wins') || '0', 10) + 1));
    setTimeout(function () { ovl(sa > sb ? 'بردی!' : 'باختی!', 'نتیجهٔ مسابقه: ' + fa(sa) + ' – ' + fa(sb) + ' در ' + fa(trail.length) + ' دست', 'بازی جدید', newGame); }, 300);
  }
}
function newGame() { sa = 0; sb = 0; hist = []; trail = []; done = false; lastMe = null; lastAi = null; render('مسابقهٔ جدید؛ اولین ۳ برد برنده است'); hud('تو ۰ – ۰ ربات'); }
$('#hint').textContent = 'سنگ قیچی را می‌بُرد، قیچی کاغذ را و کاغذ سنگ را؛ هر کس زودتر ۳ دست ببرد برندهٔ مسابقه است. حواست باشد: ربات حرکت‌های پرتکرار تو را می‌شمارد و علیه‌ات می‌چیند!';
render('انتخاب کن!');
hud('تو ۰ – ۰ ربات');
"""

RPS_CSS = r"""
.score{display:flex;align-items:center;justify-content:center;gap:14px;margin:10px 0}
.side{background:#14203a;border:1px solid #2c3f6b;border-radius:12px;padding:8px 18px;text-align:center;min-width:88px}
.side span{display:block;font-size:12px;color:#9fb0d8}
.side b{font-size:26px;color:#d9a441}
.side.ai b{color:#e26d5c}
.mid{color:#9fb0d8;font-size:13px}
.trail{text-align:center;margin:10px 0;min-height:24px}
.dot{display:inline-block;width:14px;height:14px;border-radius:50%;margin:0 3px;vertical-align:middle}
.dot.w{background:#d9a441}
.dot.l{background:#e26d5c}
.dot.d{background:#5a6c94}
.mut{color:#5a6c94;font-size:12px}
.faceoff{display:flex;justify-content:center;align-items:center;gap:18px;margin:10px 0;font-size:15px;flex-wrap:wrap}
.faceoff b{color:#3fb8af}
.btns{display:flex;gap:10px;justify-content:center;margin:14px 0;flex-wrap:wrap}
.btn{min-height:48px;min-width:96px;padding:10px 20px;font-size:16px;border-radius:10px;background:#1b2b4d;color:#e8edf7;border:1px solid #2c3f6b;cursor:pointer;touch-action:manipulation}
.btn.primary{background:#d9a441;color:#14203a;font-weight:700}
.btn:disabled{opacity:.45;cursor:default}
.msg{text-align:center;color:#67b98a;min-height:22px}
"""

RPS_TESTS = [
("رابطهٔ شکست کامل", r"""
var mv = L.MOVES, i, k, beatenBy;
T.eq(mv.length, 3, 'three moves');
T.ok(mv.indexOf('s') >= 0 && mv.indexOf('p') >= 0 && mv.indexOf('sc') >= 0, 's p sc present');
for (i = 0; i < 3; i++) {
  T.ok(L.BEATS[mv[i]] !== mv[i], 'no self-beat');
  T.ok(mv.indexOf(L.BEATS[mv[i]]) >= 0, 'beats a valid move');
  beatenBy = 0;
  for (k in L.BEATS) { if (L.BEATS[k] === mv[i]) beatenBy++; }
  T.eq(beatenBy, 1, mv[i] + ' beaten by exactly one');
}
"""),
("صحت counter", r"""
T.eq(L.counter('s'), 'p', 'paper beats rock');
T.eq(L.counter('p'), 'sc', 'scissors beat paper');
T.eq(L.counter('sc'), 's', 'rock beats scissors');
var k;
for (k in L.BEATS) { T.eq(L.counter(L.BEATS[k]), k, 'counter inverts beats'); }
"""),
("داوری و تقارن", r"""
T.eq(L.judge('s', 'sc'), 1, 'rock beats scissors');
T.eq(L.judge('p', 's'), 1, 'paper beats rock');
T.eq(L.judge('sc', 'p'), 1, 'scissors beat paper');
T.eq(L.judge('s', 's'), 0, 'tie rock');
T.eq(L.judge('p', 'p'), 0, 'tie paper');
T.eq(L.judge('sc', 'sc'), 0, 'tie scissors');
var mv = L.MOVES, i, j;
for (i = 0; i < 3; i++) { for (j = 0; j < 3; j++) { T.ok(L.judge(mv[i], mv[j]) === -L.judge(mv[j], mv[i]), 'antisymmetry'); } }
"""),
("ربات مقابل حرکت غالب", r"""
var hist = [], i, cnt = { s: 0, p: 0, sc: 0 };
for (i = 0; i < 20; i++) hist.push('s');
for (i = 0; i < 100; i++) cnt[L.aiPick(hist, rng)]++;
T.ok(cnt.p > 60, 'counters majority rock, p=' + cnt.p);
T.ok(cnt.p > cnt.s && cnt.p > cnt.sc, 'paper dominant');
"""),
("تشخیص پایان مسابقه", r"""
T.ok(L.matchOver(3, 0), '3-0 over');
T.ok(L.matchOver(0, 3), '0-3 over');
T.ok(L.matchOver(2, 3), '2-3 over');
T.ok(!L.matchOver(2, 2), '2-2 continues');
T.ok(!L.matchOver(0, 0), '0-0 continues');
T.ok(!L.matchOver(2, 1), '2-1 continues');
"""),
("مسابقهٔ کامل با بذر", r"""
function mr(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}}
var r = mr(4242), mv = L.MOVES, sa = 0, sb = 0, hist = [], n = 0, a, b, j;
while (!L.matchOver(sa, sb) && n < 200) {
  a = mv[Math.floor(r() * 3)];
  b = L.aiPick(hist, r);
  hist.push(a);
  j = L.judge(a, b);
  if (j === 1) sa++; else if (j === -1) sb++;
  n++;
}
T.ok(L.matchOver(sa, sb), 'match finished');
T.ok(n < 200, 'terminates quickly, rounds=' + n);
T.ok(sa === 3 || sb === 3, 'winner reached three');
T.eq(hist.length, n, 'history tracks rounds');
"""),
]

# ==================================================================== slots
SLOTS_LOGIC = r"""
var WOG_LOGIC = (function () {
  var SYMS = ['⬤', '▲', '★', '◆', '❋', '♣'];
  var WEIGHTS = [6, 5, 4, 3, 2, 2];
  var TRIPLE_VALS = [8, 6, 50, 25, 15, 10];
  var REELS = [[], [], []], TRIPLE = {}, i, j;
  for (i = 0; i < SYMS.length; i++) {
    TRIPLE[SYMS[i]] = TRIPLE_VALS[i];
    for (j = 0; j < WEIGHTS[i]; j++) { REELS[0].push(SYMS[i]); REELS[1].push(SYMS[i]); REELS[2].push(SYMS[i]); }
  }
  function pick1(rng) { var r = rng || Math.random; return REELS[0][Math.floor(r() * REELS[0].length)]; }
  function spin(rng) { return [pick1(rng), pick1(rng), pick1(rng)]; }
  function payout(reels) {
    var a = reels[0], b = reels[1], c = reels[2], pair = null;
    if (a === b && b === c) return TRIPLE[a] || 0;
    if (a === b || a === c) pair = a; else if (b === c) pair = b;
    if (pair === null) return 0;
    return pair === '★' ? 3 : 2;
  }
  function ev(n) { var s = 0, k; for (k = 0; k < n; k++) s += payout(spin()); return s / n; }
  return { SYMS: SYMS, WEIGHTS: WEIGHTS, REELS: REELS, TRIPLE: TRIPLE, COST: 5, pick1: pick1, spin: spin, payout: payout, ev: ev };
})();
"""

SLOTS_UI = r"""
var credits = 100, busy = false, reels = null;
function render(msg) {
  var r = reels ? reels : ['؟', '؟', '؟'];
  var h = '<div class="machine' + (busy ? ' go' : '') + '"><div class="reels">';
  var i, pt;
  for (i = 0; i < 3; i++) h += '<div class="reel"><span>' + r[i] + '</span></div>';
  h += '</div><div class="pline"></div></div>';
  h += '<div class="btns"><button id="spin" class="btn primary" data-smoke' + (busy || credits < L.COST ? ' disabled' : '') + '>چرخش (' + fa(L.COST) + ' اعتبار)</button><button id="new" class="btn" data-smoke>شروع مجدد با ' + fa(100) + '</button></div>';
  pt = '';
  for (i = 0; i < L.SYMS.length; i++) pt += '<span class="pi">' + L.SYMS[i] + L.SYMS[i] + L.SYMS[i] + '=' + fa(L.TRIPLE[L.SYMS[i]]) + '</span>';
  h += '<div class="paytable"><b>جوایز:</b> ' + pt + '<span class="pi">دو ' + L.SYMS[2] + '=۳</span><span class="pi">جفت دیگر=۲</span></div>';
  if (msg) h += '<div class="msg">' + msg + '</div>';
  $('#app').innerHTML = h;
  $('#spin').onclick = doSpin;
  $('#new').onclick = newGame;
  hud('اعتبار: ' + fa(credits) + ' · رکورد: ' + fa(store.get('wog-slots-best') || '0'));
}
function doSpin() {
  if (busy || credits < L.COST) return;
  busy = true;
  credits -= L.COST;
  render('در حال چرخش…');
  setTimeout(function () {
    var p;
    reels = L.spin();
    p = L.payout(reels);
    credits += p;
    busy = false;
    if (credits > parseInt(store.get('wog-slots-best') || '0', 10)) store.set('wog-slots-best', String(credits));
    render(p > 0 ? 'برد: ' + fa(p) + ' اعتبار!' : 'جایزه‌ای نبود؛ دوباره بچرخان');
    if (credits < L.COST) setTimeout(function () { ovl('اعتبار تمام شد', 'اعتبار نهایی تو: ' + fa(credits), 'شروع مجدد با ۱۰۰', newGame); }, 350);
  }, 700);
}
function newGame() { credits = 100; reels = null; busy = false; render('اعتبار دوباره ' + fa(100) + ' شد'); }
$('#hint').textContent = 'هر چرخش ۵ اعتبار دارد؛ سه نماد یکسان روی خط برد جایزه می‌دهد. ستاره گران‌بهاترین نماد است و دو ستاره هم ۳ اعتبار می‌دهد.';
render('');
hud('اعتبار: ' + fa(credits));
"""

SLOTS_CSS = r"""
.machine{max-width:360px;margin:12px auto;background:#14203a;border:2px solid #d9a441;border-radius:16px;padding:16px}
.reels{display:flex;gap:10px;justify-content:center}
.reel{width:84px;height:84px;background:#0d1730;border:2px solid #2c3f6b;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:42px;color:#fff}
.pline{height:3px;background:#d9a441;border-radius:2px;margin:8px 10px 0}
.machine.go .reel span{display:inline-block;animation:jig .12s linear 5}
@keyframes jig{0%{transform:translateY(-8px)}50%{transform:translateY(8px)}100%{transform:translateY(0)}}
.paytable{max-width:440px;margin:10px auto;text-align:center;color:#9fb0d8;font-size:13px;line-height:2}
.pi{display:inline-block;background:#14203a;border:1px solid #2c3f6b;border-radius:8px;padding:2px 8px;margin:2px;color:#e8edf7}
.btns{display:flex;gap:10px;justify-content:center;margin:14px 0;flex-wrap:wrap}
.btn{min-height:48px;min-width:120px;padding:10px 20px;font-size:16px;border-radius:10px;background:#1b2b4d;color:#e8edf7;border:1px solid #2c3f6b;cursor:pointer;touch-action:manipulation}
.btn.primary{background:#d9a441;color:#14203a;font-weight:700}
.btn:disabled{opacity:.45;cursor:default}
.msg{text-align:center;color:#67b98a;min-height:22px}
"""

SLOTS_TESTS = [
("جدول پرداخت سه‌برابر", r"""
var S = L.SYMS, tab = [[2, 50], [3, 25], [4, 15], [5, 10], [0, 8], [1, 6]], i;
for (i = 0; i < tab.length; i++) T.eq(L.payout([S[tab[i][0]], S[tab[i][0]], S[tab[i][0]]]), tab[i][1], 'triple of ' + S[tab[i][0]]);
"""),
("جفت و بدون جایزه", r"""
var S = L.SYMS, st = S[2];
T.eq(L.payout([st, st, S[0]]), 3, 'two stars positions 1-2');
T.eq(L.payout([st, S[0], st]), 3, 'two stars positions 1-3');
T.eq(L.payout([S[0], st, st]), 3, 'two stars positions 2-3');
T.eq(L.payout([S[0], S[0], S[1]]), 2, 'pair circles');
T.eq(L.payout([S[1], S[3], S[3]]), 2, 'pair diamonds');
T.eq(L.payout([st, S[0], S[0]]), 2, 'pair circles with single star');
T.eq(L.payout([S[0], S[1], S[5]]), 0, 'all different');
T.eq(L.payout([S[3], st, S[4]]), 0, 'all different 2');
"""),
("توزیع وزنی قرقره", r"""
var cnt = {}, i, s, N = 20000;
for (i = 0; i < L.SYMS.length; i++) cnt[L.SYMS[i]] = 0;
for (i = 0; i < N; i++) cnt[L.spin(rng)[0]]++;
for (i = 0; i < L.SYMS.length; i++) {
  s = L.SYMS[i];
  var exp = L.WEIGHTS[i] / 22 * N;
  T.near(cnt[s], exp, exp * 0.15, 'weight ' + s + ' expected ' + Math.round(exp) + ' got ' + cnt[s]);
}
T.eq(L.REELS[0].length, 22, 'reel size 22');
"""),
("برتری خانه در ۵۰۰۰ چرخ", r"""
var sum = 0, N = 5000, i;
for (i = 0; i < N; i++) sum += L.payout(L.spin(rng));
T.ok(sum < 5 * N, 'house edge holds, mean=' + (sum / N));
T.ok(sum > 0.5 * N, 'paytable alive, mean=' + (sum / N));
"""),
("ساختار چرخش و جدول وزن", r"""
var wsum = 0, i, sp;
for (i = 0; i < L.WEIGHTS.length; i++) wsum += L.WEIGHTS[i];
T.eq(wsum, 22, 'weights sum 22');
T.eq(L.REELS.length, 3, 'three reels');
T.eq(L.COST, 5, 'spin cost 5');
sp = L.spin(rng);
T.eq(sp.length, 3, 'spin triplet');
for (i = 0; i < 3; i++) T.ok(L.SYMS.indexOf(sp[i]) >= 0, 'valid symbol');
"""),
("پرداخت همیشه از جدول", r"""
var ok = { 0: 1, 2: 1, 3: 1, 6: 1, 8: 1, 10: 1, 15: 1, 25: 1, 50: 1 }, i, p;
for (i = 0; i < 3000; i++) { p = L.payout(L.spin(rng)); T.ok(ok[p] === 1, 'payout in table: ' + p); }
"""),
]

# ==================================================================== wheel
WHEEL_LOGIC = r"""
var WOG_LOGIC = (function () {
  function seg(label, value, kind, weight) { return { label: label, value: value, kind: kind, weight: weight }; }
  var SEGMENTS = [
    seg('۱۰۰', 100, 'add', 1), seg('ورشکست', 0, 'bust', 1), seg('۲۵۰', 250, 'add', 1),
    seg('نصف', 0, 'half', 1), seg('۱۰۰', 100, 'add', 1), seg('۵۰۰', 500, 'add', 1),
    seg('ورشکست', 0, 'bust', 1), seg('۲۵۰', 250, 'add', 1), seg('×۲', 0, 'x2', 1),
    seg('۱۰۰', 100, 'add', 1), seg('۲۵۰', 250, 'add', 1), seg('۵۰۰', 500, 'add', 1)
  ];
  function spin(rng) {
    var r = rng || Math.random, total = 0, i, x;
    for (i = 0; i < SEGMENTS.length; i++) total += SEGMENTS[i].weight;
    x = r() * total;
    for (i = 0; i < SEGMENTS.length; i++) { x -= SEGMENTS[i].weight; if (x < 0) return i; }
    return SEGMENTS.length - 1;
  }
  function apply(points, segOrIdx) {
    var s = (typeof segOrIdx === 'number') ? SEGMENTS[segOrIdx] : segOrIdx;
    var p = points;
    if (s.kind === 'add') p += s.value;
    else if (s.kind === 'x2') p = p * 2;
    else if (s.kind === 'half') p = Math.floor(p / 2);
    else if (s.kind === 'bust') p = 0;
    if (p < 0) p = 0;
    return p;
  }
  return { SEGMENTS: SEGMENTS, START: 200, spin: spin, apply: apply };
})();
"""

WHEEL_UI = r"""
var pts = L.START, rot = 0, busy = false, history = [], spins = 0;
function build() {
  var n = L.SEGMENTS.length, step = 360 / n, stops = '', i, k, col, w, lb = '';
  for (i = 0; i < n; i++) {
    k = L.SEGMENTS[i].kind;
    col = k === 'bust' ? '#e26d5c' : (k === 'x2' ? '#d9a441' : (k === 'half' ? '#3fb8af' : (i % 2 ? '#1b2b4d' : '#263a66')));
    if (i) stops += ',';
    stops += col + ' ' + (i * step) + 'deg ' + ((i + 1) * step) + 'deg';
  }
  $('#app').innerHTML = '<div class="wwrap"><div class="wpointer"></div><div id="wheel" class="wheel"></div><div class="whub"></div></div><div class="wpanel"><div id="wmsg" class="msg">بچرخان و شانس‌ات را امتحان کن</div><div class="btns"><button id="spin" class="btn primary" data-smoke>چرخاندن گردونه</button><button id="new" class="btn" data-smoke>بازی جدید</button></div><div id="hist" class="hist"></div></div>';
  w = document.getElementById('wheel');
  w.style.background = 'conic-gradient(' + stops + ')';
  for (i = 0; i < n; i++) lb += '<div class="seg" style="transform:rotate(' + (i * step + step / 2) + 'deg)"><span>' + L.SEGMENTS[i].label + '</span></div>';
  w.innerHTML = lb;
  $('#spin').onclick = doSpin;
  $('#new').onclick = newGame;
  update('');
}
function update(msg) {
  $('#wmsg').textContent = msg;
  $('#spin').disabled = busy;
  var hs = '', i;
  for (i = 0; i < history.length; i++) hs += '<span class="hchip">' + history[i].label + ' (' + (history[i].d > 0 ? '+' : '') + fa(history[i].d) + ')</span> ';
  $('#hist').innerHTML = hs ? 'تاریخچه: ' + hs : '';
  hud('امتیاز: ' + fa(pts) + ' · رکورد: ' + fa(store.get('wog-wheel-best') || '0') + ' · چرخش: ' + fa(spins));
}
function doSpin() {
  if (busy) return;
  var idx, n, step, target, cur;
  busy = true;
  update('در حال چرخش…');
  idx = L.spin();
  spins++;
  n = L.SEGMENTS.length; step = 360 / n;
  target = (360 - (idx * step + step / 2)) % 360;
  cur = ((rot % 360) + 360) % 360;
  rot += 360 * 4 + ((target - cur + 360) % 360);
  document.getElementById('wheel').style.transform = 'rotate(' + rot + 'deg)';
  setTimeout(function () {
    var s = L.SEGMENTS[idx], before = pts, msg;
    pts = L.apply(pts, s);
    history.unshift({ label: s.label, d: pts - before });
    if (history.length > 6) history.pop();
    busy = false;
    msg = s.kind === 'bust' ? 'ورشکست! امتیازت صفر شد' : (s.kind === 'x2' ? 'دو برابر شد!' : (s.kind === 'half' ? 'نصف شد!' : ('+' + fa(s.value) + ' امتیاز')));
    update(msg);
    if (pts > parseInt(store.get('wog-wheel-best') || '0', 10)) store.set('wog-wheel-best', String(pts));
    if (pts >= 2000) ovl('شگفت‌انگیز!', 'به ' + fa(pts) + ' امتیاز رسیدی در ' + fa(spins) + ' چرخش', 'بازی جدید', newGame);
  }, 3300);
}
function newGame() { pts = L.START; history = []; spins = 0; busy = false; update('بازی جدید؛ امتیاز دوباره ' + fa(L.START)); }
build();
$('#hint').textContent = 'خانه‌ها جایزهٔ ۱۰۰/۲۵۰/۵۰۰ یا ضربدر۲ و نصف دارند؛ ورشکست امتیاز را صفر می‌کند ولی هیچ‌وقت منفی نمی‌شود. به ۲۰۰۰ امتیاز برس!';
"""

WHEEL_CSS = r"""
.wwrap{position:relative;width:270px;height:270px;margin:16px auto 8px}
.wpointer{position:absolute;top:-10px;left:50%;transform:translateX(-50%);width:0;height:0;border-left:13px solid transparent;border-right:13px solid transparent;border-top:24px solid #d9a441;z-index:3;filter:drop-shadow(0 2px 2px rgba(0,0,0,.5))}
.wheel{width:100%;height:100%;border-radius:50%;border:5px solid #d9a441;position:relative;overflow:hidden;transition:transform 3.2s cubic-bezier(.12,.75,.2,1);box-shadow:0 0 0 5px #14203a,0 8px 24px rgba(0,0,0,.45)}
.seg{position:absolute;left:0;top:0;width:100%;height:100%;display:flex;justify-content:center;pointer-events:none}
.seg span{margin-top:10px;font-size:13px;font-weight:700;color:#fff;text-shadow:0 1px 3px #000}
.whub{position:absolute;left:50%;top:50%;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:#d9a441;border:4px solid #14203a;z-index:2}
.wpanel{max-width:440px;margin:0 auto;text-align:center}
.hist{color:#9fb0d8;font-size:13px;min-height:20px;margin-top:8px}
.hchip{display:inline-block;background:#14203a;border:1px solid #2c3f6b;border-radius:8px;padding:2px 8px;margin:2px}
.btns{display:flex;gap:10px;justify-content:center;margin:14px 0;flex-wrap:wrap}
.btn{min-height:48px;min-width:120px;padding:10px 20px;font-size:16px;border-radius:10px;background:#1b2b4d;color:#e8edf7;border:1px solid #2c3f6b;cursor:pointer;touch-action:manipulation}
.btn.primary{background:#d9a441;color:#14203a;font-weight:700}
.btn:disabled{opacity:.45;cursor:default}
.msg{text-align:center;color:#67b98a;min-height:22px}
"""

WHEEL_TESTS = [
("ساخت گردونه", r"""
T.eq(L.SEGMENTS.length, 12, '12 segments');
var w = 0, kind = {}, i, s;
for (i = 0; i < 12; i++) {
  s = L.SEGMENTS[i];
  T.ok(typeof s.label === 'string' && s.label.length > 0, 'label present');
  T.ok(s.kind === 'add' || s.kind === 'x2' || s.kind === 'half' || s.kind === 'bust', 'kind valid');
  T.ok(s.weight > 0, 'positive weight');
  w += s.weight;
  kind[s.kind] = (kind[s.kind] || 0) + 1;
}
T.eq(w, 12, 'weights sum 12');
T.eq(kind.add, 8, 'eight value segments');
T.eq(kind.x2, 1, 'one double');
T.eq(kind.half, 1, 'one half');
T.eq(kind.bust, 2, 'two bankrupt');
"""),
("شاخص در بازه و توزیع یکنواخت", r"""
var cnt = {}, i, N = 20000;
for (i = 0; i < 12; i++) cnt[i] = 0;
for (i = 0; i < N; i++) { var idx = L.spin(rng); T.ok(idx >= 0 && idx < 12, 'index range'); cnt[idx]++; }
for (i = 0; i < 12; i++) T.near(cnt[i], N / 12, N / 12 * 0.15, 'uniform segment ' + i + ' got ' + cnt[i]);
"""),
("اعمال دقیق خانه‌ها", r"""
function segByKind(k) { for (var i = 0; i < 12; i++) { if (L.SEGMENTS[i].kind === k) return L.SEGMENTS[i]; } return null; }
var a = segByKind('add');
T.eq(L.apply(200, a), 200 + a.value, 'add value');
T.eq(L.apply(200, segByKind('x2')), 400, 'double');
T.eq(L.apply(200, segByKind('half')), 100, 'half');
T.eq(L.apply(201, segByKind('half')), 100, 'half floors down');
T.eq(L.apply(1, segByKind('half')), 0, 'half floors to zero');
T.eq(L.apply(750, segByKind('bust')), 0, 'bust resets');
T.eq(L.apply(0, segByKind('bust')), 0, 'bust at zero');
T.ok(L.apply(0, a) > 0, 'add from zero positive');
"""),
("حسابداری ۱۰۰۰ چرخ", r"""
var pts = L.START, idxs = [], i;
T.eq(pts, 200, 'start 200');
for (i = 0; i < 1000; i++) { var idx = L.spin(rng); idxs.push(idx); pts = L.apply(pts, idx); T.ok(pts >= 0, 'never negative'); T.ok(Number.isInteger(pts), 'integer points'); }
var rep = L.START;
for (i = 0; i < idxs.length; i++) rep = L.apply(rep, idxs[i]);
T.eq(rep, pts, 'replay matches accounting');
"""),
("قطعیت با rng سفارشی", r"""
function stub(v){return function(){return v}}
T.eq(L.spin(stub(0)), 0, 'rng 0 -> first segment');
T.eq(L.spin(stub(0.9999)), 11, 'rng near 1 -> last segment');
var mid = L.spin(stub(0.5));
T.ok(mid >= 0 && mid < 12, 'mid in range');
"""),
("مقادیر و برچسب‌ها", r"""
var vals = [], i, s;
for (i = 0; i < 12; i++) { if (L.SEGMENTS[i].kind === 'add') vals.push(L.SEGMENTS[i].value); }
vals.sort(function (x, y) { return x - y; });
T.eq(JSON.stringify(vals), JSON.stringify([100, 100, 100, 250, 250, 250, 500, 500]), 'value segments');
for (i = 0; i < 12; i++) {
  s = L.SEGMENTS[i];
  if (s.kind === 'bust') T.eq(s.value, 0, 'bust value 0');
  if (s.kind === 'x2' || s.kind === 'half') T.eq(s.value, 0, 'multiplier value 0');
}
"""),
]

GAMES = [
    G("lcr", "چپ وسط راست", "luck", "🎯", "#d9a441", "#3fb8af",
      "تاس چپ‌وسط‌راست با دو ربات: هر تاس چ یک چیپ به چپ، ر به راست و و به دیگ وسط می‌دهد؛ آخرین بازیکنِ دارای چیپ صاحب کل دیگ می‌شود.",
      "روی نوبتت ۳ تاس بریز؛ نقطه یعنی چیپ می‌ماند. با صفر چیپ نوبتت رد می‌شود و دیگ در پایان سهم برنده است.",
      logic=LCR_LOGIC, ui=LCR_UI, css=LCR_CSS, engines=("common",), tests=LCR_TESTS),
    G("rps", "سنگ کاغذ قیچی", "luck", "✊", "#67b98a", "#e26d5c",
      "سنگ‌کاغذ‌قیچی بهترین از ۵ مقابل رباتِ تطبیقی که حرکت‌های پرتکرار تو را می‌شمارد و علیه رایج‌ترین حرکتت می‌ایستد.",
      "سنگ قیچی را می‌بُرد، قیچی کاغذ را و کاغذ سنگ را؛ اولین ۳ برد صاحب مسابقه را مشخص می‌کند.",
      logic=RPS_LOGIC, ui=RPS_UI, css=RPS_CSS, engines=("common",), tests=RPS_TESTS),
    G("slots", "چرخ میوه", "luck", "🎰", "#d9a441", "#e26d5c",
      "چرخ میوهٔ سه‌قرقره با نمادهای وزن‌دار؛ هر چرخش ۵ اعتبار دارد و سه نماد یکسان روی خط برد جایزه می‌دهد.",
      "ستاره گران‌بهاترین نماد است (۳=۵۰)؛ دو ستاره ۳ و هر جفت دیگر ۲ اعتبار می‌دهد؛ با اتمام اعتبار بازی تمام است.",
      logic=SLOTS_LOGIC, ui=SLOTS_UI, css=SLOTS_CSS, engines=("common",), tests=SLOTS_TESTS),
    G("wheel", "گردونه شانس", "luck", "🎡", "#3fb8af", "#d9a441",
      "گردونهٔ شانس ۱۲ خانه‌ای با جوایز ۱۰۰/۲۵۰/۵۰۰ و خانه‌های ویژهٔ ضربدر۲، نصف و ورشکست؛ امتیاز را جمع کن و به ۲۰۰۰ برس.",
      "خانه‌ها وزن برابر دارند؛ ورشکست امتیاز را صفر می‌کند ولی هیچ‌وقت منفی نمی‌شود.",
      logic=WHEEL_LOGIC, ui=WHEEL_UI, css=WHEEL_CSS, engines=("common",), tests=WHEEL_TESTS),
]
