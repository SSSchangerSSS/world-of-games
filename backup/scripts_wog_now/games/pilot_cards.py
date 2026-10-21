# -*- coding: utf-8 -*-
"""Pilot (adapted): pyramid + golf card games — cards are {s,r} objects per lib contract."""
from lib import G

# ---------------------------------------------------------------- pyramid ----

PYRAMID_LOGIC = r"""
var WOG_LOGIC = {
  buildGame: function (rng) {
    var d = shuffle(makeDeck(), rng), py = [], i = 0, r, c;
    for (r = 0; r < 7; r++) { var row = []; for (c = 0; c <= r; c++) row.push(d[i++]); py.push(row); }
    return { pyramid: py, stock: d.slice(28), waste: [], removed: 0 };
  },
  isExposed: function (st, pos) {
    if (!pos || pos.w) return false;
    var py = st.pyramid, r = pos.r, c = pos.c;
    if (!py[r] || py[r][c] == null) return false;
    if (py[r + 1]) { if (py[r + 1][c] != null) return false; if (py[r + 1][c + 1] != null) return false; }
    return true;
  },
  getCard: function (st, pos) {
    if (pos && pos.w) return st.waste.length ? st.waste[st.waste.length - 1] : null;
    var row = pos ? st.pyramid[pos.r] : null;
    return row ? row[pos.c] : null;
  },
  canRemove: function (a, b) {
    if (!a) return false;
    if (!b) return a.r === 13;
    return a.r + b.r === 13;
  },
  removePair: function (st, p1, p2) {
    if (!p1) return false;
    if (p2 && p1.w && p2.w) return false;
    if (!p1.w && !this.isExposed(st, p1)) return false;
    if (p2 && !p2.w && !this.isExposed(st, p2)) return false;
    var c1 = this.getCard(st, p1);
    if (c1 == null) return false;
    var c2 = p2 ? this.getCard(st, p2) : null;
    if (p2 && c2 == null) return false;
    if (!this.canRemove(c1, c2)) return false;
    if (p1.w) st.waste.pop(); else st.pyramid[p1.r][p1.c] = null;
    if (p2) { if (p2.w) st.waste.pop(); else st.pyramid[p2.r][p2.c] = null; }
    st.removed += p2 ? 2 : 1;
    return true;
  },
  drawStock: function (st) {
    if (!st.stock.length) return false;
    st.waste.push(st.stock.pop());
    return true;
  },
  hasMoves: function (st) {
    if (st.stock.length) return true;
    var wtop = st.waste.length ? st.waste[st.waste.length - 1] : null, r, c, r2, c2, cd, cd2;
    for (r = 0; r < 7; r++) for (c = 0; c <= r; c++) {
      cd = st.pyramid[r][c];
      if (cd == null || !this.isExposed(st, { r: r, c: c })) continue;
      if (cd.r === 13) return true;
      if (wtop != null && cd.r + wtop.r === 13) return true;
      for (r2 = r; r2 < 7; r2++) for (c2 = (r2 === r ? c + 1 : 0); c2 <= r2; c2++) {
        cd2 = st.pyramid[r2][c2];
        if (cd2 != null && this.isExposed(st, { r: r2, c: c2 }) && cd.r + cd2.r === 13) return true;
      }
    }
    return false;
  },
  isWin: function (st) {
    for (var r = 0; r < 7; r++) for (var c = 0; c <= r; c++) if (st.pyramid[r][c] != null) return false;
    return true;
  }
};
"""

