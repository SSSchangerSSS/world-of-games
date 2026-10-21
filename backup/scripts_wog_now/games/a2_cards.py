# -*- coding: utf-8 -*-
"""AG-A2 batch: two Persian solitaire engines (spider 1-suit + freecell) as mini browser card games."""
from lib_mini import G

SPIDER_LOGIC = r"""
function sh(a,rng){var r=rng||Math.random,i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(r()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
function snap(st){st.hist.push(JSON.stringify({p:st.piles,k:st.stock,r:st.removed,m:st.moves}));if(st.hist.length>300)st.hist.shift();}
function undo(st){var h=st.hist.pop();if(!h)return false;var o=JSON.parse(h);st.piles=o.p;st.stock=o.k;st.removed=o.r;st.moves=o.m;return true;}
function newGame(rng){var cards=[],id=0,c,r,i,p,n;for(c=0;c<8;c++)for(r=1;r<=13;r++)cards.push({s:0,r:r,id:id++});sh(cards,rng);var piles=[],k=0;for(p=0;p<10;p++){piles.push([]);n=p<4?6:5;for(i=0;i<n;i++)piles[p].push(cards[k++]);}return{piles:piles,stock:cards.slice(k),removed:0,moves:0,hist:[]};}
function movableRun(pile,fromIdx){var i;if(!pile||fromIdx<0||fromIdx>=pile.length)return null;for(i=fromIdx;i<pile.length-1;i++){if(pile[i].r!==pile[i+1].r+1)return null;}return pile.slice(fromIdx);}
function canDrop(run,top){if(!run||!run.length)return false;if(!top)return true;return top.r===run[0].r+1;}
function checkCompleted(st){var n=0,p,pl,ok,i;for(p=0;p<10;p++){pl=st.piles[p];if(pl.length<13)continue;ok=true;for(i=0;i<13;i++){if(pl[pl.length-1-i].r!==i+1){ok=false;break;}}if(ok){pl.length-=13;st.removed++;n++;}}return n;}
function applyMove(st,from,fromIdx,to){if(from===to)return false;var pl=st.piles[from],run=movableRun(pl,fromIdx),dst,i;if(!run)return false;dst=st.piles[to];if(!canDrop(run,dst[dst.length-1]))return false;snap(st);pl.length=fromIdx;for(i=0;i<run.length;i++)dst.push(run[i]);st.moves++;checkCompleted(st);return true;}
function dealRow(st){var p;if(st.stock.length<10)return false;for(p=0;p<10;p++){if(!st.piles[p].length)return false;}snap(st);for(p=0;p<10;p++)st.piles[p].push(st.stock.pop());st.moves++;checkCompleted(st);return true;}
function hasAnyMove(st){var a,i,b,pl,d;for(a=0;a<10;a++){pl=st.piles[a];if(!pl.length)continue;for(i=pl.length-1;i>=0;i--){for(b=0;b<10;b++){if(b===a)continue;d=st.piles[b];if(!d.length||d[d.length-1].r===pl[i].r+1)return true;}if(i>0&&pl[i-1].r!==pl[i].r+1)break;}}return false;}
function isWin(st){return st.removed>=8;}
function isStuck(st){return !hasAnyMove(st)&&st.stock.length===0;}
var WOG_LOGIC={newGame:newGame,movableRun:movableRun,canDrop:canDrop,applyMove:applyMove,dealRow:dealRow,checkCompleted:checkCompleted,isWin:isWin,hasAnyMove:hasAnyMove,isStuck:isStuck,undo:undo,snap:snap};
"""

