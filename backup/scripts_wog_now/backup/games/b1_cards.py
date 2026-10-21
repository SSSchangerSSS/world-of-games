# -*- coding: utf-8 -*-
# AG-B1 - batch of 3 card games: higher-lower, video-poker, thirty-one
# Cards are {s:0..3, r:1..13}; suits spade/heart/diamond/club (s:0=spade,1=heart,2=diamond,3=club); red = s 1|2. A=1 low, K=13 high.
from lib_mini import G

# ============================================================ 1) higher-lower
LOG_HL = r"""
function HLM(){
function deck52(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<=13;r++)d.push({s:s,r:r});return d}
function shuf(a,rng){var r=rng||Math.random,i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(r()*(i+1));t=a[i];a[i]=a[j];a[j]=t}return a}
function newGame(rng){var st={deck:shuf(deck52(),rng),cur:null,streak:0,best:0,points:0,drawn:1,reshuffles:0,over:false};st.cur=st.deck.pop();return st}
function streakPoints(n){return n}
function guess(st,dir,rng){
 if(st.over)return{correct:false,done:true,streak:st.streak,points:st.points};
 if(dir!=='higher'&&dir!=='lower')throw new Error('dir');
 if(st.deck.length===0){st.deck=shuf(deck52(),rng);st.reshuffles++}
 var nxt=st.deck.pop();st.drawn++;
 var ok=dir==='higher'?nxt.r>st.cur.r:nxt.r<st.cur.r;
 if(ok){st.streak++;st.points+=streakPoints(st.streak);st.cur=nxt;
  if(st.deck.length<=4){st.deck=shuf(deck52(),rng);st.reshuffles++}
  return{correct:true,done:false,streak:st.streak,points:st.points}}
 st.over=true;if(st.streak>st.best)st.best=st.streak;
 return{correct:false,done:true,streak:st.streak,points:st.points,best:st.best}
}
return{newGame:newGame,guess:guess,streakPoints:streakPoints,deck52:deck52,shuf:shuf}
}
var WOG_LOGIC=HLM();
"""

TESTS_HL = [
("امتیاز زنجیره", r"""
T.eq(L.streakPoints(1),1,'p1');T.eq(L.streakPoints(7),7,'p7');
var s=0,i;for(i=1;i<=5;i++)s+=L.streakPoints(i);T.eq(s,15,'sum 1..5');
"""),
("برابر در هر دو جهت باخت است", r"""
var st=L.newGame(rng);st.deck=[{s:1,r:7}];st.cur={s:0,r:7};
var g=L.guess(st,'higher',rng);T.eq(g.correct,false,'higher-equal-wrong');T.eq(g.done,true,'done');T.eq(st.over,true,'over');
var st2=L.newGame(rng);st2.deck=[{s:2,r:7}];st2.cur={s:0,r:7};
var g2=L.guess(st2,'lower',rng);T.eq(g2.correct,false,'lower-equal-wrong');T.eq(g2.done,true,'done2');T.eq(st2.over,true,'over2');
"""),
("حسابداری دسته و ری‌شافل", r"""
var st=L.newGame(rng);
st.deck=[{s:0,r:2},{s:0,r:3},{s:0,r:4},{s:0,r:5},{s:0,r:6}];st.cur={s:1,r:1};
var g1=L.guess(st,'higher',rng);T.ok(g1.correct===true,'g1 correct');
T.eq(st.reshuffles,1,'reshuffled at <=4');T.eq(st.deck.length,52,'fresh 52');T.eq(st.drawn,2,'drawn 2');T.eq(st.cur.r,6,'cur moved');
var g2=L.guess(st,'higher',rng);
T.eq(st.deck.length,51,'popped from new deck');T.eq(st.drawn,3,'drawn 3');T.eq(st.reshuffles,1,'no extra reshuffle');
"""),
("ریاضی زنجیره تا پایان دور", r"""
var st=L.newGame(rng);
st.deck=[{s:2,r:13},{s:2,r:13},{s:2,r:13},{s:2,r:13},{s:3,r:6},{s:3,r:5},{s:3,r:4},{s:3,r:3},{s:3,r:2}];
st.cur={s:0,r:1};
var i,g;for(i=0;i<5;i++){g=L.guess(st,'higher',rng);T.ok(g.correct===true,'step '+i)}
T.eq(st.streak,5,'streak 5');T.eq(st.points,15,'points 1+2+3+4+5');
st.deck=[{s:0,r:2}];
g=L.guess(st,'higher',rng);
T.eq(g.done,true,'run ended');T.eq(st.best,5,'best=5');T.eq(st.over,true,'over');T.eq(st.points,15,'points kept');
"""),
("نرخ برد در ۲۰۰۰ حدس", r"""
var wins=0,total=0,st=null,i,g;
for(i=0;i<2000;i++){if(!st||st.over)st=L.newGame(rng);g=L.guess(st,'higher',rng);total++;if(g.correct)wins++}
var wr=wins/total;T.ok(wr>0.35&&wr<0.65,'win-rate '+wr);
"""),
("بدون تکرار در هر دسته", r"""
var st=L.newGame(rng),i,g,seen=[];
function key(c){return c.s+':'+c.r}
seen=[key(st.cur)];
for(i=0;i<800;i++){
 var wasR=st.reshuffles;g=L.guess(st,'higher',rng);
 if(g.done){st=L.newGame(rng);seen=[key(st.cur)];continue}
 if(st.reshuffles!==wasR){seen=[key(st.cur)]}
 else{T.ok(seen.indexOf(key(st.cur))<0,'duplicate '+key(st.cur))}
 seen.push(key(st.cur));
 T.ok(st.deck.length>0,'deck never empty');
}
"""),
]

