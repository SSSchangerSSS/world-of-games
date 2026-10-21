# -*- coding: utf-8 -*-
"""AG-C1 - board games batch (kit: lib_mini): checkers, gomoku, connect4. All cat="board", engines=("common",)."""
from lib_mini import G

# ============================================================ CHECKERS
CHECKERS_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
function cloneB(b){var n=[],r,c;for(r=0;r<8;r++){n.push([]);for(c=0;c<8;c++)n[r].push(b[r][c]);}return n;}
function initial(){var b=[],r,c;for(r=0;r<8;r++){b.push([]);for(c=0;c<8;c++){if((r+c)%2===1){if(r<3)b[r].push(-1);else if(r>4)b[r].push(1);else b[r].push(0);}else b[r].push(0);}}return {b:b,q:0};}
function inB(r,c){return r>=0&&r<8&&c>=0&&c<8;}
function dirsOf(v){var k=Math.abs(v)===2;if(k)return [[1,-1],[1,1],[-1,-1],[-1,1]];return v>0?[[-1,-1],[-1,1]]:[[1,-1],[1,1]];}
function slidesFrom(b,r,c){var ds=dirsOf(b[r][c]),out=[],i,d,nr,nc;for(i=0;i<ds.length;i++){d=ds[i];nr=r+d[0];nc=c+d[1];if(inB(nr,nc)&&b[nr][nc]===0)out.push([nr,nc]);}return out;}
function capSeqs(b,r,c,block){
  var v=b[r][c],ds=dirsOf(v),res=[],i,d,nr,nc,mr,mc,sub,j,k,used,nb;
  for(i=0;i<ds.length;i++){
    d=ds[i];nr=r+2*d[0];nc=c+2*d[1];mr=r+d[0];mc=c+d[1];
    if(!inB(nr,nc)||b[nr][nc]!==0)continue;
    if(b[mr][mc]===0||(b[mr][mc]>0)===(v>0))continue;
    used=false;for(k=0;k<block.length;k++)if(block[k][0]===mr&&block[k][1]===mc)used=true;
    if(used)continue;
    nb=cloneB(b);nb[r][c]=0;nb[nr][nc]=v;
    sub=capSeqs(nb,nr,nc,block.concat([[mr,mc]]));
    if(!sub.length)res.push({path:[[nr,nc]]});
    else for(j=0;j<sub.length;j++)res.push({path:[[nr,nc]].concat(sub[j].path)});
  }
  return res;
}
function legalMoves(st,pl){
  var b=st.b,caps=[],slides=[],r,c,i,v,cs,ss;
  for(r=0;r<8;r++)for(c=0;c<8;c++){
    v=b[r][c];if(v===0||(v>0)!==(pl>0))continue;
    cs=capSeqs(b,r,c,[]);
    for(i=0;i<cs.length;i++)caps.push({from:[r,c],path:cs[i].path});
    ss=slidesFrom(b,r,c);
    for(i=0;i<ss.length;i++)slides.push({from:[r,c],path:[ss[i]]});
  }
  return caps.length?caps:slides;
}
function isCaptureMove(mv){var sq=[mv.from].concat(mv.path),i;for(i=1;i<sq.length;i++)if(Math.abs(sq[i][0]-sq[i-1][0])===2)return true;return false;}
function applyMove(st,mv){
  var b=st.b,r=mv.from[0],c=mv.from[1],v=b[r][c],i,p;
  b[r][c]=0;
  for(i=0;i<mv.path.length;i++){p=mv.path[i];
    if(Math.abs(p[0]-r)===2)b[(p[0]+r)/2][(p[1]+c)/2]=0;
    r=p[0];c=p[1];}
  b[r][c]=v;
  if(v===1&&r===0)b[r][c]=2;else if(v===-1&&r===7)b[r][c]=-2;
  if(isCaptureMove(mv)||v===1||v===-1)st.q=0;else st.q=(st.q||0)+1;
  return st;
}
function winner(st){
  var b=st.b,p1=0,p2=0,r,c;
  for(r=0;r<8;r++)for(c=0;c<8;c++){if(b[r][c]>0)p1++;else if(b[r][c]<0)p2++;}
  if(p2===0)return 1;
  if(p1===0)return -1;
  if(legalMoves(st,1).length===0)return -1;
  if(legalMoves(st,-1).length===0)return 1;
  if((st.q||0)>=80)return 'draw';
  return 0;
}
function evaluate(st){
  var b=st.b,s=0,r,c,v;
  for(r=0;r<8;r++)for(c=0;c<8;c++){v=b[r][c];if(!v)continue;
    if(v>0){s+=(v===2?170:100);if(v===1){s+=(7-r)*4;if(r===7)s+=10;}if(c===0||c===7)s+=3;}
    else{s-=(v===-2?170:100);if(v===-1){s-=r*4;if(r===0)s-=10;}if(c===0||c===7)s-=3;}}
  return s;
}
function clone(st){return {b:cloneB(st.b),q:st.q};}
function negamax(st,depth,a,bta,pl){
  if(depth<=0)return pl>0?evaluate(st):-evaluate(st);
  var ms=legalMoves(st,pl),i,ns,sc,best=-1e9;
  if(!ms.length)return -99999-depth;
  for(i=0;i<ms.length;i++){
    ns=clone(st);applyMove(ns,ms[i]);
    sc=-negamax(ns,depth-1,-bta,-a,-pl);
    if(sc>best)best=sc;
    if(best>a)a=best;
    if(a>=bta)break;
  }
  return best;
}
function aiMove(st,rng,depth,pl){
  if(pl===undefined)pl=-1;
  var d=depth||4,ms=legalMoves(st,pl),i,ns,sc,best=-1e9,cand=[];
  if(!ms.length)return null;
  for(i=0;i<ms.length;i++){
    ns=clone(st);applyMove(ns,ms[i]);
    sc=-negamax(ns,d-1,-1e9,1e9,-pl);
    if(sc>best+0.5){best=sc;cand=[ms[i]];}
    else if(sc>best-0.5){cand.push(ms[i]);if(sc>best)best=sc;}
  }
  if(cand.length>1&&rng)return cand[Math.floor(rng()*cand.length)%cand.length];
  return cand[0];
}
return {initial:initial,legalMoves:legalMoves,applyMove:applyMove,isCaptureMove:isCaptureMove,winner:winner,aiMove:aiMove,evaluate:evaluate};
})();
"""

CHECKERS_UI = r"""
var st=L.initial(),sel=null,hm=[],turn=1,over=false,busy=false,last=null,cb;
function movesFrom(rc){var out=[],i;for(i=0;i<hm.length;i++)if(hm[i].from[0]===rc[0]&&hm[i].from[1]===rc[1])out.push(hm[i]);return out;}
function cnt(p){var n=0,r,c,x;for(r=0;r<8;r++)for(c=0;c<8;c++){x=st.b[r][c];if(p>0?x>0:x<0)n++;}return n;}
function render(){
  var dst={},i,ms=sel?movesFrom(sel):[];
  for(i=0;i<ms.length;i++){var f=ms[i].path[ms[i].path.length-1];dst[f[0]+'_'+f[1]]=1;}
  var h='';
  for(var r=0;r<8;r++)for(var c=0;c<8;c++){
    var v=st.b[r][c],cls='sq '+((r+c)%2===0?'lt':'dk'),inner='';
    if(sel&&sel[0]===r&&sel[1]===c)cls+=' sel';
    if(dst[r+'_'+c])cls+=' dst';
    if(last&&((last.from[0]===r&&last.from[1]===c)||(last.path[last.path.length-1][0]===r&&last.path[last.path.length-1][1]===c)))cls+=' lmv';
    if(v)inner='<div class="pc '+(v>0?'p1':'p2')+(Math.abs(v)===2?' kg':'')+'">'+(Math.abs(v)===2?'\u265B':'')+'</div>';
    h+='<div class="'+cls+'" data-r="'+r+'" data-c="'+c+'">'+inner+'</div>';
  }
  cb.innerHTML=h;
  document.getElementById('sc').innerHTML='شما '+fa(cnt(1))+' — ربات '+fa(cnt(-1));
}
function endGame(w){
  over=true;hm=[];sel=null;render();
  if(w===1)ovl('بردی!','همهٔ مهره‌های ربات از بین رفتند.','بازی جدید',newGame);
  else if(w===-1)ovl('باختی!','مهره‌های شما تمام شد یا حرکتی ندارید.','بازی جدید',newGame);
  else ovl('مساوی','چهل حرکت پیاپی بدون گرفتن یا پیشرویِ مرد انجام شد.','بازی جدید',newGame);
}
function newGame(){
  st=L.initial();sel=null;turn=1;over=false;busy=false;last=null;
  hm=L.legalMoves(st,1);render();hud('نوبت شما — مهره‌های طلایی');
}
function boardClick(e){
  if(over||busy||turn!==1)return;
  var el=e.target;
  while(el&&el!==cb&&!(el.getAttribute&&el.getAttribute('data-r')))el=el.parentNode;
  if(!el||el===cb)return;
  var r=+el.getAttribute('data-r'),c=+el.getAttribute('data-c'),v=st.b[r][c];
  if(sel){
    var ms=movesFrom(sel),mv=null,i;
    for(i=0;i<ms.length;i++){var f=ms[i].path[ms[i].path.length-1];if(f[0]===r&&f[1]===c){mv=ms[i];break;}}
    if(mv){
      L.applyMove(st,mv);last=mv;sel=null;turn=-1;busy=true;render();hud('نوبت ربات…');
      var w=L.winner(st);
      if(w!==0){busy=false;endGame(w);return;}
      setTimeout(function(){
        var am=L.aiMove(st,Math.random,4);
        if(am){L.applyMove(st,am);last=am;}
        busy=false;turn=1;hm=L.legalMoves(st,1);render();
        var w2=L.winner(st);
        if(w2!==0){endGame(w2);return;}
        hud('نوبت شما');
      },560);
      return;
    }
  }
  if(v>0){
    var ms2=movesFrom([r,c]);
    if(ms2.length){sel=[r,c];render();hud('خانهٔ مقصد را بزنید');}
    else{sel=null;render();hud('این مهره در حال حاضر حرکت مجازی ندارد');}
  }else{
    sel=null;render();hud('نوبت شما — یکی از مهره‌های طلایی را بزنید');
  }
}
var app=$('#app');
app.innerHTML='<div id="cbw"><div id="cb" dir="ltr"></div></div><div id="tools"><button id="ng" class="btn gold" data-smoke>بازی جدید</button><span id="sc"></span></div>';
cb=document.getElementById('cb');
cb.onclick=boardClick;
$('#ng').onclick=newGame;
newGame();
$('#hint').textContent='مهرهٔ طلایی‌تان را انتخاب و سپس خانهٔ مقصد را بزنید؛ پرشِ گرفتن اجباری است و مردی که به ردیف آخر برسد شاه می‌شود.';
"""

CHECKERS_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0d1526;color:#e8e4d8;font-family:Vazirmatn,Tahoma,sans-serif;text-align:center}
.wog-home{display:inline-block;margin:8px 14px 0;color:#3fb8af;text-decoration:none;font-size:.9em}
header{padding:6px 12px 0}
h1{margin:2px 0;color:#d9a441;font-size:1.3em}
#hud{color:#9fb0d0;min-height:1.4em}
#cbw{display:flex;justify-content:center;padding:10px 6px 4px}
#cb{display:grid;grid-template-columns:repeat(8,1fr);width:min(94vw,460px);height:min(94vw,460px);border-radius:10px;overflow:hidden;box-shadow:0 8px 22px rgba(0,0,0,.45);touch-action:manipulation;cursor:pointer}
.sq{position:relative;display:flex;align-items:center;justify-content:center}
.lt{background:#33456e}.dk{background:#1b2846}
.sq.sel{box-shadow:inset 0 0 0 3px #d9a441}
.sq.dst::after{content:'';position:absolute;width:32%;height:32%;border-radius:50%;background:#3fb8af;box-shadow:0 0 10px #3fb8af}
.sq.lmv{box-shadow:inset 0 0 0 3px rgba(63,184,175,.8)}
.pc{width:76%;height:76%;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;box-shadow:0 3px 7px rgba(0,0,0,.55);border:2px solid rgba(255,255,255,.16)}
.p1{background:radial-gradient(circle at 35% 30%,#f4d491,#d9a441 62%,#9c7420);color:#6b4a00}
.p2{background:radial-gradient(circle at 35% 30%,#8fdcd5,#3fb8af 62%,#1e756f);color:#093d39}
.kg{font-size:min(5vw,22px)}
#tools{display:flex;gap:10px;justify-content:center;align-items:center;padding:10px;flex-wrap:wrap}
.btn{min-height:44px;min-width:110px;border:0;border-radius:10px;font-family:inherit;font-size:1em;cursor:pointer;background:#1b2846;color:#e8e4d8;touch-action:manipulation}
.btn.gold{background:#d9a441;color:#231803;font-weight:700}
#sc{color:#9fb0d0}
#hint{color:#9fb0d0;padding:0 16px;line-height:1.9}
"""