SPIDER_UI = r"""
var st=null,sel=null;
function rk(r){return r===1?'A':(r===11?'J':(r===12?'Q':(r===13?'K':fa(r))));}
function start(){st=L.newGame();sel=null;$('#hint').textContent='اول روی کارت مبدأ بزن و بعد روی مقصد؛ ردیف نزولی بساز و ۸ ردیف کامل K تا A را جمع کن.';render();}
function isSel(p,i){return !!sel&&sel.p===p&&i>=sel.i;}
function render(){
 var app=$('#app');app.innerHTML='';
 var bar=ce('div','bar','');
 var bd=ce('button','bt','پخش ('+fa(st.stock.length/10)+')');
 bd.setAttribute('data-smoke','deal');bd.onclick=function(){doDeal();};
 var bu=ce('button','bt','برگرد');
 bu.setAttribute('data-smoke','undo');bu.onclick=function(){if(L.undo(st)){sel=null;render();}else{toast('چیزی برای برگشت نیست');}};
 var bn=ce('button','bt','بازی جدید');
 bn.setAttribute('data-smoke','new');bn.onclick=function(){start();};
 var bh=ce('button','bt','راهنما');
 bh.onclick=function(){ovl('راهنما','کارت هر ستون باید روی کارتی با یک رتبه بیشتر بنشیند و هر ردیف نزولی پیوسته یکجا جابه‌جا می‌شود. ستونی که از K تا A پیوسته باشد پس از هر حرکت خودکار حذف می‌شود. دکمه پخش به هر ۱۰ ستون یک کارت اضافه می‌کند، اما اگر ستون خالی داشته باشی اجازه پخش نیست. با حذف ۸ ردیف برنده می‌شوی.','فهمیدم',function(){});};
 bar.appendChild(bd);bar.appendChild(bu);bar.appendChild(bn);bar.appendChild(bh);
 app.appendChild(bar);
 var row=ce('div','tabs','');
 for(var p=0;p<10;p++){
  var col=ce('div','col','');
  col.setAttribute('data-pile',p);
  col.onclick=(function(q){return function(){tap(q,-1);};})(p);
  var pl=st.piles[p];
  for(var i=0;i<pl.length;i++){
   var d=ce('div','cd'+(isSel(p,i)?' sel':''),'<b>'+rk(pl[i].r)+'</b><i>♠</i>');
   d.setAttribute('data-card',p+'-'+i);
   d.onclick=(function(q,j){return function(ev){ev.stopPropagation();tap(q,j);};})(p,i);
   col.appendChild(d);
  }
  row.appendChild(col);
 }
 app.appendChild(row);
 hud('حرکت: '+fa(st.moves)+' — دسته: '+fa(st.stock.length/10)+' — ردیف کامل: '+fa(st.removed)+' از ۸');
}
function tap(p,i){
 if(sel&&sel.p!==p){
  var ok=L.applyMove(st,sel.p,sel.i,p);
  if(ok){sel=null;after();return;}
  sel=null;
  if(i>=0&&L.movableRun(st.piles[p],i))sel={p:p,i:i};
  render();return;
 }
 if(sel&&sel.p===p&&i===sel.i){sel=null;render();return;}
 if(i>=0&&L.movableRun(st.piles[p],i)){sel={p:p,i:i};render();return;}
 if(sel){sel=null;render();}
}
function doDeal(){
 sel=null;
 if(!L.dealRow(st)){toast(st.stock.length?'هر ستون باید حداقل یک کارت داشته باشد':'دسته خالی است');render();return;}
 after();
}
function after(){
 render();
 if(L.isWin(st)){ovl('آفرین! بردی','هر ۸ ردیف کامل شد','بازی جدید',function(){start();});return;}
 if(L.isStuck(st)){ovl('بازی تمام شد','حرکت و پخش ممکن نیست','بازی جدید',function(){start();});}
}
start();
"""

SPIDER_CSS = r"""
body{margin:0;background:#123d16;color:#fff;font-family:Tahoma,Arial,sans-serif}
header{text-align:center;padding:4px}
h1{margin:2px 0;font-size:17px}
#hud{font-size:13px;color:#dcedc8}
.wog-home{display:inline-block;color:#fff;text-decoration:none;font-size:12px;opacity:.7;margin:3px}
.bar{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;padding:5px}
.bt{background:#ffffff22;border:1px solid #ffffff55;color:#fff;border-radius:8px;padding:6px 12px;font-family:inherit;font-size:13px;cursor:pointer}
#app{padding:2px 4px}
.tabs{display:flex;gap:3px;justify-content:center;align-items:flex-start}
.col{flex:1 1 0;min-width:30px;max-width:50px;min-height:70px}
.cd{position:relative;width:100%;height:60px;background:#fcfcf4;border:1px solid #444;border-radius:6px;color:#111;font-size:14px;cursor:pointer;box-sizing:border-box}
.col .cd+.cd{margin-top:-45px}
.cd b{position:absolute;top:2px;right:4px}
.cd i{position:absolute;bottom:1px;left:4px;font-style:normal}
.cd.sel{outline:3px solid #ffca28;background:#fff59d}
#hint{text-align:center;font-size:12px;color:#ffe0b2;margin:8px 4px}
#wog-toast{position:fixed;bottom:10px;left:0;right:0;text-align:center;font-size:13px;color:#fff;pointer-events:none;text-shadow:0 1px 2px #000}
"""

