# -*- coding: utf-8 -*-
# AG-E3: 4 puzzle games in one batch — hanoi, maze, 8queens, lights-out. cat=puzzle, engines=(common,)
from lib_mini import G

SHARED_CSS = r"""
.p-bar{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;align-items:center;margin:12px 0 4px}
.btn{min-width:44px;min-height:40px;padding:7px 13px;border-radius:9px;border:1px solid #2a3b5e;background:#14203a;color:#cdd8ee;font-size:14px;cursor:pointer;touch-action:manipulation;font-family:inherit}
.btn.p-gold{background:#d9a441;border-color:#d9a441;color:#10192e;font-weight:bold}
.btn.p-on{border-color:#d9a441;color:#d9a441}
.p-lbl{font-size:13px;color:#8fa3c8}
"""

# ============================================================ 1. hanoi
hanoi_logic = r"""
var WOG_LOGIC = (function () {
  function initial(n) {
    var a = [], i;
    for (i = n; i >= 1; i--) a.push(i);
    return [a, [], []];
  }
  function move(state, from, to) {
    if (from === to) return false;
    if (from < 0 || from > 2 || to < 0 || to > 2) return false;
    if (!state[from].length) return false;
    if (state[to].length && state[to][state[to].length - 1] < state[from][state[from].length - 1]) return false;
    state[to].push(state[from].pop());
    return true;
  }
  function isSolved(state, n) {
    var t = state[2];
    if (t.length !== n) return false;
    for (var i = 0; i < n; i++) if (t[i] !== n - i) return false;
    return true;
  }
  function optimal(n) { return Math.pow(2, n) - 1; }
  function rec(n, from, to, via, out) {
    if (n <= 0) return;
    rec(n - 1, from, via, to, out);
    out.push({ from: from, to: to });
    rec(n - 1, via, to, from, out);
  }
  function solveSeq(n) {
    var out = [];
    rec(n, 0, 2, 1, out);
    return out;
  }
  return { initial: initial, move: move, isSolved: isSolved, optimal: optimal, solveSeq: solveSeq };
})();
"""

hanoi_ui = r"""
var n = 3, st, sel = -1, moves = 0, busy = false;
function diskW(d) { return 24 + d * 11; }
function newGame(k) {
  n = k; st = L.initial(n); sel = -1; moves = 0; busy = false;
  store.set('wog-hanoi-n', String(n));
  render();
}
function render() {
  var app = $('#app');
  app.innerHTML = '';
  var wrap = ce('div', 'h-wrap');
  for (var t = 0; t < 3; t++) {
    (function (t) {
      var col = ce('div', 'h-col' + (sel === t ? ' h-sel' : ''));
      var disks = ce('div', 'h-disks');
      for (var i = 0; i < st[t].length; i++) {
        var d = ce('div', 'h-disk');
        d.style.width = diskW(st[t][i]) + 'px';
        disks.appendChild(d);
      }
      col.appendChild(disks);
      col.appendChild(ce('div', 'h-pole'));
      col.appendChild(ce('div', 'h-base'));
      col.appendChild(ce('div', 'h-label', 'برج ' + fa(t + 1)));
      col.addEventListener('click', function () { tapTower(t); });
      wrap.appendChild(col);
    })(t);
  }
  app.appendChild(wrap);
  var bar = ce('div', 'p-bar');
  var nb = ce('button', 'btn', 'بازی جدید');
  nb.setAttribute('data-smoke', '1');
  nb.addEventListener('click', function () { newGame(n); });
  bar.appendChild(nb);
  var sb = ce('button', 'btn p-gold', 'حل خودکار');
  sb.addEventListener('click', autoSolve);
  bar.appendChild(sb);
  bar.appendChild(ce('span', 'p-lbl', 'تعداد دیسک:'));
  for (var k = 3; k <= 7; k++) {
    (function (k) {
      var b = ce('button', 'btn' + (k === n ? ' p-on' : ''), fa(k));
      b.addEventListener('click', function () { if (!busy) newGame(k); });
      bar.appendChild(b);
    })(k);
  }
  app.appendChild(bar);
  hud('حرکت‌ها: ' + fa(moves) + ' · حداقل ممکن: ' + fa(L.optimal(n)));
}
function tapTower(t) {
  if (busy) return;
  if (sel === -1) {
    if (st[t].length) { sel = t; render(); }
    else toast('این برج خالی است');
    return;
  }
  if (sel === t) { sel = -1; render(); return; }
  if (L.move(st, sel, t)) {
    moves++; sel = -1; render();
    if (L.isSolved(st, n)) win();
  } else {
    toast('حرکت نامعتبر: دیسک بزرگ‌تر روی کوچک‌تر نمی‌نشیند');
  }
}
function win() {
  busy = true;
  ovl('آفرین! برج حل شد', fa(moves) + ' حرکت (بهینه: ' + fa(L.optimal(n)) + ')', 'بازی جدید', function () { newGame(n); });
}
function autoSolve() {
  if (busy) return;
  busy = true; sel = -1;
  st = L.initial(n); moves = 0;
  var seq = L.solveSeq(n), i = 0;
  render();
  var iv = setInterval(function () {
    if (i >= seq.length) { clearInterval(iv); busy = false; win(); return; }
    L.move(st, seq[i].from, seq[i].to);
    moves++; i++; render();
  }, 260);
}
newGame(parseInt(store.get('wog-hanoi-n') || '3', 10) || 3);
$('#hint').textContent = 'اول روی برج مبدأ بزن، بعد روی برج مقصد. دیسک بزرگ‌تر هرگز روی کوچک‌تر نمی‌نشیند.';
"""

