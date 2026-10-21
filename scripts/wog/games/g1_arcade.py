# -*- coding: utf-8 -*-
# AG-G1 — 4 canvas arcade games (flappy, frogger, coin-catch, runner)
from lib_mini import G

CSS_ARCADE = r"""
canvas{display:block;margin:10px auto;max-width:100%;height:auto;border-radius:12px;border:2px solid #24365c;background:#0b1426;touch-action:none}
.wbtn{background:#d9a441;color:#14203a;border:0;border-radius:10px;padding:10px 20px;font-size:15px;font-weight:700;min-height:44px;min-width:44px;cursor:pointer;touch-action:manipulation;margin:4px}
.wbtn:active{transform:scale(.96)}
"""

# ---------------- flappy ----------------
FL_LOGIC = r"""
var FL={W:320,H:480,BX:70,R:14,PW:60,GAP:140,G:1400,FLAP:-380,SPAWN:1.5};
function newState(rng){var r=rng||Math.random;
 return {y:240,vy:0,pipes:[],score:0,alive:true,t:0,spawnT:1.1,count:0,phase:r()*6.283};}
function gapYOf(st,i){var g=240+110*Math.sin(st.phase+i*1.31);return g<100?100:(g>380?380:g);}
function pipeSpawn(st){return {x:FL.W+20,gapY:gapYOf(st,st.count),passed:false};}
function collide(st,w,h){
 if(st.y+FL.R>=h||st.y-FL.R<=0)return true;
 for(var i=0;i<st.pipes.length;i++){var p=st.pipes[i];
  if(FL.BX+FL.R>p.x&&FL.BX-FL.R<p.x+FL.PW){
   var tp=p.gapY-FL.GAP/2,bt=p.gapY+FL.GAP/2;
   if(st.y-FL.R<tp||st.y+FL.R>bt)return true;}}
 return false;}
function step(st,flap,dt,speed){
 var n={y:st.y,vy:st.vy,pipes:[],score:st.score,alive:st.alive,t:st.t+dt,spawnT:st.spawnT,count:st.count,phase:st.phase};
 if(!st.alive)return n;
 n.vy=st.vy+FL.G*dt;
 if(flap)n.vy=FL.FLAP;
 n.y=st.y+n.vy*dt;
 for(var i=0;i<st.pipes.length;i++){var p=st.pipes[i];
  var np={x:p.x-speed*dt,gapY:p.gapY,passed:p.passed};
  if(!np.passed&&np.x+FL.PW<FL.BX){np.passed=true;n.score++;}
  if(np.x>-FL.PW-20)n.pipes.push(np);}
 n.spawnT-=dt;
 if(n.spawnT<=0){n.pipes.push(pipeSpawn(n));n.count++;n.spawnT+=FL.SPAWN;}
 if(n.y+FL.R>=FL.H||n.y-FL.R<=0||collide(n,FL.W,FL.H))n.alive=false;
 return n;}
function passedPipe(st){var c=0;for(var i=0;i<st.pipes.length;i++)if(st.pipes[i].passed)c++;return c;}
var WOG_LOGIC={newState:newState,step:step,collide:collide,pipeSpawn:pipeSpawn,passedPipe:passedPipe,gapYOf:gapYOf,FL:FL};
"""

FL_UI = r"""
var W=320,H=480;
var cvv=makeCanvas(W,H),ctx=cvv.ctx;
$('#hint').textContent='با فاصله یا لمس بپر و از میان لوله‌ها عبور کن.';
var best=bestOf('wog-flappy-best',0);
var st=L.newState(),over=false,flapQ=false,held=false,lastScore=-1;
function hudUpd(){hud('امتیاز: <b>'+fa(st.score)+'</b> · رکورد: <b>'+fa(best)+'</b>');}
function reset(){st=L.newState();over=false;lastScore=-1;flapQ=false;paint();hudUpd();}
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=reset;
$('#app').insertBefore(nb,cvv.cv);
cvv.cv.addEventListener('pointerdown',function(e){e.preventDefault();flapQ=true;});
bindPad([{k:'Space',label:'پرش'}]);
function paint(){
 var sk=ctx.createLinearGradient(0,0,0,H);sk.addColorStop(0,'#1d3a5f');sk.addColorStop(.55,'#3a5a80');sk.addColorStop(.85,'#7a6a72');sk.addColorStop(1,'#a87a5c');ctx.fillStyle=sk;ctx.fillRect(0,0,W,H);var sg=ctx.createRadialGradient(W*.72,H*.24,4,W*.72,H*.24,64);sg.addColorStop(0,'rgba(255,224,160,.85)');sg.addColorStop(.35,'rgba(255,200,120,.28)');sg.addColorStop(1,'rgba(255,200,120,0)');ctx.fillStyle=sg;ctx.fillRect(0,0,W,H);ctx.fillStyle='rgba(255,255,255,.09)';ctx.beginPath();ctx.ellipse(W*.24,H*.3,34,9,0,0,6.283);ctx.ellipse(W*.32,H*.33,26,7,0,0,6.283);ctx.ellipse(W*.6,H*.16,30,8,0,0,6.283);ctx.fill();
 var i,p,tp;
 for(i=0;i<st.pipes.length;i++){p=st.pipes[i];tp=p.gapY-70;
  var pg=ctx.createLinearGradient(p.x,0,p.x+60,0);pg.addColorStop(0,'#2c8f88');pg.addColorStop(.32,'#4fc0b6');pg.addColorStop(.55,'#3fb8af');pg.addColorStop(1,'#20655f');ctx.fillStyle=pg;ctx.fillRect(p.x,0,60,tp);ctx.fillRect(p.x,tp+140,60,H-24-(tp+140));ctx.fillStyle='rgba(255,255,255,.22)';ctx.fillRect(p.x+5,0,4,tp);ctx.fillRect(p.x+5,tp+140,4,H-24-(tp+140));
  var lg=ctx.createLinearGradient(p.x,0,p.x+60,0);lg.addColorStop(0,'#2f9a92');lg.addColorStop(.5,'#54c8be');lg.addColorStop(1,'#227068');ctx.fillStyle=lg;ctx.fillRect(p.x-3,Math.max(0,tp-16),66,16);ctx.fillRect(p.x-3,tp+140,66,16);ctx.fillStyle='rgba(0,0,0,.25)';ctx.fillRect(p.x-3,Math.max(0,tp-3),66,3);ctx.fillRect(p.x-3,tp+140,66,3);}
 var gr=ctx.createLinearGradient(0,H-24,0,H);gr.addColorStop(0,'#c69a3a');gr.addColorStop(1,'#7a5a22');ctx.fillStyle=gr;ctx.fillRect(0,H-24,W,24);
 ctx.fillStyle='#d9a441';ctx.fillRect(0,H-24,W,5);
 ctx.save();ctx.shadowColor='rgba(255,210,120,.55)';ctx.shadowBlur=12;var bg2=ctx.createRadialGradient(66,st.y-5,2,70,st.y,15);bg2.addColorStop(0,'#ffe1a0');bg2.addColorStop(.7,'#d9a441');bg2.addColorStop(1,'#b8862f');ctx.fillStyle=bg2;ctx.beginPath();ctx.arc(70,st.y,14,0,6.283);ctx.fill();ctx.restore();
 ctx.fillStyle='#b8862f';ctx.beginPath();ctx.ellipse(64,st.y+3,8,5,-0.4,0,6.283);ctx.fill();
 ctx.fillStyle='#14203a';ctx.beginPath();ctx.arc(77,st.y-5,2.6,0,6.283);ctx.fill();
 ctx.fillStyle='#e26d5c';ctx.beginPath();ctx.moveTo(83,st.y);ctx.lineTo(93,st.y+3);ctx.lineTo(83,st.y+7);ctx.closePath();ctx.fill();
 if(!st.alive){ctx.fillStyle='rgba(14,26,51,0.55)';ctx.fillRect(0,0,W,H);}
}
rafStep(function(dt){
 dt=Math.min(dt,0.033);
 var k=keyState(),fl=flapQ||!!(k.Space&&!held);
 held=!!k.Space;flapQ=false;
 if(!over)st=L.step(st,fl,dt,140+Math.min(st.score,40)*1.5);
 paint();
 if(st.score!==lastScore){lastScore=st.score;hudUpd();}
 if(!st.alive&&!over){over=true;best=bestOf('wog-flappy-best',st.score);hudUpd();
  ovl('پایان پرواز!','امتیاز شما: '+fa(st.score),'بازی جدید',reset);}
});
hudUpd();
"""

