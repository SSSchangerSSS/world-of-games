# -*- coding: utf-8 -*-
# AG-A3 — four light card games for World of Games (one mini-kit batch)
# tripeaks / clock / crazy-eights / war  — cat="cards", engines=("common","card")
from lib_mini import G

CSS_BASE = r"""#app{max-width:720px;margin:0 auto}.panel{background:#14203a;border:1px solid #22335c;border-radius:14px;padding:10px;margin:8px 0}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;justify-content:center;min-height:44px}.lbl{color:#9fb0cf;font-size:14px}.cnt{color:#d9a441;font-size:13px}.tslot{width:30px;height:44px;border:1px dashed #2a3a5f;border-radius:6px}button{min-height:44px;border-radius:10px;border:1px solid #2a3a5f;background:#1b2a4a;color:#e8ecf4;font-size:15px;padding:8px 14px;cursor:pointer;touch-action:manipulation}button.gold{background:#d9a441;border-color:#d9a441;color:#1a1408;font-weight:700}.wcard.live{outline:2px solid #d9a441;cursor:pointer}"""

# ---------------------------------------------------------------- tripeaks
LOGIC_TRI = r"""var WOG_LOGIC=(function(){
function mkD(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<14;r++)d.push({s:s,r:r});return d;}
function shuf(a,f){var i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(f()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
var ROWS=[3,4,5,6,10],START=[0,3,7,12,18];
function rowOf(i){var k;for(k=4;k>=0;k--){if(i>=START[k])return k;}return 0;}
function covers(i){var k=rowOf(i),j,out=[];if(k<1||k>3)return out;j=i-START[k];if(j-1>=0&&j-1<ROWS[k-1])out.push(START[k-1]+j-1);if(j<ROWS[k-1])out.push(START[k-1]+j);return out;}
function newGame(rng){var f=rng||Math.random,d=shuf(mkD(),f),st={t:d.slice(0,28),stock:d.slice(28),waste:[],combo:0,score:0,removed:0};drawStock(st);return st;}
function wasteTop(st){return st.waste.length?st.waste[st.waste.length-1]:null;}
function isExposed(st,i){if(i<0||i>27||!st.t[i])return false;var cv=covers(i),k;for(k=0;k<cv.length;k++)if(st.t[cv[k]])return false;return true;}
function canPlay(card,wt){if(!card||!wt)return false;var d=(card.r-wt.r+13)%13;return d===1||d===12;}
function play(st,i){if(!isExposed(st,i))throw new Error('poshide');if(!canPlay(st.t[i],wasteTop(st)))throw new Error('rank');st.waste.push(st.t[i]);st.t[i]=null;st.combo++;st.score+=st.combo;st.removed++;}
function drawStock(st){if(!st.stock.length)return false;st.waste.push(st.stock.pop());st.combo=0;return true;}
function hasMoves(st){var i;if(wasteTop(st)){for(i=0;i<28;i++)if(st.t[i]&&isExposed(st,i)&&canPlay(st.t[i],wasteTop(st)))return true;}return st.stock.length>0;}
function isWin(st){return st.removed===28;}
function accounted(st){var i,n=0;for(i=0;i<28;i++)if(st.t[i])n++;return n+st.stock.length+st.waste.length;}
return {newGame:newGame,isExposed:isExposed,canPlay:canPlay,play:play,drawStock:drawStock,hasMoves:hasMoves,isWin:isWin,wasteTop:wasteTop,accounted:accounted};
})();
"""

UI_TRI = r"""var st=null;
function tcnt(){var i,n=0;for(i=0;i<28;i++)if(st.t[i])n++;return n;}
function wtop(){return st.waste.length?st.waste[st.waste.length-1]:null;}
function deal(){st=L.newGame();render();}
function render(){
 var best=store.get('wog-tripeaks-best');
 hud('امتیاز: <b>'+fa(st.score)+'</b> · کمبو: <b>'+fa(st.combo)+'</b> · مانده: <b>'+fa(tcnt())+'</b>'+(best?' · رکورد: <b>'+fa(+best)+'</b>':''));
 var app=$('#app');app.innerHTML='';
 var wrap=ce('div','panel','');
 var seg=[[0,3,0],[3,4,1],[7,5,2],[12,6,3],[18,10,4]];
 seg.forEach(function(sg){
  var r=ce('div','trow r'+sg[2],'');
  for(var i=sg[0];i<sg[0]+sg[1];i++){
   (function(i){
    var c=st.t[i];
    if(!c){r.appendChild(ce('div','tslot',''));return;}
    var el=cardEl(c,true,'tiny');
    if(sg[2]<4&&L.isExposed(st,i))el.classList.add('live');
    el.onclick=function(){act(i);};
    r.appendChild(el);
   })(i);
  }
  wrap.appendChild(r);
 });
 app.appendChild(wrap);
 var bot=ce('div','row','');
 var dw=ce('div','panel row','');
 dw.appendChild(ce('span','lbl','روی میز:'));
 if(wtop())dw.appendChild(cardEl(wtop(),true,'small'));else dw.appendChild(ce('div','tslot',''));
 bot.appendChild(dw);
 var sb=ce('button','gold','دانته ('+fa(st.stock.length)+')');
 sb.setAttribute('data-smoke','1');
 sb.onclick=function(){if(!L.drawStock(st))toast('دانته خالی است');render();checkEnd();};
 bot.appendChild(sb);
 var nb=ce('button','','بازی جدید');nb.onclick=deal;bot.appendChild(nb);
 app.appendChild(bot);
 $('#hint').textContent='کارت آزادی بردار که رتبهاش یکی کمتر یا بیشتر از کارتِ روی میز باشد (شاه و آس به هم میچسبند)؛ در گیری از دانته بکش.';
}
function act(i){
 var c=st.t[i];if(!c)return;
 if(!L.isExposed(st,i)){toast('این کارت هنوز زیر کارت دیگری است');return;}
 if(!L.canPlay(c,wtop())){toast('رتبه سازگار نیست');return;}
 L.play(st,i);render();checkEnd();
}
function checkEnd(){
 if(L.isWin(st)){
  var b=store.get('wog-tripeaks-best');
  if(!b||st.score>+b)store.set('wog-tripeaks-best',''+st.score);
  ovl('بردی!','هر ۲۸ کارت تپهها رفت — امتیاز '+fa(st.score),'دوباره',deal);
  return;}
 if(!L.hasMoves(st))ovl('باختی','نه حرکتی ماند و نه دانته‌ای — امتیاز '+fa(st.score),'دوباره',deal);
}
deal();"""