SPIDER_TESTS = [
("initial deal counts", r"""
var s=L.newGame(rng),tot=0,ids={},i,j,cnt=0;
for(i=0;i<10;i++){T.eq(s.piles[i].length,i<4?6:5,'pile len '+i);tot+=s.piles[i].length;
 for(j=0;j<s.piles[i].length;j++){var c=s.piles[i][j];T.ok(ids[c.id]===undefined,'dup id');ids[c.id]=1;T.eq(c.s,0,'all spades');T.ok(c.r>=1&&c.r<=13,'rank range');}}
T.eq(tot,54,'tableau 54');T.eq(s.stock.length,50,'stock 50');
for(j=0;j<s.stock.length;j++){var c2=s.stock[j];T.ok(ids[c2.id]===undefined,'dup id stock');ids[c2.id]=1;}
for(var k in ids)cnt++;
T.eq(cnt,104,'104 unique ids');T.eq(s.removed,0,'removed 0');T.eq(s.moves,0,'moves 0');
"""),
("run move legality and undo", r"""
var s=L.newGame(rng);
s.piles[0]=[{s:0,r:9,id:0},{s:0,r:8,id:1},{s:0,r:7,id:2}];
T.eq(L.movableRun(s.piles[0],0).length,3,'run of 3');
T.eq(L.movableRun(s.piles[0],2).length,1,'run of 1');
T.ok(!L.movableRun(s.piles[0],3),'idx out of range');
T.ok(!L.movableRun(s.piles[0],-1),'negative idx');
s.piles[1]=[{s:0,r:9,id:3},{s:0,r:7,id:4},{s:0,r:6,id:5}];
T.ok(!L.movableRun(s.piles[1],0),'gap rejected');
T.ok(L.movableRun(s.piles[1],1),'tail valid');
T.ok(L.canDrop([{s:0,r:6,id:9}],{s:0,r:7,id:10}),'drop on +1');
T.ok(!L.canDrop([{s:0,r:6,id:9}],{s:0,r:6,id:10}),'drop on equal');
T.ok(!L.canDrop([{s:0,r:6,id:9}],{s:0,r:5,id:10}),'drop on lower');
T.ok(L.canDrop([{s:0,r:6,id:9}],null),'drop on empty');
s.piles[2]=[{s:0,r:8,id:6}];
T.ok(L.applyMove(s,1,1,2),'move 7-6 onto 8');
T.eq(s.piles[2].length,3,'dest 3');T.eq(s.piles[1].length,1,'src 1');T.eq(s.moves,1,'move counted');
T.ok(!L.applyMove(s,2,0,2),'same pile rejected');
s.piles[3]=[{s:0,r:12,id:7}];
T.ok(!L.applyMove(s,2,1,3),'7-6 onto Q rejected');
T.ok(L.undo(s),'undo');T.eq(s.piles[1].length,3,'src restored');T.eq(s.piles[2].length,1,'dest restored');T.eq(s.moves,0,'moves restored');
T.ok(!L.undo(s),'history empty');
"""),
("deal blocked by empty pile", r"""
var s=L.newGame(rng);
s.piles[4]=[];
T.ok(!L.dealRow(s),'deal blocked');
T.eq(s.stock.length,50,'stock intact');T.eq(s.moves,0,'moves intact');
s.piles[4]=[{s:0,r:3,id:99}];
T.ok(L.dealRow(s),'deal ok');T.eq(s.stock.length,40,'stock 40');T.eq(s.moves,1,'deal counted');
var i;for(i=0;i<10;i++)T.ok(s.piles[i].length>0,'pile '+i+' received');
"""),
("completed run auto removal", r"""
var s=L.newGame(rng),p=[],r;
for(r=13;r>=1;r--)p.push({s:0,r:r,id:r});
s.piles[0]=p;
s.piles[1]=[{s:0,r:13,id:20},{s:0,r:12,id:21},{s:0,r:11,id:22}];
T.ok(!L.isWin(s),'not won');
T.eq(L.checkCompleted(s),1,'one removed');
T.eq(s.piles[0].length,0,'pile emptied');T.eq(s.removed,1,'counter 1');
T.eq(L.checkCompleted(s),0,'partial kept');T.eq(s.piles[1].length,3,'partial intact');
s.removed=8;T.ok(L.isWin(s),'win at 8');
"""),
("stock exhaustion", r"""
var s=L.newGame(rng),n=0;
while(L.dealRow(s))n++;
T.eq(n,5,'five deals');T.eq(s.stock.length,0,'stock empty');T.ok(!L.dealRow(s),'sixth rejected');
"""),
("bot playout conservation", r"""
var s=L.newGame(rng),steps=0;
function tot(){var t=s.stock.length,i;for(i=0;i<10;i++)t+=s.piles[i].length;return t+s.removed*13;}
function fm(){var a,i,b,pl,d,g=null;
 for(a=0;a<10;a++){pl=s.piles[a];if(!pl.length)continue;
  for(i=pl.length-1;i>=0;i--){
   for(b=0;b<10;b++){if(b===a)continue;d=s.piles[b];
    if(!d.length){if(!g)g=[a,i,b];}else if(d[d.length-1].r===pl[i].r+1)return[a,i,b];}
   if(i>0&&pl[i-1].r!==pl[i].r+1)break;}}
 return g;}
T.eq(tot(),104,'initial 104');
while(steps<2500){steps++;var m=fm();
 if(m){T.ok(L.applyMove(s,m[0],m[1],m[2]),'legal move at '+steps);T.eq(tot(),104,'conserved at '+steps);continue;}
 if(L.dealRow(s)){T.eq(tot(),104,'conserved deal at '+steps);continue;}
 break;}
T.ok(steps>10,'bot progressed: '+steps);T.eq(tot(),104,'final 104');
"""),
]

