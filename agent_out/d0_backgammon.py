# -*- coding: utf-8 -*-
"""Backgammon (نرد) — full rules: dice, bar, hitting, bearing off, max-sequence rule, greedy AI."""
from lib import G

BG_LOGIC = r"""
var WOG_LOGIC = (function () {
'use strict';
function initial() {
  var pts = [], i;
  for (i = 0; i <= 24; i++) pts.push({ c: 0, n: 0 });
  function put(p, c, n) { pts[p] = { c: c, n: n }; }
  put(24, 1, 2); put(13, 1, 5); put(8, 1, 3); put(6, 1, 5);
  put(1, -1, 2); put(12, -1, 5); put(17, -1, 3); put(19, -1, 5);
  return { pts: pts, bar: { '1': 0, '-1': 0 }, off: { '1': 0, '-1': 0 }, turn: 1, phase: 'roll' };
}
function clone(st) {
  var pts = [], i;
  for (i = 0; i <= 24; i++) pts.push({ c: st.pts[i].c, n: st.pts[i].n });
  return { pts: pts, bar: { '1': st.bar['1'], '-1': st.bar['-1'] }, off: { '1': st.off['1'], '-1': st.off['-1'] }, turn: st.turn, phase: st.phase };
}
function allHome(st, p) {
  if (st.bar[p] !== 0) return false;
  var home = p === 1 ? sumRange(st, 1, 6, p) : sumRange(st, 19, 24, p);
  return st.off[p] + home === 15;
}
function sumRange(st, a, b, p) {
  var s = 0, i;
  for (i = a; i <= b; i++) if (st.pts[i].c === p) s += st.pts[i].n;
  return s;
}
function canLand(st, p, player) {
  var pt = st.pts[p];
  return pt.c !== -player || pt.n <= 1;
}
function singleMoves(st, player, die) {
  var out = [], i, to, entry;
  if (st.bar[player] > 0) {
    entry = player === 1 ? 25 - die : die;
    if (canLand(st, entry, player)) out.push({ from: 'bar', to: entry, die: die });
    return out;
  }
  for (i = 1; i <= 24; i++) {
    if (st.pts[i].c !== player || st.pts[i].n === 0) continue;
    to = player === 1 ? i - die : i + die;
    if (to >= 1 && to <= 24) {
      if (canLand(st, to, player)) out.push({ from: i, to: to, die: die });
    } else if (allHome(st, player)) {
      var dist = player === 1 ? i : 25 - i;
      if (die === dist) out.push({ from: i, to: 'off', die: die });
      else if (die > dist && noHigher(st, player, i)) out.push({ from: i, to: 'off', die: die });
    }
  }
  return out;
}
function noHigher(st, player, i) {
  var k;
  if (player === 1) { for (k = i + 1; k <= 6; k++) if (st.pts[k].c === 1 && st.pts[k].n) return false; }
  else { for (k = 19; k < i; k++) if (st.pts[k].c === -1 && st.pts[k].n) return false; }
  return true;
}
function applyMove(st, player, mv) {
  var n = clone(st), pt;
  if (mv.from === 'bar') n.bar[player] -= 1;
  else { pt = n.pts[mv.from]; pt.n -= 1; if (pt.n === 0) pt.c = 0; }
  if (mv.to === 'off') { n.off[player] += 1; }
  else {
    pt = n.pts[mv.to];
    if (pt.c === -player && pt.n === 1) { n.bar[-player] += 1; pt.c = player; pt.n = 1; }
    else if (pt.n === 0) { pt.c = player; pt.n = 1; }
    else pt.n += 1;
  }
  return n;
}
function diceList(d1, d2) { return d1 === d2 ? [d1, d1, d1, d1] : [d1, d2]; }
function maxSeqArr(st, player, dice) {
  var best = [], bestLen = -1;
  function dfs(cur, remaining, seq) {
    var usedAny = false, i, j, d, mvs, seen;
    for (j = 0; j < remaining.length; j++) {
      d = remaining[j];
      mvs = singleMoves(cur, player, d);
      seen = {};
      for (i = 0; i < mvs.length; i++) {
        (function (mv) {
          var key = mv.from + '>' + mv.to;
          if (seen[key]) return; seen[key] = 1;
          usedAny = true;
          var nxt = applyMove(cur, player, mv);
          var rem2 = remaining.slice(); rem2.splice(j, 1);
          dfs(nxt, rem2, seq.concat([mv]));
        })(mvs[i]);
      }
    }
    if (!usedAny) {
      if (seq.length > bestLen) { bestLen = seq.length; best = [seq.slice()]; }
      else if (seq.length === bestLen) { best.push(seq.slice()); }
    }
  }
  dfs(st, dice, []);
  if (bestLen <= 0) return [];
  if (dice.length === 2 && dice[0] !== dice[1] && bestLen === 1) {
    var larger = Math.max(dice[0], dice[1]), big = [], k;
    for (k = 0; k < best.length; k++) if (best[k][0].die === larger) big.push(best[k]);
    if (big.length) best = big;
  }
  return best;
}
function maxSequences(st, player, d1, d2) { return maxSeqArr(st, player, diceList(d1, d2)); }
function firstMoves(st, player, d1, d2) { return firstMovesDice(st, player, diceList(d1, d2)); }
function firstMovesDice(st, player, dice) {
  var seqs = maxSeqArr(st, player, dice), out = [], seen = {}, i, k, key, mv;
  for (i = 0; i < seqs.length; i++) {
    if (!seqs[i].length) continue;
    mv = seqs[i][0];
    key = mv.from + '>' + mv.to + ':' + mv.die;
    if (!seen[key]) { seen[key] = 1; out.push(mv); }
  }
  return out;
}
function remainingAfter(st, player, used, d1, d2) {
  var dice = diceList(d1, d2), i;
  for (i = 0; i < used.length; i++) { var k = dice.indexOf(used[i].die); if (k >= 0) dice.splice(k, 1); }
  return dice;
}
function canStillPlay(st, player, dice) {
  var i;
  for (i = 0; i < dice.length; i++) if (singleMoves(st, player, dice[i]).length) return true;
  return false;
}
function pip(st, player) {
  var s = 0, i, n;
  s += st.bar[player] * 25;
  for (i = 1; i <= 24; i++) if (st.pts[i].c === player) { n = st.pts[i].n; s += (player === 1 ? i : 25 - i) * n; }
  return s;
}
function blots(st, player) {
  var c = 0, i;
  for (i = 1; i <= 24; i++) if (st.pts[i].c === player && st.pts[i].n === 1) c++;
  return c;
}
function winner(st) {
  if (st.off['1'] >= 15) return 1;
  if (st.off['-1'] >= 15) return -1;
  return 0;
}
function aiTurn(st, player, d1, d2) {
  var seqs = maxSequences(st, player, d1, d2), i, k, cur, best = null, bestE = -1e9, e, noise, bl;
  if (!seqs.length) return [];
  for (i = 0; i < seqs.length; i++) {
    cur = st;
    for (k = 0; k < seqs[i].length; k++) cur = applyMove(cur, player, seqs[i][k]);
    bl = blots(cur, player);
    e = (pip(cur, -player) - pip(cur, player)) - 11 * bl;
    if (winner(cur) === player) e += 1e6;
    noise = 0.01 * i;
    if (e + noise > bestE) { bestE = e + noise; best = seqs[i]; }
  }
  return best;
}
function roll(rng) { rng = rng || Math.random; return 1 + Math.floor(rng() * 6); }
return { initial: initial, clone: clone, singleMoves: singleMoves, applyMove: applyMove, maxSequences: maxSequences, maxSeqArr: maxSeqArr,
  firstMoves: firstMoves, firstMovesDice: firstMovesDice, remainingAfter: remainingAfter, canStillPlay: canStillPlay, diceList: diceList,
  allHome: allHome, pip: pip, blots: blots, winner: winner, aiTurn: aiTurn, roll: roll };
})();
"""

