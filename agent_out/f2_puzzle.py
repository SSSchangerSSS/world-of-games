# -*- coding: utf-8 -*-
# AG-F2 — 4 Persian puzzle games in one batch: water-sort, calc24, kakuro, memory-grid
import sys, os
_p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _p not in sys.path:
    sys.path.insert(0, _p)
from lib_mini import G

WATER_LOGIC = r"""
var WOG_LOGIC=(function(){
function allSame(a){var i;if(!a.length)return true;for(i=1;i<a.length;i++)if(a[i]!==a[0])return false;return true;}
function canPour(b,s,d){
 if(s===d)return false;
 if(!b[s]||!b[s].length)return false;
 if(!b[d]||b[d].length>=4)return false;
 if(!b[d].length)return true;
 return b[d][b[d].length-1]===b[s][b[s].length-1];
}
function pour(b,s,d){
 var nb=[],i;
 for(i=0;i<b.length;i++)nb.push(b[i].slice());
 var src=nb[s],run=1;
 while(run<src.length&&src[src.length-1-run]===src[src.length-1])run++;
 var n=Math.min(run,4-nb[d].length);
 for(i=0;i<n;i++)nb[d].push(src.pop());
 return nb;
}
function isWin(b){
 for(var i=0;i<b.length;i++){
  var x=b[i];
  if(!x.length)continue;
  if(x.length>4)return false;
  for(var j=1;j<x.length;j++)if(x[j]!==x[0])return false;
 }
 return true;
}
function stKey(b){var p=[],i;for(i=0;i<b.length;i++)p.push(b[i].join('.'));return p.sort().join('|');}
function mScore(b,s,d){
 var sb=b[s],db=b[d],run=1;
 while(run<sb.length&&sb[sb.length-1-run]===sb[sb.length-1])run++;
 var v=db.length?3:1;
 if(run>=4-db.length)v+=3;
 if(run===sb.length)v+=2;
 return v;
}
function solve(bottles){
 var seen={},count=0,stack=[{b:bottles,path:[],ps:-1,pd:-1}];
 while(stack.length&&count<2000){
  var nd=stack.pop();count++;
  if(isWin(nd.b))return nd.path;
  var k=stKey(nd.b);
  if(seen[k])continue;
  seen[k]=1;
  var mv=[],s,d;
  for(s=0;s<nd.b.length;s++){
   if(!nd.b[s].length)continue;
   for(d=0;d<nd.b.length;d++){
    if(d===s)continue;
    if(s===nd.pd&&d===nd.ps)continue;
    if(canPour(nd.b,s,d))mv.push([s,d]);
   }
  }
  mv.sort(function(a,c){return mScore(nd.b,a[0],a[1])-mScore(nd.b,c[0],c[1]);});
  for(var i=0;i<mv.length;i++){
   stack.push({b:pour(nd.b,mv[i][0],mv[i][1]),path:nd.path.concat([mv[i]]),ps:mv[i][0],pd:mv[i][1]});
  }
 }
 return null;
}
function genLevel(colors,rng){
 if(!rng)rng=Math.random;
 var N=colors+2,b=[],c,pass=0;
 for(c=0;c<colors;c++)b.push([c,c,c,c]);
 b.push([]);b.push([]);
 var K=colors*2;
 while(isWin(b)&&pass<3){
  pass++;
  var lastS=-1,lastD=-1,done=0,guard=0;
  while(done<K&&guard<900){
   guard++;
   var pairs=[],s,d;
   for(s=0;s<N;s++){
    if(!b[s].length)continue;
    for(d=0;d<N;d++){
     if(d===s)continue;
     if(s===lastD&&d===lastS)continue;
     if(!canPour(b,s,d))continue;
     if(!b[d].length&&b[s].length===4&&allSame(b[s]))continue;
     pairs.push([s,d]);
    }
   }
   if(!pairs.length)break;
   var m=pairs[Math.floor(rng()*pairs.length)];
   b=pour(b,m[0],m[1]);
   lastS=m[0];lastD=m[1];done++;
  }
 }
 return b;
}
return {genLevel:genLevel,canPour:canPour,pour:pour,isWin:isWin,solve:solve};
})();
"""