FREE_LOGIC = r"""
function sh(a,rng){var r=rng||Math.random,i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(r()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
function isRed(c){return c.s===1||c.s===2;}
function snap(st){st.hist.push(JSON.stringify({c:st.cas,e:st.cells,f:st.found,m:st.moves}));if(st.hist.length>300)st.hist.shift();}
function undo(st){var h=st.hist.pop();if(!h)return false;var o=JSON.parse(h);st.cas=o.c;st.cells=o.e;st.found=o.f;st.moves=o.m;return true;}
function newGame(rng){var cards=[],s,r,id=0,i,j,k=0,n;for(s=0;s<4;s++)for(r=1;r<=13;r++)cards.push({s:s,r:r,id:id++});sh(cards,rng);var cas=[];for(i=0;i<8;i++){cas.push([]);n=i<4?7:6;for(j=0;j<n;j++)cas[i].push(cards[k++]);}return{cas:cas,cells:[null,null,null,null],found:[[],[],[],[]],moves:0,hist:[]};}
function freeCells(st){var n=0,i;for(i=0;i<4;i++)if(!st.cells[i])n++;return n;}
function emptyCas(st){var n=0,i;for(i=0;i<8;i++)if(!st.cas[i].length)n++;return n;}
function maxRun(st,dest){var f=freeCells(st),e=emptyCas(st);if(dest!==null&&dest!==undefined&&!st.cas[dest].length)e--;return(1+f)*(1+e);}
function canDropCascade(run,top){if(!run||!run.length)return false;if(!top)return true;return top.r===run[0].r+1&&isRed(top)!==isRed(run[0]);}
function canFound(card,found){var f=found[card.s];if(!f.length)return card.r===1;return f[f.length-1].r===card.r-1;}
function validRun(a){var i;if(!a||!a.length)return false;for(i=0;i<a.length-1;i++){if(a[i].r!==a[i+1].r+1||isRed(a[i])===isRed(a[i+1]))return false;}return true;}
function applyMove(st,from,to){var run,i,c;
 if(!from||!to)return false;
 if(from.type==='cascade'){var pl=st.cas[from.idx],len=from.runLen||1;
  if(from.idx<0||from.idx>7||len<1||len>pl.length)return false;
  run=pl.slice(pl.length-len);
  if(!validRun(run))return false;
  if(to.type!=='cascade'&&len>1)return false;
  if(len>maxRun(st,to.type==='cascade'?to.idx:null))return false;
 }else if(from.type==='free'){
  if(to.type==='free')return false;
  c=st.cells[from.idx];if(!c)return false;run=[c];
 }else{return false;}
 if(to.type==='cascade'){
  if(from.type==='cascade'&&from.idx===to.idx)return false;
  if(to.idx<0||to.idx>7)return false;
  var d=st.cas[to.idx];
  if(!canDropCascade(run,d[d.length-1]))return false;
  if(from.type==='cascade')st.cas[from.idx].length-=run.length;else st.cells[from.idx]=null;
  for(i=0;i<run.length;i++)d.push(run[i]);
 }else if(to.type==='free'){
  var slot=-1;for(i=0;i<4;i++)if(!st.cells[i]){slot=i;break;}
  if(slot<0)return false;
  st.cas[from.idx].length-=1;st.cells[slot]=run[0];
 }else if(to.type==='foundation'){
  c=run[0];
  if(!canFound(c,st.found))return false;
  if(from.type==='cascade')st.cas[from.idx].length-=1;else st.cells[from.idx]=null;
  st.found[c.s].push(c);
 }else{return false;}
 st.moves++;
 return true;}
function autoFound(st){var n=0,again=true,i,c,t;
 while(again){again=false;
  for(i=0;i<4;i++){c=st.cells[i];if(c&&(c.r===1||c.r===2)&&canFound(c,st.found)){st.cells[i]=null;st.found[c.s].push(c);st.moves++;n++;again=true;}}
  for(i=0;i<8;i++){t=st.cas[i][st.cas[i].length-1];if(t&&(t.r===1||t.r===2)&&canFound(t,st.found)){st.cas[i].length-=1;st.found[t.s].push(t);st.moves++;n++;again=true;}}
 }
 return n;}
function founded(st){var n=0,i;for(i=0;i<4;i++)n+=st.found[i].length;return n;}
function isWin(st){return founded(st)===52;}
function hasAnyMove(st){var i,b,a,pl,d,c;
 for(i=0;i<4;i++){c=st.cells[i];if(!c)continue;
  if(canFound(c,st.found))return true;
  for(b=0;b<8;b++){d=st.cas[b];if(d.length&&canDropCascade([c],d[d.length-1]))return true;}}
 for(a=0;a<8;a++){pl=st.cas[a];if(!pl.length)continue;
  var k=1;while(k<pl.length){var x=pl[pl.length-1-k],y=pl[pl.length-k];if(x.r===y.r+1&&isRed(x)!==isRed(y))k++;else break;}
  var mr=maxRun(st,null),cap=k<mr?k:mr;
  for(var len=1;len<=cap;len++){var card=pl[pl.length-len];
   if(len===1){if(canFound(card,st.found))return true;if(freeCells(st)>0)return true;}
   for(b=0;b<8;b++){if(b===a)continue;var d2=st.cas[b];
    if(len<=maxRun(st,b)&&(!d2.length||canDropCascade(pl.slice(pl.length-len),d2[d2.length-1])))return true;}}
 }
 return false;}
var WOG_LOGIC={newGame:newGame,maxRun:maxRun,canDropCascade:canDropCascade,canFound:canFound,validRun:validRun,applyMove:applyMove,autoFound:autoFound,founded:founded,isWin:isWin,hasAnyMove:hasAnyMove,isRed:isRed,undo:undo,snap:snap};
"""