CHECKERS_TESTS = [
("چیدمان اولیه و ۷ حرکت مجاز",
 r"""var st=L.initial(),mv=L.legalMoves(st,1),i,p1=0,p2=0,r,c;
for(r=0;r<8;r++)for(c=0;c<8;c++){if(st.b[r][c]>0)p1++;if(st.b[r][c]<0)p2++;}
T.eq(p1,12,'۱۲ مهرهٔ انسان');T.eq(p2,12,'۱۲ مهرهٔ ربات');
T.eq(mv.length,7,'۷ حرکت آغازین');
for(i=0;i<mv.length;i++){T.eq(mv[i].from[0],5,'از ردیف ۵');T.eq(mv[i].path[0][0],4,'به ردیف ۴');T.ok(!L.isCaptureMove(mv[i]),'بدون پرش');}
T.eq(L.winner(st),0,'بازی در جریان است');"""),
("پرش اجباری — حرکت ساده کنار گذاشته می‌شود",
 r"""var b=[],r,c;for(r=0;r<8;r++){b.push([]);for(c=0;c<8;c++)b[r].push(0);}
b[5][2]=1;b[6][5]=1;b[4][3]=-1;
var st={b:b,q:0},mv=L.legalMoves(st,1);
T.eq(mv.length,1,'فقط یک پرش مجاز مانده');
T.ok(L.isCaptureMove(mv[0]),'پرش است');
T.eq(mv[0].path,[[3,4]],'مقصد پرش');
L.applyMove(st,mv[0]);
T.eq(st.b[3][4],1,'فرود');T.eq(st.b[4][3],0,'مهرهٔ ربات گرفته شد');T.eq(st.b[5][2],0,'مبدأ خالی');T.eq(st.b[6][5],1,'مهرهٔ دیگر دست‌نخورده');"""),
("ادامهٔ پرش چندگانه با همان مهره اجباری است",
 r"""var b=[],r,c;for(r=0;r<8;r++){b.push([]);for(c=0;c<8;c++)b[r].push(0);}
b[5][2]=1;b[4][3]=-1;b[2][3]=-1;b[6][6]=1;
var st={b:b,q:0},mv=L.legalMoves(st,1);
T.eq(mv.length,1,'توقف بعد از پرش اول مجاز نیست');
T.eq(mv[0].path,[[3,4],[1,2]],'دو مرحله پرش');
L.applyMove(st,mv[0]);
T.eq(st.b[1][2],1,'فرود نهایی');T.eq(st.b[4][3],0,'قربانی اول');T.eq(st.b[2][3],0,'قربانی دوم');T.eq(st.b[5][2],0,'مبدأ');T.eq(st.b[3][4],0,'میانه خالی');"""),
("تاج‌گذاری در ردیف آخر و حرکت چهارجهتهٔ شاه",
 r"""function mk(){var b=[],r,c;for(r=0;r<8;r++){b.push([]);for(c=0;c<8;c++)b[r].push(0);}return {b:b,q:0};}
var s1=mk();s1.b[1][2]=1;
L.applyMove(s1,{from:[1,2],path:[[0,1]]});
T.eq(s1.b[0][1],2,'مرد پ۱ شاه شد');
var s2=mk();s2.b[6][5]=-1;
L.applyMove(s2,{from:[6,5],path:[[7,4]]});
T.eq(s2.b[7][4],-2,'مرد پ۲ شاه ربات شد');
var s3=mk();s3.b[3][4]=2;
var km=L.legalMoves(s3,1);
T.eq(km.length,4,'شاه ۴ حرکت');
T.ok(km.some(function(m){return m.path[0][0]===4;}),'شاه به پایین هم می‌رود');"""),
("برنده با حذف کامل یا بی‌حرکتی",
 r"""function mk(){var b=[],r,c;for(r=0;r<8;r++){b.push([]);for(c=0;c<8;c++)b[r].push(0);}return {b:b,q:0};}
var s1=mk();s1.b[4][3]=-1;T.eq(L.winner(s1),-1,'بدون مهرهٔ انسان ⇒ ربات برنده');
var s2=mk();s2.b[4][3]=1;T.eq(L.winner(s2),1,'بدون مهرهٔ ربات ⇒ انسان برنده');
var s3=mk();s3.b[0][1]=1;s3.b[1][0]=-1;s3.b[1][2]=-1;T.eq(L.winner(s3),-1,'انسان بی‌حرکت ⇒ باخت');
var s4=L.initial();T.eq(L.winner(s4),0,'اولیه ⇒ بدون برنده');"""),
("ارزیابی متعادل/متناهی و حرکت مجاز AI",
 r"""var st=L.initial(),ev=L.evaluate(st);
T.eq(ev,0,'تعادل دقیق چیدمان اولیه');
T.ok(isFinite(ev),'ارزیابی متناهی (بدون NaN)');
var mv=L.aiMove(st,function(){return 0.5;},2);
T.ok(!!mv,'AI حرکت برمی‌گرداند');
var lm=L.legalMoves(st,-1),found=false,i;
for(i=0;i<lm.length;i++)if(JSON.stringify(lm[i])===JSON.stringify(mv))found=true;
T.ok(found,'حرکت AI در فهرست حرکات مجاز');"""),
("بازی کامل AI مقابل AI با سید (حداکثر ۲۰۰ نیم‌حرکت)",
 r"""var st=L.initial(),pl=1,n=0,w=0,mv,lm,ok,i;
while(n<200){
  w=L.winner(st);if(w!==0)break;
  mv=L.aiMove(st,rng,2,pl);
  T.ok(!!mv,'حرکت موجود در نوبت '+n);
  lm=L.legalMoves(st,pl);ok=false;
  for(i=0;i<lm.length;i++)if(JSON.stringify(lm[i])===JSON.stringify(mv))ok=true;
  T.ok(ok,'حرکت قانونی در نوبت '+n);
  L.applyMove(st,mv);n++;pl=-pl;
}
w=L.winner(st);
if(n>=200){T.ok(w===0||w==='draw','بازی تا سقف حرکت بدون خطا ادامه یافت: '+w);}
else{T.ok(w===1||w===-1||w==='draw','پایان معتبر: '+w);}
T.ok(n<=200,'زیر ۲۰۰ نیم‌حرکت: '+n);
T.ok(isFinite(L.evaluate(st)),'ارزیابی متناهی در پایان');"""
),
]

