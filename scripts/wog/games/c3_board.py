# -*- coding: utf-8 -*-
# AG-C3 — 3 board games: nim (misere) + mancala (kalah) + dots-and-boxes
from lib_mini import G

# ----------------------------- NIM (misere) -----------------------------
NIM_LOGIC = r"""
var WOG_LOGIC={
initial:function(){return{heaps:[3,5,7],turn:0,over:false,loser:-1};},
take:function(st,idx,n){
  if(!st||st.over||idx<0||idx>=st.heaps.length||n<1||n>st.heaps[idx])return false;
  st.heaps[idx]-=n;
  var t=st.heaps[0]+st.heaps[1]+st.heaps[2];
  if(t===0){st.over=true;st.loser=st.turn;}
  else st.turn=1-st.turn;
  return true;
},
isOver:function(st){return !!st.over;},
loser:function(st){return st.loser;},
aiMove:function(st,rng){
  var h=st.heaps,big=[],ones=0,i,x=0;
  for(i=0;i<h.length;i++){if(h[i]>1)big.push(i);else if(h[i]===1)ones++;x^=h[i];}
  if(big.length>=2){
    if(x!==0){for(i=0;i<h.length;i++){var v=h[i]^x;if(v<h[i])return{heap:i,n:h[i]-v};}}
    var bi=big[0];for(i=1;i<big.length;i++)if(h[i]>h[bi])bi=i;
    return{heap:bi,n:1};
  }
  if(big.length===1){var b=big[0];return ones%2===0?{heap:b,n:h[b]-1}:{heap:b,n:h[b]};}
  for(i=0;i<h.length;i++)if(h[i]===1)return{heap:i,n:1};
  return null;
}};
""".strip()

NIM_UI = r"""
var st=L.initial(),sel=-1;
function pips(n){var s='',i;for(i=0;i<n;i++)s+='<span class="pip"></span>';return s;}
function draw(){
  var app=$('#app');app.innerHTML='';
  var wrap=ce('div','board');
  st.heaps.forEach(function(h,i){
    var row=ce('div','heap'+(sel===i?' sel':''));
    row.appendChild(ce('div','hname','توده '+fa(i+1)));
    var dp=ce('div','pips');
    if(h>0)dp.innerHTML=pips(h);else dp.appendChild(ce('span','none','خالی'));
    row.appendChild(dp);
    row.appendChild(ce('div','hcount',fa(h)+' مهره'));
    row.onclick=function(){if(!st.over&&st.turn===0&&st.heaps[i]>0){sel=i;draw();}};
    wrap.appendChild(row);
  });
  app.appendChild(wrap);
  var bar=ce('div','bar');
  if(st.over){bar.appendChild(ce('div','msg',st.loser===0?'پایان — باختی!':'پایان — بردی!'));}
  else if(st.turn===1){bar.appendChild(ce('div','msg','نوبت رایانه...'));}
  else if(sel<0||st.heaps[sel]<1){bar.appendChild(ce('div','msg','یک توده را انتخاب کن'));}
  else{
    var h=st.heaps[sel],n;
    var mk=function(k){return function(){mv(sel,k);};};
    for(n=1;n<=h;n++){var b=ce('button','hbtn',fa(n));b.onclick=mk(n);bar.appendChild(b);}
    var ba=ce('button','hbtn gold','همه');ba.onclick=mk(h);bar.appendChild(ba);
  }
  app.appendChild(bar);
  var ng=ce('button','newbtn','بازی جدید');ng.setAttribute('data-smoke','1');ng.onclick=function(){newGame();};
  app.appendChild(ng);
  hud('نوبت: '+(st.over?'پایان':(st.turn===0?'شما':'رایانه')));
  $('#hint').textContent='توده‌ای را انتخاب کن و ۱ تا همهٔ مهره‌هایش را بردار؛ هر کس آخرین مهره را بردارد می‌بازد.';
}
function mv(i,n){if(st.over||st.turn!==0)return;if(!L.take(st,i,n))return;sel=-1;draw();if(st.over){setTimeout(end,300);return;}setTimeout(aiTurn,700);}
function aiTurn(){if(st.over)return;var m=L.aiMove(st,null);if(m)L.take(st,m.heap,m.n);draw();if(st.over)setTimeout(end,300);}
function newGame(){st=L.initial();sel=-1;draw();}
function end(){var win=st.loser===1;ovl(win?'بردی!':'باختی!',win?'رایانه آخرین مهره را برداشت؛ آفرین!':'تو آخرین مهره را برداشتی و باختی.','بازی جدید',function(){newGame();});}
draw();
""".strip()

