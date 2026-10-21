# -*- coding: utf-8 -*-
# AG-G3 — three canvas arcade games: asteroids + invaders + dodge (cat=arcade, engines common+arcade)
from lib_mini import G

CSS_ARC = r""".wbar{display:flex;gap:8px;justify-content:center;margin:10px 0;flex-wrap:wrap}
.wbtn{min-width:64px;min-height:44px;border-radius:10px;border:1px solid #d9a441;background:#14203a;color:#d9a441;font-size:15px;padding:8px 14px;touch-action:manipulation;cursor:pointer}
.wbtn:active{background:#1d2c4e}
canvas{touch-action:none;max-width:100%;border:1px solid #1e2c4a;border-radius:8px;display:block;margin:0 auto}"""

AST_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
var TAU=Math.PI*2,W=480,H=640,ROT=4,THR=260,FR=1.2,BSPD=420;
function wrapPos(x,y,w,h){return{x:((x%w)+w)%w,y:((y%h)+h)%h};}
function spawnWave(s,r){var n=2+s.wave,i;for(i=0;i<n;i++){var a=r()*TAU,d=170+r()*90,p=wrapPos(W/2+Math.cos(a)*d,H/2+Math.sin(a)*d,W,H);s.asteroids.push({x:p.x,y:p.y,vx:(r()*2-1)*60,vy:(r()*2-1)*60,r:34,size:3});}}
function newState(rng){var r=rng||Math.random;var s={w:W,h:H,rng:r,ship:{x:W/2,y:H/2,a:0,vx:0,vy:0,cool:0},asteroids:[],bullets:[],lives:3,score:0,wave:1,t:0,over:false,inv:2};spawnWave(s,r);return s;}
function shoot(s){var sh=s.ship;if(s.over||sh.cool>0)return false;sh.cool=0.22;s.bullets.push({x:sh.x+Math.cos(sh.a)*14,y:sh.y+Math.sin(sh.a)*14,vx:Math.cos(sh.a)*BSPD+sh.vx*0.4,vy:Math.sin(sh.a)*BSPD+sh.vy*0.4,life:1.1,r:3});return true;}
function splitAsteroid(ast,rng){var r=rng||Math.random;if(!ast||ast.size<=1)return[];var out=[],i;for(i=0;i<2;i++){var a=r()*TAU,sp=40+r()*70;out.push({x:ast.x,y:ast.y,vx:ast.vx*0.5+Math.cos(a)*sp,vy:ast.vy*0.5+Math.sin(a)*sp,r:ast.r*0.55,size:ast.size-1});}return out;}
function collide(s){var shipHit=false,bh=[],ah=[],i,j;
 for(i=0;i<s.asteroids.length;i++){var a=s.asteroids[i],dx=a.x-s.ship.x,dy=a.y-s.ship.y;
  if(dx*dx+dy*dy<(a.r+10)*(a.r+10))shipHit=true;
  for(j=0;j<s.bullets.length;j++){var b=s.bullets[j],ux=a.x-b.x,uy=a.y-b.y,rr=a.r+b.r;if(ux*ux+uy*uy<rr*rr){bh.push(j);ah.push(i);}}}
 return{shipHit:shipHit,bulletsHit:bh,astsHit:ah};}
function step(s,dt,keys){if(s.over)return s;keys=keys||{};var sh=s.ship,i,p;
 s.t+=dt;sh.cool-=dt;s.inv-=dt;
 if(keys.left)sh.a-=ROT*dt;
 if(keys.right)sh.a+=ROT*dt;
 sh.a=((sh.a%TAU)+TAU)%TAU;
 if(keys.up){sh.vx+=Math.cos(sh.a)*THR*dt;sh.vy+=Math.sin(sh.a)*THR*dt;}
 var f=Math.exp(-FR*dt);sh.vx*=f;sh.vy*=f;
 p=wrapPos(sh.x+sh.vx*dt,sh.y+sh.vy*dt,W,H);sh.x=p.x;sh.y=p.y;
 for(i=s.bullets.length-1;i>=0;i--){var b=s.bullets[i];b.life-=dt;if(b.life<=0){s.bullets.splice(i,1);continue;}p=wrapPos(b.x+b.vx*dt,b.y+b.vy*dt,W,H);b.x=p.x;b.y=p.y;}
 for(i=0;i<s.asteroids.length;i++){var a2=s.asteroids[i];p=wrapPos(a2.x+a2.vx*dt,a2.y+a2.vy*dt,W,H);a2.x=p.x;a2.y=p.y;}
 if(keys.fire)shoot(s);
 var col=collide(s);
 if(col.shipHit&&s.inv<=0){s.lives--;s.inv=2;sh.x=W/2;sh.y=H/2;sh.vx=0;sh.vy=0;if(s.lives<=0)s.over=true;}
 if(col.bulletsHit.length){var keep=[];for(i=0;i<s.bullets.length;i++)if(col.bulletsHit.indexOf(i)<0)keep.push(s.bullets[i]);s.bullets=keep;}
 if(col.astsHit.length){var na=[];for(i=0;i<s.asteroids.length;i++){if(col.astsHit.indexOf(i)>=0){var as=s.asteroids[i];s.score+=as.size===3?20:(as.size===2?50:100);na=na.concat(splitAsteroid(as,s.rng));}else na.push(s.asteroids[i]);}s.asteroids=na;}
 if(!s.asteroids.length){s.wave++;s.score+=100;spawnWave(s,s.rng);}
 return s;}
