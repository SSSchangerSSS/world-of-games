# -*- coding: utf-8 -*-
# AG-C2 — board batch: morris9 (Nine Men's Morris) + hex (11x11) + chomp (5x6)
from lib_mini import G

MORRIS_LOGIC = r"""
var PTS=[[0,0],[3,0],[6,0],[6,3],[6,6],[3,6],[0,6],[0,3],[1,1],[3,1],[5,1],[5,3],[5,5],[3,5],[1,5],[1,3],[2,2],[3,2],[4,2],[4,3],[4,4],[3,4],[2,4],[2,3]];
var MILLS=[[0,1,2],[2,3,4],[4,5,6],[6,7,0],[8,9,10],[10,11,12],[12,13,14],[14,15,8],[16,17,18],[18,19,20],[20,21,22],[22,23,16],[1,9,17],[3,11,19],[5,13,21],[7,15,23]];
var ADJ=(function(){var E=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,0],[8,9],[9,10],[10,11],[11,12],[12,13],[13,14],[14,15],[15,8],[16,17],[17,18],[18,19],[19,20],[20,21],[21,22],[22,23],[23,16],[0,8],[1,9],[2,10],[3,11],[4,12],[5,13],[6,14],[7,15],[8,16],[9,17],[10,18],[11,19],[12,20],[13,21],[14,22],[15,23]];var A=[],i;for(i=0;i<24;i++)A.push([]);for(i=0;i<E.length;i++){A[E[i][0]].push(E[i][1]);A[E[i][1]].push(E[i][0]);}return A;})();
function initial(){var b=[],i;for(i=0;i<24;i++)b.push(0);return {b:b,tp:[9,9],turn:1,rm:0,ply:0,lost:[0,0]};}
function millsAt(st,pt){var out=[],own=st.b[pt],i,M;if(!own)return out;for(i=0;i<16;i++){M=MILLS[i];if(M[0]===pt||M[1]===pt||M[2]===pt){if(st.b[M[0]]===own&&st.b[M[1]]===own&&st.b[M[2]]===own)out.push(i);}}return out;}
function legalMoves(st,pl){var out=[],i,j,a;if(st.rm===1){var opp=3-pl,c=[],free=[];for(i=0;i<24;i++)if(st.b[i]===opp)c.push(i);for(i=0;i<c.length;i++)if(millsAt(st,c[i]).length===0)free.push(c[i]);if(free.length===0)free=c;for(i=0;i<free.length;i++)out.push({t:'r',at:free[i]});return out;}if(st.tp[pl-1]>0){for(i=0;i<24;i++)if(st.b[i]===0)out.push({t:'p',to:i});return out;}var cnt=0;for(i=0;i<24;i++)if(st.b[i]===pl)cnt++;for(i=0;i<24;i++)if(st.b[i]===pl){if(cnt===3){for(j=0;j<24;j++)if(st.b[j]===0)out.push({t:'m',from:i,to:j});}else{a=ADJ[i];for(j=0;j<a.length;j++)if(st.b[a[j]]===0)out.push({t:'m',from:i,to:a[j]});}}return out;}
function applyMove(st,mv){if(!mv)return st;if(st.rm===1){if(mv.t!=='r'||st.b[mv.at]!==3-st.turn)return st;st.b[mv.at]=0;st.lost[2-st.turn]++;st.rm=0;st.turn=3-st.turn;st.ply=(st.ply||0)+1;return st;}var pl=st.turn;if(mv.t==='p'){if(st.tp[pl-1]<=0||st.b[mv.to]!==0)return st;st.b[mv.to]=pl;st.tp[pl-1]--;}else if(mv.t==='m'){if(st.tp[pl-1]>0||st.b[mv.from]!==pl||st.b[mv.to]!==0)return st;st.b[mv.from]=0;st.b[mv.to]=pl;}else return st;st.ply=(st.ply||0)+1;if(millsAt(st,mv.to).length>0){var opp=3-pl,n=0,i;for(i=0;i<24;i++)if(st.b[i]===opp)n++;if(n>0)st.rm=1;else st.turn=3-pl;}else st.turn=3-pl;return st;}
function winner(st){var i,c1=0,c2=0;for(i=0;i<24;i++){if(st.b[i]===1)c1++;else if(st.b[i]===2)c2++;}if(st.tp[0]===0&&c1<3)return 2;if(st.tp[1]===0&&c2<3)return 1;if(st.rm===0&&legalMoves(st,st.turn).length===0)return 3-st.turn;return 0;}
function threatCount(b,pl,at){var n=0,i,k,mine,empty,M;for(i=0;i<16;i++){M=MILLS[i];if(M[0]!==at&&M[1]!==at&&M[2]!==at)continue;mine=0;empty=0;for(k=0;k<3;k++){if(b[M[k]]===pl)mine++;else if(b[M[k]]===0)empty++;}if(mine===2&&empty===1)n++;}return n;}
function millCount(b,pl,pt){var n=0,i,M;for(i=0;i<16;i++){M=MILLS[i];if(M[0]!==pt&&M[1]!==pt&&M[2]!==pt)continue;if(b[M[0]]===pl&&b[M[1]]===pl&&b[M[2]]===pl)n++;}return n;}
function aiMove(st,rng){var r=rng||Math.random,me=st.turn||2,mv=legalMoves(st,me),i,m,b2,s,best,bs,oppRisk,j;if(mv.length===0)return null;if(st.rm===1){best=null;bs=-1e9;for(i=0;i<mv.length;i++){s=threatCount(st.b,3-me,mv[i].at)*4+ADJ[mv[i].at].length+r();if(s>bs){bs=s;best=mv[i];}}return best;}best=null;bs=-1e9;for(i=0;i<mv.length;i++){m=mv[i];b2=st.b.slice();if(m.t==='m')b2[m.from]=0;b2[m.to]=me;s=0;if(millCount(b2,me,m.to)>0)s+=100;s+=threatCount(st.b,3-me,m.to)*45;s+=threatCount(b2,me,m.to)*10;oppRisk=0;for(j=0;j<24;j++)if(b2[j]===0)oppRisk+=threatCount(b2,3-me,j);s-=oppRisk*2;s+=ADJ[m.to].length*2+(m.t==='m'?ADJ[m.from].length:0);if((st.ply||0)>110)s+=r()*20;s+=r()*3;if(s>bs){bs=s;best=m;}}return best;}
var WOG_LOGIC={PTS:PTS,MILLS:MILLS,ADJ:ADJ,initial:initial,millsAt:millsAt,legalMoves:legalMoves,applyMove:applyMove,winner:winner,aiMove:aiMove};
"""