UI_HL = r"""
var S=null;
function getBest(){var v=parseInt(store.get('wog-higher-lower-best')||'0',10);return v>0?v:0}
function start(){S=L.newGame();S.msg='اولین حدس را بزن!';paint()}
function paint(){
 hud('امتیاز: <b>'+fa(S.points)+'</b> · زنجیره: <b>'+fa(S.streak)+'</b> · رکورد: <b>'+fa(getBest())+'</b> · کارت مانده: '+fa(S.deck.length));
 var app=$('#app');app.innerHTML='';
 var w=ce('div','hl');
 w.appendChild(cardEl(S.cur,true,'small'));
 w.appendChild(ce('div','hl-lab','کارت فعلی: '+suitOf(S.cur)+' '+rankFa(S.cur.r)));
 var row=ce('div','hl-row');
 var b1=ce('button','btn gold','بالاتر');b1.setAttribute('data-smoke','higher');
 b1.onclick=function(){go('higher')};
 var b2=ce('button','btn turq','پایین‌تر');b2.setAttribute('data-smoke','lower');
 b2.onclick=function(){go('lower')};
 row.appendChild(b1);row.appendChild(b2);
 w.appendChild(row);
 w.appendChild(ce('div','hl-msg',S.msg||''));
 app.appendChild(w);
}
function go(d){
 var g=L.guess(S,d);
 if(g.done){
  if(S.streak>getBest())store.set('wog-higher-lower-best',String(S.streak));
  paint();
  ovl('دور تمام شد!','زنجیره: '+fa(S.streak)+' — امتیاز: '+fa(S.points),'بازی دوباره',function(){start()});
 }else{S.msg='آفرین! زنجیره: '+fa(S.streak);paint()}
}
$('#hint').textContent='کارت بعدی باید اکیداً بالاتر یا پایین‌تر باشد — برابر یعنی باخت!';
start();
"""

CSS_HL = r"""
.hl{display:flex;flex-direction:column;align-items:center;gap:14px;padding:16px 8px}
.hl-row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.btn{min-width:110px;min-height:46px;border:0;border-radius:12px;font-size:17px;font-family:inherit;cursor:pointer;touch-action:manipulation;padding:10px 18px}
.gold{background:#d9a441;color:#1a2438;font-weight:bold}
.turq{background:#3fb8af;color:#0e1626;font-weight:bold}
.hl-lab{color:#d9a441;font-size:17px}
.hl-msg{color:#67b98a;min-height:22px;font-size:15px;text-align:center}
"""

# ============================================================ 2) video-poker
LOG_VP = r"""
function VPM(){
function deck52(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<=13;r++)d.push({s:s,r:r});return d}
function shuf(a,rng){var r=rng||Math.random,i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(r()*(i+1));t=a[i];a[i]=a[j];a[j]=t}return a}
var PAY={royal:250,sf:50,'4k':25,fh:9,flush:6,straight:4,'3k':3,'2p':2,job:1,none:0};
function payout(cat){return PAY[cat]||0}
function evaluate5(cs){
 var s0=cs[0].s,flush=true,cnt={},i,k;
 for(i=0;i<5;i++){if(cs[i].s!==s0)flush=false;cnt[cs[i].r]=(cnt[cs[i].r]||0)+1}
 var ranks=[];for(k in cnt)ranks.push(+k);ranks.sort(function(a,b){return a-b});
 var c4=false,c3=false,pr=0,hp=false;
 for(k in cnt){var v=cnt[k];if(v===4)c4=true;else if(v===3)c3=true;else if(v===2){pr++;if(+k>=11)hp=true}}
 var st=false,br=false,n=ranks.length;
 if(n===5){
  if(ranks[4]-ranks[0]===4)st=true;
  else if(ranks[0]===1&&ranks[1]===10&&ranks[2]===11&&ranks[3]===12&&ranks[4]===13){st=true;br=true}
 }
 if(flush&&st)return br?'royal':'sf';
 if(c4)return'4k';
 if(c3&&pr===1)return'fh';
 if(flush)return'flush';
 if(st)return'straight';
 if(c3)return'3k';
 if(pr===2)return'2p';
 if(pr===1&&hp)return'job';
 return'none';
}
function newGame(rng){return{deck:shuf(deck52(),rng),hand:[],holds:[false,false,false,false,false],credits:100,bet:5,phase:'deal',cat:null,net:0}}
function startDeal(st,bet,rng){
 if(st.phase!=='deal')throw new Error('phase');
 if(bet===undefined||bet===null)bet=st.bet;
 if(bet!==5&&bet!==10&&bet!==25)throw new Error('bet');
 if(st.credits<bet)throw new Error('credits');
 st.bet=bet;st.credits-=bet;st.cat=null;st.net=-bet;
 if(st.deck.length<10)st.deck=shuf(deck52(),rng);
 st.hand=[];var i;for(i=0;i<5;i++)st.hand.push(st.deck.pop());
 st.holds=[false,false,false,false,false];st.phase='draw';
 return{dealt:true,hand:st.hand.slice(),phase:'draw',credits:st.credits}
}
function finishRound(st,holds){
 if(st.phase!=='draw')throw new Error('phase');
 var hs=holds||[0,0,0,0,0],i;
 for(i=0;i<5;i++){if(!hs[i])st.hand[i]=st.deck.pop();st.holds[i]=!!hs[i]}
 st.cat=evaluate5(st.hand);
 var win=payout(st.cat)*st.bet;st.credits+=win;st.net=win-st.bet;
 st.phase=st.credits>=5?'deal':'over';
 return{cat:st.cat,net:st.net,win:win,hand:st.hand.slice(),credits:st.credits,phase:st.phase}
}
function playRound(st,holds,bet,rng){
 if(st.phase==='deal')return startDeal(st,bet,rng);
 return finishRound(st,holds);
}
function bestHolds(h){
 var cat=evaluate5(h),i,j,s;
 var out=[false,false,false,false,false];
 function mark(ix){var m;for(m=0;m<ix.length;m++)out[ix[m]]=true}
 if(cat==='royal'||cat==='sf'||cat==='4k'||cat==='fh'||cat==='flush'||cat==='straight')return[true,true,true,true,true];
 var byRank={};for(i=0;i<5;i++){var r=h[i].r;(byRank[r]=byRank[r]||[]).push(i)}
 var trip=null,pairs=[];
 for(var rr in byRank){var g=byRank[rr];if(g.length===3)trip=+rr;else if(g.length===2)pairs.push(+rr)}
 if(trip!==null){mark(byRank[trip]);return out}
 if(pairs.length===2){mark(byRank[pairs[0]]);mark(byRank[pairs[1]]);return out}
 for(s=0;s<4;s++){var ix=[],hi=0;
  for(i=0;i<5;i++)if(h[i].s===s)ix.push(i);
  if(ix.length===4){for(j=0;j<4;j++){var rv=h[ix[j]].r;if(rv===1||rv>=10)hi++}
   if(hi===4){mark(ix);return out}}}
 if(pairs.length===1&&pairs[0]>=11){mark(byRank[pairs[0]]);return out}
 for(s=0;s<4;s++){var ix2=[];for(i=0;i<5;i++)if(h[i].s===s)ix2.push(i);
  if(ix2.length===4){mark(ix2);return out}}
 if(pairs.length===1){mark(byRank[pairs[0]]);return out}
 var his=[];for(i=0;i<5;i++)if(h[i].r>=11)his.push(i);
 if(his.length>0){mark(his);return out}
 return out;
}
return{evaluate5:evaluate5,payout:payout,playRound:playRound,newGame:newGame,bestHolds:bestHolds,startDeal:startDeal,deck52:deck52,shuf:shuf}
}
var WOG_LOGIC=VPM();
"""