CSS_TRI = CSS_BASE + r""".trow{display:flex;gap:4px;justify-content:center;margin:3px 0}.r0{gap:44px}.r1{gap:18px}.r2{gap:9px}"""

TESTS_TRI = [
(r"""مجاورت با چرخهٔ کیو-ک-آس""", r"""
T.ok(L.canPlay({s:0,r:12},{s:1,r:13}),'Q-K');
T.ok(L.canPlay({s:0,r:13},{s:1,r:1}),'K-A wrap');
T.ok(L.canPlay({s:0,r:1},{s:1,r:13}),'A-K wrap');
T.ok(!L.canPlay({s:0,r:2},{s:1,r:13}),'2-K no');
T.ok(!L.canPlay({s:0,r:5},{s:1,r:5}),'equal no');
T.ok(L.canPlay({s:0,r:7},{s:1,r:6}),'down one');
T.ok(L.canPlay({s:0,r:7},{s:1,r:8}),'up one');
T.ok(!L.canPlay({s:0,r:7},null),'no waste card');
"""),
(r"""دروازهٔ رو بودن (کارت پوشیده رد میشود)""", r"""
var st=L.newGame(rng),i;
for(i=0;i<3;i++)T.ok(L.isExposed(st,i),'top '+i);
for(i=18;i<28;i++)T.ok(L.isExposed(st,i),'base '+i);
for(i=3;i<18;i++)T.ok(!L.isExposed(st,i),'covered '+i);
st.t[0]={s:0,r:6};st.t[3]={s:0,r:5};st.waste=[{s:1,r:6}];
T.ok(!L.isExposed(st,3),'slot3 covered');
T.throws(function(){L.play(st,3);},'covered rejected');
st.t[0]=null;
T.ok(L.isExposed(st,3),'slot3 freed');
L.play(st,3);
T.eq(st.removed,1,'removed 1');
"""),
(r"""کمبو و امتیاز با بازنشانی روی کشیدن""", r"""
var st=L.newGame(rng),i;
for(i=0;i<28;i++)st.t[i]=null;
st.stock=[];st.waste=[{s:1,r:5}];st.combo=0;st.score=0;st.removed=0;
st.t[18]={s:0,r:4};st.t[19]={s:2,r:3};st.t[20]={s:3,r:2};st.t[21]={s:0,r:8};
L.play(st,18);T.eq(st.combo,1,'c1');T.eq(st.score,1,'s1');
L.play(st,19);T.eq(st.combo,2,'c2');T.eq(st.score,3,'s2');
L.play(st,20);T.eq(st.combo,3,'c3');T.eq(st.score,6,'s3');
st.stock=[{s:2,r:9}];
L.drawStock(st);T.eq(st.combo,0,'combo reset on draw');T.eq(st.score,6,'score kept');
L.play(st,21);T.eq(st.combo,1,'combo after draw');T.eq(st.score,7,'s4');
"""),
(r"""حسابداری ۵۲ کارت در پخش کامل""", r"""
var st=L.newGame(rng),g=0,plays=0;
function acc(){var i,n=0;for(i=0;i<28;i++)if(st.t[i])n++;return n+st.stock.length+st.waste.length;}
function onestep(){var i;
 for(i=0;i<28;i++)if(st.t[i]&&L.isExposed(st,i)&&L.canPlay(st.t[i],L.wasteTop(st))){L.play(st,i);plays++;return true;}
 if(st.stock.length){L.drawStock(st);return true;}
 return false;}
while(g<60&&onestep()){g++;T.eq(acc(),52,'52 @'+g);}
T.ok(g<60,'terminated');
if(L.isWin(st))T.eq(plays,28,'win means 28 plays');
else T.eq(st.stock.length,0,'stuck means empty stock');
"""),
(r"""تشخیص برد و باخت""", r"""
var st=L.newGame(rng),i;
T.ok(!L.isWin(st),'fresh not win');
T.ok(L.hasMoves(st),'fresh has moves');
for(i=0;i<28;i++)st.t[i]=null;st.removed=28;
T.ok(L.isWin(st),'win detected');
var s2=L.newGame(rng);
for(i=0;i<28;i++)s2.t[i]=(i===19)?{s:0,r:2}:null;
s2.stock=[];s2.waste=[{s:0,r:5}];
T.ok(!L.hasMoves(s2),'stuck: no moves');
T.ok(!L.isWin(s2),'stuck: not win');
"""),
(r"""قطعیت پخش اولیه (۲۸+۲۳+۱)""", r"""
function mb(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t^(t>>>14))>>>0;return t/4294967296;};}
var s1=L.newGame(mb(777)),s2=L.newGame(mb(777));
T.eq(JSON.stringify(s1),JSON.stringify(s2),'same seed same deal');
T.eq(s1.t.length,28,'28 tableau');
T.eq(s1.stock.length,23,'23 stock');
T.eq(s1.waste.length,1,'1 waste');
T.eq(s1.t.length+s1.stock.length+s1.waste.length,52,'52 total');
"""),
]

