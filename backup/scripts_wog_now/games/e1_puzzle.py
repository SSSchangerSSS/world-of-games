# -*- coding: utf-8 -*-
from lib_mini import G

P15_LOGIC = r"""
var WOG_LOGIC=(function(){
function initial(){var b=[],i;for(i=1;i<=15;i++)b.push(i);b.push(0);return{b:b,moves:0,hist:[]};}
function blank(s){return s.b.indexOf(0);}
function slide(s,r,c){if(r<0||r>3||c<0||c>3)return false;var bi=blank(s),br=(bi/4)|0,bc=bi%4;
 if(Math.abs(br-r)+Math.abs(bc-c)!==1)return false;
 var t=r*4+c;s.hist.push({b:s.b.slice(),moves:s.moves});
 s.b[bi]=s.b[t];s.b[t]=0;s.moves++;return true;}
function undo(s){if(!s.hist||!s.hist.length)return false;var h=s.hist.pop();s.b=h.b;s.moves=h.moves;return true;}
function isSolved(s){var i;for(i=0;i<15;i++)if(s.b[i]!==i+1)return false;return s.b[15]===0;}
function inversions(p){var n=0,i,j;for(i=0;i<p.length;i++){if(!p[i])continue;for(j=i+1;j<p.length;j++)if(p[j]&&p[i]>p[j])n++;}return n;}
function solvable(s,w){w=w||4;var b=(s&&s.b)?s.b:s;var bi=b.indexOf(0);var row=(bi/w)|0;return((inversions(b)+row)%2)===1;}
function shuffle(s,n,rng){var r=rng||Math.random,i,bi,br,last=-1,pick,cand,d,t;
 for(i=0;i<n;i++){bi=blank(s);br=(bi/4)|0;cand=[];
  var nb=[bi-4,bi+4,bi-1,bi+1];
  for(d=0;d<4;d++){t=nb[d];if(t<0||t>15||t===last)continue;
   if(d>=2&&((t/4)|0)!==br)continue;cand.push(t);}
  pick=cand[(r()*cand.length)|0];last=bi;
  s.b[bi]=s.b[pick];s.b[pick]=0;}
 s.moves=0;s.hist=[];return s;}
return{initial:initial,blank:blank,slide:slide,undo:undo,isSolved:isSolved,inversions:inversions,solvable:solvable,shuffle:shuffle};
})();
"""

P15_UI = r"""
var st=null,iv=null,secs=0,started=false;
var app=$('#app'),wrap=ce('div','p15wrap');app.appendChild(wrap);
var board=ce('div','p15board');wrap.appendChild(board);
var tiles={};
function mkTile(vv){var el=ce('div','p15tile');el.textContent=fa(vv);
 el.addEventListener('click',function(){if(!st)return;var i=st.b.indexOf(vv);trySlide((i/4)|0,i%4);});
 board.appendChild(el);tiles[vv]=el;}
for(var v=1;v<=15;v++)mkTile(v);
var bar=ce('div','btnrow');wrap.appendChild(bar);
function mkBtn(t,fn,sm){var b=ce('button','wbtn',t);if(sm)b.setAttribute('data-smoke','1');b.addEventListener('click',fn);bar.appendChild(b);return b;}
mkBtn('بازی جدید',newGame,true);
mkBtn('واگرد',function(){if(L.undo(st)){render();hudUpd();}else{toast('چیزی برای واگرد نیست');}});
function render(){for(var i=1;i<=15;i++){var k=st.b.indexOf(i),r=(k/4)|0,c=k%4;
  tiles[i].style.left=(c*25)+'%';tiles[i].style.top=(r*25)+'%';}}
function hudUpd(){var b=store.get('wog-p15-best');
 hud('حرکت‌ها: '+fa(st.moves)+' | زمان: '+fa(secs)+' ثانیه'+(b?' | بهترین: '+fa(+b):''));}
function startT(){if(iv)return;iv=setInterval(function(){secs++;hudUpd();},1000);}
function stopT(){if(iv){clearInterval(iv);iv=null;}}
function trySlide(r,c){if(L.slide(st,r,c)){if(!started){started=true;startT();}
  render();hudUpd();if(L.isSolved(st))win();}}
function win(){stopT();var prev=+(store.get('wog-p15-best')||0);var nb=!prev||st.moves<prev;
 if(nb)store.set('wog-p15-best',String(st.moves));
 ovl('بردی!','پازل در '+fa(st.moves)+' حرکت و '+fa(secs)+' ثانیه حل شد'+(nb?' — رکورد جدید!':''),'بازی جدید',newGame);}
function newGame(){st=L.initial();L.shuffle(st,250,Math.random);secs=0;started=false;stopT();render();hudUpd();}
document.addEventListener('keydown',function(e){var bi=L.blank(st),r=(bi/4)|0,c=bi%4,m=null;
 if(e.code==='ArrowUp')m=[r-1,c];else if(e.code==='ArrowDown')m=[r+1,c];
 else if(e.code==='ArrowLeft')m=[r,c-1];else if(e.code==='ArrowRight')m=[r,c+1];
 if(m){e.preventDefault();trySlide(m[0],m[1]);}});
$('#hint').textContent='کاشیِ مجاور خانهٔ خالی را لمس کن؛ کلیدهای جهت‌نما خانهٔ خالی را حرکت می‌دهند. هدف: چیدن ۱ تا ۱۵ به ترتیب.';
newGame();
"""