# ============================================================ GOMOKU
GOMOKU_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
var N=15,C=7;
function initial(){var b=[],r,c;for(r=0;r<N;r++){b.push([]);for(c=0;c<N;c++)b[r].push(0);}return {b:b,n:0};}
function inB(r,c){return r>=0&&r<N&&c>=0&&c<N;}
function place(st,r,c,p){if(!inB(r,c)||st.b[r][c]!==0)return false;st.b[r][c]=p;st.n=(st.n||0)+1;return true;}
function winB(b,r,c){
  var p=b[r][c];if(!p)return false;
  var D=[[0,1],[1,0],[1,1],[1,-1]],i,d,k,cnt;
  for(i=0;i<4;i++){d=D[i];cnt=1;
    for(k=1;k<5;k++){if(inB(r+d[0]*k,c+d[1]*k)&&b[r+d[0]*k][c+d[1]*k]===p)cnt++;else break;}
    for(k=1;k<5;k++){if(inB(r-d[0]*k,c-d[1]*k)&&b[r-d[0]*k][c-d[1]*k]===p)cnt++;else break;}
    if(cnt>=5)return true;}
  return false;
}
function winAt(st,r,c){return winB(st.b,r,c);}
function lineInfo(b,r,c,p,dr,dc){
  var n=1,e1=0,e2=0,k,rr,cc;
  for(k=1;k<5;k++){rr=r+dr*k;cc=c+dc*k;if(!inB(rr,cc))break;if(b[rr][cc]===p){n++;continue;}if(b[rr][cc]===0)e1=1;break;}
  for(k=1;k<5;k++){rr=r-dr*k;cc=c-dc*k;if(!inB(rr,cc))break;if(b[rr][cc]===p){n++;continue;}if(b[rr][cc]===0)e2=1;break;}
  return {n:n,o:e1+e2};
}
function patt(n,o){if(n>=5)return 1e7;if(n===4)return o===2?1e6:(o===1?1e5:0);if(n===3)return o===2?5e4:(o===1?5e3:0);if(n===2)return o===2?2e3:(o===1?200:0);return o===2?100:10;}
function scorePt(b,r,c,p){var D=[[0,1],[1,0],[1,1],[1,-1]],s=0,i,li;for(i=0;i<4;i++){li=lineInfo(b,r,c,p,D[i][0],D[i][1]);s+=patt(li.n,li.o);}return s;}
function hasN(b,r,c){var i,j;for(i=-2;i<=2;i++)for(j=-2;j<=2;j++){if((i||j)&&inB(r+i,c+j)&&b[r+i][c+j]!==0)return true;}return false;}
function aiMove(st,rng,pl){
  if(pl===undefined)pl=-1;
  var b=st.b,op=-pl,em=[],r,c,i;
  for(r=0;r<N;r++)for(c=0;c<N;c++)if(b[r][c]===0)em.push([r,c]);
  if(!em.length)return null;
  if((st.n||0)===0)return [C,C];
  for(i=0;i<em.length;i++){r=em[i][0];c=em[i][1];b[r][c]=pl;var w=winB(b,r,c);b[r][c]=0;if(w)return [r,c];}
  var blocks=[],bs=-1,bi=0;
  for(i=0;i<em.length;i++){r=em[i][0];c=em[i][1];b[r][c]=op;var w2=winB(b,r,c);b[r][c]=0;if(w2)blocks.push([r,c]);}
  if(blocks.length){
    for(i=0;i<blocks.length;i++){var s=scorePt(b,blocks[i][0],blocks[i][1],pl);if(s>bs){bs=s;bi=i;}}
    return blocks[bi];
  }
  var best=null,bsc=-1;
  for(i=0;i<em.length;i++){
    r=em[i][0];c=em[i][1];
    if(!hasN(b,r,c))continue;
    var sc=scorePt(b,r,c,pl)+0.85*scorePt(b,r,c,op)-(Math.abs(r-C)+Math.abs(c-C))+(rng?rng()*40:0);
    if(sc>bsc){bsc=sc;best=[r,c];}
  }
  if(best)return best;
  var bd=1e9;
  for(i=0;i<em.length;i++){var dd=Math.abs(em[i][0]-C)+Math.abs(em[i][1]-C);if(dd<bd){bd=dd;best=em[i];}}
  return best;
}
return {initial:initial,place:place,winAt:winAt,aiMove:aiMove,scorePt:scorePt};
})();
"""

GOMOKU_UI = r"""
var st=L.initial(),turn=1,over=false,busy=false,last=null,gb;
function cntp(p){var n=0,r,c;for(r=0;r<15;r++)for(c=0;c<15;c++)if(st.b[r][c]===p)n++;return n;}
function render(){
  var h='',r,c,cls,inner;
  for(r=0;r<15;r++)for(c=0;c<15;c++){
    cls='gc'+(((r===3||r===7||r===11)&&(c===3||c===7||c===11))?' hp':'');
    if(last&&last[0]===r&&last[1]===c)cls+=' lm';
    inner=st.b[r][c]?'<div class="st '+(st.b[r][c]>0?'sb':'sw')+'"></div>':'';
    h+='<div class="'+cls+'" data-r="'+r+'" data-c="'+c+'">'+inner+'</div>';
  }
  gb.innerHTML=h;
  document.getElementById('gm-cnt').innerHTML='سیاه '+fa(cntp(1))+' · سفید '+fa(cntp(-1));
}
function endGame(w){
  over=true;
  if(w===1)ovl('بردی!','پنج مهرهٔ سیاهِ شما در یک ردیف قرار گرفت.','بازی جدید',newGame);
  else if(w===-1)ovl('باختی!','سفید پنج‌تایی ساخت؛ دفعهٔ بعد چهارخط‌ها را زودتر ببندید.','بازی جدید',newGame);
  else ovl('مساوی','صفحه پر شد و برنده‌ای شکل نگرفت.','بازی جدید',newGame);
}
function newGame(){st=L.initial();turn=1;over=false;busy=false;last=null;render();hud('نوبت شما — مهرهٔ سیاه');}
function gclick(e){
  if(over||busy||turn!==1)return;
  var el=e.target;
  while(el&&el!==gb&&!(el.getAttribute&&el.getAttribute('data-r')))el=el.parentNode;
  if(!el||el===gb)return;
  var r=+el.getAttribute('data-r'),c=+el.getAttribute('data-c');
  if(st.b[r][c]){toast('این خانه اشغال است');return;}
  if(!L.place(st,r,c,1))return;
  last=[r,c];render();
  if(L.winAt(st,r,c)){endGame(1);return;}
  if(st.n>=225){endGame(0);return;}
  turn=-1;busy=true;hud('نوبت ربات…');
  setTimeout(function(){
    var mv=L.aiMove(st,Math.random);
    if(mv){L.place(st,mv[0],mv[1],-1);last=mv;}
    busy=false;turn=1;render();
    if(mv&&L.winAt(st,mv[0],mv[1])){endGame(-1);return;}
    if(st.n>=225){endGame(0);return;}
    hud('نوبت شما — مهرهٔ سیاه');
  },430);
}
var app=$('#app');
app.innerHTML='<div id="gb" dir="ltr"></div><div id="tools"><button id="ng" class="btn gold" data-smoke>بازی جدید</button><span id="gm-cnt"></span></div>';
gb=document.getElementById('gb');
gb.onclick=gclick;
$('#ng').onclick=newGame;
newGame();
$('#hint').textContent='روی تقاطع خالی بزنید؛ پنج مهرهٔ پیاپی در هر جهتی برنده است؛ چهارخط حریف را فوراً ببندید.';
"""

GOMOKU_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0d1526;color:#e8e4d8;font-family:Vazirmatn,Tahoma,sans-serif;text-align:center}
.wog-home{display:inline-block;margin:8px 14px 0;color:#3fb8af;text-decoration:none;font-size:.9em}
header{padding:6px 12px 0}
h1{margin:2px 0;color:#d9a441;font-size:1.3em}
#hud{color:#9fb0d0;min-height:1.4em}
#gb{display:grid;grid-template-columns:repeat(15,1fr);width:min(96vw,500px);height:min(96vw,500px);margin:0 auto;background:#152238;border:2px solid #24345a;border-radius:10px;overflow:hidden;touch-action:manipulation;cursor:pointer}
.gc{position:relative;border:1px solid #223254;display:flex;align-items:center;justify-content:center}
.gc.hp::before{content:'';position:absolute;width:5px;height:5px;border-radius:50%;background:#2c4270;z-index:0}
.gc.lm{box-shadow:inset 0 0 0 2px #d9a441;z-index:2}
.st{width:84%;height:84%;border-radius:50%;z-index:1;box-shadow:0 2px 4px rgba(0,0,0,.5)}
.sb{background:radial-gradient(circle at 35% 30%,#6d7f9f,#131f38 72%);border:1px solid #d9a441}
.sw{background:radial-gradient(circle at 35% 30%,#ffffff,#c7d3e8 72%);border:1px solid #8496b8}
#tools{display:flex;gap:10px;justify-content:center;align-items:center;padding:10px;flex-wrap:wrap}
.btn{min-height:44px;min-width:110px;border:0;border-radius:10px;font-family:inherit;font-size:1em;cursor:pointer;background:#1b2846;color:#e8e4d8;touch-action:manipulation}
.btn.gold{background:#d9a441;color:#231803;font-weight:700}
#gm-cnt{color:#9fb0d0}
#hint{color:#9fb0d0;padding:0 16px;line-height:1.9}
"""