NIM_CSS = r"""
.board{display:flex;flex-direction:column;gap:12px;max-width:560px;margin:0 auto}
.heap{background:#14203a;border:1px solid #2a3a5c;border-radius:14px;padding:12px 14px;cursor:pointer;transition:border-color .15s}
.heap.sel{border-color:#d9a441}
.hname{font-size:13px;color:#8fa3c8;margin-bottom:6px}
.pips{display:flex;flex-wrap:wrap;gap:6px;min-height:16px;align-items:center}
.pip{width:14px;height:14px;border-radius:50%;background:#d9a441;display:inline-block}
.none{color:#5a6b8f;font-size:13px}
.hcount{margin-top:6px;color:#3fb8af;font-size:13px}
.bar{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:14px;min-height:46px;align-items:center}
.msg{color:#8fa3c8;padding:8px}
button{font-family:inherit}
.hbtn{min-width:44px;min-height:44px;border-radius:10px;border:1px solid #2a3a5c;background:#1b2b4d;color:#e8eefc;font-size:16px;cursor:pointer;touch-action:manipulation}
.hbtn.gold{background:#d9a441;color:#14203a;font-weight:700}
.newbtn{display:block;margin:18px auto 0;min-height:44px;padding:0 22px;border-radius:12px;border:1px solid #d9a441;background:transparent;color:#d9a441;font-size:15px;cursor:pointer;touch-action:manipulation}
""".strip()

NIM_TESTS = [
("قانون‌مندی برداشتن", r"""
var st=L.initial();T.eq(st.heaps,[3,5,7]);T.eq(st.turn,0);
T.eq(L.take(st,0,0),false);T.eq(L.take(st,0,4),false);T.eq(L.take(st,3,1),false);T.eq(L.take(st,-1,2),false);
T.ok(L.take(st,0,3)===true);T.eq(st.heaps,[0,5,7]);T.eq(st.turn,1);
T.ok(L.take(st,1,5)===true);T.eq(st.heaps,[0,0,7]);T.eq(st.turn,0);
T.ok(L.take(st,2,7)===true);
T.ok(L.isOver(st)===true);T.eq(L.loser(st),0);
T.eq(L.take(st,0,1),false);
"""),
("راهبرد مِسره در نمونه‌ها", r"""
function mk(h){return{heaps:h,turn:1,over:false,loser:-1};}
function ap(st,m){T.ok(!!m,'move exists');T.ok(L.take(st,m.heap,m.n)===true,'legal move');}
var s1=mk([2,3]);ap(s1,L.aiMove(s1,null));T.eq(s1.heaps,[2,2]);
var s2=mk([1,1,4]);ap(s2,L.aiMove(s2,null));T.eq(s2.heaps,[1,1,1]);
var s3=mk([1,0,3]);ap(s3,L.aiMove(s3,null));T.eq(s3.heaps,[1,0,0]);
var s4=mk([0,1,1]);ap(s4,L.aiMove(s4,null));T.eq(s4.heaps,[0,0,1]);
"""),
("بهینگی AI در همهٔ موقعیت‌های برنده (درخت بازی کامل)", r"""
var memo={};
function win(h){var k=h.join(',');if(memo[k]!==undefined)return memo[k];
  var tot=h[0]+h[1]+h[2];
  if(tot===0){memo[k]=true;return true;}
  var r=false,i,n;
  for(i=0;i<3&&!r;i++)for(n=1;n<=h[i]&&!r;n++){var g=h.slice();g[i]-=n;
    g.sort(function(x,y){return x-y;});if(!win(g))r=true;}
  memo[k]=r;return r;}
function srt(h){return h.slice().sort(function(x,y){return x-y;});}
var cnt=0,a,b,c;
for(a=0;a<=3;a++)for(b=0;b<=5;b++)for(c=0;c<=7;c++){
  if(a+b+c===0)continue;
  var h=[a,b,c];
  if(win(srt(h))){
    cnt++;
    var st={heaps:h,turn:1,over:false,loser:-1};
    var m=L.aiMove(st,null);
    T.ok(!!m&&m.heap>=0&&m.heap<3&&m.n>=1&&m.n<=h[m.heap],'illegal ai move from '+h);
    var g2=st.heaps.slice();g2[m.heap]-=m.n;
    T.ok(win(srt(g2))===false,'AI errs from ['+a+','+b+','+c+']');
  }
}
T.ok(cnt>20,'winning positions: '+cnt);
"""),
("بازی کامل با بذر — AI پیروز می‌شود", r"""
var st=L.initial(),guard=0;
function optsOf(s){var o=[],i,n;for(i=0;i<3;i++)for(n=1;n<=s.heaps[i];n++)o.push([i,n]);return o;}
while(!L.isOver(st)&&guard++<300){
  if(st.turn===0){var o=optsOf(st),mv=o[Math.floor(rng()*o.length)];
    T.ok(L.take(st,mv[0],mv[1])===true,'human move');}
  else{var m=L.aiMove(st,null);T.ok(!!m,'ai move');T.ok(L.take(st,m.heap,m.n)===true,'ai legal');}
}
T.ok(L.isOver(st)===true,'terminated in '+guard+' plies');
T.eq(L.loser(st),0,'AI must win, loser='+L.loser(st));
"""),
]