FREE_UI = r"""
var st=null,sel=null;
var SUI=['♠','♥','♦','♣'];
function rk(r){return r===1?'A':(r===11?'J':(r===12?'Q':(r===13?'K':fa(r))));}
function freeN(){var n=0,i;for(i=0;i<4;i++)if(!st.cells[i])n++;return n;}
function start(){st=L.newGame();sel=null;$('#hint').textContent='روی کارت بزن تا انتخاب شود، بعد روی مقصد. ستون‌ها نزولی و با رنگ یک‌درمیان چیده می‌شوند و آ و ۲ خودکار به بنیاد می‌روند.';render();}
function tryMove(from,to){
 L.snap(st);
 if(!L.applyMove(st,from,to)){st.hist.pop();toast('حرکت مجاز نیست');return false;}
 L.autoFound(st);sel=null;after();return true;
}
function render(){
 var app=$('#app');app.innerHTML='';
 var bar=ce('div','bar','');
 var bd=ce('button','bt','بازی جدید');
 bd.setAttribute('data-smoke','deal');bd.onclick=function(){start();};
 var bu=ce('button','bt','برگرد');
 bu.setAttribute('data-smoke','undo');bu.onclick=function(){if(L.undo(st)){sel=null;render();}else{toast('چیزی برای برگشت نیست');}};
 var bh=ce('button','bt','راهنما');
 bh.onclick=function(){ovl('راهنما','در ستون‌ها هر کارت روی کارتی یک رتبه بیشتر با رنگ مخالف می‌نشیند. یک ردیف مرتب را یکجا می‌توان جابه‌جا کرد؛ بیشینه طول آن برابر است با (خانه‌های خالی + ۱) ضرب‌در (ستون‌های خالی + ۱) و ستون مقصد اگر خالی باشد در شمارش نمی‌آید. هر خانه آزاد فقط یک کارت می‌گیرد. کارت مجاز از ستون یا خانه به بنیاد هم‌خال خودش می‌رود و آ و ۲ خودکار می‌روند. با بنیاد کردن ۵۲ کارت برنده شو.','فهمیدم',function(){});};
 bar.appendChild(bd);bar.appendChild(bu);bar.appendChild(bh);
 app.appendChild(bar);
 var top=ce('div','top','');
 for(var i=0;i<4;i++){
  (function(j){
   var c=st.cells[j];
   var cls='slot'+(c?' cd '+(L.isRed(c)?'red':''):'')+((sel&&sel.type==='free'&&sel.idx===j)?' sel':'');
   var s=ce('div',cls,c?'<b>'+rk(c.r)+'</b><i>'+SUI[c.s]+'</i>':'<span class="gh">خانه</span>');
   s.setAttribute('data-cell',j);
   s.onclick=function(){tapCell(j);};
   top.appendChild(s);
  })(i);
 }
 for(i=0;i<4;i++){
  (function(j){
   var fl=st.found[j];
   var cls='slot fnd'+(fl.length?' cd '+((j===1||j===2)?'red':''):'');
   var s=ce('div',cls,fl.length?'<b>'+rk(fl[fl.length-1].r)+'</b><i>'+SUI[j]+'</i>':'<span class="gh">'+SUI[j]+'</span>');
   s.setAttribute('data-found',j);
   s.onclick=function(){tapFound(j);};
   top.appendChild(s);
  })(i);
 }
 app.appendChild(top);
 var row=ce('div','tabs','');
 for(var p=0;p<8;p++){
  var col=ce('div','col','');
  col.setAttribute('data-cas',p);
  col.onclick=(function(q){return function(){tapCas(q,-1);};})(p);
  var pl=st.cas[p];
  var cut=(sel&&sel.type==='cascade'&&sel.idx===p)?pl.length-sel.runLen:-1;
  for(i=0;i<pl.length;i++){
   var c2=pl[i];
   var d=ce('div','cd '+(L.isRed(c2)?'red':'')+((sel&&sel.type==='cascade'&&sel.idx===p&&i>=cut)?' sel':''),'<b>'+rk(c2.r)+'</b><i>'+SUI[c2.s]+'</i>');
   d.setAttribute('data-card',p+'-'+i);
   d.onclick=(function(q,j){return function(ev){ev.stopPropagation();tapCas(q,j);};})(p,i);
   col.appendChild(d);
  }
  row.appendChild(col);
 }
 app.appendChild(row);
 hud('حرکت: '+fa(st.moves)+' — خانه آزاد: '+fa(freeN())+' — بنیاد: '+fa(L.founded(st))+' از ۵۲');
}
function tapCas(p,i){
 var pl=st.cas[p];
 if(sel){
  if(sel.type==='cascade'&&sel.idx===p){sel=null;render();return;}
  if(tryMove(sel,{type:'cascade',idx:p}))return;
  sel=null;
 }
 if(i>=0){
  var run=pl.slice(i);
  if(L.validRun(run)){sel={type:'cascade',idx:p,runLen:pl.length-i};render();return;}
  toast('این ردیف یکپارچه قابل جابه‌جایی نیست');
 }
 render();
}
function tapCell(j){
 if(sel){
  if(sel.type==='free'&&sel.idx===j){sel=null;render();return;}
  if(tryMove(sel,{type:'free',idx:j}))return;
  sel=null;render();return;
 }
 if(st.cells[j]){sel={type:'free',idx:j,runLen:1};render();}
}
function tapFound(j){
 if(sel)tryMove(sel,{type:'foundation',idx:j});
}
function after(){
 render();
 if(L.isWin(st)){ovl('آفرین! بردی','هر ۵۲ کارت روی بنیاد رفت','بازی جدید',function(){start();});return;}
 if(!L.hasAnyMove(st)){ovl('بازی تمام شد','حرکت مجازی باقی نماند','بازی جدید',function(){start();});}
}
start();
"""