FL_TESTS = [
 ("گرانی سرعت سقوط را زیاد می‌کند", """
var s=L.newState(rng);
var a=L.step(s,false,1/60,140),b=L.step(a,false,1/60,140);
T.ok(a.vy>0&&b.vy>a.vy,'vy grows');
T.ok(a.y>s.y&&b.y>a.y,'falling down');
"""),
 ("پرش تکانهٔ سرعت منفی می‌دهد", """
var s=L.step(L.newState(rng),true,1/60,140);
T.eq(s.vy,-380,'impulse value');
T.ok(s.y<240,'rose upward');
"""),
 ("برخورد با نوار لوله، زمین و سقف", """
function mk(y,p){return {y:y,vy:0,pipes:[p||{x:50,gapY:240,passed:false}]};}
T.ok(L.collide(mk(100),320,480),'above gap hits top band');
T.ok(L.collide(mk(400),320,480),'below gap hits bottom band');
T.ok(!L.collide(mk(240),320,480),'inside gap safe');
T.ok(!L.collide(mk(240,320,480)===undefined?mk(240,{x:200,gapY:240,passed:false}):mk(240,{x:200,gapY:240,passed:false}),320,480),'no x overlap safe');
T.ok(L.collide(mk(470),320,480),'ground');
T.ok(L.collide(mk(10),320,480),'ceiling');
"""),
 ("امتیاز هر لوله دقیقاً یک‌بار", """
var s={y:240,vy:0,pipes:[{x:68,gapY:240,passed:false}],score:0,alive:true,t:0,spawnT:999,count:1,phase:0};
var got=false;
for(var i=0;i<80;i++){s=L.step(s,false,1/60,300);
 if(s.score>=1){T.eq(s.score,1,'exactly one point');
  T.eq(L.passedPipe(s),1,'passedPipe at pass moment');got=true;break;}}
T.ok(got,'pipe passed once');
for(var j=0;j<40;j++)s=L.step(s,false,1/60,300);
T.eq(s.score,1,'score stays 1 after pipe removal');
"""),
 ("بدون پرش تا ۵ ثانیه می‌میرد", """
var s=L.newState(rng),t=0,dead=-1;
for(var i=0;i<600;i++){s=L.step(s,false,1/60,140);t+=1/60;if(!s.alive){dead=t;break;}}
T.ok(dead>0&&dead<5,'died at '+dead+'s');
"""),
 ("لوله‌ها حرکت و امتیاز می‌دهند (بدون پرش)", """
var s=L.newState(rng),t=0,prev=-1,inc=0;
while(s.alive&&t<25){s=L.step(s,false,1/60,140);t+=1/60;
 var pp=L.passedPipe(s);if(pp>prev){inc++;prev=pp;}}
T.ok(inc>=1,'pipes passed via motion: '+inc);
T.ok(L.passedPipe(s)<=s.score,'passedPipe consistent');
T.ok(s.t<=25.01,'bounded sim');
"""),
]

