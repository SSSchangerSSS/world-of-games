# -*- coding: utf-8 -*-
"""AG-F1 batch: nonogram + mastermind + simon. All cat="puzzle", engines=("common",)."""
from lib_mini import G

# ============================== nonogram ==============================
NONOGRAM_LOGIC = r"""
var WOG_LOGIC = {
  genPattern: function (n, fill, rng) {
    var r = rng || Math.random;
    var total = n * n, idx = [], i, j, t;
    for (i = 0; i < total; i++) idx.push(i);
    for (i = 0; i < fill && i < total; i++) {
      j = i + Math.floor(r() * (total - i));
      t = idx[i]; idx[i] = idx[j]; idx[j] = t;
    }
    var b = [];
    for (i = 0; i < n; i++) { var row = []; for (var k = 0; k < n; k++) row.push(0); b.push(row); }
    for (i = 0; i < fill && i < total; i++) {
      var c = idx[i];
      b[Math.floor(c / n)][c % n] = 1;
    }
    return b;
  },
  runs: function (line) {
    var out = [], c = 0;
    for (var i = 0; i <= line.length; i++) {
      if (i < line.length && line[i] === 1) c++;
      else { if (c > 0) out.push(c); c = 0; }
    }
    return out;
  },
  rowClues: function (row) { return WOG_LOGIC.runs(row); },
  colClues: function (col) { return WOG_LOGIC.runs(col); },
  cluesFor: function (board) {
    var n = board.length, res = { rows: [], cols: [] }, i, j, col;
    for (i = 0; i < n; i++) res.rows.push(WOG_LOGIC.rowClues(board[i]));
    for (j = 0; j < n; j++) {
      col = [];
      for (i = 0; i < n; i++) col.push(board[i][j]);
      res.cols.push(WOG_LOGIC.colClues(col));
    }
    return res;
  },
  checkWin: function (userBoard, solution) {
    var n = solution.length, i, j;
    if (!userBoard || userBoard.length !== n) return false;
    for (i = 0; i < n; i++) {
      if (!userBoard[i] || userBoard[i].length !== n) return false;
      for (j = 0; j < n; j++) {
        if ((userBoard[i][j] === 1) !== (solution[i][j] === 1)) return false;
      }
    }
    return true;
  }
};
"""
NONOGRAM_UI = r"""
var st = null, APP = $('#app');
function newGame(n) {
  var fill = n === 5 ? 12 : 22, i, j;
  var sol = L.genPattern(n, fill, Math.random);
  st = { n: n, sol: sol, clues: L.cluesFor(sol), user: [], moves: 0, done: false };
  for (i = 0; i < n; i++) { var row = []; for (j = 0; j < n; j++) row.push(0); st.user.push(row); }
  hud('اندازه ' + fa(n) + '×' + fa(n) + ' · خانه‌های پر: ' + fa(fill));
  draw();
}
function lineDone(clue, k, isCol) {
  var sum = 0, f = 0, i;
  for (i = 0; i < clue.length; i++) sum += clue[i];
  for (i = 0; i < st.n; i++) {
    var v = isCol ? st.user[i][k] : st.user[k][i];
    if (v === 0) return false;
    if (v === 1) f++;
  }
  return f === sum;
}
function draw() {
  APP.innerHTML = '';
  var box = ce('div', 'nbox');
  var tools = ce('div', 'rowc');
  var b5 = ce('button', 'btn' + (st.n === 5 ? ' gold' : ''), '۵×۵');
  var b8 = ce('button', 'btn' + (st.n === 8 ? ' gold' : ''), '۸×۸');
  var bn = ce('button', 'btn gold', 'بازی جدید');
  bn.setAttribute('data-smoke', '1');
  b5.onclick = function () { newGame(5); };
  b8.onclick = function () { newGame(8); };
  bn.onclick = function () { newGame(st.n); };
  tools.appendChild(b5); tools.appendChild(b8); tools.appendChild(bn);
  box.appendChild(tools);
  var g = ce('div', 'ngrid');
  g.style.gridTemplateColumns = 'auto repeat(' + st.n + ',minmax(30px,44px))';
  g.appendChild(ce('div', 'ncorn'));
  var i, j;
  for (j = 0; j < st.n; j++) {
    var cc = ce('div', 'ncol' + (lineDone(st.clues.cols[j], j, true) ? ' dim' : ''));
    cc.textContent = st.clues.cols[j].join('\n') || '0';
    g.appendChild(cc);
  }
  for (i = 0; i < st.n; i++) {
    var rl = ce('div', 'nrowl' + (lineDone(st.clues.rows[i], i, false) ? ' dim' : ''));
    rl.textContent = st.clues.rows[i].join(' ') || '0';
    g.appendChild(rl);
    for (j = 0; j < st.n; j++) {
      var cell = ce('button', 'ncell');
      cell.type = 'button';
      var v = st.user[i][j];
      if (v === 1) cell.classList.add('on');
      else if (v === 2) { cell.classList.add('mx'); cell.textContent = '×'; }
      (function (r, c, el) { el.onclick = function () { tap(r, c); }; })(i, j, cell);
      g.appendChild(cell);
    }
  }
  box.appendChild(g);
  APP.appendChild(box);
}
function tap(r, c) {
  if (st.done) return;
  st.user[r][c] = (st.user[r][c] + 1) % 3;
  st.moves++;
  if (L.checkWin(st.user, st.sol)) {
    st.done = true;
    var bk = store.get('wog-nonogram-best-' + st.n);
    var best = bk === null ? st.moves : Math.min(parseInt(bk, 10) || st.moves, st.moves);
    store.set('wog-nonogram-best-' + st.n, '' + best);
    hud('حل شد در ' + fa(st.moves) + ' حرکت · رکورد: ' + fa(best));
    draw();
    ovl('آفرین! حل شد', 'اندازه ' + fa(st.n) + '×' + fa(st.n) + ' در ' + fa(st.moves) + ' حرکت · رکورد: ' + fa(best), 'بازی جدید', function () { newGame(st.n); });
    return;
  }
  hud('حرکت‌ها: ' + fa(st.moves));
  draw();
}
$('#hint').textContent = 'لمس خانه: پر ← علامت × ← خالی. سرنخ هر خط، طول رشته‌های پیوستهٔ آن است.';
newGame(5);
"""
NONOGRAM_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0b1220;color:#e8ecf4;font-family:Tahoma,sans-serif}
header h1{color:#d9a441;font-size:20px}
#app{padding:8px;text-align:center}
.rowc{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:8px 0}
.btn{min-height:42px;min-width:64px;padding:8px 14px;border-radius:10px;border:1px solid #2a3b5e;background:#14203a;color:#e8ecf4;font-size:15px;cursor:pointer;touch-action:manipulation}
.btn.gold{background:#d9a441;color:#14203a;border-color:#d9a441;font-weight:bold}
.ngrid{display:grid;gap:3px;justify-content:center;direction:ltr;margin:10px auto}
.ncell{width:100%;min-width:30px;min-height:30px;aspect-ratio:1/1;border:1px solid #2a3b5e;background:#14203a;border-radius:7px;cursor:pointer;touch-action:manipulation;font-size:15px;color:#e26d5c;padding:0}
.ncell.on{background:#3fb8af;border-color:#3fb8af}
.nrowl{display:flex;align-items:center;justify-content:flex-end;gap:5px;padding:0 6px 0 2px;font-size:12px;font-weight:bold;color:#d9a441;white-space:nowrap}
.ncol{display:flex;flex-direction:column;justify-content:flex-end;align-items:center;font-size:12px;font-weight:bold;color:#d9a441;white-space:pre;padding-bottom:2px}
.dim{opacity:.3}
"""
NONOGRAM_TESTS = [
    ("درون‌یابی سرنخ از خط", r"""T.eq(JSON.stringify(L.rowClues([1,0,1,1,0])),'[1,2]');
T.eq(JSON.stringify(L.rowClues([0,0,0,0])),'[]');
T.eq(JSON.stringify(L.rowClues([1,1,1,1,1])),'[5]');
T.eq(JSON.stringify(L.rowClues([0,1,1,0,1])),'[2,1]');
var b=[[1,0,1],[0,1,0],[1,0,0]],c=L.cluesFor(b);
T.eq(JSON.stringify(c.rows),'[[1,1],[1],[1]]');
T.eq(JSON.stringify(c.cols),'[[1,1],[1],[1]]');"""),
    ("سازگاری جمع سرنخ‌ها در ۵۰ بذر", r"""function sc(cs){var s=0;for(var i=0;i<cs.length;i++)for(var j=0;j<cs[i].length;j++)s+=cs[i][j];return s;}
for(var s=0;s<50;s++){
 var n=(s%2)?8:5,fill=(s%2)?20:12;
 var b=L.genPattern(n,fill,rng),c=L.cluesFor(b);
 T.eq(sc(c.rows),fill,'rows seed '+s);
 T.eq(sc(c.cols),fill,'cols seed '+s);
 T.ok(b.length===n,'dims '+s);
 T.ok(L.checkWin(b,b),'self '+s);
}"""),
    ("تشخیص برد و علامت ×", r"""var sol=[[1,0],[0,1]];
T.ok(L.checkWin([[1,0],[0,1]],sol),'exact');
T.ok(L.checkWin([[1,2],[0,1]],sol),'x as empty');
T.ok(!L.checkWin([[2,0],[0,2]],sol),'x on filled');
T.ok(!L.checkWin([[0,0],[0,1]],sol),'missing fill');
T.ok(!L.checkWin([[1,1],[0,1]],sol),'extra fill');
T.ok(!L.checkWin([[1,0],[0,0]],sol),'partial');"""),
    ("الگوی غیرتهی و شمارش پرشده", r"""function cnt(b){var s=0;for(var i=0;i<b.length;i++)for(var j=0;j<b.length;j++)if(b[i][j]===1)s++;return s;}
for(var s=0;s<8;s++){var b=L.genPattern(5,10,rng);T.eq(cnt(b),10,'count '+s);T.ok(cnt(b)>0,'nonempty');}
var b8=L.genPattern(8,1,rng);T.eq(cnt(b8),1,'min fill');"""),
]

# ============================== mastermind ==============================
MASTERMIND_LOGIC = r"""
var WOG_LOGIC = {
  genCode: function (rng) {
    var r = rng || Math.random, code = [], i;
    for (i = 0; i < 4; i++) code.push(Math.floor(r() * 6));
    return code;
  },
  feedback: function (guess, code) {
    var black = 0, white = 0, i, cLeft = [], gLeft = [];
    for (i = 0; i < 6; i++) { cLeft.push(0); gLeft.push(0); }
    for (i = 0; i < code.length; i++) {
      if (guess[i] === code[i]) black++;
      else { cLeft[code[i]]++; gLeft[guess[i]]++; }
    }
    for (i = 0; i < 6; i++) white += Math.min(cLeft[i], gLeft[i]);
    return { black: black, white: white };
  },
  isWin: function (fb) { return !!fb && fb.black === 4; }
};
"""
MASTERMIND_UI = r"""
var COLORS = ['#e26d5c', '#67b98a', '#4a90d9', '#d9a441', '#9b6dd6', '#3fb8af'];
var CNAMES = ['قرمز', 'سبز', 'آبی', 'زرد', 'بنفش', 'فیروزه‌ای'];
var st = null, sel = -1, APP = $('#app');
function newGame() {
  st = { code: L.genCode(Math.random), guess: [-1, -1, -1, -1], hist: [], done: false };
  sel = -1;
  hud('حدس ' + fa(1) + ' از ' + fa(10));
  draw();
}
function codeNames(code) {
  var a = [], i;
  for (i = 0; i < code.length; i++) a.push(CNAMES[code[i]]);
  return a.join('، ');
}
function draw() {
  APP.innerHTML = '';
  var box = ce('div', 'mbox');
  var top = ce('div', 'rowc');
  var bn = ce('button', 'btn gold', 'بازی جدید');
  bn.setAttribute('data-smoke', '1');
  bn.onclick = newGame;
  top.appendChild(bn);
  box.appendChild(top);
  var pal = ce('div', 'pal'), i, k;
  for (i = 0; i < 6; i++) {
    (function (c) {
      var s = ce('button', 'sw' + (sel === c ? ' selc' : ''));
      s.type = 'button';
      s.style.background = COLORS[c];
      s.onclick = function () { if (!st.done) { sel = c; draw(); } };
      pal.appendChild(s);
    })(i);
  }
  box.appendChild(pal);
  var gr = ce('div', 'grow');
  for (k = 0; k < 4; k++) {
    (function (k) {
      var s = ce('button', 'slot');
      s.type = 'button';
      var v = st.guess[k];
      if (v >= 0) s.style.background = COLORS[v];
      else s.textContent = '؟';
      s.onclick = function () {
        if (st.done) return;
        if (sel >= 0) st.guess[k] = sel;
        else { var nx = st.guess[k] + 1; if (nx > 5) nx = -1; st.guess[k] = nx; }
        draw();
      };
      gr.appendChild(s);
    })(k);
  }
  box.appendChild(gr);
  var ops = ce('div', 'rowc');
  var clr = ce('button', 'btn', 'پاک کردن');
  clr.onclick = function () { if (!st.done) { st.guess = [-1, -1, -1, -1]; draw(); } };
  var ok = true;
  for (k = 0; k < 4; k++) if (st.guess[k] < 0) ok = false;
  var sub = ce('button', 'btn gold', 'ثبت حدس');
  sub.setAttribute('data-smoke', '1');
  sub.disabled = !ok || st.done;
  sub.onclick = submit;
  ops.appendChild(clr); ops.appendChild(sub);
  box.appendChild(ops);
  box.appendChild(ce('p', 'legend', '● رنگ درست در جای درست · ○ رنگ درست در جای نادرست'));
  var hl = ce('div', 'hist');
  for (i = st.hist.length - 1; i >= 0; i--) {
    var it = st.hist[i], row = ce('div', 'hrow');
    for (k = 0; k < 4; k++) { var d = ce('span', 'peg'); d.style.background = COLORS[it.g[k]]; row.appendChild(d); }
    var fb = ce('span', 'fb');
    for (var b = 0; b < it.fb.black; b++) fb.appendChild(ce('span', 'pb'));
    for (var w = 0; w < it.fb.white; w++) fb.appendChild(ce('span', 'pw'));
    row.appendChild(fb);
    row.appendChild(ce('span', 'hnum', fa(i + 1)));
    hl.appendChild(row);
  }
  box.appendChild(hl);
  APP.appendChild(box);
}
function submit() {
  if (st.done) return;
  var fb = L.feedback(st.guess, st.code);
  st.hist.push({ g: st.guess.slice(), fb: fb });
  if (L.isWin(fb)) {
    st.done = true;
    var bk = store.get('wog-mastermind-best');
    var best = bk === null ? st.hist.length : Math.min(parseInt(bk, 10) || st.hist.length, st.hist.length);
    store.set('wog-mastermind-best', '' + best);
    hud('رمز شکسته شد در ' + fa(st.hist.length) + ' حدس · رکورد: ' + fa(best));
    draw();
    ovl('رمز شکسته شد!', 'در ' + fa(st.hist.length) + ' حدس · رکورد: ' + fa(best), 'بازی جدید', newGame);
    return;
  }
  if (st.hist.length >= 10) {
    st.done = true;
    hud('باختی! رمز: ' + codeNames(st.code));
    draw();
    ovl('باختی!', 'رمز بود: ' + codeNames(st.code), 'بازی جدید', newGame);
    return;
  }
  st.guess = [-1, -1, -1, -1];
  hud('حدس ' + fa(st.hist.length + 1) + ' از ' + fa(10));
  draw();
}
$('#hint').textContent = 'از پالت رنگ انتخاب کن و روی خانه بزن، یا هر خانه را لمس کن تا رنگش بچرخد. ۱۰ حدس داری.';
newGame();
"""
MASTERMIND_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0b1220;color:#e8ecf4;font-family:Tahoma,sans-serif}
header h1{color:#d9a441;font-size:20px}
#app{padding:8px;text-align:center}
.rowc{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:8px 0}
.btn{min-height:42px;padding:8px 16px;border-radius:10px;border:1px solid #2a3b5e;background:#14203a;color:#e8ecf4;font-size:15px;cursor:pointer;touch-action:manipulation}
.btn.gold{background:#d9a441;color:#14203a;border-color:#d9a441;font-weight:bold}
.btn:disabled{opacity:.4}
.pal{display:flex;gap:10px;justify-content:center;margin:10px 0}
.sw{width:44px;height:44px;border-radius:50%;border:3px solid transparent;cursor:pointer;touch-action:manipulation}
.sw.selc{border-color:#fff}
.grow{display:flex;gap:10px;justify-content:center;margin:8px 0}
.slot{width:52px;height:52px;border-radius:12px;border:2px dashed #2a3b5e;background:#14203a;color:#8fa0c0;font-size:18px;cursor:pointer;touch-action:manipulation}
.legend{color:#8fa0c0;font-size:13px}
.hist{max-width:340px;margin:10px auto;display:flex;flex-direction:column;gap:6px}
.hrow{display:flex;align-items:center;gap:8px;justify-content:center;background:#14203a;border:1px solid #2a3b5e;border-radius:10px;padding:6px}
.peg{width:22px;height:22px;border-radius:50%;display:inline-block}
.fb{display:inline-flex;gap:4px}
.pb,.pw{width:14px;height:14px;border-radius:50%;display:inline-block}
.pb{background:#0b1220;border:2px solid #d9a441}
.pw{background:transparent;border:2px solid #cfd8ea}
.hnum{color:#8fa0c0;font-size:12px}
"""
MASTERMIND_TESTS = [
    ("بردار کلاسیک بازخورد", r"""T.eq(JSON.stringify(L.feedback([0,1,2,3],[0,1,2,3])),'{"black":4,"white":0}');
T.eq(JSON.stringify(L.feedback([3,1,2,0],[0,1,2,3])),'{"black":2,"white":2}');
T.eq(JSON.stringify(L.feedback([0,0,0,0],[0,1,2,3])),'{"black":1,"white":0}');
T.eq(JSON.stringify(L.feedback([5,5,5,5],[0,1,2,3])),'{"black":0,"white":0}');"""),
    ("رنگ‌های تکراری", r"""T.eq(JSON.stringify(L.feedback([0,1,0,3],[0,0,1,2])),'{"black":1,"white":2}');
T.eq(JSON.stringify(L.feedback([0,0,1,1],[0,0,2,2])),'{"black":2,"white":0}');
T.eq(JSON.stringify(L.feedback([1,1,0,0],[0,0,1,1])),'{"black":0,"white":4}');
T.eq(JSON.stringify(L.feedback([0,0,0,0],[0,0,0,0])),'{"black":4,"white":0}');"""),
    ("تشخیص برد", r"""T.ok(L.isWin(L.feedback([2,2,2,2],[2,2,2,2])),'win');
T.ok(!L.isWin({black:3,white:1}),'not win');
T.ok(!L.isWin(null),'null safe');"""),
    ("محدودهٔ رمز تولیدشده", r"""for(var s=0;s<20;s++){var c=L.genCode(rng);T.eq(c.length,4,'len');for(var i=0;i<4;i++)T.ok(c[i]>=0&&c[i]<6,'range');}
T.eq(JSON.stringify(L.genCode(function(){return 0;})),'[0,0,0,0]');
T.eq(JSON.stringify(L.genCode(function(){return 0.999;})),'[5,5,5,5]');"""),
    ("شبیه‌سازی بازیکن خودکار تا ۱۰ دور", r"""var code=L.genCode(rng),won=false,rounds=0;
for(var r=0;r<10;r++){
 rounds++;
 var g=[Math.floor(rng()*6),Math.floor(rng()*6),Math.floor(rng()*6),Math.floor(rng()*6)];
 var fb=L.feedback(g,code);
 T.ok(fb.black+fb.white<=4,'fb bound');
 T.ok(fb.black>=0&&fb.white>=0,'fb range');
 if(L.isWin(fb)){won=true;T.ok(fb.black===4,'win exact');break;}
}
T.ok(rounds>=1&&rounds<=10,'terminates');
T.ok(won||rounds===10,'flow end');"""),
]

# ============================== simon ==============================
SIMON_LOGIC = r"""
var WOG_LOGIC = {
  nextColor: function (rng) {
    var r = rng || Math.random;
    return Math.floor(r() * 4);
  },
  extend: function (seq, color) {
    var s = seq.slice();
    s.push(color);
    return s;
  },
  check: function (seq, input, i) {
    if (i < 0 || i >= seq.length) return 'wrong';
    return input === seq[i] ? 'ok' : 'wrong';
  },
  speedFor: function (level) {
    var ms = 900 - (level - 1) * 60;
    if (ms < 320) ms = 320;
    return ms;
  }
};
"""
SIMON_UI = r"""
var PCOLORS = ['#e26d5c', '#67b98a', '#4a90d9', '#d9a441'];
var FREQ = [329.63, 261.63, 220, 164.81];
var st = { seq: [], level: 0, phase: 'idle', idx: 0 }, AC = null, APP = $('#app');
function tone(i, ms) {
  try {
    if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)();
    var o = AC.createOscillator(), g = AC.createGain(), t = AC.currentTime;
    o.type = 'sine';
    o.frequency.value = FREQ[i] || 220;
    o.connect(g); g.connect(AC.destination);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.22, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + ms / 1000);
    o.start(t); o.stop(t + ms / 1000 + 0.05);
  } catch (e) {}
}
function lockPads(on) {
  var pads = $$('.pad');
  for (var i = 0; i < pads.length; i++) pads[i].disabled = on;
}
function lite(i, ms) {
  var pads = $$('.pad');
  if (!pads[i]) return;
  pads[i].classList.add('lit');
  setTimeout(function () { pads[i].classList.remove('lit'); }, ms);
}
function start() {
  st = { seq: L.extend([], L.nextColor(Math.random)), level: 1, phase: 'show', idx: 0 };
  draw();
  playSeq();
}
function playSeq() {
  st.phase = 'show';
  lockPads(true);
  hud('سطح ' + fa(st.level) + ' — تماشا کن…');
  var ms = L.speedFor(st.level), i = 0;
  function step() {
    if (i >= st.seq.length) {
      st.phase = 'input';
      st.idx = 0;
      lockPads(false);
      hud('سطح ' + fa(st.level) + ' — حالا تکرار کن');
      return;
    }
    lite(st.seq[i], Math.round(ms * 0.62));
    tone(st.seq[i], Math.round(ms * 0.62));
    i++;
    setTimeout(step, ms);
  }
  setTimeout(step, 550);
}
function tapPad(i) {
  if (st.phase !== 'input') return;
  lite(i, 240);
  tone(i, 240);
  if (L.check(st.seq, i, st.idx) === 'wrong') { gameOver(); return; }
  st.idx++;
  if (st.idx === st.seq.length) {
    st.phase = 'wait';
    hud('درست بود!');
    setTimeout(function () {
      st.level++;
      st.seq = L.extend(st.seq, L.nextColor(Math.random));
      playSeq();
    }, 650);
  }
}
function gameOver() {
  st.phase = 'over';
  lockPads(true);
  var best = bestOf('wog-simon-best', st.level);
  hud('باختی در سطح ' + fa(st.level) + ' · رکورد: ' + fa(best));
  ovl('باختی!', 'به سطح ' + fa(st.level) + ' رسیدی · رکورد: ' + fa(best), 'بازی دوباره', start);
}
function draw() {
  APP.innerHTML = '';
  var box = ce('div', 'sbox');
  var top = ce('div', 'rowc');
  var bn = ce('button', 'btn gold', 'بازی جدید');
  bn.setAttribute('data-smoke', '1');
  bn.onclick = start;
  top.appendChild(bn);
  box.appendChild(top);
  var grid = ce('div', 'sgrid');
  for (var i = 0; i < 4; i++) {
    (function (i) {
      var p = ce('button', 'pad');
      p.type = 'button';
      p.style.background = PCOLORS[i];
      p.onclick = function () { tapPad(i); };
      grid.appendChild(p);
    })(i);
  }
  box.appendChild(grid);
  APP.appendChild(box);
}
$('#hint').textContent = 'دنبالهٔ نور و صدا را ببین و به همان ترتیب لمس کن؛ هر سطح یک رنگ اضافه و کمی سریع‌تر می‌شود.';
draw();
var b0 = store.get('wog-simon-best');
hud('آماده‌ای؟ رکورد: ' + fa(b0 === null ? 0 : parseInt(b0, 10) || 0));
"""
SIMON_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0b1220;color:#e8ecf4;font-family:Tahoma,sans-serif}
header h1{color:#d9a441;font-size:20px}
#app{padding:8px;text-align:center}
.rowc{display:flex;gap:8px;justify-content:center;margin:8px 0}
.btn{min-height:42px;padding:8px 16px;border-radius:10px;border:1px solid #2a3b5e;background:#14203a;color:#e8ecf4;font-size:15px;cursor:pointer;touch-action:manipulation}
.btn.gold{background:#d9a441;color:#14203a;border-color:#d9a441;font-weight:bold}
.sgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:400px;margin:12px auto}
.pad{aspect-ratio:1/1;border:0;border-radius:16px;opacity:.55;cursor:pointer;touch-action:manipulation;transition:opacity .12s,transform .12s}
.pad.lit{opacity:1;transform:scale(.96)}
.pad:disabled{cursor:default;opacity:.55}
"""
SIMON_TESTS = [
    ("رشد دنباله", r"""var seq=[];
for(var i=0;i<12;i++){var c=L.nextColor(rng);T.ok(c>=0&&c<4,'range');seq=L.extend(seq,c);T.eq(seq.length,i+1,'growth');}
T.eq(seq.length,12,'final');"""),
    ("منطق بررسی و عدم تغییر دنباله", r"""var seq=[0,1,2];
T.eq(L.check(seq,0,0),'ok');T.eq(L.check(seq,1,0),'wrong');
T.eq(L.check(seq,1,1),'ok');T.eq(L.check(seq,2,2),'ok');
T.eq(L.check(seq,3,0),'wrong');T.eq(L.check(seq,0,3),'wrong');T.eq(L.check(seq,0,-1),'wrong');
var a=[0],b=L.extend(a,2);
T.eq(a.length,1,'no mutate');T.eq(JSON.stringify(b),'[0,2]');"""),
    ("سرعت پخش کاهنده و کف‌دار", r"""T.eq(L.speedFor(1),900,'base');
T.ok(L.speedFor(5)<L.speedFor(1),'faster 5');
T.ok(L.speedFor(10)<L.speedFor(5),'faster 10');
T.eq(L.speedFor(100),320,'floor');
var prev=Infinity;
for(var lv=1;lv<=30;lv++){var ms=L.speedFor(lv);T.ok(ms<=prev,'non-increasing');T.ok(ms>=320,'bounded');prev=ms;}"""),
    ("شبیه‌سازی خودکار ۱۲ سطح", r"""var seq=[];
for(var lv=1;lv<=12;lv++){
 seq=L.extend(seq,L.nextColor(rng));
 T.eq(seq.length,lv,'level size');
 for(var i=0;i<seq.length;i++)T.eq(L.check(seq,seq[i],i),'ok','replay');
 var w=(seq[seq.length-1]+1)%4;
 T.eq(L.check(seq,w,seq.length-1),'wrong','miss');
}
T.eq(seq.length,12,'done');"""),
]

GAMES = [
    G(slug="nonogram", title="نونوگرام", cat="puzzle", icon="▦",
      g1="#3fb8af", g2="#14203a",
      desc="نونوگرام ۵×۵ و ۸×۸ با الگوهای تصادفی؛ سرنخ هر سطر و ستون را بخوان و خانه‌های درست را پر کن.",
      hint="لمس خانه: پر ← علامت × ← خالی. سرنخ هر خط، طول رشته‌های پیوستهٔ آن است.",
      logic=NONOGRAM_LOGIC, ui=NONOGRAM_UI, css=NONOGRAM_CSS,
      engines=("common",), tests=NONOGRAM_TESTS, seed=12345),
    G(slug="mastermind", title="رمزنگار", cat="puzzle", icon="●",
      g1="#d9a441", g2="#9b6dd6",
      desc="رمز ۴ رنگی از میان ۶ رنگ را در حدس ۱۰گانه کشف کن؛ راهنمای سیاه و سفید مسیر را نشان می‌دهد.",
      hint="از پالت رنگ انتخاب کن و روی خانه بزن، یا هر خانه را لمس کن تا رنگش بچرخد. ۱۰ حدس داری.",
      logic=MASTERMIND_LOGIC, ui=MASTERMIND_UI, css=MASTERMIND_CSS,
      engines=("common",), tests=MASTERMIND_TESTS, seed=12345),
    G(slug="simon", title="سیمون", cat="puzzle", icon="♪",
      g1="#e26d5c", g2="#4a90d9",
      desc="دنبالهٔ نور و صدا را به خاطر بسپار و تکرار کن؛ هر سطح یک گام بلندتر و سریع‌تر می‌شود.",
      hint="دنبالهٔ نور و صدا را ببین و به همان ترتیب لمس کن؛ هر سطح یک رنگ اضافه و کمی سریع‌تر می‌شود.",
      logic=SIMON_LOGIC, ui=SIMON_UI, css=SIMON_CSS,
      engines=("common",), tests=SIMON_TESTS, seed=12345),
]