# ---------------------------------------------------------------- clock
LOGIC_CLK = r"""var WOG_LOGIC=(function(){
function mkD(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<14;r++)d.push({s:s,r:r});return d;}
function shuf(a,f){var i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(f()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
function newGame(rng){var f=rng||Math.random,d=shuf(mkD(),f),p=[],i;
 for(i=0;i<13;i++)p.push(d.slice(i*4,i*4+4));
 return{piles:p,up:[[],[],[],[],[],[],[],[],[],[],[],[],[]],cur:0,kings:0,revealed:0,done:false,won:false};}
function step(st){
 if(st.done)return{card:null,toPile:-1,kings:st.kings,done:true,won:st.won};
 var p=st.piles[st.cur];
 if(!p.length){st.done=true;return{card:null,toPile:-1,kings:st.kings,done:true,won:false};}
 var c=p.pop();st.revealed++;var tp=c.r-1;st.up[tp].push(c);
 if(c.r===13)st.kings++;
 if(st.kings===4){st.done=true;st.won=(st.revealed===52);}
 else if(st.revealed===52){st.done=true;st.won=true;}
 else st.cur=tp;
 return{card:c,toPile:tp,kings:st.kings,done:st.done,won:st.won};}
function runToEnd(rng){var st=newGame(rng),n=0,steps=[];while(!st.done&&n<60){steps.push(step(st));n++;}return{state:st,steps:steps};}
function countLeft(st){var i,n=0;for(i=0;i<13;i++)n+=st.piles[i].length+st.up[i].length;return n;}
return{newGame:newGame,step:step,runToEnd:runToEnd,countLeft:countLeft};
})();
"""

UI_CLK = r"""var st=null,last=null;
function deal(){st=L.newGame();last=null;render();}
function render(){
 hud('رو شده: <b>'+fa(st.revealed)+'</b> از ۵۲ · شاه: <b>'+fa(st.kings)+'</b> از ۴');
 var app=$('#app');app.innerHTML='';
 var grid=ce('div','cgrid','');
 for(var i=0;i<13;i++){
  (function(i){
   var cell=ce('div','ccell'+(i===12?' ctr':'')+((i===st.cur&&!st.done)?' cur':''),'');
   cell.appendChild(ce('div','clbl',rankFa(i+1)));
   var n=st.piles[i].length;
   if(n){
    cell.appendChild(cardEl(st.piles[i][n-1],false,'tiny'));
    cell.appendChild(ce('div','cnt',fa(n)+' کارت'));
   }else{
    var d=ce('div','edone',''),u=st.up[i];
    if(u.length)d.appendChild(cardEl(u[u.length-1],true,'tiny'));
    else d.appendChild(ce('div','tslot',''));
    cell.appendChild(d);
   }
   grid.appendChild(cell);
  })(i);
 }
 app.appendChild(grid);
 var big=ce('div','panel row','');
 if(last&&last.card){
  big.appendChild(cardEl(last.card,true,'small'));
  big.appendChild(ce('span','lbl','به پشتهٔ '+rankFa(last.toPile+1)+' رفت'));
 }else big.appendChild(ce('span','lbl','شروع: کارت اول از پشتهٔ آس رو میشود'));
 app.appendChild(big);
 var r=ce('div','row','');
 var b1=ce('button','gold','یک کارت رو کن');
 b1.setAttribute('data-smoke','1');b1.onclick=stepOnce;
 var b2=ce('button','','تا آخر، خودکار');b2.onclick=autoRun;
 var b3=ce('button','','بازی جدید');b3.onclick=deal;
 r.appendChild(b1);r.appendChild(b2);r.appendChild(b3);
 app.appendChild(r);
 $('#hint').textContent='کارت رو شده به پشتهٔ هم رتبه خودش میرود و کارت تازه از همان پشته رو میشود؛ چهارمین شاه یعنی باخت، مگر آخرین کارت باشد.';
}
function stepOnce(){if(st.done)return;last=L.step(st);render();if(st.done)end();}
function autoRun(){var g=0;while(!st.done&&g<60){last=L.step(st);g++;}render();end();}
function end(){
 if(st.won)ovl('بردی!','چهارمین شاه آخرین کارت بود؛ هر ۵۲ کارت رو شدند','بازی جدید',deal);
 else if(st.kings>=4)ovl('باختی','چهارمین شاه رو شد؛ '+fa(st.revealed)+' کارت رو شده بود','بازی جدید',deal);
 else ovl('گیر کردی','پشتهٔ مقصد خالی بود؛ '+fa(st.revealed)+' کارت رو شده بود','بازی جدید',deal);
}
deal();"""

CSS_CLK = CSS_BASE + r""".cgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.ccell{background:#14203a;border:1px solid #22335c;border-radius:10px;padding:6px;text-align:center}.ccell.cur{border-color:#d9a441;box-shadow:0 0 0 2px #d9a441}.ccell.ctr{grid-column:1/-1}.clbl{color:#9fb0cf;font-size:13px}.edone{min-height:30px}"""