MORRIS_UI = r"""
var st=L.initial(),sel=-1,over=false,busy=false;
app.innerHTML='<div id="mv-board"></div><div class="rowc"><button id="mv-new" class="wbtn" data-smoke>بازی جدید</button></div>';
var boardEl=$('#mv-board');
$('#mv-new').addEventListener('click',function(){newGame();});
$('#hint').textContent='با چیدن یا حرکت، سه سنگ خودی را در یک خط ردیف کن (میلی) و یک سنگ حریف را بردار. با ۳ سنگ می‌توانی به هر خانهٔ خالی پرواز کنی.';
function cnt(pl){var n=0,i;for(i=0;i<24;i++)if(st.b[i]===pl)n++;return n;}
function X(p){return 22+L.PTS[p][0]*43;}
function Y(p){return 22+L.PTS[p][1]*43;}
function render(){
  var lm=(over||st.turn!==1)?[]:L.legalMoves(st,1);
  var html='<svg viewBox="0 0 302 302" class="mv-svg">';
  var SQ=[[0,0,6,0,6,6,0,6],[1,1,5,1,5,5,1,5],[2,2,4,2,4,4,2,4]],SP=[[3,0,3,2],[0,3,2,3],[6,3,4,3],[3,6,3,4]];
  var i,k;
  for(k=0;k<3;k++){html+='<polygon points="';for(i=0;i<8;i+=2)html+=(22+SQ[k][i]*43)+','+(22+SQ[k][i+1]*43)+' ';html+='" fill="none" stroke="#3a4a6b" stroke-width="2.5"/>';}
  for(k=0;k<4;k++)html+='<line x1="'+(22+SP[k][0]*43)+'" y1="'+(22+SP[k][1]*43)+'" x2="'+(22+SP[k][2]*43)+'" y2="'+(22+SP[k][3]*43)+'" stroke="#3a4a6b" stroke-width="2.5"/>';
  var targets={},froms={},remov={};
  if(!over&&st.turn===1){
    if(st.rm===1){for(i=0;i<lm.length;i++)remov[lm[i].at]=1;}
    else for(i=0;i<lm.length;i++){
      if(lm[i].t==='p')targets[lm[i].to]=1;
      else{froms[lm[i].from]=1;if(sel===lm[i].from)targets[lm[i].to]=1;}
    }
  }
  for(i=0;i<24;i++){
    var v=st.b[i],fill='#16233f',strk='#44557e',w=2;
    if(v===1){fill='#d9a441';strk='#f0c46a';}
    else if(v===2){fill='#e26d5c';strk='#f0937f';}
    if(remov[i]){strk='#ffffff';w=3.5;}
    else if(targets[i]){strk='#3fb8af';w=3.5;}
    else if(sel===i){strk='#3fb8af';w=4;}
    else if(froms[i]){strk='#8fa2cc';w=3;}
    html+='<circle data-pt="'+i+'" class="mv-pt" cx="'+X(i)+'" cy="'+Y(i)+'" r="13" fill="'+fill+'" stroke="'+strk+'" stroke-width="'+w+'"/>';
  }
  html+='</svg>';
  boardEl.innerHTML=html;
  var cs=boardEl.querySelectorAll('circle');
  for(i=0;i<cs.length;i++)cs[i].addEventListener('click',onPt);
  hudUpd();
}
function hudUpd(){
  var t;
  if(over)t=(L.winner(st)===1?'پایان — برد شما':'پایان — برد ربات');
  else if(st.turn===2)t='نوبت ربات';
  else if(st.rm===1)t='میلی ساختید! یک سنگ حریف را بردارید';
  else if(st.tp[0]>0)t='چیدن سنگ — '+fa(st.tp[0])+' سنگ در دست';
  else t='حرکت سنگ'+(cnt(1)===3?' — پرواز آزاد':'');
  hud('شما '+fa(cnt(1)+st.tp[0])+' سنگ · ربات '+fa(cnt(2)+st.tp[1])+' سنگ — '+t);
}
function onPt(e){
  if(over||busy||st.turn!==1)return;
  var p=+e.currentTarget.getAttribute('data-pt'),lm=L.legalMoves(st,1),i;
  if(st.rm===1){
    for(i=0;i<lm.length;i++)if(lm[i].at===p){L.applyMove(st,lm[i]);step();return;}
    return;
  }
  if(st.tp[0]>0){
    for(i=0;i<lm.length;i++)if(lm[i].to===p){L.applyMove(st,lm[i]);step();return;}
    return;
  }
  if(st.b[p]===1){sel=(sel===p)?-1:p;render();return;}
  if(sel>=0){
    for(i=0;i<lm.length;i++)if(lm[i].t==='m'&&lm[i].from===sel&&lm[i].to===p){sel=-1;L.applyMove(st,lm[i]);step();return;}
    sel=-1;render();
  }
}
function step(){
  render();
  var w=L.winner(st);
  if(w){over=true;render();finish(w);return;}
  if(st.turn===2){busy=true;setTimeout(aiStep,650);}
}
function aiStep(){
  if(over)return;
  var mv=L.aiMove(st,Math.random);
  if(mv)L.applyMove(st,mv);
  var w=L.winner(st);
  if(w){over=true;busy=false;render();finish(w);return;}
  if(st.turn===2){render();setTimeout(aiStep,650);return;}
  busy=false;render();
}
function finish(w){
  if(w===1)ovl('بردی!','ربات سنگ کافی یا حرکت ممکن ندارد.','بازی جدید',newGame);
  else ovl('ربات برد','این‌بار ربات بهتر بازی کرد؛ دوباره تلاش کن.','بازی جدید',newGame);
}
function newGame(){st=L.initial();sel=-1;over=false;busy=false;render();}
render();
"""