# ----------------------------- MANCALA (kalah) -----------------------------
MAN_LOGIC = r"""
function mgLegal(st,pl){var a=pl===0?0:7,r=[],i;for(i=a;i<a+6;i++)if(st.p[i]>0)r.push(i);return r;}
function mgEmpty(st,pl){var a=pl===0?0:7,s=0,i;for(i=a;i<a+6;i++)s+=st.p[i];return s===0;}
function mgFinish(st){var pl,i,a,s;for(pl=0;pl<2;pl++){a=pl===0?0:7;s=0;for(i=a;i<a+6;i++){s+=st.p[i];st.p[i]=0;}st.p[pl===0?6:13]+=s;}st.over=true;}
function mgSow(st,pit){
  var pl=st.turn;
  if(st.over||pit<0||pit>13||mgLegal(st,pl).indexOf(pit)<0)return null;
  var p=st.p,my=pl===0?6:13,os=pl===0?13:6,hand=p[pit],extra=false,cap=0;
  p[pit]=0;
  while(hand>0){
    pit=(pit+1)%14;
    if(pit===os)continue;
    p[pit]++;hand--;
    if(hand===0){
      if(pit===my)extra=true;
      else if(pl===0?pit<6:pit>6){
        if(p[pit]===1){var op=12-pit;
          if(p[op]>0){cap=p[op]+1;p[my]+=cap;p[op]=0;p[pit]=0;}}
      }
    }
  }
  if(mgEmpty(st,0)||mgEmpty(st,1))mgFinish(st);
  else if(!extra)st.turn=1-pl;
  return{extra:extra,captured:cap};
}
var WOG_LOGIC={
initial:function(){var p=[],i;for(i=0;i<14;i++)p[i]=(i===6||i===13)?0:4;return{p:p,turn:0,over:false};},
legalPits:mgLegal,
sideEmpty:mgEmpty,
finishGame:mgFinish,
sow:mgSow,
winner:function(st){if(!st.over)return -2;if(st.p[6]>st.p[13])return 0;if(st.p[13]>st.p[6])return 1;return -1;},
aiMove:function(st,rng){
  var pl=st.turn,my=pl===0?6:13,os=pl===0?13:6,pits=mgLegal(st,pl);
  if(!pits.length)return null;
  function cp(s){return{p:s.p.slice(),turn:s.turn,over:s.over};}
  var cands=[],best=-1e9,i;
  for(i=0;i<pits.length;i++){
    var s1=cp(st),r=mgSow(s1,pits[i]);
    if(!r)continue;
    var sc;
    if(s1.over)sc=s1.p[my]-s1.p[os];
    else{
      var op=1-pl,ol=mgLegal(s1,op),bv=-1e9,bs=null,j;
      for(j=0;j<ol.length;j++){var s2=cp(s1);s2.turn=op;mgSow(s2,ol[j]);
        var d=s2.p[os]-s2.p[my];if(d>bv){bv=d;bs=s2;}}
      sc=bs?(bs.p[my]-bs.p[os]):(s1.p[my]-s1.p[os]);
    }
    sc+=0.5*(r.extra?1:0)+0.4*r.captured;
    if(sc>best+1e-9){best=sc;cands=[pits[i]];}
    else if(sc>best-1e-9)cands.push(pits[i]);
  }
  if(!cands.length)return null;
  var pick=cands[0];
  if(rng&&cands.length>1)pick=cands[Math.floor(rng()*cands.length)];
  return{pit:pick,score:best};
}};
""".strip()

