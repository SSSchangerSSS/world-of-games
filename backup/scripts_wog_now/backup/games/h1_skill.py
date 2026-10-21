# -*- coding: utf-8 -*-
# AG-H1: 4 skill games (whack, reaction, aim, digits) — mini-kit batch, all cat="arcade"
from lib_mini import G

# ---------------- 1) whack / موشکوبی ----------------
WHACK_LOGIC = r"""
var WOG_LOGIC={
  DUR:30,CAP:3,
  upTime:function(t){return Math.max(0.5,1.4-t*0.03);},
  comboBonus:function(c){return Math.pow(2,Math.floor(c/5));},
  newState:function(){return{t:0,score:0,combo:0,bestCombo:0,hits:0,misses:0,spawnT:0.6,over:false,holes:[null,null,null,null,null,null,null,null,null]};},
  tick:function(s,dt,rng){
    if(s.over)return s;
    rng=rng||Math.random;
    s.t=Math.min(30,s.t+dt);
    var i,h,up,free,j,idx;
    for(i=0;i<9;i++){h=s.holes[i];if(h){h.ttl-=dt;if(h.ttl<=0)s.holes[i]=null;}}
    s.spawnT-=dt;
    var guard=0;
    while(s.spawnT<=0&&guard++<40){
      up=0;free=[];
      for(j=0;j<9;j++){if(s.holes[j])up++;else free.push(j);}
      if(up<3&&free.length){idx=free[Math.floor(rng()*free.length)];s.holes[idx]={ttl:WOG_LOGIC.upTime(s.t)};}
      s.spawnT+=Math.max(0.22,0.85-s.t*0.02)*(0.6+0.8*rng());
    }
    if(s.t>=30){s.over=true;for(i=0;i<9;i++)s.holes[i]=null;}
    return s;
  },
  whack:function(s,i){
    if(s.over||i<0||i>8)return{hit:false,points:0,score:s.score};
    var h=s.holes[i];
    if(h){s.holes[i]=null;s.combo++;if(s.combo>s.bestCombo)s.bestCombo=s.combo;s.hits++;var p=10*WOG_LOGIC.comboBonus(s.combo);s.score+=p;return{hit:true,points:p,score:s.score};}
    s.combo=0;s.misses++;return{hit:false,points:0,score:s.score};
  }
};
"""
WHACK_UI = r"""
var st=null,timer=null;
var panel=ce('div','wpanel');
panel.innerHTML='<div class="wgrid" id="wg"></div><div class="btnrow"><button type="button" class="gbtn gold" id="wnew" data-smoke>بازی جدید</button></div><div class="gstat" id="wstat"></div>';
$('#app').appendChild(panel);
var cells=[],grid=$('#wg'),i;
for(i=0;i<9;i++){(function(k){var b=ce('button','wcell');b.type='button';b.setAttribute('aria-label','سوراخ '+fa(k+1));b.onclick=function(){doWhack(k);};grid.appendChild(b);cells.push(b);})(i);}
function draw(){var k;for(k=0;k<9;k++)cells[k].className='wcell'+(st&&st.holes[k]?' up':'');
 hud('امتیاز: <b>'+fa(st?st.score:0)+'</b> | زمان: <b>'+fa(Math.max(0,Math.ceil(30-(st?st.t:0))))+'</b> | کمبو: <b>'+fa(st?st.combo:0)+'×</b>');}
function doWhack(k){if(!st||st.over)return;var r=L.whack(st,k);if(r.hit)toast('+'+fa(r.points));draw();}
function stop(){if(timer){clearInterval(timer);timer=null;}}
function start(){stop();st=L.newState();$('#wstat').textContent='';draw();
 timer=setInterval(function(){L.tick(st,0.1);draw();
  if(st.over){stop();
   var b=parseFloat(store.get('wog-whack-best'));if(isNaN(b)||st.score>b)store.set('wog-whack-best',String(st.score));
   ovl('پایان زمان!','امتیاز: '+fa(st.score)+' | رکورد: '+fa(Math.max(isNaN(b)?0:b,st.score)),'دوباره!',start);}},100);}
$('#wnew').onclick=start;
$('#hint').textContent='موش‌ها را سریع بزن؛ هر ۵ ضربهٔ پیوسته امتیاز ضربه را دوبرابر می‌کند. زدن به سوراخ خالی کمبو را صفر می‌کند.';
start();
"""
WHACK_CSS = r"""
.wpanel{max-width:360px;margin:0 auto}
.wgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}
.wcell{position:relative;aspect-ratio:1/1;min-height:64px;border-radius:50%;border:3px solid #26365a;background:#0d1526;cursor:pointer;touch-action:manipulation;overflow:hidden;padding:0}
.wcell:after{content:'';position:absolute;left:50%;top:105%;width:58%;height:58%;transform:translateX(-50%);border-radius:46% 46% 42% 42%;background:#8a5a33;transition:top .13s ease}
.wcell.up:after{top:16%}
.wcell.up{border-color:#d9a441}
.btnrow{display:flex;justify-content:center;gap:10px;margin:10px 0}
.gbtn{min-height:48px;min-width:120px;padding:10px 20px;border-radius:10px;border:1px solid #2c3b5e;background:#1b2947;color:#e8ecf5;font-size:16px;cursor:pointer;touch-action:manipulation}
.gbtn.gold{background:#d9a441;border-color:#d9a441;color:#14203a;font-weight:700}
.gstat{min-height:20px;text-align:center;color:#9fb0cd}
"""
whack_tests=[
("سقف ۳ موش و شبیه‌سازی کامل ۳۰ ثانیه",
 "var s=L.newState(),upMax=0,i,j;for(i=0;i<610;i++){L.tick(s,0.05,rng);var up=0;for(j=0;j<9;j++)if(s.holes[j])up++;upMax=Math.max(upMax,up);T.ok(up<=3,'cap 3');T.ok(s.t<=30.0001,'t clamp');T.eq(s.holes.length,9,'9 holes');}T.eq(s.t,30,'final t');T.ok(s.over,'over');T.ok(upMax>=1,'moles appeared');var snap=JSON.stringify(s);L.tick(s,1,rng);L.tick(s,1,rng);T.eq(JSON.stringify(s),snap,'frozen');"),
("پنهان شدن با پایان مهلت و کوچک شدن زمان",
 "var s=L.newState();s.spawnT=999;s.holes[4]={ttl:0.5};L.tick(s,1,rng);T.eq(s.holes[4],null,'mole hidden after ttl');T.ok(L.upTime(0)>L.upTime(15),'shrink 1');T.ok(L.upTime(15)>L.upTime(29),'shrink 2');T.ok(L.upTime(99)===0.5,'floor 0.5');"),
("جدول ضریب کمبو",
 "T.eq([0,1,4,5,9,10,14,15,20,25].map(L.comboBonus),[1,1,1,2,2,4,4,8,16,32],'bonus table');"),
("امتیازدهی ضربه و خطا",
 "var s=L.newState();s.holes[2]={ttl:1};var r=L.whack(s,2);T.eq([r.hit,r.points,r.score],[true,10,10],'first hit');s.holes[5]={ttl:1};r=L.whack(s,5);T.eq(r.score,20,'second hit');s.holes[0]={ttl:1};L.whack(s,0);s.holes[3]={ttl:1};L.whack(s,3);s.holes[6]={ttl:1};r=L.whack(s,6);T.eq([s.combo,r.points,r.score],[5,20,60],'combo5 doubles');r=L.whack(s,8);T.eq([r.hit,s.combo,s.score,s.misses],[false,0,60,1],'miss: no score change');"),
("ریست کمبو و انجماد پس از پایان",
 "var s=L.newState();s.combo=7;var r=L.whack(s,1);T.eq([r.hit,s.combo],[false,0],'miss resets combo');var b=L.newState();L.tick(b,30.5,rng);T.ok(b.over,'over at 30');T.eq(b.t,30,'clamped');var snap=JSON.stringify(b);var rb=L.whack(b,0);T.eq([rb.hit,rb.score],[false,0],'no whack after over');T.eq(JSON.stringify(b),snap,'state frozen');"),
]

