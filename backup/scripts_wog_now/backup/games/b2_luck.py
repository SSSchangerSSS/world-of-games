# -*- coding: utf-8 -*-
"""AG-B2 — دستهٔ بازی‌های شانس (luck): یاتزی، تاس پیگ، سه‌تاس (chuck-a-luck)."""
from lib_mini import G

YAHTZEE_LOGIC = r"""
var Y_UPPER=['ones','twos','threes','fours','fives','sixes'];
var Y_CATS=Y_UPPER.concat(['threeKind','fourKind','fullHouse','smallStraight','largeStraight','chance','yahtzee']);
function yCounts(d){var c=[0,0,0,0,0,0,0],i;for(i=0;i<5;i++)c[d[i]]++;return c;}
function ySum(d){var s=0,i;for(i=0;i<5;i++)s+=d[i];return s;}
function yMaxC(c){var m=0,i;for(i=1;i<=6;i++)if(c[i]>m)m=c[i];return m;}
function yAllEq(d){return yMaxC(yCounts(d))===5;}
function yRun(c,len){var run=0,i;for(i=1;i<=6;i++){run=c[i]>0?run+1:0;if(run>=len)return true;}return false;}
function yCalc(cat,d){var c=yCounts(d),s=ySum(d),m=yMaxC(c),i,two,three;
 if(cat==='ones')return c[1];if(cat==='twos')return c[2]*2;if(cat==='threes')return c[3]*3;
 if(cat==='fours')return c[4]*4;if(cat==='fives')return c[5]*5;if(cat==='sixes')return c[6]*6;
 if(cat==='threeKind')return m>=3?s:0;
 if(cat==='fourKind')return m>=4?s:0;
 if(cat==='fullHouse'){two=false;three=false;for(i=1;i<=6;i++){if(c[i]===2)two=true;if(c[i]===3)three=true;}return(two&&three)?25:0;}
 if(cat==='smallStraight')return yRun(c,4)?30:0;
 if(cat==='largeStraight')return yRun(c,5)?40:0;
 if(cat==='chance')return s;
 if(cat==='yahtzee')return m===5?50:0;
 return 0;}
function yNew(){return{dice:[0,0,0,0,0],rollsLeft:3,sheet:{}};}
function yScore(state,cat,d){d=d||state.dice;var p=yCalc(cat,d);
 if(!p&&(cat==='fullHouse'||cat==='smallStraight'||cat==='largeStraight')&&yAllEq(d)&&state&&state.sheet){
  var up=Y_UPPER[d[0]-1];
  if(state.sheet[up]!==undefined&&state.sheet[up]!==null){if(cat==='fullHouse')p=25;else if(cat==='smallStraight')p=30;else p=40;}}
 return p;}
function yRoll(state,holds,rng){if(state.rollsLeft<=0)throw new Error('no-rolls');
 var r=rng||Math.random;holds=holds||[];
 for(var i=0;i<5;i++)if(holds.indexOf(i)<0)state.dice[i]=1+Math.floor(r()*6);
 state.rollsLeft--;return state.dice;}
function yAssign(state,cat,d){if(state.sheet[cat]!==undefined)return state;
 state.sheet[cat]=yScore(state,cat,d||state.dice);
 state.rollsLeft=3;state.dice=[0,0,0,0,0];return state;}
function yUpper(sheet){var s=0,i;for(i=0;i<6;i++)if(sheet[Y_UPPER[i]]!==undefined)s+=sheet[Y_UPPER[i]];return s;}
function yBonus(sheet){return yUpper(sheet)>=63?35:0;}
function yUsed(sheet,cat){return sheet[cat]!==undefined;}
function yFull(sheet){for(var i=0;i<Y_CATS.length;i++)if(sheet[Y_CATS[i]]===undefined)return false;return true;}
function yTotals(sheet){var u=yUpper(sheet),b=yBonus(sheet),l=0,i;
 for(i=6;i<Y_CATS.length;i++)if(sheet[Y_CATS[i]]!==undefined)l+=sheet[Y_CATS[i]];
 return{upper:u,bonus:b,lower:l,grand:u+b+l};}
var WOG_LOGIC={UPPER:Y_UPPER,CATS:Y_CATS,newGame:yNew,rollDice:yRoll,calc:yCalc,score:yScore,assign:yAssign,
 upperSubtotal:yUpper,bonus:yBonus,isUsed:yUsed,isSheetFull:yFull,totals:yTotals};
"""