hanoi_css = r"""
.h-wrap{display:flex;justify-content:center;gap:16px;margin:20px 0 10px}
.h-col{position:relative;width:108px;height:238px;background:#14203a;border:2px solid #223252;border-radius:12px;cursor:pointer;touch-action:manipulation}
.h-col.h-sel{border-color:#d9a441;box-shadow:0 0 0 3px rgba(217,164,65,.25)}
.h-base{position:absolute;bottom:10px;left:6px;right:6px;height:8px;border-radius:4px;background:#3fb8af}
.h-pole{position:absolute;bottom:10px;left:50%;width:8px;height:186px;margin-left:-4px;border-radius:4px 4px 0 0;background:#2a3b5e}
.h-disks{position:absolute;bottom:18px;left:0;right:0;display:flex;flex-direction:column-reverse;align-items:center}
.h-disk{height:20px;border-radius:10px;margin:1px 0;background:linear-gradient(180deg,#e5b866,#b07f27)}
.h-label{position:absolute;bottom:-24px;left:0;right:0;text-align:center;font-size:12px;color:#8fa3c8}
"""

hanoi_tests = [
    ("قانونی بودن حرکت‌ها", r"""
var s = L.initial(3);
T.eq(s, [[3,2,1],[],[]], 'initial state');
T.ok(!L.move(s, 0, 0), 'same tower rejected');
T.ok(!L.move(s, 1, 0), 'empty source rejected');
T.ok(!L.move(s, 5, 0), 'bad index rejected');
T.ok(L.move(s, 0, 2), 'legal move ok');
T.ok(!L.move(s, 0, 2), 'bigger-on-smaller rejected');
T.eq(s[2], [1], 'state unchanged by illegal move');
T.eq(s[0], [3, 2], 'source unchanged by illegal move');
T.eq(L.optimal(1), 1, 'optimal 1');
T.eq(L.optimal(3), 7, 'optimal 3');
T.eq(L.optimal(7), 127, 'optimal 7');
"""),
    ("پخش راه‌حل canonical برای n=1..7", r"""
for (var n = 1; n <= 7; n++) {
  var seq = L.solveSeq(n);
  T.eq(seq.length, Math.pow(2, n) - 1, 'seq length n=' + n);
  var st = L.initial(n);
  for (var i = 0; i < seq.length; i++) {
    T.ok(L.move(st, seq[i].from, seq[i].to), 'replay move valid n=' + n + ' i=' + i);
  }
  T.ok(L.isSolved(st, n), 'solved after replay n=' + n);
}
"""),
    ("تشخیص برد", r"""
T.ok(L.isSolved([[], [], [4, 3, 2, 1]], 4), 'win detected');
T.ok(!L.isSolved([[], [], [1, 2, 3, 4]], 4), 'wrong order not win');
T.ok(!L.isSolved([[], [], [4, 3, 2]], 4), 'incomplete not win');
T.ok(!L.isSolved([[4], [3, 2, 1], []], 4), 'wrong tower not win');
T.ok(!L.isSolved(L.initial(4), 4), 'start not win');
"""),
]

# ============================================================ 2. maze
maze_logic = r"""
var WOG_LOGIC = (function () {
  function genMaze(n, rng) {
    rng = rng || Math.random;
    var W = 2 * n + 1, g = [], vis = [], i, j;
    for (i = 0; i < W; i++) { g.push([]); for (j = 0; j < W; j++) g[i].push(1); }
    for (i = 0; i < n; i++) { vis.push([]); for (j = 0; j < n; j++) vis[i].push(false); }
    var DR = [-1, 1, 0, 0], DC = [0, 0, -1, 1];
    var stack = [[0, 0]];
    vis[0][0] = true; g[1][1] = 0;
    while (stack.length) {
      var cur = stack[stack.length - 1], opts = [], d;
      for (d = 0; d < 4; d++) {
        var nr = cur[0] + DR[d], nc = cur[1] + DC[d];
        if (nr >= 0 && nr < n && nc >= 0 && nc < n && !vis[nr][nc]) opts.push(d);
      }
      if (!opts.length) { stack.pop(); continue; }
      d = opts[Math.floor(rng() * opts.length)];
      var r2 = cur[0] + DR[d], c2 = cur[1] + DC[d];
      vis[r2][c2] = true;
      g[cur[0] * 2 + 1 + DR[d]][cur[1] * 2 + 1 + DC[d]] = 0;
      g[r2 * 2 + 1][c2 * 2 + 1] = 0;
      stack.push([r2, c2]);
    }
    return { n: n, g: g };
  }
  function neighbors(maze, r, c) {
    var n = maze.n, out = [], DR = [-1, 1, 0, 0], DC = [0, 0, -1, 1];
    for (var d = 0; d < 4; d++) {
      var nr = r + DR[d], nc = c + DC[d];
      if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
      if (maze.g[r * 2 + 1 + DR[d]][c * 2 + 1 + DC[d]] === 0) out.push([nr, nc]);
    }
    return out;
  }
  function bfs(maze, start, goal) {
    var n = maze.n, prev = [], seen = [], i, j;
    for (i = 0; i < n; i++) { prev.push([]); seen.push([]); for (j = 0; j < n; j++) { prev[i].push(null); seen[i].push(false); } }
    var q = [start];
    seen[start[0]][start[1]] = true;
    var head = 0;
    while (head < q.length) {
      var cur = q[head++];
      if (cur[0] === goal[0] && cur[1] === goal[1]) break;
      var nb = neighbors(maze, cur[0], cur[1]);
      for (var k = 0; k < nb.length; k++) {
        if (!seen[nb[k][0]][nb[k][1]]) { seen[nb[k][0]][nb[k][1]] = true; prev[nb[k][0]][nb[k][1]] = cur; q.push(nb[k]); }
      }
    }
    if (!seen[goal[0]][goal[1]]) return null;
    var path = [], cur2 = goal;
    while (cur2) { path.push(cur2); cur2 = prev[cur2[0]][cur2[1]]; }
    path.reverse();
    return path;
  }
  function isPerfect(maze) {
    var n = maze.n, g = maze.g, edges = 0, r, c;
    for (r = 0; r < n; r++) for (c = 0; c < n; c++) {
      if (c + 1 < n && g[2 * r + 1][2 * c + 2] === 0) edges++;
      if (r + 1 < n && g[2 * r + 2][2 * c + 1] === 0) edges++;
    }
    if (edges !== n * n - 1) return false;
    var seen = [], stack = [[0, 0]], count = 0;
    for (r = 0; r < n; r++) { seen.push([]); for (c = 0; c < n; c++) seen[r].push(false); }
    seen[0][0] = true;
    while (stack.length) {
      var cur = stack.pop(); count++;
      var nb = neighbors(maze, cur[0], cur[1]);
      for (var k = 0; k < nb.length; k++) if (!seen[nb[k][0]][nb[k][1]]) { seen[nb[k][0]][nb[k][1]] = true; stack.push(nb[k]); }
    }
    return count === n * n;
  }
  function canMove(maze, r, c, dr, dc) {
    var n = maze.n, nr = r + dr, nc = c + dc;
    if (nr < 0 || nr >= n || nc < 0 || nc >= n) return false;
    return maze.g[2 * r + 1 + dr][2 * c + 1 + dc] === 0;
  }
  return { genMaze: genMaze, neighbors: neighbors, bfs: bfs, isPerfect: isPerfect, canMove: canMove };
})();
"""