# ---------------- 2) reaction / عکس‌العمل ----------------
REACTION_LOGIC = r"""
var WOG_LOGIC={
  ROUNDS:5,PENALTY:500,
  newState:function(){return{results:[],cur:null,over:false};},
  startRound:function(s,waitMs,nowMs){
    if(s.over)return s;
    s.cur={goAt:(nowMs||0)+(waitMs||0),penalized:false};
    return s;
  },
  tap:function(s,nowMs){
    if(s.over||!s.cur)return{early:false,ms:null,idle:true};
    if(nowMs<s.cur.goAt){
      if(!s.cur.penalized){s.cur.penalized=true;return{early:true,ms:null,penalized:true};}
      return{early:true,ms:null,penalized:false};
    }
    var ms=(nowMs-s.cur.goAt)+(s.cur.penalized?500:0);
    s.results.push(ms);s.cur=null;
    if(s.results.length>=5)s.over=true;
    return{early:false,ms:ms,done:s.over};
  },
  stats:function(ms){
    if(!ms||!ms.length)return{mean:0,median:0,best:0};
    var a=ms.slice().sort(function(x,y){return x-y;}),n=a.length,sum=0,i;
    for(i=0;i<n;i++)sum+=a[i];
    return{mean:sum/n,median:(n%2)?a[(n-1)/2]:(a[n/2-1]+a[n/2])/2,best:a[0]};
  },
  rating:function(mean){
    if(mean<250)return'فوق‌العاده';
    if(mean<350)return'خوب';
    if(mean<450)return'متوسط';
    return'کند';
  }
};
"""
REACTION_UI = r"""
var st=null,tGo=null,tNext=null;
var panel=ce('div','rpanel');
panel.innerHTML='<div class="rscreen" id="rscr"><div class="rmsg" id="rmsg">با دکمهٔ زیر شروع کن</div></div>'+
 '<div class="btnrow"><button type="button" class="gbtn gold" id="rtap" data-smoke>بازی جدید</button></div>'+
 '<div class="rlist" id="rlist"></div>';
$('#app').appendChild(panel);
function msg(m){$('#rmsg').textContent=m;}
function setBtn(t,cls){var b=$('#rtap');b.textContent=t;b.className='gbtn gold'+(cls?' '+cls:'');}
function drawList(){var h='',i,rs=st?st.results:[];
 for(i=0;i<5;i++)h+='<span class="rchip'+(i<rs.length?' done':'')+'">'+(i<rs.length?fa(Math.round(rs[i])):'-')+'</span>';
 $('#rlist').innerHTML=h;hud('دور: <b>'+fa(st?st.results.length:0)+'</b> از ۵');}
function clearT(){if(tGo){clearTimeout(tGo);tGo=null;}if(tNext){clearTimeout(tNext);tNext=null;}}
function armRound(){var wait=1000+Math.floor(Math.random()*3000);
 L.startRound(st,wait,performance.now());
 tGo=setTimeout(function(){msg('بزن!');setBtn('بزن!','go');},wait);}
function newGame(){clearT();st=L.newState();drawList();msg('آماده...');setBtn('صبر کن','wait');armRound();}
function finish(){var m=st.results.reduce(function(a,b){return a+b;},0)/st.results.length;
 var mr=Math.round(m),rt=L.rating(m);
 var ob=parseFloat(store.get('wog-reaction-best'));if(isNaN(ob)||mr<ob)store.set('wog-reaction-best',String(mr));
 var bb=isNaN(ob)?mr:Math.min(ob,mr);
 ovl('پایان!','میانگین: '+fa(mr)+' میلی‌ثانیه | رتبه: '+rt+' | رکورد: '+fa(bb),'بازی دوباره',newGame);}
$('#rtap').onclick=function(){
 if(!st||st.over){newGame();return;}
 if(!st.cur)return;
 var r=L.tap(st,performance.now());
 if(r.early){msg('زود بود! ۰٫۵ ثانیه جریمه');setBtn('صبر کن','wait');return;}
 if(tGo){clearTimeout(tGo);tGo=null;}
 drawList();msg(fa(Math.round(r.ms))+' میلی‌ثانیه');setBtn('...','idle');
 if(st.over)finish();else tNext=setTimeout(armRound,900);
};
$('#hint').textContent='صبر کن تا علامت «بزن!» ظاهر شود، بعد فوری ضربه بزن؛ زود زدن یعنی ۰٫۵ ثانیه جریمه (هر دور حداکثر یک‌بار).';
drawList();
"""
REACTION_CSS = r"""
.rpanel{max-width:420px;margin:0 auto}
.rscreen{background:#14203a;border:1px solid #26365a;border-radius:14px;min-height:120px;display:flex;align-items:center;justify-content:center;margin:12px 0}
.rmsg{font-size:22px;color:#e8ecf5;text-align:center;padding:12px}
.btnrow{display:flex;justify-content:center;gap:10px;margin:10px 0}
.gbtn{min-height:56px;min-width:200px;padding:10px 20px;border-radius:10px;border:1px solid #2c3b5e;background:#1b2947;color:#e8ecf5;font-size:18px;cursor:pointer;touch-action:manipulation}
.gbtn.gold{background:#d9a441;border-color:#d9a441;color:#14203a;font-weight:700}
.gbtn.go{background:#67b98a;border-color:#67b98a;color:#10241a}
.gbtn.wait{opacity:.75}
.rlist{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.rchip{min-width:52px;min-height:36px;padding:6px 8px;border-radius:8px;background:#1b2947;border:1px solid #2c3b5e;color:#9fb0cd;text-align:center}
.rchip.done{color:#d9a441;border-color:#d9a441}
"""
reaction_tests=[
("تشخیص زدن زود و جریمه یک‌باره",
 "var s=L.newState();L.startRound(s,1000,0);var r=L.tap(s,500);T.eq([r.early,r.ms],[true,null],'early');r=L.tap(s,700);T.eq(r.early,true,'early again');T.eq(r.penalized,false,'no second penalty');r=L.tap(s,1250);T.eq([r.early,r.ms],[false,750],'penalty applied exactly once');T.eq(s.results,[750],'recorded');T.eq(s.cur,null,'round consumed');"),
("مرز دقیق GO و حالت بی‌کار",
 "var s0=L.newState();var r=L.tap(s0,5);T.eq(r.idle,true,'idle before start');L.startRound(s0,1000,0);r=L.tap(s0,1000);T.eq([r.early,r.ms],[false,0],'exact go boundary');T.eq(s0.results,[0],'zero recorded');T.eq(s0.over,false,'not over yet');"),
("آمار میانگین، میانه، بهترین",
 "var a=L.stats([250,300,200]);T.eq([a.mean,a.median,a.best],[250,250,200],'odd count');var b=L.stats([200,300,400,100]);T.eq([b.mean,b.median,b.best],[250,250,100],'even count');T.eq(L.stats([]).best,0,'empty safe');var c=L.stats([100,900,300]);T.eq([c.mean,c.median,c.best],[433.3333333333333,300,100],'unsorted input');"),
("سطوح رتبه‌بندی",
 "T.eq(L.rating(249),L.rating(0),'same top tier');T.ok(L.rating(249)!==L.rating(250),'tier change');T.eq(L.rating(250),'خوب','250=khoob');T.eq(L.rating(349),'خوب','349=khoob');T.eq(L.rating(350),'متوسط','350=mid');T.eq(L.rating(449),'متوسط','449=mid');T.eq(L.rating(450),'کند','450=slow');T.eq(L.rating(100),'فوق‌العاده','top literal');"),
("جریان کامل ۵ دور",
 "var s=L.newState(),t0=0,i,r;for(i=0;i<5;i++){var wait=1000+i*100;L.startRound(s,wait,t0);T.ok(s.cur,'round armed');r=L.tap(s,t0+wait+150+i*10);T.eq(r.ms,150+i*10,'ms round');T.eq(!!r.done,i===4,'done flag');t0+=wait+1000;}T.eq(s.results,[150,160,170,180,190],'results');T.ok(s.over,'over');T.eq(L.stats(s.results).mean,170,'mean');r=L.tap(s,99999);T.eq(r.idle,true,'idle after over');L.startRound(s,500,0);T.eq(s.cur,null,'no arm after over');"),
]