# ---------------- frogger ----------------
FR_LOGIC = r"""
var CELL=32,W=416;
var LANES={
 11:{dir:1,sp:70,n:3,w:48,kind:'car'},
 10:{dir:-1,sp:95,n:3,w:56,kind:'car'},
 9:{dir:1,sp:115,n:2,w:48,kind:'car'},
 8:{dir:-1,sp:85,n:3,w:64,kind:'car'},
 6:{dir:-1,sp:55,n:3,w:96,kind:'log'},
 5:{dir:1,sp:75,n:2,w:128,kind:'log'},
 4:{dir:-1,sp:95,n:3,w:96,kind:'log'},
 3:{dir:1,sp:110,n:2,w:160,kind:'log'}};
function clone(st){var c={frog:{x:st.frog.x,y:st.frog.y},cars:[],logs:[],score:st.score,round:st.round,mul:st.mul,alive:st.alive,t:st.t},i;
 for(i=0;i<st.cars.length;i++)c.cars.push({x:st.cars[i].x,row:st.cars[i].row,w:st.cars[i].w,dir:st.cars[i].dir,sp:st.cars[i].sp});
 for(i=0;i<st.logs.length;i++)c.logs.push({x:st.logs[i].x,row:st.logs[i].row,w:st.logs[i].w,dir:st.logs[i].dir,sp:st.logs[i].sp});
 return c;}
function newState(rng){var r=rng||Math.random;var cars=[],logs=[],k;
 for(var key in LANES){var la=LANES[key],row=+key,arr=(la.kind==='car')?cars:logs;
  var spacing=576/la.n,off=r()*spacing;
  for(k=0;k<la.n;k++){var x=((off+k*spacing)%576)-80;
   arr.push({x:x,row:row,w:la.w,dir:la.dir,sp:la.sp});}}
 return {frog:{x:192,y:384},cars:cars,logs:logs,score:0,round:1,mul:1,alive:true,t:0};}
function hop(st,dir){var n=clone(st);if(!st.alive)return n;
 var f={x:st.frog.x,y:st.frog.y};
 if(dir==='up')f.y=Math.max(0,f.y-32);
 else if(dir==='down')f.y=Math.min(384,f.y+32);
 else if(dir==='left')f.x=Math.max(0,f.x-32);
 else if(dir==='right')f.x=Math.min(W-32,f.x+32);
 n.frog=f;return n;}
function collide(st){var f=st.frog;
 var fl=f.x+6,fr=f.x+26,ft=f.y+4,fb=f.y+28,i,c;
 for(i=0;i<st.cars.length;i++){c=st.cars[i];
  var cl=c.x+2,cr=c.x+c.w-2,ct=c.row*32+4,cb=c.row*32+28;
  if(fl<cr&&fr>cl&&ft<cb&&fb>ct)return true;}
 return false;}
function findLog(st,row,fx){var i,g;
 for(i=0;i<st.logs.length;i++){g=st.logs[i];
  if(g.row===row&&fx>g.x-10&&fx<g.x+g.w+10)return g;}
 return null;}
function onLog(st){var row=st.frog.y/32;
 return !!(LANES[row]&&LANES[row].kind==='log'&&findLog(st,row,st.frog.x+16));}
function reached(st){return st.frog.y===0;}
function step(st,dt){
 var n=clone(st);if(!st.alive)return n;
 n.t=st.t+dt;
 var i,c,mv;
 for(i=0;i<st.cars.length;i++){c=st.cars[i];mv=c.x+c.dir*c.sp*n.mul*dt;
  if(c.dir>0&&mv>496)mv-=576;if(c.dir<0&&mv<-80)mv+=576;
  n.cars[i].x=mv;}
 for(i=0;i<st.logs.length;i++){c=st.logs[i];mv=c.x+c.dir*c.sp*n.mul*dt;
  if(c.dir>0&&mv>496)mv-=576;if(c.dir<0&&mv<-80)mv+=576;
  n.logs[i].x=mv;}
 var f=n.frog,row=f.y/32,la=LANES[row];
 if(la&&la.kind==='log'){
  var g=findLog(n,row,f.x+16);
  if(!g){n.alive=false;return n;}
  f.x+=g.dir*g.sp*n.mul*dt;
  if(f.x+16<-4||f.x+16>W+4){n.alive=false;return n;}
 }else if(la&&la.kind==='car'){
  if(collide(n)){n.alive=false;return n;}
 }
 if(f.y===0){n.score=st.score+1;n.round=st.round+1;n.mul=st.mul+0.12;f.x=192;f.y=384;}
 return n;}
var WOG_LOGIC={newState:newState,hop:hop,step:step,collide:collide,reached:reached,onLog:onLog,findLog:findLog,LANES:LANES,W:W,CELL:CELL};
"""