TESTS_VP = [
("ارزیابی دست‌های پوکری ۱", r"""
function C(s,r){return{s:s,r:r}}
T.eq(L.evaluate5([C(0,1),C(0,10),C(0,11),C(0,12),C(0,13)]),'royal','royal');
T.eq(L.evaluate5([C(1,1),C(1,2),C(1,3),C(1,4),C(1,5)]),'sf','wheel-sf A2345 suited');
T.eq(L.evaluate5([C(0,8),C(0,9),C(0,10),C(0,11),C(0,12)]),'sf','sf not royal');
T.eq(L.evaluate5([C(1,1),C(0,2),C(2,3),C(3,4),C(1,5)]),'straight','A2345 mixed suits');
T.eq(L.evaluate5([C(0,1),C(1,10),C(2,11),C(3,12),C(1,13)]),'straight','TJQKA mixed suits');
T.eq(L.evaluate5([C(3,2),C(3,5),C(3,7),C(3,9),C(3,13)]),'flush','flush');
"""),
("ارزیابی دست‌های پوکری ۲", r"""
function C(s,r){return{s:s,r:r}}
T.eq(L.evaluate5([C(0,7),C(1,7),C(2,7),C(3,7),C(0,2)]),'4k','four of a kind');
T.eq(L.evaluate5([C(0,5),C(1,5),C(2,9),C(3,9),C(1,9)]),'fh','full house');
T.eq(L.evaluate5([C(0,6),C(1,6),C(2,6),C(3,2),C(1,9)]),'3k','three of a kind');
T.eq(L.evaluate5([C(0,4),C(1,4),C(2,8),C(3,8),C(0,12)]),'2p','two pair');
T.eq(L.evaluate5([C(0,11),C(1,11),C(2,2),C(3,5),C(1,9)]),'job','pair of J pays');
T.eq(L.evaluate5([C(0,10),C(1,10),C(2,2),C(3,5),C(1,9)]),'none','pair of T does not pay');
"""),
("جدول پرداخت و سود خالص", r"""
T.eq(L.payout('royal'),250,'royal');T.eq(L.payout('sf'),50,'sf');T.eq(L.payout('4k'),25,'4k');
T.eq(L.payout('fh'),9,'fh');T.eq(L.payout('flush'),6,'flush');T.eq(L.payout('straight'),4,'straight');
T.eq(L.payout('3k'),3,'3k');T.eq(L.payout('2p'),2,'2p');T.eq(L.payout('job'),1,'job');T.eq(L.payout('none'),0,'none');
function C(s,r){return{s:s,r:r}}
var st=L.newGame(rng);
st.hand=[C(0,5),C(1,5),C(2,9),C(3,9),C(1,9)];st.bet=10;st.phase='draw';st.credits=90;
var r=L.playRound(st,[true,true,true,true,true],10);
T.eq(r.cat,'fh','cat');T.eq(r.net,80,'net=90-10');T.eq(st.credits,180,'credits 90+90');
"""),
("بدون تکرار و حسابداری در ۲۰۰ دست", r"""
var st=L.newGame(rng),i,k,r,pre;
function uniq(h){var a,b;for(a=0;a<5;a++)for(b=a+1;b<5;b++)if(h[a].s===h[b].s&&h[a].r===h[b].r)return false;return true}
for(i=0;i<200;i++){
 if(st.phase==='over')st=L.newGame(rng);
 pre=st.credits;
 L.playRound(st,null,5);
 var holds=[];for(k=0;k<5;k++)holds.push(rng()<0.5);
 r=L.playRound(st,holds,5);
 T.ok(uniq(r.hand),'no dup in deal+draw');
 T.eq(st.credits,pre+r.net,'credits accounting');
}
"""),
("RTP شبیه‌سازی ۳۰۰۰ دست", r"""
var st=L.newGame(rng),i,totalNet=0,betSum=0;
for(i=0;i<3000;i++){
 if(st.phase==='over')st=L.newGame(rng);
 var d=L.playRound(st,null,5);
 var h=L.bestHolds(d.hand);
 var r=L.playRound(st,h,5);
 totalNet+=r.net;betSum+=5;
}
var rtp=1+totalNet/betSum;
T.ok(rtp>0.6&&rtp<1.6,'RTP '+rtp);
"""),
("فازها و خطاها", r"""
var st=L.newGame(rng);
var d=L.playRound(st,null,5);
T.eq(d.dealt,true,'dealt');T.eq(d.hand.length,5,'5 cards');T.eq(st.phase,'draw','phase draw');T.eq(st.credits,95,'95 after bet 5');
T.throws(function(){L.playRound(L.newGame(rng),null,7)},'bad bet rejected');
var st2=L.newGame(rng);st2.credits=3;
T.throws(function(){L.playRound(st2,null,5)},'insufficient credits');
var st3=L.newGame(rng);L.playRound(st3,null,5);
T.throws(function(){L.startDeal(st3,5)},'double deal rejected');
var st4=L.newGame(rng);L.playRound(st4,null,25);
T.eq(st4.credits,75,'bet 25 accepted');
"""),
]