TESTS_CLK = [
(r"""نقشهٔ رتبه به پشته""", r"""
var r=L.runToEnd(rng),i;
T.ok(r.steps.length>0,'steps exist');
for(i=0;i<r.steps.length;i++){var s=r.steps[i];
 if(!s.card)continue;
 T.eq(s.toPile,s.card.r-1,'pile of rank @'+i);}
"""),
(r"""باخت با چهارمین شاه""", r"""
var st=L.newGame(rng);st.kings=3;st.piles[st.cur].push({s:0,r:13});
var res=L.step(st);
T.eq(res.kings,4,'kings 4');
T.eq(res.card.r,13,'revealed K');
T.ok(res.done,'done');
T.ok(!res.won,'lost');
"""),
(r"""برد در آخرین کارت""", r"""
var st=L.newGame(rng);st.kings=3;st.revealed=51;st.piles[st.cur].push({s:1,r:13});
var res=L.step(st);
T.ok(res.done&&res.won,'won on final K');
T.eq(st.revealed,52,'all 52 revealed');
"""),
(r"""قطعیت و خاتمه روی ۲۰ بذر""", r"""
function mb(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t^(t>>>14))>>>0;return t/4294967296;};}
var s;
for(s=1;s<=20;s++){
 var r1=L.runToEnd(mb(s)),r2=L.runToEnd(mb(s));
 T.ok(r1.state.done,'done seed '+s);
 T.ok(r1.steps.length<=53,'bounded seed '+s);
 T.eq(JSON.stringify(r1.steps),JSON.stringify(r2.steps),'deterministic seed '+s);}
"""),
(r"""حفظ ۵۲ کارت در طول بازی""", r"""
var st=L.newGame(rng),g=0,i,up;
function left(){var n=0,k;for(k=0;k<13;k++)n+=st.piles[k].length+st.up[k].length;return n;}
T.eq(left(),52,'initial 52');
while(!st.done&&g<60){L.step(st);g++;T.eq(left(),52,'52 @'+g);}
T.eq(left(),52,'final 52');
up=0;for(i=0;i<13;i++)up+=st.up[i].length;
T.eq(up,st.revealed,'face-up equals revealed');
"""),
(r"""ساختار بازی جدید""", r"""
var st=L.newGame(rng),i,k,seen={};
T.eq(st.piles.length,13,'13 piles');
for(i=0;i<13;i++){T.eq(st.piles[i].length,4,'4 cards @'+i);
 for(k=0;k<4;k++){var c=st.piles[i][k],key=c.s*13+c.r;T.ok(!seen[key],'unique '+key);seen[key]=1;}}
T.eq(st.cur,0,'start at pile 0');
T.eq(st.kings,0,'no kings yet');
T.ok(!st.done,'not done');
"""),
]

# ---------------------------------------------------------------- crazy-eights
LOGIC_E8 = r"""var WOG_LOGIC=(function(){
function mkD(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<14;r++)d.push({s:s,r:r});return d;}
function shuf(a,f){var i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(f()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
function newGame(rng,prev){var f=rng||Math.random,d=shuf(mkD(),f),h0=[],h1=[],i,c;
 for(i=0;i<5;i++){h0.push(d.pop());h1.push(d.pop());}
 for(;;){c=d.pop();if(c.r===8){d.unshift(c);}else break;}
 var sc=(prev&&prev.scores)?[prev.scores[0],prev.scores[1]]:[0,0];
 var rd=(prev&&typeof prev.round==='number')?prev.round:0;
 return{hands:[h0,h1],stock:d,discard:[c],suit:c.s,turn:rd%2,scores:sc,round:rd,passes:0,over:false,winner:-1,pts:0};}
function topCard(st){return st.discard[st.discard.length-1];}
function legalPlays(st,p){var h=st.hands[p],t=topCard(st),out=[],i,c;
 for(i=0;i<h.length;i++){c=h[i];
  if(c.r===8||c.s===st.suit||(t.r!==8&&c.r===t.r))out.push(c);}
 return out;}
function findIdx(h,card){var i;for(i=0;i<h.length;i++)if(h[i].s===card.s&&h[i].r===card.r)return i;return -1;}
function playCard(st,p,card,chosen){var h=st.hands[p],i=findIdx(h,card),t=topCard(st);
 if(i<0)throw new Error('not-in-hand');
 if(!(card.r===8||card.s===st.suit||(t.r!==8&&card.r===t.r)))throw new Error('illegal');
 h.splice(i,1);st.discard.push(card);
 st.suit=(card.r===8&&typeof chosen==='number'&&chosen>=0&&chosen<=3)?chosen:card.s;
 st.passes=0;
 if(!h.length){st.over=true;st.winner=p;st.pts=handPoints(st.hands[1-p]);st.scores[p]+=st.pts;}
 else st.turn=1-p;
 return st;}
function drawUpTo(st,p,n){var h=st.hands[p],k=0;while(k<n&&st.stock.length){h.push(st.stock.pop());k++;}if(k)st.passes=0;return k;}
function passTurn(st,p){st.passes++;if(st.passes>=2){st.over=true;st.winner=-1;st.pts=0;}else st.turn=1-p;return st;}
function handPoints(h){var n=0,i,c;for(i=0;i<h.length;i++){c=h[i];if(c.r===8)n+=50;else if(c.r===1)n+=1;else if(c.r>=11)n+=10;else n+=c.r;}return n;}
function isRoundOver(st){return !!st.over;}
function isMatchOver(st){return st.scores[0]>=200?0:(st.scores[1]>=200?1:-1);}
function aiChooseSuit(h){var cnt=[0,0,0,0],i,b=0;for(i=0;i<h.length;i++)cnt[h[i].s]++;for(i=1;i<4;i++)if(cnt[i]>cnt[b])b=i;return b;}
function no8(h){var out=[],i,g=false;for(i=0;i<h.length;i++){if(!g&&h[i].r===8){g=true;continue;}out.push(h[i]);}return out;}
function pick(legal){var i;for(i=0;i<legal.length;i++)if(legal[i].r!==8)return legal[i];return legal.length?legal[0]:null;}
function aiTurn(st){if(st.over)return null;var p=st.turn,b=pick(legalPlays(st,p)),cs;
 if(!b){drawUpTo(st,p,3);b=pick(legalPlays(st,p));}
 if(!b)return passTurn(st,p);
 if(b.r===8){var rem=no8(st.hands[p]);cs=rem.length?aiChooseSuit(rem):b.s;}
 return playCard(st,p,b,cs);}
return{newGame:newGame,legalPlays:legalPlays,playCard:playCard,drawUpTo:drawUpTo,passTurn:passTurn,handPoints:handPoints,isRoundOver:isRoundOver,isMatchOver:isMatchOver,aiChooseSuit:aiChooseSuit,aiTurn:aiTurn};
})();
"""