P15_CSS = r"""
.p15board{position:relative;width:min(92vw,360px);height:min(92vw,360px);margin:10px auto;background:#0d1830;border:2px solid #d9a441;border-radius:14px;direction:ltr}
.p15tile{position:absolute;width:25%;height:25%;display:flex;align-items:center;justify-content:center;background:#3fb8af;color:#08111f;font-size:1.45rem;font-weight:700;border-radius:10px;cursor:pointer;transition:left .13s ease,top .13s ease;user-select:none;-webkit-user-select:none;box-shadow:inset 0 -3px 0 rgba(0,0,0,.28)}
.btnrow{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}
.wbtn{background:#d9a441;color:#08111f;border:none;border-radius:8px;padding:10px 18px;font-size:1rem;font-weight:700;min-height:44px;min-width:44px;cursor:pointer;touch-action:manipulation}
.wbtn:active{transform:scale(.96)}
"""

P15_TESTS = [
("حالت اولیه و تشخیص حل", """
var s0=L.initial();
T.eq(s0.b.length,16,'16 cells');T.eq(s0.b[0],1,'first tile');T.eq(s0.b[14],15,'tile 15');T.eq(s0.b[15],0,'blank');T.eq(L.blank(s0),15,'blank idx');
T.ok(L.isSolved(s0),'solved');
T.ok(!L.isSolved({b:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,0,15],moves:0,hist:[]}),'tail swap not solved');
"""),
("قانونیت اسلاید", """
var s=L.initial();
T.ok(L.slide(s,3,2),'15 slides');
T.eq(L.blank(s),14,'blank moved');T.eq(s.moves,1,'one move');T.eq(s.b[15],15,'tile at old blank');T.eq(s.b[14],0,'blank at 14');
T.ok(!L.slide(s,0,0),'far rejected');T.ok(!L.slide(s,3,0),'dist2 rejected');T.ok(!L.slide(s,2,1),'dist2b rejected');T.ok(!L.slide(s,3,2),'blank cell rejected');
T.eq(s.moves,1,'no move counted on reject');
T.ok(L.slide(s,2,2),'11 slides up');
T.eq(s.b[10],0,'blank at (2,2)');T.eq(s.b[14],11,'11 moved down');T.eq(s.moves,2,'two moves');
"""),
("وارونگی و پاریتی", """
T.eq(L.inversions([1,2,3]),0,'sorted');T.eq(L.inversions([3,2,1]),3,'reversed');T.eq(L.inversions([2,1,3]),1,'one inv');T.eq(L.inversions([1,3,2,4]),1,'one inv 4');T.eq(L.inversions([1,2,3,0]),0,'blank ignored');
T.ok(L.solvable(L.initial()),'solved solvable');
T.ok(!L.solvable({b:[1,2,3,4,5,6,7,8,9,10,11,12,13,15,14,0]}),'14-15 swap unsolvable');
T.ok(L.solvable({b:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,0,15]}),'one blank-up slide solvable');
"""),
("شافل ۲۵۰ حرکتی برای ۳۰ بذر همیشه حل‌پذیر", """
function permOK(b){var a=b.slice().sort(function(x,y){return x-y;});for(var i=0;i<16;i++)if(a[i]!==i)return false;return true;}
for(var i=0;i<30;i++){var s=L.initial();L.shuffle(s,250,rng);
 T.ok(permOK(s.b),'permutation seed '+i);
 T.ok(L.solvable(s),'solvable seed '+i);
 T.eq(s.moves,0,'moves reset seed '+i);T.eq(s.hist.length,0,'hist reset seed '+i);}
"""),
("پاریتی با دستیابی‌پذیری ۲×۲ برابر است", """
function sw(b,i,j){var a=b.slice(),t=a[i];a[i]=a[j];a[j]=t;return a;}
function nbrs(b){var z=b.indexOf(0),r=(z/2)|0,c=z%2,out=[];
 if(r>0)out.push(sw(b,z,z-2));if(r<1)out.push(sw(b,z,z+2));
 if(c>0)out.push(sw(b,z,z-1));if(c<1)out.push(sw(b,z,z+1));return out;}
var seen={'1,2,3,0':1},q=[[1,2,3,0]],cnt=1,i;
while(q.length){var cur=q.pop(),ns=nbrs(cur);
 for(i=0;i<ns.length;i++){var k=ns[i].join(',');
  if(seen[k])continue;seen[k]=1;cnt++;q.push(ns[i]);}}
T.eq(cnt,12,'exactly 12 reachable states of 2x2');
var perms=[[0,1,2,3],[0,1,3,2],[0,2,1,3],[0,2,3,1],[0,3,1,2],[0,3,2,1],[1,0,2,3],[1,0,3,2],[1,2,0,3],[1,2,3,0],[1,3,0,2],[1,3,2,0],[2,0,1,3],[2,0,3,1],[2,1,0,3],[2,1,3,0],[2,3,0,1],[2,3,1,0],[3,0,1,2],[3,0,2,1],[3,1,0,2],[3,1,2,0],[3,2,0,1],[3,2,1,0]];
var flagged=0;
for(i=0;i<24;i++){var p=perms[i],sv=L.solvable({b:p},2),inReach=!!seen[p.join(',')];
 if(inReach){T.ok(sv,'reachable must be solvable: '+p.join(','));}else{T.ok(!sv,'unreachable must be unsolvable: '+p.join(','));}
 if(sv)flagged++;}
T.eq(flagged,12,'parity flags exactly 12');
"""),
("واگرد وضعیت را کامل برمی‌گرداند", """
var s=L.initial(),snap=s.b.join(','),snapM=s.moves,sld=0,i;
for(i=0;i<6;i++){var bi=L.blank(s),r=(bi/4)|0,c=bi%4;
 if(r>0){if(L.slide(s,r-1,c))sld++;}else{if(L.slide(s,r+1,c))sld++;}}
T.eq(sld,6,'six slides done');T.eq(s.hist.length,6,'history grows');
for(i=0;i<6;i++)T.ok(L.undo(s),'undo '+i);
T.eq(s.b.join(','),snap,'board restored');T.eq(s.moves,snapM,'moves restored');
T.ok(!L.undo(s),'empty history rejected');
"""),
]