GOMOKU_TESTS = [
("تشخیص برد در چهار جهت و بیش‌خط",
 r"""function mk(){var b=[],r,c;for(r=0;r<15;r++){b.push([]);for(c=0;c<15;c++)b[r].push(0);}return {b:b,n:0};}
function put(st,cells,p){for(var i=0;i<cells.length;i++)st.b[cells[i][0]][cells[i][1]]=p;return st;}
var s=put(mk(),[[7,5],[7,6],[7,7],[7,8],[7,9]],1);
T.ok(L.winAt(s,7,7),'افقی');
var s2=put(mk(),[[3,4],[4,4],[5,4],[6,4],[7,4]],-1);
T.ok(L.winAt(s2,5,4),'عمودی');
var s3=put(mk(),[[4,4],[5,5],[6,6],[7,7],[8,8]],1);
T.ok(L.winAt(s3,6,6),'قطر ↘');
var s4=put(mk(),[[8,4],[7,5],[6,6],[5,7],[4,8]],-1);
T.ok(L.winAt(s4,6,6),'قطر ↙');
var s5=put(mk(),[[7,3],[7,4],[7,5],[7,6],[7,7],[7,8]],1);
T.ok(L.winAt(s5,7,5),'بیش‌خط ۶تایی هم برد است');
var s6=put(mk(),[[7,5],[7,6],[7,7],[7,8]],1);
T.ok(!L.winAt(s6,7,6),'چهارتایی برد نیست');
var s7=put(mk(),[[7,5],[7,6],[7,8],[7,9],[7,10]],1);
T.ok(!L.winAt(s7,7,8),'پنج ناپیوسته برد نیست');
T.ok(!L.winAt(mk([]),7,7),'خانهٔ خالی برد نیست');"""),
("place: موفق، اشغال و خارج از محدوده رد می‌شود",
 r"""var st=L.initial();
T.ok(L.place(st,7,7,1),'قرار دادن موفق');
T.eq(st.b[7][7],1,'سنگ ثبت شد');
T.ok(!L.place(st,7,7,-1),'خانهٔ اشغال رد شد');
T.eq(st.b[7][7],1,'تغییر نکرد');
T.ok(!L.place(st,15,3,1),'ردیف خارج از محدوده');
T.ok(!L.place(st,-1,3,1),'ردیف منفی');
T.ok(!L.place(st,3,15,1),'ستون خارج از محدوده');
var full=L.initial(),r,c;for(r=0;r<15;r++)for(c=0;c<15;c++)full.b[r][c]=1;
T.eq(L.aiMove(full,rng),null,'صفحهٔ پر ⇒ null');"""),
("AI برد فوری خود را می‌گیرد",
 r"""var st=L.initial();
st.b[7][5]=-1;st.b[7][6]=-1;st.b[7][7]=-1;st.b[7][8]=-1;st.b[0][0]=1;st.n=5;
var mv=L.aiMove(st,rng);
T.ok(!!mv,'حرکت دارد');
T.ok(mv[0]===7&&(mv[1]===4||mv[1]===9),'تکمیل پنج‌تایی: '+JSON.stringify(mv));"""),
("AI برد فوری حریف را مسدود می‌کند",
 r"""var st=L.initial();
st.b[7][5]=1;st.b[7][6]=1;st.b[7][7]=1;st.b[7][8]=1;
st.b[0][0]=-1;st.b[1][1]=-1;st.b[2][2]=-1;st.n=7;
var mv=L.aiMove(st,rng);
T.ok(!!mv,'حرکت دارد');
T.ok(mv[0]===7&&(mv[1]===4||mv[1]===9),'سرِ چهارخط بسته شد: '+JSON.stringify(mv));"""),
("اولین حرکت AI مرکز صفحه است",
 r"""var st=L.initial();
T.eq(L.aiMove(st,rng),[7,7],'مرکز ۱۵×۱۵');"""),
("بازی کامل AI مقابل AI با سید تا تعیین برنده",
 r"""var st=L.initial(),pl=1,n=0,w=0,mv;
while(n<225&&st.n<225){
  mv=L.aiMove(st,rng,pl);
  T.ok(!!mv,'حرکت در دسترس در حرکت '+n);
  T.ok(L.place(st,mv[0],mv[1],pl),'جایگذاری معتبر');
  n++;
  if(L.winAt(st,mv[0],mv[1])){w=pl;break;}
  pl=-pl;
}
T.ok(w!==0,'بازی با برنده تمام شد نه پر شدن صفحه');
T.ok(L.winAt(st,mv[0],mv[1]),'برد روی آخرین حرکت');
T.ok(st.n<=225,'سقف ۲۲۵ سنگ');"""
),
]