WATER_UI = r"""
var PAL=['#e26d5c','#3fb8af','#d9a441','#67b98a','#b07ad4','#5a8fe0','#e0913f','#8fbf5a'];
var lvl=4,bottles=[],sel=-1,hist=[],moves=0;
function newGame(){bottles=L.genLevel(lvl);sel=-1;hist=[];moves=0;render();}
function render(){
 var app=$('#app');app.innerHTML='';
 var w=ce('div','bw');
 for(var i=0;i<bottles.length;i++){
  (function(i){
   var d=ce('div','wb'+(sel===i?' sb':''));
   for(var j=3;j>=0;j--){
    var sg=ce('div','sg');
    if(j<bottles[i].length)sg.style.background=PAL[bottles[i][j]];
    d.appendChild(sg);
   }
   d.onclick=function(){tap(i);};
   w.appendChild(d);
  })(i);
 }
 app.appendChild(w);
 var bar=ce('div','bar');
 var nb=ce('button','','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=newGame;bar.appendChild(nb);
 var ub=ce('button','','واگرد');ub.disabled=!hist.length;
 ub.onclick=function(){if(hist.length){bottles=hist.pop();moves=Math.max(0,moves-1);sel=-1;render();}};
 bar.appendChild(ub);
 var lbs=[4,6,8];
 for(var k=0;k<lbs.length;k++){
  (function(c){
   var b2=ce('button','lv'+(lvl===c?' on':''),fa(c)+' رنگ');
   b2.onclick=function(){lvl=c;newGame();};
   bar.appendChild(b2);
  })(lbs[k]);
 }
 app.appendChild(bar);
 hud('رنگ‌ها: '+fa(lvl)+' | حرکت‌ها: '+fa(moves));
}
function tap(i){
 if(sel<0){if(bottles[i].length){sel=i;render();}return;}
 if(i===sel){sel=-1;render();return;}
 if(L.canPour(bottles,sel,i)){
  var snap=[],q;
  for(q=0;q<bottles.length;q++)snap.push(bottles[q].slice());
  hist.push(snap);
  bottles=L.pour(bottles,sel,i);
  moves++;sel=-1;render();
  if(L.isWin(bottles)){
   setTimeout(function(){ovl('آفرین!','همهٔ رنگ‌ها در '+fa(moves)+' حرکت جدا شدند','مرحلهٔ جدید',function(){newGame();});},350);
  }
 }else{
  toast('این ریختن ممکن نیست');
  sel=-1;render();
 }
}
$('#hint').textContent='روی بطریِ مبدأ و سپس بطری مقصد بزن؛ رنگِ یکسان روی هم می‌نشیند و بطری خالی هر رنگی می‌پذیرد.';
newGame();
"""

WATER_CSS = r"""
body{background:#0b1526;color:#e8edf7;font-family:Tahoma,'Segoe UI',sans-serif;margin:0;padding:10px;text-align:center}
h1{color:#d9a441;font-size:1.25em;margin:.3em}
#hud{color:#3fb8af;min-height:1.3em;font-size:.95em}
.wog-home{color:#3fb8af;font-size:.8em;text-decoration:none}
button{background:#14203a;color:#e8edf7;border:1px solid #d9a441;border-radius:8px;padding:9px 13px;min-height:40px;margin:3px;font-size:1em;touch-action:manipulation;cursor:pointer}
button:disabled{opacity:.4}
button.on{background:#d9a441;color:#0b1526}
.bw{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:14px 0}
.wb{width:36px;height:150px;border:2px solid #3fb8af;border-top-width:1px;border-radius:4px 4px 12px 12px;background:#14203a;display:flex;flex-direction:column;overflow:hidden;cursor:pointer}
.wb.sb{border-color:#d9a441;box-shadow:0 0 8px rgba(217,164,65,.5)}
.sg{flex:1;min-height:0;border-bottom:1px solid rgba(11,21,38,.35)}
.bar{margin:8px 0}
#hint{color:#8fa3c8;font-size:.85em}
"""

CALC_LOGIC = r"""
var WOG_LOGIC=(function(){
var EPS=1e-6;
function solve24(nums){
 function rec(it){
  if(it.length===1){
   var o=it[0];
   if(isFinite(o.v)&&Math.abs(o.v-24)<=EPS)return {value:o.v,expr:o.e};
   return null;
  }
  for(var i=0;i<it.length;i++){
   for(var j=0;j<it.length;j++){
    if(i===j)continue;
    var rest=[],k;
    for(k=0;k<it.length;k++)if(k!==i&&k!==j)rest.push(it[k]);
    var A=it[i],B=it[j],cd=[];
    if(i<j)cd.push({v:A.v+B.v,e:'('+A.e+'+'+B.e+')'});
    cd.push({v:A.v-B.v,e:'('+A.e+'-'+B.e+')'});
    if(i<j)cd.push({v:A.v*B.v,e:'('+A.e+'*'+B.e+')'});
    if(Math.abs(B.v)>EPS)cd.push({v:A.v/B.v,e:'('+A.e+'/'+B.e+')'});
    for(var c=0;c<cd.length;c++){
     if(!isFinite(cd[c].v))continue;
     var r=rec([cd[c]].concat(rest));
     if(r)return r;
    }
   }
  }
  return null;
 }
 var it=[],i;
 for(i=0;i<nums.length;i++)it.push({v:nums[i],e:String(nums[i])});
 return rec(it);
}
function drawHand(rng){
 if(!rng)rng=Math.random;
 var ns=null,t,i,h;
 for(t=0;t<40;t++){
  h=[];
  for(i=0;i<4;i++)h.push(1+Math.floor(rng()*13));
  ns=h;
  if(solve24(h))break;
 }
 return ns;
}
return {solve24:solve24,drawHand:drawHand};
})();
"""