UI_VP = r"""
var S=L.newGame(),bet=5,holds=[false,false,false,false,false],shown=false,msg='شرط را انتخاب کن و پخش بزن.';
var CATFA={royal:'رویال فلاش',sf:'استریت فلاش','4k':'چهارلایی',fh:'خانهٔ کامل',flush:'فلاش',straight:'استریت','3k':'سه‌تایی','2p':'دو جفت',job:'جفت سرباز یا بهتر',none:'دستی نیامد'};
function getBest(){var v=parseInt(store.get('wog-video-poker-best')||'0',10);return v>0?v:0}
function paint(){
 hud('اعتبار: <b>'+fa(S.credits)+'</b> · رکورد اعتبار: <b>'+fa(getBest())+'</b> · شرط: '+fa(bet));
 var app=$('#app');app.innerHTML='';
 var w=ce('div','vp');
 var row=ce('div','vp-row');
 var i;
 if(S.hand.length===5&&shown){
  for(i=0;i<5;i++){(function(idx){
   var cell=ce('div','vp-cell');
   var el=cardEl(S.hand[idx],true,'small');
   if(S.phase==='draw'){
    if(holds[idx])el.className+=' sel';
    el.onclick=function(){holds[idx]=!holds[idx];paint()};
   }
   cell.appendChild(el);
   if(S.phase==='draw'&&holds[idx])cell.appendChild(ce('div','vp-hold','نگه'));
   row.appendChild(cell)})(i)}
 }else{
  for(i=0;i<5;i++)row.appendChild(ce('div','wcard back',''));
 }
 w.appendChild(row);
 w.appendChild(ce('div','vp-msg',msg));
 var br=ce('div','vp-row');
 if(S.phase==='deal'){
  [5,10,25].forEach(function(b){
   var bb=ce('button','btn '+(b===bet?'gold':'ghost'),'شرط '+fa(b));
   bb.onclick=function(){bet=b;paint()};
   br.appendChild(bb)});
  var db=ce('button','btn gold big','پخش');db.setAttribute('data-smoke','deal');
  db.onclick=function(){
   if(S.credits<bet){toast('اعتبار کافی نیست!');return}
   L.playRound(S,null,bet);
   holds=[false,false,false,false,false];shown=true;
   msg='روی کارت‌هایی که می‌خواهی نگه داری بزن.';paint()};
  br.appendChild(db);
 }else if(S.phase==='draw'){
  var hb=ce('button','btn gold big','تعویض');hb.setAttribute('data-smoke','draw');
  hb.onclick=function(){
   var r=L.playRound(S,holds,0);
   if(S.credits>getBest())store.set('wog-video-poker-best',String(S.credits));
   msg=CATFA[r.cat]+' — '+(r.net>0?'برد: +'+fa(r.net):(r.net===0?'سر به سر':'باخت: '+fa(r.net)));
   paint();
   if(S.phase==='over')setTimeout(function(){ovl('اعتبار تمام شد!','اعتبار نهایی: '+fa(S.credits),'شروع دوباره',function(){S=L.newGame();bet=5;shown=false;msg='شرط را انتخاب کن و پخش بزن.';paint()})},150);
  };
  br.appendChild(hb);
 }
 w.appendChild(br);
 app.appendChild(w);
}
$('#hint').textContent='جفت سرباز (J) یا بالاتر برنده است؛ روی کارت بزن تا نگه داشته شود، بعد تعویض بزن.';
paint();
"""