maze_ui = r"""
var N = 11, mz, pr, pc, mvs, t0, timer, solved = false, S, cellEls, plEl, hintEls;
var SIZES = [11, 17, 25];
function newGame(size) {
  N = size || N;
  mz = L.genMaze(N);
  pr = 0; pc = 0; mvs = 0; solved = false; hintEls = [];
  if (timer) clearInterval(timer);
  t0 = Date.now();
  build();
  timer = setInterval(tick, 500);
  tick();
}
function tick() {
  if (solved) return;
  hud('زمان: ' + fa(Math.floor((Date.now() - t0) / 1000)) + ' ثانیه · حرکت‌ها: ' + fa(mvs) + ' · اندازه: ' + fa(N) + '×' + fa(N));
}
function build() {
  var app = $('#app');
  app.innerHTML = '';
  var W = 2 * N + 1;
  S = Math.max(7, Math.floor(350 / W));
  var grid = ce('div', 'm-grid');
  grid.style.gridTemplateColumns = 'repeat(' + W + ', ' + S + 'px)';
  grid.style.gridAutoRows = S + 'px';
  cellEls = [];
  for (var r = 0; r < W; r++) {
    cellEls.push([]);
    for (var c = 0; c < W; c++) {
      var d = ce('div', mz.g[r][c] ? 'm-w' : 'm-o');
      grid.appendChild(d);
      cellEls[r].push(d);
    }
  }
  cellEls[1][1].className = 'm-o m-start';
  cellEls[2 * N - 1][2 * N - 1].className = 'm-o m-exit';
  plEl = ce('div', 'm-player');
  plEl.style.width = S + 'px';
  plEl.style.height = S + 'px';
  grid.appendChild(plEl);
  app.appendChild(grid);
  var bar = ce('div', 'p-bar');
  var nb = ce('button', 'btn', 'بازی جدید');
  nb.setAttribute('data-smoke', '1');
  nb.addEventListener('click', function () { newGame(N); });
  bar.appendChild(nb);
  var hb = ce('button', 'btn p-gold', 'راهنما');
  hb.addEventListener('click', showHint);
  bar.appendChild(hb);
  for (var i = 0; i < SIZES.length; i++) {
    (function (s) {
      var b = ce('button', 'btn' + (s === N ? ' p-on' : ''), fa(s) + '×' + fa(s));
      b.addEventListener('click', function () { newGame(s); });
      bar.appendChild(b);
    })(SIZES[i]);
  }
  app.appendChild(bar);
  var pad = ce('div', 'm-pad');
  var dirs = [[-1, 0, '▲'], [1, 0, '▼'], [0, -1, '◀'], [0, 1, '▶']];
  for (var k = 0; k < 4; k++) {
    (function (dr, dc, lbl) {
      var b = ce('button', 'btn', lbl);
      b.addEventListener('click', function () { step(dr, dc); });
      pad.appendChild(b);
    })(dirs[k][0], dirs[k][1], dirs[k][2]);
  }
  app.appendChild(pad);
  place();
}
function place() {
  plEl.style.transform = 'translate(' + (pc * 2 + 1) * S + 'px,' + (pr * 2 + 1) * S + 'px)';
}
function step(dr, dc) {
  if (solved) return;
  if (L.canMove(mz, pr, pc, dr, dc)) {
    pr += dr; pc += dc; mvs++;
    place(); tick();
    if (pr === N - 1 && pc === N - 1) win();
  }
}
function clearHint() {
  for (var i = 0; i < hintEls.length; i++) hintEls[i].className = 'm-o';
  hintEls = [];
}
function showHint() {
  if (solved) return;
  clearHint();
  var path = L.bfs(mz, [pr, pc], [N - 1, N - 1]);
  if (!path) { toast('مسیری وجود ندارد!'); return; }
  for (var i = 0; i < path.length; i++) {
    var el = cellEls[path[i][0] * 2 + 1][path[i][1] * 2 + 1];
    if (el.className === 'm-o') { el.className = 'm-o m-hint'; hintEls.push(el); }
  }
  toast('کوتاه‌ترین مسیر تا خروجی: ' + fa(path.length - 1) + ' گام');
}
function win() {
  solved = true;
  clearInterval(timer);
  var sec = Math.floor((Date.now() - t0) / 1000);
  bestOf('wog-maze-best-' + N, mvs);
  ovl('به خروجی رسیدی!', 'زمان: ' + fa(sec) + ' ثانیه · حرکت‌ها: ' + fa(mvs), 'بازی جدید', function () { newGame(N); });
}
document.addEventListener('keydown', function (e) {
  var map = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1], w: [-1, 0], s: [1, 0], a: [0, -1], d: [0, 1] };
  var m = map[e.key];
  if (m) { e.preventDefault(); step(m[0], m[1]); }
});
newGame(11);
$('#hint').textContent = 'با فلش‌ها یا دکمه‌های جهت‌دار حرکت کن و خودت را به خانهٔ فیروزه‌ای برسان. راهنما کوتاه‌ترین مسیر را نشان می‌دهد.';
"""