CALC_UI = r"""
var OPS=[['+','+'],['−','-'],['×','*'],['÷','/']];
var tiles=[],sel=[],hist=[],start=[],solText='';
function fmt(v){
 var s=(Math.round(v*100)/100).toString().replace('.','٫');
 return s.replace(/[0-9]/g,function(d){return '۰۱۲۳۴۵۶۷۸۹'[+d];});
}
function pretty(e){return e.replace(/\*/g,'×').replace(/\//g,'÷').replace(/-/g,'−');}
function newHand(){
 start=L.drawHand();
 tiles=[];hist=[];sel=[];solText='';
 for(var i=0;i<start.length;i++)tiles.push({v:start[i],e:String(start[i])});
 render();
}
function render(){
 var app=$('#app');app.innerHTML='';
 var tr=ce('div','trow');
 for(var i=0;i<tiles.length;i++){
  (function(i){
   var b=ce('button','tile'+(sel.indexOf(i)>=0?' st':''),fmt(tiles[i].v));
   b.onclick=function(){pick(i);};
   tr.appendChild(b);
  })(i);
 }
 app.appendChild(tr);
 var bar=ce('div','bar');
 for(var j=0;j<OPS.length;j++){
  (function(o){
   var b=ce('button','op',o[0]);
   b.disabled=sel.length!==2;
   b.onclick=function(){applyOp(o[1]);};
   bar.appendChild(b);
  })(OPS[j]);
 }
 var ub=ce('button','','واگرد');ub.disabled=!hist.length;
 ub.onclick=function(){if(hist.length){tiles=hist.pop();sel=[];render();}};
 bar.appendChild(ub);
 var nb=ce('button','','دست جدید');nb.setAttribute('data-smoke','1');nb.onclick=newHand;bar.appendChild(nb);
 var hb=ce('button','','راه‌حل');
 hb.onclick=function(){var s=L.solve24(start);solText=s?('یک راه‌حل: '+pretty(s.expr)):'برای این دست راه‌حلی نیست!';render();};
 bar.appendChild(hb);
 app.appendChild(bar);
 app.appendChild(ce('div','solbox',solText));
 hud('هدف: ۲۴ | کاشی‌ها: '+fa(tiles.length));
}
function pick(i){
 var ix=sel.indexOf(i);
 if(ix>=0){sel.splice(ix,1);render();return;}
 if(sel.length>=2){sel=[i];}else{sel.push(i);}
 render();
}
function applyOp(op){
 if(sel.length!==2)return;
 var a=tiles[sel[0]],b=tiles[sel[1]],v;
 if(op==='+')v=a.v+b.v;
 else if(op==='-')v=a.v-b.v;
 else if(op==='*')v=a.v*b.v;
 else{
  if(Math.abs(b.v)<1e-9){toast('تقسیم بر صفر ممکن نیست');return;}
  v=a.v/b.v;
 }
 hist.push(tiles);
 var nt={v:v,e:'('+a.e+op+b.e+')'};
 var ntiles=[];
 tiles.forEach(function(t,i){if(i!==sel[0]&&i!==sel[1])ntiles.push(t);});
 ntiles.push(nt);
 tiles=ntiles;sel=[];
 render();
 if(tiles.length===1&&Math.abs(tiles[0].v-24)<=1e-6){
  ovl('بردی!',pretty(tiles[0].e)+' = ۲۴','دست جدید',function(){newHand();});
 }
}
$('#hint').textContent='دو عدد را انتخاب کن و یکی از چهار عمل را بزن تا به ۲۴ برسی؛ با واگرد می‌توانی عقب برگردی.';
newHand();
"""

CALC_CSS = r"""
body{background:#0b1526;color:#e8edf7;font-family:Tahoma,'Segoe UI',sans-serif;margin:0;padding:10px;text-align:center}
h1{color:#d9a441;font-size:1.25em;margin:.3em}
#hud{color:#3fb8af;min-height:1.3em;font-size:.95em}
.wog-home{color:#3fb8af;font-size:.8em;text-decoration:none}
button{background:#14203a;color:#e8edf7;border:1px solid #d9a441;border-radius:8px;padding:9px 13px;min-height:40px;margin:3px;font-size:1em;touch-action:manipulation;cursor:pointer}
button:disabled{opacity:.4}
.trow{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:12px 0}
.tile{width:70px;height:56px;font-size:1.25em;background:#1c2c4a;border:1px solid #3fb8af}
.tile.st{border-color:#d9a441;box-shadow:0 0 8px rgba(217,164,65,.5);background:#26375c}
.op{width:52px;font-size:1.2em;border-color:#3fb8af}
.solbox{min-height:1.6em;color:#d9a441;font-size:.95em;margin-top:8px}
.bar{margin:8px 0}
#hint{color:#8fa3c8;font-size:.85em}
"""