return{newState:newState,step:step,shoot:shoot,splitAsteroid:splitAsteroid,wrapPos:wrapPos,collide:collide};
})();
"""

AST_UI = r"""
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=function(){newGame();};$('#app').appendChild(nb);
var cv=makeCanvas(480,640),ctx=cv.ctx,keys=keyState(),s=null,ended=false;
var best=storeBest('wog-asteroids-best')||0;
bindPad([{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'},{k:'ArrowUp',label:'▲'},{k:'Space',label:'شلیک'}]);
$('#hint').textContent='چپ/راست چرخش، بالا پیشران، فاصله شلیک؛ سیارک بزرگ با هر شلیک به دو تکه کوچک‌تر می‌شکند.';
function newGame(){s=L.newState(Math.random);ended=false;rep();}
function rep(){hud('امتیاز '+fa(s.score)+' · رکورد '+fa(Math.max(best,s.score))+' · جان '+fa(s.lives)+' · موج '+fa(s.wave));}
function draw(){var asg=ctx.createLinearGradient(0,0,0,640);asg.addColorStop(0,'#070a18');asg.addColorStop(1,'#10142a');ctx.fillStyle=asg;ctx.fillRect(0,0,480,640);ctx.fillStyle='rgba(255,255,255,.22)';for(var as2=0;as2<40;as2++){ctx.fillRect((as2*113)%480,(as2*61)%640,1.3,1.3);}var i,a;
 ctx.lineWidth=2;ctx.strokeStyle='#3fb8af';
 for(i=0;i<s.asteroids.length;i++){a=s.asteroids[i];ctx.beginPath();ctx.arc(a.x,a.y,a.r,0,6.2832);ctx.stroke();}
 ctx.fillStyle='#d9a441';
 for(i=0;i<s.bullets.length;i++){a=s.bullets[i];ctx.fillRect(a.x-2,a.y-2,4,4);}
 if(!s.over){ctx.save();ctx.translate(s.ship.x,s.ship.y);ctx.rotate(s.ship.a);
  ctx.strokeStyle='#d9a441';ctx.beginPath();ctx.moveTo(14,0);ctx.lineTo(-10,8);ctx.lineTo(-5,0);ctx.lineTo(-10,-8);ctx.closePath();ctx.stroke();
  if(keys['ArrowUp']){ctx.strokeStyle='#e26d5c';ctx.beginPath();ctx.moveTo(-8,4);ctx.lineTo(-17,0);ctx.lineTo(-8,-4);ctx.stroke();}
  ctx.restore();}}
rafStep(function(dt){if(!s)return;
 if(!s.over){s=L.step(s,Math.min(dt,0.05),{left:!!keys['ArrowLeft'],right:!!keys['ArrowRight'],up:!!keys['ArrowUp'],fire:!!keys['Space']});rep();}
 draw();
 if(s.over&&!ended){ended=true;best=bestOf('wog-asteroids-best',s.score);
  ovl('سفینه نابود شد','امتیاز: '+fa(s.score)+' · تا موج '+fa(s.wave),'بازی دوباره',function(){newGame();});}});
newGame();
"""

AST_TESTS=[
("چرخش و پیچش زاویه", r"""
var s=L.newState(rng);s.asteroids.length=0;
s.ship.a=0.1;L.step(s,1,{left:1});
T.ok(s.ship.a>=0&&s.ship.a<Math.PI*2,'range');T.approx(s.ship.a,Math.PI*2-3.9,1e-9);
s.ship.a=6.3;L.step(s,0.05,{right:1});T.approx(s.ship.a,6.5-Math.PI*2,1e-9);
s.ship.a=1;L.step(s,0.1,{right:1});T.approx(s.ship.a,1.4,1e-9);
s.ship.a=0;L.step(s,0.1,{left:1});T.approx(s.ship.a,Math.PI*2-0.4,1e-9);
"""),
("پیشران و اصطکاک همگرا", r"""
var s=L.newState(rng),i,k={up:1};
for(i=0;i<1800;i++){s.inv=9999;L.step(s,1/60,k);}
var sp=Math.sqrt(s.ship.vx*s.ship.vx+s.ship.vy*s.ship.vy);
T.ok(sp>170&&sp<270,'terminal '+sp);
T.ok(Math.abs(s.ship.vy)<1e-9,'axis');
for(i=0;i<180;i++){s.inv=9999;L.step(s,1/60,{});}
sp=Math.sqrt(s.ship.vx*s.ship.vx+s.ship.vy*s.ship.vy);
T.ok(sp<20,'decayed '+sp);
"""),
("پیچش موقعیت در صفحه", r"""
var w=L.wrapPos(-10,20,500,400);T.approx(w.x,490,1e-9);T.approx(w.y,20,1e-9);
w=L.wrapPos(510,-5,500,400);T.approx(w.x,10,1e-9);T.approx(w.y,395,1e-9);
w=L.wrapPos(500,400,500,400);T.approx(w.x,0,1e-9);T.approx(w.y,0,1e-9);
w=L.wrapPos(-500,-400,500,400);T.approx(w.x,0,1e-9);T.approx(w.y,0,1e-9);
"""),
("شکاف سیارک به دو قطعه", r"""
var big={x:100,y:100,vx:50,vy:-20,r:34,size:3};
var ch=L.splitAsteroid(big,rng);T.eq(ch.length,2);
var i;for(i=0;i<2;i++){T.eq(ch[i].size,2);T.approx(ch[i].r,18.7,1e-9);T.ok(ch[i].r>0&&ch[i].r<34,'valid r');T.ok(isFinite(ch[i].vx)&&isFinite(ch[i].vy),'vel');T.approx(ch[i].x,100,1e-9);}
T.eq(L.splitAsteroid({x:0,y:0,vx:0,vy:0,r:10,size:1},rng).length,0);
var ch2=L.splitAsteroid({x:0,y:0,vx:10,vy:10,r:18.7,size:2},rng);
T.eq(ch2.length,2);T.eq(ch2[0].size,1);
"""),
("برخورد گلوله، امتیاز و موج", r"""
var s=L.newState(rng);s.asteroids.length=0;s.bullets.length=0;
s.asteroids.push({x:100,y:100,vx:0,vy:0,r:34,size:3});
s.bullets.push({x:100,y:100,vx:0,vy:0,life:1,r:3});
var c=L.collide(s);
T.eq(c.bulletsHit.length,1);T.eq(c.astsHit.length,1);T.ok(!c.shipHit);
s=L.step(s,0.016,{});
T.eq(s.score,20);T.eq(s.bullets.length,0);T.eq(s.asteroids.length,2);T.eq(s.asteroids[0].size,2);
var s2=L.newState(rng);s2.asteroids.length=0;s2.bullets.length=0;
s2.asteroids.push({x:100,y:100,vx:0,vy:0,r:10.3,size:1});
s2.bullets.push({x:100,y:100,vx:0,vy:0,life:1,r:3});
s2=L.step(s2,0.016,{});
T.eq(s2.score,200);T.eq(s2.wave,2);T.eq(s2.asteroids.length,4);
"""),
("شبیه‌سازی ۳۰ ثانیه", r"""
var s=L.newState(rng),i,j;
for(i=0;i<s.asteroids.length;i++){s.asteroids[i].vx=0;s.asteroids[i].vy=0;}
var fired=false;
for(i=0;i<1800;i++){
 s=L.step(s,1/60,{fire:(i%18===0)});
 for(j=0;j<s.asteroids.length;j++){s.asteroids[j].vx=0;s.asteroids[j].vy=0;}
 if(s.bullets.length>0)fired=true;
 if(i%120===0){
  for(j=0;j<s.asteroids.length;j++){var a=s.asteroids[j];T.ok(isFinite(a.x)&&isFinite(a.y),'ast nan');T.ok(a.x>=0&&a.x<s.w&&a.y>=0&&a.y<s.h,'ast wrap');}
  for(j=0;j<s.bullets.length;j++)T.ok(isFinite(s.bullets[j].x)&&isFinite(s.bullets[j].y),'b nan');
  T.ok(isFinite(s.ship.x)&&isFinite(s.ship.y),'ship nan');
  T.ok(s.bullets.length<=8,'bullet cap');}}
T.ok(fired,'bullets fired');T.ok(!s.over,'alive');T.eq(s.lives,3);T.ok(s.score>=0,'score');
T.approx(s.ship.x,240,1e-6);T.approx(s.ship.y,320,1e-6);
"""),
]

INV_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
var W=360,H=560,ROWS=5,COLS=8;
function speedFor(n){return 20+(40-n)*4;}
function gridInto(s){var off=(s.wave-1)*8,r,c;for(r=0;r<ROWS;r++)for(c=0;c<COLS;c++)s.ali.push({x:46+c*36,y:46+r*30+off,r:r,c:c,a:1});}
function newState(wave,rng){var r=rng||Math.random;var s={w:W,h:H,rng:r,wave:wave||1,ali:[],bombs:[],bullets:[],px:W/2,py:H-36,dirn:1,lives:3,score:0,over:false,cool:0,bombT:1.2};gridInto(s);return s;}
function descend(s){var i;for(i=0;i<s.ali.length;i++)if(s.ali[i].a)s.ali[i].y+=12;}
function bombDrop(s,rng){var r=rng||Math.random,idx=[],i;for(i=0;i<s.ali.length;i++)if(s.ali[i].a)idx.push(i);if(!idx.length)return null;var a=s.ali[idx[Math.floor(r()*idx.length)]],b={x:a.x,y:a.y+10,vy:130+15*s.wave};s.bombs.push(b);return b;}
function killAlien(s,idx){var a=s.ali[idx];if(!a||!a.a)return false;a.a=0;s.score+=a.r===0?30:(a.r<3?20:10);return true;}
function playerHit(s){var i;for(i=s.bombs.length-1;i>=0;i--){var b=s.bombs[i];if(Math.abs(b.x-s.px)<15&&Math.abs(b.y-s.py)<15){s.bombs.splice(i,1);s.lives--;if(s.lives<=0)s.over=true;return true;}}return false;}
function reachBottom(s){var i;for(i=0;i<s.ali.length;i++){var a=s.ali[i];if(a.a&&a.y>=s.py-22)return true;}return false;}
function step(s,dt,dir,shooting){if(s.over)return s;var i,j;dir=dir||0;
 s.px+=dir*190*dt;if(s.px<14)s.px=14;if(s.px>s.w-14)s.px=s.w-14;
 s.cool-=dt;
 if(shooting&&s.cool<=0&&s.bullets.length<2){s.bullets.push({x:s.px,y:s.py-12,vy:-320});s.cool=0.4;}
 var alive=0;for(i=0;i<s.ali.length;i++)if(s.ali[i].a)alive++;
 var sp=speedFor(alive)*(1+(s.wave-1)*0.15),minX=1e9,maxX=-1e9;
 for(i=0;i<s.ali.length;i++){var a=s.ali[i];if(!a.a)continue;a.x+=s.dirn*sp*dt;if(a.x<minX)minX=a.x;if(a.x>maxX)maxX=a.x;}
 if(maxX>-1e8){if(s.dirn>0&&maxX>=s.w-22){s.dirn=-1;descend(s);}else if(s.dirn<0&&minX<=22){s.dirn=1;descend(s);}}
 s.bombT-=dt;
 if(s.bombT<=0){bombDrop(s,s.rng);s.bombT=0.6+s.rng()*1.4;}
 for(i=s.bombs.length-1;i>=0;i--){var bo=s.bombs[i];bo.y+=bo.vy*dt;if(bo.y>s.h+10)s.bombs.splice(i,1);}
 for(i=s.bullets.length-1;i>=0;i--){var bl=s.bullets[i];bl.y+=bl.vy*dt;
  if(bl.y<-10){s.bullets.splice(i,1);continue;}
  var hit=-1;for(j=0;j<s.ali.length;j++){var al=s.ali[j];if(al.a&&Math.abs(al.x-bl.x)<15&&Math.abs(al.y-bl.y)<13){hit=j;break;}}
  if(hit>=0){killAlien(s,hit);s.bullets.splice(i,1);}}
 playerHit(s);
 if(reachBottom(s))s.over=true;
 alive=0;for(i=0;i<s.ali.length;i++)if(s.ali[i].a)alive++;
 if(alive===0){s.wave++;s.bombs.length=0;s.bullets.length=0;s.bombT=1.2;s.ali=[];gridInto(s);}
 return s;}
return{newState:newState,step:step,speedFor:speedFor,bombDrop:bombDrop,killAlien:killAlien,playerHit:playerHit,reachBottom:reachBottom};
})();
"""

INV_UI = r"""
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=function(){newGame();};$('#app').appendChild(nb);
var cv=makeCanvas(360,560),ctx=cv.ctx,keys=keyState(),s=null,ended=false;
var best=storeBest('wog-invaders-best')||0;
bindPad([{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'},{k:'Space',label:'شلیک'}]);
$('#hint').textContent='صف بیگانگان را نابود کن؛ به لبه که برسند یک ردیف پایین می‌آیند و با رسیدن به تو می‌بازی.';
function newGame(){s=L.newState(1,Math.random);ended=false;rep();}
function rep(){hud('امتیاز '+fa(s.score)+' · رکورد '+fa(Math.max(best,s.score))+' · جان '+fa(s.lives)+' · موج '+fa(s.wave));}
function draw(){var ivg=ctx.createLinearGradient(0,0,0,560);ivg.addColorStop(0,'#080c1c');ivg.addColorStop(1,'#0e1a26');ctx.fillStyle=ivg;ctx.fillRect(0,0,360,560);ctx.fillStyle='rgba(255,255,255,.2)';for(var iv2=0;iv2<26;iv2++){ctx.fillRect((iv2*97)%360,(iv2*53)%560,1.2,1.2);}var i,a;
 ctx.fillStyle='#3fb8af';
 for(i=0;i<s.ali.length;i++){a=s.ali[i];if(a.a)ctx.fillRect(a.x-12,a.y-7,24,14);}
 ctx.fillStyle='#e26d5c';
 for(i=0;i<s.bombs.length;i++){a=s.bombs[i];ctx.fillRect(a.x-2,a.y-5,4,10);}
 ctx.fillStyle='#d9a441';
 for(i=0;i<s.bullets.length;i++){a=s.bullets[i];ctx.fillRect(a.x-1.5,a.y-6,3,10);}
 if(!s.over)ctx.fillRect(s.px-13,s.py-6,26,12);}
rafStep(function(dt){if(!s)return;
 if(!s.over){var d=0;if(keys['ArrowLeft'])d--;if(keys['ArrowRight'])d++;
  s=L.step(s,Math.min(dt,0.05),d,!!keys['Space']);rep();}
 draw();
 if(s.over&&!ended){ended=true;best=bestOf('wog-invaders-best',s.score);
  ovl(s.lives<=0?'سفینه نابود شد':'بیگانگان فرود آمدند','امتیاز: '+fa(s.score),'بازی دوباره',function(){newGame();});}});
newGame();
"""

INV_TESTS=[
("مارش و گردش در لبه", r"""
var s=L.newState(1,rng);T.eq(s.dirn,1);
var flips=0,guard=0,i;
while(flips<2&&guard<1200){guard++;
 var first=null;for(i=0;i<s.ali.length;i++)if(s.ali[i].a){first=s.ali[i];break;}
 var y0=first.y,d0=s.dirn;
 L.step(s,0.05,0,false);
 if(s.dirn!==d0){flips++;T.eq(s.dirn,-d0,'flip');T.approx(first.y-y0,12,1e-9);}}
T.ok(flips===2,'two flips in '+guard);
"""),
("افزایش سرعت با مرگ بیگانگان", r"""
T.eq(L.speedFor(40),20);T.eq(L.speedFor(1),176);
var n;for(n=1;n<40;n++)T.ok(L.speedFor(n)>L.speedFor(n+1),'mono');
var s=L.newState(1,rng),i,j,dx0=0;
for(i=0;i<60;i++){var mx0=-1e9;for(j=0;j<s.ali.length;j++)if(s.ali[j].a&&s.ali[j].x>mx0)mx0=s.ali[j].x;
 L.step(s,1/60,0,false);
 var mx1=-1e9;for(j=0;j<s.ali.length;j++)if(s.ali[j].a&&s.ali[j].x>mx1)mx1=s.ali[j].x;
 dx0=mx1-mx0;}
L.killAlien(s,0);L.killAlien(s,1);L.killAlien(s,2);
var mxA=-1e9;for(j=0;j<s.ali.length;j++)if(s.ali[j].a&&s.ali[j].x>mxA)mxA=s.ali[j].x;
L.step(s,1/60,0,false);
var mxB=-1e9;for(j=0;j<s.ali.length;j++)if(s.ali[j].a&&s.ali[j].x>mxB)mxB=s.ali[j].x;
T.ok((mxB-mxA)>dx0,'moved faster after kills');
"""),
("بمب بازیکن را می‌کشد", r"""
var s=L.newState(1,rng);
s.bombs.push({x:s.px,y:s.py,vy:0});
T.ok(L.playerHit(s));T.eq(s.lives,2);T.eq(s.bombs.length,0);
s.bombs.push({x:s.px+60,y:s.py,vy:0});
T.ok(!L.playerHit(s));T.eq(s.lives,2);T.eq(s.bombs.length,1);
s.lives=1;s.bombs.push({x:s.px,y:s.py,vy:0});
T.ok(L.playerHit(s));T.ok(s.over);
"""),
("رسیدن به پایین = باخت", r"""
var s=L.newState(1,rng);T.ok(!L.reachBottom(s));
var idx=-1,i;for(i=0;i<s.ali.length;i++)if(s.ali[i].a){idx=i;break;}
T.ok(idx>=0,'alive exists');
s.ali[idx].y=s.py-22;T.ok(L.reachBottom(s));
s=L.step(s,0.016,0,false);T.ok(s.over,'game over');
var s3=L.step(s,0.1,1,true);T.ok(s3.over,'stays over');
"""),
("تشخیص پاک‌سازی موج", r"""
var s=L.newState(1,rng),i,killed=0;
for(i=0;i<40;i++)if(L.killAlien(s,i))killed++;
T.eq(killed,40);T.ok(!L.killAlien(s,0),'no double kill');T.eq(s.score,720);
s=L.step(s,0.016,0,false);
T.eq(s.wave,2);T.eq(s.ali.length,40);
var alive=0;for(i=0;i<s.ali.length;i++)if(s.ali[i].a)alive++;
T.eq(alive,40);T.eq(s.bombs.length,0);T.eq(s.bullets.length,0);
"""),
("شبیه‌سازی ۶۰ ثانیه", r"""
var s=L.newState(1,rng),i,j,over=false;
for(i=0;i<3600;i++){
 var dir=(Math.floor(i/60)%2===0)?-1:1;
 s=L.step(s,1/60,dir,(i%15===0));
 if(i%30===0){
  for(j=0;j<s.ali.length;j++){var a=s.ali[j];T.ok(isFinite(a.x)&&isFinite(a.y),'nan');if(a.a)T.ok(a.x>=10&&a.x<=s.w-10,'x bounds');}
  for(j=0;j<s.bombs.length;j++)T.ok(isFinite(s.bombs[j].y),'bomb nan');
  T.ok(s.bombs.length<=25,'bomb count '+s.bombs.length);
  T.ok(s.bullets.length<=2,'bullet cap');}
 if(s.over){over=true;break;}}
T.ok(isFinite(s.px),'px nan');
T.ok(s.lives>=0&&s.lives<=3,'lives');
T.ok(s.score>=0,'score');
T.eq(s.ali.length,40,'grid size');
if(!over){for(j=0;j<s.ali.length;j++){var a2=s.ali[j];if(a2.a)T.ok(a2.y<s.py-22,'not bottom');}}
"""),
]

DOD_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
var W=360,H=480,PH=11;
function intervalFor(k){var v=1.6-k*0.07;return v<0.45?0.45:v;}
function bounce(b,vx,vy,w,h){var r=b.r||6,x=b.x,y=b.y,nx=vx,ny=vy,hit=0;
 if(x-r<=0&&nx<0){nx=-nx;hit=1;}
 if(x+r>=w&&nx>0){nx=-nx;hit=1;}
 if(y-r<=0&&ny<0){ny=-ny;hit=1;}
 if(y+r>=h&&ny>0){ny=-ny;hit=1;}
 return{x:x,y:y,vx:nx,vy:ny,hit:hit};}
function newState(rng){var r=rng||Math.random;return{w:W,h:H,rng:r,px:W/2,py:H-60,ph:PH,balls:[],spawnT:1.2,spawnCount:0,grace:2,t:0,score:0,over:false};}
function spawnBall(s,r){var side=Math.floor(r()*4),sp=80+r()*90,j=(r()-0.5)*0.8,x,y,ang;
 if(side===0){x=r()*s.w;y=8;ang=Math.PI/2+j;}
 else if(side===1){x=s.w-8;y=r()*s.h;ang=Math.PI+j;}
 else if(side===2){x=r()*s.w;y=s.h-8;ang=-Math.PI/2+j;}
 else{x=8;y=r()*s.h;ang=0+j;}
 s.balls.push({x:x,y:y,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp,r:5+r()*5});}
function hitPlayer(s){if(s.grace>0||s.over)return false;var h=s.ph,i;
 for(i=0;i<s.balls.length;i++){var b=s.balls[i],cx=Math.max(s.px-h,Math.min(b.x,s.px+h)),cy=Math.max(s.py-h,Math.min(b.y,s.py+h)),dx=b.x-cx,dy=b.y-cy;
  if(dx*dx+dy*dy<b.r*b.r)return true;}
 return false;}
function step(s,dt,vx,vy){if(s.over)return s;var i;
 s.t+=dt;s.score=Math.floor(s.t*10);
 if(s.grace>0){s.grace-=dt;if(s.grace<0)s.grace=0;}
 s.px+=vx*dt;s.py+=vy*dt;
 if(s.px<s.ph)s.px=s.ph;if(s.px>s.w-s.ph)s.px=s.w-s.ph;
 if(s.py<s.ph)s.py=s.ph;if(s.py>s.h-s.ph)s.py=s.h-s.ph;
 s.spawnT-=dt;
 if(s.spawnT<=0){spawnBall(s,s.rng);s.spawnCount++;s.spawnT=intervalFor(s.spawnCount);}
 for(i=0;i<s.balls.length;i++){var b=s.balls[i],o=bounce(b,b.vx,b.vy,s.w,s.h);
  b.vx=o.vx;b.vy=o.vy;b.x=o.x+o.vx*dt;b.y=o.y+o.vy*dt;
  if(b.x<b.r)b.x=b.r;if(b.x>s.w-b.r)b.x=s.w-b.r;
  if(b.y<b.r)b.y=b.r;if(b.y>s.h-b.r)b.y=s.h-b.r;}
 if(hitPlayer(s))s.over=true;
 return s;}
return{newState:newState,step:step,bounce:bounce,hitPlayer:hitPlayer,intervalFor:intervalFor};
})();
"""

DOD_UI = r"""
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=function(){newGame();};$('#app').appendChild(nb);
var cv=makeCanvas(360,480),ctx=cv.ctx,keys=keyState(),s=null,ended=false;
var best=storeBest('wog-dodge-best')||0;
var pt={x:180,y:240,on:false};
bindPad([{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'},{k:'ArrowUp',label:'▲'},{k:'ArrowDown',label:'▼'}]);
function setPt(e){var r=cv.cv.getBoundingClientRect();pt.x=(e.clientX-r.left)*cv.w/r.width;pt.y=(e.clientY-r.top)*cv.h/r.height;}
cv.cv.addEventListener('pointerdown',function(e){pt.on=true;setPt(e);});
cv.cv.addEventListener('pointermove',function(e){if(pt.on)setPt(e);});
cv.cv.addEventListener('pointerup',function(){pt.on=false;});
$('#hint').textContent='با کلیدها، دکمه‌ها یا کشیدن انگشت فرار کن؛ هر ثانیه ۱۰ امتیاز و توپ‌ها بیشتر می‌شوند. ۲ ثانیه سپر داری.';
function newGame(){s=L.newState(Math.random);ended=false;rep();}
function rep(){hud('امتیاز '+fa(s.score)+' · رکورد '+fa(Math.max(best,s.score))+' · توپ‌ها '+fa(s.balls.length)+(s.grace>0?' · سپر '+fa(Math.ceil(s.grace)):''));}
function draw(){var ddg=ctx.createLinearGradient(0,0,0,480);ddg.addColorStop(0,'#1a0c14');ddg.addColorStop(1,'#0e101e');ctx.fillStyle=ddg;ctx.fillRect(0,0,360,480);var i,b;
 ctx.fillStyle='#3fb8af';
 for(i=0;i<s.balls.length;i++){b=s.balls[i];ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,6.2832);ctx.fill();}
 if(!s.over){if(s.grace>0){ctx.strokeStyle='#67b98a';ctx.lineWidth=2;ctx.strokeRect(s.px-15,s.py-15,30,30);}
  ctx.fillStyle='#d9a441';ctx.fillRect(s.px-11,s.py-11,22,22);}}
rafStep(function(dt){if(!s)return;
 if(!s.over){var vx=0,vy=0;
  if(keys['ArrowLeft'])vx-=260;if(keys['ArrowRight'])vx+=260;
  if(keys['ArrowUp'])vy-=260;if(keys['ArrowDown'])vy+=260;
  if(vx===0&&vy===0&&pt.on){vx=clamp((pt.x-s.px)*9,-400,400);vy=clamp((pt.y-s.py)*9,-400,400);}
  s=L.step(s,Math.min(dt,0.05),vx,vy);rep();}
 draw();
 if(s.over&&!ended){ended=true;best=bestOf('wog-dodge-best',s.score);
  ovl('برخورد!','امتیاز: '+fa(s.score)+' · '+fa(Math.floor(s.t))+' ثانیه دوام آوردی','بازی دوباره',function(){newGame();});}});
newGame();
"""

DOD_TESTS=[
("بازتاب دقیق از دیوارها", r"""
var r1=L.bounce({x:3,y:100,r:6},-50,25,360,480);T.approx(r1.vx,50,1e-9);T.approx(r1.vy,25,1e-9);T.eq(r1.hit,1);
var r2=L.bounce({x:357,y:100,r:6},40,0,360,480);T.approx(r2.vx,-40,1e-9);T.eq(r2.hit,1);
var r3=L.bounce({x:100,y:4,r:6},0,-20,360,480);T.approx(r3.vy,20,1e-9);T.eq(r3.hit,1);
var r4=L.bounce({x:2,y:3,r:6},-30,-40,360,480);T.approx(r4.vx,30,1e-9);T.approx(r4.vy,40,1e-9);T.eq(r4.hit,1);
var r5=L.bounce({x:180,y:240,r:6},33,44,360,480);T.approx(r5.vx,33,1e-9);T.approx(r5.vy,44,1e-9);T.eq(r5.hit,0);
var r6=L.bounce({x:180,y:477,r:6},0,30,360,480);T.approx(r6.vy,-30,1e-9);T.eq(r6.hit,1);
"""),
("محدودسازی حرکت بازیکن", r"""
var s=L.newState(rng);s.grace=1e9;
L.step(s,2,-1000,0);T.eq(s.px,s.ph);
L.step(s,2,1000,1000);T.eq(s.px,s.w-s.ph);T.eq(s.py,s.h-s.ph);
L.step(s,1,0,-1000);T.eq(s.py,s.ph);
"""),
("کاهش بازهٔ تولید توپ", r"""
T.eq(L.intervalFor(0),1.6);T.eq(L.intervalFor(100),0.45);
var k;for(k=0;k<60;k++)T.ok(L.intervalFor(k+1)<=L.intervalFor(k),'mono');
T.ok(L.intervalFor(10)<L.intervalFor(0),'decreasing');
T.eq(L.intervalFor(17),0.45);
"""),
("سپر آغازین از مرگ جلوگیری می‌کند", r"""
var s=L.newState(rng);
s.balls.push({x:s.px,y:s.py,vx:0,vy:0,r:8});
s=L.step(s,0.016,0,0);T.ok(!s.over,'grace protects');
s.grace=0;s=L.step(s,0.016,0,0);T.ok(s.over,'dies after grace');
"""),
("بازتاب واقعی توپ در بازی", r"""
var s=L.newState(rng);s.grace=1e9;s.spawnT=99;
s.balls.push({x:20,y:240,vx:-100,vy:0,r:6});
var i,flipped=false;
for(i=0;i<12;i++){s=L.step(s,0.05,0,0);
 if(s.balls[0].vx>0)flipped=true;
 T.ok(s.balls[0].x>=0&&s.balls[0].x<=s.w,'in bounds');
 T.ok(isFinite(s.balls[0].x),'nan');}
T.ok(flipped,'reflected');T.ok(s.balls[0].vx>0&&s.balls[0].x>10,'moving away');
"""),
("شبیه‌سازی ۶۰ ثانیه", r"""
var s=L.newState(rng),i,j,overAt=-1;
for(i=0;i<3600;i++){
 var ax=0,ay=0,nn=null,nd=1e18;
 for(j=0;j<s.balls.length;j++){var bb=s.balls[j],ex=s.px-bb.x,ey=s.py-bb.y,d2=ex*ex+ey*ey;
  if(d2<nd){nd=d2;nn=bb;}}
 if(nn&&nd<16900){var dd=Math.sqrt(nd)||1;ax=(s.px-nn.x)/dd*300;ay=(s.py-nn.y)/dd*300;}
 var vx=(180-s.px)*2.2+ax,vy=(300-s.py)*2.2+ay;
 s=L.step(s,1/60,vx,vy);
 if(i%30===0){
  for(j=0;j<s.balls.length;j++){var b=s.balls[j];T.ok(isFinite(b.x)&&isFinite(b.y),'nan');T.ok(b.x>=0&&b.x<=s.w&&b.y>=0&&b.y<=s.h,'bounds');}
  T.ok(isFinite(s.px)&&isFinite(s.py),'p nan');
  T.ok(s.score===Math.floor(s.t*10),'score');}
 if(s.over){overAt=i;break;}}
T.ok(s.balls.length>10,'balls spawned');
if(overAt>=0)T.ok(s.grace<=0,'died only after grace');
"""),
]

GAMES=[
G("asteroids","سیارک‌ها","arcade","🚀","#d9a441","#3fb8af",
  "کشتی را بچرخان، پیشران بگیر و سیارک‌ها را بشکن؛ هر سیارک به دو تکه کوچک‌تر شکافته می‌شود.",
  "چپ/راست چرخش · بالا پیشران · فاصله شلیک · سیارک‌ها در لبه صفحه می‌پیچند",
  logic=AST_LOGIC,ui=AST_UI,css=CSS_ARC,engines=("common","arcade"),tests=AST_TESTS,seed=20260301),
G("invaders","تهاجم فضایی","arcade","👾","#e26d5c","#d9a441",
  "صف ۵×۸ بیگانگان چپ و راست می‌رود و هر بار در لبه پایین‌تر می‌آید؛ هرچه کمتر بمانند تندتر می‌شوند.",
  "چپ/راست حرکت · فاصله شلیک · اگر بیگانه به ردیف تو برسد می‌بازی",
  logic=INV_LOGIC,ui=INV_UI,css=CSS_ARC,engines=("common","arcade"),tests=INV_TESTS,seed=20260302),
G("dodge","دوری از توپ‌ها","arcade","⚪","#3fb8af","#67b98a",
  "توپ‌ها در میدان جهش می‌کنند و شمارشان پیوسته بیشتر می‌شود؛ تا می‌توانی زنده بمان و امتیاز بگیر.",
  "کلیدها، دکمه‌ها یا کشیدن انگشت برای حرکت · برخورد با توپ = پایان (۲ ثانیه سپر آغازین)",
  logic=DOD_LOGIC,ui=DOD_UI,css=CSS_ARC,engines=("common","arcade"),tests=DOD_TESTS,seed=20260303),
]