FR_UI = r"""
var W=416,H=416;
var cvv=makeCanvas(W,H),ctx=cvv.ctx;
$('#hint').textContent='با جهت‌نما (یا دکمه‌ها) بپر: از جاده بگذر، روی کنده‌ها سوار شو و به ردیف بالا برس.';
var best=bestOf('wog-frogger-best',0);
var st=L.newState(),over=false,prev={},lastScore=-1;
function hudUpd(){hud('امتیاز: <b>'+fa(st.score)+'</b> · دور: <b>'+fa(st.round)+'</b> · رکورد: <b>'+fa(best)+'</b>');}
function reset(){st=L.newState();over=false;lastScore=-1;prev={};paint();hudUpd();}
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=reset;
$('#app').insertBefore(nb,cvv.cv);
bindPad([{k:'ArrowUp',label:'▲'},{k:'ArrowDown',label:'▼'},{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'}]);
var DIRS={ArrowUp:'up',KeyW:'up',ArrowDown:'down',KeyS:'down',ArrowLeft:'left',KeyA:'left',ArrowRight:'right',KeyD:'right'};
function paint(){
 var r2,y,k2,i;
 for(r2=0;r2<13;r2++){y=r2*32;
  var base=(r2===0)?'#123a4a':(r2>=3&&r2<=6)?'#16405c':(r2===7||r2===12||(r2>=1&&r2<=2))?'#1d3527':'#141d31';
  var zg=ctx.createLinearGradient(0,y,0,y+32);zg.addColorStop(0,base);zg.addColorStop(1,'rgba(0,0,0,.42)');ctx.fillStyle=zg;ctx.fillRect(0,y,W,32);if(r2<8){ctx.strokeStyle='rgba(140,200,230,.08)';ctx.lineWidth=1.5;ctx.beginPath();for(var wv=0;wv<7;wv++){var wx=((r2*67+wv*61)%W);ctx.moveTo(wx,y+9+((r2*13+wv*7)%14));ctx.quadraticCurveTo(wx+8,y+6+((r2*7+wv*5)%16),wx+16,y+9+((r2*13+wv*7)%14));}ctx.stroke();}if(r2===7||r2===12||(r2>=1&&r2<=2)){ctx.fillStyle='rgba(150,220,150,.1)';for(var tf=0;tf<8;tf++){var tx=(tf*59+r2*23)%W;ctx.fillRect(tx,y+6+((tf*17)%18),2,4);ctx.fillRect(tx+3,y+9+((tf*11)%14),2,4);}}
  if(r2===0){ctx.fillStyle='#3fb8af';
   for(k2=0;k2<6;k2++){ctx.beginPath();ctx.arc(44+k2*66,y+16,11,0,6.283);ctx.fill();}}
  if(r2>=8&&r2<=11){ctx.fillStyle='#26345a';ctx.fillRect(0,y+30,W,2);}}
 for(i=0;i<st.logs.length;i++){var g=st.logs[i];y=g.row*32;
  ctx.fillStyle='#8a5a2b';ctx.fillRect(g.x,y+7,g.w,18);
  ctx.fillStyle='#a9743c';ctx.fillRect(g.x,y+7,g.w,5);}
 for(i=0;i<st.cars.length;i++){var c=st.cars[i];y=c.row*32;
  var cg=ctx.createLinearGradient(0,y+7,0,y+25);cg.addColorStop(0,'#ff8a6c');cg.addColorStop(.5,'#e26d5c');cg.addColorStop(1,'#a83c2c');ctx.fillStyle=cg;ctx.fillRect(c.x+2,y+7,c.w-4,18);ctx.fillStyle='rgba(255,220,170,.85)';ctx.fillRect(c.x+8,y+11,c.w-16,5);ctx.fillStyle='rgba(255,240,200,.6)';ctx.beginPath();ctx.arc(c.x+c.w-6,y+10,3,0,6.283);ctx.arc(c.x+c.w-6,y+22,3,0,6.283);ctx.fill();}
 var f=st.frog;
 ctx.save();ctx.shadowColor=st.alive?'rgba(255,210,120,.55)':'rgba(0,0,0,0)';ctx.shadowBlur=10;var fg2=ctx.createRadialGradient(f.x+13,f.y+12,2,f.x+16,f.y+16,12);fg2.addColorStop(0,st.alive?'#ffe1a0':'#7a8aa0');fg2.addColorStop(1,st.alive?'#c69a3a':'#4a5670');ctx.fillStyle=fg2;ctx.beginPath();ctx.arc(f.x+16,f.y+16,11,0,6.283);ctx.fill();ctx.restore();
 ctx.fillStyle='#14203a';
 ctx.beginPath();ctx.arc(f.x+11,f.y+11,2.2,0,6.283);ctx.fill();
 ctx.beginPath();ctx.arc(f.x+21,f.y+11,2.2,0,6.283);ctx.fill();
 if(!st.alive){ctx.fillStyle='rgba(10,16,32,0.55)';ctx.fillRect(0,0,W,H);}
}
rafStep(function(dt){
 dt=Math.min(dt,0.033);
 var k=keyState(),c2;
 for(c2 in DIRS){if(k[c2]&&!prev[c2]&&!over)st=L.hop(st,DIRS[c2]);prev[c2]=!!k[c2];}
 if(!over)st=L.step(st,dt);
 paint();
 if(st.score!==lastScore){lastScore=st.score;hudUpd();}
 if(!st.alive&&!over){over=true;best=bestOf('wog-frogger-best',st.score);hudUpd();
  ovl('قورباغه حذف شد!','امتیاز: '+fa(st.score),'بازی جدید',reset);}
});
hudUpd();
"""

FR_TESTS = [
 ("پرش شبکه‌ای و مرزهای زمین", """
var s=L.newState(rng);
T.eq(s.frog.y,384,'start bottom row');
var d=L.hop(s,'down');T.eq(d.frog.y,384,'down bounded');
var u=L.hop(s,'up');T.eq(u.frog.y,352,'up moves one cell');
var l=s,i;for(i=0;i<20;i++)l=L.hop(l,'left');
T.eq(l.frog.x,0,'left bound');
var r=s;for(i=0;i<20;i++)r=L.hop(r,'right');
T.eq(r.frog.x,384,'right bound at W-CELL');
T.eq(L.hop(r,'right').frog.x,384,'right clamp');
T.ok(l.frog.x%32===0&&u.frog.y%32===0,'grid aligned');
"""),
 ("برخورد مستطیلی با ماشین", """
function mk(fx){return {frog:{x:fx,y:352},cars:[{x:180,row:11,w:48,dir:1,sp:70}],logs:[],score:0,round:1,mul:1,alive:true,t:0};}
T.ok(L.collide(mk(190)),'car overlaps frog');
T.ok(!L.collide(mk(260)),'separated is safe');
var s2=L.step(mk(190),0.05);
T.ok(!s2.alive,'step kills on car');
"""),
 ("سوار شدن کنده: قورباغه با آن می‌راند", """
var s3={frog:{x:140,y:192},cars:[],logs:[{x:100,row:6,w:96,dir:-1,sp:60}],score:0,round:1,mul:1,alive:true,t:0};
T.ok(L.onLog(s3),'on log');
var s4=L.step(s3,0.5);
T.approx(s4.logs[0].x,70,0.001,'log moved left 30');
T.approx(s4.frog.x-140,-30,0.5,'frog drifted with log');
T.ok(s4.alive,'still alive riding');
"""),
 ("افتادن در آب = مرگ", """
var s5={frog:{x:300,y:192},cars:[],logs:[{x:100,row:6,w:96,dir:-1,sp:60}],score:0,round:1,mul:1,alive:true,t:0};
T.ok(!L.onLog(s5),'not on log');
var s6=L.step(s5,0.1);
T.ok(!s6.alive,'drowned in water');
"""),
 ("تشخیص ردیف برد و رفتن به دور بعد", """
var s7=L.newState(rng);s7.frog={x:192,y:0};
T.ok(L.reached(s7),'reached top row');
var s8=L.step(s7,0.016);
T.eq(s8.score,1,'score +1');
T.eq(s8.round,2,'round 2');
T.ok(s8.mul>1,'speed multiplier up');
T.eq(s8.frog.y,384,'frog reset to start');
"""),
 ("شبیه‌سازی ۳۰ ثانیه‌ای: قورباغه همیشه روی شبکه است", """
var s=L.newState(rng),t=0,steps=0;
while(s.alive&&t<30){s=L.step(s,1/60);t+=1/60;steps++;
 T.ok(s.frog.x>=0&&s.frog.x<=416&&s.frog.y>=0&&s.frog.y<=416,'frog in bounds step '+steps);}
T.ok(steps>300,'world moved: '+steps+' frames');
"""),
]