MAN_UI = r"""
var st=L.initial();
function pips(n){var s='',i;for(i=0;i<Math.min(n,8);i++)s+='<span class="seed"></span>';return s;}
function storeEl(idx){var d=ce('div','store');d.appendChild(ce('div','cnt',fa(st.p[idx])));d.appendChild(ce('div','spips',pips(st.p[idx])));return d;}
function pitEl(idx){var d=ce('div','pit');d.appendChild(ce('div','cnt',fa(st.p[idx])));d.appendChild(ce('div','spips',pips(st.p[idx])));
  if(!st.over&&st.turn===0&&idx<6&&st.p[idx]>0){d.classList.add('clickable');d.onclick=function(){mv(idx);};}
  return d;}
function draw(){
  var app=$('#app');app.innerHTML='';
  var b=ce('div','mboard');
  b.appendChild(ce('div','plab','گودال‌های رایانه'));
  var top=ce('div','mrow');
  top.appendChild(storeEl(13));
  for(var i=12;i>=7;i--)top.appendChild(pitEl(i));
  b.appendChild(top);
  var bot=ce('div','mrow');
  for(var j=0;j<6;j++)bot.appendChild(pitEl(j));
  bot.appendChild(storeEl(6));
  b.appendChild(bot);
  b.appendChild(ce('div','plab','گودال‌های تو — انبار تو سمت چپ'));
  app.appendChild(b);
  var ng=ce('button','newbtn','بازی جدید');ng.setAttribute('data-smoke','1');ng.onclick=function(){newGame();};
  app.appendChild(ng);
  hud('شما '+fa(st.p[6])+' — رایانه '+fa(st.p[13])+(st.over?' | پایان':' | نوبت: '+(st.turn===0?'شما':'رایانه')));
  $('#hint').textContent='از گودال‌های خودت دانه بپاش؛ آخرین دانه در انبارت = نوبت اضافه، در گودال خالی‌ات = گرفتن دانه‌های روبه‌رو.';
}
function mv(idx){if(st.over||st.turn!==0)return;var r=L.sow(st,idx);if(!r)return;draw();
  if(st.over){setTimeout(end,300);return;}
  if(r.extra){toast('نوبت اضافه!');return;}
  setTimeout(aiTurn,750);}
function aiTurn(){if(st.over)return;var m=L.aiMove(st,null);if(!m)return;var r=L.sow(st,m.pit);draw();
  if(st.over){setTimeout(end,300);return;}
  if(r&&r.extra)setTimeout(aiTurn,750);}
function newGame(){st=L.initial();draw();}
function end(){var w=L.winner(st);
  ovl(w===0?'بردی!':(w===1?'باختی!':'مساوی'),'شما '+fa(st.p[6])+' — رایانه '+fa(st.p[13]),'بازی جدید',function(){newGame();});}
draw();
""".strip()

MAN_CSS = r"""
.mboard{max-width:560px;margin:0 auto;background:#14203a;border:1px solid #2a3a5c;border-radius:16px;padding:12px}
.plab{text-align:center;font-size:12px;color:#8fa3c8;margin:4px 0}
.mrow{display:flex;justify-content:center;gap:8px;margin:8px 0;align-items:center}
.pit{width:52px;min-height:72px;border-radius:12px;background:#0f1a33;border:1px solid #2a3a5c;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:4px;touch-action:manipulation}
.pit.clickable{border-color:#d9a441;cursor:pointer;box-shadow:0 0 0 2px rgba(217,164,65,.25)}
.store{width:58px;min-height:150px;border-radius:14px;background:#0f1a33;border:2px solid #3fb8af;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;margin:0 6px}
.cnt{font-size:18px;font-weight:700;color:#e8eefc}
.store .cnt{color:#3fb8af;font-size:20px}
.spips{display:flex;flex-wrap:wrap;gap:3px;justify-content:center;max-width:44px}
.seed{width:7px;height:7px;border-radius:50%;background:#d9a441;display:inline-block}
button{font-family:inherit}
.newbtn{display:block;margin:16px auto 0;min-height:44px;padding:0 22px;border-radius:12px;border:1px solid #d9a441;background:transparent;color:#d9a441;font-size:15px;cursor:pointer;touch-action:manipulation}
""".strip()