PYRAMID_UI = r"""
var PS = null, sel = null, PW = storeBest('wog-pyramid-wins');
function pCount() { var n = 0, r, c; for (r = 0; r < 7; r++) for (c = 0; c <= r; c++) if (PS.pyramid[r][c] != null) n++; return n; }
function pNew() { PS = L.buildGame(); sel = null; pRender(); }
function pRender() {
  hud('کارت‌های هرم: <b>' + fa(pCount()) + '</b> — بردها: <b>' + fa(PW) + '</b>');
  var app = $('#app'); app.innerHTML = '';
  var py = ce('div', 'pyr'), r, c;
  for (r = 0; r < 7; r++) {
    var row = ce('div', 'pyr-row');
    for (c = 0; c <= r; c++) {
      (function (rr, cc) {
        var card = PS.pyramid[rr][cc];
        if (card == null) { row.appendChild(ce('div', 'pyr-slot')); return; }
        var el = cardEl(card, true, 'small');
        el.classList.add(L.isExposed(PS, { r: rr, c: cc }) ? 'exposed' : 'covered');
        if (sel && !sel.w && sel.r === rr && sel.c === cc) el.classList.add('sel');
        el.addEventListener('click', function () { pTap({ r: rr, c: cc }); });
        row.appendChild(el);
      })(r, c);
    }
    py.appendChild(row);
  }
  app.appendChild(py);
  var bar = ce('div', 'pyr-bar');
  var sb = ce('button', null, 'پشت کار (' + fa(PS.stock.length) + ')');
  sb.setAttribute('data-smoke', '');
  sb.addEventListener('click', pDraw);
  bar.appendChild(sb);
  var wtop = L.getCard(PS, { w: 1 });
  var wwrap = ce('div', 'waste-col');
  var wEl = wtop ? cardEl(wtop, true, 'small') : ce('div', 'wcard small back');
  if (wtop) {
    wEl.classList.add('exposed');
    if (sel && sel.w) wEl.classList.add('sel');
    wEl.addEventListener('click', function () { pTap({ w: 1 }); });
  }
  wwrap.appendChild(wEl);
  wwrap.appendChild(ce('div', 'slot-lbl', 'زباله'));
  bar.appendChild(wwrap);
  var rb = ce('button', 'sec', 'شروع دوباره');
  rb.setAttribute('data-smoke', '');
  rb.addEventListener('click', pNew);
  bar.appendChild(rb);
  app.appendChild(bar);
}
function pTap(pos) {
  var card = L.getCard(PS, pos);
  if (card == null) return;
  if (!pos.w && !L.isExposed(PS, pos)) { toast('این کارت هنوز پوشیده است'); return; }
  if (sel) {
    var same = pos.w ? !!sel.w : (sel.r === pos.r && sel.c === pos.c);
    if (same) { sel = null; pRender(); return; }
    if (L.removePair(PS, sel, pos)) { sel = null; pRender(); pEnd(); return; }
    sel = null;
  }
  if (L.canRemove(card)) { L.removePair(PS, pos, null); pRender(); pEnd(); return; }
  sel = pos; pRender();
}
function pDraw() {
  if (!PS.stock.length) { toast('پشت کار خالی است'); return; }
  L.drawStock(PS); pRender(); pEnd();
}
function pEnd() {
  if (L.isWin(PS)) {
    PW++; store.set('wog-pyramid-wins', String(PW));
    ovl('آفرین! هرم فرو ریخت', 'هر ۲۸ کارت پاک شد.', 'بازی جدید', pNew);
    return;
  }
  if (!L.hasMoves(PS)) {
    ovl('حرکتی نماند', 'نه جفت ۱۳‌ای روی صفحه است و نه کارتی در پشت کار', 'بازی جدید', pNew);
  }
}
pNew();
$('#hint').textContent = 'دو کارت باز که جمعشان ۱۳ می‌شود را بردار؛ شاه را تنها بزن. پشت کار فقط یک بار مرور می‌شود.';
"""

PYRAMID_CSS = r"""
.pyr{display:flex;flex-direction:column;align-items:center;gap:5px;margin:6px auto 10px}
.pyr-row{display:flex;gap:5px}
.pyr-slot{width:34px;height:48px;border:1px dashed rgba(255,255,255,.25);border-radius:6px}
.wcard.exposed{cursor:pointer}
.wcard.covered{opacity:.55}
.pyr-bar{display:flex;align-items:center;justify-content:center;gap:16px;margin:8px 0}
.waste-col{display:flex;flex-direction:column;align-items:center;gap:3px}
.slot-lbl{font-size:11px;color:#a8b3c9}
"""