SOK_LOGIC = r"""
var WOG_LOGIC=(function(){
var LEVELS=[
["#######","#     #","# @$. #","#     #","#######"],
["#######","#  .  #","#  $  #","# @   #","#     #","#######"],
["########","#      #","# @$ . #","#    $ #","#  .   #","#      #","########"],
["########","#      #","# .$   #","#  @   #","#   $  #","#  .   #","#      #","########"],
["########","#  .   #","# @$   #","#  $.  #","# .$   #","#      #","########"],
["#########","#       #","# .   . #","#  $$$  #","#   @   #","#   .   #","#       #","#########"]
];
function parse(level){var h=level.length,w=0,i,j;
 for(i=0;i<h;i++)if(level[i].length>w)w=level[i].length;
 var walls=[],goals=[],boxes=[],p=-1;
 for(i=0;i<h;i++)for(j=0;j<w;j++){var ch=level[i].charAt(j),id=i*w+j;
  if(ch==='#')walls[id]=1;
  if(ch==='.'||ch==='*'||ch==='+')goals[id]=1;
  if(ch==='$'||ch==='*')boxes.push(id);
  if(ch==='@'||ch==='+')p=id;}
 boxes.sort(function(a,b){return a-b;});
 return{w:w,h:h,walls:walls,goals:goals,boxes:boxes,p:p,player:p,moves:0,hist:[]};}
function step(i,d,w,h){if(d!=='U'&&d!=='D'&&d!=='L'&&d!=='R')return -1;
 var r=(i/w)|0,c=i%w;
 if(d==='U')r--;else if(d==='D')r++;else if(d==='L')c--;else c++;
 if(r<0||r>=h||c<0||c>=w)return -1;return r*w+c;}
function bIdx(st,i){for(var k=0;k<st.boxes.length;k++)if(st.boxes[k]===i)return k;return -1;}
function move(st,d){var np=step(st.p,d,st.w,st.h);if(np<0||st.walls[np])return false;
 var bi=bIdx(st,np),nb=-1;
 if(bi>=0){nb=step(np,d,st.w,st.h);if(nb<0||st.walls[nb]||bIdx(st,nb)>=0)return false;}
 st.hist.push({p:st.p,boxes:st.boxes.slice(),moves:st.moves});
 if(bi>=0)st.boxes[bi]=nb;
 st.p=np;st.moves++;return true;}
function undo(st){if(!st.hist.length)return false;var h=st.hist.pop();st.p=h.p;st.boxes=h.boxes;st.moves=h.moves;return true;}
function isWin(st){for(var k=0;k<st.boxes.length;k++)if(!st.goals[st.boxes[k]])return false;return true;}
function boxesOnGoals(st){var n=0,k;for(k=0;k<st.boxes.length;k++)if(st.goals[st.boxes[k]])n++;return n;}
function solve(level){var base=level.w?level:parse(level);
 var w=base.w,h=base.h,walls=base.walls,goals=base.goals;
 function win(b){for(var k=0;k<b.length;k++)if(!goals[b[k]])return false;return true;}
 var start=base.boxes.slice();
 if(win(start))return 0;
 var seen={};seen[base.p+'|'+start.join(',')]=1;
 var q=[{p:base.p,b:start}],depth=0;
 while(q.length){var nq=[];depth++;
  for(var qi=0;qi<q.length;qi++){var cur=q[qi];
   for(var di=0;di<4;di++){var d='URDL'.charAt(di),np=step(cur.p,d,w,h);
    if(np<0||walls[np])continue;
    var nb=cur.b.slice(),bi=nb.indexOf(np);
    if(bi>=0){var nn=step(np,d,w,h);
     if(nn<0||walls[nn]||nb.indexOf(nn)>=0)continue;
     nb[bi]=nn;nb.sort(function(a,b){return a-b;});}
    var key=np+'|'+nb.join(',');
    if(seen[key])continue;seen[key]=1;
    if(win(nb))return depth;
    nq.push({p:np,b:nb});}}
  q=nq;}
 return -1;}
return{LEVELS:LEVELS,parse:parse,move:move,undo:undo,isWin:isWin,boxesOnGoals:boxesOnGoals,solve:solve,step:step};
})();
"""