# ---------------- 3) aim / تیرانداز هدف ----------------
AIM_LOGIC = r"""
var WOG_LOGIC={
  W:320,H:320,DUR:30,LIFE:1500,
  speedBonus:function(ms){if(ms<=400)return 10;if(ms<=800)return 6;if(ms<=1200)return 3;return 0;},
  accuracy:function(s){var n=s.hits+s.misses;return n?Math.round(100*s.hits/n):0;},
  spawnNext:function(s,rng){
    rng=rng||Math.random;
    var r=24+10*rng(),m=r+2;
    s.target={x:m+rng()*(320-2*m),y:m+rng()*(320-2*m),r:r,born:s.t*1000};
    s.spawned=(s.spawned||0)+1;
    return s.target;
  },
  newState:function(rng){var s={t:0,score:0,hits:0,misses:0,combo:0,bestCombo:0,target:null,over:false,spawned:0};WOG_LOGIC.spawnNext(s,rng);return s;},
  shoot:function(s,x,y,nowMs){
    if(s.over||!s.target)return{hit:false,speedMs:null,points:0};
    var dx=x-s.target.x,dy=y-s.target.y,d=Math.sqrt(dx*dx+dy*dy);
    if(d<=s.target.r){
      var sp=Math.max(0,(nowMs||0)-s.target.born),pts=10+WOG_LOGIC.speedBonus(sp);
      s.hits++;s.combo++;if(s.combo>s.bestCombo)s.bestCombo=s.combo;s.score+=pts;
      s.target=null;WOG_LOGIC.spawnNext(s);
      return{hit:true,speedMs:sp,points:pts};
    }
    s.misses++;s.combo=0;s.score=Math.max(0,s.score-5);
    return{hit:false,speedMs:null,points:-5};
  },
  tick:function(s,dt,rng){
    if(s.over)return s;
    rng=rng||Math.random;
    s.t=Math.min(30,s.t+dt);
    if(s.target&&(s.t*1000-s.target.born)>1500)s.target=null;
    if(!s.target)WOG_LOGIC.spawnNext(s,rng);
    if(s.t>=30){s.over=true;s.target=null;}
    return s;
  }
};
"""
AIM_UI = r"""
var st=null,timer=null,t0=0;
var panel=ce('div','apanel');
panel.innerHTML='<div class="aboard" id="aboard"><div class="atgt" id="atgt"></div></div>'+
 '<div class="btnrow"><button type="button" class="gbtn gold" id="anew" data-smoke>بازی جدید</button></div><div class="gstat" id="astat"></div>';
$('#app').appendChild(panel);
var board=$('#aboard'),tgt=$('#atgt');
function place(){if(!st||!st.target){tgt.style.display='none';return;}
 var t=st.target,sc=board.clientWidth/320;
 tgt.style.display='';tgt.style.width=(t.r*2*sc)+'px';tgt.style.height=(t.r*2*sc)+'px';
 tgt.style.left=((t.x-t.r)*sc)+'px';tgt.style.top=((t.y-t.r)*sc)+'px';}
function draw(){place();
 hud('امتیاز: <b>'+fa(st?st.score:0)+'</b> | زمان: <b>'+fa(Math.max(0,Math.ceil(30-(st?st.t:0))))+'</b> | دقت: <b>'+fa(st?L.accuracy(st):0)+'٪</b> | کمبو: <b>'+fa(st?st.combo:0)+'</b>');}
board.addEventListener('pointerdown',function(e){
 if(!st||st.over)return;
 e.preventDefault();
 var rc=board.getBoundingClientRect(),sc=320/rc.width;
 var x=(e.clientX-rc.left)*sc,y=(e.clientY-rc.top)*sc;
 var r=L.shoot(st,x,y,performance.now()-t0);
 $('#astat').textContent=r.hit?('برخورد! +'+fa(r.points)):('خطا! -۵');
 draw();});
function stop(){if(timer){clearInterval(timer);timer=null;}}
function start(){stop();st=L.newState();t0=performance.now();$('#astat').textContent='';draw();
 timer=setInterval(function(){L.tick(st,0.1);draw();
  if(st.over){stop();
   var b=parseFloat(store.get('wog-aim-best'));if(isNaN(b)||st.score>b)store.set('wog-aim-best',String(st.score));
   ovl('پایان!','امتیاز: '+fa(st.score)+' | دقت: '+fa(L.accuracy(st))+'٪ | رکورد: '+fa(Math.max(isNaN(b)?0:b,st.score)),'دوباره!',start);}},100);}
$('#anew').onclick=start;
$('#hint').textContent='روی هدف ظاهرشده بزن؛ هرچه سریع‌تر بزنی جایزهٔ سرعت بیشتری می‌گیری. جا خالی ۵ امتیاز کم می‌کند و کمبو را صفر می‌کند.';
start();
"""
AIM_CSS = r"""
.apanel{max-width:360px;margin:0 auto}
.aboard{position:relative;width:320px;max-width:100%;aspect-ratio:1/1;margin:12px auto;background:#0d1526;border:2px solid #26365a;border-radius:14px;overflow:hidden;touch-action:manipulation;cursor:crosshair}
.atgt{position:absolute;border-radius:50%;background:#e26d5c;border:3px solid #f2c1b5;box-shadow:inset 0 0 0 6px #c1503f;cursor:pointer}
.btnrow{display:flex;justify-content:center;gap:10px;margin:10px 0}
.gbtn{min-height:48px;min-width:120px;padding:10px 20px;border-radius:10px;border:1px solid #2c3b5e;background:#1b2947;color:#e8ecf5;font-size:16px;cursor:pointer;touch-action:manipulation}
.gbtn.gold{background:#d9a441;border-color:#d9a441;color:#14203a;font-weight:700}
.gstat{min-height:20px;text-align:center;color:#9fb0cd}
"""
aim_tests=[
("برخورد در شعاع و خطا",
 "var s=L.newState(rng);s.t=0;s.target={x:160,y:160,r:26,born:0};var r=L.shoot(s,160,160,100);T.eq([r.hit,r.speedMs,r.points],[true,100,20],'center hit');s.target={x:160,y:160,r:26,born:0};r=L.shoot(s,186,160,300);T.eq([r.hit,r.points],[true,20],'rim hit');s.target={x:160,y:160,r:26,born:0};r=L.shoot(s,187,160,300);T.eq([r.hit,r.points],[false,-5],'just outside');T.eq([s.misses,s.combo,s.score],[1,0,35],'miss resets combo, -5');"),
("پله‌های جایزهٔ سرعت",
 "T.eq([100,400,401,800,801,1200,1201,2000].map(L.speedBonus),[10,10,6,6,3,3,0,0],'speed tiers');"),
("محاسبهٔ دقت",
 "var s=L.newState(rng);T.eq(L.accuracy(s),0,'no shots');s.hits=3;s.misses=1;T.eq(L.accuracy(s),75,'75 percent');s.hits=2;s.misses=2;T.eq(L.accuracy(s),50,'50 percent');s.hits=1;s.misses=0;T.eq(L.accuracy(s),100,'100 percent');"),
("۲۰۰ اسپاون داخل محدوده",
 "var s=L.newState(rng),i,ok=true;for(i=0;i<200;i++){var t=L.spawnNext(s,rng),m=t.r+2;if(t.x<m-1e-9||t.x>320-m+1e-9||t.y<m-1e-9||t.y>320-m+1e-9)ok=false;if(t.r<24||t.r>34)ok=false;}T.ok(ok,'all in bounds');T.eq(s.spawned,201,'spawn counter');"),
("شبیه‌سازی ۳۰ ثانیه و انجماد",
 "var s=L.newState(rng),i;for(i=0;i<300;i++){L.tick(s,0.1,rng);if(s.target&&!s.over)L.shoot(s,s.target.x,s.target.y,s.t*1000);T.ok(s.t<=30.0001,'t clamp');T.ok(s.score>=0,'score floor');}T.eq(s.t,30,'end t');T.ok(s.over,'over');T.eq(s.misses,0,'no miss');T.ok(s.hits>100,'many hits');T.eq(s.score,s.hits*20,'score=20*hits');T.eq(L.accuracy(s),100,'acc 100');var snap=JSON.stringify(s);L.tick(s,1,rng);var r=L.shoot(s,160,160,99999);T.eq(r.hit,false,'locked after over');T.eq(JSON.stringify(s),snap,'frozen');"),
]