# ------------------------------------------------------------------- golf ----

GOLF_LOGIC = r"""
var WOG_LOGIC = {
  buildGame: function (rng) {
    var d = shuffle(makeDeck(), rng), cols = [], i = 0, c, r;
    for (c = 0; c < 5; c++) { var col = []; for (r = 0; r < 7; r++) col.push(d[i++]); cols.push(col); }
    var waste = [d[i++]];
    return { cols: cols, stock: d.slice(i), waste: waste, played: 0 };
  },
  canPlay: function (card, wasteTop) {
    if (card == null || wasteTop == null) return false;
    var a = card.r, b = wasteTop.r;
    return (a - b + 13) % 13 === 1 || (b - a + 13) % 13 === 1;
  },
  play: function (st, col) {
    var c = st.cols[col];
    if (!c || !c.length) return false;
    var bottom = c[c.length - 1], top = st.waste[st.waste.length - 1];
    if (!this.canPlay(bottom, top)) return false;
    st.waste.push(c.pop());
    st.played++;
    return true;
  },
  flipStock: function (st) {
    if (!st.stock.length) return false;
    st.waste.push(st.stock.pop());
    return true;
  },
  hasMoves: function (st) {
    if (st.stock.length) return true;
    var top = st.waste.length ? st.waste[st.waste.length - 1] : null;
    for (var i = 0; i < 5; i++) { var c = st.cols[i]; if (c.length && this.canPlay(c[c.length - 1], top)) return true; }
    return false;
  },
  isWin: function (st) {
    for (var i = 0; i < 5; i++) if (st.cols[i].length) return false;
    return true;
  }
};
"""

GOLF_UI = r"""
var GS = null, GW = storeBest('wog-golf-wins');
function gNew() { GS = L.buildGame(); gRender(); }
function gRender() {
  hud('کارت‌های مانده: <b>' + fa(35 - GS.played) + '</b> — بردها: <b>' + fa(GW) + '</b>');
  var app = $('#app'); app.innerHTML = '';
  var cols = ce('div', 'golf-cols');
  var top = GS.waste[GS.waste.length - 1];
  for (var c = 0; c < 5; c++) {
    (function (cc) {
      var colEl = ce('div', 'golf-col'), arr = GS.cols[cc];
      if (!arr.length) { colEl.appendChild(ce('div', 'golf-empty')); cols.appendChild(colEl); return; }
      for (var i = 0; i < arr.length - 1; i++) colEl.appendChild(cardEl(arr[i], true, 'tiny'));
      var b = cardEl(arr[arr.length - 1], true, 'small');
      b.classList.add('golf-bottom');
      if (L.canPlay(arr[arr.length - 1], top)) b.classList.add('playable');
      b.addEventListener('click', function () { gTap(cc); });
      cols.appendChild(colEl);
    })(c);
  }
  app.appendChild(cols);
  var bar = ce('div', 'pyr-bar');
  var sb = ce('button', null, 'پشت کار (' + fa(GS.stock.length) + ')');
  sb.setAttribute('data-smoke', '');
  sb.addEventListener('click', gFlip);
  bar.appendChild(sb);
  var wwrap = ce('div', 'waste-col');
  wwrap.appendChild(top ? cardEl(top, true, 'small') : ce('div', 'wcard small back'));
  wwrap.appendChild(ce('div', 'slot-lbl', 'زباله'));
  bar.appendChild(wwrap);
  var rb = ce('button', 'sec', 'شروع دوباره');
  rb.setAttribute('data-smoke', '');
  rb.addEventListener('click', gNew);
  bar.appendChild(rb);
  app.appendChild(bar);
}
function gTap(c) {
  if (!GS.cols[c].length) return;
  if (!L.play(GS, c)) { toast('این کارت قابل بازی نیست'); return; }
  gRender(); gEnd();
}
function gFlip() {
  if (!GS.stock.length) { toast('پشت کار خالی است'); return; }
  L.flipStock(GS); gRender(); gEnd();
}
function gEnd() {
  if (L.isWin(GS)) {
    GW++; store.set('wog-golf-wins', String(GW));
    ovl('آفرین! برنده شدی', 'هر ۳۵ کارت بازی شد.', 'بازی جدید', gNew);
    return;
  }
  if (!L.hasMoves(GS)) {
    ovl('باختی', 'هیچ ستونی قابل بازی نیست و پشت کار هم خالی است', 'بازی جدید', gNew);
  }
}
gNew();
$('#hint').textContent = 'کارت پایین هر ستون را با اختلاف یک رتبه (شاه به آس وصل است) روی زباله بگذار.';
"""