SOK_UI = r"""
var li=0,st=null,iv=null,secs=0,started=false;
var app=$('#app'),bar=ce('div','btnrow');app.appendChild(bar);
var i;
for(i=0;i<L.LEVELS.length;i++)(function(i){var b=ce('button','wbtn wsm',fa(i+1));
 b.setAttribute('data-smoke','1');b.addEventListener('click',function(){load(i);});bar.appendChild(b);})(i);
var bar2=ce('div','btnrow');app.appendChild(bar2);
function mkBtn(t,fn,sm){var b=ce('button','wbtn',t);if(sm)b.setAttribute('data-smoke','1');b.addEventListener('click',fn);bar2.appendChild(b);return b;}
mkBtn('شروع دوباره',function(){load(li);},true);
mkBtn('واگرد',function(){if(L.undo(st)){render();hudUpd();}else{toast('چیزی برای واگرد نیست');}});
var board=ce('div','sokboard');app.appendChild(board);
function render(){board.innerHTML='';board.style.gridTemplateColumns='repeat('+st.w+',1fr)';
 for(var r=0;r<st.h;r++)for(var c=0;c<st.w;c++){var id=r*st.w+c,cl='scell';
  if(st.walls[id])cl='scell swall';
  else{if(st.goals[id])cl+=' sgoal';
   if(st.boxes.indexOf(id)>=0)cl+=st.goals[id]?' sboxon':' sbox';
   if(id===st.p)cl+=' splayer';}
  board.appendChild(ce('div',cl));}}
function hudUpd(){hud('مرحله: '+fa(li+1)+' | حرکت‌ها: '+fa(st.moves)+' | جعبه‌ها: '+fa(L.boxesOnGoals(st))+' از '+fa(st.boxes.length)+' | زمان: '+fa(secs)+' ثانیه');}
function startT(){if(iv)return;iv=setInterval(function(){secs++;hudUpd();},1000);}
function stopT(){if(iv){clearInterval(iv);iv=null;}}
function doMove(d){if(L.move(st,d)){if(!started){started=true;startT();}
 render();hudUpd();if(L.isWin(st))winL();}}
function load(i){li=i;st=L.parse(L.LEVELS[i]);secs=0;started=false;stopT();render();hudUpd();}
function winL(){stopT();var key='wog-sokoban-best-'+li,prev=+(store.get(key)||0),nb=!prev||st.moves<prev;
 if(nb)store.set(key,String(st.moves));
 ovl('بردی!','مرحلهٔ '+fa(li+1)+' در '+fa(st.moves)+' حرکت حل شد'+(nb?' — رکورد!':''),
  li<L.LEVELS.length-1?'مرحلهٔ بعد':'از اول',function(){load(li<L.LEVELS.length-1?li+1:li);});}
var pad=bindPad([{k:'ArrowUp',label:'▲'},{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'},{k:'ArrowDown',label:'▼'}]);
if(pad&&pad.nodeType&&!pad.parentNode)app.appendChild(pad);
function mapKey(code){return code==='ArrowUp'?'U':code==='ArrowDown'?'D':code==='ArrowLeft'?'L':code==='ArrowRight'?'R':null;}
document.addEventListener('keydown',function(e){var d=mapKey(e.code);if(d){e.preventDefault();doMove(d);}});
$('#hint').textContent='با فلش‌ها یا دکمه‌های لمسی حرکت کن؛ جعبه‌ها را روی دایره‌های طلایی هل بده. هل دادن ممکن است، کشیدن نه!';
load(0);
"""

SOK_CSS = r"""
.sokboard{display:grid;gap:2px;width:min(92vw,430px);margin:10px auto;direction:ltr;touch-action:manipulation}
.scell{aspect-ratio:1/1;background:#1b2a4a;border-radius:4px;position:relative}
.swall{background:#0d1830;border:1px solid #24365e}
.sgoal::after{content:'';position:absolute;top:30%;left:30%;right:30%;bottom:30%;border:2px solid #d9a441;border-radius:50%}
.sbox{background:#d9a441;box-shadow:inset 0 0 0 3px #a87a25}
.sboxon{background:#67b98a;box-shadow:inset 0 0 0 3px #3f8a63}
.splayer{background:#3fb8af;border-radius:50%;box-shadow:0 0 8px #3fb8af}
.btnrow{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}
.wbtn{background:#d9a441;color:#08111f;border:none;border-radius:8px;padding:10px 18px;font-size:1rem;font-weight:700;min-height:44px;min-width:44px;cursor:pointer;touch-action:manipulation}
.wbtn:active{transform:scale(.96)}
.wsm{min-width:44px;padding:10px 0}
"""

