# -*- coding: utf-8 -*-
from lib_mini import G

# ----------------------------------------------------------------meteor
meteor_logic = r"""
var WOG_LOGIC=(function(){
var W=480,H=360,PW=52,TOP=H-30,BOT=H-10,PS=260;
function intervalAt(t){return Math.max(0.28,1.1-t*0.011)}
function speedAt(t){return 120+t*2.2}
function newState(rng){rng=rng||Math.random;return{t:0,px:W/2,meteors:[],picks:[],hits:0,shield:0,spawn:0,pickT:4,crystals:0,over:false}}
function inBox(s,m){return Math.abs(m.x-s.px)<=PW/2+m.r&&m.y+m.r>=TOP&&m.y-m.r<=BOT}
function shieldActive(s){return s.shield>0}
function hitShip(s){if(shieldActive(s))return false;for(var i=0;i<s.meteors.length;i++)if(inBox(s,s.meteors[i]))return true;return false}
function collect(s){var n=0;for(var i=s.picks.length-1;i>=0;i--){var p=s.picks[i];if(Math.abs(p.x-s.px)<=PW/2+10&&p.y+10>=TOP&&p.y-10<=BOT){if(p.kind==='s')s.shield=3;else s.crystals++;s.picks.splice(i,1);n++}}return n}
function step(s,dt,dir,rng){rng=rng||Math.random;s.t+=dt;s.px+=dir*PS*dt;if(s.px<PW/2)s.px=PW/2;if(s.px>W-PW/2)s.px=W-PW/2;
 if(!s.over){s.spawn+=dt;var iv=intervalAt(s.t);while(s.spawn>=iv){s.spawn-=iv;s.meteors.push({x:rng()*W,y:-16,r:9+rng()*9,vy:speedAt(s.t)*(0.8+rng()*0.5),vx:(rng()-0.5)*50})}
 s.pickT-=dt;if(s.pickT<=0){s.pickT=6+rng()*3;s.picks.push({x:30+rng()*(W-60),y:-14,vy:110,kind:rng()<0.7?'c':'s'})}}
 var i,m;for(i=s.meteors.length-1;i>=0;i--){m=s.meteors[i];m.x+=m.vx*dt;m.y+=m.vy*dt;if(m.y>H+40||m.x<-70||m.x>W+70)s.meteors.splice(i,1)}
 for(i=s.picks.length-1;i>=0;i--){m=s.picks[i];m.y+=m.vy*dt;if(m.y>H+30)s.picks.splice(i,1)}
 collect(s);
 if(s.shield>0){s.shield-=dt;if(s.shield<0)s.shield=0}
 if(!s.over&&hitShip(s)){var keep=[],k;for(k=0;k<s.meteors.length;k++){var mm=s.meteors[k];if(inBox(s,mm))s.hits++;else keep.push(mm)}s.meteors=keep;if(s.hits>=3)s.over=true}
 return s}
function scoreOf(s){return Math.floor(s.t)*10+s.crystals*25}
return{newState:newState,step:step,hitShip:hitShip,collect:collect,shieldActive:shieldActive,scoreOf:scoreOf,intervalAt:intervalAt,speedAt:speedAt,inBox:inBox,W:W,H:H,PW:PW,TOP:TOP,BOT:BOT}})();
"""