maze_css = r"""
.m-grid{position:relative;display:grid;direction:ltr;width:max-content;margin:14px auto;padding:4px;background:#14203a;border-radius:8px}
.m-w{background:#0d1526;border-radius:1px}
.m-o{background:#223252}
.m-start{background:#2b4a3f}
.m-exit{background:#3fb8af;box-shadow:0 0 6px #3fb8af inset}
.m-hint{background:#3f6f6b}
.m-player{position:absolute;top:0;left:0;border-radius:30%;background:#d9a441;box-shadow:0 0 8px rgba(217,164,65,.8);transition:transform .12s;pointer-events:none;z-index:2}
.m-pad{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:10px 0 4px;direction:ltr}
.m-pad .btn{width:56px}
"""

maze_tests = [
    ("اتصال کامل: ۵۰ بذر × ۳ اندازه", r"""
var sizes = [11, 17, 25], conn = 0;
for (var s = 0; s < 3; s++) {
  for (var i = 0; i < 50; i++) {
    var mz = L.genMaze(sizes[s], rng);
    var p = L.bfs(mz, [0, 0], [sizes[s] - 1, sizes[s] - 1]);
    T.ok(p && p.length >= 2, 'path found size=' + sizes[s] + ' i=' + i);
    T.eq(p[0], [0, 0], 'path starts at start');
    var e = p[p.length - 1];
    T.ok(e[0] === sizes[s] - 1 && e[1] === sizes[s] - 1, 'path ends at exit');
    conn++;
  }
}
T.eq(conn, 150, '150 mazes all connected');
"""),
    ("کامل بودن (بدون حلقه) و تشخیص خرابی", r"""
for (var t = 0; t < 21; t++) {
  var n = [11, 17, 25][t % 3];
  var mz = L.genMaze(n, rng);
  T.ok(L.isPerfect(mz), 'perfect n=' + n);
  var g = mz.g, broken = false;
  for (var r = 0; r < n && !broken; r++) for (var c = 0; c < n - 1 && !broken; c++) {
    if (g[2 * r + 1][2 * c + 2] === 1) { g[2 * r + 1][2 * c + 2] = 0; broken = true; }
  }
  T.ok(!L.isPerfect(mz), 'cycle detected n=' + n);
  var g2 = L.genMaze(n, rng).g, closed = false;
  for (var r2 = 0; r2 < n && !closed; r2++) for (var c2 = 0; c2 < n - 1 && !closed; c2++) {
    if (g2[2 * r2 + 1][2 * c2 + 2] === 0) { g2[2 * r2 + 1][2 * c2 + 2] = 1; closed = true; }
  }
  T.ok(!L.isPerfect({ n: n, g: g2 }), 'disconnected detected n=' + n);
}
"""),
    ("اعتبار مسیر راهنما (کوتاه‌ترین مسیر BFS)", r"""
var mz3 = L.genMaze(17, rng);
var path = L.bfs(mz3, [0, 0], [16, 16]);
T.ok(path && path.length >= 2, 'hint path exists');
for (var k = 1; k < path.length; k++) {
  var a = path[k - 1], b = path[k];
  var dr = b[0] - a[0], dc = b[1] - a[1];
  T.ok(Math.abs(dr) + Math.abs(dc) === 1, 'adjacent step k=' + k);
  T.ok(mz3.g[2 * a[0] + 1 + dr][2 * a[1] + 1 + dc] === 0, 'no wall crossed k=' + k);
}
var dist = [], Q = [[0, 0]];
for (var i = 0; i < 17; i++) { dist.push([]); for (var j = 0; j < 17; j++) dist[i].push(-1); }
dist[0][0] = 0;
for (var h = 0; h < Q.length; h++) {
  var cur = Q[h], nb = L.neighbors(mz3, cur[0], cur[1]);
  for (var x = 0; x < nb.length; x++) if (dist[nb[x][0]][nb[x][1]] < 0) { dist[nb[x][0]][nb[x][1]] = dist[cur[0]][cur[1]] + 1; Q.push(nb[x]); }
}
T.eq(path.length, dist[16][16] + 1, 'hint path is shortest');
"""),
    ("حرکت بازیگر و دیوارها", r"""
var mz = L.genMaze(11, rng);
var blocked = 0;
for (var r = 0; r < 11; r++) for (var c = 0; c < 11; c++) {
  var nb = L.neighbors(mz, r, c);
  T.ok(nb.length >= 1 && nb.length <= 4, 'neighbor count bounds');
  var cm = 0;
  cm += L.canMove(mz, r, c, -1, 0) ? 1 : 0;
  cm += L.canMove(mz, r, c, 1, 0) ? 1 : 0;
  cm += L.canMove(mz, r, c, 0, -1) ? 1 : 0;
  cm += L.canMove(mz, r, c, 0, 1) ? 1 : 0;
  T.eq(cm, nb.length, 'canMove==neighbors at ' + r + ',' + c);
  if (nb.length === 0) blocked++;
}
T.eq(blocked, 0, 'no isolated cell');
T.eq(mz.g[0][1], 1, 'north border wall');
T.eq(mz.g[1][0], 1, 'west border wall');
T.eq(mz.g[21][22], 1, 'east border wall');
T.eq(mz.g[22][21], 1, 'south border wall');
T.eq(mz.g[1][1], 0, 'start cell open');
T.eq(mz.g[21][21], 0, 'exit cell open');
T.ok(!L.canMove(mz, 0, 0, -1, 0), 'cannot move outside north');
T.ok(!L.canMove(mz, 0, 0, 0, -1), 'cannot move outside west');
"""),
]