SOK_TESTS = [
("پارس درست هر ۶ مرحله", """
T.eq(L.LEVELS.length,6,'6 levels');
for(var i=0;i<6;i++){var lv=L.LEVELS[i],w=lv[0].length,boxes=0,goals=0,players=0;
 for(var r=0;r<lv.length;r++){T.eq(lv[r].length,w,'rect level '+i);
  for(var c=0;c<w;c++){var ch=lv[r].charAt(c);
   if(ch==='$'||ch==='*')boxes++;
   if(ch==='.'||ch==='*'||ch==='+')goals++;
   if(ch==='@'||ch==='+')players++;}}
 T.eq(boxes,goals,'boxes==goals level '+i);T.eq(players,1,'one player level '+i);
 var st=L.parse(lv);T.eq(st.boxes.length,boxes,'parsed boxes '+i);T.eq(st.w,w,'w '+i);T.eq(st.h,lv.length,'h '+i);T.ok(st.p>=0,'player '+i);}
"""),
("قانونیت هل دادن", """
var st=L.parse(['#####','#@$##','#   #','#####']);
T.ok(!L.move(st,'R'),'box into wall rejected');T.eq(st.p,6,'player unmoved');T.eq(st.boxes[0],7,'box unmoved');T.eq(st.hist.length,0,'no phantom history');
T.ok(L.move(st,'D'),'walk down');T.eq(st.p,11,'at (2,1)');
T.ok(L.move(st,'U'),'walk back');T.eq(st.p,6,'at (1,1)');
T.ok(!L.move(st,'U'),'wall above rejected');T.eq(st.p,6,'still there');
T.ok(!L.move(st,'X'),'bad dir rejected');
var s2=L.parse(['#######','#@$ $ #','#     #','#######']);
T.ok(L.move(s2,'R'),'first push');T.eq(s2.boxes[0],10,'box to col3');T.eq(s2.p,9,'player follows');
T.ok(!L.move(s2,'R'),'box into box rejected');T.eq(s2.boxes[0],10,'box1 same');T.eq(s2.boxes[1],11,'box2 same');
"""),
("تشخیص برد", """
var done=L.parse(['#####','#@* #','#####']);T.ok(L.isWin(done),'pre-solved wins');
T.eq(L.boxesOnGoals(done),1,'one on goal');
var st=L.parse(L.LEVELS[0]);T.ok(!L.isWin(st),'not yet');
T.ok(L.move(st,'R'),'push to goal');T.ok(L.isWin(st),'win');T.eq(st.boxes[0],18,'box on (2,4)');
"""),
("واگرد دقیق", """
var st=L.parse(L.LEVELS[2]);
var snap=JSON.stringify([st.p,st.boxes,st.moves]);
var seq=['R','R','D','L','U'],doneN=0,i;
for(i=0;i<seq.length;i++)if(L.move(st,seq[i]))doneN++;
T.ok(doneN>=2,'some moves happened: '+doneN);
for(i=0;i<doneN;i++)T.ok(L.undo(st),'undo '+i);
T.eq(JSON.stringify([st.p,st.boxes,st.moves]),snap,'exact restore');
T.ok(!L.undo(st),'no more undos');
"""),
("BFS هر ۶ مرحله را حل‌پذیر اثبات می‌کند", """
var lens=[],i;
for(i=0;i<6;i++){var n=L.solve(L.LEVELS[i]);T.ok(n>0,'level '+i+' solvable');lens.push(n);}
T.eq(lens[0],1,'level 1 is exactly one push');
for(i=0;i<6;i++)T.ok(lens[i]<500,'sane length '+i);
"""),
("BFS حالت‌های مرزی", """
T.eq(L.solve(['#####','#@* #','#####']),0,'already solved = 0');
T.eq(L.solve(['#####','#@$#.','#####']),-1,'walled-off box unsolvable');
var s5=L.parse(L.LEVELS[0]);T.ok(L.move(s5,'R'),'push');T.ok(L.isWin(s5),'win');
T.ok(L.undo(s5),'undo');T.eq(s5.boxes[0],17,'box restored');T.ok(!L.isWin(s5),'undo clears win');
"""),
]