CSS_VP = r"""
.vp{display:flex;flex-direction:column;align-items:center;gap:12px;padding:12px}
.vp-row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.vp-cell{display:flex;flex-direction:column;align-items:center;gap:4px}
.vp-cell .wcard{cursor:pointer}
.vp-hold{color:#d9a441;font-size:13px;font-weight:bold}
.vp-msg{color:#67b98a;min-height:22px;font-size:16px;text-align:center}
.btn{min-width:104px;min-height:46px;border:0;border-radius:12px;font-size:16px;font-family:inherit;cursor:pointer;touch-action:manipulation;padding:10px 16px}
.btn.big{min-width:140px}
.gold{background:#d9a441;color:#1a2438;font-weight:bold}
.turq{background:#3fb8af;color:#0e1626;font-weight:bold}
.ghost{background:#24365c;color:#cdd8ee}
"""

# ============================================================ 3) thirty-one
LOG_T31 = r"""
function T31M(){
function deck52(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<=13;r++)d.push({s:s,r:r});return d}
function shuf(a,rng){var r=rng||Math.random,i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(r()*(i+1));t=a[i];a[i]=a[j];a[j]=t}return a}
function cardVal(c){return c.r===1?11:(c.r>=11?10:c.r)}
function handValue(cards){var sum={},i,m=0,s;for(i=0;i<cards.length;i++){var c=cards[i];sum[c.s]=(sum[c.s]||0)+cardVal(c)}for(s in sum)if(sum[s]>m)m=sum[s];return m}
function activeList(st){var a=[],i;for(i=0;i<st.players.length;i++)if(st.players[i].lives>0)a.push(i);return a}
function nextActiveAfter(st,pi){var n=st.players.length,i,j;for(i=1;i<=n;i++){j=(pi+i+n)%n;if(st.players[j].lives>0)return j}return null}
function restock(st,rng){if(st.deck.length===0&&st.discard.length>1){var top=st.discard.pop();while(st.discard.length>0)st.deck.push(st.discard.pop());shuf(st.deck,rng);st.discard.push(top)}}
function startRound(st,rng){
 st.deck=shuf(deck52(),rng);st.discard=[];st.knocked=null;st.mustPlay=[];st.lastDiscarder=null;st.phase='play';
 var act=activeList(st),i;
 for(i=0;i<st.players.length;i++){st.players[i].hand=act.indexOf(i)>=0?[st.deck.pop(),st.deck.pop(),st.deck.pop()]:[]}
 st.discard.push(st.deck.pop());
 var nx=nextActiveAfter(st,st.turnIdx);
 st.turnIdx=(nx===null?act[0]:nx);
}
function newGame(rng){
 var st={players:[{lives:3,hand:[]},{lives:3,hand:[]},{lives:3,hand:[]}],deck:[],discard:[],turnIdx:-1,knocked:null,mustPlay:[],lastDiscarder:null,phase:'play',winner:null,round:0,lastShowdown:null};
 startRound(st,rng);st.round=1;return st;
}
function turn(st,pi,act,rng){
 if(st.phase!=='play')throw new Error('phase');
 if(pi!==st.turnIdx)throw new Error('turn');
 if(st.knocked!==null&&(st.mustPlay.length===0||st.mustPlay[0]!==pi))throw new Error('postknock');
 var p=st.players[pi];
 if(act.type==='draw'){
  if(p.hand.length!==3)throw new Error('hand3');
  restock(st,rng);
  if(st.deck.length===0)throw new Error('deck');
  p.hand.push(st.deck.pop());
 }else if(act.type==='take'){
  if(p.hand.length!==3)throw new Error('hand3');
  if(st.discard.length===0)throw new Error('discard');
  p.hand.push(st.discard.pop());
 }else if(act.type==='discard'){
  if(p.hand.length!==4)throw new Error('hand4');
  var ci=act.idx;
  if(ci!==0&&ci!==1&&ci!==2&&ci!==3)throw new Error('idx');
  var c=p.hand.splice(ci,1)[0];
  st.discard.push(c);st.lastDiscarder=pi;
  if(st.knocked!==null){
   st.mustPlay.shift();
   if(st.mustPlay.length===0){showdown(st,rng);return st}
   st.turnIdx=st.mustPlay[0];
  }else{
   st.turnIdx=nextActiveAfter(st,pi);
  }
 }else{throw new Error('action')}
 return st;
}
function knock(st,pi){
 if(st.phase!=='play')throw new Error('phase');
 if(st.knocked!==null)throw new Error('knocked');
 if(st.lastDiscarder!==pi)throw new Error('after-discard');
 if(st.players[pi].lives<=0)throw new Error('dead');
 st.knocked=pi;st.mustPlay=[];
 var n=st.players.length,i,j;
 for(i=1;i<=n;i++){j=(pi+i+n)%n;if(j!==pi&&st.players[j].lives>0)st.mustPlay.push(j)}
 st.turnIdx=st.mustPlay[0];
 return st;
}
function showdown(st,rng){
 var act=activeList(st),i,vals={},min=1e9;
 for(i=0;i<act.length;i++){vals[act[i]]=handValue(st.players[act[i]].hand);if(vals[act[i]]<min)min=vals[act[i]]}
 var losers=[];
 for(i=0;i<act.length;i++)if(vals[act[i]]===min)losers.push(act[i]);
 for(i=0;i<losers.length;i++)st.players[losers[i]].lives--;
 st.lastShowdown={vals:vals,losers:losers.slice()};
 var remain=activeList(st);
 if(remain.length<=1){
  st.phase='over';st.winner=remain.length===1?remain[0]:null;
  for(i=0;i<st.players.length;i++)st.players[i].hand=[];
 }else{startRound(st,rng);st.round++}
 return losers.slice();
}
function lowestIdx(hand){var bi=0,bv=99,i;for(i=0;i<hand.length;i++){var v=cardVal(hand[i]);if(v<bv){bv=v;bi=i}}return bi}
function projValue(hand,c){var h2=hand.concat([c]);h2.splice(lowestIdx(h2),1);return handValue(h2)}
function aiMove(st,pi,rng){
 var p=st.players[pi];
 if(p.hand.length===4)return{type:'discard',idx:lowestIdx(p.hand)};
 if(p.hand.length!==3)throw new Error('aihand');
 if(st.knocked===null&&st.discard.length>0){
  var top=st.discard[st.discard.length-1];
  if(projValue(p.hand,top)>handValue(p.hand))return{type:'take'};
 }
 return{type:'draw'};
}
function aiKnock(st,pi){return handValue(st.players[pi].hand)>=27}
function aiGame(rng){
 var st=newGame(rng),guard=0;
 while(st.phase!=='over'&&guard++<8000){
  var pi=st.turnIdx;
  turn(st,pi,aiMove(st,pi,rng),rng);
  if(st.phase==='play'&&st.turnIdx===pi&&st.players[pi].hand.length===4){
   turn(st,pi,aiMove(st,pi,rng),rng);
   if(st.phase==='play'&&st.knocked===null&&st.lastDiscarder===pi&&aiKnock(st,pi))knock(st,pi);
  }
 }
 return st;
}
return{handValue:handValue,cardVal:cardVal,newGame:newGame,turn:turn,knock:knock,showdown:showdown,aiMove:aiMove,aiKnock:aiKnock,aiGame:aiGame,activeList:activeList}
}
var WOG_LOGIC=T31M();
"""