YAHTZEE_UI = r"""
var CAT_FA={ones:'یک‌ها',twos:'دوها',threes:'سه‌ها',fours:'چهارها',fives:'پنج‌ها',sixes:'شش‌ها',threeKind:'سه‌تایی',fourKind:'چهارتایی',fullHouse:'خانه کامل',smallStraight:'خیابان کوچک',largeStraight:'خیابان بزرگ',chance:'شانس',yahtzee:'یاتزی'};
var DIE='⚀⚁⚂⚃⚄⚅';
var st=L.newGame(),holds=[0,0,0,0,0],bestCat=null;
$('#hint').textContent='تاس را لمس کنید تا ثابت بماند؛ در هر نوبت ۳ پرتاب دارید و باید امتیاز را در یکی از ۱۳ خانهٔ باز ثبت کنید.';
$('#app').innerHTML='<div class="dice" id="diceRow"></div><div class="btns"><button class="btn" id="btnRoll" data-smoke>پرتاب تاس‌ها</button><button class="btn alt" id="btnNew" data-smoke>بازی جدید</button></div><div class="sheet" id="sheet"></div>';
function dieCh(v){return v>0?DIE.charAt(v-1):'؟';}
function rolled(){return st.rollsLeft<3&&st.dice[0]>0;}
function catRow(cat){var v=st.sheet[cat];
 if(v!==undefined)return '<div class="row used"><span>'+CAT_FA[cat]+'</span><b>'+fa(v)+'</b></div>';
 var p=rolled()?L.score(st,cat):null;
 return '<button class="row catbtn'+(cat===bestCat?' best':'')+'" data-cat="'+cat+'"><span>'+CAT_FA[cat]+'</span><b>'+(p===null?'—':fa(p))+'</b></button>';}
function render(){var html='',i;
 for(i=0;i<5;i++)html+='<button class="die'+(holds[i]?' hold':'')+'" data-i="'+i+'"'+((st.dice[i]>0&&st.rollsLeft<3)?'':' disabled')+'>'+dieCh(st.dice[i])+'</button>';
 $('#diceRow').innerHTML=html;
 bestCat=null;
 if(rolled()){var bp=-1;for(i=0;i<L.CATS.length;i++){if(st.sheet[L.CATS[i]]!==undefined)continue;var pv=L.score(st,L.CATS[i]);if(pv>bp){bp=pv;bestCat=L.CATS[i];}}}
 var s='';for(i=0;i<6;i++)s+=catRow(L.CATS[i]);
 var u=L.upperSubtotal(st.sheet);
 s+='<div class="sep">جایزهٔ بالایی: '+fa(u)+' از ۶۳'+(u>=63?' — ۳۵ امتیاز جایزه فعال شد':'')+'</div>';
 for(i=6;i<L.CATS.length;i++)s+=catRow(L.CATS[i]);
 var t=L.totals(st.sheet);
 s+='<div class="sep tot">امتیاز کل فعلی: '+fa(t.grand)+'</div>';
 $('#sheet').innerHTML=s;
 hud('پرتاب باقی‌مانده: '+fa(st.rollsLeft)+' — بالایی: '+fa(u)+' — جایزه: '+fa(t.bonus)+' — کل: '+fa(t.grand));}
function play(cat){if(!cat||st.sheet[cat]!==undefined)return;
 if(!rolled()){toast('اول تاس‌ها را برانید');return;}
 var pts=L.score(st,cat);L.assign(st,cat);holds=[0,0,0,0,0];
 toast(CAT_FA[cat]+': '+fa(pts)+' امتیاز ثبت شد');
 if(L.isSheetFull(st.sheet)){var t=L.totals(st.sheet),b=+(store.get('wog-yahtzee-best')||0);
  if(t.grand>b){store.set('wog-yahtzee-best',String(t.grand));toast('رکورد جدید!');}
  ovl('پایان یاتزی','امتیاز کل: '+fa(t.grand)+' — بالایی '+fa(t.upper)+' + جایزه '+fa(t.bonus)+' + پایینی '+fa(t.lower),'بازی جدید',newG);}
 render();}
function newG(){st=L.newGame();holds=[0,0,0,0,0];render();}
$('#app').addEventListener('click',function(e){var el=e.target.closest?e.target.closest('.die'):null;
 if(el&&!el.disabled){var i=+el.getAttribute('data-i');holds[i]=holds[i]?0:1;render();return;}
 el=e.target.closest?e.target.closest('.catbtn'):null;
 if(el&&el.getAttribute)play(el.getAttribute('data-cat'));});
$('#btnRoll').addEventListener('click',function(){if(st.rollsLeft<=0){toast('پرتابی نمانده؛ خانه‌ای را برای ثبت انتخاب کنید');return;}
 var hs=[],i;for(i=0;i<5;i++)if(holds[i])hs.push(i);
 L.rollDice(st,hs);render();});
$('#btnNew').addEventListener('click',newG);
render();
"""