# ---------------- 4) digits / رقم‌های کوتاه ----------------
DIGITS_LOGIC = r"""
var WOG_LOGIC={
  MIN:3,MAX:12,LIVES:3,
  genSeq:function(n,rng){
    rng=rng||Math.random;
    var a=[],n=Math.max(0,n|0);
    while(a.length<n){
      var d=Math.floor(rng()*10);
      if(a.length>=2&&a[a.length-1]===d&&a[a.length-2]===d)continue;
      a.push(d);
    }
    return a;
  },
  check:function(seq,input){
    if(!input||input.length!==seq.length)return false;
    for(var i=0;i<seq.length;i++)if(seq[i]!==input[i])return false;
    return true;
  },
  newState:function(){return{span:3,lives:3,seq:[],input:[],over:false,won:false,best:0,rounds:0};},
  beginLevel:function(s,rng){
    if(s.over)return s.seq;
    s.seq=WOG_LOGIC.genSeq(s.span,rng);s.input=[];
    return s.seq;
  },
  pushDigit:function(s,d){
    if(s.over)return{done:true,correct:false,over:true};
    s.input.push(d);
    if(s.input.length<s.seq.length)return{done:false,correct:null};
    var ok=WOG_LOGIC.check(s.seq,s.input);
    s.rounds++;
    if(ok){
      if(s.span>s.best)s.best=s.span;
      if(s.span>=12){s.over=true;s.won=true;return{done:true,correct:true,over:true,won:true};}
      s.span++;s.input=[];return{done:true,correct:true,over:false};
    }
    s.lives--;s.input=[];
    if(s.lives<=0){s.over=true;return{done:true,correct:false,over:true};}
    return{done:true,correct:false,over:false};
  }
};
"""
DIGITS_UI = r"""
var st=null,timers=[],accepting=false;
var panel=ce('div','dpanel');
panel.innerHTML='<div class="ddisp" id="ddisp">آماده‌ای؟</div><div class="dinp" id="dinp"></div>'+
 '<div class="dpad" id="dpad"></div><div class="btnrow"><button type="button" class="gbtn gold" id="dnew" data-smoke>بازی جدید</button></div>';
$('#app').appendChild(panel);
var pad=$('#dpad'),d;
for(d=0;d<10;d++){(function(k){var b=ce('button','dkey');b.type='button';b.textContent=fa(k);b.onclick=function(){press(k);};pad.appendChild(b);})(d);}
var bk=ce('button','dkey dwide');bk.type='button';bk.textContent='پاک کردن';
bk.onclick=function(){if(st&&!st.over&&accepting&&st.input.length){st.input.pop();drawIn();}};
pad.appendChild(bk);
function clearT(){while(timers.length)clearTimeout(timers.pop());}
function drawIn(){var i,h='',n=st?st.seq.length:0,inp=st?st.input:[];
 for(i=0;i<n;i++)h+='<span class="dsl'+(i<inp.length?' on':'')+'">'+(i<inp.length?fa(inp[i]):'.')+'</span>';
 $('#dinp').innerHTML=h;
 hud('طول رشته: <b>'+fa(st?st.span:3)+'</b> | جان: <b>'+(st&&st.lives>0?new Array(st.lives+1).join('.'):'')+'</b> | رکورد: <b>'+fa(st?st.best:0)+'</b>');}
function showSeq(){clearT();accepting=false;st.input=[];var seq=st.seq;drawIn();
 var el=$('#ddisp'),idx=0;
 el.textContent='دقت کن';
 var step=function(){
  if(idx>=seq.length){el.textContent='حالا بنویس';accepting=true;return;}
  el.textContent=fa(seq[idx]);
  timers.push(setTimeout(function(){el.textContent='?';idx++;timers.push(setTimeout(step,220));},640));};
 timers.push(setTimeout(step,400));}
function press(k){if(!st||st.over||!accepting)return;
 var r=L.pushDigit(st,k);drawIn();
 if(!r.done)return;
 accepting=false;
 if(r.correct){$('#ddisp').textContent='درست!';
  if(r.over){finish();return;}
  timers.push(setTimeout(showSeq,850));}
 else{$('#ddisp').textContent='اشتباه بود!';
  if(r.over){finish();return;}
  timers.push(setTimeout(showSeq,950));}}
function finish(){var b=parseFloat(store.get('wog-digits-best'));
 if(isNaN(b)||st.best>b)store.set('wog-digits-best',String(st.best));
 var bb=Math.max(isNaN(b)?0:b,st.best);
 ovl(st.won?'شگفت‌انگیز!':'باختی!','بلندترین رشته: '+fa(st.best)+' | رکورد: '+fa(bb),'بازی دوباره',start);}
function start(){clearT();st=L.newState();$('#ddisp').textContent='آماده';drawIn();timers.push(setTimeout(showSeq,600));}
$('#dnew').onclick=start;
$('#hint').textContent='اعداد یکی‌یکی نمایش داده می‌شوند؛ سپس به همان ترتیب روی صفحه‌کلید بزن. با هر موفقیت رشته بلندتر و با ۳ خطا بازی تمام می‌شود.';
start();
"""
DIGITS_CSS = r"""
.dpanel{max-width:380px;margin:0 auto}
.ddisp{background:#14203a;border:1px solid #26365a;border-radius:14px;min-height:90px;display:flex;align-items:center;justify-content:center;font-size:42px;color:#d9a441;margin:12px 0 6px;letter-spacing:6px}
.dinp{display:flex;gap:8px;justify-content:center;min-height:48px;align-items:center;margin:6px 0;flex-wrap:wrap}
.dsl{width:34px;height:44px;border-radius:8px;background:#1b2947;border:1px solid #2c3b5e;color:#9fb0cd;display:flex;align-items:center;justify-content:center;font-size:20px}
.dsl.on{color:#67b98a;border-color:#67b98a}
.dpad{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:10px 0}
.dkey{min-height:48px;border-radius:10px;border:1px solid #2c3b5e;background:#1b2947;color:#e8ecf5;font-size:18px;cursor:pointer;touch-action:manipulation}
.dkey.dwide{grid-column:span 2;color:#e26d5c}
.btnrow{display:flex;justify-content:center;gap:10px;margin:10px 0}
.gbtn{min-height:48px;min-width:120px;padding:10px 20px;border-radius:10px;border:1px solid #2c3b5e;background:#1b2947;color:#e8ecf5;font-size:16px;cursor:pointer;touch-action:manipulation}
.gbtn.gold{background:#d9a441;border-color:#d9a441;color:#14203a;font-weight:700}
"""
digits_tests=[
("طول و بازهٔ ارقام",
 "var a=L.genSeq(12,rng);T.eq(a.length,12,'len 12');var b=L.genSeq(3,rng);T.eq(b.length,3,'len 3');T.eq(L.genSeq(0,rng).length,0,'len 0');var c=L.genSeq(50,rng),ok=true,i;for(i=0;i<50;i++)if(!(c[i]>=0&&c[i]<=9&&c[i]===(c[i]|0)))ok=false;T.ok(ok,'digits 0..9 only');"),
("ممنوعیت سه رقم پشت سر هم در ۲۰۰ دنباله",
 "var bad=0,i,j;for(i=0;i<200;i++){var s=L.genSeq(12,rng);for(j=2;j<12;j++)if(s[j]===s[j-1]&&s[j]===s[j-2])bad++;}T.eq(bad,0,'no triple in 200 seqs');"),
("بررسی دقیق تطابق",
 "T.eq(L.check([1,2,3],[1,2,3]),true,'exact');T.eq(L.check([1,2,3],[1,2,4]),false,'wrong last');T.eq(L.check([1,2,3],[1,2]),false,'too short');T.eq(L.check([1,2,3],[1,2,3,4]),false,'too long');T.eq(L.check([],[]),true,'empty ok');T.eq(L.check([5,5,1],[5,5,1]),true,'repeat ok');"),
("سه خطا = پایان",
 "var s=L.newState();T.eq([s.span,s.lives,s.over],[3,3,false],'fresh state');T.eq(L.beginLevel(s,rng).length,3,'seq len 3');var r=L.pushDigit(s,7);T.eq(r.done,false,'partial input');r=L.pushDigit(s,7);T.eq(r.done,false,'partial input 2');r=L.pushDigit(s,7);T.eq([r.done,r.correct,r.over,s.lives],[true,false,false,2],'wrong 1');L.beginLevel(s,rng);r=L.pushDigit(s,7);while(!r.done)r=L.pushDigit(s,7);T.eq([r.correct,s.lives,s.over],[false,1,false],'wrong 2');L.beginLevel(s,rng);r=L.pushDigit(s,7);while(!r.done)r=L.pushDigit(s,7);T.eq([r.correct,r.over,s.over,s.lives,s.won],[false,true,true,0,false],'wrong 3 = game over');"),
("سقف ۱۲ و جریان ارتقا",
 "var s=L.newState();s.span=11;L.beginLevel(s,rng);var i,r;for(i=0;i<11;i++)r=L.pushDigit(s,s.seq[i]);T.eq([r.correct,s.span],[true,12],'up to 12');L.beginLevel(s,rng);for(i=0;i<12;i++)r=L.pushDigit(s,s.seq[i]);T.eq([r.correct,r.over,s.won,s.span,s.best],[true,true,true,12,12],'cap 12 win');r=L.pushDigit(s,1);T.eq(r.over,true,'locked after over');"),
]