MAN_TESTS = [
("پاشیدن با رد شدن از انبار حریف", r"""
var st=L.initial();st.p[5]=7;st.p[1]=1;
var r=L.sow(st,5);
T.eq(r,{extra:false,captured:0});
T.eq(st.p[13],0,'opponent store must be skipped');
T.eq(st.p[6],1);
T.eq(st.p,[4,1,4,4,4,0,1,5,5,5,5,5,5,0]);
T.eq(st.turn,1);
var st2=L.initial();st2.p[5]=9;st2.p[0]=1;
r=L.sow(st2,5);
T.eq(st2.p[13],0,'skip on wrap too');
T.eq(st2.p[0],2);T.eq(st2.p[1],5);T.eq(st2.p[6],1);
"""),
("نوبت اضافه با آخرین دانه در انبار خودی", r"""
var st=L.initial();
var r=L.sow(st,2);
T.ok(r.extra===true);
T.eq(st.turn,0,'extra keeps turn');
T.eq(st.p[6],1);T.eq(st.p[2],0);T.eq(st.p[3],5);T.eq(st.p[4],5);T.eq(st.p[5],5);
var s2=L.initial();s2.turn=1;
r=L.sow(s2,9);
T.ok(r.extra===true);T.eq(s2.turn,1);T.eq(s2.p[13],1);T.eq(s2.p[6],0);T.eq(s2.p[10],5);
"""),
("قانون گرفتن دانه‌ها (کپچر)", r"""
var st=L.initial();st.p[4]=0;st.p[8]=5;
var r=L.sow(st,0);
T.eq(r.captured,6);
T.eq(st.p[6],6);T.eq(st.p[4],0);T.eq(st.p[8],0);
var s2=L.initial();s2.p[4]=0;s2.p[8]=0;
r=L.sow(s2,0);
T.eq(r.captured,0);T.eq(s2.p[4],1);T.eq(s2.p[6],0);
var s3=L.initial();s3.p[8]=5;
r=L.sow(s3,0);
T.eq(r.captured,0);T.eq(s3.p[4],5);T.eq(s3.p[8],5);
"""),
("جمع‌آوری پایان بازی و برنده", r"""
var st=L.initial(),i;
for(i=0;i<6;i++)st.p[i]=0;
st.p[6]=20;
T.eq(L.sideEmpty(st,0),true);
L.finishGame(st);
T.ok(st.over===true);
T.eq(st.p[13],24);T.eq(st.p[6],20);
T.eq(L.winner(st),1);
var s2=L.initial(),j;
for(j=7;j<13;j++)s2.p[j]=0;
s2.p[13]=6;s2.p[6]=18;
T.eq(L.sideEmpty(s2,1),true);
L.finishGame(s2);
T.eq(s2.p[6],42);T.eq(s2.p[13],6);
T.eq(L.winner(s2),0);
T.eq(L.winner(L.initial()),-2,'not over yet');
"""),
("حرکت‌های مجاز و نامجاز", r"""
var st=L.initial();
T.eq(L.legalPits(st,0),[0,1,2,3,4,5]);
T.eq(L.legalPits(st,1),[7,8,9,10,11,12]);
st.p[3]=0;
T.eq(L.legalPits(st,0),[0,1,2,4,5]);
T.eq(L.sow(st,3),null,'empty pit');
T.eq(L.sow(st,6),null,'store is not a pit');
T.eq(L.sow(st,7),null,'opponent pit');
var over=L.initial();over.over=true;
T.eq(L.sow(over,0),null,'game over');
"""),
("بازی کامل دو AI — پایایی ۴۸ دانه و برندهٔ قاطع", r"""
var st=L.initial(),cur=0,guard=0;
while(!st.over&&guard++<400){
  st.turn=cur;
  var m=L.aiMove(st,rng);
  T.ok(!!m,'ai move at ply '+guard);
  var r=L.sow(st,m.pit);
  T.ok(!!r,'sow ok at ply '+guard);
  var tot=0,i;for(i=0;i<14;i++)tot+=st.p[i];
  T.eq(tot,48,'48 seeds conserved at ply '+guard);
  if(!r.extra)cur=1-cur;
}
T.ok(st.over===true,'game terminated in '+guard+' plies');
var w=L.winner(st);
T.ok(w===0||w===1,'decisive winner, got '+w);
T.ok((w===0?st.p[6]:st.p[13])>=25,'winner seeds >=25: '+(w===0?st.p[6]:st.p[13]));
"""),
]