# ============================================================ CONNECT4
CONNECT4_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
function initial(){var b=[],r,c;for(r=0;r<6;r++){b.push([]);for(c=0;c<7;c++)b[r].push(0);}return {b:b,n:0};}
function drop(st,col,p){if(col<0||col>6)return -1;var r;for(r=5;r>=0;r--)if(st.b[r][col]===0){st.b[r][col]=p;st.n=(st.n||0)+1;return r;}return -1;}
function full(st,col){return st.b[0][col]!==0;}
function winAtB(b,r,c){
  var p=b[r][c];if(!p)return false;
  var D=[[0,1],[1,0],[1,1],[1,-1]],i,d,k,cnt;
  for(i=0;i<4;i++){d=D[i];cnt=1;
    for(k=1;k<4;k++){var r1=r+d[0]*k,c1=c+d[1]*k;if(r1>=0&&r1<6&&c1>=0&&c1<7&&b[r1][c1]===p)cnt++;else break;}
    for(k=1;k<4;k++){var r2=r-d[0]*k,c2=c-d[1]*k;if(r2>=0&&r2<6&&c2>=0&&c2<7&&b[r2][c2]===p)cnt++;else break;}
    if(cnt>=4)return true;}
  return false;
}
function winAt(st,r,c){return winAtB(st.b,r,c);}
function ws(a,h){if(a===4)return 1e5;if(h===4)return -1e5;if(a&&h)return 0;if(a===3)return 60;if(a===2)return 10;if(a===1)return 1;if(h===3)return -75;if(h===2)return -12;if(h===1)return -1;return 0;}
function evalBoard(b){
  var s=0,r,c,i,a,h,v;
  for(r=0;r<6;r++)for(c=0;c<4;c++){a=0;h=0;for(i=0;i<4;i++){v=b[r][c+i];if(v===1)a++;else if(v===-1)h++;}s+=ws(a,h);}
  for(c=0;c<7;c++)for(r=0;r<3;r++){a=0;h=0;for(i=0;i<4;i++){v=b[r+i][c];if(v===1)a++;else if(v===-1)h++;}s+=ws(a,h);}
  for(r=0;r<3;r++)for(c=0;c<4;c++){
    a=0;h=0;for(i=0;i<4;i++){v=b[r+i][c+i];if(v===1)a++;else if(v===-1)h++;}s+=ws(a,h);
    a=0;h=0;for(i=0;i<4;i++){v=b[r+i][c+3-i];if(v===1)a++;else if(v===-1)h++;}s+=ws(a,h);}
  for(r=0;r<6;r++)for(c=0;c<7;c++){v=b[r][c];if(v===1)s+=(3-Math.abs(c-3))*2;else if(v===-1)s-=(3-Math.abs(c-3))*2;}
  return s;
}
var COLS=[3,2,4,1,5,0,6];
function lowest(b,c){var r;for(r=5;r>=0;r--)if(b[r][c]===0)return r;return -1;}
function search(b,depth,a,bta,pl){
  var best=-1e9,any=false,i,c,r,sc;
  for(i=0;i<7;i++){
    c=COLS[i];if(b[0][c]!==0)continue;any=true;
    r=lowest(b,c);
    b[r][c]=pl;
    if(winAtB(b,r,c)){b[r][c]=0;return 1e6+depth;}
    if(depth<=1)sc=pl>0?evalBoard(b):-evalBoard(b);
    else sc=-search(b,depth-1,-bta,-a,-pl);
    b[r][c]=0;
    if(sc>best)best=sc;
    if(best>a)a=best;
    if(a>=bta)break;
  }
  return any?best:0;
}
function aiMove(st,rng,pl){
  if(pl===undefined)pl=-1;
  var b=st.b,alpha=-1e9,bestS=-1e9,bestC=-1,i,c,r,sc;
  if(st.n===0)return 3;
  for(i=0;i<7;i++){
    c=COLS[i];if(b[0][c]!==0)continue;
    r=lowest(b,c);
    b[r][c]=pl;
    if(winAtB(b,r,c)){b[r][c]=0;return c;}
    sc=-search(b,3,-1e9,-alpha,-pl);
    b[r][c]=0;
    if(sc>bestS){bestS=sc;bestC=c;}
    if(sc>alpha)alpha=sc;
  }
  return bestC;
}
return {initial:initial,drop:drop,full:full,winAt:winAt,aiMove:aiMove,evalBoard:evalBoard};
})();
"""

CONNECT4_UI = r"""
var st=L.initial(),turn=1,over=false,busy=false,b4;
function render(winCells){
  winCells=winCells||[];
  var mark={},i;
  for(i=0;i<winCells.length;i++)mark[winCells[i][0]*7+winCells[i][1]]=1;
  var h='',r,c,cls,inner;
  for(r=0;r<6;r++)for(c=0;c<7;c++){
    cls='cc';inner='';
    if(mark[r*7+c])cls+=' wc';
    if(st.b[r][c])inner='<div class="ds '+(st.b[r][c]>0?'dr':'dg')+'"></div>';
    h+='<div class="'+cls+'" data-c="'+c+'">'+inner+'</div>';
  }
  b4.innerHTML=h;
  document.getElementById('c4-mv').innerHTML='حرکت '+fa(st.n);
}
function winCellsUI(r,c){
  var p=st.b[r][c],D=[[0,1],[1,0],[1,1],[1,-1]],i,d,k,cells,rr,cc;
  for(i=0;i<4;i++){d=D[i];cells=[[r,c]];
    for(k=1;k<4;k++){rr=r+d[0]*k;cc=c+d[1]*k;if(rr<0||rr>5||cc<0||cc>6||st.b[rr][cc]!==p)break;cells.push([rr,cc]);}
    for(k=1;k<4;k++){rr=r-d[0]*k;cc=c-d[1]*k;if(rr<0||rr>5||cc<0||cc>6||st.b[rr][cc]!==p)break;cells.push([rr,cc]);}
    if(cells.length>=4)return cells;}
  return [];
}
function endGame(w,wc){over=true;render(wc||[]);
  if(w===1)ovl('بردی!','چهار مهرهٔ قرمز در یک خط نشست.','بازی جدید',newGame);
  else if(w===-1)ovl('باختی!','ربات چهار در یک خط ساخت.','بازی جدید',newGame);
  else ovl('مساوی','همهٔ خانه‌ها پر شد.','بازی جدید',newGame);}