UI_E8 = r"""var st=null,pending=null,ended=false;
function fresh(s,r){
 st=s?L.newGame(null,{scores:s,round:r}):L.newGame();
 pending=null;ended=false;render();tick();
}
function deal(){fresh(null,0);}
function render(){
 hud('تو <b>'+fa(st.scores[0])+'</b> · حریف <b>'+fa(st.scores[1])+'</b> · دست '+fa(st.round+1)+' · '+(st.turn===0?'نوبت تو':'نوبت حریف'));
 var app=$('#app');app.innerHTML='';
 var ai=ce('div','panel row','');
 ai.appendChild(ce('span','lbl','حریف: '+fa(st.hands[1].length)+' کارت'));
 app.appendChild(ai);
 var mid=ce('div','panel row','');
 mid.appendChild(ce('span','lbl','روی میز:'));
 mid.appendChild(cardEl(st.discard[st.discard.length-1],true,'small'));
 mid.appendChild(ce('span','suit'+((st.suit===1||st.suit===2)?' red':''),SUITS[st.suit]));
 mid.appendChild(ce('span','lbl','دانته: '+fa(st.stock.length)));
 app.appendChild(mid);
 if(pending){app.appendChild(suitChooser());app.appendChild(hintBtns(true,[]));}
 else{
  var lp=(st.turn===0&&!st.over)?L.legalPlays(st,0):[];
  var hr=ce('div','panel row','');
  st.hands[0].forEach(function(c){
   var el=cardEl(c,true,'small');
   var ok=lp.some(function(x){return x.s===c.s&&x.r===c.r;});
   if(ok)el.classList.add('live');
   el.onclick=function(){humanPlay(c);};
   hr.appendChild(el);
  });
  app.appendChild(hr);
  app.appendChild(hintBtns(false,lp));
 }
 $('#hint').textContent='با خال یا عدد یکسان بازی کن؛ هشت هر وقت بخواهی میافتد و خال بعدی را خودت تعیین میکنی؛ اگر ساخ نیست تا ۳ کارت بکش.';
}
function hintBtns(choosing,lp){
 var r=ce('div','row','');
 if(!choosing&&st.turn===0&&!st.over&&lp&&!lp.length){
  var db=ce('button','gold','نداری؟ تا ۳ کارت بکش');
  db.setAttribute('data-smoke','1');
  db.onclick=function(){
   var got=L.drawUpTo(st,0,3);
   toast(fa(got)+' کارت کشیدی');
   render();
   if(!L.legalPlays(st,0).length){toast('باز هم ساخ نیست — رد');L.passTurn(st,0);render();tick();}
  };
  r.appendChild(db);
 }
 var nb=ce('button','','بازی جدید');nb.onclick=deal;r.appendChild(nb);
 return r;
}
function suitChooser(){
 var p=ce('div','panel row','');
 p.appendChild(ce('span','lbl','خال بعدی را انتخاب کن:'));
 for(var k=0;k<4;k++){
  (function(k){
   var b=ce('button','gold'+((k===1||k===2)?' red':''),SUITS[k]);
   b.setAttribute('data-smoke','1');
   b.onclick=function(){var c=pending;pending=null;L.playCard(st,0,c,k);render();tick();};
   p.appendChild(b);
  })(k);
 }
 return p;
}
function humanPlay(c){
 if(st.over||st.turn!==0||pending)return;
 if(c.r===8){pending=c;render();return;}
 var lp=L.legalPlays(st,0);
 var ok=lp.some(function(x){return x.s===c.s&&x.r===c.r;});
 if(!ok){toast('این کارت الان ساخ نیست');return;}
 L.playCard(st,0,c);render();tick();
}
function tick(){
 if(st.over){roundEnd();return;}
 if(st.turn===1){
  setTimeout(function(){
   if(st.over)return;
   L.aiTurn(st);render();
   if(st.over)roundEnd();
  },700);
 }
}
function roundEnd(){
 if(ended)return;ended=true;
 var mw=L.isMatchOver(st);
 if(mw>=0){
  ovl(mw===0?'بردی!':'باختی','پایان مسابقه: '+fa(st.scores[0])+' در برابر '+fa(st.scores[1]),'بازی جدید',deal);
  return;
 }
 var w=st.winner;
 ovl(w===0?'دست را بردی':'دست را باختی',w>=0?(fa(st.pts)+' امتیاز گرفتی'):'بازی قفل شد؛ بدون امتیاز','دست بعد',function(){
  fresh(st.scores,st.round+1);
 });
}
deal();"""

CSS_E8 = CSS_BASE + r""".suit{font-size:24px;color:#e8ecf4}.suit.red{color:#e26d5c}"""

