# -*- coding: utf-8 -*-
"""Batch J — شانس و سرگرمی."""
from lib import G

GAMES = [

# ============================================================ guess-number
G(slug="guess-number", title="حدس عدد", cat="luck", icon="🔢", g1="#5b3fa8", g2="#d9a441",
  desc="عدد مخفی بین ۱ تا ۱۰۰ را با کمترین تلاش پیدا کن؛ راهنمای گرم/سرد و بازهٔ هوشمند همراهی‌ات می‌کند.",
  hint="با جست‌وجوی دودویی هر عدد در حداکثر ۷ تلاش پیدا می‌شود!",
  logic="""
var WOG_LOGIC = {
  LO: 1, HI: 100,
  newGame: function (rng) { rng = rng || Math.random; var secret = 1 + Math.floor(rng() * 100); return { secret: secret, count: 0, done: false, lastD: 0, hist: [] }; },
  guess: function (st, n) {
    n = Math.floor(Number(n));
    if (!(n >= 1 && n <= 100)) throw new Error('out-of-range');
    if (st.done) throw new Error('game-over');
    st.count++; st.lastD = n - st.secret; st.hist.push(n);
    if (n === st.secret) st.done = true;
    return { cmp: n < st.secret ? -1 : (n > st.secret ? 1 : 0), done: st.done, count: st.count };
  },
  temp: function (d) { var a = Math.abs(d); return a === 0 ? 'درست!' : a <= 3 ? 'داغ' : a <= 10 ? 'گرم' : a <= 25 ? 'ولرم' : 'سرد'; },
  par: function () { return 7; }
};
""",
  tests=[
    ("binary search finds every secret in <=7 guesses", """
      var worst=0;
      for(var s=1;s<=100;s++){var st=L.newGame(rng);st.secret=s;var lo=1,hi=100;
        while(!st.done){var mid=Math.floor((lo+hi)/2);var r=L.guess(st,mid);if(r.cmp<0)lo=mid+1;else if(r.cmp>0)hi=mid-1;}
        if(st.count>worst)worst=st.count;}
      T.ok(worst<=7,'worst='+worst);
    """),
    ("out of range and post-done throw", """
      var st=L.newGame(rng); T.throws(function(){L.guess(st,0)}); T.throws(function(){L.guess(st,101)});
      L.guess(st,50); if(!st.done){L.guess(st,st.secret);}
      T.throws(function(){L.guess(st,1)});
    """),
    ("count increments and cmp direction correct", """
      var st=L.newGame(rng);st.secret=70;var r1=L.guess(st,30);T.eq(r1.cmp,-1);T.eq(r1.count,1);
      var r2=L.guess(st,90);T.eq(r2.cmp,1);T.eq(r2.count,2);
    """),
  ],
  ui="""
var st = L.newGame();
function draw() {
  hud('تلاش‌ها: <b>' + fa(st.count) + '</b> — بازه: <b>' + fa(lo) + ' تا ' + fa(hi) + '</b>');
  app.innerHTML = '';
  var p = ce('div', 'wpanel'); p.style.width = 'min(92vw,420px)'; p.style.textAlign = 'center';
  p.appendChild(ce('p', null, 'عدد مخفی بین <b style="color:#e8c073">۱</b> تا <b style="color:#e8c073">۱۰۰</b> است'));
  var inp = ce('input'); inp.type = 'number'; inp.min = 1; inp.max = 100;
  inp.style.cssText = 'font-family:inherit;font-size:1.3rem;width:120px;text-align:center;background:#0d1526;color:#f3ead8;border:1px solid rgba(217,164,65,.4);border-radius:10px;padding:8px;margin:10px';
  var btn = ce('button', null, 'حدس بزن'); btn.setAttribute('data-smoke', '');
  var msg = ce('p'); msg.style.minHeight = '1.5em'; msg.style.marginTop = '8px';
  btn.addEventListener('click', try1);
  inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') try1(); });
  p.appendChild(inp); p.appendChild(ce('br')); p.appendChild(btn); p.appendChild(msg);
  app.appendChild(p);
  function try1() {
    var v = parseInt(inp.value, 10);
    try { var r = L.guess(st, v); } catch (e) { toast('عدد بین ۱ تا ۱۰۰ بگو'); return; }
    if (r.done) {
      draw();
      ovl('آفرین!', 'عدد <b style="color:#e8c073">' + fa(st.secret) + '</b> بود — در ' + fa(st.count) + ' تلاش' +
        (st.count <= L.par() ? ' (عالی، بهتر از حد معیار!)' : ''), 'بازی جدید', function () { st = L.newGame(); lo = 1; hi = 100; draw(); });
    } else {
      if (r.cmp < 0) { lo = Math.max(lo, v + 1); msg.textContent = 'برو بالاتر ↑ (' + L.temp(st.lastD) + ')'; }
      else { hi = Math.min(hi, v - 1); msg.textContent = 'بیا پایین‌تر ↓ (' + L.temp(st.lastD) + ')'; }
      draw();
    }
  }
}
var app = $('#app'), lo = 1, hi = 100;
draw();
$('#hint').textContent = 'هر عدد ۱ تا ۱۰۰ در حداکثر ۷ تلاش با جست‌وجوی دودویی پیدا می‌شود.';
"""),

# ============================================================ coin-flip
G(slug="coin-flip", title="سکه طلایی", cat="luck", icon="🪙", g1="#8a6d1f", g2="#e8c073",
  desc="روی یا خط؟ زنجیره‌ی بردهای پشت‌سرهم بساز و رکورد بزن.",
  hint="احتمال روی و خط ۵۰-۵۰ است؛ زنجیره بلندتر = امتیاز بیشتر.",
  logic="""
var WOG_LOGIC = {
  flip: function (rng) { rng = rng || Math.random; return rng() < 0.5 ? 'r' : 'k'; },
  judge: function (call, side) { return call === side ? 1 : 0; },
  longest: function (hist, side) { var b = 0, c = 0; for (var i = 0; i < hist.length; i++) { if (hist[i].res === side) { c++; if (c > b) b = c; } else c = 0; } return b; },
  streakPts: function (n) { return n * (n + 1) / 2; },
  headsRate: function (hist) { if (!hist.length) return 0; var h = 0; hist.forEach(function (x) { if (x.res === 'r') h++; }); return h / hist.length; }
};
""",
  tests=[
    ("flip returns r/k only", """
      for(var i=0;i<500;i++){var f=L.flip(rng);T.ok(f==='r'||f==='k',f);}
    """),
    ("heads rate within sane bounds over 3000 flips", """
      var h=[];for(var i=0;i<3000;i++)h.push({res:L.flip(rng)});
      var rate=L.headsRate(h);T.ok(rate>0.44&&rate<0.56,'rate='+rate);
    """),
    ("longest streak calc", """
      var h=[{res:'r'},{res:'r'},{res:'k'},{res:'r'},{res:'r'},{res:'r'},{res:'k'}];
      T.eq(L.longest(h,'r'),3);T.eq(L.longest(h,'k'),1);T.eq(L.longest([],'r'),0);
    """),
    ("judge and streak points", """
      T.eq(L.judge('r','r'),1);T.eq(L.judge('r','k'),0);T.eq(L.streakPts(4),10);T.eq(L.streakPts(0),0);
    """),
  ],
  ui="""
var hist = [], wins = 0, cur = 0, best = storeBest('wog-coin-best');
function draw() {
  hud('بردها: <b>' + fa(wins) + '</b> — زنجیره: <b>' + fa(cur) + '</b> — رکورد: <b>' + fa(best) + '</b>');
}
function pick(call) {
  var side = L.flip();
  var ok = L.judge(call, side) === 1;
  hist.push({ res: side });
  if (ok) { cur++; wins++; best = bestOf('wog-coin-best', cur); toast('درست حدس زدی! زنجیره ' + fa(cur)); }
  else { cur = 0; toast('اشتباه شد — زنجیره صفر'); }
  var face = side === 'r' ? 'روی' : 'خط';
  $('#res').textContent = 'سکه: ' + face;
  draw();
}
var app = $('#app');
var p = ce('div', 'wpanel'); p.style.width = 'min(92vw,420px)'; p.style.textAlign = 'center';
var coin = ce('div', null, '؟'); coin.style.cssText = 'width:110px;height:110px;line-height:110px;margin:10px auto;border-radius:50%;background:radial-gradient(circle at 35% 30%,#f5d98b,#c98f2b);color:#221806;font-size:1.6rem;font-weight:900';
var res = ce('p'); res.id = 'res'; res.style.minHeight = '1.5em';
var r1 = ce('button', null, 'روی'); r1.setAttribute('data-smoke', '');
var r2 = ce('button', 'sec', 'خط');
r1.addEventListener('click', function () { pick('r') });
r2.addEventListener('click', function () { pick('k') });
var row = ce('div', 'wrow'); row.appendChild(r1); row.appendChild(r2);
p.appendChild(coin); p.appendChild(res); p.appendChild(row);
app.appendChild(p);
draw();
$('#hint').textContent = 'زنجیره برد = مجموع ۱+۲+۳+… ؛ رکوردت ذخیره می‌شود.';
"""),

# ============================================================ lotto
G(slug="lotto", title="لوتو ۶ از ۴۹", cat="luck", icon="🎟", g1="#0f4c5c", g2="#3fb8af",
  desc="شانست را امتحان کن: ۶ عدد را انتخاب کن و با قرعه رسمی مقایسه کن.",
  hint="قرعه‌کشی با ۶ عدد یکتای ۱ تا ۴۹ انجام می‌شود.",
  logic="""
var WOG_LOGIC = {
  draw: function (rng) {
    rng = rng || Math.random; var pool = [], out = [];
    for (var i = 1; i <= 49; i++) pool.push(i);
    for (var j = 0; j < 6; j++) { var k = Math.floor(rng() * pool.length); out.push(pool.splice(k, 1)[0]); }
    return out.sort(function (a, b) { return a - b; });
  },
  matches: function (ticket, drawn) { var s = {}; drawn.forEach(function (x) { s[x] = 1 }); return ticket.filter(function (x) { return s[x]; }).length; },
  prize: function (m) { return m === 6 ? 'جایزه بزرگ!' : m === 5 ? 'خیلی خوب!' : m === 4 ? 'خوب' : m === 3 ? 'کوچک' : 'برنده نشدی'; },
  odds: function () { var c = 1; for (var i = 0; i < 6; i++) c = c * (49 - i) / (i + 1); return Math.round(c); }
};
""",
  tests=[
    ("draw: 6 unique sorted numbers 1..49", """
      for(var t=0;t<300;t++){var d=L.draw(rng);T.eq(d.length,6);var s={};d.forEach(function(x){T.ok(x>=1&&x<=49);s[x]=1});T.eq(Object.keys(s).length,6);
      for(var i=1;i<6;i++)T.ok(d[i-1]<d[i],'sorted');}
    """),
    ("matches counting", """
      T.eq(L.matches([1,2,3,4,5,6],[1,2,3,40,41,42]),3);
      T.eq(L.matches([1,2],[3,4,5,6,7,8]),0);T.eq(L.matches([7],[1,2,3,4,5,7]),1);
    """),
    ("prize tiers", """
      T.ok(L.prize(6).indexOf('جایزه')>=0);
      T.ok(L.prize(2).length>0);T.ok(L.prize(0).length>0);
    """),
    ("odds magnitude (13,983,816)", """
      T.eq(L.odds(),13983816);
    """),
  ],
  ui="""
var ticket = [];
var drawn = null;
function drawUI() {
  hud('انتخاب: <b>' + fa(ticket.length) + '/۶</b>' + (drawn ? ' — تطابق: <b>' + fa(L.matches(ticket, drawn)) + '</b>' : ''));
  var app = $('#app'); app.innerHTML = '';
  var p = ce('div', 'wpanel'); p.style.width = 'min(94vw,520px)';
  var grid = ce('div'); grid.style.cssText = 'display:grid;grid-template-columns:repeat(7,1fr);gap:5px;direction:ltr';
  for (var n = 1; n <= 49; n++) {
    (function (n) {
      var b = ce('button', 'sec', fa(n)); b.style.cssText = 'padding:7px 2px;font-size:.85rem;min-width:0';
      if (ticket.indexOf(n) >= 0) { b.style.background = '#d9a441'; b.style.color = '#221806'; }
      if (drawn && drawn.indexOf(n) >= 0) { b.style.borderColor = '#3fb8af'; b.style.color = '#3fb8af'; }
      b.addEventListener('click', function () {
        if (drawn) return;
        var i = ticket.indexOf(n);
        if (i >= 0) ticket.splice(i, 1); else if (ticket.length < 6) ticket.push(n); else toast('حداکثر ۶ عدد');
        drawUI();
      });
      grid.appendChild(b);
    })(n);
  }
  p.appendChild(grid);
  var row = ce('div', 'wrow');
  var go = ce('button', null, 'قرعه‌کشی!'); go.setAttribute('data-smoke', '');
  var rnd = ce('button', 'sec', 'انتخاب تصادفی');
  var clr = ce('button', 'sec', 'پاک کردن');
  go.addEventListener('click', function () {
    if (drawn) { drawn = null; ticket = []; drawUI(); return; }
    if (ticket.length !== 6) { toast('دقیقاً ۶ عدد انتخاب کن'); return; }
    drawn = L.draw();
    var m = L.matches(ticket, drawn);
    ovl('قرعه: ' + drawn.map(fa).join(' ، '), 'تطابق: ' + fa(m) + ' — ' + L.prize(m), 'دور بعد', function () { drawn = null; ticket = []; drawUI(); });
    drawUI();
  });
  rnd.addEventListener('click', function () { if (drawn) return; ticket = L.draw(); drawUI(); });
  clr.addEventListener('click', function () { if (drawn) return; ticket = []; drawUI(); });
  row.appendChild(go); row.appendChild(rnd); row.appendChild(clr);
  p.appendChild(row); app.appendChild(p);
}
drawUI();
$('#hint').textContent = 'این بازی صرفاً سرگرمی با امتیاز فرضی است و هیچ پول واقعی در میان نیست.';
"""),

# ============================================================ plinko
G(slug="plinko", title="سنگ‌ریزه", cat="luck", icon="🎯", g1="#1f5c3f", g2="#67b98a",
  desc="سنگ‌ریزه را بین میخ‌ها رها کن و جوایز خانه‌های پایین را بگیر.",
  hint="مسیر هر سنگ‌ریزه مجموع ۱۲ انتخاب چپ/راست است؛ خانه‌های وسط شانس بیشتری دارند.",
  engines=("common", "arcade"),
  logic="""
var ROWS = 12;
var PAYOUT = [8, 3, 1.6, 1, 0.7, 0.5, 0.3, 0.5, 0.7, 1, 1.6, 3, 8];
var WOG_LOGIC = {
  rows: function () { return ROWS; },
  payoutTable: function () { return PAYOUT.slice(); },
  drop: function (rng) { rng = rng || Math.random; var pos = 0; for (var i = 0; i < ROWS; i++) pos += rng() < 0.5 ? 0 : 1; return pos; },
  payout: function (slot, bet) { return Math.round(bet * PAYOUT[slot]); },
  ev: function (bet) { var c = 1, s = 0; for (var k = 0; k <= ROWS; k++) { if (k > 0) c = c * (ROWS - k + 1) / k; s += c * PAYOUT[k]; } return s / Math.pow(2, ROWS) * bet; }
};
""",
  tests=[
    ("drop lands in 0..ROWS", """
      for(var i=0;i<2000;i++){var s=L.drop(rng);T.ok(s>=0&&s<=12,'s='+s);}
    """),
    ("binomial mean near center", """
      var sum=0,N=4000;for(var i=0;i<N;i++)sum+=L.drop(rng);
      var mean=sum/N;T.near(mean,6,0.25,'mean='+mean);
    """),
    ("payout mapping", """
      var t=L.payoutTable();T.eq(t.length,13);T.eq(t[0],8);T.eq(t[6],0.3);T.eq(t[12],8);
      T.eq(L.payout(0,100),800);T.eq(L.payout(6,100),30);
    """),
    ("expected value < bet", """
      T.ok(L.ev(100)<100,'ev='+L.ev(100));T.ok(L.ev(100)>50);
    """),
  ],
  ui="""
var app = $('#app');
var W = 360, H = 470, ROWS = L.rows(), slots = L.payoutTable().length;
var g = makeCanvas(W, H), ctx = g.ctx;
var balls = [], credits = 100, bet = 10;
var colors = ['#d9a441', '#3fb8af', '#e8c073', '#67b98a', '#e26d5c'];
function layout() {
  var top = 26, gap = (H - top - 46) / ROWS, pw = W / (slots + 1);
  return { top: top, gap: gap, pw: pw };
}
function render() {
  var plg=ctx.createLinearGradient(0,0,0,H);plg.addColorStop(0,'#1c1430');plg.addColorStop(1,'#241636');ctx.fillStyle=plg;ctx.fillRect(0,0,W,H);
  var ly = layout();
  ctx.fillStyle = '#8fa1c7';
  for (var r = 0; r < ROWS; r++) for (var c = 0; c <= r; c++) {
    var x = W / 2 + (c - r / 2) * ly.pw, y = ly.top + (r + .6) * ly.gap;
    ctx.beginPath(); ctx.arc(x, y, 2.6, 0, 7); ctx.fill();
  }
  var sw = W / slots;
  for (var s = 0; s < slots; s++) {
    ctx.fillStyle = 'rgba(217,164,65,' + (0.25 + 0.5 * (1 - Math.abs(s - (slots - 1) / 2) / (slots / 2))) + ')';
    ctx.fillRect(s * sw, H - 40, sw - 2, 30);
    ctx.fillStyle = 'rgba(255,225,160,.9)'; ctx.font = 'bold 11px Vazirmatn,Tahoma'; ctx.textAlign = 'center';
    ctx.fillText(slots[s] + '×', s * sw + sw / 2 - 1, H - 21);
  }
  balls.forEach(function (b) {
    ctx.beginPath(); ctx.arc(b.x, b.y, 6, 0, 7);
    ctx.fillStyle = b.color; ctx.fill();
  });
}
rafStep(function (dt) {
  balls.forEach(function (b) {
    b.t += dt * 7.5;
    var r = Math.floor(b.t);
    if (r < ROWS) { b.row = r; b.x = W / 2 + (b.pos - b.row / 2) * layout().pw; b.y = layout().top + (b.row + .6) * layout().gap; }
    else { b.row = ROWS; b.y += 340 * dt; b.x = (b.slot + .5) * (W / slots); }
  });
  for (var i = balls.length - 1; i >= 0; i--) if (balls[i].y > H - 44) {
    var b = balls.splice(i, 1)[0];
    credits += L.payout(b.slot, b.bet);
    toast('+' + fa(L.payout(b.slot, b.bet)) + ' امتیاز');
    drawHud();
  }
  render();
});
function launch() {
  if (credits < bet) { toast('امتیاز کافی نداری'); return; }
  credits -= bet;
  var pos = L.drop();
  balls.push({ t: 0, pos: pos, slot: pos, x: W / 2, y: layout().top - 10, bet: bet, color: pick(colors) });
}
function drawHud() { hud('اعتبار: <b>' + fa(credits) + '</b> — شرط: <b>' + fa(bet) + '</b>'); }
var bar = ce('div', 'wrow');
var minus = ce('button', 'sec', '−'); var plus = ce('button', 'sec', '+'); var go = ce('button', null, 'رها کن!');
go.setAttribute('data-smoke', '');
minus.addEventListener('click', function () { bet = Math.max(5, bet - 5); drawHud() });
plus.addEventListener('click', function () { bet = Math.min(50, bet + 5); drawHud() });
go.addEventListener('click', launch);
bar.appendChild(minus); bar.appendChild(go); bar.appendChild(plus);
$('#app').appendChild(bar);
drawHud();
$('#hint').textContent = 'این بازی فقط با امتیاز سرگرمی است؛ خانه‌های کناری جایزه بزرگ‌تر ولی شانس کمتر دارند.';
"""),
]