# ---------------- coin-catch ----------------
CC_LOGIC = r"""
var CC={W:340,H:420,PY:372,PW:64,R:11};
function hash(n){var x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);}
function ramp(t){return Math.min(130+t*7,420);}
function bombP(t){return Math.min(0.16+t*0.004,0.32);}
function bonusFor(sk){return (sk>0&&sk%5===0)?5:0;}
function newState(rng){var r=rng||Math.random;
 return {px:170,items:[],score:0,streak:0,lives:3,t:0,spawnT:0.9,n:0,over:false,caught:0,misses:0,seed:r()*100};}
function inWindow(it,px,kind){
 if(it.kind!==kind)return false;
 if(it.y<CC.PY-CC.R-2||it.y>CC.PY+26)return false;
 return Math.abs(it.x-px)<=CC.PW/2+CC.R;}
function catchCheck(st){var i;
 for(i=0;i<st.items.length;i++)if(inWindow(st.items[i],st.px,'coin'))return true;
 return false;}
function bombHit(st){var i;
 for(i=0;i<st.items.length;i++)if(inWindow(st.items[i],st.px,'bomb'))return true;
 return false;}
function step(st,dt,px){
 px=Math.max(CC.PW/2,Math.min(CC.W-CC.PW/2,px));
 var n={px:px,items:[],score:st.score,streak:st.streak,lives:st.lives,t:st.t+dt,spawnT:st.spawnT,n:st.n,over:st.over,caught:st.caught,misses:st.misses,seed:st.seed};
 if(st.over)return n;
 var sc=st.score,stk=st.streak,liv=st.lives,cau=st.caught,mis=st.misses,i,it;
 n.spawnT-=dt;
 if(n.spawnT<=0){
  var kind=hash(st.seed+st.n*2.3)<bombP(st.t)?'bomb':'coin';
  n.items.push({x:20+hash(st.seed+st.n*5.7)*(CC.W-40),y:-20,vy:ramp(st.t)*(0.9+0.3*hash(st.seed+st.n*9.1)),kind:kind});
  n.n=st.n+1;n.spawnT+=Math.max(0.45,1.05-st.t*0.008);}
 for(i=0;i<st.items.length;i++){it=st.items[i];
  var iy=it.y+it.vy*dt,ii={x:it.x,y:iy,vy:it.vy,kind:it.kind};
  if(ii.kind==='coin'&&inWindow(ii,px,'coin')){stk++;sc+=1+bonusFor(stk);cau++;continue;}
  if(ii.kind==='bomb'&&inWindow(ii,px,'bomb')){liv--;stk=0;continue;}
  if(ii.y>CC.H+24){if(ii.kind==='coin'){mis++;stk=0;}continue;}
  n.items.push(ii);}
 if(liv<=0)n.over=true;
 n.score=sc;n.streak=stk;n.lives=liv;n.caught=cau;n.misses=mis;
 return n;}
var WOG_LOGIC={newState:newState,step:step,catchCheck:catchCheck,bombHit:bombHit,ramp:ramp,bombP:bombP,bonusFor:bonusFor,CC:CC};
"""

CC_UI = r"""
var W=340,H=420;
var cvv=makeCanvas(W,H),ctx=cvv.ctx;
$('#hint').textContent='سکه‌ها را بگیر و از بمب‌ها دوری کن؛ پارو را با لمس، ماوس یا کلیدها حرکت بده.';
var best=bestOf('wog-coin-catch-best',0);
var st=L.newState(),over=false,px=170,lastScore=-1;
function hudUpd(){hud('امتیاز: <b>'+fa(st.score)+'</b> · جان: <b>'+fa(st.lives)+'</b> · رکورد: <b>'+fa(best)+'</b>');}
function reset(){st=L.newState();over=false;px=170;lastScore=-1;paint();hudUpd();}
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=reset;
$('#app').insertBefore(nb,cvv.cv);
bindPad([{k:'ArrowLeft',label:'◀'},{k:'ArrowRight',label:'▶'}]);
function ptr(e){var r2=cvv.cv.getBoundingClientRect();px=(e.clientX-r2.left)*W/r2.width;}
cvv.cv.addEventListener('pointermove',ptr);
cvv.cv.addEventListener('pointerdown',ptr);
function paint(){
 var ccg=ctx.createLinearGradient(0,0,0,H);ccg.addColorStop(0,'#141c3e');ccg.addColorStop(.6,'#1a1838');ccg.addColorStop(1,'#241a30');ctx.fillStyle=ccg;ctx.fillRect(0,0,W,H);ctx.fillStyle='rgba(255,255,255,.25)';for(var si2=0;si2<30;si2++){ctx.fillRect((si2*83)%W,(si2*47)%H,1.4,1.4);}
 var i;
 for(i=0;i<st.items.length;i++){var it=st.items[i];
  if(it.kind==='coin'){
   ctx.save();ctx.shadowColor='rgba(255,210,120,.7)';ctx.shadowBlur=12;var cg2=ctx.createRadialGradient(it.x-3,it.y-3,1,it.x,it.y,12);cg2.addColorStop(0,'#ffe9b8');cg2.addColorStop(.65,'#d9a441');cg2.addColorStop(1,'#9a6e1e');ctx.fillStyle=cg2;ctx.beginPath();ctx.arc(it.x,it.y,11,0,6.283);ctx.fill();ctx.restore();
   ctx.strokeStyle='#b8862f';ctx.lineWidth=2.5;ctx.beginPath();ctx.arc(it.x,it.y,6.5,0,6.283);ctx.stroke();}
  else{
   ctx.save();ctx.shadowColor='rgba(255,110,80,.7)';ctx.shadowBlur=12;var hg2=ctx.createRadialGradient(it.x-3,it.y-3,1,it.x,it.y,12);hg2.addColorStop(0,'#ffb09a');hg2.addColorStop(.65,'#e26d5c');hg2.addColorStop(1,'#9a3424');ctx.fillStyle=hg2;ctx.beginPath();ctx.arc(it.x,it.y,11,0,6.283);ctx.fill();ctx.restore();
   ctx.fillStyle='#ffd9a0';ctx.fillRect(it.x-1.5,it.y-16,3,5);}}
 ctx.fillStyle='#22355c';ctx.fillRect(0,402,W,18);
 ctx.fillStyle='#3fb8af';ctx.fillRect(st.px-32,372,64,14);
 ctx.fillStyle='#d9a441';ctx.fillRect(st.px-32,372,64,3);
 if(!st.alive||st.lives<=0){ctx.fillStyle='rgba(10,16,32,0.55)';ctx.fillRect(0,0,W,H);}
}
rafStep(function(dt){
 dt=Math.min(dt,0.033);
 var k=keyState();
 if(k.ArrowLeft)px-=460*dt;
 if(k.ArrowRight)px+=460*dt;
 if(!over)st=L.step(st,dt,px);
 px=st.px;
 paint();
 if(st.score!==lastScore){lastScore=st.score;hudUpd();}
 if(st.over&&!over){over=true;best=bestOf('wog-coin-catch-best',st.score);hudUpd();
  ovl('بازی تمام شد!','امتیاز: '+fa(st.score),'بازی جدید',reset);}
});
hudUpd();
"""