# ============================================================ 3. 8queens
queens_logic = r"""
var WOG_LOGIC = (function () {
  function attacks(q1, q2) {
    if (q1[0] === q2[0] && q1[1] === q2[1]) return false;
    return q1[0] === q2[0] || q1[1] === q2[1] || Math.abs(q1[0] - q2[0]) === Math.abs(q1[1] - q2[1]);
  }
  function hasConflict(queens) {
    for (var i = 0; i < queens.length; i++)
      for (var j = i + 1; j < queens.length; j++)
        if (attacks(queens[i], queens[j])) return true;
    return false;
  }
  var _sols = null;
  function solveAll() {
    if (_sols) return _sols;
    var sols = [], q = [];
    function ok(r, c) {
      for (var i = 0; i < r; i++)
        if (q[i] === c || q[i] - i === c - r || q[i] + i === c + r) return false;
      return true;
    }
    function rec(r) {
      if (r === 8) { sols.push(q.slice()); return; }
      for (var c = 0; c < 8; c++) if (ok(r, c)) { q.push(c); rec(r + 1); q.pop(); }
    }
    rec(0);
    _sols = sols;
    return sols;
  }
  function pairs(colArr) {
    var out = [];
    for (var r = 0; r < colArr.length; r++) out.push([r, colArr[r]]);
    return out;
  }
  function firstSolution() { return pairs(solveAll()[0]); }
  return { attacks: attacks, hasConflict: hasConflict, solveAll: solveAll, pairs: pairs, firstSolution: firstSolution };
})();
"""

queens_ui = r"""
var queens = [], solvedShown = false;
function hasQ(r, c) {
  for (var i = 0; i < queens.length; i++) if (queens[i][0] === r && queens[i][1] === c) return i;
  return -1;
}
function conflictsAt(r, c) {
  for (var i = 0; i < queens.length; i++) {
    var q = queens[i];
    if (q[0] === r && q[1] === c) continue;
    if (L.attacks(q, [r, c])) return true;
  }
  return false;
}
function render() {
  var app = $('#app');
  app.innerHTML = '';
  var bd = ce('div', 'q-board');
  for (var r = 0; r < 8; r++) for (var c = 0; c < 8; c++) {
    (function (r, c) {
      var idx = hasQ(r, c);
      var cls = 'q-cell ' + ((r + c) % 2 ? 'q-dark' : 'q-light');
      if (idx >= 0) cls += conflictsAt(r, c) ? ' q-bad' : ' q-ok';
      var cell = ce('div', cls, idx >= 0 ? '♕' : '');
      cell.addEventListener('click', function () { tap(r, c); });
      bd.appendChild(cell);
    })(r, c);
  }
  app.appendChild(bd);
  var bar = ce('div', 'p-bar');
  var nb = ce('button', 'btn', 'بازی جدید');
  nb.setAttribute('data-smoke', '1');
  nb.addEventListener('click', function () { queens = []; solvedShown = false; render(); });
  bar.appendChild(nb);
  var sb = ce('button', 'btn p-gold', 'راه‌حل');
  sb.addEventListener('click', function () { queens = L.firstSolution(); render(); maybeWin(); toast('یک راه‌حل نشان داده شد'); });
  bar.appendChild(sb);
  var cb = ce('button', 'btn', 'پاک کردن');
  cb.addEventListener('click', function () { queens = []; solvedShown = false; render(); });
  bar.appendChild(cb);
  app.appendChild(bar);
  hud('وزیرها: ' + fa(queens.length) + ' از ۸ · تعارض: ' + (L.hasConflict(queens) ? 'دارد' : 'ندارد') + ' · کل راه‌حل‌ها: ' + fa(L.solveAll().length));
}
function maybeWin() {
  if (queens.length === 8 && !L.hasConflict(queens) && !solvedShown) {
    solvedShown = true;
    ovl('هشت وزیر حل شد!', 'هیچ دو وزیری همدیگر را تهدید نمی‌کنند', 'بازی جدید', function () { queens = []; solvedShown = false; render(); });
  }
}
function tap(r, c) {
  var idx = hasQ(r, c);
  if (idx >= 0) queens.splice(idx, 1);
  else queens.push([r, c]);
  render();
  maybeWin();
}
render();
$('#hint').textContent = 'روی خانه‌ها بزن تا وزیر بگذاری یا برداری. هدف: ۸ وزیر بدون هیچ تعارضی.';
"""