YAHTZEE_CSS = r"""
#app{max-width:540px;margin:0 auto;padding:6px 10px}
.dice{display:flex;gap:8px;justify-content:center;margin:12px 0;flex-wrap:wrap}
.die{width:58px;height:58px;font-size:36px;line-height:1;border-radius:12px;border:2px solid #3fb8af;background:#14203a;color:#f3ead8;cursor:pointer;touch-action:manipulation;padding:0;font-family:inherit}
.die.hold{border-color:#d9a441;background:#332a12;color:#d9a441;transform:translateY(-5px)}
.die[disabled]{opacity:.5;transform:none}
.btns{display:flex;gap:10px;justify-content:center;margin:10px 0;flex-wrap:wrap}
.btn{min-height:44px;border:0;border-radius:10px;background:#d9a441;color:#14203a;font-weight:700;padding:10px 18px;cursor:pointer;touch-action:manipulation;font-family:inherit;font-size:15px}
.btn.alt{background:#3fb8af;color:#0c1526}
.sheet{display:flex;flex-direction:column;gap:4px}
.row{display:flex;justify-content:space-between;align-items:center;min-height:40px;background:#14203a;border:1px solid #233052;border-radius:9px;padding:6px 12px;color:#f3ead8;width:100%;box-sizing:border-box;cursor:pointer;touch-action:manipulation;font-family:inherit;font-size:15px}
.row.best{border-color:#d9a441}
.row.used,.row.used b{color:#67b98a;cursor:default}
.row b{color:#d9a441;font-size:16px}
.sep{text-align:center;color:#8fa3c8;font-size:13px;margin:4px 0}
.sep.tot{color:#d9a441;font-size:15px;font-weight:700}
"""