meteor_ui = r"""
var cv=makeCanvas(480,360),ctx=cv.ctx;
var s=L.newState(),ended=false;
function best(v){var k='wog-meteor-best',o=parseInt(store.get(k)||'0',10)||0;if(v>o){o=v;store.set(k,''+v)}return o}
function reset(){s=L.newState();ended=false}
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=reset;$('#app').appendChild(nb);
var keys=keyState();
bindPad([{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'}]);
var stars=[],i;for(i=0;i<40;i++)stars.push({x:Math.random()*L.W,y:Math.random()*(L.H-80),a:0.25+Math.random()*0.6});
$('#hint').textContent='با فلش‌ها یا دکمه‌های لمسی حرکت کن؛ از شهاب‌ها فرار کن، بلور فیروزه‌ای ۲۵+ امتیاز و سپر طلایی ۳ ثانیه محافظت می‌کند. سه برخورد = پایان.';
function render(){var m,i;
 ctx.fillStyle='#0b1226';ctx.fillRect(0,0,L.W,L.H);
 ctx.fillStyle='#d9a441';
 for(i=0;i<stars.length;i++){ctx.globalAlpha=stars[i].a;ctx.fillRect(stars[i].x,stars[i].y,2,2)}
 ctx.globalAlpha=1;
 for(i=0;i<s.picks.length;i++){m=s.picks[i];
  if(m.kind==='s'){ctx.strokeStyle='#d9a441';ctx.lineWidth=2;ctx.beginPath();ctx.arc(m.x,m.y,9,0,6.3);ctx.stroke();ctx.fillStyle='#d9a441';ctx.fillRect(m.x-3,m.y-3,6,6)}
  else{ctx.fillStyle='#3fb8af';ctx.beginPath();ctx.moveTo(m.x,m.y-9);ctx.lineTo(m.x+7,m.y);ctx.lineTo(m.x,m.y+9);ctx.lineTo(m.x-7,m.y);ctx.closePath();ctx.fill()}}
 for(i=0;i<s.meteors.length;i++){m=s.meteors[i];ctx.fillStyle='#e26d5c';ctx.beginPath();ctx.arc(m.x,m.y,m.r,0,6.3);ctx.fill();ctx.fillStyle='#8c3b30';ctx.beginPath();ctx.arc(m.x-m.r*0.3,m.y-m.r*0.3,m.r*0.45,0,6.3);ctx.fill()}
 ctx.fillStyle='#d9a441';ctx.beginPath();ctx.moveTo(s.px,L.BOT-14);ctx.lineTo(s.px-24,L.BOT+8);ctx.lineTo(s.px+24,L.BOT+8);ctx.closePath();ctx.fill();
 if(L.shieldActive(s)&&Math.floor(s.t*8)%2===0){ctx.strokeStyle='#d9a441';ctx.lineWidth=3;ctx.beginPath();ctx.arc(s.px,L.BOT-4,34,0,6.3);ctx.stroke()}
 for(i=0;i<3;i++){ctx.beginPath();ctx.arc(16+i*20,16,7,0,6.3);ctx.fillStyle=i<s.hits?'#e26d5c':'#22304f';ctx.fill()}}
rafStep(function(dt){
 var d=(keys.ArrowLeft||keys.KeyA?-1:0)+(keys.ArrowRight||keys.KeyD?1:0);
 if(!ended){L.step(s,Math.min(dt,0.05),d);
  if(s.over){ended=true;var sc=L.scoreOf(s);best(sc);
   ovl('کشتی سقوط کرد!','امتیاز: '+fa(sc)+' | بلور: '+fa(s.crystals)+' | رکورد: '+fa(best(0)),'بازی جدید',reset)}}
 render();hud('امتیاز: '+fa(L.scoreOf(s))+' | رکورد: '+fa(best(0)))});
"""

meteor_tests = [
("محدودهٔ حرکت کشتی", r"""
var s=L.newState();
for(var i=0;i<300;i++)L.step(s,0.1,1,rng);
T.eq(s.px,L.W-L.PW/2,'clamped to right edge exactly');
for(i=0;i<400;i++)L.step(s,0.1,-1,rng);
T.eq(s.px,L.PW/2,'clamped to left edge exactly');
T.ok(s.px>=L.PW/2&&s.px<=L.W-L.PW/2,'always inside bounds');
"""),
("جعبهٔ برخورد دقیق", r"""
var s=L.newState();s.shield=0;var r=10,mid=(L.TOP+L.BOT)/2;
s.meteors.push({x:s.px+L.PW/2+r,y:mid,r:r});T.ok(L.hitShip(s),'touch from right hits');s.meteors.pop();
s.meteors.push({x:s.px+L.PW/2+r+0.2,y:mid,r:r});T.ok(!L.hitShip(s),'just outside x misses');s.meteors.pop();
s.meteors.push({x:s.px,y:L.TOP-r,r:r});T.ok(L.hitShip(s),'touch from top hits');s.meteors.pop();
s.meteors.push({x:s.px,y:L.TOP-r-0.2,r:r});T.ok(!L.hitShip(s),'just above top misses');s.meteors.pop();
T.ok(!L.hitShip(s),'empty sky no hit');
"""),
("سپر مسدود می‌کند و بعد از ۳ ثانیه می‌گذرد", r"""
var s=L.newState();s.shield=3;
s.meteors.push({x:s.px,y:(L.TOP+L.BOT)/2,r:10});
T.ok(L.shieldActive(s),'shield on');
T.ok(!L.hitShip(s),'blocked while shield active');
L.step(s,0.1,0,rng);
T.eq(s.hits,0,'no hit counted under shield');
T.ok(s.meteors.length===1,'meteor passes through, not removed');
var k=0;while(L.shieldActive(s)&&k<100){L.step(s,0.1,0,rng);k++}
T.ok(k>=29&&k<=31,'shield lasted ~3s, got '+k);
T.eq(s.shield,0,'expired exactly to zero');
s.meteors.push({x:s.px,y:(L.TOP+L.BOT)/2,r:10});
T.ok(L.hitShip(s),'vulnerable after expiry');
"""),
("شیب یکنوای دشواری", r"""
var prev=L.intervalAt(0);
for(var t=1;t<=120;t++){var v=L.intervalAt(t);T.ok(v<=prev+1e-12,'spawn interval non-increasing');prev=v}
T.eq(L.intervalAt(120),0.28,'interval floor reached');
var p2=L.speedAt(0);
for(t=1;t<=120;t++){var v2=L.speedAt(t);T.ok(v2>=p2,'speed non-decreasing');p2=v2}
T.ok(L.speedAt(60)>L.speedAt(30)&&L.speedAt(30)>L.speedAt(0),'speed strictly ramps');
"""),
("جمع‌آوری بلور و سپر", r"""
var s=L.newState();
s.picks.push({x:s.px,y:(L.TOP+L.BOT)/2,vy:0,kind:'c'});
T.eq(L.collect(s),1,'one pickup collected');
T.eq(s.crystals,1,'crystal counted');
T.eq(L.scoreOf(s),25,'crystal worth 25');
s.picks.push({x:s.px,y:(L.TOP+L.BOT)/2,vy:0,kind:'s'});
T.eq(L.collect(s),1,'shield pickup collected');
T.ok(L.shieldActive(s),'shield granted');
T.eq(s.shield,3,'shield is 3 seconds');
T.eq(L.collect(L.newState()),0,'nothing to collect on empty state');
"""),
("شبیه‌سازی ۶۰ ثانیه با ورودی برنامه‌ریزی‌شده", r"""
var s=L.newState(),prev=-1;
for(var i=0;i<3600;i++){var dir=(Math.floor(i/60)%3)-1;L.step(s,1/60,dir,rng);
 var sc=L.scoreOf(s);T.ok(sc>=prev,'score monotonic');prev=sc;
 if(i%60===0){T.ok(s.meteors.length<=40,'meteor count sane: '+s.meteors.length);
  for(var j=0;j<s.meteors.length;j++){var m=s.meteors[j];
   T.ok(isFinite(m.x)&&isFinite(m.y)&&isFinite(m.vy),'no NaN in meteors');
   T.ok(m.y>-40&&m.y<L.H+60&&m.x>-70&&m.x<L.W+70,'meteor in flight zone')}
  T.ok(s.hits>=0&&s.hits<=3,'hits sane');
  T.ok(s.over===(s.hits>=3),'over iff 3 hits');
  T.ok(Math.abs(s.t-(i+1)/60)<1e-6,'t tracks sim time')}}
T.ok(s.crystals>=0,'crystals non-negative');
T.ok(isFinite(s.px)&&isFinite(s.shield),'final state sane');
"""),
]