queens_css = r"""
.q-board{display:grid;grid-template-columns:repeat(8,44px);grid-template-rows:repeat(8,44px);width:max-content;margin:14px auto;border:3px solid #223252;border-radius:8px;overflow:hidden}
.q-cell{display:flex;align-items:center;justify-content:center;font-size:26px;cursor:pointer;user-select:none;touch-action:manipulation}
.q-light{background:#2a3b5e;color:#d9a441}
.q-dark{background:#1b2a47;color:#d9a441}
.q-ok{color:#67b98a}
.q-bad{background:#5e2a2a;color:#e26d5c}
@media(max-width:420px){.q-board{grid-template-columns:repeat(8,40px);grid-template-rows:repeat(8,40px)}}
"""

queens_tests = [
    ("جدول حملهٔ وزیر", r"""
T.ok(L.attacks([0, 0], [0, 7]), 'same row attacks');
T.ok(L.attacks([0, 0], [7, 0]), 'same col attacks');
T.ok(L.attacks([2, 3], [5, 6]), 'diagonal attacks');
T.ok(L.attacks([2, 3], [0, 1]), 'anti-diagonal attacks');
T.ok(!L.attacks([0, 0], [1, 2]), 'knight move is safe');
T.ok(!L.attacks([0, 0], [7, 1]), 'far squares safe');
T.ok(!L.attacks([3, 3], [3, 3]), 'same square is not an attack pair');
"""),
    ("مقایسه با نیروی بی‌رحم روی تخته‌های تصادفی", r"""
var allPos = [];
for (var r = 0; r < 8; r++) for (var c = 0; c < 8; c++) allPos.push([r, c]);
for (var it = 0; it < 30; it++) {
  var pool = allPos.slice(), k = 1 + Math.floor(rng() * 8);
  for (var i = 0; i < k; i++) {
    var j = i + Math.floor(rng() * (pool.length - i));
    var tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp;
  }
  var qs = pool.slice(0, k), brute = false;
  for (var a = 0; a < qs.length && !brute; a++)
    for (var b = a + 1; b < qs.length; b++) {
      var p1 = qs[a], p2 = qs[b];
      var atk = (p1[0] === p2[0]) || (p1[1] === p2[1]) || (Math.abs(p1[0] - p2[0]) === Math.abs(p1[1] - p2[1]));
      T.eq(L.attacks(p1, p2), atk, 'attacks matches brute it=' + it);
      if (atk) brute = true;
    }
  T.eq(L.hasConflict(qs), brute, 'hasConflict matches brute it=' + it);
}
"""),
    ("دقیقاً ۹۲ راه‌حل، یکتا و معتبر", r"""
var sols = L.solveAll();
T.eq(sols.length, 92, 'exactly 92 solutions');
var seen = {}, okAll = true;
for (var i = 0; i < sols.length; i++) {
  var key = sols[i].join(',');
  if (seen[key]) okAll = false;
  seen[key] = 1;
  var pr = L.pairs(sols[i]);
  if (L.hasConflict(pr)) okAll = false;
  if (pr.length !== 8) okAll = false;
  var rows = {}, cols = {}, kk, rc = 0, cc = 0;
  for (var k = 0; k < 8; k++) { rows[pr[k][0]] = 1; cols[pr[k][1]] = 1; }
  for (kk in rows) rc++;
  for (kk in cols) cc++;
  if (rc !== 8 || cc !== 8) okAll = false;
}
T.ok(okAll, 'all 92 unique and conflict-free');
T.ok(L.solveAll() === sols, 'solver result is cached');
"""),
    ("اولین راه‌حل و تشخیص برد", r"""
var fs = L.firstSolution();
T.eq(fs.length, 8, 'first solution has 8 queens');
T.ok(!L.hasConflict(fs), 'first solution conflict-free');
T.ok(L.hasConflict([[0, 0], [0, 1]]), 'row conflict detected');
T.ok(L.hasConflict([[0, 0], [1, 1]]), 'diagonal conflict detected');
T.ok(!L.hasConflict([]), 'empty board no conflict');
T.ok(!L.hasConflict([[0, 0], [1, 2], [2, 4]]), 'non-attacking triple ok');
"""),
]

# ============================================================ 4. lights-out
lights_logic = r"""
var WOG_LOGIC = (function () {
  function toggle(state, r, c) {
    var n = state.length;
    var cells = [[r, c], [r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]];
    for (var i = 0; i < cells.length; i++) {
      var rr = cells[i][0], cc = cells[i][1];
      if (rr < 0 || rr >= n || cc < 0 || cc >= state[rr].length) continue;
      state[rr][cc] = state[rr][cc] ? 0 : 1;
    }
    return state;
  }
  function isWin(board) {
    for (var r = 0; r < board.length; r++)
      for (var c = 0; c < board[r].length; c++)
        if (board[r][c]) return false;
    return true;
  }
  function genBoard(size, k, rng) {
    rng = rng || Math.random;
    var total = size * size, i, board, presses;
    for (var attempt = 0; attempt < 20; attempt++) {
      var idx = [];
      for (i = 0; i < total; i++) idx.push(i);
      for (i = 0; i < k; i++) {
        var j = i + Math.floor(rng() * (total - i));
        var t = idx[i]; idx[i] = idx[j]; idx[j] = t;
      }
      board = [];
      for (i = 0; i < size; i++) { board.push([]); for (var c = 0; c < size; c++) board[i].push(0); }
      presses = [];
      for (i = 0; i < k; i++) {
        var p = idx[i], pr = Math.floor(p / size), pc = p % size;
        presses.push([pr, pc]);
        toggle(board, pr, pc);
      }
      if (!isWin(board)) return { board: board, presses: presses };
    }
    return { board: board, presses: presses };
  }
  var _l3 = null;
  function pressesToSolve(board) {
    if (!_l3) {
      _l3 = {};
      for (var m = 0; m < 512; m++) {
        var b = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
        for (var i = 0; i < 9; i++) if ((m >> i) & 1) toggle(b, Math.floor(i / 3), i % 3);
        var key = '';
        for (var r = 0; r < 3; r++) for (var c = 0; c < 3; c++) key += b[r][c];
        _l3[key] = m;
      }
    }
    var key2 = '';
    for (var r2 = 0; r2 < 3; r2++) for (var c2 = 0; c2 < 3; c2++) key2 += board[r2][c2];
    var mask = _l3[key2];
    if (mask === undefined) return null;
    var out = [];
    for (var i2 = 0; i2 < 9; i2++) if ((mask >> i2) & 1) out.push([Math.floor(i2 / 3), i2 % 3]);
    return out;
  }
  return { toggle: toggle, genBoard: genBoard, isWin: isWin, pressesToSolve: pressesToSolve };
})();
"""