TESTS_E8 = [
(r"""قوانین مجوز بازی""", r"""
var st=L.newGame(rng);
st.hands[0]=[{s:0,r:9},{s:1,r:5},{s:2,r:11},{s:3,r:7},{s:1,r:13}];
st.discard=[{s:0,r:5}];st.suit=0;st.turn=0;st.over=false;
var lp=L.legalPlays(st,0);
T.eq(lp.length,2,'two legal');
T.ok(lp.some(function(c){return c.s===0&&c.r===9;}),'suit match');
T.ok(lp.some(function(c){return c.s===1&&c.r===5;}),'rank match');
T.ok(!lp.some(function(c){return c.s===3&&c.r===7;}),'no match');
st.hands[0].push({s:3,r:8});
T.eq(L.legalPlays(st,0).length,3,'eight always legal');
T.throws(function(){L.playCard(st,0,{s:3,r:7});},'illegal throws');
T.throws(function(){L.playCard(st,0,{s:2,r:4});},'not in hand throws');
L.playCard(st,0,{s:1,r:5});
T.eq(st.suit,1,'suit follows card');
T.eq(st.turn,1,'turn passed');
"""),
(r"""ماندگاری خال انتخابی هشت""", r"""
var st=L.newGame(rng);
st.hands[0]=[{s:0,r:8},{s:3,r:2}];
st.hands[1]=[{s:2,r:4},{s:1,r:8},{s:1,r:4}];
st.discard=[{s:0,r:5}];st.suit=0;st.turn=0;st.over=false;st.passes=0;
L.playCard(st,0,{s:0,r:8},2);
T.eq(st.suit,2,'chosen suit persists');
T.eq(st.turn,1,'turn moved on');
var lp=L.legalPlays(st,1);
T.eq(lp.length,2,'suit or eight only');
T.ok(lp.some(function(c){return c.s===2&&c.r===4;}),'chosen suit playable');
T.ok(lp.some(function(c){return c.r===8;}),'eight playable');
T.ok(!lp.some(function(c){return c.s===1&&c.r===4;}),'rank match with 8 forbidden');
"""),
(r"""سقف برداشت سه کارت و گذر""", r"""
var st=L.newGame(rng);
st.hands[0]=[{s:0,r:2}];st.stock=[{s:0,r:3},{s:1,r:4}];
T.eq(L.drawUpTo(st,0,3),2,'stock cap');
T.eq(st.hands[0].length,3,'hand grew');
T.eq(st.stock.length,0,'stock empty');
st.stock=[{s:2,r:5},{s:2,r:6},{s:2,r:7},{s:2,r:8},{s:2,r:9}];
T.eq(L.drawUpTo(st,0,3),3,'three cap');
T.eq(st.stock.length,2,'two left');
var s2=L.newGame(rng);
s2.turn=1;s2.hands[1]=[{s:3,r:2}];s2.discard=[{s:0,r:5}];s2.suit=0;
s2.stock=[{s:1,r:6},{s:2,r:7}];s2.passes=0;s2.over=false;
L.aiTurn(s2);
T.eq(s2.hands[1].length,3,'AI drew 2');
T.eq(s2.turn,0,'AI passed back');
T.ok(!s2.over,'still going');
"""),
(r"""امتیاز کارت‌های دست""", r"""
T.eq(L.handPoints([{s:0,r:8},{s:1,r:1},{s:2,r:13},{s:3,r:7},{s:0,r:2}]),70,'mixed 70');
T.eq(L.handPoints([]),0,'empty 0');
T.eq(L.handPoints([{s:0,r:11},{s:1,r:12},{s:2,r:10}]),30,'faces 10 each');
T.eq(L.handPoints([{s:0,r:8},{s:1,r:8}]),100,'two eights 100');
"""),
(r"""امتیازدهی پایان دست و مسابقه""", r"""
var st=L.newGame(rng);
st.hands[0]=[{s:0,r:8}];
st.hands[1]=[{s:1,r:13},{s:2,r:5},{s:3,r:1}];
st.discard=[{s:0,r:5}];st.suit=0;st.turn=0;st.scores=[10,20];st.over=false;st.passes=0;st.round=0;
L.playCard(st,0,{s:0,r:8},1);
T.ok(L.isRoundOver(st),'round over');
T.eq(st.winner,0,'human wins round');
T.eq(st.pts,16,'opponent hand 16');
T.eq(st.scores[0],26,'score updated');
T.eq(L.isMatchOver(st),-1,'match continues');
st.scores[0]=200;
T.eq(L.isMatchOver(st),0,'match ends at 200');
"""),
(r"""مسابقهٔ کامل تا ۲۰۰ روی ۵ بذر""", r"""
function mb(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t^(t>>>14))>>>0;return t/4294967296;};}
function cnt(x){return x.hands[0].length+x.hands[1].length+x.stock.length+x.discard.length;}
var s;
for(s=0;s<5;s++){
 var m=mb(4242+s*13),cur=L.newGame(m),rounds=0,g;
 while(L.isMatchOver(cur)<0&&rounds<120){
  g=0;
  while(!L.isRoundOver(cur)&&g<400){L.aiTurn(cur);g++;T.eq(cnt(cur),52,'52 cards @r'+rounds+'t'+g);}
  T.ok(g<400,'round bounded');
  rounds++;
  if(L.isMatchOver(cur)>=0)break;
  cur=L.newGame(m,{scores:cur.scores,round:cur.round+1});
 }
 T.ok(L.isMatchOver(cur)>=0,'seed '+s+' reached 200 in '+rounds+' rounds');}
"""),
]