KAK_LOGIC = r"""
var WOG_LOGIC=(function(){
function runCells(run){return run.cells;}
function checkRun(cells,clue){
 var sum=0,seen={},i,v;
 for(i=0;i<cells.length;i++){
  v=cells[i];
  if(typeof v!=='number'||v%1!==0||v<1||v>9)return false;
  if(seen[v])return false;
  seen[v]=1;sum+=v;
 }
 return sum===clue;
}
function isWin(grid,layout){
 for(var i=0;i<layout.runs.length;i++){
  var run=layout.runs[i],arr=[],j;
  for(j=0;j<run.cells.length;j++){
   var cell=grid[run.cells[j][0]][run.cells[j][1]];
   if(typeof cell!=='number')return false;
   arr.push(cell);
  }
  if(!checkRun(arr,run.sum))return false;
 }
 return true;
}
var EASY={id:0,name:'آسان',
 blocked:[[0,0],[0,4],[2,2],[4,0],[4,4]],
 runs:[
  {cells:[[0,1],[0,2],[0,3]],sum:6},
  {cells:[[1,0],[1,1],[1,2],[1,3],[1,4]],sum:25},
  {cells:[[2,0],[2,1]],sum:11},
  {cells:[[2,3],[2,4]],sum:9},
  {cells:[[3,0],[3,1],[3,2],[3,3],[3,4]],sum:25},
  {cells:[[4,1],[4,2],[4,3]],sum:14},
  {cells:[[1,0],[2,0],[3,0]],sum:18},
  {cells:[[0,1],[1,1],[2,1],[3,1],[4,1]],sum:21},
  {cells:[[0,2],[1,2],[3,2],[4,2]],sum:20},
  {cells:[[0,3],[1,3],[2,3],[3,3],[4,3]],sum:25},
  {cells:[[1,4],[2,4],[3,4]],sum:6}
 ],
 solution:[[0,3,1,2,0],[4,8,7,5,1],[9,2,0,6,3],[5,1,8,9,2],[0,7,4,3,0]]};
var NORMAL={id:1,name:'معمولی',
 blocked:[[0,0],[1,3],[3,1],[4,3],[4,4]],
 runs:[
  {cells:[[0,1],[0,2],[0,3],[0,4]],sum:10},
  {cells:[[1,0],[1,1],[1,2]],sum:18},
  {cells:[[2,0],[2,1],[2,2],[2,3],[2,4]],sum:29},
  {cells:[[3,2],[3,3],[3,4]],sum:14},
  {cells:[[4,0],[4,1],[4,2]],sum:10},
  {cells:[[1,0],[2,0],[3,0],[4,0]],sum:17},
  {cells:[[0,1],[1,1],[2,1],[4,1]],sum:14},
  {cells:[[0,2],[1,2],[2,2],[3,2],[4,2]],sum:23},
  {cells:[[0,3],[2,3],[3,3]],sum:9},
  {cells:[[0,4],[1,4],[2,4],[3,4]],sum:27}
 ],
 solution:[[0,1,2,3,4],[5,6,7,0,8],[9,4,8,2,6],[1,0,1,4,9],[2,3,5,0,0]]};
return {LAYOUTS:[EASY,NORMAL],runCells:runCells,checkRun:checkRun,isWin:isWin};
})();
"""

KAK_UI = r"""
var cur=0,grid=[];
function newGame(){
 grid=[];
 for(var r=0;r<5;r++)grid.push([0,0,0,0,0]);
 render();
}
function render(){
 var lay=L.LAYOUTS[cur];
 var blocked={},starts={};
 lay.blocked.forEach(function(rc){blocked[rc[0]+'-'+rc[1]]=1;});
 lay.runs.forEach(function(run){
  var rc=run.cells[0];
  var horiz=run.cells.length>1&&run.cells[0][0]===run.cells[1][0];
  starts[rc[0]+'-'+rc[1]]={s:run.sum,h:horiz};
 });
 var app=$('#app');app.innerHTML='';
 var tb=ce('table','kg');
 for(var r=0;r<5;r++){
  var tr=ce('tr');
  for(var c=0;c<5;c++){
   var td=ce('td');
   var kk=r+'-'+c;
   if(blocked[kk]){td.className='kb';}
   else{
    td.className='kc';
    td.textContent=grid[r][c]>0?fa(grid[r][c]):'';
    (function(r,c){
     td.onclick=function(){grid[r][c]=(grid[r][c]+1)%10;render();maybeWin();};
    })(r,c);
   }
   if(starts[kk]){
    var st=starts[kk];
    td.appendChild(ce('span',st.h?'ch':'cv',fa(st.s)));
   }
   tr.appendChild(td);
  }
  tb.appendChild(tr);
 }
 app.appendChild(tb);
 var bar=ce('div','bar');
 var nb=ce('button','','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=function(){newGame();toast('جدول پاک شد');};bar.appendChild(nb);
 var cb=ce('button','','پاک کردن');cb.onclick=function(){newGame();toast('جدول پاک شد');};bar.appendChild(cb);
 L.LAYOUTS.forEach(function(lay){
  var b2=ce('button','lv'+(cur===lay.id?' on':''),lay.name);
  b2.onclick=function(){cur=lay.id;newGame();};
  bar.appendChild(b2);
 });
 app.appendChild(bar);
 hud('چیدمان: '+lay.name);
}
function maybeWin(){
 if(L.isWin(grid,L.LAYOUTS[cur])){
  ovl('کاکورو حل شد!','همهٔ اجراها جمع و عدم‌تکرار درست دارند','چیدمان دیگر',function(){cur=(cur+1)%L.LAYOUTS.length;newGame();});
 }
}
$('#hint').textContent='روی خانه بزن تا عدد ۱ تا ۹ عوض شود؛ در هر اجرا ارقام غیرتکراری و برابر جمع سرنخ باشند.';
newGame();
"""