FREE_CSS = r"""
body{margin:0;background:#0d2b4e;color:#fff;font-family:Tahoma,Arial,sans-serif}
header{text-align:center;padding:4px}
h1{margin:2px 0;font-size:17px}
#hud{font-size:13px;color:#bbdefb}
.wog-home{display:inline-block;color:#fff;text-decoration:none;font-size:12px;opacity:.7;margin:3px}
.bar{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;padding:5px}
.bt{background:#ffffff22;border:1px solid #ffffff55;color:#fff;border-radius:8px;padding:6px 12px;font-family:inherit;font-size:13px;cursor:pointer}
#app{padding:2px 4px}
.top{display:flex;gap:6px;justify-content:center;margin:6px 0;flex-wrap:wrap}
.slot{position:relative;width:44px;height:60px;border:2px dashed #ffffff66;border-radius:6px;box-sizing:border-box;cursor:pointer;font-size:14px;color:#111;background:#fcfcf4}
.slot .gh{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#888;font-size:12px}
.slot.fnd{border:2px solid #ffd54f88;background:#ffffff18}
.slot.fnd .gh{color:#ffffff99}
.red{color:#c62828}
.tabs{display:flex;gap:3px;justify-content:center;align-items:flex-start}
.col{flex:1 1 0;min-width:34px;max-width:50px;min-height:70px}
.cd{position:relative;width:100%;height:60px;background:#fcfcf4;border:1px solid #444;border-radius:6px;color:#111;font-size:14px;cursor:pointer;box-sizing:border-box}
.col .cd+.cd{margin-top:-44px}
.cd b{position:absolute;top:2px;right:4px}
.cd i{position:absolute;bottom:1px;left:4px;font-style:normal}
.cd.sel,.slot.sel{outline:3px solid #ffca28;background:#fff59d}
#hint{text-align:center;font-size:12px;color:#ffe0b2;margin:8px 4px}
#wog-toast{position:fixed;bottom:10px;left:0;right:0;text-align:center;font-size:13px;color:#fff;pointer-events:none;text-shadow:0 1px 2px #000}
"""