meteor = G(slug='meteor', title='شهاب‌سنگ', cat='arcade', icon='☄', g1='#d9a441', g2='#e26d5c',
 desc='کشتی تو در پایین صفحه است؛ از ریزش شهاب‌ها فرار کن، بلور بگیر و با سپر زنده بمان.',
 hint='فلش چپ/راست یا دکمه‌های لمسی برای حرکت. امتیاز = ثانیه‌های بقا ×۱۰ + بلورها.',
 logic=meteor_logic, ui=meteor_ui, engines=('common','arcade'), tests=meteor_tests, seed=20251)

# ----------------------------------------------------------------stacker
stacker_logic = r"""
var WOG_LOGIC=(function(){
var W=320,MAXW=110,BONUS=4;
function newState(rng){rng=rng||Math.random;var w=MAXW;return{tower:[{x:(W-w)/2,w:w}],cur:{x:rng()*(W-w),w:w,dir:rng()<0.5?-1:1},phase:'move',combo:0,over:false,side:1}}
function step(s,dt,speed){if(s.phase!=='move')return s;var c=s.cur;c.x+=c.dir*speed*dt;
 if(c.x<=0){c.x=0;c.dir=1}
 if(c.x>=W-c.w){c.x=W-c.w;c.dir=-1}
 return s}
function drop(s){if(s.phase!=='move')return{overlapW:0,perfect:false,over:true};
 var t=s.tower[s.tower.length-1],c=s.cur;
 var oL=Math.max(c.x,t.x),oR=Math.min(c.x+c.w,t.x+t.w),ow=oR-oL;if(ow<0)ow=0;
 if(ow<=0){s.phase='over';s.over=true;return{overlapW:0,perfect:false,over:true}}
 var perfect=ow>=c.w-1e-9,nw,nx;
 if(perfect){nw=Math.min(t.w+BONUS,MAXW);nx=t.x+t.w/2-nw/2;if(nx<0)nx=0;if(nx+nw>W)nx=W-nw;s.combo++}
 else{nw=ow;nx=oL;s.combo=0}
 s.tower.push({x:nx,w:nw});
 s.side=-s.side;
 s.cur={x:s.side>0?0:W-nw,w:nw,dir:s.side>0?1:-1};
 return{overlapW:ow,perfect:perfect,over:false}}
function scoreOf(s){return s.tower.length-1}
return{newState:newState,step:step,drop:drop,scoreOf:scoreOf,W:W,MAXW:MAXW,BONUS:BONUS}})();
"""