KAK_CSS = r"""
body{background:#0b1526;color:#e8edf7;font-family:Tahoma,'Segoe UI',sans-serif;margin:0;padding:10px;text-align:center}
h1{color:#d9a441;font-size:1.25em;margin:.3em}
#hud{color:#3fb8af;min-height:1.3em;font-size:.95em}
.wog-home{color:#3fb8af;font-size:.8em;text-decoration:none}
button{background:#14203a;color:#e8edf7;border:1px solid #d9a441;border-radius:8px;padding:9px 13px;min-height:40px;margin:3px;font-size:1em;touch-action:manipulation;cursor:pointer}
button.on{background:#d9a441;color:#0b1526}
.kg{border-collapse:collapse;margin:10px auto}
.kg td{width:52px;height:52px;border:1px solid #3fb8af;position:relative;font-size:1.3em;font-weight:bold;text-align:center}
.kb{background:#0b1526;border-color:#1c2c4a}
.kc{background:#14203a;cursor:pointer}
.kc:hover{background:#1a2a4a}
.ch,.cv{position:absolute;top:2px;font-size:.62em;font-weight:normal;padding:1px 3px;border-radius:4px;line-height:1.2}
.ch{left:3px;background:#d9a441;color:#0b1526}
.cv{right:3px;background:#1c3a5a;color:#3fb8af;border:1px solid #3fb8af}
.bar{margin:8px 0}
#hint{color:#8fa3c8;font-size:.85em}
"""

MEM_LOGIC = r"""
var WOG_LOGIC=(function(){
function genCells(level,rng){
 if(!rng)rng=Math.random;
 var n=Math.min(3+level,12),pool=[],i;
 for(i=0;i<25;i++)pool.push(i);
 for(i=pool.length-1;i>0;i--){
  var j=Math.floor(rng()*(i+1)),t=pool[i];
  pool[i]=pool[j];pool[j]=t;
 }
 return pool.slice(0,n);
}
function check(cells,picked){
 var mark={},i,misses=[];
 for(i=0;i<cells.length;i++)mark[cells[i]]=1;
 var hit=picked.length>0&&mark[picked[picked.length-1]]===1;
 for(i=0;i<picked.length;i++)if(mark[picked[i]]!==1)misses.push(picked[i]);
 var complete=true;
 for(i=0;i<cells.length;i++)if(picked.indexOf(cells[i])<0){complete=false;break;}
 return {hit:hit,complete:complete,misses:misses};
}
function isLevelUp(foundCount,target){return foundCount>=target;}
function afterMiss(lives){var l=lives-1;return {lives:l,dead:l<=0};}
return {genCells:genCells,check:check,isLevelUp:isLevelUp,afterMiss:afterMiss};
})();
"""

MEM_UI = r"""
var level=0,lives=3,targets=[],found=[],showing=false;
function newGame(){level=0;lives=3;newRound();}
function newRound(){
 targets=L.genCells(level);
 found=[];showing=true;
 render();
 setTimeout(function(){showing=false;render();},1100+targets.length*90);
}
function render(){
 var app=$('#app');app.innerHTML='';
 var tb=ce('div','mg');
 for(var i=0;i<25;i++){
  (function(i){
   var d=ce('div','mc');
   if(showing&&targets.indexOf(i)>=0)d.className+=' tg';
   if(!showing&&found.indexOf(i)>=0)d.className+=' fd';
   d.onclick=function(){pick(i);};
   tb.appendChild(d);
  })(i);
 }
 app.appendChild(tb);
 var bar=ce('div','bar');
 var nb=ce('button','','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=newGame;bar.appendChild(nb);
 app.appendChild(bar);
 var hearts='';
 for(var h=0;h<lives;h++)hearts+='♥';
 hud('مرحلهٔ '+fa(level+1)+' | جان: '+hearts+' | پیداشده: '+fa(found.length)+' از '+fa(targets.length));
}
function pick(i){
 if(showing)return;
 if(found.indexOf(i)>=0)return;
 var res=L.check(targets,found.concat([i]));
 if(res.hit){
  found.push(i);render();
  if(res.complete){
   toast('مرحله کامل شد!');
   setTimeout(function(){level++;newRound();},800);
  }
 }else{
  var r=L.afterMiss(lives);
  lives=r.lives;
  if(r.dead){
   render();
   var best=parseInt(store.get('wog-memory-grid-best')||'0',10)||0;
   if(level>best)store.set('wog-memory-grid-best',String(level));
   ovl('باختی!','به مرحلهٔ '+fa(level+1)+' رسیدی | رکورد: '+fa(Math.max(best,level)),'بازی جدید',function(){newGame();});
  }else{
   toast('اشتباه بود! یک جان کم شد؛ دوباره نگاه کن');
   found=[];
   showing=true;
   render();
   setTimeout(function(){showing=false;render();},1100+targets.length*90);
  }
 }
}
$('#hint').textContent='خانه‌های روشن را به خاطر بسپار و بعد از خاموشی همهٔ آن‌ها را پیدا کن؛ هر خطا یک جان می‌گیرد.';
newGame();
"""

MEM_CSS = r"""
body{background:#0b1526;color:#e8edf7;font-family:Tahoma,'Segoe UI',sans-serif;margin:0;padding:10px;text-align:center}
h1{color:#d9a441;font-size:1.25em;margin:.3em}
#hud{color:#3fb8af;min-height:1.3em;font-size:.95em}
.wog-home{color:#3fb8af;font-size:.8em;text-decoration:none}
button{background:#14203a;color:#e8edf7;border:1px solid #d9a441;border-radius:8px;padding:9px 13px;min-height:40px;margin:3px;font-size:1em;touch-action:manipulation;cursor:pointer}
.mg{display:grid;grid-template-columns:repeat(5,54px);gap:6px;justify-content:center;margin:12px 0}
.mc{height:54px;border-radius:8px;background:#14203a;border:1px solid #1c2c4a;cursor:pointer;transition:background .25s;touch-action:manipulation}
.mc.tg{background:#3fb8af;border-color:#3fb8af}
.mc.fd{background:#67b98a;border-color:#67b98a}
.bar{margin:8px 0}
#hint{color:#8fa3c8;font-size:.85em}
"""