# ---------------------------------------------------------------- war
LOGIC_WAR = r"""var WOG_LOGIC=(function(){
function mkD(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<14;r++)d.push({s:s,r:r});return d;}
function shuf(a,f){var i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(f()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
function val(r){return r===1?14:r;}
function newGame(rng){var f=rng||Math.random,d=shuf(mkD(),f);
 return{a:d.slice(0,26),b:d.slice(26),rounds:0,over:false,winner:-1,last:null};}
function isOver(st){return st.a.length===0||st.b.length===0;}
function winner(st){if(!st.a.length&&!st.b.length)return st.winner>=0?st.winner:-1;if(!st.b.length)return 0;if(!st.a.length)return 1;return -1;}
function takePot(st,w,pot,f){shuf(pot,f);var arr=w===0?st.a:st.b,i;for(i=0;i<pot.length;i++)arr.push(pot[i]);}
function commit(st,p){var arr=p===0?st.a:st.b;if(!arr.length)return null;
 var down=Math.min(3,arr.length-1),t=[],k;
 for(k=0;k<down;k++)t.push(arr.shift());
 t.push(arr.shift());return t;}
function battle(st,rng){
 if(st.over)return null;
 var f=rng||Math.random,pot=[],ca,cb,va,vb,war=0,t,t2,w,lw;
 if(!st.a.length||!st.b.length){st.over=true;st.winner=st.a.length?0:1;return{winner:st.winner,war:0,pot:0};}
 ca=st.a.shift();cb=st.b.shift();pot.push(ca,cb);
 for(;;){
  va=val(ca.r);vb=val(cb.r);
  if(va!==vb){
   w=va>vb?0:1;
   takePot(st,w,pot,f);st.rounds++;
   st.last={winner:w,war:war,pot:pot.length,ca:ca,cb:cb};
   if(!st.a.length){st.over=true;st.winner=1;}else if(!st.b.length){st.over=true;st.winner=0;}
   return st.last;}
  war++;
  t=commit(st,0);
  if(t===null){takePot(st,1,pot,f);st.rounds++;st.over=true;st.winner=1;
   st.last={winner:1,war:war,pot:pot.length,ca:ca,cb:cb};return st.last;}
  pot=pot.concat(t);
  t2=commit(st,1);
  if(t2===null){takePot(st,0,pot,f);st.rounds++;st.over=true;st.winner=0;
   st.last={winner:0,war:war,pot:pot.length,ca:ca,cb:cb};return st.last;}
  pot=pot.concat(t2);
  ca=t[t.length-1];cb=t2[t2.length-1];
 }
}
return{newGame:newGame,battle:battle,isOver:isOver,winner:winner,val:val};
})();
"""

UI_WAR = r"""var st=null;
function deal(){st=L.newGame();render();}
function pileBox(lbl,n){
 var d=ce('div','pile','');
 d.appendChild(cardEl({s:0,r:2},false,'small'));
 d.appendChild(ce('div','cnt',lbl+': '+fa(n)));
 return d;
}
function render(){
 hud('کارت‌های تو: <b>'+fa(st.a.length)+'</b> · حریف: <b>'+fa(st.b.length)+'</b> · نبرد: <b>'+fa(st.rounds)+'</b>');
 var app=$('#app');app.innerHTML='';
 var p=ce('div','panel row','');
 p.appendChild(pileBox('تو',st.a.length));
 var mid=ce('div','wmid','');
 if(st.last){
  mid.appendChild(cardEl(st.last.ca,true,'small'));
  mid.appendChild(ce('span','vs','×'));
  mid.appendChild(cardEl(st.last.cb,true,'small'));
  mid.appendChild(ce('div','wres',st.last.war?('جنگ با '+fa(st.last.pot)+' کارت'):(st.last.winner===0?'بردم':'حریف برد')));
 }else mid.appendChild(ce('div','wres','نبرد را شروع کن'));
 p.appendChild(mid);
 p.appendChild(pileBox('حریف',st.b.length));
 app.appendChild(p);
 var r=ce('div','row','');
 var bb=ce('button','gold','نبرد!');
 bb.setAttribute('data-smoke','1');bb.onclick=fight;
 var ab=ce('button','','تا پایان، خودکار');ab.onclick=autoRun;
 var nb=ce('button','','بازی جدید');nb.onclick=deal;
 r.appendChild(bb);r.appendChild(ab);r.appendChild(nb);
 app.appendChild(r);
 $('#hint').textContent='رتبهٔ بالاتر هر دو کارت را میبرد (آس بیشترین)؛ برابر یعنی جنگ: سه کارت بسته و یک کارت رو؛ کسی که کارت نداشته باشد میبازد.';
}
function fight(){
 if(st.over)return;
 var res=L.battle(st);
 render();
 if(st.over)end();
 else if(res&&res.war)toast('جنگ! '+fa(res.pot)+' کارت روی میز');
}
function autoRun(){var g=0;while(!st.over&&g<5000){L.battle(st);g++;}render();end();}
function end(){
 var w=L.winner(st);
 ovl(w===0?'بردی!':'باختی','همهٔ ۵۲ کارت دست '+(w===0?'تو شد':'حریف شد'),'دوباره',deal);
}
deal();"""

CSS_WAR = CSS_BASE + r""".pile{display:flex;flex-direction:column;align-items:center;gap:4px}.vs{margin:0 8px;font-size:18px;color:#9fb0cf}.wres{width:100%;text-align:center;color:#d9a441;font-weight:700}"""