RUSH_LOGIC = r"""
var WOG_LOGIC=(function(){
var LEVELS=[
["......","......","AA..B.","....B.","....B.","......"],
["..B...","..B...","AA.C..","...C..","......","......"],
["......",".BB...","AA.C..","...C..","..DD..","......"],
[".BB...","....C.","AA.FC.","...FC.","......","......"],
["E.....","E..B..","AA.B..","...BCC","..F...","..F..."],
["..BB..","....C.","AA.C..","..D.C.","..DEE.","......"],
["C.....","C..DD.","AA..E.","..FFE.","..G.H.","..G.H."],
[".BB.D.","....D.","AA.C..","FF.C..","...CEE","......"]
];
function parse(grid){var veh={},order=[],r,c,ch;
 for(r=0;r<6;r++)for(c=0;c<6;c++){ch=grid[r].charAt(c);
  if(ch==='.'||ch==='')continue;
  if(!veh[ch]){veh[ch]={id:ch,r:r,c:c,len:1,horiz:(c<5&&grid[r].charAt(c+1)===ch)};order.push(ch);}
  else veh[ch].len++;}
 return{w:6,h:6,veh:veh,vehicles:veh,order:order,moves:0};}
function vehAt(st,r,c){var i,v;
 for(i=0;i<st.order.length;i++){v=st.veh[st.order[i]];
  if(v.horiz){if(v.r===r&&c>=v.c&&c<v.c+v.len)return v;}
  else if(v.c===c&&r>=v.r&&r<v.r+v.len)return v;}
 return null;}
function canMove(st,id,d,steps){var v=st.veh[id];if(!v||!(steps>0))return false;
 var dr=0,dc=0;
 if(d==='L')dc=-1;else if(d==='R')dc=1;else if(d==='U')dr=-1;else if(d==='D')dr=1;else return false;
 if(v.horiz?dr!==0:dc!==0)return false;
 var s,lr,lc,o;
 for(s=1;s<=steps;s++){
  if(dc<0){lr=v.r;lc=v.c-s;}else if(dc>0){lr=v.r;lc=v.c+v.len-1+s;}
  else if(dr<0){lr=v.r-s;lc=v.c;}else{lr=v.r+v.len-1+s;lc=v.c;}
  if(lr<0||lr>=st.h||lc<0||lc>=st.w)return false;
  o=vehAt(st,lr,lc);if(o&&o.id!==id)return false;}
 return true;}
function move(st,id,d,steps){steps=steps||1;
 if(!canMove(st,id,d,steps))return false;
 var v=st.veh[id];
 if(d==='L')v.c-=steps;else if(d==='R')v.c+=steps;else if(d==='U')v.r-=steps;else v.r+=steps;
 st.moves++;return true;}
function isWin(st){var a=st.veh.A;if(!a||!a.horiz||a.r!==2)return false;return a.c+a.len-1===st.w-1;}
function solve(st){var base=(st&&st.order)?st:parse(st);
 var ids=base.order,veh=[],i;
 for(i=0;i<ids.length;i++){var v0=base.veh[ids[i]];veh.push({horiz:v0.horiz,len:v0.len});}
 var ai=ids.indexOf('A');
 function winPos(pos){if(ai<0)return false;var p=pos[ai],r=(p/6)|0,c=p%6;
  return veh[ai].horiz&&r===2&&c+veh[ai].len-1===5;}
 var start=[];
 for(i=0;i<ids.length;i++)start.push(base.veh[ids[i]].r*6+base.veh[ids[i]].c);
 if(winPos(start))return 0;
 var seen={},q=[start],depth=0;seen[start.join(',')]=1;
 while(q.length){var nq=[];depth++;
  for(var qi=0;qi<q.length;qi++){var pos=q[qi];
   var occ=[],z;for(z=0;z<36;z++)occ[z]=false;
   for(var j=0;j<ids.length;j++){var p2=pos[j],r2=(p2/6)|0,c2=p2%6,v2=veh[j];
    for(var k2=0;k2<v2.len;k2++){if(v2.horiz)occ[r2*6+c2+k2]=true;else occ[(r2+k2)*6+c2]=true;}}
   for(var j2=0;j2<ids.length;j2++){var v3=veh[j2],p3=pos[j2],r3=(p3/6)|0,c3=p3%6;
    var dd=v3.horiz?[[0,-1],[0,1]]:[[-1,0],[1,0]];
    for(var di=0;di<2;di++){var dr=dd[di][0],dc=dd[di][1];
     for(var s=1;s<=5;s++){var lr2,lc2;
      if(dc<0){lr2=r3;lc2=c3-s;}else if(dc>0){lr2=r3;lc2=c3+v3.len-1+s;}
      else if(dr<0){lr2=r3-s;lc2=c3;}else{lr2=r3+v3.len-1+s;lc2=c3;}
      if(lr2<0||lr2>5||lc2<0||lc2>5)break;
      if(occ[lr2*6+lc2])break;
      var np=pos.slice();np[j2]=(r3+dr*s)*6+(c3+dc*s);
      var key=np.join(',');
      if(!seen[key]){seen[key]=1;
       if(winPos(np))return depth;
       nq.push(np);}}}}}
  q=nq;}
 return -1;}
return{LEVELS:LEVELS,parse:parse,vehAt:vehAt,canMove:canMove,move:move,isWin:isWin,solve:solve};
})();
"""