MRJS = "function MR(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}"

water_tests = [
("قوانین ریختن: ناهم‌رنگ، هدف پر، مبدأ خالی، خود بطری",
 "var b=[[1,2],[2,1],[],[]];"
 "T.ok(!L.canPour(b,0,1),'color mismatch');"
 "T.ok(!L.canPour(b,1,0),'reverse mismatch');"
 "T.ok(L.canPour(b,0,2),'pour to empty ok');"
 "T.ok(L.canPour(b,1,2),'second to empty ok');"
 "var c=[[1],[1,2,3,4],[],[]];"
 "T.ok(!L.canPour(c,0,1),'target full');"
 "T.ok(!L.canPour(b,2,0),'empty source');"
 "T.ok(!L.canPour(b,0,0),'same bottle');"),
("مقدار ریختن = کمینهٔ ران هم‌رنگ و جای خالی + عدم تغییر مبدأ",
 "var b=[[1,1,1,2],[1],[],[]];var r=L.pour(b,0,1);"
 "T.eq(r[0],[1,1,1],'src after run-1 pour');T.eq(r[1],[1,2],'dst after');"
 "var b2=[[1,1,2,2],[2],[],[]];var r2=L.pour(b2,0,1);"
 "T.eq(r2[0],[1,1],'run 2 moved');T.eq(r2[1],[2,2,2],'run 2 landed on existing 2');"
 "var b3=[[1,2,2,2],[2,2,2],[],[]];var r3=L.pour(b3,0,1);"
 "T.eq(r3[0],[1,2,2],'capped by free space');T.eq(r3[1],[2,2,2,2],'dst full');"
 "T.eq(b[0],[1,1,1,2],'original untouched');T.eq(b[1],[1],'original dst untouched');"),
("تشخیص برد: یکدست یا خالی",
 "T.ok(L.isWin([[0,0,0,0],[1,1,1,1],[],[]]),'solved');"
 "T.ok(L.isWin([[],[],[],[]]),'all empty');"
 "T.ok(L.isWin([[],[2,2],[3,3,3,3]]),'uniform partial ok per rules');"
 "T.ok(!L.isWin([[0,0,1,0],[],[],[]]),'mixed bottle');"
 "T.ok(!L.isWin([[0,0],[0,0,1,1],[],[]]),'second mixed');"),
("ساختار genLevel و حالت بدون راه‌حل",
 MRJS +
 "var lvl=L.genLevel(6,MR(42));"
 "T.eq(lvl.length,8,'N=C+2 bottles');"
 "var cnt={},tot=0;"
 "lvl.forEach(function(x){T.ok(x.length<=4,'capacity');x.forEach(function(v){cnt[v]=(cnt[v]||0)+1;tot++;});});"
 "T.eq(tot,24,'total units 6x4');"
 "for(var c=0;c<6;c++)T.eq(cnt[c],4,'4 units of color '+c);"
 "T.eq(L.solve([[0,1],[1,0]]),null,'no-move state unsolvable');"
 "T.ok(L.solve([[0,0],[1,1],[],[]]),'easy state solvable');"),
("همهٔ مراحل ۴..۸ رنگ با ۵ بذر توسط حل‌کننده حل می‌شوند",
 MRJS +
 "var total=0;"
 "for(var colors=4;colors<=8;colors++){"
 " for(var s=1;s<=5;s++){"
 "  var rng=MR(s*7919+colors*13+1);"
 "  var lvl=L.genLevel(colors,rng);"
 "  T.eq(lvl.length,colors+2,'bottles c='+colors);"
 "  var sol=L.solve(lvl);"
 "  T.ok(sol,'solvable c='+colors+' s='+s+' state='+JSON.stringify(lvl));"
 "  if(sol){"
 "   var cur=[];for(var i=0;i<lvl.length;i++)cur.push(lvl[i].slice());"
 "   for(var m=0;m<sol.length;m++){"
 "    T.ok(L.canPour(cur,sol[m][0],sol[m][1]),'legal move '+m+' c='+colors+' s='+s);"
 "    cur=L.pour(cur,sol[m][0],sol[m][1]);"
 "   }"
 "   T.ok(L.isWin(cur),'path wins c='+colors+' s='+s);"
 "  }"
 "  total++;"
 " }"
 "}"
 "T.eq(total,25,'25 gen+solve cases');"),
]