lights_ui = r"""
var SIZE = 5, board, mvs, done = false;
function litCount() {
  var n = 0;
  for (var r = 0; r < SIZE; r++) for (var c = 0; c < SIZE; c++) if (board[r][c]) n++;
  return n;
}
function bestStr(v) { return v ? fa(parseInt(v, 10)) : '—'; }
function newGame(size) {
  SIZE = size || SIZE;
  var g = L.genBoard(SIZE, SIZE === 3 ? 4 : 6, Math.random);
  board = g.board; mvs = 0; done = false;
  render();
}
function render() {
  var app = $('#app');
  app.innerHTML = '';
  var gd = ce('div', 'l-grid');
  gd.style.gridTemplateColumns = 'repeat(' + SIZE + ', 52px)';
  for (var r = 0; r < SIZE; r++) for (var c = 0; c < SIZE; c++) {
    (function (r, c) {
      var b = ce('button', 'l-cell ' + (board[r][c] ? 'l-on' : 'l-off'));
      b.addEventListener('click', function () { tap(r, c); });
      gd.appendChild(b);
    })(r, c);
  }
  app.appendChild(gd);
  var bar = ce('div', 'p-bar');
  var nb = ce('button', 'btn', 'بازی جدید');
  nb.setAttribute('data-smoke', '1');
  nb.addEventListener('click', function () { newGame(SIZE); });
  bar.appendChild(nb);
  var b3 = ce('button', 'btn' + (SIZE === 3 ? ' p-on' : ''), '۳×۳ سریع');
  b3.addEventListener('click', function () { newGame(3); });
  bar.appendChild(b3);
  var b5 = ce('button', 'btn' + (SIZE === 5 ? ' p-on' : ''), '۵×۵');
  b5.addEventListener('click', function () { newGame(5); });
  bar.appendChild(b5);
  var hb = ce('button', 'btn p-gold', 'راهنما');
  hb.addEventListener('click', hintSol);
  bar.appendChild(hb);
  app.appendChild(bar);
  hud('حرکت‌ها: ' + fa(mvs) + ' · روشن: ' + fa(litCount()) + ' · رکورد: ' + bestStr(store.get('wog-lights-best-' + SIZE)));
}
function tap(r, c) {
  if (done) return;
  L.toggle(board, r, c);
  mvs++;
  render();
  if (L.isWin(board)) {
    done = true;
    var best = bestOf('wog-lights-best-' + SIZE, mvs);
    ovl('همهٔ چراغ‌ها خاموش شد!', fa(mvs) + ' حرکت' + (best ? ' · رکورد: ' + bestStr(best) : ''), 'بازی جدید', function () { newGame(SIZE); });
  }
}
function hintSol() {
  if (SIZE !== 3) { toast('راهنما فقط در حالت ۳×۳ فعال است'); return; }
  var sol = L.pressesToSolve(board);
  if (!sol) { toast('راه‌حلی یافت نشد'); return; }
  var cells = $('#app').querySelectorAll('.l-cell');
  for (var i = 0; i < sol.length; i++) cells[sol[i][0] * SIZE + sol[i][1]].className += ' l-hint';
  toast('راه‌حل: ' + fa(sol.length) + ' خانهٔ مشخص‌شده را بزن');
  setTimeout(function () {
    var cs = $('#app').querySelectorAll('.l-hint');
    for (var i = 0; i < cs.length; i++) cs[i].className = cs[i].className.replace(' l-hint', '');
  }, 1400);
}
newGame(5);
$('#hint').textContent = 'با هر لمس، آن خانه و چهار همسایهٔ بالا/پایین/چپ/راست تغییر می‌کنند. همه را خاموش کن!';
"""

lights_css = r"""
.l-grid{display:grid;gap:6px;width:max-content;margin:16px auto}
.l-cell{width:52px;height:52px;border-radius:10px;border:2px solid #223252;cursor:pointer;touch-action:manipulation}
.l-on{background:#d9a441;box-shadow:0 0 10px rgba(217,164,65,.55)}
.l-off{background:#16233d}
.l-hint{outline:2px solid #3fb8af}
"""