stacker_ui = r"""
var cv=makeCanvas(320,440),ctx=cv.ctx,g=cv.cv;
g.style.touchAction='none';
var s=L.newState(),endedShown=false,BH=26;
function best(v){var k='wog-stacker-best',o=parseInt(store.get(k)||'0',10)||0;if(v>o){o=v;store.set(k,''+v)}return o}
function reset(){s=L.newState();endedShown=false}
function drop(){if(s.phase!=='move')return;var r=L.drop(s);
 if(r.perfect)toast('چیدمان کامل! عرض +۴');
 if(r.over&&!endedShown){endedShown=true;var sc=L.scoreOf(s);best(sc);
  ovl('برج افتاد!','ارتفاع: '+fa(sc)+' | رکورد: '+fa(best(0)),'بازی جدید',reset)}}
g.addEventListener('pointerdown',function(){drop()});
var b1=ce('button','wbtn','انداختن');b1.setAttribute('data-smoke','1');b1.onclick=drop;
var b2=ce('button','wbtn','بازی جدید');b2.onclick=reset;
$('#app').appendChild(b1);$('#app').appendChild(b2);
var keys=keyState(),ps=false;
$('#hint').textContent='بلوک خودکار می‌لغزد؛ با لمس بوم، دکمه یا Space رهایش کن. هم‌پوشانی با بالای برج عرض بعدی را می‌سازد و چیدمان کامل ۴+ عرض و زنجیره می‌دهد. خطای کامل = پایان.';
function render(){var i,b;
 ctx.fillStyle='#0b1226';ctx.fillRect(0,0,L.W,440);
 var n=s.tower.length,baseY=416,off=Math.max(0,n-14)*BH;
 for(i=0;i<n;i++){b=s.tower[i];var y=baseY-i*BH+off;if(y<-BH)continue;
  ctx.fillStyle=i===n-1?'#d9a441':(i%2?'#2a3c63':'#3fb8af');
  ctx.fillRect(b.x,y,b.w,BH-2)}
 if(s.phase==='move'){var c=s.cur,y2=baseY-n*BH+off;
  ctx.fillStyle='#d9a441';ctx.fillRect(c.x,y2,c.w,BH-2);
  ctx.fillStyle='#14203a';ctx.fillRect(c.x+c.w/2-2,y2+6,4,BH-14)}
 ctx.fillStyle='#22304f';ctx.fillRect(0,baseY+BH-2,L.W,440-baseY-BH+2)}
rafStep(function(dt){
 if(s.phase==='move')L.step(s,Math.min(dt,0.05),110+s.tower.length*7);
 var sp=keys.Space;if(sp&&!ps)drop();ps=sp;
 render();hud('ارتفاع: '+fa(L.scoreOf(s))+' | رکورد: '+fa(best(0))+' | زنجیره: '+fa(s.combo))});
"""

stacker_tests = [
("ریاضی هم‌پوشانی", r"""
var s=L.newState(rng);s.phase='move';
s.tower=[{x:100,w:80}];s.cur={x:140,w:80,dir:1};
var r=L.drop(s);
T.eq(r.overlapW,40,'overlap exactly 40');
T.ok(!r.perfect&&!r.over,'partial overlap flags');
T.eq(s.tower.length,2,'tower grew by one');
T.eq(s.tower[1].w,40,'new width trimmed to overlap');
T.eq(s.tower[1].x,140,'new block starts at overlap left edge');
T.eq(L.scoreOf(s),1,'score equals height above base');
"""),
("پاداش چیدمان کامل و سقف عرض", r"""
var s=L.newState(rng);s.tower=[{x:100,w:80}];s.combo=0;
for(var i=0;i<10;i++){var t=s.tower[s.tower.length-1];s.cur={x:t.x,w:t.w,dir:1};
 var r=L.drop(s);T.ok(r.perfect,'drop '+(i+1)+' perfect')}
T.eq(s.combo,10,'combo counts perfects');
T.eq(s.tower[s.tower.length-1].w,110,'width capped at MAXW');
var b=s.tower[s.tower.length-1];
T.ok(b.x>=0&&b.x+b.w<=L.W,'grown block stays in bounds');
s.combo=0;s.cur={x:b.x,w:b.w,dir:1};L.drop(s);
T.eq(s.tower[s.tower.length-1].w,110,'stays capped');
T.eq(s.combo,1,'combo keeps counting at cap');
"""),
("برش به هم‌پوشانی", r"""
var s=L.newState(rng);s.phase='move';
s.tower=[{x:100,w:80}];s.cur={x:160,w:80,dir:1};
var r=L.drop(s);
T.eq(r.overlapW,20,'overlap 20');
T.eq(s.tower[1].w,20,'trimmed to 20');
T.eq(s.tower[1].x,160,'kept overlap region only');
T.eq(s.cur.w,20,'next block inherits trimmed width');
"""),
("از دست رفتن کامل = پایان", r"""
var s=L.newState(rng);s.phase='move';
s.tower=[{x:100,w:80}];s.cur={x:220,w:80,dir:1};
var r=L.drop(s);
T.ok(r.over,'full miss is over');
T.eq(r.overlapW,0,'zero overlap');
T.ok(s.over&&s.phase==='over','state marked over');
T.eq(s.tower.length,1,'tower unchanged on miss');
"""),
("جهش در لبه‌ها", r"""
var s=L.newState(rng);s.phase='move';
s.cur={x:0,w:110,dir:-1};
L.step(s,0.016,200);
T.eq(s.cur.x,0,'left edge clamp exact');
T.eq(s.cur.dir,1,'bounces rightward at left edge');
L.step(s,0.016,200);
T.ok(Math.abs(s.cur.x-3.2)<1e-9,'moves after bounce');
s.cur={x:L.W-110,w:110,dir:1};
L.step(s,0.016,200);
T.eq(s.cur.x,L.W-110,'right edge clamp exact');
T.eq(s.cur.dir,-1,'bounces leftward at right edge');
"""),
("شبیه‌سازی ۳۰۰ مرحلهٔ بذردار", r"""
var s=L.newState(rng),drops=0;
for(var i=0;i<300;i++){L.step(s,1/60,140+rng()*40);
 T.ok(s.cur.x>=-1e-9&&s.cur.x<=L.W-s.cur.w+1e-9,'cur always in bounds');
 T.ok(s.cur.dir===1||s.cur.dir===-1,'dir is unit');
 if((i+1)%50===0&&s.phase==='move'){var r=L.drop(s);drops++;
  T.ok(r.overlapW>=0,'overlap non-negative');
  if(r.over)break;
  for(var j=0;j<s.tower.length;j++)T.ok(s.tower[j].w>0&&s.tower[j].w<=L.MAXW,'width in (0,MAXW], got '+s.tower[j].w)}}
T.ok(drops>=2,'several drops happened: '+drops);
T.ok(s.tower.length-1===L.scoreOf(s),'score equals height');
T.eq(s.tower[0].w,L.MAXW,'base block intact');
"""),
]