RUSH_UI = r"""
var li=0,st=null,sel=null,iv=null,secs=0,started=false,vEls={};
var app=$('#app'),wrap=ce('div','rhwrap');app.appendChild(wrap);
var bar=ce('div','btnrow');wrap.appendChild(bar);
var i;
for(i=0;i<L.LEVELS.length;i++)(function(i){var b=ce('button','wbtn wsm',fa(i+1));
 b.setAttribute('data-smoke','1');b.addEventListener('click',function(){load(i);});bar.appendChild(b);})(i);
var bar2=ce('div','btnrow');wrap.appendChild(bar2);
function mkBtn(t,fn){var b=ce('button','wbtn',t);b.setAttribute('data-smoke','1');b.addEventListener('click',fn);bar2.appendChild(b);return b;}
mkBtn('بازی جدید',function(){load(li);});
var board=ce('div','rhboard');wrap.appendChild(board);
var grid=ce('div','rhgrid');board.appendChild(grid);
for(var z=0;z<36;z++)grid.appendChild(ce('div','rhcell'));
var exitM=ce('div','rhexit');board.appendChild(exitM);
var vehLayer=ce('div','rhlayer');board.appendChild(vehLayer);
function buildVehs(){vehLayer.innerHTML='';vEls={};
 for(var k=0;k<st.order.length;k++)(function(id){var el=ce('div','rhveh',id);
  el.addEventListener('click',function(){sel=(sel===id?null:id);render();});
  vehLayer.appendChild(el);vEls[id]=el;})(st.order[k]);}
function render(){for(var k=0;k<st.order.length;k++){var id=st.order[k],v=st.veh[id],el=vEls[id];
  el.style.left=(v.c*100/6)+'%';el.style.top=(v.r*100/6)+'%';
  el.style.width=(v.len*100/6)+'%';el.style.height=(100/6)+'%';
  el.className='rhveh'+(id==='A'?' rhred':'')+(sel===id?' rhsel':'');}}
function hudUpd(){hud('مرحله: '+fa(li+1)+' | حرکت‌ها: '+fa(st.moves)+' | زمان: '+fa(secs)+' ثانیه');}
function startT(){if(iv)return;iv=setInterval(function(){secs++;hudUpd();},1000);}
function stopT(){if(iv){clearInterval(iv);iv=null;}}
function go(d){if(!sel){toast('اول یک خودرو را لمس کن');return;}
 if(L.move(st,sel,d,1)){if(!started){started=true;startT();}
  render();hudUpd();if(L.isWin(st))winL();}
 else toast('حرکت ممکن نیست');}
function load(k){li=k;st=L.parse(L.LEVELS[k]);sel=null;secs=0;started=false;stopT();buildVehs();render();hudUpd();}
function winL(){stopT();var key='wog-rush-hour-best-'+li,prev=+(store.get(key)||0),nb=!prev||st.moves<prev;
 if(nb)store.set(key,String(st.moves));
 ovl('بردی!','ماشین قرمز در '+fa(st.moves)+' حرکت خارج شد'+(nb?' — رکورد!':''),
  li<L.LEVELS.length-1?'مرحلهٔ بعد':'از اول',function(){load(li<L.LEVELS.length-1?li+1:li);});}
var arrows=ce('div','btnrow');wrap.appendChild(arrows);
[['◀','L'],['▲','U'],['▼','D'],['▶','R']].forEach(function(a){
 var b=ce('button','wbtn',a[0]);b.addEventListener('click',function(){go(a[1]);});arrows.appendChild(b);});
document.addEventListener('keydown',function(e){
 var d=e.code==='ArrowLeft'?'L':e.code==='ArrowRight'?'R':e.code==='ArrowUp'?'U':e.code==='ArrowDown'?'D':null;
 if(d){e.preventDefault();go(d);}});
$('#hint').textContent='یک خودرو را لمس کن تا انتخاب شود، سپس با فلش‌ها لغزش بده. ماشین قرمز باید تا لبهٔ راستِ ردیف سوم برسد.';
load(0);
"""

RUSH_CSS = r"""
.rhboard{position:relative;width:min(92vw,360px);height:min(92vw,360px);margin:10px auto;background:#0d1830;border:2px solid #d9a441;border-radius:14px;direction:ltr;overflow:hidden}
.rhgrid{position:absolute;top:0;left:0;width:100%;height:100%;display:grid;grid-template-columns:repeat(6,1fr);grid-template-rows:repeat(6,1fr)}
.rhcell{border:1px solid #1b2a4a}
.rhlayer{position:absolute;top:0;left:0;width:100%;height:100%}
.rhveh{position:absolute;display:flex;align-items:center;justify-content:center;background:#3fb8af;color:#08111f;font-weight:700;font-size:1.1rem;border-radius:8px;box-sizing:border-box;border:2px solid #0b1830;cursor:pointer;transition:left .14s ease,top .14s ease;user-select:none;-webkit-user-select:none}
.rhred{background:#e26d5c;color:#2a0f0a}
.rhsel{outline:3px solid #d9a441;outline-offset:-3px;z-index:2}
.rhexit{position:absolute;top:33.333%;right:-2px;width:6px;height:16.666%;background:#67b98a}
.btnrow{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}
.wbtn{background:#d9a441;color:#08111f;border:none;border-radius:8px;padding:10px 18px;font-size:1rem;font-weight:700;min-height:44px;min-width:44px;cursor:pointer;touch-action:manipulation}
.wbtn:active{transform:scale(.96)}
.wsm{min-width:44px;padding:10px 0}
"""