GOLF_CSS = r"""
.golf-cols{display:flex;justify-content:center;gap:8px;margin:8px 0}
.golf-col{display:flex;flex-direction:column;align-items:center;min-width:34px}
.golf-col .wcard.tiny{margin-top:-24px}
.golf-col .wcard.tiny:first-child{margin-top:0}
.golf-col .wcard.golf-bottom{margin-top:-18px}
.golf-empty{width:34px;height:48px;border:1px dashed rgba(255,255,255,.25);border-radius:6px}
.wcard.playable{outline:2px solid #67b98a;cursor:pointer}
"""

# ------------------------------------------------------------------ tests ----

PYRAMID_TESTS = [
    ("shah-alone", r"""
var K={s:0,r:13},Q={s:0,r:12},st={pyramid:[[K]],stock:[],waste:[],removed:0};
T.ok(L.canRemove(K),'K alone allowed');
T.ok(!L.canRemove(Q),'Q alone rejected');
T.ok(L.removePair(st,{r:0,c:0},null),'K removed alone');
T.eq(st.pyramid[0][0],null,'slot empty');
T.eq(st.removed,1,'removed count 1');
"""),
    ("pair-8-5", r"""
function C(s,r){return{s:s,r:r}}
T.ok(L.canRemove(C(0,8),C(1,5)),'8+5 accepted');
T.ok(!L.canRemove(C(0,8),C(1,4)),'8+4 rejected');
T.ok(!L.canRemove(C(0,13),C(0,1)),'K+A rejected (K goes alone)');
var st={pyramid:[[C(0,8),C(1,5)]],stock:[],waste:[],removed:0};
T.ok(L.removePair(st,{r:0,c:0},{r:0,c:1}),'pair removed');
T.eq(st.pyramid[0][0],null,'first null');
T.eq(st.removed,2,'removed count 2');
"""),
    ("exposure-gate", r"""
function C(s,r){return{s:s,r:r}}
var st={pyramid:[[C(0,8),C(1,2)],[C(2,13),C(3,4),C(0,9)]],stock:[],waste:[C(1,5)],removed:0};
T.ok(!L.isExposed(st,{r:0,c:0}),'covered by two children');
T.ok(L.isExposed(st,{r:1,c:2}),'bottom row always exposed');
T.eq(L.removePair(st,{r:0,c:0},{w:1}),false,'covered card rejected despite 8+5');
T.ok(L.removePair(st,{r:1,c:0},null),'K alone clears first cover');
T.ok(!L.isExposed(st,{r:0,c:0}),'still covered by remaining child');
T.ok(L.removePair(st,{r:1,c:1},{r:1,c:2}),'4+9 cleared');
T.ok(L.isExposed(st,{r:0,c:0}),'now exposed');
T.ok(L.removePair(st,{r:0,c:0},{w:1}),'8+5 with waste works');
T.eq(st.removed,5,'removed count 5');
"""),
    ("draw-stock", r"""
var st=L.buildGame(rng);
T.eq(st.stock.length,24,'24 cards in stock');
T.eq(st.waste.length,0,'waste starts empty');
var top=st.stock[st.stock.length-1];
T.ok(L.drawStock(st),'draw ok');
T.eq(st.waste[st.waste.length-1],top,'stock top moved to waste');
T.eq(st.stock.length,23,'stock shrank');
T.ok(!L.drawStock({pyramid:[[{s:0,r:1}]],stock:[],waste:[],removed:0}),'empty stock rejected');
"""),
    ("build-shape", r"""
var st=L.buildGame(rng);
T.eq(st.pyramid.length,7,'7 rows');
var n=0,r,c;
for(r=0;r<7;r++){T.eq(st.pyramid[r].length,r+1,'row length');n+=st.pyramid[r].length;}
T.eq(n,28,'28 pyramid cards');
T.eq(st.stock.length,24,'24 stock cards');
var seen={},dup=0,all=[];
for(r=0;r<7;r++)for(c=0;c<=r;c++)all.push(st.pyramid[r][c]);
all=all.concat(st.stock);
for(var j=0;j<all.length;j++){var k=all[j].s*13+all[j].r;if(seen[k])dup++;seen[k]=1;}
T.eq(dup,0,'no duplicate cards');
"""),
    ("seeded-playout-accounting", r"""
var st=L.buildGame(rng);
function pc(s){var n=0,r,c;for(r=0;r<7;r++)for(c=0;c<=r;c++)if(s.pyramid[r][c]!=null)n++;return n;}
function acc(s){return pc(s)+s.stock.length+s.waste.length+(s.removed||0);}
T.eq(acc(st),52,'start accounting');
var guard=0,moves=0;
while(guard++<200){
  T.eq(acc(st),52,'accounting step '+guard);
  if(L.isWin(st))break;
  if(!L.hasMoves(st))break;
  var moved=false,w=L.getCard(st,{w:1});
  for(var r=0;r<7&&!moved;r++)for(var c=0;c<=r&&!moved;c++){
    var cd=st.pyramid[r][c];
    if(cd==null||!L.isExposed(st,{r:r,c:c}))continue;
    if(L.canRemove(cd)){L.removePair(st,{r:r,c:c},null);moved=true;moves++;break;}
    if(w!=null&&L.canRemove(cd,w)){L.removePair(st,{r:r,c:c},{w:1});moved=true;moves++;break;}
    for(var r2=r;r2<7&&!moved;r2++)for(var c2=(r2===r?c+1:0);c2<=r2;c2++){
      var cd2=st.pyramid[r2][c2];
      if(cd2!=null&&L.isExposed(st,{r:r2,c:c2})&&L.canRemove(cd,cd2)){
        L.removePair(st,{r:r,c:c},{r:r2,c:c2});moved=true;moves++;break;
      }
    }
  }
  if(!moved){T.ok(L.drawStock(st),'draw stock');moves++;}
}
T.eq(acc(st),52,'end accounting');
T.ok(moves>0,'playout did something');
"""),
]