stacker = G(slug='stacker', title='برج‌ساز', cat='arcade', icon='🧱', g1='#3fb8af', g2='#d9a441',
 desc='بلوک را در لحظهٔ درست رها کن تا برج بلندتر شود؛ چیدمان کامل عرض از دست رفته را برمی‌گرداند.',
 hint='لمس بوم، دکمهٔ انداختن یا Space. هم‌پوشانی = بقا، خطای کامل = پایان.',
 logic=stacker_logic, ui=stacker_ui, engines=('common','arcade'), tests=stacker_tests, seed=20252)

# ----------------------------------------------------------------kite
kite_logic = r"""
var WOG_LOGIC=(function(){
var W=800,H=500,AM={x:330,y:470},AA={x:470,y:470};
var AMIN=0.26,AMAX=Math.PI-0.26,RMIN=70,RMAX=420,EPS=12,KHIT=34;
var WOM=2.4,VRM=280,WOA=1.7,VRA=220,CD=0.7;
function pos(k,a){return{x:a.x+Math.cos(k.ang)*k.rad,y:a.y-Math.sin(k.ang)*k.rad}}
function clampP(ang,rad){if(ang<AMIN)ang=AMIN;if(ang>AMAX)ang=AMAX;if(rad<RMIN)rad=RMIN;if(rad>RMAX)rad=RMAX;return{ang:ang,rad:rad}}
function cross(o,a,b){return(a.x-o.x)*(b.y-o.y)-(a.y-o.y)*(b.x-o.x)}
function onSeg(a,b,p){return Math.min(a.x,b.x)-1e-9<=p.x&&p.x<=Math.max(a.x,b.x)+1e-9&&Math.min(a.y,b.y)-1e-9<=p.y&&p.y<=Math.max(a.y,b.y)+1e-9}
function segIntersect(p1,p2,p3,p4){var d1=cross(p3,p4,p1),d2=cross(p3,p4,p2),d3=cross(p1,p2,p3),d4=cross(p1,p2,p4);
 if(((d1>0&&d2<0)||(d1<0&&d2>0))&&((d3>0&&d4<0)||(d3<0&&d4>0)))return true;
 if(d1===0&&onSeg(p3,p4,p1))return true;
 if(d2===0&&onSeg(p3,p4,p2))return true;
 if(d3===0&&onSeg(p1,p2,p3))return true;
 if(d4===0&&onSeg(p1,p2,p4))return true;
 return false}
function segDist(px,py,x1,y1,x2,y2){var dx=x2-x1,dy=y2-y1,l2=dx*dx+dy*dy;var t=l2?((px-x1)*dx+(py-y1)*dy)/l2:0;t=t<0?0:(t>1?1:t);return Math.hypot(px-(x1+t*dx),py-(y1+t*dy))}
function segOf(k,a){var p=pos(k,a);return[a.x,a.y,p.x,p.y]}
function newState(rng){rng=rng||Math.random;return{me:{ang:Math.PI/2+(rng()-0.5)*0.6,rad:200+rng()*80},ai:{ang:Math.PI/2+(rng()-0.5)*0.6,rad:200+rng()*80},meT:3,aiT:3,cd:0,t:0,over:false,winner:null}}
function checkCut(s){var ms=segOf(s.me,AM),as=segOf(s.ai,AA),ap=pos(s.ai,AA),mp=pos(s.me,AM);
 if(segDist(ap.x,ap.y,ms[0],ms[1],ms[2],ms[3])<EPS)return'me';
 if(segDist(mp.x,mp.y,as[0],as[1],as[2],as[3])<EPS)return'ai';
 return null}
function move(k,des,om,vr,dt){var da=des.ang-k.ang,m=om*dt;if(da>m)da=m;if(da<-m)da=-m;k.ang+=da;
 var dr=des.rad-k.rad,m2=vr*dt;if(dr>m2)dr=m2;if(dr<-m2)dr=-m2;k.rad+=dr}
function step(s,dt,target){if(s.over)return s;s.t+=dt;if(s.cd>0)s.cd=Math.max(0,s.cd-dt);
 var pm=pos(s.me,AM);
 if(target){var des=clampP(Math.atan2(AM.y-target.y,target.x-AM.x),Math.hypot(target.x-AM.x,AM.y-target.y));move(s.me,des,WOM,VRM,dt)}
 var mp=pos(s.me,AM);
 var attack=Math.sin(s.t*0.7+1.3)>-0.2,tx,ty;
 if(attack){tx=(AM.x+mp.x)/2+Math.sin(s.t*2.3)*40;ty=(AM.y+mp.y)/2+Math.cos(s.t*1.9)*30}
 else{tx=W/2+Math.sin(s.t*0.5)*200;ty=H*0.42+Math.cos(s.t*0.8)*80}
 var desA=clampP(Math.atan2(AA.y-ty,tx-AA.x),Math.hypot(tx-AA.x,AA.y-ty));
 var pa=pos(s.ai,AA);
 move(s.ai,desA,WOA,VRA,dt);
 var ap=pos(s.ai,AA),ms=segOf(s.me,AM),as=segOf(s.ai,AA);
 if(s.cd<=0){
  var iCut=segDist(mp.x,mp.y,as[0],as[1],as[2],as[3])<EPS||segIntersect(pm,mp,{x:AA.x,y:AA.y},ap);
  var aCut=segDist(ap.x,ap.y,ms[0],ms[1],ms[2],ms[3])<EPS||segIntersect(pa,ap,{x:AM.x,y:AM.y},mp);
  var ev=null;
  if(Math.hypot(mp.x-ap.x,mp.y-ap.y)<KHIT)ev='hit';
  else if(iCut)ev='cutthem';
  else if(aCut)ev='cutme';
  if(ev==='hit'){s.meT--;s.cd=CD}
  else if(ev==='cutthem'){s.aiT--;s.cd=CD}
  else if(ev==='cutme'){s.meT--;s.cd=CD}
  if(s.aiT<=0){s.over=true;s.winner='me'}
  else if(s.meT<=0){s.over=true;s.winner='ai'}}
 return s}
function tension(s){return{me:s.meT,ai:s.aiT}}
return{newState:newState,step:step,checkCut:checkCut,tension:tension,segIntersect:segIntersect,segDist:segDist,pos:pos,clampP:clampP,AM:AM,AA:AA,AMIN:AMIN,AMAX:AMAX,RMIN:RMIN,RMAX:RMAX,EPS:EPS,KHIT:KHIT}})();
"""