TESTS_T31 = [
("ارزش دست", r"""
T.eq(L.handValue([{s:0,r:1},{s:0,r:10},{s:0,r:9}]),30,'single suit run');
T.eq(L.handValue([{s:0,r:1},{s:1,r:10},{s:2,r:10}]),11,'best single suit only');
T.eq(L.handValue([{s:3,r:13},{s:3,r:7},{s:3,r:6}]),23,'face=10');
T.eq(L.handValue([{s:2,r:1},{s:2,r:2},{s:2,r:3}]),16,'ace=11');
T.eq(L.handValue([{s:0,r:11},{s:1,r:12},{s:2,r:13},{s:0,r:1}]),21,'four cards, mixed');
"""),
("جریان کوبیدن دقیق", r"""
var st=L.newGame(rng);
st.players[0].hand=[{s:0,r:1},{s:0,r:10},{s:0,r:9}];
st.players[1].hand=[{s:1,r:5},{s:1,r:6},{s:1,r:7}];
st.players[2].hand=[{s:2,r:2},{s:2,r:3},{s:2,r:4}];
st.deck=[{s:3,r:5},{s:1,r:8}];st.discard=[{s:0,r:2}];st.turnIdx=0;st.lastDiscarder=null;st.knocked=null;st.mustPlay=[];
L.turn(st,0,{type:'draw'},rng);
L.turn(st,0,{type:'discard',idx:3},rng);
L.knock(st,0);
T.eq(st.knocked,0,'knocker recorded');T.eq(st.turnIdx,1,'next is p1');T.eq(st.mustPlay.length,2,'two final turns');
L.turn(st,1,{type:'draw'},rng);
L.turn(st,1,{type:'discard',idx:3},rng);
T.eq(st.turnIdx,2,'then p2');
L.turn(st,2,{type:'take'},rng);
L.turn(st,2,{type:'discard',idx:3},rng);
T.eq(st.lastShowdown.losers.length,1,'one loser');T.eq(st.lastShowdown.losers[0],2,'p2 loses');
T.eq(st.lastShowdown.vals[0],30,'v0');T.eq(st.lastShowdown.vals[1],18,'v1');T.eq(st.lastShowdown.vals[2],9,'v2');
T.eq(st.players[2].lives,2,'p2 lost a life');T.eq(st.players[0].lives,3,'p0 safe');T.eq(st.players[1].lives,3,'p1 safe');
T.eq(st.phase,'play','next round started');T.eq(st.round,2,'round 2');T.eq(st.knocked,null,'knock reset');
T.throws(function(){L.knock(st,1)},'knock only right after own discard');
"""),
("تساوی: همه بازنده‌اند", r"""
var st=L.newGame(rng);
st.players[0].hand=[{s:0,r:7},{s:0,r:8},{s:1,r:3}];
st.players[1].hand=[{s:1,r:9},{s:1,r:6},{s:2,r:13}];
st.players[2].hand=[{s:2,r:10},{s:2,r:11},{s:2,r:9}];
var ls=L.showdown(st,rng);
T.eq(ls.length,2,'two tied losers');T.ok(ls.indexOf(0)>=0&&ls.indexOf(1)>=0,'players 0 and 1');
T.eq(st.players[0].lives,2,'p0 life lost');T.eq(st.players[1].lives,2,'p1 life lost');T.eq(st.players[2].lives,3,'p2 safe');
"""),
("حذف بازیکن و ادامه", r"""
var st=L.newGame(rng);
st.players[0].lives=1;
st.players[0].hand=[{s:0,r:2},{s:0,r:3},{s:0,r:4}];
st.players[1].hand=[{s:1,r:10},{s:1,r:9},{s:1,r:8}];
st.players[2].hand=[{s:2,r:10},{s:2,r:9},{s:2,r:8}];
var ls=L.showdown(st,rng);
T.eq(ls[0],0,'p0 loses');T.eq(st.players[0].lives,0,'p0 eliminated');
T.eq(st.phase,'play','game continues');
T.eq(st.players[0].hand.length,0,'dead hand cleared');
T.eq(st.players[1].hand.length,3,'p1 dealt');T.eq(st.players[2].hand.length,3,'p2 dealt');
T.ok(st.turnIdx===1||st.turnIdx===2,'turn skips eliminated');
"""),
("تصمیم‌های AI", r"""
var st=L.newGame(rng);
st.players[1].hand=[{s:0,r:1},{s:1,r:5},{s:2,r:9}];
st.discard=[{s:0,r:3},{s:2,r:12}];
var a=L.aiMove(st,1,rng);
T.eq(a.type,'take','takes discard when it improves');
st.players[1].hand.push({s:2,r:12});
var a2=L.aiMove(st,1,rng);
T.eq(a2.type,'discard','discards when holding 4');T.eq(a2.idx,1,'discards lowest card');
var st2=L.newGame(rng);
st2.players[0].hand=[{s:0,r:1},{s:0,r:12},{s:0,r:6}];
T.eq(L.handValue(st2.players[0].hand),27,'27 exactly');
T.eq(L.aiKnock(st2,0),true,'knocks at 27');
st2.players[0].hand=[{s:0,r:1},{s:0,r:12},{s:0,r:5}];
T.eq(L.aiKnock(st2,0),false,'no knock at 26');
"""),
("بازی کامل تا بازماندهٔ آخر", r"""
var st=L.aiGame(rng);
T.eq(st.phase,'over','game ended');
var alive=0,win=-1,i;
for(i=0;i<3;i++)if(st.players[i].lives>0){alive++;win=i}
T.eq(alive,1,'exactly one survivor');
T.eq(st.winner,win,'winner is the survivor');
T.ok(st.round>=1,'rounds were played');
"""),
]