YAHTZEE_TESTS = [
("امتیازدهی سیزده مقوله روی تاس‌های ساخته‌شده", """
var g=L.newGame();
T.eq(L.score(g,'ones',[1,1,1,4,5]),3,'ones');
T.eq(L.score(g,'sixes',[6,6,1,2,3]),12,'sixes');
T.eq(L.score(g,'threeKind',[3,3,3,2,6]),17,'3k sums all');
T.eq(L.score(g,'threeKind',[3,3,2,2,6]),0,'3k none');
T.eq(L.score(g,'fourKind',[4,4,4,4,1]),17,'4k sums all');
T.eq(L.score(g,'fourKind',[4,4,4,1,1]),0,'4k none');
T.eq(L.score(g,'fullHouse',[2,2,2,5,5]),25,'fh 3+2');
T.eq(L.score(g,'fullHouse',[2,2,2,2,5]),0,'4+1 is not fh');
T.eq(L.score(g,'smallStraight',[1,2,3,4,6]),30,'ss A1234+6');
T.eq(L.score(g,'smallStraight',[2,3,4,5,6]),30,'ss 23456');
T.eq(L.score(g,'smallStraight',[1,2,3,5,6]),0,'no ss');
T.eq(L.score(g,'largeStraight',[1,2,3,4,5]),40,'ls A1234');
T.eq(L.score(g,'largeStraight',[2,3,4,5,6]),40,'ls 23456');
T.eq(L.score(g,'largeStraight',[1,2,3,4,4]),0,'no ls');
T.eq(L.score(g,'chance',[5,5,5,5,5]),25,'chance sum');
T.eq(L.score(g,'yahtzee',[5,5,5,5,5]),50,'yahtzee');
T.eq(L.score(g,'yahtzee',[1,2,3,4,5]),0,'no yahtzee');
"""),
("پرتاب با نگه‌داشتن و سقف سه پرتاب", """
var st=L.newGame();
T.eq(st.rollsLeft,3,'fresh 3 rolls');
T.eq(st.dice,[0,0,0,0,0],'no dice yet');
st.dice=[3,5,2,4,6];
var seq=[0,1/6,2/6],i=0,r=function(){return seq[i++%3];};
L.rollDice(st,[0,4],r);
T.eq(st.dice,[3,1,2,3,6],'held dice kept, rest rolled');
T.eq(st.rollsLeft,2,'decrement');
L.rollDice(st,[],r);L.rollDice(st,[],r);
T.eq(st.rollsLeft,0,'exhausted');
T.throws(function(){L.rollDice(st,[],r);},'no fourth roll');
"""),
("جایزه بالایی روی آستانه ۶۳", """
var sheet={ones:1,twos:2,threes:3,fours:4,fives:5,sixes:48};
T.eq(L.upperSubtotal(sheet),63,'subtotal exactly 63');
T.eq(L.bonus(sheet),35,'bonus fires at 63');
var t=L.totals(sheet);
T.eq(t.grand,t.upper+t.bonus+t.lower,'grand consistent');
T.eq(t.grand,98,'98 = 63+35');
var s2={sixes:36,fives:15,fours:8,threes:3};
T.eq(L.upperSubtotal(s2),62,'62 subtotal');
T.eq(L.bonus(s2),0,'no bonus under 63');
"""),
("قانون جوکر یاتزی", """
var st={dice:[6,6,6,6,6],rollsLeft:0,sheet:{sixes:30}};
T.eq(L.score(st,'fullHouse'),25,'joker fh 25');
T.eq(L.score(st,'smallStraight'),30,'joker ss 30');
T.eq(L.score(st,'largeStraight'),40,'joker ls 40');
T.eq(L.score(st,'chance'),30,'chance sums 30');
var open=L.newGame();open.dice=[6,6,6,6,6];
T.eq(L.score(open,'fullHouse'),0,'no joker while upper open');
T.eq(L.score(open,'smallStraight'),0,'no joker ss while open');
T.eq(L.score(open,'largeStraight'),0,'no joker ls while open');
"""),
("بازی کامل ۱۳ دسته و سازگاری جمع کل", """
var st=L.newGame(),turn,k;
for(turn=0;turn<13;turn++){
 L.rollDice(st,[],rng);L.rollDice(st,[],rng);L.rollDice(st,[],rng);
 var best=null,bp=-1;
 for(k=0;k<L.CATS.length;k++){var c=L.CATS[k];if(L.isUsed(st.sheet,c))continue;
  var p=L.score(st,c);if(p>bp){bp=p;best=c;}}
 L.assign(st,best);}
T.ok(L.isSheetFull(st.sheet),'sheet full after 13 turns');
var n=0;for(k in st.sheet)if(st.sheet.hasOwnProperty(k))n++;
T.eq(n,13,'each category used exactly once');
var t=L.totals(st.sheet);
T.eq(t.grand,t.upper+t.bonus+t.lower,'grand = upper+bonus+lower');
var before=JSON.stringify(st.sheet);
L.assign(st,'chance');
T.eq(JSON.stringify(st.sheet),before,'used category locked');
"""),
]

PIG_LOGIC = r"""
function pNew(){return{scores:[0,0],current:0,turnTotal:0,over:false,winner:-1};}
function pStart(state,idx){state.current=idx;state.turnTotal=0;return state;}
function pRoll(state,rng){if(state.over)throw new Error('game-over');
 var r=rng||Math.random,die=1+Math.floor(r()*6);
 if(die===1){state.turnTotal=0;return{die:1,busted:true};}
 state.turnTotal+=die;return{die:die,busted:false};}
function pHold(state){var b=state.scores[state.current]+state.turnTotal;
 state.scores[state.current]=b;state.turnTotal=0;
 if(b>=100){state.over=true;state.winner=state.current;}
 return b;}
function pAI(state){var tot=state.scores[state.current]+state.turnTotal;
 if(tot>=100)return'hold';
 if(state.turnTotal>=20)return'hold';
 return'roll';}
function pTurn(state,idx,decide,rng){pStart(state,idx);var guard=0;
 while(!state.over&&guard++<500){
  if(decide(state)==='hold'){pHold(state);break;}
  if(pRoll(state,rng).busted)break;}
 return state;}
var WOG_LOGIC={newGame:pNew,startTurn:pStart,roll:pRoll,hold:pHold,aiDecision:pAI,takeTurn:pTurn};
"""