function newGame(){st=L.initial();turn=1;over=false;busy=false;render();hud('نوبت شما — مهرهٔ قرمز');}
function humanDrop(c){
  if(over||busy||turn!==1)return;
  var r=L.drop(st,c,1);
  if(r<0){toast('این ستون پر است');return;}
  render();
  var wc=winCellsUI(r,c);
  if(wc.length){endGame(1,wc);return;}
  if(st.n>=42){endGame(0);return;}
  turn=-1;busy=true;hud('نوبت ربات…');
  setTimeout(function(){
    var ac=L.aiMove(st,Math.random);
    var ar=ac>=0?L.drop(st,ac,-1):-1;
    busy=false;turn=1;render();
    if(ar>=0){
      var wc2=winCellsUI(ar,ac);
      if(wc2.length){endGame(-1,wc2);return;}
    }
    if(st.n>=42){endGame(0);return;}
    hud('نوبت شما — مهرهٔ قرمز');
  },560);
}
var app=$('#app');
app.innerHTML='<div id="b4" dir="ltr"></div><div id="tools"><button id="ng" class="btn gold" data-smoke>بازی جدید</button><span id="c4-mv"></span></div>';
b4=document.getElementById('b4');
b4.onclick=function(e){
  var el=e.target;
  while(el&&el!==b4&&!(el.getAttribute&&el.getAttribute('data-c')))el=el.parentNode;
  if(!el||el===b4)return;
  humanDrop(+el.getAttribute('data-c'));
};
$('#ng').onclick=newGame;
newGame();
$('#hint').textContent='روی ستون دلخواه بزنید تا مهرهٔ قرمز پایین بریزد؛ چهار مهرهٔ پیاپی در هر جهتی برنده است؛ ستون میانی ارزشمندترین است.';
"""

CONNECT4_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0d1526;color:#e8e4d8;font-family:Vazirmatn,Tahoma,sans-serif;text-align:center}
.wog-home{display:inline-block;margin:8px 14px 0;color:#3fb8af;text-decoration:none;font-size:.9em}
header{padding:6px 12px 0}
h1{margin:2px 0;color:#d9a441;font-size:1.3em}
#hud{color:#9fb0d0;min-height:1.4em}
#b4{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;width:min(96vw,480px);margin:0 auto;padding:10px;background:#1b2846;border-radius:12px;box-shadow:0 8px 22px rgba(0,0,0,.45);touch-action:manipulation;cursor:pointer}
.cc{position:relative;aspect-ratio:1/1;min-height:36px;border-radius:50%;background:#0d1526;display:flex;align-items:center;justify-content:center}
.cc.wc{box-shadow:inset 0 0 0 3px #67b98a}
.ds{width:100%;height:100%;border-radius:50%;box-shadow:0 2px 5px rgba(0,0,0,.5)}
.dr{background:radial-gradient(circle at 35% 30%,#f0937f,#e26d5c 60%,#a3402f)}
.dg{background:radial-gradient(circle at 35% 30%,#f2cd7f,#d9a441 60%,#a97c22)}
#tools{display:flex;gap:10px;justify-content:center;align-items:center;padding:10px;flex-wrap:wrap}
.btn{min-height:44px;min-width:110px;border:0;border-radius:10px;font-family:inherit;font-size:1em;cursor:pointer;background:#1b2846;color:#e8e4d8;touch-action:manipulation}
.btn.gold{background:#d9a441;color:#231803;font-weight:700}
#c4-mv{color:#9fb0d0}
#hint{color:#9fb0d0;padding:0 16px;line-height:1.9}
"""