MORRIS_TESTS = [
("ساختار صفحه: ۲۴ نقطه، ۱۶ خط، تقارن مجاورت", """
T.eq(L.PTS.length,24,'24 points');
T.eq(L.MILLS.length,16,'16 mills');
var i,j,cntm=[];
for(i=0;i<24;i++){cntm.push(0);T.ok(L.ADJ[i].length>=2&&L.ADJ[i].length<=4,'deg '+i);
  for(j=0;j<L.ADJ[i].length;j++){var nb=L.ADJ[i][j];T.ok(L.ADJ[nb].indexOf(i)>=0,'sym '+i+'-'+nb);}}
T.eq(L.ADJ[8].length,4,'middle ring deg 4');
for(i=0;i<16;i++){var M=L.MILLS[i];T.eq(M.length,3,'mill size');
  T.ok(L.ADJ[M[0]].indexOf(M[1])>=0&&L.ADJ[M[1]].indexOf(M[2])>=0,'mill consecutive pairs adjacent');
  T.ok(L.ADJ[M[0]].indexOf(M[2])<0,'mill endpoints not adjacent (straight line)');
  for(j=0;j<3;j++)cntm[M[j]]++;}
for(i=0;i<24;i++)T.eq(cntm[i],2,'point '+i+' in exactly 2 mills');
"""),
("تشخیص میلی روی حالت‌های ساخته‌شده", """
var st=L.initial();
st.b[0]=1;st.b[1]=1;st.b[2]=1;
var ms=L.millsAt(st,0);
T.ok(ms.length===1&&L.MILLS[ms[0]].indexOf(2)>=0,'mill via point 0');
T.ok(L.millsAt(st,1).length===1&&L.millsAt(st,2).length===1,'all members see mill');
st.b[2]=2;T.eq(L.millsAt(st,0).length,0,'mixed line is not mill');
st.b[2]=0;T.eq(L.millsAt(st,0).length,0,'incomplete is not mill');
var s2=L.initial();s2.b[16]=1;s2.b[17]=1;s2.b[18]=1;
T.ok(L.millsAt(s2,17).length===1,'inner ring mill');
var s3=L.initial();s3.b[0]=1;s3.b[8]=1;s3.b[16]=1;
T.eq(L.millsAt(s3,8).length,0,'diagonal trio is not a mill');
"""),
("محافظت از سنگ‌های میل و استثنای همه-در-میل", """
var st=L.initial();
st.turn=2;st.rm=1;st.tp=[4,7];
st.b[0]=1;st.b[1]=1;st.b[2]=1;st.b[16]=1;st.b[17]=1;
st.b[8]=2;st.b[9]=2;
var mv=L.legalMoves(st,2);
T.eq(mv.length,2,'only non-mill stones removable');
var ats=[mv[0].at,mv[1].at].sort(function(a,b){return a-b;});
T.eq(ats,[16,17],'removable set exact');
T.eq(mv[0].t,'r','removal move type');
T.eq(L.winner(st),0,'pending removal = ongoing');
var st2=L.initial();
st2.turn=2;st2.rm=1;
st2.b[0]=1;st2.b[1]=1;st2.b[2]=1;
st2.b[8]=2;st2.b[9]=2;st2.b[10]=2;
var mv2=L.legalMoves(st2,2);
T.eq(mv2.length,3,'all-in-mills exception: mill stones removable');
var a2=[mv2[0].at,mv2[1].at,mv2[2].at].sort(function(a,b){return a-b;});
T.eq(a2,[0,1,2],'exception removable set');
L.applyMove(st2,mv2[0]);
T.eq(st2.b[mv2[0].at],0,'stone removed');
T.eq(st2.turn,1,'turn passed after removal');
T.eq(st2.rm,0,'removal flag cleared');
"""),
("پرواز فقط با دقیقا ۳ سنگ", """
var st=L.initial();st.tp=[0,0];
st.b[0]=1;st.b[6]=1;st.b[16]=1;
st.b[8]=2;st.b[9]=2;st.b[10]=2;
var mv=L.legalMoves(st,1),i,found=false;
T.eq(mv.length,54,'3 stones x 18 empties');
for(i=0;i<mv.length;i++)if(mv[i].from===0&&mv[i].to===12)found=true;
T.ok(found,'flying to a far empty point');
var s2=L.initial();s2.tp=[0,0];
s2.b[0]=1;s2.b[6]=1;s2.b[16]=1;s2.b[17]=1;
s2.b[8]=2;s2.b[9]=2;s2.b[10]=2;s2.b[11]=2;
var m2=L.legalMoves(s2,1),far=false,adj=false;
for(i=0;i<m2.length;i++){if(m2[i].t==='m'&&m2[i].from===0&&m2[i].to===12)far=true;if(m2[i].t==='m'&&m2[i].from===0&&m2[i].to===1)adj=true;}
T.ok(!far,'4 stones: no flying');
T.ok(adj,'4 stones: adjacent move exists');
"""),
("شرط باخت: کمتر از ۳ سنگ یا بی‌حرکتی", """
var st=L.initial();st.tp=[0,0];
st.b[0]=1;st.b[6]=1;
st.b[8]=2;st.b[9]=2;st.b[10]=2;st.b[11]=2;
T.eq(L.winner(st),2,'fewer than 3 stones loses');
var s2=L.initial();s2.tp=[0,0];s2.turn=1;
var ones=[0,2,4,6],twos=[1,3,5,7,8,10,12,14],i;
for(i=0;i<4;i++)s2.b[ones[i]]=1;
for(i=0;i<8;i++)s2.b[twos[i]]=2;
T.eq(L.winner(s2),2,'immobilized player loses');
T.eq(L.winner(L.initial()),0,'fresh game ongoing');
"""),
("شبیه‌سازی AI مقابل AI: پایان معتبر تا ۳۰۰ نیم‌حرکت", """
var st=L.initial(),plies=0,w=0,mv,i,c1=0,c2=0;
while(plies<300){
  w=L.winner(st);if(w)break;
  mv=L.aiMove(st,rng);
  T.ok(mv,'ai move exists at ply '+plies);
  L.applyMove(st,mv);plies++;
}
T.ok(w===1||w===2,'terminated with valid winner after '+plies+' plies');
for(i=0;i<24;i++){if(st.b[i]===1)c1++;if(st.b[i]===2)c2++;}
T.eq(c1+c2+st.tp[0]+st.tp[1]+st.lost[0]+st.lost[1],18,'piece conservation incl. removed');
T.ok(c1>=2&&c2>=2,'sane final counts');
"""),
]