PIG_UI = r"""
var st=L.newGame(),busy=false,last=0,wins=+(store.get('wog-pig-wins')||0);
$('#hint').textContent='تاس ببرانید و شمارش نوبت را جمع کنید؛ اگر ۱ بیاید همهٔ شمارش نوبت می‌سوزد. با «نگه‌دار» امتیاز را ثبت کنید؛ اولین نفری که به ۱۰۰ برسد برنده است.';
$('#app').innerHTML='<div class="scores"><div class="pcard" id="p0"><div>شما</div><div class="big" id="s0">۰</div><div class="sub" id="t0"></div></div><div class="pcard" id="p1"><div>ربات</div><div class="big" id="s1">۰</div><div class="sub" id="t1"></div></div></div><div class="diebig" id="die">⚄</div><div class="tot" id="tt"></div><div class="btns"><button class="btn" id="btnRoll" data-smoke>پرتاب</button><button class="btn alt" id="btnHold" data-smoke>نگه‌دار</button><button class="btn alt" id="btnNew" data-smoke>بازی جدید</button></div>';
function render(){
 $('#s0').textContent=fa(st.scores[0]);$('#s1').textContent=fa(st.scores[1]);
 $('#t0').textContent=(st.current===0&&!st.over)?('در نوبت: '+fa(st.turnTotal)):'';
 $('#t1').textContent=(st.current===1&&!st.over)?('در نوبت: '+fa(st.turnTotal)):'';
 $('#p0').className='pcard'+((st.current===0&&!st.over)?' on':'');
 $('#p1').className='pcard'+((st.current===1&&!st.over)?' on':'');
 if(last)$('#die').textContent='⚀⚁⚂⚃⚄⚅'.charAt(last-1);
 $('#tt').textContent=st.over?'':('شمارش این نوبت: '+fa(st.turnTotal));
 hud('شما '+fa(st.scores[0])+' — ربات '+fa(st.scores[1])+' | بردها: '+fa(wins));}
function newG(){st=L.newGame();busy=false;last=0;L.startTurn(st,0);render();}
function end(){var win=st.winner===0;
 if(win){wins++;store.set('wog-pig-wins',String(wins));}
 busy=true;render();
 ovl(win?'بردی!':'باختی!','نتیجهٔ نهایی — شما '+fa(st.scores[0])+' : ربات '+fa(st.scores[1]),'بازی جدید',newG);}
function aiTurn(){if(st.over)return;busy=true;L.startTurn(st,1);render();
 (function step(){
  if(st.over){end();return;}
  if(L.aiDecision(st)==='hold'){L.hold(st);render();
   if(st.over){end();return;}
   busy=false;setTimeout(function(){L.startTurn(st,0);render();},700);return;}
  var res=L.roll(st);last=res.die;render();
  if(res.busted){busy=false;toast('ربات سوخت!');setTimeout(function(){L.startTurn(st,0);render();},700);return;}
  setTimeout(step,650);})();}
$('#btnRoll').addEventListener('click',function(){if(busy||st.over||st.current!==0)return;
 var res=L.roll(st);last=res.die;
 if(res.busted){toast('تاس ۱ آمد! شمارش این نوبت سوخت');render();setTimeout(aiTurn,700);return;}
 render();});
$('#btnHold').addEventListener('click',function(){if(busy||st.over||st.current!==0)return;
 if(st.turnTotal===0){toast('هنوز در این نوبت تاسی نیاورده‌اید');return;}
 L.hold(st);last=0;render();
 if(st.over){end();return;}
 setTimeout(aiTurn,700);});
$('#btnNew').addEventListener('click',newG);
L.startTurn(st,0);render();
"""

PIG_CSS = r"""
#app{max-width:540px;margin:0 auto;padding:6px 10px}
.scores{display:flex;gap:10px;justify-content:center;margin:10px 0}
.pcard{background:#14203a;border:2px solid #233052;border-radius:12px;padding:10px 14px;text-align:center;flex:1;max-width:220px;color:#8fa3c8}
.pcard.on{border-color:#d9a441}
.pcard .big{font-size:30px;font-weight:800;color:#d9a441;line-height:1.3}
.pcard .sub{min-height:20px;color:#3fb8af;font-size:14px}
.diebig{font-size:76px;text-align:center;line-height:1.15;color:#f3ead8}
.tot{text-align:center;color:#3fb8af;font-size:17px;min-height:24px;margin:6px 0}
.btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.btn{min-height:44px;border:0;border-radius:10px;background:#d9a441;color:#14203a;font-weight:700;padding:10px 20px;cursor:pointer;touch-action:manipulation;font-family:inherit;font-size:15px}
.btn.alt{background:#3fb8af;color:#0c1526}
"""