FREE_TESTS = [
("deal counts", r"""
var s=L.newGame(rng),tot=0,ids={},i,j,cnt=0;
for(i=0;i<8;i++){T.eq(s.cas[i].length,i<4?7:6,'cas len '+i);tot+=s.cas[i].length;
 for(j=0;j<s.cas[i].length;j++){var c=s.cas[i][j];T.ok(ids[c.id]===undefined,'dup id');ids[c.id]=1;T.ok(c.s>=0&&c.s<=3,'suit range');T.ok(c.r>=1&&c.r<=13,'rank range');}}
T.eq(tot,52,'52 dealt');
for(var k in ids)cnt++;
T.eq(cnt,52,'unique ids');
for(i=0;i<4;i++){T.eq(s.cells[i],null,'cell empty');T.eq(s.found[i].length,0,'found empty');}
"""),
("alternating run legality", r"""
T.ok(L.canDropCascade([{s:1,r:5,id:1}],{s:0,r:6,id:2}),'red on black');
T.ok(L.canDropCascade([{s:0,r:5,id:1}],{s:2,r:6,id:2}),'black on red');
T.ok(!L.canDropCascade([{s:1,r:5,id:1}],{s:2,r:6,id:2}),'red on red rejected');
T.ok(!L.canDropCascade([{s:0,r:5,id:1}],{s:3,r:6,id:2}),'black on black rejected');
T.ok(!L.canDropCascade([{s:0,r:5,id:1}],{s:0,r:6,id:2}),'same suit rejected');
T.ok(!L.canDropCascade([{s:0,r:5,id:1}],{s:0,r:5,id:2}),'equal rank rejected');
T.ok(L.canDropCascade([{s:3,r:2,id:1}],null),'empty dest ok');
var s=L.newGame(rng);
s.cas[0]=[{s:0,r:6,id:1},{s:1,r:5,id:2}];
s.cas[1]=[{s:2,r:7,id:9}];
T.ok(L.applyMove(s,{type:'cascade',idx:0,runLen:2},{type:'cascade',idx:1}),'run of 2 moved');
T.eq(s.cas[0].length,0,'src empty');T.eq(s.cas[1].length,3,'dest 3');T.eq(s.moves,1,'move counted');
s.cas[2]=[{s:1,r:9,id:3},{s:2,r:8,id:4}];
T.ok(!L.applyMove(s,{type:'cascade',idx:2,runLen:2},{type:'cascade',idx:0}),'non alternating rejected');
s.cas[3]=[{s:0,r:12,id:31},{s:1,r:11,id:32},{s:0,r:10,id:33},{s:1,r:9,id:34},{s:0,r:8,id:35},{s:1,r:7,id:36}];
T.ok(!L.applyMove(s,{type:'cascade',idx:3,runLen:6},{type:'cascade',idx:0}),'run 6 over cap');
T.ok(L.applyMove(s,{type:'cascade',idx:3,runLen:5},{type:'cascade',idx:0}),'run 5 onto empty ok');
T.ok(!L.applyMove(s,{type:'cascade',idx:1,runLen:1},{type:'cascade',idx:1}),'same pile rejected');
"""),
("maxRun formula", r"""
var s=L.newGame(rng);
T.eq(L.maxRun(s,null),5,'4 free 0 empty = 5');
s.cells[0]={s:0,r:2,id:100};s.cells[1]={s:0,r:3,id:101};
T.eq(L.maxRun(s,null),3,'2 free 0 empty = 3');
s.cas[1]=[];
T.eq(L.maxRun(s,null),6,'2 free 1 empty = 6');
T.eq(L.maxRun(s,1),3,'dest empty excluded = 3');
s.cas[2]=[];
T.eq(L.maxRun(s,null),9,'2 free 2 empty = 9');
s.cells[0]=null;s.cells[1]=null;
T.eq(L.maxRun(s,null),15,'4 free 2 empty = 15');
"""),
("foundation and free cells", r"""
var s=L.newGame(rng);
T.ok(L.canFound({s:0,r:1,id:1},s.found),'ace to empty');
T.ok(!L.canFound({s:0,r:5,id:2},s.found),'non ace to empty');
s.found[0]=[{s:0,r:1,id:3}];
T.ok(L.canFound({s:0,r:2,id:4},s.found),'2 on ace');
T.ok(!L.canFound({s:0,r:3,id:5},s.found),'gap rejected');
T.ok(!L.canFound({s:1,r:2,id:6},s.found),'wrong suit rejected');
s.cas[0]=[{s:2,r:1,id:7}];
T.ok(L.applyMove(s,{type:'cascade',idx:0,runLen:1},{type:'foundation',idx:2}),'ace founded');
T.eq(s.found[2].length,1,'founded len');
s.cells[1]={s:2,r:2,id:8};
T.ok(L.applyMove(s,{type:'free',idx:1,runLen:1},{type:'foundation',idx:2}),'2 from cell founded');
T.eq(s.cells[1],null,'cell freed');T.eq(s.found[2].length,2,'foundation grew');
s.cas[4]=[{s:0,r:3,id:9},{s:1,r:2,id:10}];
T.ok(!L.applyMove(s,{type:'cascade',idx:4,runLen:2},{type:'foundation',idx:0}),'multi to foundation rejected');
s.cells[0]={s:2,r:8,id:11};
s.cas[5]=[{s:0,r:9,id:12}];
T.ok(L.applyMove(s,{type:'free',idx:0,runLen:1},{type:'cascade',idx:5}),'cell to cascade');
T.eq(s.cas[5].length,2,'cascade grew');T.eq(s.cells[0],null,'cell emptied');
s.cas[6]=[{s:3,r:4,id:13}];
T.ok(L.applyMove(s,{type:'cascade',idx:6,runLen:1},{type:'free',idx:2}),'cascade to cell');
T.ok(!!s.cells[0],'cell filled');
s.cas[6]=[{s:3,r:4,id:14},{s:2,r:3,id:15}];
T.ok(!L.applyMove(s,{type:'cascade',idx:6,runLen:2},{type:'free',idx:3}),'multi to cell rejected');
"""),
("undo snapshot", r"""
var s=L.newGame(rng);
L.snap(s);
var before=s.cas[7].length;
s.cas[7]=[];
T.ok(L.undo(s),'undo ok');
T.eq(s.cas[7].length,before,'restored');
T.ok(!L.undo(s),'no more history');
"""),
("safe autoplay", r"""
var s=L.newGame(rng),q;
for(q=0;q<8;q++)s.cas[q]=[];
s.cas[0]=[{s:0,r:1,id:1}];
s.cas[1]=[{s:1,r:1,id:2},{s:0,r:2,id:3}];
s.cas[2]=[{s:2,r:3,id:4}];
s.cells[2]={s:3,r:1,id:5};
var n=L.autoFound(s);
T.eq(n,4,'four auto moves');
T.eq(s.found[0].length,2,'spade A and 2');
T.eq(s.found[1].length,1,'heart ace');
T.eq(s.found[2].length,0,'three not auto');
T.eq(s.found[3].length,1,'club ace');
T.eq(s.cas[0].length,0,'cas0 emptied');
T.eq(s.cas[1].length,0,'cas1 emptied');
T.eq(s.cells[2],null,'cell emptied');
T.eq(L.autoFound(s),0,'no more autos');
"""),
("win detection and dead position", r"""
var s=L.newGame(rng);
T.ok(!L.isWin(s),'not won');
var id=0,sa,r;
for(sa=0;sa<4;sa++)for(r=1;r<=13;r++)s.found[sa].push({s:sa,r:r,id:id++});
T.ok(L.isWin(s),'won at 52');
var d=L.newGame(rng),i;
for(i=0;i<8;i++)d.cas[i]=[{s:1,r:2+i,id:i}];
for(i=0;i<4;i++)d.cells[i]={s:1,r:10+i,id:20+i};
T.ok(!L.hasAnyMove(d),'dead position detected');
var f=L.newGame(rng);
T.ok(L.hasAnyMove(f),'fresh game has moves');
"""),
("bot playout conservation", r"""
var s=L.newGame(rng),steps=0;
function tot(){var t=0,i;for(i=0;i<8;i++)t+=s.cas[i].length;for(i=0;i<4;i++){if(s.cells[i])t++;t+=s.found[i].length;}return t;}
function bm(){var i,b,f,pl,k,x,y,mr,cap,len,card,d2;
 for(i=0;i<4;i++){var c=s.cells[i];if(!c)continue;
  if(L.canFound(c,s.found))return{from:{type:'free',idx:i,runLen:1},to:{type:'foundation',idx:c.s}};
  for(b=0;b<8;b++){d2=s.cas[b];if(d2.length&&L.canDropCascade([c],d2[d2.length-1]))return{from:{type:'free',idx:i,runLen:1},to:{type:'cascade',idx:b}};}}
 for(var a=0;a<8;a++){pl=s.cas[a];if(!pl.length)continue;
  k=1;
  while(k<pl.length){x=pl[pl.length-1-k];y=pl[pl.length-k];if(x.r===y.r+1&&L.isRed(x)!==L.isRed(y))k++;else break;}
  mr=L.maxRun(s,null);cap=k<mr?k:mr;
  for(len=1;len<=cap;len++){card=pl[pl.length-len];
   if(len===1&&L.canFound(card,s.found))return{from:{type:'cascade',idx:a,runLen:1},to:{type:'foundation',idx:card.s}};
   for(b=0;b<8;b++){if(b===a)continue;d2=s.cas[b];
    if(len<=L.maxRun(s,b)&&(!d2.length||L.canDropCascade(pl.slice(pl.length-len),d2[d2.length-1])))return{from:{type:'cascade',idx:a,runLen:len},to:{type:'cascade',idx:b}};}}
  for(f=0;f<4;f++)if(!s.cells[f])return{from:{type:'cascade',idx:a,runLen:1},to:{type:'free',idx:f}};}
 return null;}
T.eq(tot(),52,'initial 52');
while(steps<2000){steps++;var m=bm();
 if(!m)break;
 T.ok(L.applyMove(s,m.from,m.to),'legal bot move at '+steps);
 L.autoFound(s);
 T.eq(tot(),52,'conserved at '+steps);
 if(L.isWin(s))break;}
T.ok(steps>5,'bot progressed: '+steps);
T.eq(tot(),52,'final 52');
"""),
]

GAMES = [
G(
 slug="spider", title="سولیتر عنکبوتی", cat="cards", icon="🕷️",
 g1="#2e7d32", g2="#0b3d0b",
 desc="سولیتر عنکبوتی تک‌خال با ۱۰ ستون و ۵ بار پخش از دسته",
 hint="ردیف نزولی بساز و ردیف کامل K تا A را جمع کن",
 logic=SPIDER_LOGIC, ui=SPIDER_UI, css=SPIDER_CSS,
 engines=("common","card"), tests=SPIDER_TESTS, seed=12345
),
G(
 slug="freecell", title="فری‌سل", cat="cards", icon="🃏",
 g1="#1565c0", g2="#0a3d7a",
 desc="فری‌سل با ۸ ستون، ۴ خانه آزاد و ۴ بنیاد",
 hint="ردیف‌های رنگ متناوب را یکجا جابه‌جا کن و بنیادها را پر کن",
 logic=FREE_LOGIC, ui=FREE_UI, css=FREE_CSS,
 engines=("common","card"), tests=FREE_TESTS, seed=12345
),
]