calc_tests = [
("[3,3,8,8] حل‌شدنی و حاصل ۲۴",
 "var r=L.solve24([3,3,8,8]);"
 "T.ok(r&&typeof r.expr==='string'&&r.expr.length>5,'expr returned');"
 "T.ok(r&&isFinite(r.value),'finite value');"
 "T.near(r.value,24,1e-6,'equals 24');"),
("[1,1,1,1] ناممکن (جست‌وجوی محدود تمام می‌شود)",
 "T.eq(L.solve24([1,1,1,1]),null,'unsolvable hand');"
 "T.eq(L.solve24([13,13,13,13]),null,'another unsolvable');"),
("محافظت تقسیم بر صفر — بدون NaN/Inf",
 "T.eq(L.solve24([0,0,0,0]),null,'0000 no throw no result');"
 "var a=L.solve24([5,0,0,0]);T.ok(a===null||isFinite(a.value),'finite or null 5000');"
 "var b=L.solve24([1,2,3,0]);T.ok(b===null||isFinite(b.value),'finite or null 1230');"
 "var c=L.solve24([9,0,3,3]);T.ok(c===null||isFinite(c.value),'finite or null 9033');"),
("۵۰ دست دانه‌دار: هر راه‌حل دقیقاً ۲۴",
 MRJS +
 "var rng=MR(2024);"
 "for(var i=0;i<50;i++){"
 " var hand=L.drawHand(rng);"
 " T.ok(hand&&hand.length===4,'hand size '+i);"
 " for(var j=0;j<4;j++)T.ok(hand[j]>=1&&hand[j]<=13,'range '+i);"
 " var r=L.solve24(hand);"
 " T.ok(r,'solvable hand '+i+': '+JSON.stringify(hand));"
 " if(r){T.ok(isFinite(r.value),'finite '+i);T.near(r.value,24,1e-6,'value 24 hand '+i);}"
 "}"),
("دست‌های کلاسیک و تکرار‌پذیری drawHand",
 MRJS +
 "T.ok(L.solve24([5,5,5,1]),'5*(5-1/5)=24');"
 "T.ok(L.solve24([1,3,4,6]),'6/(1-3/4)=24');"
 "T.ok(L.solve24([4,7,8,8]),'classic');"
 "T.eq(L.drawHand(MR(7)),L.drawHand(MR(7)),'deterministic draws');"
 "var h=L.drawHand(MR(99));"
 "T.ok(h.length===4,'draw size');"
 "h.forEach(function(n){T.ok(n>=1&&n<=13,'draw range');});"),
]

kak_tests = [
("checkRun: جمع و عدم‌تکرار درست",
 "T.ok(L.checkRun([1,2,3],6),'1+2+3=6');"
 "T.ok(L.checkRun([2,7],9),'2+7=9');"
 "T.ok(L.checkRun([9],9),'single 9');"
 "T.ok(L.checkRun([1,3,5,7,9],25),'five distinct');"),
("checkRun: ارقام تکراری رد شود",
 "T.ok(!L.checkRun([2,2,3],7),'duplicate 2');"
 "T.ok(!L.checkRun([5,5],10),'duplicate 5');"
 "T.ok(!L.checkRun([1,1,1,1,1],5),'all same');"),
("checkRun: جمع غلط رد شود",
 "T.ok(!L.checkRun([1,2,4],6),'sum 7 != 6');"
 "T.ok(!L.checkRun([1,2,3],7),'sum 6 != 7');"
 "T.ok(!L.checkRun([4],9),'sum 4 != 9');"),
("کران ارقام ۱..۹",
 "T.ok(!L.checkRun([0,2,3],5),'zero rejected');"
 "T.ok(!L.checkRun([10,2],12),'ten rejected');"
 "T.ok(!L.checkRun([-1,3],2),'negative rejected');"
 "T.ok(!L.checkRun([1.5,2],3.5),'fraction rejected');"),
("هر دو چیدمان با راه‌حلِ ثبت‌شده برده می‌شوند",
 "T.ok(L.LAYOUTS.length===2,'two layouts');"
 "L.LAYOUTS.forEach(function(lay,ix){"
 " T.ok(L.isWin(lay.solution,lay),'layout '+ix+' solution wins');"
 " var empty=[];for(var r=0;r<5;r++)empty.push([0,0,0,0,0]);"
 " T.ok(!L.isWin(empty,lay),'layout '+ix+' empty not win');"
 " var bad=[];lay.solution.forEach(function(row){bad.push(row.slice());});"
 " var done=false;"
 " for(var r2=0;r2<5&&!done;r2++)for(var c=0;c<5&&!done;c++){"
 "  if(bad[r2][c]>0&&bad[r2][c]<9){bad[r2][c]++;done=true;}"
 " }"
 " T.ok(!L.isWin(bad,lay),'layout '+ix+' corrupted rejected');"
 "});"),
("ساختار چیدمان‌ها: پوشش کامل خانه‌ها و کران‌ها",
 "L.LAYOUTS.forEach(function(lay){"
 " T.ok(lay.runs.length>=8,'at least 8 runs');"
 " var cover={};"
 " lay.runs.forEach(function(run){"
 "  T.eq(L.runCells(run),run.cells,'runCells identity');"
 "  T.ok(run.cells.length>=2,'run length >=2');"
 "  T.ok(run.sum>=3&&run.sum<=45,'sum plausible');"
 "  run.cells.forEach(function(rc){"
 "   T.ok(rc[0]>=0&&rc[0]<5&&rc[1]>=0&&rc[1]<5,'cell in grid');"
 "   cover[rc[0]+'-'+rc[1]]=1;"
 "  });"
 " });"
 " var filled=0;"
 " for(var r=0;r<5;r++)for(var c=0;c<5;c++){"
 "  if(lay.solution[r][c]>0){"
 "   filled++;"
 "   T.ok(cover[r+'-'+c],'cell covered by a run '+r+','+c);"
 "   T.ok(lay.solution[r][c]>=1&&lay.solution[r][c]<=9,'digit bounds');"
 "  }"
 " }"
 " T.ok(filled>=18,'enough fillable cells');"
 "});"),
]