HEX_LOGIC = r"""
var N=11;
function initial(){var b=[],i;for(i=0;i<121;i++)b.push(0);return {b:b,turn:1};}
function nbrs(r,c){var D=[[0,-1],[0,1],[-1,0],[1,0],[-1,1],[1,-1]],o=[],i;for(i=0;i<6;i++){var rr=r+D[i][0],cc=c+D[i][1];if(rr>=0&&rr<11&&cc>=0&&cc<11)o.push([rr,cc]);}return o;}
function place(st,r,c,pl){if(r<0||r>10||c<0||c>10||st.b[r*11+c]!==0)return false;st.b[r*11+c]=pl;st.turn=3-pl;return true;}
function chainWin(b,pl){var seen=[],q=[],head=0,i,k,D=[[0,-1],[0,1],[-1,0],[1,0],[-1,1],[1,-1]];for(i=0;i<121;i++)seen.push(false);for(i=0;i<11;i++){var s=(pl===1)?i:(i*11);if(b[s]===pl){seen[s]=true;q.push(s);}}while(head<q.length){var cur=q[head++],r0=(cur/11)|0,c0=cur-r0*11;for(k=0;k<6;k++){var rr=r0+D[k][0],cc=c0+D[k][1];if(rr<0||rr>10||cc<0||cc>10)continue;var j=rr*11+cc;if(!seen[j]&&b[j]===pl){seen[j]=true;q.push(j);}}}for(i=0;i<11;i++){var e=(pl===1)?(110+i):(i*11+10);if(seen[e])return true;}return false;}
function winner(st){if(chainWin(st.b,1))return 1;if(chainWin(st.b,2))return 2;return 0;}
function heur(st,r,c){var D=[[0,-1],[0,1],[-1,0],[1,0],[-1,1],[1,-1]],s=0,i;for(i=0;i<6;i++){var rr=r+D[i][0],cc=c+D[i][1];if(rr<0||rr>10||cc<0||cc>10)continue;var v=st.b[rr*11+cc];if(v===2)s+=6;else if(v===1)s+=2;}s+=(10-Math.abs(c-5))*1.2+(10-Math.abs(r-5))*0.6;return s;}
function aiMove(st,rng){var r=rng||Math.random,empt=[],i,k,b2;for(i=0;i<121;i++)if(st.b[i]===0)empt.push(i);if(empt.length===0)return null;for(k=0;k<empt.length;k++){b2=st.b.slice();b2[empt[k]]=2;if(chainWin(b2,2))return [(empt[k]/11)|0,empt[k]%11];}var blocks=[];for(k=0;k<empt.length;k++){b2=st.b.slice();b2[empt[k]]=1;if(chainWin(b2,1))blocks.push(empt[k]);}if(blocks.length>0){var bp=blocks[0],bs=-1e9;for(k=0;k<blocks.length;k++){var rr=(blocks[k]/11)|0,cc=blocks[k]%11,hs=heur(st,rr,cc);if(hs>bs){bs=hs;bp=blocks[k];}}return [(bp/11)|0,bp%11];}var best=null,bs2=-1e9;for(k=0;k<empt.length;k++){var rr2=(empt[k]/11)|0,cc2=empt[k]%11,s2=heur(st,rr2,cc2)+r()*4;if(s2>bs2){bs2=s2;best=[rr2,cc2];}}return best;}
var WOG_LOGIC={initial:initial,place:place,winner:winner,aiMove:aiMove,nbrs:nbrs,chainWin:chainWin};
"""