BG_UI = r"""
var st = L.initial(), dice = [], used = [], selected = null, busy = false, wins = storeBest('wog-backgammon-wins');
var HUMAN = 1, AI = -1;
function rollPair() { return [L.roll(), L.roll()]; }
function drawDice() {
  var rem = L.remainingAfter(st, st.turn, used, dice[0], dice[1]), h = '', i, all = L.diceList(dice[0], dice[1]);
  var pipH = 'پیپ شما: <b>' + fa(L.pip(st, HUMAN)) + '</b>';
  hud(pipH + ' — تاس: <b>' + fa(dice[0]) + ' ، ' + fa(dice[1]) + '</b> — بیرون‌آمده: شما <b>' + fa(st.off[HUMAN]) + '</b> / ربات <b>' + fa(st.off[AI]) + '</b> — بردها: <b>' + fa(wins) + '</b>');
  var dc = $('#dice'); if (!dc) return;
  dc.innerHTML = '';
  for (i = 0; i < all.length; i++) {
    (function (i) {
      var usedNow = i < used.length || (all.length - rem.length) > i;
      var b = ce('span', 'die' + (usedNow ? ' used' : ''), fa(all[i]));
      dc.appendChild(b);
    })(i);
  }
}
function legalTargets(from) {
  var out = [], i, rem = L.remainingAfter(st, st.turn, used, dice[0], dice[1]);
  if (!rem.length) return out;
  var fm = L.firstMovesDice(st, st.turn, rem);
  for (i = 0; i < fm.length; i++) if (String(fm[i].from) === String(from)) out.push(fm[i]);
  return out;
}
function ptClickable(p) {
  if (busy || st.phase !== 'move' || st.turn !== HUMAN) return false;
  var pt = st.pts[p];
  if (selected === null) return pt.c === HUMAN && pt.n > 0 && legalTargets(p).length > 0;
  return legalTargets(selected).some(function (m) { return String(m.to) === String(p); });
}
function barClickable() {
  if (busy || st.phase !== 'move' || st.turn !== HUMAN) return false;
  if (st.bar[HUMAN] === 0) return false;
  return legalTargets('bar').length > 0;
}
function render() {
  drawDice();
  var app = $('#app'); app.innerHTML = '';
  var bd = ce('div', 'bgb');
  var barCol = ce('div', 'bbar');
  function cell(p, top) {
    var el = ce('div', 'bpt' + (top ? ' top' : '') + ((p % 2) ? ' odd' : ''));
    var pt = st.pts[p];
    var stack = ce('div', 'bstack');
    var n = Math.min(pt.n, 5), i;
    for (i = 0; i < n; i++) stack.appendChild(ce('div', 'bch ' + (pt.c === 1 ? 'w' : 'b')));
    if (pt.n > 5) stack.appendChild(ce('div', 'bmore', fa(pt.n)));
    el.appendChild(stack);
    if (selected === p) el.classList.add('sel');
    if (ptClickable(p)) el.classList.add('can');
    el.addEventListener('click', function () { tapPoint(p); });
    return el;
  }
  var i, p;
  for (p = 13; p <= 18; p++) bd.appendChild(cell(p, true));
  if (st.bar[HUMAN] > 0) {
    var bw = ce('div', 'bch w');
    if (selected === 'bar') bw.classList.add('selb');
    if (barClickable()) bw.classList.add('can');
    bw.addEventListener('click', function () { tapPoint('bar'); });
    barCol.appendChild(bw);
    barCol.appendChild(ce('div', 'blab', fa(st.bar[HUMAN])));
  }
  if (st.bar[AI] > 0) { barCol.appendChild(ce('div', 'bch b')); barCol.appendChild(ce('div', 'blab', fa(st.bar[AI]))); }
  bd.appendChild(barCol);
  for (p = 19; p <= 24; p++) bd.appendChild(cell(p, true));
  for (p = 12; p >= 7; p--) bd.appendChild(cell(p, false));
  var sp = ce('div'); sp.style.gridRow = '2'; sp.style.gridColumn = '7'; bd.appendChild(sp);
  for (p = 6; p >= 1; p--) bd.appendChild(cell(p, false));
  app.appendChild(bd);
  var msg = ce('div', 'bmsg');
  if (st.phase === 'roll') msg.textContent = st.turn === HUMAN ? 'تاس بریز!' : 'ربات دارد تاس می‌ریزد…';
  else msg.textContent = st.turn === HUMAN ? (selected === null ? 'مهره‌ای را انتخاب کن' : 'مقصد را لمس کن (یا دوباره انتخاب کن)') : 'ربات فکر می‌کند…';
  app.appendChild(msg);
  var dc = ce('div', 'wrow'); dc.id = 'dice'; app.appendChild(dc);
  var act = ce('div', 'wrow');
  if (st.phase === 'roll' && st.turn === HUMAN && !busy) {
    var rb = ce('button', null, 'تاس بریز');
    rb.setAttribute('data-smoke', '');
    rb.addEventListener('click', function () { doRoll(); });
    act.appendChild(rb);
  }
  if (st.phase === 'move' && st.turn === HUMAN && selected !== null) {
    var cb = ce('button', 'sec', 'لغو انتخاب');
    cb.addEventListener('click', function () { selected = null; render(); });
    act.appendChild(cb);
  }
  var nb = ce('button', 'sec', 'بازی جدید');
  nb.setAttribute('data-smoke', '');
  nb.addEventListener('click', newGame);
  act.appendChild(nb);
  app.appendChild(act);
}
function tapPoint(p) {
  if (busy || st.phase !== 'move' || st.turn !== HUMAN) return;
  if (selected === null) {
    if (p === 'bar' && st.bar[HUMAN] > 0) { selected = 'bar'; render(); return; }
    if (st.pts[p].c === HUMAN && st.pts[p].n > 0) { selected = p; render(); }
    return;
  }
  var mvs = legalTargets(selected), i, mv;
  for (i = 0; i < mvs.length; i++) {
    if (String(mvs[i].to) === String(p)) { mv = mvs[i]; break; }
  }
  if (!mv) { selected = null; if (st.pts[p].c === HUMAN && st.pts[p].n > 0 && p !== 'bar') selected = p; render(); return; }
  st = L.applyMove(st, HUMAN, mv);
  used.push(mv); selected = null;
  afterHumanMove();
}
function afterHumanMove() {
  var w = L.winner(st);
  if (w) { endGame(w); return; }
  var rem = L.remainingAfter(st, HUMAN, used, dice[0], dice[1]);
  if (!rem.length || !L.canStillPlay(st, HUMAN, rem)) passTurn();
  else render();
}
function doRoll() {
  if (st.phase !== 'roll' || busy) return;
  dice = rollPair(); used = []; selected = null;
  st.phase = 'move';
  var fm = L.firstMoves(st, st.turn, dice[0], dice[1]);
  if (!fm.length) { toast('حرکتی ممکن نیست — نوبت رد شد'); render(); setTimeout(passTurn, 700); return; }
  render();
}
function passTurn() {
  selected = null;
  if (L.winner(st)) { endGame(L.winner(st)); return; }
  st.turn = -st.turn; used = []; dice = []; st.phase = 'roll';
  if (st.turn === AI) { busy = true; render(); setTimeout(aiPlay, 550); }
  else { busy = false; render(); }
}
function aiPlay() {
  dice = rollPair(); used = [];
  st.phase = 'move';
  var seq = L.aiTurn(st, AI, dice[0], dice[1]);
  if (!seq.length) { toast('ربات: حرکتی ندارد'); setTimeout(function () { busy = false; passTurn(); }, 500); return; }
  var i = 0;
  (function step() {
    if (i >= seq.length || L.winner(st)) {
      busy = false;
      if (L.winner(st)) { endGame(L.winner(st)); return; }
      setTimeout(passTurn, 420); return;
    }
    st = L.applyMove(st, AI, seq[i]);
    used.push(seq[i]); i++;
    render();
    setTimeout(step, 430);
  })();
}
function endGame(w) {
  busy = true; render();
  var mars = (w === 1 && st.off[AI] === 0) || (w === -1 && st.off[HUMAN] === 0);
  if (w === HUMAN) { wins++; store.set('wog-backgammon-wins', String(wins)); }
  ovl(w === HUMAN ? 'بردی!' : 'ربات برد',
    (w === HUMAN ? 'هر ۱۵ مهره‌ات بیرون آمد' + (mars ? ' — مارسی!' : '') : 'ربات زودتر تمام کرد' + (mars ? ' — مارسی!' : '')),
    'بازی جدید', newGame);
}
function newGame() { st = L.initial(); dice = []; used = []; selected = null; busy = false; st.phase = 'roll'; st.turn = HUMAN; render(); }
newGame();
$('#hint').textContent = 'مهره را انتخاب و مقصد را لمس کن؛ تاس دوبل چهار حرکت می‌دهد؛ روی مهره‌تکی حریف بینداز تا به میله برود؛ وقتی همهٔ مهره‌ها در خانهٔ خودت باشند از تخته بیرون بیاور. (بدون مکعب دوبرابر)';
"""