kite_ui = r"""
var cv=makeCanvas(800,500),ctx=cv.ctx,g=cv.cv;
g.style.touchAction='none';g.style.maxWidth='100%';g.style.height='auto';
var s=L.newState(),ended=false,target={x:400,y:250};
function reset(){s=L.newState();ended=false;target={x:400,y:250}}
function toXY(e){var r=g.getBoundingClientRect();return{x:(e.clientX-r.left)*L.W/r.width,y:(e.clientY-r.top)*500/r.height}}
g.addEventListener('pointermove',function(e){target=toXY(e)});
g.addEventListener('pointerdown',function(e){target=toXY(e)});
var keys=keyState();
bindPad([{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'},{k:'ArrowUp',label:'▲'},{k:'ArrowDown',label:'▼'}]);
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=reset;$('#app').appendChild(nb);
$('#hint').textContent='نشانگر را روی بوم حرکت بده (یا فلش‌ها/دکمه‌ها)؛ حریف رشتهٔ تو را نشانه می‌گیرد. بادبادکت را از روی رشتهٔ او عبور بده تا پاره شود؛ سه برش برد است. برخورد بدنه‌ها به ضرر توست.';
function drawKite(x,y,col){ctx.fillStyle=col;ctx.beginPath();ctx.moveTo(x,y-16);ctx.lineTo(x+11,y);ctx.lineTo(x,y+20);ctx.lineTo(x-11,y);ctx.closePath();ctx.fill();
 ctx.strokeStyle=col;ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(x,y+20);ctx.lineTo(x+3,y+30);ctx.lineTo(x-2,y+38);ctx.stroke()}
function render(){var mp=L.pos(s.me,L.AM),ap=L.pos(s.ai,L.AA),i;
 ctx.fillStyle='#0b1226';ctx.fillRect(0,0,L.W,500);
 ctx.strokeStyle='#1d2b4a';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(0,470);ctx.lineTo(L.W,470);ctx.stroke();
 ctx.strokeStyle='#3fb8af';ctx.beginPath();ctx.moveTo(L.AM.x,L.AM.y);ctx.lineTo(mp.x,mp.y);ctx.stroke();
 ctx.strokeStyle='#e26d5c';ctx.beginPath();ctx.moveTo(L.AA.x,L.AA.y);ctx.lineTo(ap.x,ap.y);ctx.stroke();
 ctx.fillStyle='#8fa3c8';ctx.fillRect(L.AM.x-8,462,16,8);ctx.fillRect(L.AA.x-8,462,16,8);
 ctx.strokeStyle='#3fb8af';ctx.beginPath();ctx.arc(target.x,target.y,6,0,6.3);ctx.stroke();
 drawKite(mp.x,mp.y,'#d9a441');drawKite(ap.x,ap.y,'#e26d5c');
 for(i=0;i<3;i++){ctx.beginPath();ctx.arc(24+i*22,20,8,0,6.3);ctx.fillStyle=i<s.meT?'#67b98a':'#22304f';ctx.fill()}
 for(i=0;i<3;i++){ctx.beginPath();ctx.arc(L.W-24-i*22,20,8,0,6.3);ctx.fillStyle=i<s.aiT?'#e26d5c':'#22304f';ctx.fill()}}
rafStep(function(dt){
 var sp=200;
 if(keys.ArrowLeft||keys.KeyA)target.x-=sp*dt;
 if(keys.ArrowRight||keys.KeyD)target.x+=sp*dt;
 if(keys.ArrowUp||keys.KeyW)target.y-=sp*dt;
 if(keys.ArrowDown||keys.KeyS)target.y+=sp*dt;
 target.x=Math.max(0,Math.min(L.W,target.x));target.y=Math.max(0,Math.min(500,target.y));
 if(!ended){L.step(s,Math.min(dt,0.05),target);
  if(s.over){ended=true;var win=s.winner==='me';
   if(win){var w=(parseInt(store.get('wog-kite-wins')||'0',10)||0)+1;store.set('wog-kite-wins',''+w)}
   ovl(win?'بردی!':'باختی!',win?'رشتهٔ حریف سه بار پاره شد.':'رشتهٔ تو پاره شد؛ دوباره تلاش کن.','بازی جدید',reset)}}
 render();
 hud('برش‌های تو: '+fa(3-s.aiT)+' | آسیب حریف: '+fa(3-s.meT)+' | بردها: '+fa(parseInt(store.get('wog-kite-wins')||'0',10)||0))});
"""