HEX_UI = r"""
var st=L.initial(),over=false,busy=false;
app.innerHTML='<div id="hx-board"></div><div class="rowc"><button id="hx-new" class="wbtn" data-smoke>بازی جدید</button></div>';
var boardEl=$('#hx-board');
$('#hx-new').addEventListener('click',function(){newGame();});
$('#hint').textContent='شما سیاه هستید و باید دو ضلع بالا و پایین را وصل کنید؛ ربات سفید است و چپ به راست. تساوی وجود ندارد.';
function CX(r,c){return 20+(c+r*0.5)*24;}
function CY(r){return 18+r*20;}
function countP(pl){var n=0,i;for(i=0;i<121;i++)if(st.b[i]===pl)n++;return n;}
function render(){
  var html='<svg viewBox="0 0 400 238" class="hx-svg">',r,c;
  html+='<line x1="'+(CX(0,0)-10)+'" y1="'+(CY(0)-9)+'" x2="'+(CX(0,10)+10)+'" y2="'+(CY(0)-9)+'" stroke="#3fb8af" stroke-width="5" stroke-linecap="round"/>';
  html+='<line x1="'+(CX(10,0)-10)+'" y1="'+(CY(10)+9)+'" x2="'+(CX(10,10)+10)+'" y2="'+(CY(10)+9)+'" stroke="#3fb8af" stroke-width="5" stroke-linecap="round"/>';
  html+='<line x1="'+(CX(0,0)-12)+'" y1="'+(CY(0)-2)+'" x2="'+(CX(10,0)-12)+'" y2="'+(CY(10)+2)+'" stroke="#d9a441" stroke-width="5" stroke-linecap="round"/>';
  html+='<line x1="'+(CX(0,10)+12)+'" y1="'+(CY(0)-2)+'" x2="'+(CX(10,10)+12)+'" y2="'+(CY(10)+2)+'" stroke="#d9a441" stroke-width="5" stroke-linecap="round"/>';
  for(r=0;r<11;r++)for(c=0;c<11;c++){
    var v=st.b[r*11+c],fill='#1d2b4d',strk='#44557e';
    if(v===1){fill='#3fb8af';strk='#a8e6e2';}
    else if(v===2){fill='#d9a441';strk='#f0c46a';}
    html+='<circle data-r="'+r+'" data-c="'+c+'" class="hx-pt" cx="'+CX(r,c)+'" cy="'+CY(r)+'" r="10" fill="'+fill+'" stroke="'+strk+'" stroke-width="1.5"/>';
  }
  html+='</svg>';
  boardEl.innerHTML=html;
  var cs=boardEl.querySelectorAll('circle'),i;
  for(i=0;i<cs.length;i++)cs[i].addEventListener('click',onCell);
  hudUpd();
}
function hudUpd(){
  var t=over?(L.winner(st)===1?'پایان — برد شما':'پایان — برد ربات'):(st.turn===1?'نوبت شما (سیاه)':'نوبت ربات (سفید)');
  hud('سیاه '+fa(countP(1))+' · سفید '+fa(countP(2))+' — '+t);
}
function onCell(e){
  if(over||busy)return;
  var r=+e.currentTarget.getAttribute('data-r'),c=+e.currentTarget.getAttribute('data-c');
  if(!L.place(st,r,c,1)){toast('این خانه پُر است');return;}
  var w=L.winner(st);
  render();
  if(w){over=true;finish(w);return;}
  if(st.turn===2){busy=true;setTimeout(aiStep,550);}
}
function aiStep(){
  if(over)return;
  var mv=L.aiMove(st,Math.random);
  if(mv)L.place(st,mv[0],mv[1],2);
  var w=L.winner(st);
  busy=false;render();
  if(w){over=true;finish(w);return;}
}
function finish(w){
  if(w===1)ovl('بردی!','زنجیرهٔ سیاه بالا و پایین را به هم رساند.','بازی جدید',newGame);
  else ovl('ربات برد','زنجیرهٔ سفید چپ و راست را به هم رساند.','بازی جدید',newGame);
}
function newGame(){st=L.initial();over=false;busy=false;render();}
render();
"""