# ----------------------------- DOTS AND BOXES -----------------------------
DOTS_LOGIC = r"""
function dbBoxLines(b){var r=Math.floor(b/4),c=b%4;return[r*4+c,(r+1)*4+c,20+r*5+c,21+r*5+c];}
function dbAdj(i){var out=[];
  if(i<20){var r=Math.floor(i/4),c=i%4;
    if(r<4)out.push(r*4+c);
    if(r>0)out.push((r-1)*4+c);
  }else{var v=i-20;r=Math.floor(v/5);c=v%5;
    if(c<4)out.push(r*4+c);
    if(c>0)out.push(r*4+c-1);}
  out.sort(function(a,b){return a-b;});return out;}
function dbSides(st,b){var l=dbBoxLines(b),s=0,i;for(i=0;i<4;i++)if(st.lines[l[i]])s++;return s;}
var WOG_LOGIC={
initial:function(){var l=[],b=[],i;for(i=0;i<40;i++)l.push(0);for(i=0;i<16;i++)b.push(0);
  return{lines:l,boxes:b,turn:1,over:false};},
adjBoxes:dbAdj,
boxLines:dbBoxLines,
boxSides:dbSides,
boxOwner:function(st,b){return st.boxes[b];},
score:function(st){var h=0,a=0,i;for(i=0;i<16;i++){if(st.boxes[i]===1)h++;else if(st.boxes[i]===2)a++;}return[h,a];},
claimLine:function(st,id,pl){
  if(st.over||id<0||id>39||st.lines[id]||pl!==st.turn)return null;
  st.lines[id]=pl;
  var adj=dbAdj(id),done=[],i;
  for(i=0;i<adj.length;i++){var b=adj[i];
    if(!st.boxes[b]&&dbSides(st,b)===4){st.boxes[b]=pl;done.push(b);}}
  var left=0;for(i=0;i<40;i++)if(!st.lines[i])left++;
  if(left===0)st.over=true;
  else if(!done.length)st.turn=(pl===1?2:1);
  return{boxes:done,extra:done.length>0};
},
isOver:function(st){return !!st.over;},
aiMove:function(st,rng){
  var un=[],i;
  for(i=0;i<40;i++)if(!st.lines[i])un.push(i);
  if(!un.length)return null;
  var comp=[],safe=[],risky=[],j;
  for(i=0;i<un.length;i++){
    var id=un[i],adj=dbAdj(id),c=false,sf=true,d=0;
    for(j=0;j<adj.length;j++){var b=adj[j];
      if(st.boxes[b])continue;
      var s=dbSides(st,b);
      if(s===3)c=true;
      if(s>=2){sf=false;d++;}}
    if(c)comp.push(id);else if(sf)safe.push(id);else risky.push({id:id,d:d});
  }
  var pool;
  if(comp.length)pool=comp;
  else if(safe.length)pool=safe;
  else{var m=1e9;
    for(i=0;i<risky.length;i++)if(risky[i].d<m)m=risky[i].d;
    pool=[];for(i=0;i<risky.length;i++)if(risky[i].d===m)pool.push(risky[i].id);}
  var pick=pool[0];
  if(rng&&pool.length>1)pick=pool[Math.floor(rng()*pool.length)];
  return{line:pick,kind:comp.length?'comp':(safe.length?'safe':'risk')};
}};
""".strip()

DOTS_UI = r"""
var st=L.initial();
function lineBtn(id,dir){var b=ce('button','dline '+dir+(st.lines[id]?' p'+st.lines[id]:''));
  if(!st.lines[id]&&st.turn===1&&!st.over)b.onclick=function(){mv(id);};
  return b;}
function draw(){
  var app=$('#app');app.innerHTML='';
  var wrap=ce('div','dwrap'),g=ce('div','dgrid'),r,c;
  for(r=0;r<9;r++)for(c=0;c<9;c++){
    var cell;
    if(r%2===0&&c%2===0){cell=ce('div','dcell');cell.appendChild(ce('span','ddot'));}
    else if(r%2===0){cell=ce('div','dcell');cell.appendChild(lineBtn((r/2)*4+(c-1)/2,'h'));}
    else if(c%2===0){cell=ce('div','dcell');cell.appendChild(lineBtn(20+((r-1)/2)*5+c/2,'v'));}
    else{var bx=((r-1)/2)*4+((c-1)/2),ow=st.boxes[bx];
      cell=ce('div','dcell dbox'+(ow?' own'+ow:''));
      cell.appendChild(ce('span','bmark',ow===1?'تو':(ow===2?'رایانه':'')));}
    g.appendChild(cell);}
  wrap.appendChild(g);app.appendChild(wrap);
  var ng=ce('button','newbtn','بازی جدید');ng.setAttribute('data-smoke','1');ng.onclick=function(){newGame();};
  app.appendChild(ng);
  var sc=L.score(st);
  hud('شما '+fa(sc[0])+' — رایانه '+fa(sc[1])+(st.over?' | پایان':' | نوبت: '+(st.turn===1?'شما':'رایانه')));
  $('#hint').textContent='خط خالی را لمس کن؛ ضلع آخرِ هر کادر را بگذاری کادر مال توست و یک نوبت اضافه می‌گیری.';
}
function mv(id){if(st.over||st.turn!==1)return;var r=L.claimLine(st,id,1);if(!r)return;draw();
  if(st.over){setTimeout(end,300);return;}
  if(r.extra){if(r.boxes.length)toast('کادر گرفتی! نوبت اضافه');return;}
  setTimeout(aiTurn,600);}
function aiTurn(){if(st.over)return;var m=L.aiMove(st,null);if(!m)return;var r=L.claimLine(st,m.line,2);draw();
  if(r&&r.boxes.length)toast('رایانه کادر گرفت');
  if(st.over){setTimeout(end,300);return;}
  if(r&&r.extra)setTimeout(aiTurn,600);}
function newGame(){st=L.initial();draw();}
function end(){var sc=L.score(st),d=sc[0]-sc[1];
  ovl(d>0?'بردی!':(d<0?'باختی!':'مساوی'),'شما '+fa(sc[0])+' کادر — رایانه '+fa(sc[1])+' کادر','بازی جدید',function(){newGame();});}
draw();
""".strip()