GAMES=[
 G(slug="whack",title="موشکوبی",cat="arcade",icon="hammer",g1="#d9a441",g2="#3fb8af",
   desc="۳۰ ثانیه وقت داری؛ موش‌ها از ۹ سوراخ بیرون می‌آیند و باید سریع روی آن‌ها بزنی. ضربه‌های پیوسته امتیاز دوبرابر می‌دهند.",
   hint="موش‌ها را سریع بزن؛ کمبو هر ۵ ضربه امتیاز را دوبرابر می‌کند.",
   logic=WHACK_LOGIC,ui=WHACK_UI,css=WHACK_CSS,engines=("common",),tests=whack_tests,seed=12345),
 G(slug="reaction",title="عکس‌العمل",cat="arcade",icon="bolt",g1="#3fb8af",g2="#d9a441",
   desc="پنج دور آزمون عکس‌العمل: منتظر علامت بمان و فوری ضربه بزن. زود زدن جریمهٔ نیم‌ثانیه دارد و رتبهٔ نهایی می‌گیری.",
   hint="صبر کن تا علامت ظاهر شود، بعد فوری بزن.",
   logic=REACTION_LOGIC,ui=REACTION_UI,css=REACTION_CSS,engines=("common",),tests=reaction_tests,seed=12345),
 G(slug="aim",title="تیرانداز هدف",cat="arcade",icon="target",g1="#e26d5c",g2="#d9a441",
   desc="در ۳۰ ثانیه به هدف‌هایی که یکی‌یکی ظاهر می‌شوند شلیک کن؛ سرعت عمل جایزه دارد و هر خطا ۵ امتیاز کم می‌کند.",
   hint="سریع و دقیق بزن؛ جا خالی گران تمام می‌شود.",
   logic=AIM_LOGIC,ui=AIM_UI,css=AIM_CSS,engines=("common",),tests=aim_tests,seed=12345),
 G(slug="digits",title="رقم‌های کوتاه",cat="arcade",icon="grid",g1="#67b98a",g2="#3fb8af",
   desc="رشتهٔ اعداد را به حافظه بسپار و به همان ترتیب تایپ کن؛ از طول ۳ تا ۱۲ پیش می‌روی و ۳ جان داری.",
   hint="به ترتیب اعداد دقت کن؛ هر سطح یک رقم بلندتر می‌شود.",
   logic=DIGITS_LOGIC,ui=DIGITS_UI,css=DIGITS_CSS,engines=("common",),tests=digits_tests,seed=12345),
]