GOLF_TESTS = [
    ("wrap-adjacency", r"""
function C(s,r){return{s:s,r:r}}
T.ok(L.canPlay(C(0,13),C(1,1)),'K over A wraps');
T.ok(L.canPlay(C(1,1),C(0,13)),'A over K wraps');
T.ok(L.canPlay(C(2,2),C(0,1)),'2 over A');
T.ok(L.canPlay(C(0,1),C(2,2)),'A over 2');
T.ok(L.canPlay(C(0,12),C(0,13)),'Q over K normal');
T.ok(!L.canPlay(C(0,12),C(0,1)),'Q over A rejected');
T.ok(!L.canPlay(C(1,7),C(2,9)),'gap of 2 rejected');
T.ok(!L.canPlay(C(1,7),C(2,7)),'same rank rejected');
T.ok(!L.canPlay(C(0,5),null),'null waste rejected');
"""),
    ("bottom-only-rule", r"""
function C(s,r){return{s:s,r:r}}
var st={cols:[[C(0,9),C(0,6),C(0,7)],[C(1,2),C(1,9),C(2,3)],[C(0,1)],[C(2,13)],[C(1,4)]],stock:[],waste:[C(0,8)],played:47};
T.ok(L.canPlay(st.cols[0][0],st.waste[0]),'non-bottom 9 would fit but rule is bottom-only');
T.ok(L.play(st,0),'bottom played');
T.eq(st.waste[st.waste.length-1],C(0,7),'bottom 7 moved to waste');
T.eq(st.cols[0].length,2,'column shrank to 2');
T.eq(st.played,48,'played counter incremented');
T.eq(L.play(st,1),false,'3 vs 8 not playable');
T.eq(L.play(st,2),false,'empty col2 rejected');
"""),
    ("build-shape", r"""
var st=L.buildGame(rng);
T.eq(st.cols.length,5,'5 columns');
T.eq(st.waste.length,1,'one waste card');
T.eq(st.stock.length,16,'16 stock cards');
var all=[],i;
for(i=0;i<5;i++){T.eq(st.cols[i].length,7,'col has 7');all=all.concat(st.cols[i]);}
all=all.concat(st.stock).concat(st.waste);
T.eq(all.length,52,'52 cards dealt');
var seen={},dup=0;
for(var j=0;j<all.length;j++){var k=all[j].s*13+all[j].r;if(seen[k])dup++;seen[k]=1;}
T.eq(dup,0,'no duplicates');
"""),
    ("seeded-playout-accounting", r"""
var st=L.buildGame(rng);
function colSum(s){var n=0,i;for(i=0;i<5;i++)n+=s.cols[i].length;return n;}
function acc(s){return colSum(s)+s.stock.length+s.waste.length;}
T.eq(acc(st),52,'start accounting');
var guard=0,moves=0;
while(guard++<200){
  T.eq(acc(st),52,'accounting step '+guard);
  T.eq(st.played,35-colSum(st),'counter step '+guard);
  if(L.isWin(st))break;
  if(!L.hasMoves(st))break;
  var moved=false;
  for(var i=0;i<5;i++){
    if(st.cols[i].length&&L.canPlay(st.cols[i][st.cols[i].length-1],st.waste[st.waste.length-1])){
      T.ok(L.play(st,i),'played col '+i);moved=true;moves++;break;
    }
  }
  if(!moved){T.ok(L.flipStock(st),'flip stock');moves++;}
}
T.eq(acc(st),52,'end accounting');
T.ok(moves>0,'playout did something');
"""),
    ("win-loss-detection", r"""
function C(s,r){return{s:s,r:r}}
var w={cols:[[],[],[],[],[]],stock:[],waste:[C(0,2),C(0,3)],played:50};
T.ok(L.isWin(w),'win when all columns empty');
var l={cols:[[C(0,7)],[C(1,9)],[C(2,2)],[C(3,13)],[C(1,4)]],stock:[],waste:[C(0,7)],played:47};
T.ok(!L.isWin(l),'not win with cards left');
T.eq(L.hasMoves(l),false,'stuck detected');
"""),
]