DOTS_CSS = r"""
.dwrap{direction:ltr;display:flex;justify-content:center;overflow-x:auto;padding:8px 0}
.dgrid{display:grid;gap:2px}
.dcell{display:flex;align-items:center;justify-content:center}
.ddot{width:8px;height:8px;border-radius:50%;background:#8fa3c8}
.dline{border:none;border-radius:4px;background:#2a3a5c;cursor:pointer;touch-action:manipulation;padding:0}
.dline.h{width:40px;height:16px}
.dline.v{width:16px;height:40px}
.dline.p1{background:#3fb8af;cursor:default}
.dline.p2{background:#e26d5c;cursor:default}
.dline:not(.p1):not(.p2):hover{background:#d9a441}
.dbox{width:40px;height:40px;border-radius:6px;background:rgba(20,32,58,.5)}
.dbox.own1{background:rgba(63,184,175,.22);border:1px solid #3fb8af}
.dbox.own2{background:rgba(226,109,92,.2);border:1px solid #e26d5c}
.bmark{font-size:10px;color:#cfe3ff}
button{font-family:inherit}
.newbtn{display:block;margin:16px auto 0;min-height:44px;padding:0 22px;border-radius:12px;border:1px solid #d9a441;background:transparent;color:#d9a441;font-size:15px;cursor:pointer;touch-action:manipulation}
""".strip()

DOTS_TESTS = [
("مجاورت خط و کادر (گوشه، لبه، مرکز)", r"""
T.eq(L.adjBoxes(0),[0]);T.eq(L.adjBoxes(20),[0]);
T.eq(L.adjBoxes(3),[3]);T.eq(L.adjBoxes(24),[3]);
T.eq(L.adjBoxes(16),[12]);T.eq(L.adjBoxes(19),[15]);
T.eq(L.adjBoxes(35),[12]);T.eq(L.adjBoxes(39),[15]);
T.eq(L.adjBoxes(4),[0,4]);T.eq(L.adjBoxes(9),[5,9]);
T.eq(L.adjBoxes(21),[0,1]);T.eq(L.adjBoxes(26),[4,5]);
T.eq(L.boxLines(0),[0,4,20,21]);
T.eq(L.boxLines(5),[5,9,26,27]);
T.eq(L.boxLines(15),[15,19,38,39]);
"""),
("تکمیل کادر، نوبت اضافه و اعتبارسنجی", r"""
var st=L.initial();
T.eq(L.claimLine(st,0,1),{boxes:[],extra:false});
T.eq(st.turn,2);
T.eq(L.claimLine(st,4,2),{boxes:[],extra:false});
T.eq(st.turn,1);
T.eq(L.claimLine(st,20,1),{boxes:[],extra:false});
T.eq(L.claimLine(st,21,1),null,'occupied line');
T.eq(L.claimLine(st,1,1),null,'wrong player');
var r=L.claimLine(st,21,2);
T.eq(r,{boxes:[0],extra:true});
T.eq(L.boxOwner(st,0),2);T.eq(st.turn,2,'extra keeps turn');
T.eq(L.score(st),[0,1]);
T.eq(L.claimLine(st,1,1),null,'wrong player while turn=2');
T.eq(L.claimLine(st,1,2),{boxes:[],extra:false});
T.eq(st.turn,1,'turn passed');
"""),
("کادر دوتایی با یک خط", r"""
var st=L.initial(),seq=[[0,1],[1,2],[4,1],[5,2],[20,1],[22,2]],i;
for(i=0;i<seq.length;i++)T.ok(L.claimLine(st,seq[i][0],seq[i][1])!==null,'claim '+seq[i][0]);
var r=L.claimLine(st,21,1);
T.eq(r,{boxes:[0,1],extra:true});
T.eq(L.score(st),[2,0]);
"""),
("بازی کامل با بذر — ۴۰ خط، ۱۶ کادر، پایان", r"""
var st=L.initial(),moves=0;
while(!L.isOver(st)&&moves<60){
  if(st.turn===1){var opts=[],i;
    for(i=0;i<40;i++)if(!st.lines[i])opts.push(i);
    T.ok(L.claimLine(st,opts[Math.floor(rng()*opts.length)],1)!==null,'human claim');}
  else{var m=L.aiMove(st,rng);
    T.ok(!!m&&L.claimLine(st,m.line,2)!==null,'ai claim');}
  moves++;}
T.ok(L.isOver(st)===true,'terminated in '+moves);
T.eq(moves,40);
var i2;for(i2=0;i2<40;i2++)T.ok(st.lines[i2]!==0,'line '+i2+' unclaimed');
var sc=L.score(st);T.eq(sc[0]+sc[1],16);
var b2;for(b2=0;b2<16;b2++)T.ok(st.boxes[b2]!==0,'box '+b2+' unowned');
"""),
("AI هرگز کادر سه‌ضلعی را باز نمی‌کند وقتی خط امن هست (۵۰ وضعیت)", r"""
var checked=0,guard=0;
while(checked<50&&guard++<400){
  var st=L.initial(),k=6+Math.floor(rng()*12),i;
  for(i=0;i<k;i++){var un=[],j;
    for(j=0;j<40;j++)if(!st.lines[j])un.push(j);
    if(!un.length)break;
    L.claimLine(st,un[Math.floor(rng()*un.length)],st.turn);}
  if(st.over)continue;
  var safe=[];
  for(i=0;i<40;i++)if(!st.lines[i]){
    var adj=L.adjBoxes(i),ok=true;
    for(var j2=0;j2<adj.length;j2++){var b=adj[j2];
      if(!st.boxes[b]&&L.boxSides(st,b)>=2){ok=false;break;}}
    if(ok)safe.push(i);}
  if(!safe.length)continue;
  st.turn=2;
  var m=L.aiMove(st,rng);
  T.ok(!!m,'ai move exists');
  checked++;
  var comp=false,adj2=L.adjBoxes(m.line);
  for(var j3=0;j3<adj2.length;j3++){var b3=adj2[j3];
    if(!st.boxes[b3]&&L.boxSides(st,b3)===3)comp=true;}
  T.ok(safe.indexOf(m.line)>=0||comp===true,'AI opened a 3-sided box (game '+guard+')');
}
T.ok(checked>=50,'checked '+checked+' states');
"""),
]