UI_T31 = r"""
var S=null,msg='',tick=0,lastRoundShown=0,ended=false;
function getWins(){var v=parseInt(store.get('wog-thirty-one-wins')||'0',10);return v>0?v:0}
function dots(n){var s='',i;for(i=0;i<3;i++)s+=(i<n?'●':'○');return s}
function start(){S=L.newGame();msg='نوبت شماست.';lastRoundShown=0;ended=false;paint()}
function schedule(){tick++;var t=tick;setTimeout(function(){if(t===tick)aiStep()},850)}
function paint(){
 if(S.lastShowdown&&lastRoundShown!==S.round&&S.phase==='play'){
  lastRoundShown=S.round;
  msg='بازنده(های) دور قبل: '+S.lastShowdown.losers.map(function(x){return fa(x+1)}).join(' و ')+' — یک جان کم شد';
 }
 hud('جان شما: '+dots(S.players[0].lives)+' · بردها: '+fa(getWins())+' · دور: '+fa(S.round)+(S.knocked!==null?' · کوبیده شده':''));
 var app=$('#app');app.innerHTML='';
 var w=ce('div','t31');
 var top=ce('div','t31-top');
 top.appendChild(ce('div','t31-pile','دسته ('+fa(S.deck.length)+')'));
 top.appendChild(ce('div','t31-pile gold','دورریز: '+(S.discard.length?suitOf(S.discard[S.discard.length-1])+rankFa(S.discard[S.discard.length-1].r):'—')));
 w.appendChild(top);
 var ops=ce('div','t31-ops');
 var i;
 for(i=1;i<3;i++){
  ops.appendChild(ce('div','t31-op'+(S.turnIdx===i&&S.phase==='play'?' on':''),'بازیکن '+fa(i+1)+' — جان: '+dots(S.players[i].lives)+' — '+fa(S.players[i].hand.length)+' کارت'+(S.knocked===i?' — کوبید!':'')));
 }
 w.appendChild(ops);
 var me=ce('div','t31-me'+(S.turnIdx===0&&S.phase==='play'?' on':''));
 var h0=S.players[0].hand;
 var hv=L.handValue(h0);
 me.appendChild(ce('div','t31-meh','دست شما — بهترین خال: <b>'+fa(hv)+'</b>'+(S.players[0].lives===0?' — حذف شدی، تماشاگر':'')));
 var hr=ce('div','t31-hand');
 for(i=0;i<h0.length;i++){(function(idx){
  var el=cardEl(h0[idx],true,'small');
  if(S.phase==='play'&&S.turnIdx===0&&h0.length===4){el.className+=' pick';el.onclick=function(){humDiscard(idx)}}
  hr.appendChild(el)})(i)}
 me.appendChild(hr);
 w.appendChild(me);
 var ab=ce('div','t31-acts');
 if(S.phase==='play'&&S.turnIdx===0&&h0.length===3){
  var b1=ce('button','btn gold','از دسته بکش');b1.setAttribute('data-smoke','draw');
  b1.onclick=function(){L.turn(S,0,{type:'draw'});msg='یکی از کارت‌هایت را دور بریز.';paint()};
  var b2=ce('button','btn turq','برداشتن دورریز');b2.setAttribute('data-smoke','take');
  b2.onclick=function(){L.turn(S,0,{type:'take'});msg='دورریز را برداشتی؛ یکی را دور بریز.';paint()};
  ab.appendChild(b1);ab.appendChild(b2);
 }else if(S.phase==='play'&&S.knocked===null&&S.lastDiscarder===0&&S.turnIdx!==0){
  var k1=ce('button','btn gold','کوبیدن! ('+fa(hv)+')');k1.setAttribute('data-smoke','knock');
  k1.onclick=function(){L.knock(S,0);msg='کوبیدی! رقیب‌ها فقط یک نوبت دارند.';paint();schedule()};
  var k2=ce('button','btn turq','ادامه بدون کوبیدن');
  k2.onclick=function(){msg='';paint();schedule()};
  ab.appendChild(k1);ab.appendChild(k2);
 }
 w.appendChild(ab);
 w.appendChild(ce('div','t31-msg',msg));
 app.appendChild(w);
 $('#hint').textContent='بهترین تک‌خال را بساز (آ=۱۱، تصویری=۱۰). بعد از دورریز می‌توانی بکوبی؛ ضعیف‌ترین دست یک جان از دست می‌دهد.';
 if(S.phase==='over'&&!ended){
  ended=true;
  if(S.winner===0)store.set('wog-thirty-one-wins',String(getWins()+1));
  var wt=S.winner===null?'همه حذف شدند — مساوی!':(S.winner===0?'بردی! آخرین بازمانده تویی':'بازیکن '+fa(S.winner+1)+' برنده شد');
  ovl('پایان بازی',wt,'بازی دوباره',function(){start()});
 }
}
function humDiscard(idx){
 L.turn(S,0,{type:'discard',idx});
 paint();
 if(S.phase==='play'&&S.turnIdx!==0)schedule();
}
function aiStep(){
 if(S.phase!=='play')return;
 var pi=S.turnIdx;
 if(pi!==0){
  var a=L.aiMove(S,pi);
  L.turn(S,pi,a);
  if(S.phase==='play'&&S.turnIdx===pi&&S.players[pi].hand.length===4){
   var a2=L.aiMove(S,pi);
   L.turn(S,pi,a2);
   if(S.phase==='play'&&S.knocked===null&&S.lastDiscarder===pi&&L.aiKnock(S,pi))L.knock(S,pi);
  }
 }
 paint();
 if(S.phase==='play'&&S.turnIdx!==0)schedule();
}
start();
"""