GAMES = [
    G(slug="pyramid", title="هرم", cat="cards", icon="🔺", g1="#134e5e", g2="#71b280",
      desc="سولیتر هرم: ۲۸ کارت به شکل هرم چیده شده‌اند؛ هر بار دو کارتِ باز که جمعشان ۱۳ می‌شود را بردار و کل هرم را فرو بریز.",
      hint="شاه (۱۳) را تنها می‌شود برداشت. با دکمه پشت کار کارت جدید بکش؛ فقط یک بار مرور می‌شود.",
      engines=("common", "card"), logic=PYRAMID_LOGIC, ui=PYRAMID_UI, css=PYRAMID_CSS, tests=PYRAMID_TESTS),
    G(slug="golf", title="گلف", cat="cards", icon="⛳", g1="#1a2980", g2="#26d0ce",
      desc="سولیتر گلف: ۵ ستون ۷ کارتی؛ کارت‌های پایین ستون‌ها را با اختلاف یک رتبه روی زباله بگذار و هر ۳۵ کارت را تمام کن.",
      hint="شاه به آس وصل است. اول ستون‌ها را امتحان کن؛ پشت کار فقط یک بار برگردانده می‌شود.",
      engines=("common", "card"), logic=GOLF_LOGIC, ui=GOLF_UI, css=GOLF_CSS, tests=GOLF_TESTS),
]