GAMES=[
 G(slug="nim", title="نیم", cat="board", icon="🪨", g1="#d9a441", g2="#3fb8af",
   desc="نیمِ مِسره با سه تودهٔ ۳، ۵ و ۷ مهره‌ای؛ هر بار از یک توده چند مهره (یا همه) بردار — ولی مواظب باش: هر کس آخرین مهره را بردارد می‌بازد! رایانه بی‌نقص بازی می‌کند.",
   hint="توده‌ای را انتخاب کن و مهره بردار؛ هر کس آخرین مهره را بردارد می‌بازد.",
   logic=NIM_LOGIC, ui=NIM_UI, css=NIM_CSS, engines=("common",), tests=NIM_TESTS, seed=12345),
 G(slug="mancala", title="منقله", cat="board", icon="🐚", g1="#3fb8af", g2="#d9a441",
   desc="منقلهٔ کلاسیک با ۱۲ گودال و ۴۸ دانه؛ دانه‌ها را در جهت پادساعتگرد بپاش، با افتادن آخرین دانه در انبارت نوبت اضافه بگیر و دانه‌های حریف را بگیر. بیشترین دانه برنده است.",
   hint="از گودال‌های خودت دانه بپاش؛ آخرین دانه در انبارت = نوبت اضافه، در گودال خالی‌ات = گرفتن دانه‌های روبه‌رو.",
   logic=MAN_LOGIC, ui=MAN_UI, css=MAN_CSS, engines=("common",), tests=MAN_TESTS, seed=12345),
 G(slug="dots-boxes", title="نقطه و خط", cat="board", icon="✒️", g1="#e26d5c", g2="#3fb8af",
   desc="نقطه و خط روی شبکهٔ ۴×۴؛ خط بکش و کادر بساز — هر کادرِ کامل یک امتیاز و یک نوبت اضافه دارد. در پایان بیشترین کادر برنده است.",
   hint="خط خالی را لمس کن؛ ضلع آخرِ هر کادر را بگذاری کادر مال توست و نوبت اضافه می‌گیری.",
   logic=DOTS_LOGIC, ui=DOTS_UI, css=DOTS_CSS, engines=("common",), tests=DOTS_TESTS, seed=12345),
]