CONNECT4_TESTS = [
("جاذبه و ستون پر",
 r"""var st=L.initial(),i;
T.eq(L.drop(st,3,1),5,'اولین مهره ته می‌نشیند');
T.eq(L.drop(st,3,-1),4,'دومین روی آن');
T.eq(L.drop(st,3,1),3,'سومین');
T.eq(st.b[5][3],1,'ردیف پایین قرمز');
T.eq(st.b[4][3],-1,'ربات بالای آن');
T.eq(L.drop(st,7,1),-1,'ستون ۷ نامعتبر');
T.eq(L.drop(st,-1,1),-1,'ستون منفی نامعتبر');
for(i=0;i<3;i++)L.drop(st,3,i%2?-1:1);
T.ok(L.full(st,3),'ستون ۳ پر شد');
T.eq(L.drop(st,3,1),-1,'ریختن در ستون پر ⇒ -۱');
T.ok(!L.full(st,0),'ستون ۰ خالی است');
T.eq(st.n,6,'شش مهره افتاد');"""),
("چهار در یک خط در هر چهار جهت",
 r"""function mk(f){var st=L.initial(),i;for(i=0;i<f.length;i++)st.b[f[i][0]][f[i][1]]=1;return st;}
var h=mk([[5,1],[5,2],[5,3],[5,4]]);
T.ok(L.winAt(h,5,3),'افقی');T.ok(!L.winAt(h,4,3),'خارج از خط برد نیست');
var v=mk([[1,2],[2,2],[3,2],[4,2]]);
T.ok(L.winAt(v,4,2),'عمودی');
var d1=mk([[2,0],[3,1],[4,2],[5,3]]);
T.ok(L.winAt(d1,4,2),'قطر ↘');
var d2=mk([[5,0],[4,1],[3,2],[2,3]]);
T.ok(L.winAt(d2,3,2),'قطر ↙');
var t3=mk([[5,1],[5,2],[5,3]]);
T.ok(!L.winAt(t3,5,3),'سه‌تایی کافی نیست');
var brk=mk([[5,1],[5,2],[5,4],[5,5]]);
T.ok(!L.winAt(brk,5,2),'خط شکسته برد نیست');
T.ok(!L.winAt(mk([]),0,0),'صفحهٔ خالی');"""),
("AI برد فوری خود را می‌گیرد",
 r"""var st=L.initial();
st.b[5][2]=-1;st.b[5][3]=-1;st.b[5][4]=-1;st.b[5][0]=1;st.n=4;
var c=L.aiMove(st,rng);
T.ok(c===1||c===5,'تکمیل چهارخط در ستون ۱ یا ۵: '+c);
L.drop(st,c,-1);
T.ok(L.winAt(st,5,c),'بعد از حرکت، چهارخط برقرار است');"""),
("AI باخت فوری را مسدود می‌کند",
 r"""var st=L.initial();
st.b[5][2]=1;st.b[5][3]=1;st.b[5][4]=1;
st.b[5][1]=-1;st.b[5][6]=-1;st.b[4][6]=-1;st.n=6;
var c=L.aiMove(st,rng);
T.eq(c,5,'تنها ستون نجات‌بخش ۵ است');"""),
("ترجیح مرکز و صفحهٔ پر",
 r"""T.eq(L.aiMove(L.initial(),rng),3,'شروع از ستون مرکزی');
var st=L.initial(),i,k;
for(k=0;k<6;k++)for(i=0;i<7;i++)L.drop(st,i,(k+i)%2?1:-1);
T.eq(L.aiMove(st,rng),-1,'صفحهٔ پر ⇒ -۱');
T.ok(isFinite(L.evalBoard(st.b)),'ارزیابی متناهی');"""),
("بازی کامل AI مقابل AI با سید",
 r"""var st=L.initial(),pl=1,n=0,w=0,c,r;
while(n<42){
  c=L.aiMove(st,rng,pl);
  T.ok(c>=0&&c<=6,'ستون معتبر: '+c);
  r=L.drop(st,c,pl);
  T.ok(r>=0,'ریختن موفق در حرکت '+n);
  n++;
  if(L.winAt(st,r,c)){w=pl;break;}
  if(st.n>=42)break;
  pl=-pl;
}
T.ok(w!==0||st.n>=42,'پایان با برد یا پر شدن صفحه');
T.ok(isFinite(L.evalBoard(st.b)),'ارزیابی متناهی در پایان');"""
),
]