mem_tests = [
("genCells: یکتایی و اندازه در هر مرحله",
 MRJS +
 "var sizes=[0,1,5,9,20];"
 "for(var i=0;i<sizes.length;i++){"
 " var lv=sizes[i];"
 " var cs=L.genCells(lv,MR(1000+lv));"
 " T.eq(cs.length,Math.min(3+lv,12),'size lv'+lv);"
 " var un={};"
 " cs.forEach(function(c){un[c]=1;T.ok(c>=0&&c<25,'range 0..24');});"
 " T.eq(Object.keys(un).length,cs.length,'unique lv'+lv);"
 "}"),
("check: بردارهای hit/complete/miss",
 "var r1=L.check([1,2,3],[1,3]);T.ok(r1.hit,'hit on last');T.ok(!r1.complete,'not complete');T.eq(r1.misses,[],'no miss');"
 "var r2=L.check([1,2,3],[1,7]);T.ok(!r2.hit,'miss on last');T.eq(r2.misses,[7],'miss recorded');"
 "var r3=L.check([1,2,3],[2,3,1]);T.ok(r3.complete,'order-free complete');T.ok(r3.hit,'last is hit');"
 "var r4=L.check([1,2,3],[5,1,2,3]);T.ok(r4.complete,'complete despite early miss');T.eq(r4.misses,[5],'early miss kept');"
 "var r5=L.check([1,2,3],[]);T.ok(!r5.hit,'empty picks');T.ok(!r5.complete,'empty not complete');T.eq(r5.misses,[],'no misses');"),
("۳۰ مرحلهٔ دانه‌دار با اندازهٔ معتبر",
 MRJS +
 "for(var i=0;i<30;i++){"
 " var cs=L.genCells(i,MR(i*13+7));"
 " T.eq(cs.length,Math.min(3+i,12),'valid size lv'+i);"
 " var un={};cs.forEach(function(c){un[c]=1;});"
 " T.eq(Object.keys(un).length,cs.length,'unique lv'+i);"
 "}"),
("سقف تعداد خانه‌ها و isLevelUp",
 MRJS +
 "T.eq(L.genCells(9,MR(1)).length,12,'cap reached at 9');"
 "T.eq(L.genCells(100,MR(2)).length,12,'hard cap 12');"
 "T.ok(L.isLevelUp(12,12),'levelup on equal');"
 "T.ok(!L.isLevelUp(11,12),'no levelup below');"
 "T.ok(L.isLevelUp(13,12),'levelup above');"),
("جریان جان‌ها با afterMiss",
 "var a=L.afterMiss(3);T.eq(a.lives,2,'3->2');T.eq(a.dead,false,'alive');"
 "var b=L.afterMiss(2);T.eq(b.lives,1,'2->1');T.eq(b.dead,false,'alive');"
 "var c=L.afterMiss(1);T.eq(c.lives,0,'1->0');T.eq(c.dead,true,'dead at 0');"
 "var d=L.afterMiss(0);T.eq(d.lives,-1,'stays consistent');T.eq(d.dead,true,'still dead');"),
]

GAMES = [
 G(
  slug="water-sort", title="آب‌ریز", cat="puzzle", icon="💧",
  g1="#2e86ab", g2="#3fb8af",
  desc="بطری‌های رنگی را با ریختنِ هوشمندانه از هم جدا کن؛ هر بطری در پایان فقط یک رنگ.",
  hint="روی بطری مبدأ و بعد مقصد بزن؛ فقط رنگ یکسان روی هم می‌نشیند.",
  logic=WATER_LOGIC, ui=WATER_UI, css=WATER_CSS, engines=("common",),
  tests=water_tests, seed=12345),
 G(
  slug="calc24", title="۲۴ با اعداد", cat="puzzle", icon="🧮",
  g1="#d9a441", g2="#e26d5c",
  desc="با چهار عدد و چهار عمل به ۲۴ برس؛ بازی هوش و حساب با راه‌نمای راه‌حل.",
  hint="دو عدد را انتخاب کن و عمل بزن؛ واگرد هم داری.",
  logic=CALC_LOGIC, ui=CALC_UI, css=CALC_CSS, engines=("common",),
  tests=calc_tests, seed=12345),
 G(
  slug="kakuro", title="کاکورو", cat="puzzle", icon="🔢",
  g1="#3fb8af", g2="#67b98a",
  desc="جدولی از جمع‌ها؛ در هر اجرا ارقام غیرتکراری باید دقیقاً برابر سرنخ شوند.",
  hint="روی خانه‌ها بزن تا عدد ۱ تا ۹ عوض شود.",
  logic=KAK_LOGIC, ui=KAK_UI, css=KAK_CSS, engines=("common",),
  tests=kak_tests, seed=12345),
 G(
  slug="memory-grid", title="شبکهٔ حافظه", cat="puzzle", icon="🧠",
  g1="#7e5ad4", g2="#3fb8af",
  desc="خانه‌های روشن را لحظه‌ای ببین و بعد پیدا کن؛ هر مرحله خانه‌های بیشتری دارد.",
  hint="خوب نگاه کن؛ هر خطا یک جان کم می‌کند.",
  logic=MEM_LOGIC, ui=MEM_UI, css=MEM_CSS, engines=("common",),
  tests=mem_tests, seed=12345),
]