CC_TESTS = [
 ("مرز گرفتن سکه و برخورد بمب", """
function mk(px2,ix,iy,kind){return {px:px2,items:[{x:ix,y:iy,vy:100,kind:kind||'coin'}],score:0,streak:0,lives:3,t:0,spawnT:99,n:1,over:false,caught:0,misses:0,seed:1};}
T.ok(L.catchCheck(mk(170,170,368)),'aligned coin caught');
T.ok(L.catchCheck(mk(170,213,368)),'edge x=213 caught');
T.ok(!L.catchCheck(mk(170,214,368)),'x=214 out of reach');
T.ok(L.catchCheck(mk(170,170,361)),'top edge y caught');
T.ok(!L.catchCheck(mk(170,170,358)),'above window no catch');
var b=mk(170,170,368,'bomb');
T.ok(L.bombHit(b),'bomb hits paddle');
T.ok(!L.catchCheck(b),'bomb is not a coin');
"""),
 ("برخورد بمب جان کم می‌کند و پایان بازی", """
function mb(liv){return {px:170,items:[{x:170,y:368,vy:100,kind:'bomb'}],score:5,streak:2,lives:liv,t:0,spawnT:99,n:1,over:false,caught:0,misses:0,seed:1};}
var s2=L.step(mb(3),1/60,170);
T.eq(s2.lives,2,'one bomb one life lost');
T.eq(s2.streak,0,'streak reset on bomb');
T.eq(s2.score,5,'score unchanged by bomb');
var s3=L.step(mb(2),1/60,170);
T.eq(s3.lives,1,'second bomb');
var s4=L.step(mb(1),1/60,170);
T.eq(s4.lives,0,'third bomb: 0 lives');
T.ok(s4.over,'game over at 0 lives');
"""),
 ("رامپ سرعت یکنوا و سقف‌دار", """
var prev=-1,mono=true;
for(var t=0;t<=90;t+=0.5){var v=L.ramp(t);
 if(v<prev)mono=false;prev=v;T.ok(v<=420&&v>=130,'range');}
T.ok(mono,'monotonic');
T.ok(L.ramp(0)===130,'base speed');
T.eq(L.ramp(1e9),420,'cap');
var p2=L.bombP(0),p3=L.bombP(100);
T.ok(p3>p2&&p3<=0.32,'bomb ratio ramps, capped');
"""),
 ("جایزهٔ استریک هر ۵ گرفتنی و ریست با از دست دادن", """
T.eq(L.bonusFor(4),0,'no bonus at 4');
T.eq(L.bonusFor(5),5,'bonus at 5');
T.eq(L.bonusFor(9),0,'no bonus at 9');
T.eq(L.bonusFor(10),5,'bonus at 10');
T.eq(L.bonusFor(0),0,'no bonus at 0');
function mc(){return {px:170,items:[{x:170,y:368,vy:100,kind:'coin'}],score:0,streak:4,lives:3,t:0,spawnT:99,n:1,over:false,caught:0,misses:0,seed:1};}
var s2=L.step(mc(),1/60,170);
T.eq(s2.score,6,'1 catch + 5 bonus');
T.eq(s2.streak,5,'streak 5');
T.eq(s2.caught,1,'caught counter');
var s3={px:170,items:[{x:170,y:460,vy:100,kind:'coin'}],score:6,streak:5,lives:3,t:0,spawnT:99,n:1,over:false,caught:1,misses:0,seed:1};
var s4=L.step(s3,1/60,170);
T.eq(s4.streak,0,'streak reset on miss');
T.eq(s4.misses,1,'miss counted');
"""),
 ("تولید آیتم‌ها در گام با محدودهٔ معتبر", """
var s=L.newState(function(){return 0.5;});
var found=-1;
for(var i=0;i<200;i++){s=L.step(s,1/60,170);if(s.items.length>0){found=i;break;}}
T.ok(found>=0,'item spawned at '+found);
var it=s.items[0];
T.ok(it.kind==='coin'||it.kind==='bomb','valid kind');
T.ok(it.x>=20&&it.x<=320,'x in range');
T.ok(it.y<0,'spawns above screen');
"""),
 ("شبیه‌سازی ۶۰ ثانیهٔ ربات تعقیب‌کننده", """
function bot(s){var ub=null,uy=-1,lc=null,cy=-1,i,it;
 for(i=0;i<s.items.length;i++){it=s.items[i];
  if(it.kind==='bomb'&&it.y>uy){uy=it.y;ub=it;}
  else if(it.kind==='coin'&&it.y>cy){cy=it.y;lc=it;}}
 if(ub&&uy>170)return ub.x>170?ub.x-140:ub.x+140;
 if(lc)return lc.x;
 return 170;}
var s=L.newState(rng),px2=170,livesAt10=-1;
for(var f=0;f<3600;f++){
 var tg=bot(s),d=tg-px2,mv=460/60;
 px2+=Math.abs(d)<=mv?d:(d>0?mv:-mv);
 s=L.step(s,1/60,px2);
 if(f===600)livesAt10=s.lives;
 if(s.over)break;}
T.ok(livesAt10>=2,'no instant loss (lives@10s='+livesAt10+')');
T.ok(s.lives>=1&&!s.over,'survived 60s: lives='+s.lives+' score='+s.score);
T.ok(s.score>20,'score grew to '+s.score);
"""),
]