HEX_TESTS = [
("همسایگی شش‌وجهی (نه قطری مربعی)", """
var n=L.nbrs(5,5).map(function(p){return p[0]+','+p[1];}).sort();
T.eq(n,['4,5','4,6','5,4','5,6','6,4','6,5'],'six hex neighbors of center');
var n0=L.nbrs(0,0).map(function(p){return p[0]+','+p[1];}).sort();
T.eq(n0,['0,1','1,0'],'corner has 2 neighbors');
T.eq(L.nbrs(10,10).length,2,'far corner has 2 neighbors');
"""),
("برد BFS در هر دو جهت + زنجیرهٔ زیگزاگ", """
function board(pairs,val){var s=L.initial();for(var i=0;i<pairs.length;i++)s.b[pairs[i][0]*11+pairs[i][1]]=val;return s;}
var col=[],row=[],zig=[],r,c;
for(r=0;r<11;r++)col.push([r,3]);
T.eq(L.winner(board(col,1)),1,'black vertical chain wins');
for(c=0;c<11;c++)row.push([7,c]);
T.eq(L.winner(board(row,2)),2,'white horizontal chain wins');
for(r=0;r<11;r++)zig.push([r,10-r]);
T.eq(L.winner(board(zig,1)),1,'anti-diagonal chain uses hex diagonal adjacency');
var broken=[];for(r=0;r<10;r++)broken.push([r,3]);
T.eq(L.winner(board(broken,1)),0,'gap breaks the chain');
T.eq(L.winner(L.initial()),0,'empty board no winner');
"""),
("اتصال قطریِ مربعی مجاز نیست", """
function board(pairs,val){var s=L.initial();for(var i=0;i<pairs.length;i++)s.b[pairs[i][0]*11+pairs[i][1]]=val;return s;}
var diag=[],r;
for(r=0;r<11;r++)diag.push([r,r]);
T.eq(L.winner(board(diag,1)),0,'square-diagonal stones never connect');
"""),
("AI برد فوری را می‌گیرد", """
var st=L.initial(),c;
for(c=0;c<10;c++)st.b[5*11+c]=2;
st.b[2]=1;st.b[14]=1;st.b[26]=1;
T.eq(L.winner(st),0,'game still open');
var mv=L.aiMove(st,rng);
T.ok(mv&&mv.length===2,'ai returns a move');
T.eq(L.place(st,mv[0],mv[1],2),true,'placed');
T.eq(L.winner(st),2,'white wins immediately');
"""),
("AI باخت حتمی را دفاع می‌کند", """
var st=L.initial(),r;
for(r=0;r<10;r++)st.b[r*11]=1;
st.b[5*11+5]=2;st.b[6*11+5]=2;
T.eq(L.winner(st),0,'black is one step from winning');
var mv=L.aiMove(st,rng);
T.eq(mv,[10,0],'unique winning cell (10,0) blocked');
T.eq(L.place(st,10,0,2),true,'block placed');
T.eq(L.winner(st),0,'threat neutralized');
"""),
("حرکت نامعتبر رد می‌شود", """
var st=L.initial();
T.eq(L.place(st,5,5,1),true,'first placement ok');
T.eq(st.b[60],1,'board updated');
T.eq(L.place(st,5,5,2),false,'occupied rejected');
T.eq(st.b[60],1,'unchanged after reject');
T.eq(L.place(st,-1,0,1),false,'negative row');
T.eq(L.place(st,0,11,1),false,'column 11');
T.eq(L.place(st,11,0,1),false,'row 11');
T.eq(st.turn,2,'turn moved only on valid');
T.eq(L.place(st,3,3,2),true,'white placement ok');
T.eq(st.turn,1,'turn alternates');
"""),
("پر کردن کامل: دقیقا یک برنده (۳۰ تختهٔ سیددار)", """
var blackWins=0,i,k,w;
for(i=0;i<30;i++){
  var s=L.initial();
  for(k=0;k<121;k++)s.b[k]=rng()<0.5?1:2;
  w=L.winner(s);
  T.ok(w===1||w===2,'full board '+i+' has a winner');
  if(w===1)blackWins++;
}
T.ok(blackWins>0&&blackWins<30,'both colors win across boards: '+blackWins);
"""),
]

CHOMP_LOGIC = r"""
function initial(){return {h:[5,5,5,5,5,5],turn:1};}
function applyPick(st,r,c){var h=st.h;if(c<0||c>5||r<0||r>=h[c])return false;var eaten=[],cc,rr;for(cc=c;cc<6;cc++){for(rr=r;rr<h[cc];rr++)eaten.push([rr,cc]);if(r<h[cc])h[cc]=r;}st.turn=3-st.turn;return eaten;}
function isOver(st){return st.h[0]===0;}
var MEMO={};
function winMove(h){var key=h.join('');if(MEMO.hasOwnProperty(key))return MEMO[key];var out=null,c,r,cc,g;if(h[0]===0){MEMO[key]=[0,0];return [0,0];}for(c=0;c<6;c++){for(r=0;r<h[c];r++){if(r===0&&c===0)continue;g=h.slice();for(cc=c;cc<6;cc++)if(g[cc]>r)g[cc]=r;if(!winMove(g)){out=[r,c];MEMO[key]=out;return out;}}}MEMO[key]=null;return null;}
function aiMove(st,rng){var r=rng||Math.random;if(isOver(st))return null;var wm=winMove(st.h);if(wm)return [wm[0],wm[1]];var best=null,bi=-1e9,c,rr,s;for(c=0;c<6;c++)for(rr=0;rr<st.h[c];rr++){if(rr===0&&c===0)continue;s=rr*2+c+r()*4;if(s>bi){bi=s;best=[rr,c];}}return best?best:[0,0];}
var WOG_LOGIC={initial:initial,applyPick:applyPick,isOver:isOver,aiMove:aiMove,winMove:winMove};
"""