lights_tests = [
    ("الگوی دقیق toggle", r"""
var b = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
L.toggle(b, 1, 1);
T.eq(b, [[0, 1, 0], [1, 1, 1], [0, 1, 0]], 'center plus shape');
L.toggle(b, 1, 1);
T.eq(b, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'toggle twice is identity');
L.toggle(b, 0, 0);
T.eq(b, [[1, 1, 0], [1, 0, 0], [0, 0, 0]], 'corner toggles 3 cells');
L.toggle(b, 0, 2);
T.eq(b, [[1, 0, 1], [1, 0, 1], [0, 0, 0]], 'top-right corner overlap');
"""),
    ("پخش دکمه‌های سازنده، ۳۰ بذر × دو اندازه", r"""
var sizes = [3, 5];
for (var s = 0; s < 2; s++) {
  var k = sizes[s] === 3 ? 4 : 6;
  for (var i = 0; i < 30; i++) {
    var g = L.genBoard(sizes[s], k, rng);
    T.eq(g.presses.length, k, 'press count size=' + sizes[s] + ' i=' + i);
    T.ok(!L.isWin(g.board), 'generated board not already solved');
    for (var p = 0; p < g.presses.length; p++) L.toggle(g.board, g.presses[p][0], g.presses[p][1]);
    T.ok(L.isWin(g.board), 'replaying presses solves i=' + i);
  }
}
"""),
    ("حل‌گر ۳×۳: حداقلی و درست", r"""
for (var t = 0; t < 5; t++) {
  var g2 = L.genBoard(3, 4, rng);
  var sol = L.pressesToSolve(g2.board);
  T.ok(sol && sol.length >= 1, 'solver found solution t=' + t);
  var b2 = [];
  for (var rr = 0; rr < 3; rr++) b2.push(g2.board[rr].slice());
  for (var p2 = 0; p2 < sol.length; p2++) L.toggle(b2, sol[p2][0], sol[p2][1]);
  T.ok(L.isWin(b2), 'solver replay solves t=' + t);
  var flatB = '';
  for (var r0 = 0; r0 < 3; r0++) for (var c0 = 0; c0 < 3; c0++) flatB += g2.board[r0][c0];
  var cnt = 0, minLen = 99;
  for (var m = 0; m < 512; m++) {
    var b3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], bits = 0;
    for (var i3 = 0; i3 < 9; i3++) if ((m >> i3) & 1) { L.toggle(b3, Math.floor(i3 / 3), i3 % 3); bits++; }
    var flat = '';
    for (var r3 = 0; r3 < 3; r3++) for (var c3 = 0; c3 < 3; c3++) flat += b3[r3][c3];
    if (flat === flatB) { cnt++; if (bits < minLen) minLen = bits; }
  }
  T.ok(cnt >= 1, 'board solvable by brute force t=' + t);
  T.eq(sol.length, minLen, 'solver presses are minimal t=' + t);
  var seenP = {};
  for (var q3 = 0; q3 < sol.length; q3++) seenP[sol[q3][0] + ',' + sol[q3][1]] = 1;
  T.eq(Object.keys(seenP).length, sol.length, 'solver presses distinct t=' + t);
}
"""),
    ("تشخیص برد و ساختار تختهٔ تولیدشده", r"""
T.ok(L.isWin([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), 'all off is win');
T.ok(!L.isWin([[0, 1, 0], [0, 0, 0], [0, 0, 0]]), 'one on is not win');
var g3 = L.genBoard(5, 6, rng);
T.eq(g3.board.length, 5, '5 rows');
T.eq(g3.board[0].length, 5, '5 cols');
T.eq(g3.presses.length, 6, '6 presses stored');
var binary = true;
for (var r = 0; r < 5; r++) for (var c = 0; c < 5; c++) if (g3.board[r][c] !== 0 && g3.board[r][c] !== 1) binary = false;
T.ok(binary, 'cells are binary');
T.ok(!L.isWin(g3.board), 'generated 5x5 board not already won');
"""),
]

GAMES = [
    G("hanoi", "برج هانوی", "puzzle", "🗼", "#d9a441", "#7a5220",
      "برج هانوی با ۳ تا ۷ دیسک: همهٔ دیسک‌ها را از برج اول به برج سوم ببر؛ دیسک بزرگ‌تر هرگز روی کوچک‌تر نمی‌نشیند.",
      "اول مبدأ، بعد مقصد. حل خودکار و شمارش حرکت‌ها با نمایش حداقل ممکن.",
      logic=hanoi_logic, ui=hanoi_ui, css=SHARED_CSS + hanoi_css, engines=("common",), tests=hanoi_tests),
    G("maze", "هزارتو", "puzzle", "🧭", "#3fb8af", "#1f6f6a",
      "هزارتوی کامل (بدون حلقه) در سه اندازه: از خانهٔ شروع تا خروجیِ فیروزه‌ای با کمترین حرکت برس.",
      "فلش‌ها یا دکمه‌های جهت‌دار برای حرکت؛ دکمهٔ راهنما کوتاه‌ترین مسیر را روشن می‌کند.",
      logic=maze_logic, ui=maze_ui, css=SHARED_CSS + maze_css, engines=("common",), tests=maze_tests),
    G("8queens", "هشت وزیر", "puzzle", "👑", "#c977d9", "#6f3a8a",
      "هشت وزیر روی تختهٔ شطرنج بچین طوری که هیچ دو وزیری همدیگر را تهدید نکنند؛ ۹۲ راه‌حل وجود دارد.",
      "لمس هر خانه وزیر می‌گذارد یا برمی‌دارد؛ تعارض‌ها زنده قرمز می‌شوند.",
      logic=queens_logic, ui=queens_ui, css=SHARED_CSS + queens_css, engines=("common",), tests=queens_tests),
    G("lights-out", "چراغ‌ها را خاموش کن", "puzzle", "💡", "#67b98a", "#2f5f4a",
      "هر لمس یک خانه و چهار همسایه‌اش را تغییر می‌دهد؛ همهٔ چراغ‌ها را خاموش کن. حالت سریع ۳×۳ هم دارد.",
      "تخته‌ها همیشه قابل حل‌اند؛ رکورد کمترین حرکت برای هر اندازه ذخیره می‌شود.",
      logic=lights_logic, ui=lights_ui, css=SHARED_CSS + lights_css, engines=("common",), tests=lights_tests),
]