RUSH_TESTS = [
("پارس و صحت هر ۸ نقشه", """
T.eq(L.LEVELS.length,8,'8 levels');
for(var i=0;i<8;i++){var g=L.LEVELS[i];T.eq(g.length,6,'6 rows '+i);
 for(var j=0;j<6;j++)T.eq(g[j].length,6,'6 cols '+i+' row '+j);
 var st=L.parse(g);
 T.ok(st.veh.A,'red car exists '+i);T.ok(st.veh.A.horiz,'red horizontal '+i);T.eq(st.veh.A.r,2,'red on row 2 '+i);
 T.ok(st.order.length>=2,'enough vehicles '+i);
 var occ={},cells=0;
 for(var k=0;k<st.order.length;k++){var v=st.veh[st.order[k]];
  T.ok(v.len>=2&&v.len<=3,'len 2-3 '+i);
  for(var s=0;s<v.len;s++){var key=v.horiz?(v.r*6+v.c+s):((v.r+s)*6+v.c);
   T.ok(!occ[key],'no overlap '+i);occ[key]=1;cells++;}}
 T.eq(cells,Object.keys(occ).length,'cells consistent '+i);}
"""),
("قانونیت لغزش", """
var st=L.parse(['......','......','AABB..','......','......','......']);
T.ok(!L.canMove(st,'A','R',1),'car blocks car');T.eq(st.veh.A.c,0,'A unmoved');
T.ok(!L.canMove(st,'B','L',1),'B blocked by A');
T.ok(!L.canMove(st,'A','U',1),'wrong axis rejected');
T.ok(!L.canMove(st,'A','R',0),'zero steps rejected');
T.ok(!L.canMove(st,'Z','R',1),'unknown id rejected');
T.ok(L.canMove(st,'B','R',2),'B free to slide 2');
T.ok(L.move(st,'B','R',2),'B slides');T.eq(st.veh.B.c,4,'B at col4');
T.ok(!L.canMove(st,'B','R',1),'B out of bounds rejected');
"""),
("تشخیص برد", """
T.ok(L.isWin(L.parse(['......','......','....AA','......','......','......'])),'right end at col5 wins');
T.ok(!L.isWin(L.parse(['......','......','...AA.','......','......','......'])),'not at edge');
T.ok(!L.isWin(L.parse(['......','....AA','......','......','......','......'])),'wrong row');
var st=L.parse(L.LEVELS[0]);T.ok(!L.isWin(st),'not yet');
T.ok(L.move(st,'B','D',1),'truck slides down');T.ok(L.move(st,'A','R',4),'red exits');
T.ok(L.isWin(st),'win');T.eq(st.moves,2,'two moves');
"""),
("BFS حل‌پذیری هر ۸ مرحله را اثبات می‌کند", """
for(var i=0;i<8;i++){var n=L.solve(L.parse(L.LEVELS[i]));
 T.ok(n>0,'level '+i+' solvable');T.ok(n<60,'sane min '+i);}
T.eq(L.solve(L.parse(['......','......','....AA','......','......','......'])),0,'already won = 0');
"""),
("شمارندهٔ حرکت", """
var st=L.parse(L.LEVELS[0]);T.eq(st.moves,0,'start 0');
T.ok(L.move(st,'A','R',1),'r1');T.eq(st.moves,1,'1');
T.ok(L.move(st,'A','L',1),'back');T.eq(st.moves,2,'2');T.eq(st.veh.A.c,0,'A home');
T.ok(!L.move(st,'A','U',1),'axis fail');T.eq(st.moves,2,'unchanged');
T.ok(!L.move(st,'A','R',9),'too far');T.eq(st.moves,2,'unchanged2');
T.ok(L.move(st,'B','U',1),'truck up');T.eq(st.moves,3,'3');T.eq(st.veh.B.r,1,'truck row1');
"""),
("سازگاری اشغال پس از بازی کامل", """
var st=L.parse(L.LEVELS[0]);
var seq=[['B','D',1],['A','R',1],['A','L',1],['A','R',4]],i;
for(i=0;i<seq.length;i++)T.ok(L.move(st,seq[i][0],seq[i][1],seq[i][2]),'step '+i);
T.ok(L.isWin(st),'won');
var seen={},cnt=0;
for(i=0;i<st.order.length;i++){var v=st.veh[st.order[i]];
 for(var s=0;s<v.len;s++){var key=v.horiz?(v.r*6+v.c+s):((v.r+s)*6+v.c);
  if(!seen[key]){seen[key]=1;cnt++;}}}
T.eq(cnt,5,'exactly 5 occupied cells (2+3)');
"""),
]

p15 = G(slug="p15", title="پازل ۱۵", cat="puzzle", icon="🧩", g1="#d9a441", g2="#3fb8af",
    desc="پازل کلاسیک ۱۵ روی شبکهٔ ۴×۴: کاشی‌ها را هل بده تا اعداد ۱ تا ۱۵ مرتب شوند. هر شافل با ۲۵۰ حرکت معتبر از حالت حل‌شده ساخته می‌شود و تضمیناً حل‌پذیر است.",
    hint="کاشی مجاور خانهٔ خالی را لمس کن یا با کلیدهای جهت‌نما خانهٔ خالی را حرکت بده؛ دکمهٔ واگرد آخرین حرکت را پس می‌گیرد.",
    logic=P15_LOGIC, ui=P15_UI, css=P15_CSS, engines=("common",), tests=P15_TESTS)

sokoban = G(slug="sokoban", title="سوکوبان", cat="puzzle", icon="📦", g1="#d9a441", g2="#3fb8af",
    desc="۶ مرحلهٔ دست‌ساز سوکوبان: جعبه‌ها را فقط هل بده (هیچ کشیدنی در کار نیست) و همه را روی اهداف بگذار. حل‌پذیری همهٔ مرحله‌ها با جست‌وجوی BFS اثبات شده است.",
    hint="با فلش‌ها یا دکمه‌های لمسی حرکت کن؛ جعبه در گوشه گیر می‌افتد، پس قبل از هل دادن مسیر برگشت را چک کن.",
    logic=SOK_LOGIC, ui=SOK_UI, css=SOK_CSS, engines=("common","arcade"), tests=SOK_TESTS)

rush = G(slug="rush-hour", title="ترافیک", cat="puzzle", icon="🚗", g1="#d9a441", g2="#3fb8af",
    desc="ترافیک ۶×۶ با ۸ نقشهٔ دست‌ساز: خودروها را روی محور خودشان لغزش بده تا ماشین قرمز از لبهٔ راست ردیف سوم خارج شود. حداقل حرکت هر نقشه با BFS محاسبه شده است.",
    hint="اول یک خودرو را لمس کن تا انتخاب شود، بعد با فلش‌ها یکی‌یکی لغزش بده؛ ماشین قرمز باید به لبهٔ راست ردیف سوم برسد.",
    logic=RUSH_LOGIC, ui=RUSH_UI, css=RUSH_CSS, engines=("common",), tests=RUSH_TESTS)

GAMES = [p15, sokoban, rush]