CHOMP_UI = r"""
var st=L.initial(),over=false,busy=false;
app.innerHTML='<div id="ch-grid" class="ch-grid"></div><div class="rowc"><button id="ch-new" class="wbtn" data-smoke>بازی جدید</button></div>';
var gridEl=$('#ch-grid');
$('#ch-new').addEventListener('click',function(){newGame();});
$('#hint').textContent='خانه‌ای را لمس کن؛ همهٔ خانه‌های پایین و راستِ آن هم خورده می‌شوند. خانهٔ سم (✕) را نخور — کسی سم را بخورد می‌بازد.';
function alive(r,c){return r<st.h[c];}
function remain(){var n=0,c;for(c=0;c<6;c++)n+=st.h[c];return n;}
function render(){
  var html='',r,c;
  for(r=0;r<5;r++)for(c=0;c<6;c++){
    var a=alive(r,c);
    var cls='ch-cell'+(a?'':' ch-gone')+((r===0&&c===0&&a)?' ch-poison':'');
    html+='<div class="'+cls+'" data-r="'+r+'" data-c="'+c+'">'+((r===0&&c===0&&a)?'✕':'')+'</div>';
  }
  gridEl.innerHTML=html;
  var cs=gridEl.querySelectorAll('.ch-cell'),i;
  for(i=0;i<cs.length;i++)cs[i].addEventListener('click',onCell);
  hudUpd();
}
function hudUpd(){
  var t=over?'پایان بازی':(st.turn===1?'نوبت شما':'نوبت ربات (حل‌گر دقیق)');
  hud('خانه‌های باقی‌مانده: '+fa(remain())+' — '+t);
}
function onCell(e){
  if(over||busy)return;
  var r=+e.currentTarget.getAttribute('data-r'),c=+e.currentTarget.getAttribute('data-c');
  if(!alive(r,c)){toast('این خانه خورده شده');return;}
  var eaten=L.applyPick(st,r,c);
  if(eaten===false){toast('حرکت نامعتبر');return;}
  render();
  if(L.isOver(st)){finish();return;}
  busy=true;setTimeout(aiStep,650);
}
function aiStep(){
  if(over)return;
  var mv=L.aiMove(st,Math.random);
  if(mv)L.applyPick(st,mv[0],mv[1]);
  busy=false;render();
  if(L.isOver(st))finish();
}
function finish(){
  over=true;
  var loser=3-st.turn;
  if(loser===1)ovl('ربات برد','خانهٔ سم را خوردی!','بازی جدید',newGame);
  else ovl('بردی!','ربات مجبور شد خانهٔ سم را بخورد.','بازی جدید',newGame);
}
function newGame(){st=L.initial();over=false;busy=false;render();}
render();
"""

CHOMP_TESTS = [
("حذف مستطیل دقیق و ارتفاع ستون‌ها", """
var st=L.initial();
T.eq(st.h,[5,5,5,5,5,5],'fresh skyline');
var e=L.applyPick(st,2,3);
T.ok(Array.isArray(e)&&e.length===9,'9 cells eaten');
var want=[],r,c;
for(r=2;r<5;r++)for(c=3;c<6;c++)want.push(r+':'+c);
var got=e.map(function(p){return p[0]+':'+p[1];}).sort();
T.eq(got,want,'exact rectangle r>=2 && c>=3');
T.eq(st.h,[5,5,5,2,2,2],'column heights updated');
T.eq(L.applyPick(st,2,3),false,'eaten cell rejected');
T.eq(L.applyPick(st,7,0),false,'out of range rejected');
var e2=L.applyPick(st,4,1);
T.ok(Array.isArray(e2)&&e2.length===2,'partial bite eats 2');
T.eq(st.h,[5,4,4,2,2,2],'heights after partial bite');
"""),
("خوردن سم یعنی باخت", """
var st=L.initial();
var e=L.applyPick(st,0,0);
T.ok(Array.isArray(e)&&e.length===30,'opening poison eats all 30');
T.eq(L.isOver(st),true,'game over');
T.eq(st.turn,2,'poison-taker lost, winner to move');
var s2=L.initial();
T.ok(L.applyPick(s2,0,4)!==false,'p1 trim');T.eq(s2.h,[5,5,5,5,0,0],'h1');
T.ok(L.applyPick(s2,1,1)!==false,'p2 bite');T.eq(s2.h,[5,1,1,1,0,0],'h2');
T.ok(L.applyPick(s2,0,1)!==false,'p1 sweep');T.eq(s2.h,[5,0,0,0,0,0],'h3');
T.eq(L.isOver(s2),false,'poison still intact');
T.ok(L.applyPick(s2,1,0)!==false,'p2 column');T.eq(s2.h,[1,0,0,0,0,0],'h4');
var ep=L.applyPick(s2,0,0);
T.ok(Array.isArray(ep)&&ep.length===1&&ep[0][0]===0&&ep[0][1]===0,'poison cell eaten last');
T.eq(L.isOver(s2),true,'over after poison');
T.eq(s2.turn,2,'poison-taker (p1) is the loser');
"""),
("حل‌گر ۲×۲: شروع با سم ممنوع", """
T.eq(L.winMove([2,2]),[1,1],'2x2 winning opening is (1,1)');
T.eq(L.winMove([2,1]),null,'[2,1] is a loss for mover');
T.eq(L.winMove([1,0,0,0,0,0]),null,'only poison left: mover loses');
T.eq(L.winMove([2,0,0,0,0,0]),[1,0],'reduce to 1x1 poison-only');
var wm=L.winMove([5,5,5,5,5,5]);
T.ok(wm&&!(wm[0]===0&&wm[1]===0),'5x6 first-player win exists, not poison');
"""),
("قطعیت حافظهٔ موب", """
var a=L.winMove([3,2,2,1,1,1]),b=L.winMove([3,2,2,1,1,1]);
T.eq(a,b,'winMove memo stable');
T.ok(a===null||a.length===2,'solver shape sane');
var st=L.initial();
var m1=L.aiMove(st,rng),m2=L.aiMove(st,rng);
T.eq(m1,m2,'aiMove deterministic on start');
T.ok(m1&&!(m1[0]===0&&m1[1]===0),'ai never opens with poison');
var s2={h:[4,3,3,2,2,1],turn:2};
T.eq(L.aiMove(s2,rng),L.aiMove(s2,rng),'aiMove deterministic midgame');
"""),
("بازی کامل ۵×۶ سیددار: پایان با باختِ خورندهٔ سم", """
var st=L.initial(),picks=0,mv;
while(!L.isOver(st)&&picks<40){
  mv=L.aiMove(st,rng);
  T.ok(mv&&mv.length===2,'move '+picks);
  T.ok(mv[0]>=0&&mv[0]<5&&mv[1]>=0&&mv[1]<6,'in bounds '+picks);
  T.ok(L.applyPick(st,mv[0],mv[1])!==false,'valid pick '+picks);
  picks++;
}
T.ok(L.isOver(st),'game reached poison');
T.ok(picks<=31,'picks='+picks+' bounded by cell count');
T.eq(st.turn,1,'optimal first player wins; poison-taker is the loser');
"""),
]