GAMES = [
    G("checkers", "چکرز", "board", "♟", "#d9a441", "#3fb8af",
      "چکرز آمریکایی روی صفحهٔ ۸×۸ در برابر ربات؛ گرفتن با پرش اجباری است، پرش چندگانه باید ادامه یابد و مهره‌ای که به ردیف آخر برسد شاه می‌شود.",
      "مهرهٔ طلایی را انتخاب و خانهٔ مقصد را بزنید؛ اگر پرشی در کار باشد گرفتن اجباری است.",
      logic=CHECKERS_LOGIC, ui=CHECKERS_UI, css=CHECKERS_CSS, engines=("common",), tests=CHECKERS_TESTS, seed=12345),
    G("gomoku", "پنج‌درردیف", "board", "⚫", "#e8e4d8", "#3fb8af",
      "پنج‌درردیف روی صفحهٔ ۱۵×۱۵؛ شما سیاه هستید و شروع می‌کنید. نخستین پنج مهرهٔ پیاپی در چهار جهت برنده است و ربات خط‌های تهدید را می‌بندد.",
      "روی تقاطع خالی بزنید؛ چهارخط حریف را فوراً ببندید و برای خودش تهدید دوگانه بسازید.",
      logic=GOMOKU_LOGIC, ui=GOMOKU_UI, css=GOMOKU_CSS, engines=("common",), tests=GOMOKU_TESTS, seed=12345),
    G("connect4", "چهار در یک خط", "board", "🔴", "#e26d5c", "#d9a441",
      "چهار در یک خط با جاذبه روی ستون‌های هفت‌گانه؛ ربات با جست‌وجوی عمق ۴ و هرس آلفا-بتا و ارزیابی مرکزگرا بازی می‌کند.",
      "روی ستون بزنید تا مهره بیفتد؛ ستون میانی ارزشمندترین است و حمله و دفاع را هم‌زمان ببینید.",
      logic=CONNECT4_LOGIC, ui=CONNECT4_UI, css=CONNECT4_CSS, engines=("common",), tests=CONNECT4_TESTS, seed=12345),
]