kite_tests = [
("تقاطع پاره‌خط‌ها", r"""
T.ok(L.segIntersect({x:0,y:0},{x:10,y:10},{x:0,y:10},{x:10,y:0}),'X crossing');
T.ok(!L.segIntersect({x:0,y:0},{x:10,y:0},{x:0,y:5},{x:10,y:5}),'parallel no cross');
T.ok(L.segIntersect({x:0,y:0},{x:10,y:0},{x:10,y:0},{x:10,y:10}),'touching endpoint counts');
T.ok(!L.segIntersect({x:0,y:0},{x:1,y:1},{x:5,y:5},{x:6,y:0}),'disjoint segments');
T.ok(L.segIntersect({x:0,y:0},{x:10,y:0},{x:5,y:0},{x:15,y:0}),'collinear overlap counts');
T.ok(!L.segIntersect({x:0,y:0},{x:10,y:0},{x:20,y:0},{x:30,y:0}),'collinear apart');
"""),
("محدودیت زاویه و شعاع حول لنگر", r"""
var s=L.newState(rng),hi={x:L.AM.x-900,y:L.AM.y-200},lo={x:L.AM.x+900,y:L.AM.y+400};
s.meT=99;s.aiT=99;
for(var i=0;i<80;i++){L.step(s,0.05,lo);
 T.ok(s.me.ang>=L.AMIN-1e-9&&s.me.ang<=L.AMAX+1e-9,'angle always in range');
 T.ok(s.me.rad>=L.RMIN-1e-9&&s.me.rad<=L.RMAX+1e-9,'radius always in range')}
T.ok(Math.abs(s.me.ang-L.AMIN)<1e-6,'converges to min angle');
T.ok(Math.abs(s.me.rad-L.RMAX)<1e-6,'converges to max radius');
for(i=0;i<80;i++)L.step(s,0.05,hi);
T.ok(Math.abs(s.me.ang-L.AMAX)<1e-6,'converges to max angle');
T.ok(Math.abs(s.me.rad-L.RMAX)<1e-6,'radius capped at max');
"""),
("برش رشتهٔ حریف (سناریوی برنامه‌ریزی‌شده)", r"""
var s=L.newState(rng);
s.ai={ang:Math.PI/2,rad:200};
s.me={ang:Math.atan2(150,110),rad:Math.hypot(110,150)};
s.t=5;s.cd=0;
var found=false;
for(var i=0;i<80&&!found;i++){L.step(s,0.02,{x:520,y:350});
 if(L.checkCut(s)==='ai')found=true}
T.ok(found,'my kite sweeping across AI string registers cut');
T.eq(s.aiT,2,'AI lost exactly one tension');
T.ok(s.cd>0,'cut cooldown engaged');
for(i=0;i<60;i++)L.step(s,0.02,{x:200,y:300});
T.eq(L.tension(s).ai,2,'no extra cuts after flying away');
T.eq(L.tension(s).me,3,'player unharmed while away');
"""),
("حریف رشتهٔ مرا می‌بُرد", r"""
var s=L.newState(rng);
s.me={ang:Math.PI/2,rad:220};
var target={x:330,y:250},cutme=false;
for(var i=0;i<150;i++){L.step(s,0.02,target);
 if(s.meT<3){cutme=true;break}}
T.ok(cutme,'AI swoop cut my string within 3s');
T.eq(s.meT,2,'exactly one cut (cooldown works)');
T.eq(L.tension(s).me,2,'tension reflects the cut');
T.eq(L.tension(s).ai,3,'AI untouched while I hold still');
T.ok(!s.over,'match continues');
"""),
("برخورد بدنه و checkCut مستقیم", r"""
var s=L.newState(rng);
s.me={ang:1.2,rad:200};
s.ai={ang:Math.atan2(186.5,-68),rad:Math.hypot(68,186.5)};
L.step(s,0.02,null);
T.eq(s.meT,2,'kite body contact costs me tension');
T.eq(s.aiT,3,'body hit is not a cut for AI');
T.ok(s.cd>0,'cooldown after body hit');
T.eq(L.checkCut(s),'me','AI kite sitting on my string reports me');
var s2=L.newState(rng);s2.me={ang:2.4,rad:150};s2.ai={ang:0.7,rad:150};
T.eq(L.checkCut(s2),null,'kites apart: no cut');
var s3=L.newState(rng);s3.ai={ang:Math.PI/2,rad:200};s3.me={ang:Math.atan2(170,140),rad:Math.hypot(140,170)};
T.eq(L.checkCut(s3),'ai','my kite on AI string reports ai');
"""),
("شبیه‌سازی ۶۰ ثانیهٔ بذردار", r"""
var s=L.newState(rng);
for(var i=0;i<3600&&!s.over;i++){var a=i/60;
 var target={x:330+Math.cos(a*0.9)*280,y:470-Math.abs(Math.sin(a*0.6))*330-30};
 L.step(s,1/60,target);
 if(i%30===0){
  T.ok(s.me.ang>=L.AMIN-1e-9&&s.me.ang<=L.AMAX+1e-9,'my angle in range');
  T.ok(s.ai.ang>=L.AMIN-1e-9&&s.ai.ang<=L.AMAX+1e-9,'ai angle in range');
  T.ok(s.me.rad>=L.RMIN-1e-9&&s.me.rad<=L.RMAX+1e-9,'my radius in range');
  T.ok(s.ai.rad>=L.RMIN-1e-9&&s.ai.rad<=L.RMAX+1e-9,'ai radius in range');
  T.ok(s.meT>=0&&s.meT<=3&&s.aiT>=0&&s.aiT<=3,'tensions sane');
  T.ok(isFinite(s.me.ang+s.me.rad+s.ai.ang+s.ai.rad+s.t),'no NaN')}}
T.ok(i>60,'sim ran a while: '+i);
if(s.over)T.ok(s.winner==='me'||s.winner==='ai','winner set on over');
var tn=L.tension(s);
T.ok(tn.me>=0&&tn.ai>=0,'tensions non-negative at end');
"""),
]

kite = G(slug='kite', title='جنگ بادبادک', cat='arcade', icon='🪁', g1='#d9a441', g2='#3fb8af',
 desc='نبرد بادبادک‌ها: با عبور بادبادکت رشتهٔ حریف را پاره کن و نگذار رشتهٔ خودت بریده شود.',
 hint='نشانگر یا فلش‌ها برای پرواز؛ سه برش برد، برخورد بدنه‌ها به ضرر توست.',
 logic=kite_logic, ui=kite_ui, engines=('common','arcade'), tests=kite_tests, seed=20253)

GAMES = [meteor, stacker, kite]