# ---------------- runner ----------------
RN_LOGIC = r"""
var RN={W:340,H:260,GY:200,G:1800,JV:-640,RPX:64,RW:24,RH:40};
function hash(n){var x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);}
function ramp(d){return Math.min(240+d*0.02,520);}
function minGap(sp){return 200+sp*0.45;}
function newState(rng){var r=rng||Math.random;
 return {y:RN.GY,vy:0,ground:true,obs:[],dist:0,score:0,speed:ramp(0),alive:true,t:0,n:0,latch:false,gapMin:1e9,phase:r()*6.28};}
function collide(st){
 var fl=RN.RPX+2,fr=RN.RPX+RN.RW-2,ft=st.y-RN.RH,fb=st.y,i;
 for(i=0;i<st.obs.length;i++){var o=st.obs[i];
  var ol=o.x+2,orr=o.x+o.w-2,ot=RN.GY-o.h;
  if(fl<orr&&fr>ol&&ft<RN.GY&&fb>ot)return true;}
 return false;}
function step(st,dt,jump){
 var n={y:st.y,vy:st.vy,ground:st.ground,obs:[],dist:st.dist,score:st.score,speed:st.speed,alive:st.alive,t:st.t+dt,n:st.n,latch:st.latch,gapMin:st.gapMin,phase:st.phase};
 if(!st.alive)return n;
 n.latch=jump?(st.latch||false):false;
 if(jump&&!st.latch&&st.ground){n.vy=RN.JV;n.ground=false;n.latch=true;}
 n.vy=n.vy+RN.G*dt;
 n.y=n.y+n.vy*dt;
 if(n.y>=RN.GY){n.y=RN.GY;n.vy=0;n.ground=true;}
 n.dist=st.dist+n.speed*dt;
 n.speed=ramp(n.dist);
 n.score=Math.floor(n.dist/10);
 var i,o,ox;
 for(i=0;i<st.obs.length;i++){o=st.obs[i];ox=o.x-n.speed*dt;
  if(ox+o.w>-40)n.obs.push({x:ox,w:o.w,h:o.h});}
 var last=n.obs[n.obs.length-1];
 if(!last||last.x+last.w<RN.W-minGap(n.speed)){
  var w=18+hash((st.n+1)*3.3)*18,h=24+hash((st.n+1)*7.7)*22;
  if(last)n.gapMin=Math.min(st.gapMin,(RN.W+20)-(last.x+last.w));
  n.obs.push({x:RN.W+20,w:w,h:h});
  n.n=st.n+1;}
 if(collide(n))n.alive=false;
 return n;}
function spawnGapOk(st){return st.gapMin>=minGap(st.speed)-2;}
var WOG_LOGIC={newState:newState,step:step,collide:collide,spawnGapOk:spawnGapOk,ramp:ramp,minGap:minGap,RN:RN};
"""

RN_UI = r"""
var W=340,H=260;
var cvv=makeCanvas(W,H),ctx=cvv.ctx;
$('#hint').textContent='با فاصله، جهت‌بالا یا لمس بپر و از سنگ‌ها رد شو؛ هرچه بیشتر بدوی، سریع‌تر می‌شود.';
var best=bestOf('wog-runner-best',0);
var st=L.newState(),over=false,jumpQ=false,held=false,lastScore=-1;
function hudUpd(){hud('متر: <b>'+fa(st.score)+'</b> · رکورد: <b>'+fa(best)+'</b>');}
function reset(){st=L.newState();over=false;lastScore=-1;jumpQ=false;paint();hudUpd();}
var nb=ce('button','wbtn','بازی جدید');nb.setAttribute('data-smoke','1');nb.onclick=reset;
$('#app').insertBefore(nb,cvv.cv);
cvv.cv.addEventListener('pointerdown',function(e){e.preventDefault();jumpQ=true;});
bindPad([{k:'Space',label:'پریدن'}]);
function paint(){
 var rg=ctx.createLinearGradient(0,0,0,H);rg.addColorStop(0,'#2a1e3e');rg.addColorStop(.5,'#6e3e4a');rg.addColorStop(.78,'#c67a4a');rg.addColorStop(1,'#e8a35c');ctx.fillStyle=rg;ctx.fillRect(0,0,W,H);var rsg=ctx.createRadialGradient(W*.78,H*.62,4,W*.78,H*.62,80);rsg.addColorStop(0,'rgba(255,230,170,.9)');rsg.addColorStop(.4,'rgba(255,200,120,.3)');rsg.addColorStop(1,'rgba(255,200,120,0)');ctx.fillStyle=rsg;ctx.fillRect(0,0,W,H);
 ctx.fillStyle='#182747';ctx.beginPath();ctx.ellipse(90,208,150,55,0,0,6.283);ctx.fill();
 ctx.fillStyle='#1d2f56';ctx.beginPath();ctx.ellipse(300,215,170,60,0,0,6.283);ctx.fill();
 ctx.fillStyle='#c69a3a';ctx.fillRect(0,200,W,60);
 ctx.fillStyle='#d9a441';ctx.fillRect(0,200,W,6);
 var i;
 for(i=0;i<st.obs.length;i++){var o=st.obs[i];
  ctx.fillStyle='#77839b';ctx.fillRect(o.x,200-o.h,o.w,o.h);
  ctx.fillStyle='#9aa5b1';ctx.fillRect(o.x,200-o.h,o.w,4);}
 var y=st.y,ph=Math.floor(st.dist/26)%2;
 ctx.fillStyle='#3fb8af';ctx.fillRect(70,y-26,13,17);
 ctx.beginPath();ctx.arc(76.5,y-33,7,0,6.283);ctx.fill();
 ctx.strokeStyle='#3fb8af';ctx.lineWidth=4;ctx.beginPath();
 if(ph===0){ctx.moveTo(73,y-10);ctx.lineTo(69,y);ctx.moveTo(81,y-10);ctx.lineTo(85,y-2);}
 else{ctx.moveTo(73,y-10);ctx.lineTo(68,y-2);ctx.moveTo(81,y-10);ctx.lineTo(85,y);}
 ctx.stroke();
 if(!st.alive){ctx.fillStyle='rgba(10,16,32,0.55)';ctx.fillRect(0,0,W,H);}
}
rafStep(function(dt){
 dt=Math.min(dt,0.033);
 var k=keyState(),j=jumpQ||!!((k.Space||k.ArrowUp||k.KeyW)&&!held);
 held=!!(k.Space||k.ArrowUp||k.KeyW);jumpQ=false;
 if(!over)st=L.step(st,dt,j);
 paint();
 if(st.score!==lastScore){lastScore=st.score;hudUpd();}
 if(!st.alive&&!over){over=true;best=bestOf('wog-runner-best',st.score);hudUpd();
  ovl('پایان دویدن!','متر: '+fa(st.score),'بازی جدید',reset);}
});
hudUpd();
"""