TESTS_WAR = [
(r"""مقایسهٔ رتبه با آسِ بالا""", r"""
T.eq(L.val(1),14,'A high');
T.eq(L.val(13),13,'K=13');
var st=L.newGame(rng);
st.a=[{s:0,r:1}];st.b=[{s:1,r:13}];st.over=false;st.winner=-1;st.rounds=0;st.last=null;
var res=L.battle(st,rng);
T.eq(res.winner,0,'A beats K');
T.ok(st.over,'game over');
T.eq(st.a.length,2,'winner holds pot');
T.eq(st.b.length,0,'loser empty');
var s2=L.newGame(rng);
s2.a=[{s:0,r:13},{s:0,r:2},{s:0,r:3}];s2.b=[{s:1,r:5},{s:1,r:6},{s:1,r:7}];
s2.over=false;s2.winner=-1;s2.rounds=0;s2.last=null;
res=L.battle(s2,rng);
T.eq(res.winner,0,'K beats 5');
T.ok(!s2.over,'battle continues');
T.eq(s2.a.length,4,'winner 4 cards');
T.eq(s2.a.length+s2.b.length,6,'6 conserved');
"""),
(r"""جنگ کامل (۳ بسته + ۱ رو)""", r"""
var st=L.newGame(rng);
st.a=[{s:0,r:7},{s:0,r:2},{s:0,r:3},{s:0,r:4}];
st.b=[{s:1,r:7},{s:1,r:5},{s:1,r:6},{s:1,r:8}];
st.over=false;st.winner=-1;st.rounds=0;st.last=null;
var res=L.battle(st,rng);
T.eq(res.war,1,'war happened');
T.eq(res.pot,8,'pot of 8');
T.eq(res.winner,1,'8 beats 4');
T.ok(st.over,'over');
T.eq(st.a.length,0,'A empty');
T.eq(st.b.length,8,'B holds 8');
"""),
(r"""کمبود کارت در میانهٔ جنگ""", r"""
var st=L.newGame(rng);
st.a=[{s:0,r:7}];st.b=[{s:1,r:7},{s:1,r:4},{s:1,r:5},{s:1,r:6}];
st.over=false;st.winner=-1;st.rounds=0;st.last=null;
var res=L.battle(st,rng);
T.eq(res.war,1,'war declared');
T.eq(res.winner,1,'A lacked cards, lost');
T.ok(st.over,'immediate end');
T.eq(st.a.length+st.b.length,5,'5 conserved');
T.eq(st.b.length,5,'B holds all');
"""),
(r"""حفظ ۵۲ کارت در هر نبرد""", r"""
var st=L.newGame(rng),n=0;
T.eq(st.a.length+st.b.length,52,'52 at start');
while(!L.isOver(st)&&n<5000){L.battle(st,rng);n++;T.eq(st.a.length+st.b.length,52,'52 @'+n);}
T.ok(L.isOver(st),'game ended');
var w=L.winner(st);
T.ok(w===0||w===1,'has winner');
T.eq((w===0?st.a:st.b).length,52,'winner holds 52');
"""),
(r"""۳۰ بازی بذردار زیر ۵۰۰۰ نبرد""", r"""
function mb(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t^(t>>>14))>>>0;return t/4294967296;};}
var s;
for(s=1;s<=30;s++){
 var m=mb(s),g=L.newGame(m),n=0;
 while(!L.isOver(g)&&n<5000){L.battle(g,m);n++;}
 T.ok(L.isOver(g),'over seed '+s);
 T.ok(n<5000,'bounded seed '+s+' at '+n);
 var w=L.winner(g);
 T.ok(w===0||w===1,'winner seed '+s);
 T.eq((w===0?g.a:g.b).length,52,'52 to winner seed '+s);}
"""),
(r"""قطعیت و ساختار""", r"""
function mb(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t^(t>>>14))>>>0;return t/4294967296;};}
var g1=L.newGame(mb(99)),g2=L.newGame(mb(99));
T.eq(JSON.stringify(g1),JSON.stringify(g2),'same seed same split');
T.eq(g1.a.length,26,'26 cards each');
T.eq(g1.b.length,26,'26');
T.eq(L.winner(g1),-1,'ongoing');
T.ok(!L.isOver(g1),'not over');
var seen={},i;
for(i=0;i<52;i++){var c=i<26?g1.a[i]:g1.b[i-26],k=c.s*13+c.r;T.ok(!seen[k],'unique '+k);seen[k]=1;}
var g3=L.newGame(mb(99)),g4=L.newGame(mb(99));
var r1=L.battle(g3,mb(99)),r2=L.battle(g4,mb(99));
T.eq(JSON.stringify(r1),JSON.stringify(r2),'battle deterministic');
T.eq(JSON.stringify(g3),JSON.stringify(g4),'state deterministic');
"""),
]

GAMES = [
 G(slug="tripeaks", title="سه قله", cat="cards", icon="⛰️", g1="#d9a441", g2="#3fb8af",
   desc="سولیتیر سه‌قله با ۲۸ کارت روی تپه‌ها و ۲۳ کارت دانته؛ هر بردار کمبو را بالا میبرد و امتیاز میسازد.",
   hint="کارت آزاد با رتبهٔ ±۱ یا هم ردهٔ کارتِ روی میز را بردار؛ شاه و آس به هم میرسند.",
   logic=LOGIC_TRI, ui=UI_TRI, css=CSS_TRI, engines=("common","card"), tests=TESTS_TRI, seed=12345),
 G(slug="clock", title="ساعت آس", cat="cards", icon="🕐", g1="#3fb8af", g2="#d9a441",
   desc="پاسور ساعت: ۱۳ پشتهٔ چهارکارته؛ هر کارت رو شده به پشتهٔ رتبهٔ خودش میرود؛ قبل از شاه چهارم همه را رو کن.",
   hint="کارت رو شده به پشتهٔ هم رده می‌رود؛ چهارمین شاه یعنی باخت مگر آخرین کارت باشد.",
   logic=LOGIC_CLK, ui=UI_CLK, css=CSS_CLK, engines=("common","card"), tests=TESTS_CLK, seed=12345),
 G(slug="crazy-eights", title="هشت دیوانه", cat="cards", icon="🎱", g1="#e26d5c", g2="#d9a441",
   desc="هشت دیوانه در برابر حریف هوشمند؛ هشت جانشین هر خالی است و مسابقه تا ۲۰۰ امتیاز ادامه دارد.",
   hint="با خال یا عدد یکسان بازی کن؛ هشت خال بعدی را تعیین میکند؛ اگر ساخ نیست تا ۳ کارت بکش.",
   logic=LOGIC_E8, ui=UI_E8, css=CSS_E8, engines=("common","card"), tests=TESTS_E8, seed=12345),
 G(slug="war", title="جنگ کارتی", cat="cards", icon="⚔️", g1="#67b98a", g2="#e26d5c",
   desc="جنگ کارتی کلاسیک با ۲۶ کارت هر طرف؛ برابری یعنی جنگ با سه کارت بسته و یک کارت رو.",
   hint="رتبهٔ بالاتر هر دو کارت را میبرد (آس بیشترین)؛ برابر یعنی جنگ؛ بی‌کارت یعنی باخت.",
   logic=LOGIC_WAR, ui=UI_WAR, css=CSS_WAR, engines=("common","card"), tests=TESTS_WAR, seed=12345),
]