BASE_CSS = "body{background:#0b1220;color:#e8ecf5;font-family:Vazirmatn,Tahoma,sans-serif;margin:0;padding:8px}.rowc{display:flex;justify-content:center;gap:10px;margin:12px 0}.wbtn{min-height:44px;padding:10px 22px;border-radius:12px;border:1px solid #d9a441;background:#14203a;color:#f5d78e;font-size:15px;cursor:pointer;touch-action:manipulation;font-family:inherit}.wbtn:active{transform:scale(.97)}"

morris9 = G(
    slug="morris9", title="موریس نه‌سنگ", cat="board", icon="◉", g1="#d9a441", g2="#3fb8af",
    desc="موریس نه‌سنگ کلاسیک روی صفحهٔ ۲۴ نقطه‌ای: ابتدا ۹ سنگ می‌چینی، بعد جابه‌جا می‌کنی و با ساختن خط سه‌تایی سنگ حریف را بردار.",
    hint="سه سنگ در یک خط = میلی؛ بعد از هر میلی یک سنگ حریف برداشته می‌شود. با ۳ سنگ، پرواز آزاد داری.",
    logic=MORRIS_LOGIC, ui=MORRIS_UI,
    css=BASE_CSS+".mv-svg{width:100%;max-width:350px;display:block;margin:6px auto;background:#14203a;border:1px solid #223052;border-radius:14px}.mv-pt{cursor:pointer}",
    engines=("common",), tests=MORRIS_TESTS)

hexg = G(
    slug="hex", title="هکس", cat="board", icon="⬡", g1="#3fb8af", g2="#d9a441",
    desc="هکس ۱۱×۱۱: شما با سیاه دو ضلع بالا و پایین را وصل می‌کنید و ربات با سفید چپ و راست را. تساوی در هکس وجود ندارد.",
    hint="روی خانهٔ خالی بزن. همسایه‌ها شش‌جهته‌اند؛ زنجیرهٔ پیوستهٔ سنگ‌های همسایه بساز.",
    logic=HEX_LOGIC, ui=HEX_UI,
    css=BASE_CSS+".hx-svg{width:100%;max-width:430px;display:block;margin:6px auto;background:#14203a;border:1px solid #223052;border-radius:14px}.hx-pt{cursor:pointer}",
    engines=("common",), tests=HEX_TESTS)

chomp = G(
    slug="chomp", title="چامپ", cat="board", icon="◕", g1="#67b98a", g2="#e26d5c",
    desc="چامپ روی تختهٔ شکلاتی ۵×۶ با خانهٔ سم در گوشه: هر حرکت خانهٔ انتخابی و همهٔ پایین‌راست آن را می‌خورد؛ خورندهٔ سم می‌بازد.",
    hint="خانه‌ای را لمس کن تا مستطیل پایین‌راستش خورده شود. ربات با حل‌گر دقیق بازی می‌کند؛ خانهٔ سم (✕) را نخور.",
    logic=CHOMP_LOGIC, ui=CHOMP_UI,
    css=BASE_CSS+".ch-grid{display:grid;grid-template-columns:repeat(6,48px);gap:6px;justify-content:center;margin:14px 0}.ch-cell{height:44px;border-radius:10px;background:#1d2b4d;border:1px solid #3a4a6b;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;color:#fff;touch-action:manipulation}.ch-poison{background:#5c2b24;border-color:#e26d5c;color:#f5b7ac;font-weight:bold}.ch-gone{opacity:.12;cursor:default}",
    engines=("common",), tests=CHOMP_TESTS)

GAMES = [morris9, hexg, chomp]