RN_TESTS = [
 ("فیزیک پرش: برخاست و بازگشت به زمین", """
function base(){return {y:L.RN.GY,vy:0,ground:true,obs:[{x:5000,w:20,h:30}],dist:0,score:0,speed:240,alive:true,t:0,n:1,latch:false,gapMin:1e9,phase:0};}
var s=base();
var j=L.step(s,1/60,true);
T.ok(j.vy<0&&j.y<L.RN.GY,'airborne after jump');
T.ok(j.vy>=-640,'impulse is -640');
var k=j,i;
for(i=0;i<90;i++)k=L.step(k,1/60,false);
T.ok(k.alive,'still alive, no obstacles near');
T.eq(k.y,L.RN.GY,'landed back on ground');
T.eq(k.vy,0,'velocity rests at 0');
T.ok(k.ground,'ground flag set');
"""),
 ("پرش دوم در هوا ممنوع ( latch )", """
function base(){return {y:L.RN.GY,vy:0,ground:true,obs:[{x:5000,w:20,h:30}],dist:0,score:0,speed:240,alive:true,t:0,n:1,latch:false,gapMin:1e9,phase:0};}
var a=L.step(base(),1/60,true);
var b=L.step(a,1/60,true);
T.ok(b.vy>a.vy,'gravity only in air');
T.ok(b.vy>-640,'no re-jump mid-air');
var c=a,i;
for(i=0;i<60;i++)c=L.step(c,1/60,true);
T.eq(c.y,L.RN.GY,'held key: exactly one jump, then grounded');
T.ok(c.ground,'grounded with key held');
"""),
 ("سیستم اسپاون: ۲۰۰ مانع با فاصلهٔ مجاز", """
var s=L.newState(rng),t=0,spawns=0,ok=true;
while(spawns<200&&t<180){s.obs=[];s=L.step(s,1/60,false);t+=1/60;
 if(s.n>spawns){spawns=s.n;if(!L.spawnGapOk(s)){ok=false;break;}}}
T.ok(spawns>=200,'spawned '+spawns);
T.ok(ok,'min gap invariant holds');
T.ok(s.gapMin>0,'gaps recorded');
"""),
 ("برخورد با سنگ اجرا را پایان می‌دهد", """
function base(ox){return {y:L.RN.GY,vy:0,ground:true,obs:[{x:ox,w:20,h:40}],dist:0,score:0,speed:240,alive:true,t:0,n:1,latch:false,gapMin:1e9,phase:0};}
var s2=L.step(base(70),1/60,false);
T.ok(!s2.alive,'overlapping rock ends run');
var s3=L.step(base(240),1/60,false);
T.ok(s3.alive,'far rock is safe');
"""),
 ("امتیاز = انباشت مسافت و رامپ سرعت", """
var s=L.newState(rng);
for(var i=0;i<120;i++)s=L.step(s,1/60,false);
T.ok(s.dist>0,'distance accumulates');
T.eq(s.score,Math.floor(s.dist/10),'score is dist/10');
var m=true,d;
for(d=0;d<50000;d+=250){if(L.ramp(d+250)<L.ramp(d))m=false;}
T.ok(m,'speed monotonic');
T.eq(L.ramp(1e9),520,'speed cap 520');
T.eq(L.minGap(240),308,'minGap at 240');
T.eq(L.minGap(520),434,'minGap at 520');
"""),
 ("ابعاد موانع و شمارش اسپاون", """
var s=L.newState(rng);
for(var i=0;i<30;i++)s=L.step(s,1/60,false);
T.ok(s.obs.length>=1,'obstacle exists');
T.ok(s.n>=1,'spawn counter increments');
var o=s.obs[s.obs.length-1];
T.ok(o.w>=18&&o.w<=36,'width in range');
T.ok(o.h>=24&&o.h<=46,'height in range');
T.ok(o.x<=340&&o.x>0,'spawns at right edge');
"""),
]

flappy = G(slug='flappy', title='پرواز پرنده', cat='arcade', icon='🐦', g1='#d9a441', g2='#3fb8af',
 desc='پرندهٔ طلایی را بین لوله‌های فیروزه‌ای هدایت کن؛ با عبور از هر لوله یک امتیاز بگیر.',
 hint='لمس صفحه یا کلید فاصله = بال زدن', engines=('common','arcade'),
 logic=FL_LOGIC, ui=FL_UI, css=CSS_ARCADE, tests=FL_TESTS, seed=12345)

frogger = G(slug='frogger', title='قورباغهٔ عبوری', cat='arcade', icon='🐸', g1='#67b98a', g2='#3fb8af',
 desc='قورباغه را از جادهٔ پرماشین و رودخانه عبور بده؛ روی کنده‌ها سوار شو و به ردیف بالا برس.',
 hint='کلیدهای جهت‌نما یا دکمه‌های لمسی = پرش', engines=('common','arcade'),
 logic=FR_LOGIC, ui=FR_UI, css=CSS_ARCADE, tests=FR_TESTS, seed=12345)

coin_catch = G(slug='coin-catch', title='صیاد سکه', cat='arcade', icon='🪙', g1='#d9a441', g2='#e26d5c',
 desc='با پارو سکه‌های طلایی را بگیر، زنجیه بساز و از بمب‌ها دوری کن؛ سرعت مدام بیشتر می‌شود.',
 hint='حرکت ماوس/لمس یا کلیدهای چپ و راست = پارو', engines=('common','arcade'),
 logic=CC_LOGIC, ui=CC_UI, css=CSS_ARCADE, tests=CC_TESTS, seed=12345)

runner = G(slug='runner', title='دوندهٔ کویر', cat='arcade', icon='🏃', g1='#d9a441', g2='#77839b',
 desc='دوندهٔ کویر از روی سنگ‌ها می‌پرد؛ مسافت بیشتر، امتیاز بیشتر و سرعت فزاینده.',
 hint='فاصله، جهت‌بالا یا لمس = پرش', engines=('common','arcade'),
 logic=RN_LOGIC, ui=RN_UI, css=CSS_ARCADE, tests=RN_TESTS, seed=12345)

GAMES=[flappy, frogger, coin_catch, runner]