CSS_T31 = r"""
.t31{display:flex;flex-direction:column;gap:10px;align-items:center;padding:10px}
.t31-top{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.t31-pile{background:#14203a;border:1px solid #24365c;border-radius:10px;padding:10px 14px;color:#cdd8ee;font-size:15px;min-width:110px;text-align:center}
.t31-pile.gold{border-color:#d9a441;color:#d9a441}
.t31-ops{width:100%;max-width:420px;display:flex;flex-direction:column;gap:6px}
.t31-op{background:#14203a;border:1px solid #24365c;border-radius:10px;padding:8px 12px;color:#cdd8ee;font-size:14px}
.t31-op.on{border-color:#3fb8af}
.t31-me{background:#14203a;border:1px solid #24365c;border-radius:12px;padding:10px;width:100%;max-width:460px;display:flex;flex-direction:column;align-items:center;gap:8px}
.t31-me.on{border-color:#d9a441}
.t31-meh{color:#cdd8ee;font-size:15px}
.t31-hand{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;min-height:60px}
.t31-hand .wcard{cursor:pointer}
.t31-acts{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.btn{min-width:110px;min-height:46px;border:0;border-radius:12px;font-size:16px;font-family:inherit;cursor:pointer;touch-action:manipulation;padding:10px 16px}
.gold{background:#d9a441;color:#1a2438;font-weight:bold}
.turq{background:#3fb8af;color:#0e1626;font-weight:bold}
.t31-msg{color:#67b98a;min-height:20px;font-size:15px;text-align:center}
"""

GAMES = [
    G(slug="higher-lower", title="بالاتر یا پایین‌تر", cat="cards", icon="🃏",
      g1="#d9a441", g2="#3fb8af",
      desc="کارت فعلی را ببین و حدس بزن: کارت بعدی بالاتر است یا پایین‌تر؟ هر حدس درست زنجیره و امتیازت را بلندتر می‌کند.",
      hint="برابر یعنی باخت! کارت بعدی باید اکیداً بالاتر یا پایین‌تر باشد.",
      engines=("common", "card"), logic=LOG_HL, ui=UI_HL, css=CSS_HL,
      tests=TESTS_HL, seed=12345),
    G(slug="video-poker", title="ویدیو پوکر", cat="cards", icon="🎴",
      g1="#3fb8af", g2="#d9a441",
      desc="ویدیو پوکر جک-یا-بهتر با اعتبار ۱۰۰: پنج کارت بگیر، کارت‌های خوب را نگه دار و بقیه را عوض کن تا دست ارزنده بسازی.",
      hint="جفت سرباز (J) یا بالاتر برنده است؛ روی کارت بزن تا نگه داشته شود، بعد تعویض بزن.",
      engines=("common", "card"), logic=LOG_VP, ui=UI_VP, css=CSS_VP,
      tests=TESTS_VP, seed=12345),
    G(slug="thirty-one", title="سی‌ویک", cat="cards", icon="♣",
      g1="#67b98a", g2="#e26d5c",
      desc="سی‌ویک با دو حریف: دستت را به بهترین تک‌خال برسان؛ در ۲۷ یا بالاتر بکوب تا رقیب‌ها فقط یک نوبت داشته باشند.",
      hint="ارزش دست = بهترین جمع تک‌خال؛ آ=۱۱ و کارت‌های تصویری=۱۰. بعد از دورریز می‌توانی بکوبی.",
      engines=("common", "card"), logic=LOG_T31, ui=UI_T31, css=CSS_T31,
      tests=TESTS_T31, seed=12345),
]