PIG_TESTS = [
("تاس ۱ شمارش نوبت را می‌سوزاند", """
var st=L.newGame();L.startTurn(st,0);
var one=function(){return 0;},four=function(){return 3/6;};
var res=L.roll(st,one);
T.ok(res.busted,'busted on 1');T.eq(res.die,1,'die is 1');
T.eq(st.turnTotal,0,'turn total reset');
T.eq(st.scores[0],0,'banked score safe');
var a=L.roll(st,four);T.ok(!a.busted);T.eq(a.die,4);T.eq(st.turnTotal,4,'accumulates');
var b=L.roll(st,four);T.eq(st.turnTotal,8,'keeps accumulating');
"""),
("نگه‌داشتن بانک می‌کند و برد در ۱۰۰", """
var st=L.newGame();L.startTurn(st,0);
var four=function(){return 3/6;};
L.roll(st,four);L.roll(st,four);
T.eq(st.turnTotal,8,'8 bankable');
T.eq(L.hold(st),8,'hold returns banked');
T.eq(st.scores[0],8,'banked into scores');T.eq(st.turnTotal,0,'turn total cleared');
T.ok(!st.over,'no win below 100');
var st2=L.newGame();st2.scores=[95,40];L.startTurn(st2,0);st2.turnTotal=5;
L.hold(st2);
T.ok(st2.over,'game over at 100');T.eq(st2.winner,0,'winner set');T.eq(st2.scores[0],100,'exactly 100');
"""),
("تصمیم ربات: نگه‌دار یا بران", """
var st=L.newGame();
st.scores=[0,0];L.startTurn(st,0);st.turnTotal=19;
T.eq(L.aiDecision(st),'roll','19 keeps rolling');
st.turnTotal=20;T.eq(L.aiDecision(st),'hold','20 holds');
st.scores=[97,50];st.turnTotal=3;
T.eq(L.aiDecision(st),'hold','holds when banking wins (100)');
st.scores=[90,50];st.turnTotal=9;
T.eq(L.aiDecision(st),'roll','99 keeps rolling');
st.scores=[90,50];st.turnTotal=10;
T.eq(L.aiDecision(st),'hold','never rolls past win');
"""),
("بازی کامل شبیه‌سازی‌شده تا برد", """
var st=L.newGame(),idx=0,turns=0;
while(!st.over&&turns<5000){L.takeTurn(st,idx,L.aiDecision,rng);idx=1-idx;turns++;}
T.ok(st.over,'game terminated');
T.ok(turns<5000,'terminated in finite turns: '+turns);
T.ok(st.winner===0||st.winner===1,'winner index valid');
T.ok(st.scores[st.winner]>=100,'winner has at least 100');
T.ok(st.scores[1-st.winner]<100,'loser below 100');
"""),
]

CHUCK_LOGIC = r"""
function cRoll3(rng){var r=rng||Math.random,d=[0,0,0],i;
 for(i=0;i<3;i++)d[i]=1+Math.floor(r()*6);
 return d;}
function cMatches(dice,face){var m=0,i;for(i=0;i<3;i++)if(dice[i]===face)m++;return m;}
function cPayout(stake,m){return m>0?stake*m:-stake;}
function cReturn(stake,m){return m>0?stake+stake*m:0;}
function cApply(state,rng){var dice=cRoll3(rng),m=cMatches(dice,state.bet),net=cPayout(state.stake,m);
 state.credits+=net;state.last={dice:dice,matches:m,net:net};return state.last;}
var WOG_LOGIC={roll3:cRoll3,matches:cMatches,payout:cPayout,totalReturn:cReturn,apply:cApply};
"""