BG_CSS = r"""
.bgb{display:grid;grid-template-columns:repeat(6,min(6.4vw,34px)) min(4vw,22px) repeat(6,min(6.4vw,34px));grid-auto-rows:min(19vw,110px);gap:3px;direction:ltr}
.bbar{grid-row:1/3;grid-column:7;display:flex;flex-direction:column;align-items:center;gap:2px;justify-content:center;background:rgba(0,0,0,.25);border-radius:6px}
.bpt{width:100%;height:100%;background:linear-gradient(180deg,#223257,#1a2745);border:1px solid rgba(217,164,65,.25);border-radius:6px;display:flex;justify-content:center;position:relative;cursor:default}
.bpt.top .bstack{align-self:flex-start}
.bpt.odd{background:linear-gradient(180deg,#1c2b4d,#16223d)}
.bstack{display:flex;flex-direction:column;gap:1px;align-items:center;width:100%}
.bpt:not(.top) .bstack{align-self:flex-end}
.bch{width:78%;padding-top:78%;border-radius:50%;box-shadow:0 1px 3px rgba(0,0,0,.5)}
.bch.w{background:radial-gradient(circle at 35% 30%,#fdf6e3,#cdb277 75%)}
.bch.b{background:radial-gradient(circle at 35% 30%,#5d719a,#222f4e 75%)}
.bmore{position:absolute;bottom:2px;color:#e8c073;font-size:.7rem;font-weight:700}
.bpt.sel{outline:2px solid #e8c073}
.bpt.can{cursor:pointer;border-color:rgba(63,184,175,.8)}
.bpt.can:hover{outline:2px solid #3fb8af}
.bbar .bch{width:80%;padding-top:80%}
.bbar .bch.can{cursor:pointer;outline:2px solid #3fb8af}
.blab{color:#e8c073;font-size:.65rem;font-weight:700}
.bmsg{color:#a8b3c9;font-size:.9rem;min-height:1.4em;margin-top:4px}
.die{display:inline-flex;width:34px;height:34px;align-items:center;justify-content:center;background:#f6efe0;color:#1c2438;border-radius:8px;font-weight:900;margin:2px}
.die.used{opacity:.28}
"""

