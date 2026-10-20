# -*- coding: utf-8 -*-
"""D1 board batch: ludo + snakes-ladders + dominoes — Persian WOG mini-kit contract (cat=board, engines=common)."""
from lib_mini import G

# =====================================================================
# 1) LUDO — human red vs AI blue, 4 pawns, 52-cell shared track
#    pawn state: -1 = base, 0..50 = main track (51 cells), 51..55 = home column, 56 = home
# =====================================================================
LUDO_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
var HOME=56;
function roll(rng){return 1+Math.floor((rng||Math.random)()*6);}
function startCell(pl){return pl===0?0:26;}
function trackPos(pl,p){return (startCell(pl)+p)%52;}
function initial(){return {turn:0,sixes:0,pawns:[[-1,-1,-1,-1],[-1,-1,-1,-1]]};}
function legalPawnMoves(st,pl,d){var out=[],P=st.pawns[pl],i;for(i=0;i<4;i++){if(P[i]===-1){if(d===6){out.push(i);}}else if(P[i]+d<=HOME){out.push(i);}}return out;}
function captureAt(st,pl,cell){var opp=1-pl,OP=st.pawns[opp],out=[],j;if(cell===0||cell===26){return out;}for(j=0;j<4;j++){if(OP[j]>=0&&OP[j]<=50&&trackPos(opp,OP[j])===cell){out.push(j);}}return out;}
function applyMove(st,pl,pi,d){var P=st.pawns[pl],p=P[pi],cap=false,j;if(p===-1){if(d!==6){throw new Error('need6');}p=0;}else{if(p+d>HOME){throw new Error('overshoot');}p+=d;}P[pi]=p;if(p<=50){var v=captureAt(st,pl,trackPos(pl,p));for(j=0;j<v.length;j++){st.pawns[1-pl][v[j]]=-1;cap=true;}}if(d===6){st.sixes++;}else{st.sixes=0;}var extra=(d===6&&st.sixes<3);if(!extra){st.sixes=0;st.turn=1-pl;}return {captured:cap,extra:extra,finished:p===HOME};}
function endTurn(st){st.sixes=0;st.turn=1-st.turn;}
function aiChoose(st,d,rng,mv){mv=mv||legalPawnMoves(st,st.turn,d);if(!mv.length){return -1;}var r=rng||Math.random,pl=st.turn,P=st.pawns[pl],caps=[],exits=[],i,pi,p,v;for(i=0;i<mv.length;i++){pi=mv[i];p=P[pi]===-1?0:P[pi]+d;if(P[pi]===-1){exits.push(pi);}if(p<=50){v=captureAt(st,pl,trackPos(pl,p));if(v.length){caps.push(pi);}}}function pk(a){return a[Math.floor(r()*a.length)];}if(caps.length){return pk(caps);}if(exits.length){return pk(exits);}var best=mv[0];for(i=1;i<mv.length;i++){if(P[mv[i]]>P[best]){best=mv[i];}}return best;}
function applyRoll(st,d,pick,rng){if(d===6&&st.sixes>=2){endTurn(st);return {passed:true,threeSix:true};}var mv=legalPawnMoves(st,st.turn,d);if(!mv.length){endTurn(st);return {passed:true};}var pi=pick?pick(mv):aiChoose(st,d,rng,mv);return {passed:false,pawn:pi,move:applyMove(st,st.turn,pi,d)};}
function isWin(st,pl){var P=st.pawns[pl],i;for(i=0;i<4;i++){if(P[i]!==HOME){return false;}}return true;}
return {roll:roll,startCell:startCell,trackPos:trackPos,initial:initial,legalPawnMoves:legalPawnMoves,applyMove:applyMove,endTurn:endTurn,aiChoose:aiChoose,applyRoll:applyRoll,isWin:isWin,captureAt:captureAt,HOME:HOME};
})();
"""

LUDO_UI = r"""
var app=document.getElementById('app');
var DIE=['⚀','⚁','⚂','⚃','⚄','⚅'];
var st=null,myDice=0,myMoves=[],lastD=0,seq=0,timer=null;
function homeCount(pl){var n=0,i;for(i=0;i<4;i++){if(st.pawns[pl][i]===56){n++;}}return n;}
function pawnSpan(pl,pi,mv){return '<span class="pn p'+pl+(mv?' mv':'')+'" data-pi="'+pi+'">'+fa(pi+1)+'</span>';}
function basePanel(bpl){var s='<div class="pbase pb'+bpl+'"><b>'+(bpl===0?'پایگاه شما (قرمز)':'پایگاه ربات (آبی)')+'</b><div class="slots">',pi,p;for(pi=0;pi<4;pi++){p=st.pawns[bpl][pi];var mv=(bpl===0&&st.turn===0&&myDice>0&&myMoves.indexOf(pi)>=0);s+='<div class="slot">'+(p===-1?pawnSpan(bpl,pi,mv):'')+'</div>';}return s+'</div></div>';}
function homeStrip(hpl){var s='<div class="hstrip"><b>'+(hpl===0?'ستون خانهٔ شما':'ستون خانهٔ ربات')+'</b>',k,pi;for(k=51;k<=55;k++){s+='<div class="hc">';for(pi=0;pi<4;pi++){if(st.pawns[hpl][pi]===k){s+=pawnSpan(hpl,pi,false);}}s+='</div>';}s+='<div class="hc fh">';for(pi=0;pi<4;pi++){if(st.pawns[hpl][pi]===56){s+=pawnSpan(hpl,pi,false);}}return s+'</div></div>';}
function render(){
  var i,j,pl,pi,p,t='<div class="ltrack" dir="ltr">',byCell={};
  for(pl=0;pl<2;pl++){for(pi=0;pi<4;pi++){p=st.pawns[pl][pi];if(p>=0&&p<=50){var c=L.trackPos(pl,p);if(!byCell[c]){byCell[c]=[];}byCell[c].push([pl,pi]);}}}
  for(i=0;i<52;i++){
    t+='<div class="tc'+(i===0?' s0':(i===26?' s1':''))+'">'+((i===0||i===26)?'<i>شروع</i>':'');
    var cps=byCell[i]||[];
    for(j=0;j<cps.length;j++){var m=cps[j],mv=(m[0]===0&&st.turn===0&&myDice>0&&myMoves.indexOf(m[1])>=0);t+=pawnSpan(m[0],m[1],mv);}
    t+='</div>';
  }
  t+='</div>';
  app.innerHTML=basePanel(0)+t+homeStrip(0)+homeStrip(1)+basePanel(1)+
    '<div class="lctl"><button id="rollBtn" data-smoke class="btn">تاس بریز</button><span class="die">'+(lastD?DIE[lastD-1]:'—')+'</span><button id="ngBtn" data-smoke class="btn ghost">بازی جدید</button></div>';
  var els=app.querySelectorAll('.pn.mv'),k2;
  for(k2=0;k2<els.length;k2++){els[k2].onclick=function(){humanMove(+this.getAttribute('data-pi'));};}
  $('#rollBtn').onclick=humanRoll;
  $('#ngBtn').onclick=newGame;
}
function hudUpd(){hud('نوبت: <b>'+(st.turn===0?'شما (قرمز)':'ربات (آبی)')+'</b> · تاس: '+(lastD?DIE[lastD-1]:'—')+' · خانه: شما '+fa(homeCount(0))+' / ربات '+fa(homeCount(1)));}
function newGame(){
  if(timer){clearTimeout(timer);timer=null;}
  seq++;st=L.initial();myDice=0;myMoves=[];lastD=0;
  $('#hint').textContent='با ۶ مهره از پایگاه بیرون می‌آید؛ ۵۱ خانهٔ مسیر مشترک سپس ستون خانه. ورود به خانهٔ آخر عدد دقیق می‌خواهد.';
  render();hudUpd();toast('لیدو: تو قرمزی — برای شروع ۶ بیاور');
}
function humanRoll(){
  if(!st||st.turn!==0||myDice>0||L.isWin(st,0)||L.isWin(st,1)){return;}
  var d=L.roll();lastD=d;
  if(d===6&&st.sixes>=2){L.endTurn(st);render();hudUpd();toast('سه شش پشت‌سرهم! نوبت ربات');aiTurn();return;}
  myDice=d;myMoves=L.legalPawnMoves(st,0,d);
  if(!myMoves.length){L.endTurn(st);myDice=0;render();hudUpd();toast('با '+fa(d)+' حرکتی نداشتی — نوبت ربات');aiTurn();return;}
  render();hudUpd();toast('مهرهٔ دارای حاشیهٔ طلایی را بزن');
}
function humanMove(pi){
  if(!st||st.turn!==0||!myDice||myMoves.indexOf(pi)<0){return;}
  var r=L.applyMove(st,0,pi,myDice);
  myDice=0;myMoves=[];
  if(r.captured){toast('گرفتی! مهرهٔ ربات به پایگاه برگشت');}
  if(r.finished){toast('یک مهره به خانه رسید');}
  if(L.isWin(st,0)){render();ovl('بردی!','هر چهار مهره‌ات به خانه رسیدند','بازی جدید',newGame);return;}
  if(r.extra){render();hudUpd();toast('شش! دوباره بریز');return;}
  render();hudUpd();aiTurn();
}
function aiTurn(){
  var my=++seq;
  timer=setTimeout(function step(){
    if(my!==seq||!st){return;}
    var d=L.roll();lastD=d;hudUpd();
    if(d===6&&st.sixes>=2){L.endTurn(st);render();hudUpd();toast('ربات: سه شش — نوبت شما');return;}
    var mv=L.legalPawnMoves(st,1,d);
    if(!mv.length){L.endTurn(st);render();hudUpd();toast('ربات حرکتی نداشت — نوبت شما');return;}
    timer=setTimeout(function(){
      if(my!==seq||!st){return;}
      var pi=L.aiChoose(st,d,Math.random,mv);
      var r=L.applyMove(st,1,pi,d);
      if(r.captured){toast('ربات مهرهٔ تو را گرفت!');}
      if(r.finished){toast('ربات: مهره‌ای به خانه رسید');}
      if(L.isWin(st,1)){render();ovl('باختی!','ربات زودتر همه را به خانه رساند','بازی جدید',newGame);return;}
      if(r.extra){render();hudUpd();timer=setTimeout(step,550);return;}
      render();hudUpd();toast('نوبت شما — تاس بریز');
    },700);
  },700);
}
newGame();
"""

LUDO_CSS = r"""
body{margin:0;background:#0b1526;color:#e8edf7;font-family:Vazirmatn,Tahoma,sans-serif}
#app{max-width:780px;margin:0 auto;padding:8px 10px 30px}
.ltrack{display:grid;grid-template-columns:repeat(13,1fr);gap:3px;background:#14203a;padding:6px;border-radius:12px}
.tc{position:relative;min-height:34px;background:#0e1930;border:1px solid #223252;border-radius:6px;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:1px}
.tc i{position:absolute;top:1px;right:3px;font-size:8px;color:#d9a441;font-style:normal;opacity:.85}
.tc.s0{background:#2a1418;border-color:#e26d5c}
.tc.s1{background:#101c33;border-color:#4a7bd0}
.pn{display:inline-flex;width:17px;height:17px;border-radius:50%;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#101828}
.p0{background:#e26d5c}
.p1{background:#4a7bd0;color:#fff}
.pn.mv{outline:2px solid #d9a441;cursor:pointer}
.hstrip{display:flex;align-items:center;gap:4px;margin:8px 0;background:#14203a;padding:6px 10px;border-radius:12px;flex-wrap:wrap}
.hstrip b{font-size:12px;color:#9fb3d9;min-width:96px}
.hc{min-width:30px;height:30px;border:1px dashed #2a3a5c;border-radius:6px;display:flex;align-items:center;justify-content:center;gap:1px}
.hc.fh{border-style:solid;border-color:#67b98a}
.pbase{background:#14203a;border-radius:12px;padding:8px 12px;margin:8px 0;display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.pbase b{font-size:13px;color:#d9a441}
.pb1 b{color:#9fc0ff}
.slots{display:flex;gap:6px}
.slot{width:24px;height:24px;border:1px dashed #2a3a5c;border-radius:50%;display:flex;align-items:center;justify-content:center}
.lctl{display:flex;gap:12px;align-items:center;justify-content:center;margin:12px 0}
.btn{background:#d9a441;border:0;color:#14203a;font-weight:700;padding:10px 20px;border-radius:10px;font-size:15px;min-height:42px;touch-action:manipulation;font-family:inherit}
.btn.ghost{background:#1d2c4d;color:#e8edf7}
.btn:active{transform:scale(.97)}
.die{font-size:34px;color:#d9a441;min-width:44px;text-align:center;line-height:1}
"""

LUDO_TESTS = [
    ("خروج از پایگاه فقط با ۶", r"""
var st=L.initial();
T.eq(L.legalPawnMoves(st,0,3),[],'هیچ مهره‌ای با ۳ بیرون نمی‌آید');
T.eq(L.legalPawnMoves(st,0,6),[0,1,2,3],'با ۶ هر چهار مهره قابل خروج');
T.throws(function(){L.applyMove(st,0,2,3);},'خروج بدون ۶ ممنوع');
T.eq(st.pawns[0],[-1,-1,-1,-1],'پایگاه قرمز دست‌نخورده');
T.eq(st.pawns[1],[-1,-1,-1,-1],'پایگاه آبی دست‌نخورده');
"""),
    ("ورود دقیق به خانه", r"""
var st=L.initial();
st.pawns[0]=[53,-1,-1,-1];
T.ok(L.legalPawnMoves(st,0,3).indexOf(0)>=0,'۵۳+۳=۵۶ مجاز');
st.pawns[0][0]=54;
T.ok(L.legalPawnMoves(st,0,3).indexOf(0)<0,'۵۴+۳=۵۷ غیرمجاز');
T.ok(L.legalPawnMoves(st,0,2).indexOf(0)>=0,'۵۴+۲=۵۶ مجاز');
T.throws(function(){L.applyMove(st,0,0,3);},'عبور از خانه ممنوع');
var r=L.applyMove(st,0,0,2);
T.ok(r.finished,'پرچم پایان');
T.eq(st.pawns[0][0],56,'مهره در خانه');
T.ok(!L.isWin(st,0),'با یک مهره برد نیست');
st.pawns[0]=[56,56,56,56];
T.ok(L.isWin(st,0),'برد با چهار مهره در خانه');
"""),
    ("گرفتن مهره و خانه‌های امن", r"""
var st=L.initial();
st.pawns[0]=[8,-1,-1,-1];st.pawns[1]=[36,-1,-1,-1];
var r=L.applyMove(st,0,0,2);
T.ok(r.captured,'مهرهٔ ربات گرفته شد');
T.eq(st.pawns[1][0],-1,'ربات به پایگاه برگشت');
var st2=L.initial();
st2.pawns[0]=[24,-1,-1,-1];st2.pawns[1]=[0,-1,-1,-1];
T.ok(!L.applyMove(st2,0,0,2).captured,'خانهٔ شروع آبی امن است');
var st3=L.initial();
st3.pawns[0]=[26,-1,-1,-1];st3.pawns[1]=[-1,3,-1,-1];
var r3=L.applyMove(st3,1,1,6);
T.ok(!r3.captured,'خانهٔ شروع قرمز هم امن');
T.ok(r3.extra,'شش نوبت اضافه می‌دهد');
"""),
    ("قانون سه شش", r"""
var st=L.initial();
T.ok(L.applyMove(st,0,0,6).extra,'شش اول اضافه می‌دهد');
T.ok(L.applyMove(st,0,1,6).extra,'شش دوم اضافه می‌دهد');
var rr=L.applyRoll(st,6,null);
T.ok(rr.passed&&rr.threeSix,'شش سوم نوبت را رد می‌کند');
T.eq(st.turn,1,'نوبت به ربات رسید');
T.eq(st.sixes,0,'شمارندهٔ شش صفر شد');
T.eq([st.pawns[0][2],st.pawns[0][3]],[-1,-1],'مهرهٔ سوم حرکت نکرد');
var st2=L.initial();
L.applyMove(st2,0,0,6);L.applyMove(st2,0,0,6);
var r3=L.applyMove(st2,0,0,6);
T.ok(!r3.extra,'سومین شش اضافه نمی‌دهد');
T.eq(st2.turn,1,'پس از شش سوم نوبت عوض می‌شود');
"""),
    ("بازی کامل دو ربات زیر ۲۰۰۰ نوبت", r"""
var st=L.initial(),plies=0,winner=-1;
while(plies<2000){
  if(L.isWin(st,0)){winner=0;break;}
  if(L.isWin(st,1)){winner=1;break;}
  var d=L.roll(rng);
  L.applyRoll(st,d,function(mv){return L.aiChoose(st,d,rng,mv);});
  plies++;
}
T.ok(winner>=0,'بازی تمام شد در '+plies+' نوبت');
T.ok(plies<=2000,'زیر ۲۰۰۰ نوبت');
T.ok(L.isWin(st,winner),'برنده چهار مهره در خانه دارد');
T.ok(!L.isWin(st,1-winner),'بازنده برنده نیست');
"""),
    ("سلامت وضعیت مهره‌ها", r"""
var st=L.initial(),plies=0,ok=true,i,pl;
function valid(v){return v===-1||(v>=0&&v<=56);}
while(plies<1500&&!L.isWin(st,0)&&!L.isWin(st,1)){
  var d=L.roll(rng);
  L.applyRoll(st,d,function(mv){return L.aiChoose(st,d,rng,mv);});
  for(pl=0;pl<2;pl++){for(i=0;i<4;i++){if(!valid(st.pawns[pl][i])){ok=false;}}}
  plies++;
}
T.ok(ok,'هر مهره همیشه در base یا ۰..۵۶ است');
T.ok(L.isWin(st,0)||L.isWin(st,1),'بازی به سرانجام رسید');
T.eq(L.trackPos(0,10),10,'مسیر قرمز از شروع صفر');
T.eq(L.trackPos(1,26),0,'مسیر آبی دور می‌زند');
"""),
]

# =====================================================================
# 2) SNAKES & LADDERS — human vs AI race to exactly 100
# =====================================================================
SL_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
var LADDERS={4:25,13:46,33:49,42:63,50:69,62:81,74:92,6:17};
var SNAKES={27:5,40:3,43:18,54:31,66:45,76:58,89:53,99:41};
function transport(c){var prev=-1;while(prev!==c){prev=c;if(LADDERS[c]!==undefined){c=LADDERS[c];}else if(SNAKES[c]!==undefined){c=SNAKES[c];}}return c;}
function initial(){return {pos:[0,0],turn:0};}
function roll(rng){return 1+Math.floor((rng||Math.random)()*6);}
function move(st,pl,d){var from=st.pos[pl],to=from+d,transported=false,moved=true;if(to>100){moved=false;to=from;}else{var t=transport(to);transported=(t!==to);to=t;}st.pos[pl]=to;st.turn=1-pl;return {from:from,to:to,moved:moved,transported:transported};}
function isWin(st,pl){return st.pos[pl]===100;}
return {LADDERS:LADDERS,SNAKES:SNAKES,transport:transport,initial:initial,roll:roll,move:move,isWin:isWin};
})();
"""

SL_UI = r"""
var app=document.getElementById('app');
var DIE=['⚀','⚁','⚂','⚃','⚄','⚅'];
var st=null,lastD=0,busy=false,timer=null;
function newGame(){
  if(timer){clearTimeout(timer);timer=null;}
  busy=false;st=L.initial();lastD=0;
  $('#hint').textContent='دقیقاً روی ۱۰۰ بایست؛ سرِ پله بالا می‌برد و سرِ مار پایین می‌کشد.';
  render();hudUpd();toast('مار و پله: تو قرمز، ربات آبی — به ۱۰۰ برس');
}
function hudUpd(){hud('نوبت: <b>'+(st.turn===0?'شما':'ربات')+'</b> · تاس: '+(lastD?DIE[lastD-1]:'—')+' · امتیاز: شما '+fa(st.pos[0])+' / ربات '+fa(st.pos[1]));}
function render(){
  var h='<div class="slwrap" dir="ltr"><div class="slboard">',n;
  for(n=1;n<=100;n++){
    var b=Math.floor((n-1)/10),off=(n-1)%10,col=(b%2===0)?off+1:10-off,row=10-b;
    var lad=L.LADDERS[n]!==undefined,snk=L.SNAKES[n]!==undefined;
    var cls='sc'+(lad?' lad':(snk?' snk':''));
    var inner='<span class="num">'+fa(n)+'</span>';
    if(lad){inner+='<span class="mk up">▲'+fa(L.LADDERS[n])+'</span>';}
    if(snk){inner+='<span class="mk dn">▼'+fa(L.SNAKES[n])+'</span>';}
    if(st.pos[0]===n){inner+='<span class="pp p0">ش</span>';}
    if(st.pos[1]===n){inner+='<span class="pp p1">ر</span>';}
    h+='<div class="'+cls+'" style="grid-area:'+row+' / '+col+'">'+inner+'</div>';
  }
  h+='</div></div>';
  h+='<div class="slctl"><button id="rollBtn" data-smoke class="btn">تاس بریز</button><span class="die">'+(lastD?DIE[lastD-1]:'—')+'</span><button id="ngBtn" data-smoke class="btn ghost">بازی جدید</button></div>';
  app.innerHTML=h;
  $('#rollBtn').onclick=humanRoll;
  $('#ngBtn').onclick=newGame;
}
function humanRoll(){
  if(!st||busy||st.turn!==0){return;}
  busy=true;
  var d=L.roll();lastD=d;
  var r=L.move(st,0,d);
  render();hudUpd();
  if(!r.moved){toast('بیش از ۱۰۰! حرکت نکردی');}
  else if(r.transported){toast(r.to>r.from?('پله! به '+fa(r.to)+' پریدی'):('مار! تا '+fa(r.to)+' سقوط کردی'));}
  if(L.isWin(st,0)){ovl('بردی!','دقیقاً روی ۱۰۰ ایستادی','بازی جدید',newGame);return;}
  timer=setTimeout(aiStep,800);
}
function aiStep(){
  if(!st){return;}
  var d=L.roll();lastD=d;
  var r=L.move(st,1,d);
  render();hudUpd();
  if(!r.moved){toast('ربات: بیش از ۱۰۰ — نیامد');}
  else if(r.transported){toast(r.to>r.from?('ربات پله رفت: '+fa(r.to)):('ربات مار خورد: '+fa(r.to)));}
  if(L.isWin(st,1)){ovl('باختی!','ربات زودتر به ۱۰۰ رسید','بازی جدید',newGame);return;}
  busy=false;hudUpd();
}
newGame();
"""

SL_CSS = r"""
body{margin:0;background:#0b1526;color:#e8edf7;font-family:Vazirmatn,Tahoma,sans-serif}
#app{max-width:640px;margin:0 auto;padding:8px 10px 30px}
.slboard{display:grid;grid-template-columns:repeat(10,1fr);grid-template-rows:repeat(10,1fr);gap:2px;background:#14203a;padding:6px;border-radius:12px}
.sc{position:relative;min-height:29px;background:#0e1930;border:1px solid #223252;border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:9px;line-height:1.05;padding:1px}
.sc.lad{background:#102c29;border-color:#3fb8af}
.sc.snk{background:#2b1412;border-color:#e26d5c}
.num{color:#8093b5}
.mk{font-size:8px}
.mk.up{color:#3fb8af}
.mk.dn{color:#e26d5c}
.pp{position:absolute;top:1px;left:2px;width:14px;height:14px;border-radius:50%;font-size:9px;display:flex;align-items:center;justify-content:center;font-weight:700}
.pp.p0{background:#e26d5c;color:#101828}
.pp.p1{background:#4a7bd0;color:#fff}
.pp+.pp{left:17px}
.slctl{display:flex;gap:12px;align-items:center;justify-content:center;margin:12px 0}
.btn{background:#d9a441;border:0;color:#14203a;font-weight:700;padding:10px 20px;border-radius:10px;font-size:15px;min-height:42px;touch-action:manipulation;font-family:inherit}
.btn.ghost{background:#1d2c4d;color:#e8edf7}
.die{font-size:34px;color:#d9a441;min-width:44px;text-align:center;line-height:1}
"""

SL_TESTS = [
    ("نقشهٔ جابه‌جایی هر ۱۶ پایه", r"""
T.eq(Object.keys(L.LADDERS).length,8,'۸ پله در داده');
T.eq(Object.keys(L.SNAKES).length,8,'۸ مار در داده');
var ok=true,k;
for(k in L.LADDERS){if(L.transport(+k)!==L.LADDERS[k]){ok=false;}}
for(k in L.SNAKES){if(L.transport(+k)!==L.SNAKES[k]){ok=false;}}
T.ok(ok,'هر ۱۶ پایه درست جابه‌جا می‌شود');
T.eq(L.transport(22),22,'خانهٔ ساده ثابت می‌ماند');
var nc=true;
for(k in L.LADDERS){if(L.transport(L.LADDERS[k])!==L.LADDERS[k]){nc=false;}}
for(k in L.SNAKES){if(L.transport(L.SNAKES[k])!==L.SNAKES[k]){nc=false;}}
T.ok(nc,'در داده زنجیره وجود ندارد');
"""),
    ("قانون ۱۰۰ دقیق", r"""
var st=L.initial();
st.pos[0]=99;
var r=L.move(st,0,5);
T.eq(r.to,99,'۹۹+۵ حرکت نیست');
T.ok(!L.isWin(st,0),'برد نیست');
r=L.move(st,0,1);
T.eq(r.to,100,'۹۹+۱ دقیقاً ۱۰۰');
T.ok(L.isWin(st,0),'برد');
var st2=L.initial();
st2.pos[1]=95;
T.eq(L.move(st2,1,6).to,95,'۹۵+۶ هم نه');
T.ok(!L.isWin(st2,1),'باز هم برد نیست');
"""),
    ("سازگاری دادهٔ مار و پله", r"""
var ok=true,k;
for(k in L.SNAKES){if(L.LADDERS[k]!==undefined){ok=false;}}
T.ok(ok,'هیچ خانه‌ای هم سر مار و هم پایهٔ پله نیست');
for(k in L.LADDERS){var t=L.LADDERS[k];if(!(t>+k&&t<=100)){ok=false;}}
for(k in L.SNAKES){var s=L.SNAKES[k];if(!(s<+k&&s>=1)){ok=false;}}
T.ok(ok,'پله فقط بالا می‌رود و مار فقط پایین');
T.ok(L.LADDERS[100]===undefined&&L.SNAKES[100]===undefined,'خانهٔ ۱۰۰ بی‌خطر است');
"""),
    ("حرکت روی پله و مار", r"""
var st=L.initial();st.pos[0]=2;
var r=L.move(st,0,2);
T.eq(r.from,2,'از خانهٔ ۲');
T.eq(r.to,25,'پایهٔ پله ۴ تا ۲۵ می‌برد');
T.ok(r.transported,'جابه‌جایی پله');
var st2=L.initial();st2.pos[1]=25;
var r2=L.move(st2,1,2);
T.eq(r2.to,5,'سر مار ۲۷ تا ۵ می‌برد');
T.ok(r2.transported,'سقوط با مار');
var st3=L.initial();st3.pos[0]=20;
var r3=L.move(st3,0,2);
T.eq(r3.to,22,'حرکت ساده');
T.ok(!r3.transported,'بدون جابه‌جایی');
"""),
    ("بازی کامل زیر ۵۰۰ تاس", r"""
var st=L.initial(),rolls=0;
while(!L.isWin(st,0)&&!L.isWin(st,1)&&rolls<500){L.move(st,st.turn,L.roll(rng));rolls++;}
T.ok(rolls<500,'بازی در '+rolls+' تاس تمام شد');
var w=L.isWin(st,0)?0:1;
T.eq(st.pos[w],100,'برنده روی ۱۰۰');
T.ok(st.pos[1-w]<100,'بازنده زیر ۱۰۰');
T.ok(st.pos[0]>=0&&st.pos[1]>=0,'موقعیت‌ها معتبر');
"""),
    ("تاس ۱ تا ۶", r"""
var lo=9,hi=0,i,d;
for(i=0;i<300;i++){d=L.roll(rng);T.ok(d>=1&&d<=6,'محدودهٔ تاس');if(d<lo){lo=d;}if(d>hi){hi=d;}}
T.eq(lo,1,'عدد ۱ دیده شد');
T.eq(hi,6,'عدد ۶ دیده شد');
"""),
]

# =====================================================================
# 3) DOMINOES — double-six, human vs AI, boneyard draws, blocked game
# =====================================================================
DOM_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
function initial(rng){var r=rng||Math.random,t=[],a,b,j,x;for(a=0;a<=6;a++){for(b=a;b<=6;b++){t.push([a,b]);}}for(a=t.length-1;a>0;a--){j=Math.floor(r()*(a+1));x=t[a];t[a]=t[j];t[j]=x;}return {hands:[t.slice(0,7),t.slice(7,14)],bone:t.slice(14),line:[],turn:0,passes:0,over:false};}
function ends(st){if(!st.line.length){return null;}return [st.line[0].a,st.line[st.line.length-1].b];}
function fits(st,tile){if(!st.line.length){return ['C'];}var e=ends(st),out=[];if(tile[0]===e[0]||tile[1]===e[0]){out.push('L');}if(tile[0]===e[1]||tile[1]===e[1]){out.push('R');}return out;}
function hasTile(hand,tile){for(var i=0;i<hand.length;i++){var h=hand[i];if((h[0]===tile[0]&&h[1]===tile[1])||(h[0]===tile[1]&&h[1]===tile[0])){return i;}}return -1;}
function legalTiles(st,hand){if(!st.line.length){return hand.slice();}var out=[],i;for(i=0;i<hand.length;i++){if(fits(st,hand[i]).length){out.push(hand[i]);}}return out;}
function placeTile(st,pl,tile,end){var hand=st.hands[pl],i=hasTile(hand,tile);if(i<0){return false;}var L0=st.line;if(!L0.length){L0.push({a:tile[0],b:tile[1]});}else{var e=ends(st),tries=end?[end]:['R','L'],done=false,k;for(k=0;k<tries.length&&!done;k++){if(tries[k]==='R'&&(tile[0]===e[1]||tile[1]===e[1])){L0.push(tile[0]===e[1]?{a:tile[0],b:tile[1]}:{a:tile[1],b:tile[0]});done=true;}else if(tries[k]==='L'&&(tile[0]===e[0]||tile[1]===e[0])){L0.unshift(tile[0]===e[0]?{a:tile[1],b:tile[0]}:{a:tile[0],b:tile[1]});done=true;}}if(!done){return false;}}hand.splice(i,1);st.passes=0;st.over=(hand.length===0);st.turn=1-pl;return true;}
function drawTile(st,pl){if(!st.bone.length){return null;}var t=st.bone.pop();st.hands[pl].push(t);return t;}
function pass(st){st.passes++;if(st.passes>=2){st.over=true;}st.turn=1-st.turn;return st.over;}
function aiPick(legal){var bi=0,bs=-999,i,s;for(i=0;i<legal.length;i++){s=legal[i][0]+legal[i][1]-(legal[i][0]===legal[i][1]?2:0);if(s>bs){bs=s;bi=i;}}return legal[bi];}
function autoTurn(st,rng){var pl=st.turn,legal=legalTiles(st,st.hands[pl]),draws=0;while(!legal.length&&st.bone.length){drawTile(st,pl);draws++;legal=legalTiles(st,st.hands[pl]);}if(legal.length){var t=aiPick(legal);placeTile(st,pl,t);return {played:t,draws:draws};}pass(st);return {passed:true,draws:draws};}
function blocked(st){return st.passes>=2;}
function pipSum(hand){var s=0,i;for(i=0;i<hand.length;i++){s+=hand[i][0]+hand[i][1];}return s;}
function winner(st){if(!st.hands[0].length&&!st.hands[1].length){return 'draw';}if(!st.hands[0].length){return 0;}if(!st.hands[1].length){return 1;}if(st.passes>=2){var a=pipSum(st.hands[0]),b=pipSum(st.hands[1]);if(a<b){return 0;}if(b<a){return 1;}return 'draw';}return null;}
return {initial:initial,ends:ends,fits:fits,legalTiles:legalTiles,placeTile:placeTile,drawTile:drawTile,pass:pass,aiPick:aiPick,autoTurn:autoTurn,blocked:blocked,pipSum:pipSum,winner:winner};
})();
"""

DOM_UI = r"""
var app=document.getElementById('app');
var st=null,pend=null,busy=false,seq=0,timer=null;
function hudUpd(){hud('نوبت: <b>'+(st.turn===0?'شما':'ربات')+'</b> · بونیارد: '+fa(st.bone.length)+' · پایپ: شما '+fa(L.pipSum(st.hands[0]))+' / ربات '+fa(L.pipSum(st.hands[1])));}
function newGame(){
  if(timer){clearTimeout(timer);timer=null;}
  seq++;busy=false;pend=null;
  st=L.initial(Math.random);
  $('#hint').textContent='تخته‌ای بگذار که با یکی از دو سرِ خط جور باشد؛ اگر نه، از بونیارد بکش تا بازی‌شدنی بیاید.';
  render();hudUpd();toast('دومینو شروع شد — ۷ تخته داری');
}
function endGame(w){
  busy=true;
  if(w===0){ovl('بردی!',L.blocked(st)?'با پایپ کمتر بردی':'دستت خالی شد','بازی جدید',newGame);}
  else if(w===1){ovl('باختی!',L.blocked(st)?'ربات با پایپ کمتر برد':'ربات دستش را خالی کرد','بازی جدید',newGame);}
  else{ovl('مساوی!','پایپ دو دست برابر بود','بازی جدید',newGame);}
}
function afterPlay(){
  render();hudUpd();
  var w=L.winner(st);
  if(w!==null){endGame(w);return;}
  if(st.turn===1){aiGo();}
  else{toast('نوبت شما');}
}
function playTile(t,end){
  if(!st||busy||st.turn!==0){return;}
  if(!L.placeTile(st,0,t,end)){pend=null;render();toast('این گذاشتن ممکن نیست');return;}
  pend=null;
  afterPlay();
}
function tileClick(){
  if(!st||busy||st.turn!==0){return;}
  var i=+this.getAttribute('data-i'),t=st.hands[0][i],f=L.fits(st,t);
  if(!f.length){return;}
  if(f.length===2){pend=t;render();return;}
  playTile(t,f[0]);
}
function aiGo(){
  var my=++seq;busy=true;render();hudUpd();
  timer=setTimeout(function(){
    if(my!==seq||!st||st.turn!==1){return;}
    var r=L.autoTurn(st,Math.random);
    render();hudUpd();
    if(r.played){toast('ربات تخته گذاشت');}
    else{toast('ربات پاس داد');}
    var w=L.winner(st);
    if(w!==null){endGame(w);return;}
    busy=false;
    toast('نوبت شما');
  },800);
}
function drawClick(){
  if(!st||busy||st.turn!==0){return;}
  var my=++seq;busy=true;render();
  (function step(){
    if(my!==seq||!st){return;}
    if(L.legalTiles(st,st.hands[0]).length){busy=false;render();hudUpd();toast('تختهٔ بازی‌شدنی گرفتی!');return;}
    if(!st.bone.length){
      var over=L.pass(st);
      render();hudUpd();
      if(over){endGame(L.winner(st));return;}
      toast('بونیارد خالی — پاس');aiGo();return;
    }
    var t=L.drawTile(st,0);
    toast('برداشتی: '+fa(t[0])+' و '+fa(t[1]));
    render();hudUpd();
    timer=setTimeout(step,320);
  })();
}
function passClick(){
  if(!st||busy||st.turn!==0){return;}
  var over=L.pass(st);
  render();hudUpd();
  if(over){endGame(L.winner(st));return;}
  toast('پاس دادی');aiGo();
}
function render(){
  var i,t,h='<div class="dpanel ai"><b>ربات</b><span class="cnt">'+fa(st.hands[1].length)+' تخته</span><div class="backrow">';
  for(i=0;i<st.hands[1].length;i++){h+='<div class="btile"></div>';}
  h+='</div></div>';
  h+='<div class="dlinebox"><div class="ends"><span>سر چپ: <b>'+(st.line.length?fa(st.line[0].a):'—')+'</b></span><span>سر راست: <b>'+(st.line.length?fa(st.line[st.line.length-1].b):'—')+'</b></span></div><div class="dline" dir="ltr">';
  for(i=0;i<st.line.length;i++){var o=st.line[i];h+='<div class="ltile'+((i===0||i===st.line.length-1)?' ed':'')+'"><span>'+fa(o.a)+'</span><i></i><span>'+fa(o.b)+'</span></div>';}
  if(!st.line.length){h+='<span class="empty">خط خالی است — هر تخته‌ای بگذار</span>';}
  h+='</div></div>';
  var leg=L.legalTiles(st,st.hands[0]);
  h+='<div class="dpanel you"><b>تخته‌های شما</b><div class="hand">';
  for(i=0;i<st.hands[0].length;i++){t=st.hands[0][i];var okp=(st.turn===0&&!busy)&&(leg.indexOf(t)>=0);
    h+='<button class="dtile'+(okp?' ok':'')+'" data-i="'+i+'"'+(okp?'':' disabled')+'><span>'+fa(t[0])+'</span><i></i><span>'+fa(t[1])+'</span></button>';}
  h+='</div></div>';
  h+='<div class="dctl"><span class="binfo">بونیارد: '+fa(st.bone.length)+'</span>';
  if(st.turn===0&&leg.length===0&&st.bone.length>0){h+='<button id="drawBtn" data-smoke class="btn">از بونیارد بکش</button>';}
  if(st.turn===0&&leg.length===0&&st.bone.length===0){h+='<button id="passBtn" class="btn">پاس</button>';}
  h+='<button id="ngBtn" data-smoke class="btn ghost">بازی جدید</button></div>';
  if(pend){h+='<div class="pendbar">«'+fa(pend[0])+'|'+fa(pend[1])+'» به هر دو سر می‌خورد — کجا بگذارم؟ <button id="plBtn" class="btn small">چپ</button> <button id="prBtn" class="btn small">راست</button></div>';}
  app.innerHTML=h;
  var els=app.querySelectorAll('.dtile.ok'),j;
  for(j=0;j<els.length;j++){els[j].onclick=tileClick;}
  var rb=$('#drawBtn');if(rb){rb.onclick=drawClick;}
  var pb=$('#passBtn');if(pb){pb.onclick=passClick;}
  $('#ngBtn').onclick=newGame;
  var lb=$('#plBtn');if(lb){lb.onclick=function(){playTile(pend.slice(),'L');};}
  var rr=$('#prBtn');if(rr){rr.onclick=function(){playTile(pend.slice(),'R');};}
}
newGame();
"""

DOM_CSS = r"""
body{margin:0;background:#0b1526;color:#e8edf7;font-family:Vazirmatn,Tahoma,sans-serif}
#app{max-width:820px;margin:0 auto;padding:8px 10px 30px}
.dpanel{background:#14203a;border-radius:12px;padding:8px 12px;margin:8px 0}
.dpanel b{color:#d9a441;font-size:13px}
.cnt{color:#9fb3d9;font-size:12px;margin-right:8px}
.backrow{display:flex;gap:3px;flex-wrap:wrap;margin-top:6px}
.btile{width:16px;height:26px;background:#1d2c4d;border:1px solid #2a3a5c;border-radius:4px}
.dlinebox{background:#14203a;border-radius:12px;padding:8px 12px;margin:8px 0}
.ends{display:flex;justify-content:space-between;font-size:12px;color:#9fb3d9;margin-bottom:6px}
.ends b{color:#d9a441}
.dline{display:flex;gap:3px;overflow-x:auto;padding:4px 2px;align-items:center;min-height:40px}
.ltile{display:flex;flex-direction:column;align-items:center;background:#0e1930;border:1px solid #2a3a5c;border-radius:5px;padding:2px 6px;flex:0 0 auto;font-size:12px;font-weight:700}
.ltile i{display:block;width:100%;height:1px;background:#2a3a5c;margin:2px 0}
.ltile.ed{border-color:#d9a441}
.empty{color:#8093b5;font-size:12px}
.hand{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.dtile{display:flex;flex-direction:column;align-items:center;background:#0e1930;color:#e8edf7;border:1px solid #2a3a5c;border-radius:6px;padding:3px 10px;font-size:13px;font-weight:700;min-height:44px;min-width:34px;touch-action:manipulation;font-family:inherit}
.dtile i{display:block;width:80%;height:1px;background:#2a3a5c;margin:2px 0}
.dtile.ok{border-color:#3fb8af;background:#0f2b33;cursor:pointer}
.dtile:disabled{opacity:.45}
.dctl{display:flex;gap:12px;align-items:center;justify-content:center;margin:12px 0;flex-wrap:wrap}
.binfo{color:#9fb3d9;font-size:13px}
.btn{background:#d9a441;border:0;color:#14203a;font-weight:700;padding:10px 20px;border-radius:10px;font-size:15px;min-height:42px;touch-action:manipulation;font-family:inherit}
.btn.ghost{background:#1d2c4d;color:#e8edf7}
.btn.small{padding:6px 14px;min-height:36px;font-size:13px}
.pendbar{background:#1d2c4d;border:1px solid #d9a441;border-radius:10px;padding:8px 12px;margin:8px 0;text-align:center;font-size:13px}
"""

DOM_TESTS = [
    ("قانونیت تخته در دو سر", r"""
var st={hands:[[[2,6],[5,3],[3,4],[1,1]],[]],bone:[],line:[{a:2,b:5}],turn:0,passes:0,over:false};
var lg=L.legalTiles(st,st.hands[0]);
T.eq(lg.length,2,'دو تخته قابل بازی');
T.ok(L.fits(st,[2,6]).indexOf('L')>=0,'تخته به سر چپ (۲) می‌خورد');
T.ok(L.fits(st,[5,3]).indexOf('R')>=0,'تخته به سر راست (۵) می‌خورد');
T.eq(L.fits(st,[3,4]).length,0,'۳|۴ به هیچ سر نمی‌خورد');
T.ok(L.placeTile(st,0,[6,2],'L'),'گذاشتن در سر چپ');
T.eq(st.line[0].a,6,'جهت‌دهی چپ: ۶ رو به بیرون');
T.eq(st.line[0].b,2,'جهت‌دهی چپ: ۲ رو به داخل');
T.ok(L.placeTile(st,0,[5,3],'R'),'گذاشتن در سر راست');
T.eq(st.line[2].b,3,'سر راست شد ۳');
T.ok(!L.placeTile(st,0,[1,1],'R'),'تختهٔ ناجور رد شد');
var st0={hands:[[[0,0]]],bone:[],line:[],turn:0,passes:0,over:false};
T.eq(L.legalTiles(st0,st0.hands[0]).length,1,'خط خالی: همه تخته‌ها مجاز');
"""),
    ("کشیدن از بونیارد تا بازی‌شدنی", r"""
var st={hands:[[[0,0],[1,1]],[[2,2],[3,3]]],bone:[[0,6],[1,6],[5,4]],line:[{a:2,b:5}],turn:0,passes:0,over:false};
var r=L.autoTurn(st);
T.eq(r.draws,1,'یک بار کشید (بونیارد LIFO)');
T.ok(r.played&&r.played[0]===5&&r.played[1]===4,'کشیدنیِ بازی‌شدنی گذاشته شد');
T.eq(st.bone.length,2,'دو تخته در بونیارد ماند');
T.eq(st.hands[0].length,2,'دست به‌روز شد');
T.eq(st.line.length,2,'تخته روی خط');
T.eq(st.line[1].a,5,'سر راست جدید ۵');
T.eq(st.turn,1,'نوبت ربات');
T.eq(st.passes,0,'پاس صفر');
var st2={hands:[[[0,0],[1,1]],[[2,2]]],bone:[],line:[{a:2,b:5}],turn:0,passes:0,over:false};
var r2=L.autoTurn(st2);
T.ok(r2.passed&&!st2.over,'با بونیارد خالی: پاس ساده');
T.eq(st2.passes,1,'یک پاس ثبت شد');
T.eq(st2.turn,1,'نوبت عوض شد');
"""),
    ("بن‌بست و برندهٔ پایپ کمتر", r"""
var st={hands:[[[0,1],[0,2]],[[3,3],[4,4]]],bone:[],line:[{a:5,b:5}],turn:0,passes:0,over:false};
T.ok(!L.blocked(st),'هنوز بن‌بست نیست');
L.autoTurn(st);L.autoTurn(st);
T.ok(L.blocked(st),'دو پاس پشت‌سرهم = بن‌بست');
T.ok(st.over,'بازی تمام شد');
T.eq(L.pipSum(st.hands[0]),3,'پایپ شما ۳');
T.eq(L.pipSum(st.hands[1]),14,'پایپ ربات ۱۴');
T.eq(L.winner(st),0,'دست سبک‌تر برد');
var st2={hands:[[[0,1],[0,2]],[[1,0],[2,0]]],bone:[],line:[{a:5,b:5}],turn:0,passes:0,over:false};
L.autoTurn(st2);L.autoTurn(st2);
T.eq(L.winner(st2),'draw','تساوی کامل');
"""),
    ("جمع پایپ و برنده", r"""
T.eq(L.pipSum([[6,6],[3,2],[0,0]]),17,'جمع پایپ دست');
var st={hands:[[],[[1,2]]],bone:[],line:[{a:3,b:4}],turn:0,passes:0,over:false};
T.eq(L.winner(st),0,'دست خالی یعنی برده');
var st2={hands:[[[1,2]],[]],bone:[],line:[{a:3,b:4}],turn:0,passes:0,over:false};
T.eq(L.winner(st2),1,'ربات برنده شد');
var st3=L.initial(rng);
T.eq(L.winner(st3),null,'بازی جاری بی‌برنده');
T.ok(!L.blocked(st3),'شروع بدون بن‌بست');
"""),
    ("بازی کامل با حفظ ۲۸ تخته", r"""
var st=L.initial(rng),turns=0,ok=true;
T.eq(st.hands[0].length+st.hands[1].length+st.bone.length,28,'پخش ۷/۷/۱۴');
while(!st.over&&turns<500){
  L.autoTurn(st,rng);
  var c=st.hands[0].length+st.hands[1].length+st.bone.length+st.line.length;
  if(c!==28){ok=false;}
  var pips=L.pipSum(st.hands[0])+L.pipSum(st.hands[1])+L.pipSum(st.bone),i;
  for(i=0;i<st.line.length;i++){pips+=st.line[i].a+st.line[i].b;}
  if(pips!==168){ok=false;}
  turns++;
}
T.ok(ok,'در هر نوبت ۲۸ تخته و ۱۶۸ پایپ حفظ شد');
T.ok(st.over,'بازی در '+turns+' نوبت تمام شد');
var w=L.winner(st);
T.ok(w===0||w===1||w==='draw','نتیجهٔ معتبر');
T.ok(st.hands[0].length===0||st.hands[1].length===0||w==='draw'||L.blocked(st),'سازگاری نتیجه');
"""),
    ("دستهٔ اولیه یکتا و کامل", r"""
var st=L.initial(rng),seen={},ok=true,i;
function chk(h){for(i=0;i<h.length;i++){var k=h[i][0]+':'+h[i][1];if(seen[k]){ok=false;}seen[k]=1;if(h[i][0]<0||h[i][1]>6||h[i][0]>h[i][1]){ok=false;}}}
chk(st.hands[0]);chk(st.hands[1]);chk(st.bone);
T.ok(ok,'تخته‌ها یکتا و نرمال (a<=b, ۰..۶)');
var n=0,k;for(k in seen){n++;}
T.eq(n,28,'کل ست دوروشش');
T.eq(st.line.length,0,'خط در شروع خالی');
T.eq(st.turn,0,'شروع با شما');
"""),
]

ludo = G(
    slug="ludo", title="لیدو", cat="board", icon="🎯",
    g1="#e26d5c", g2="#4a7bd0",
    desc="لیدوی ساده‌شدهٔ دونفره در برابر ربات: چهار مهره، مسیر ۵۲ خانه‌ای مشترک و ستون خانه؛ با ۶ از پایگاه بیرون بیا و اولین نفر همه را به خانه برسان.",
    hint="تاس بریز؛ با ۶ مهره از پایگاه می‌آید. ورود به خانهٔ آخر عدد دقیق می‌خواهد و گرفتن مهرهٔ حریف او را به پایگاه برمی‌گرداند. سه شش پشت‌سرهم نوبت را می‌سوزاند.",
    logic=LUDO_LOGIC, ui=LUDO_UI, css=LUDO_CSS,
    engines=("common",), tests=LUDO_TESTS, seed=12345)

sl = G(
    slug="snakes-ladders", title="مار و پله", cat="board", icon="🪜",
    g1="#3fb8af", g2="#d9a441",
    desc="مسابقه تا خانهٔ ۱۰۰ با ۸ پله و ۸ مار؛ باید دقیقاً روی ۱۰۰ بایستی و ربات هم با همین قوانین بازی می‌کند.",
    hint="تاس بریز و دقیقاً روی ۱۰۰ بایست؛ اگر از آن رد شوی حرکت نمی‌کنی. سرِ پله بالا می‌برد و سرِ مار پایین می‌کشد.",
    logic=SL_LOGIC, ui=SL_UI, css=SL_CSS,
    engines=("common",), tests=SL_TESTS, seed=12345)

dom = G(
    slug="dominoes", title="دومینو", cat="board", icon="⬛",
    g1="#d9a441", g2="#3fb8af",
    desc="دومینوی شش‌دوبله در برابر ربات: تخته‌هایت را به دو سرِ خط بزن، از بونیارد بکش و در بن‌بست دستِ سبک‌تر برنده است.",
    hint="تخته‌ای بگذار که با یکی از دو سرِ خط جور باشد؛ اگر نه از بونیارد بکش و اگر بونیارد خالی بود پاس بده.",
    logic=DOM_LOGIC, ui=DOM_UI, css=DOM_CSS,
    engines=("common",), tests=DOM_TESTS, seed=12345)

GAMES = [ludo, sl, dom]