CHUCK_UI = r"""
var DIE='⚀⚁⚂⚃⚄⚅';
var st={credits:100,stake:10,bet:1},rounds=0;
$('#hint').textContent='روی یکی از اعداد ۱ تا ۶ شرط ببندید (۵ تا ۵۰ اعتبار). هر تاس برابر عدد شما، به‌اندازهٔ شرط به شما جایزه می‌دهد و خود شرط برمی‌گردد؛ بی‌تطبیق یعنی از دست رفتن شرط.';
$('#app').innerHTML='<div class="cred" id="cr"></div><div class="lbl">مقدار شرط</div><div class="stakes" id="stakes"></div><div class="lbl">عدد شرط</div><div class="faces" id="faces"></div><div class="dice3" id="d3">⚄⚄⚄</div><div class="btns"><button class="btn" id="btnRoll" data-smoke>برانید</button><button class="btn alt" id="btnNew" data-smoke>شروع مجدد</button></div><div class="msg" id="msg"></div>';
function render(){
 $('#cr').textContent='اعتبار: '+fa(st.credits)+' — رکورد: '+fa(+(store.get('wog-chuck-best')||0));
 var sh='';[5,10,20,50].forEach(function(v){sh+='<button class="st'+(st.stake===v?' on':'')+'" data-v="'+v+'"'+(st.credits<v?' disabled':'')+'>'+fa(v)+'</button>';});
 $('#stakes').innerHTML=sh;
 var fh='',i;for(i=1;i<=6;i++)fh+='<button class="face'+(st.bet===i?' on':'')+'" data-v="'+i+'">'+DIE.charAt(i-1)+'</button>';
 $('#faces').innerHTML=fh;
 hud('اعتبار: '+fa(st.credits)+' — شرط: '+fa(st.stake)+' روی '+fa(st.bet)+' — دست: '+fa(rounds));}
function newG(){st={credits:100,stake:10,bet:1};rounds=0;$('#d3').textContent='⚄⚄⚄';$('#msg').textContent='';$('#msg').className='msg';render();}
$('#app').addEventListener('click',function(e){
 var el=e.target.closest?e.target.closest('.st'):null;
 if(el&&!el.disabled){st.stake=+el.getAttribute('data-v');render();return;}
 el=e.target.closest?e.target.closest('.face'):null;
 if(el){st.bet=+el.getAttribute('data-v');render();}});
$('#btnRoll').addEventListener('click',function(){
 if(st.credits<st.stake){toast('اعتبار برای این شرط کافی نیست');return;}
 L.apply(st);rounds++;
 var last=st.last;
 $('#d3').textContent=DIE.charAt(last.dice[0]-1)+DIE.charAt(last.dice[1]-1)+DIE.charAt(last.dice[2]-1);
 var m=$('#msg');
 if(last.matches>0){m.className='msg';m.textContent=fa(last.matches)+' تطبیق! '+fa(last.net)+' اعتبار بردید';}
 else{m.className='msg lose';m.textContent='تطبیقی نبود؛ '+fa(st.stake)+' اعتبار از دست رفت';}
 var b=+(store.get('wog-chuck-best')||0);
 if(st.credits>b)store.set('wog-chuck-best',String(st.credits));
 if(st.credits<5){ovl('اعتبار تمام شد','اعتبار پایانی: '+fa(st.credits)+' در '+fa(rounds)+' دست','شروع مجدد',newG);}
 render();});
$('#btnNew').addEventListener('click',newG);
render();
"""

CHUCK_CSS = r"""
#app{max-width:540px;margin:0 auto;padding:6px 10px;text-align:center}
.cred{font-size:20px;color:#d9a441;font-weight:700;margin:6px 0}
.lbl{color:#8fa3c8;font-size:13px;margin:10px 0 4px}
.stakes,.faces{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.st{min-width:56px;min-height:42px;border-radius:9px;border:2px solid #233052;background:#14203a;color:#f3ead8;font-size:16px;cursor:pointer;touch-action:manipulation;font-family:inherit}
.st.on{border-color:#d9a441;color:#d9a441;background:#332a12}
.st[disabled]{opacity:.4}
.face{width:50px;height:50px;font-size:28px;line-height:1;border-radius:12px;border:2px solid #233052;background:#14203a;color:#f3ead8;cursor:pointer;touch-action:manipulation;padding:0;font-family:inherit}
.face.on{border-color:#3fb8af;background:#0f2e33;color:#3fb8af}
.dice3{display:flex;gap:12px;justify-content:center;font-size:52px;margin:12px 0;color:#f3ead8}
.btns{display:flex;gap:10px;justify-content:center;margin:8px 0}
.btn{min-height:44px;border:0;border-radius:10px;background:#d9a441;color:#14203a;font-weight:700;padding:10px 22px;cursor:pointer;touch-action:manipulation;font-family:inherit;font-size:15px}
.btn.alt{background:#3fb8af;color:#0c1526}
.msg{min-height:24px;color:#67b98a;font-size:15px;margin-top:6px}
.msg.lose{color:#e26d5c}
"""