BG_TESTS = [
    ("چیدمان اولیه و پیپ", r"""
var st=L.initial();
T.eq(st.pts[24].n,2);T.eq(st.pts[13].n,5);T.eq(st.pts[8].n,3);T.eq(st.pts[6].n,5);
T.eq(st.pts[1].n,2);T.eq(st.pts[19].n,5);
T.eq(L.pip(st,1),167,'white pip 167');
T.eq(L.pip(st,-1),167,'black pip 167');
T.eq(L.pip(st,1)+L.pip(st,-1),334);
"""),
    ("حرکت‌های قانونی با ۳-۱ در آغاز", r"""
var st=L.initial();
var m3=L.singleMoves(st,1,3),m1=L.singleMoves(st,1,1);
function has(arr,f,t){return arr.some(function(m){return m.from===f&&m.to===t;});}
T.ok(has(m3,8,5),'8→5 با ۳');
T.ok(has(m3,6,3),'6→3 با ۳');
T.ok(has(m3,24,21),'24→21 با ۳');
T.ok(has(m3,13,10),'13→10 با ۳');
T.ok(has(m1,6,5),'6→5 با ۱');
T.ok(has(m1,24,23),'24→23 با ۱');
T.ok(!has(m1,13,12),'خانهٔ ۱۲ سیاه است — مسدود');
T.ok(!has(m3,5,2),'از ۵ مهره‌ای نیست');
T.ok(!has(m1,5,4),'جهت اشتباه رد');
var fm=L.firstMoves(st,1,3,1);
T.eq(fm.length,7,'first moves for 3-1 (13→12 blocked)');
"""),
    ("زدن بلوت به میله", r"""
var st=L.initial();
st.pts[2]={c:-1,n:1};
st=L.applyMove(st,1,{from:5,to:2,die:3});
T.eq(st.pts[2].c,1,'white landed on 2');
T.eq(st.pts[2].n,1,'blot replaced');
T.eq(st.bar['-1'],1,'black sent to bar');
"""),
    ("ورود از میله", r"""
var st=L.initial();
st.bar['-1']=2;
var m=L.singleMoves(st,-1,3);
T.ok(m.length===1&&m[0].from==='bar'&&m[0].to===3,'black enters at 3');
st.pts[3]={c:1,n:2};
m=L.singleMoves(st,-1,3);
T.eq(m.length,0,'blocked entry');
st.pts[3]={c:1,n:1};
m=L.singleMoves(st,-1,3);
T.ok(m.length===1,'hit to enter');
"""),
    ("بیرون‌آوردن", r"""
var st=L.initial();
var i;for(i=1;i<=24;i++)st.pts[i]={c:0,n:0};
st.pts[5]={c:1,n:2};st.off['1']=13;
T.ok(L.allHome(st,1),'all home');
var m=L.singleMoves(st,1,5);
T.ok(m.some(function(x){return x.from===5&&x.to==='off';}),'exact bear off 5');
st.pts[5]={c:1,n:1};st.pts[4]={c:1,n:1};st.off['1']=13;
m=L.singleMoves(st,1,6);
T.ok(m.some(function(x){return x.from===5&&x.to==='off';}),'die 6 bears off from HIGHEST point (5)');
T.ok(!m.some(function(x){return x.from===4&&x.to==='off';}),'lower point (4) must wait');
st.pts[6]={c:1,n:1};
m=L.singleMoves(st,1,6);
T.ok(!m.some(function(x){return x.from===4&&x.to==='off';}),'higher point blocks higher-die bearoff');
"""),
    ("قانون تاس بزرگ‌تر وقتی فقط یکی اجرا می‌شود", r"""
var st=L.initial();
var i;for(i=1;i<=24;i++)st.pts[i]={c:0,n:0};
st.pts[1]={c:1,n:1};st.off['1']=14;
var seqs=L.maxSequences(st,1,6,5);
T.ok(seqs.length>0,'has moves');
for(var k=0;k<seqs.length;k++)T.eq(seqs[k][0].die,6,'forced larger die');
var fm=L.firstMoves(st,1,6,5);
T.ok(fm.every(function(m){return m.die===6;}),'first moves use 6 only');
"""),
    ("دوبل چهار حرکت", r"""
var st=L.initial();
var seqs=L.maxSequences(st,1,2,2);
var maxLen=0,k;
for(k=0;k<seqs.length;k++)if(seqs[k].length>maxLen)maxLen=seqs[k].length;
T.eq(maxLen,4,'doubles allow 4 moves');
T.ok(L.diceList(2,2).length===4);
T.ok(L.diceList(3,5).length===2);
"""),
    ("بازی کامل AI مقابل AI", r"""
var st=L.initial(),turn=1,turns=0;
while(!L.winner(st)&&turns<400){
  var d1=L.roll(rng),d2=L.roll(rng);
  var seq=L.aiTurn(st,turn,d1,d2);
  var k;
  for(k=0;k<seq.length;k++)st=L.applyMove(st,turn,seq[k]);
  T.ok(st.off['1']+st.off['-1']<=30,'off sane');
  var total=st.off['1']+st.off['-1']+st.bar['1']+st.bar['-1'],i;
  for(i=1;i<=24;i++)total+=st.pts[i].n;
  T.eq(total,30,'30 checkers conserved');
  turn=-turn;turns++;
}
T.ok(L.winner(st)!==0,'game finished: '+turns+' turns');
T.ok(st.off[L.winner(st)]===15,'winner bore off 15');
"""),
]

GAMES = [
    G(slug="backgammon", title="نرد ایرانی", cat="board", icon="⚅", g1="#8a5a1f", g2="#d9a441",
      desc="نرد کامل با قوانین رسمی: تاس دوبل، میله، زدن بلوت، بیرون‌آوردن و هوش مصنوعی حریص — بدون مکعب دوبرابر.",
      hint="حرکت‌ها باید تمام تاس را مصرف کنند؛ اگر فقط یک تاس قابل اجرا باشد باید تاس بزرگ‌تر بازی شود.",
      engines=("common",), logic=BG_LOGIC, ui=BG_UI, css=BG_CSS, tests=BG_TESTS, seed=77),
]