CHUCK_TESTS = [
("نرخ پرداخت بر اساس تعداد تطبیق", """
T.eq(L.payout(10,0),-10,'no match loses stake');
T.eq(L.payout(10,1),10,'one match pays 1:1');
T.eq(L.payout(10,2),20,'two matches pay 2:1');
T.eq(L.payout(10,3),30,'three matches pay 3:1');
T.eq(L.payout(50,3),150,'scales with stake');
T.eq(L.totalReturn(10,0),0,'no return on 0');
T.eq(L.totalReturn(10,1),20,'stake back + win');
T.eq(L.totalReturn(10,2),30,'stake + 2x');
"""),
("ریس سه تاس و شمارش تطبیق", """
T.eq(L.roll3(function(){return 0;}),[1,1,1],'floor 0 => ones');
T.eq(L.roll3(function(){return 0.999;}),[6,6,6],'near 1 => sixes');
T.eq(L.matches([3,3,5],3),2,'two matches');
T.eq(L.matches([1,2,3],4),0,'zero matches');
T.eq(L.matches([4,4,4],4),3,'triple matches');
"""),
("اعمال شرط روی اعتبار", """
var st={credits:100,stake:10,bet:3};
var seq=[2/6,2/6,4/6],i=0,r=function(){return seq[i++%3];};
L.apply(st,r);
T.eq(st.last.dice,[3,3,5],'dice as seeded');
T.eq(st.last.matches,2,'two matches counted');
T.eq(st.last.net,20,'net +20');
T.eq(st.credits,120,'credits updated');
L.apply(st,function(){return 0.999;});
T.eq(st.last.dice,[6,6,6],'second roll');
T.eq(st.last.matches,0,'no match vs 3');
T.eq(st.last.net,-10,'net -10');
T.eq(st.credits,110,'credits debited');
"""),
("توزیع تطبیق‌ها و EV در ۵۰۰۰ دست", """
var st={credits:100,stake:10,bet:1},N=5000,nets=0,msum=0,m3=0,i;
for(i=0;i<N;i++){L.apply(st,rng);nets+=st.last.net;msum+=st.last.matches;if(st.last.matches===3)m3++;}
T.eq(st.credits,100+nets,'credits accounting exact');
T.near(msum/N,0.5,0.08,'avg matches ~0.5 (binomial mean)');
T.ok(m3/N<0.05,'triple rare, rate='+(m3/N));
T.ok(nets/N<1.05,'EV below 1.05 per round: '+(nets/N));
T.ok(nets<0,'house edge: player net negative over sim');
"""),
]

pig = G('pig','تاس پیگ','luck','🐷','#3fb8af','#d9a441',
 'تاس بیندازید و شمارش نوبت را جمع کنید؛ با آمدن ۱ همهٔ شمارش می‌سوزد. ربات محتاط را در رسیدن به ۱۰۰ امتیاز شکست دهید.',
 'اگر ۱ بیاید شمارش نوبت می‌سوزد؛ در ۲۰ یا نزدیک برد «نگه‌دار» بزنید.',
 logic=PIG_LOGIC, ui=PIG_UI, css=PIG_CSS, engines=('common',), tests=PIG_TESTS)

yahtzee = G('yahtzee','یاتزی','luck','🎲','#d9a441','#3fb8af',
 'یاتزی تک‌نفره با ۵ تاس و ۳ پرتاب در هر نوبت؛ ۱۳ خانهٔ امتیاز را هوشمندانه پر کنید و جایزهٔ ۳۵ امتیازیِ بالایی را از دست ندهید.',
 'تاس را لمس کنید تا ثابت بماند؛ پس از حداکثر ۳ پرتاب، امتیاز را در یکی از ۱۳ خانهٔ باز ثبت کنید.',
 logic=YAHTZEE_LOGIC, ui=YAHTZEE_UI, css=YAHTZEE_CSS, engines=('common',), tests=YAHTZEE_TESTS)

chuck = G('chuck-a-luck','سه تاس','luck','🎰','#e26d5c','#d9a441',
 'سه تاس می‌چرخند؛ روی عدد دلخواه شرط ببندید — هر تطبیق به‌اندازهٔ شرط شما جایزه دارد (۱تا۳ برابر).',
 'شرط (۵ تا ۵۰) و عدد را انتخاب کنید و برانید؛ ۳ تطبیق یعنی ۳ برابر شرط.',
 logic=CHUCK_LOGIC, ui=CHUCK_UI, css=CHUCK_CSS, engines=('common',), tests=CHUCK_TESTS)

GAMES = [yahtzee, pig, chuck]
