# -*- coding: utf-8 -*-
# AG-D2 — three board games: game-of-ur, battleship, pentago (cat=board, engines=("common",))
from lib_mini import G

# ============================== GAME OF UR ==============================
UR_LOGIC = r"""
var PATH=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[7,1],[6,1],[5,1],[4,1],[3,1],[2,1],[1,1],[0,1],[0,2],[1,2],[2,2],[3,2]];
var ROSETTES=[4,8,14];
var SHARED=[5,6,7,8,9,10,11,12];
function isRos(i){return ROSETTES.indexOf(i)>=0}
function isShr(i){return i>=5&&i<=12}
function newState(){return{p:[[-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1]],t:0}}
function occAt(s,i){for(var pl=0;pl<2;pl++)for(var k=0;k<7;k++)if(s.p[pl][k]===i)return pl;return -1}
function targetOf(pos,steps){return pos<0?steps-1:pos+steps}
function canLand(s,pl,tg){
 if(tg===20)return true;
 if(tg<0||tg>19)return false;
 var o=occAt(s,tg);
 if(o===pl)return false;
 if(isRos(tg)&&o>=0)return false;
 if(o===1-pl)return isShr(tg);
 return true;
}
function legalMoves(s,pl,steps){
 var out=[],k;
 for(k=0;k<7;k++){var pos=s.p[pl][k];if(pos===20)continue;if(canLand(s,pl,targetOf(pos,steps)))out.push(k)}
 return out;
}
function applyMove(s,pl,k,steps){
 var pos=s.p[pl][k],tg=targetOf(pos,steps),cap=false,extra=false,j;
 if(tg===20){s.p[pl][k]=20;return{captured:false,extra:false}}
 var o=occAt(s,tg);
 if(o===1-pl){for(j=0;j<7;j++)if(s.p[1-pl][j]===tg){s.p[1-pl][j]=-1;cap=true;break}}
 s.p[pl][k]=tg;
 if(isRos(tg))extra=true;
 return{captured:cap,extra:extra};
}
function pieceStates(s,pl){var st=0,pa=0,bo=0,k,pos;for(k=0;k<7;k++){pos=s.p[pl][k];if(pos===-1)st++;else if(pos===20)bo++;else pa++}return{start:st,path:pa,borne:bo}}
function isWin(s,pl){return pieceStates(s,pl).borne===7}
function roll4(rng){var r=rng||Math.random,n=0,i;for(i=0;i<4;i++)if(r()<0.5)n++;return n}
function moveScore(s,pl,k,steps){
 var pos=s.p[pl][k],tg=targetOf(pos,steps),sc=0;
 if(tg<=19){var o=occAt(s,tg);if(o===1-pl)sc+=100;if(isRos(tg))sc+=40}
 sc+=(pos>=0?pos:-1);
 return sc;
}
function aiChoose(s,a,b,c){
 var pl,steps,rng;
 if(c===undefined){pl=s.t;steps=a;rng=b}else{pl=a;steps=b;rng=c}
 rng=rng||Math.random;
 var ms=legalMoves(s,pl,steps);
 if(!ms.length)return -1;
 var bs=-1e9,i,sc;
 for(i=0;i<ms.length;i++){sc=moveScore(s,pl,ms[i],steps);if(sc>bs)bs=sc}
 var ties=[];
 for(i=0;i<ms.length;i++)if(moveScore(s,pl,ms[i],steps)===bs)ties.push(ms[i]);
 return ties[(rng()*ties.length)|0];
}
var WOG_LOGIC={PATH:PATH,ROSETTES:ROSETTES,SHARED:SHARED,newState:newState,occAt:occAt,targetOf:targetOf,canLand:canLand,legalMoves:legalMoves,applyMove:applyMove,pieceStates:pieceStates,isWin:isWin,roll4:roll4,aiChoose:aiChoose};
"""

UR_UI = r"""
var S=L.newState(),phase='roll',steps=0,lock=false,gen=0;
function cnt(pl,v){var n=0,k;for(k=0;k<7;k++)if(S.p[pl][k]===v)n++;return n}
function movableSet(){var ms=L.legalMoves(S,S.t,steps),set={},i;for(i=0;i<ms.length;i++)set[ms[i]]=1;return set}
function hudUp(){hud('نوبت: <b>'+(S.t===0?'تو':'ربات')+'</b> · بیرون‌آمده — تو: '+fa(cnt(0,20))+' / ربات: '+fa(cnt(1,20)))}
function diceHtml(){var h='',i;for(i=0;i<4;i++)h+='<span class="die'+(i<steps?' on':'')+'"></span>';return h}
function later(ms,fn){var g0=gen;setTimeout(function(){if(g0===gen)fn()},ms)}
function fresh(){gen++;S=L.newState();phase='roll';steps=0;lock=false;render();hudUp();toast('بازی تازه شروع شد')}
function humanApply(k){
 if(S.t!==0||phase!=='move')return;
 var res=L.applyMove(S,0,k,steps);
 steps=0;
 if(L.isWin(S,0)){phase='over';render();hudUp();ovl('بردی!','هر ۷ مهره‌ات به خانه رسید','بازی دوباره',fresh);return}
 if(res.extra){toast('روزت! نوبت اضافه داری');phase='roll';render();hudUp();return}
 if(res.captured)toast('مهرهٔ حریف به آغاز برگشت');
 S.t=1;phase='ai';render();hudUp();later(750,aiStep);
}
function aiStep(){
 steps=L.roll4();
 var k=L.aiChoose(S,steps,Math.random);
 if(k<0){steps=0;toast('ربات حرکتی نداشت');S.t=0;phase='roll';render();hudUp();return}
 var res=L.applyMove(S,1,k,steps);
 if(res.captured)toast('ربات یکی از مهره‌هایت را گرفت!');
 if(L.isWin(S,1)){steps=0;phase='over';render();hudUp();ovl('ربات برد','مهره‌های ربات زودتر رسیدند','بازی دوباره',fresh);return}
 if(res.extra){toast('ربات: روزت! دوباره می‌ریزد');render();hudUp();later(750,aiStep);return}
 steps=0;S.t=0;phase='roll';render();hudUp();
}
function doRoll(){
 if(lock||phase!=='roll'||S.t!==0)return;
 steps=L.roll4();
 var ms=L.legalMoves(S,0,steps);
 if(!ms.length){lock=true;render();toast('با تاس '+fa(steps)+' حرکتی نیست؛ نوبت رد شد');later(900,function(){lock=false;S.t=1;phase='ai';render();hudUp();later(750,aiStep)});return}
 phase='move';render();toast('تاس: '+fa(steps)+' — مهرهٔ سبزرنگ را لمس کن');
}
function cellClick(i){
 if(lock||phase!=='move'||S.t!==0)return;
 var ms=movableSet();
 for(var k=0;k<7;k++)if(S.p[0][k]===i&&ms[k]){humanApply(k);return}
 toast('این مهره با تاس '+fa(steps)+' جلو نمی‌رود');
}
function render(){
 var app=$('#app');app.innerHTML='';
 var ms=(phase==='move'&&S.t===0)?movableSet():{};
 var board=ce('div','uboard');
 for(var i=0;i<20;i++){
  var d=ce('div','ucell'+(L.SHARED.indexOf(i)>=0?' ushr':'')+(L.ROSETTES.indexOf(i)>=0?' uros':''));
  d.style.gridColumn=''+(L.PATH[i][0]+1);
  d.style.gridRow=''+(L.PATH[i][1]+1);
  var o=L.occAt(S,i);
  if(o>=0)d.appendChild(ce('span','up p'+o,'●'));
  for(var k=0;k<7;k++)if(S.p[0][k]===i&&ms[k]){d.classList.add('canmv');break}
  d.addEventListener('click',function(ii){return function(){cellClick(ii)}}(i));
  board.appendChild(d);
 }
 var ek=-1,k2;
 if(phase==='move'&&S.t===0)for(k2=0;k2<7;k2++)if(S.p[0][k2]===-1&&ms[k2])ek=k2;
 var row=ce('div','urow');
 var p0=ce('div','upanel'+(ek>=0?' canmv':''),'در آغاز — تو: '+fa(cnt(0,-1))+' · ربات: '+fa(cnt(1,-1)));
 if(ek>=0)p0.addEventListener('click',function(){humanApply(ek)});
 row.appendChild(p0);
 row.appendChild(ce('div','upanel','به خانه رسیده — تو: '+fa(cnt(0,20))+' · ربات: '+fa(cnt(1,20))));
 var bar=ce('div','ubar');
 var rb=ce('button','btn prime','تاس بریز');rb.setAttribute('data-smoke','1');rb.addEventListener('click',doRoll);
 var nb=ce('button','btn','بازی جدید');nb.setAttribute('data-smoke','1');nb.addEventListener('click',fresh);
 var dv=ce('div','udice');dv.innerHTML=diceHtml();
 bar.appendChild(rb);bar.appendChild(dv);bar.appendChild(nb);
 app.appendChild(board);app.appendChild(row);app.appendChild(bar);
 $('#hint').textContent='تاس بریز؛ مهره‌ای که دقیقاً به‌اندازهٔ تاس جلو می‌رود سبز می‌شود (ورود از پنل «در آغاز»). روزت = نوبت اضافه؛ در ناحیهٔ روشن مهرهٔ تکِ حریف را می‌گیری.';
}
render();hudUp();
"""

UR_CSS = r"""
body{background:#0b1220;color:#e8e6df;font-family:Tahoma,'Segoe UI',sans-serif;margin:0;padding:12px}
.wog-home{color:#3fb8af;font-size:12px;text-decoration:none}
header h1{color:#d9a441;font-size:20px;margin:6px 0;text-align:center}
#hud{color:#3fb8af;font-size:14px;text-align:center}
.uboard{display:grid;grid-template-columns:repeat(8,1fr);gap:5px;direction:ltr;max-width:600px;margin:10px auto}
.ucell{min-height:46px;background:#14203a;border:1px solid #2a3b5e;border-radius:8px;display:flex;align-items:center;justify-content:center;touch-action:manipulation}
.ushr{background:#1b2c4f;border-color:#33507e}
.uros{border-color:#d9a441;box-shadow:inset 0 0 0 2px rgba(217,164,65,.55)}
.up{font-size:24px;line-height:1}
.p0{color:#d9a441}.p1{color:#3fb8af}
.canmv{border-color:#67b98a;cursor:pointer;box-shadow:0 0 0 2px rgba(103,185,138,.6)}
.urow{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:8px 0}
.upanel{background:#14203a;border:1px solid #2a3b5e;border-radius:8px;padding:8px 10px;font-size:13px}
.ubar{display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:8px}
.btn{min-height:44px;min-width:44px;padding:8px 16px;border-radius:10px;border:1px solid #33507e;background:#1b2c4f;color:#e8e6df;font-size:15px;cursor:pointer;touch-action:manipulation}
.btn.prime{background:#d9a441;color:#14203a;border-color:#d9a441;font-weight:bold}
.udice{display:flex;gap:4px;align-items:center}
.die{width:16px;height:16px;border-radius:50%;border:2px solid #3fb8af;display:inline-block}
.die.on{background:#d9a441;border-color:#d9a441}
#wog-toast{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);background:#1b2c4f;color:#e8e6df;padding:8px 14px;border-radius:8px;border:1px solid #33507e;font-size:14px;pointer-events:none;z-index:9}
p#hint{color:#8fa3c7;text-align:center;font-size:13px}
"""

UR_TESTS = [
("تاس، مسیر و روزت‌ها", r"""
T.eq(L.roll4(function(){return 0.1}),4,'all ones');
T.eq(L.roll4(function(){return 0.9}),0,'all zeros');
var seq=[0.1,0.9,0.1,0.9],i=0;
T.eq(L.roll4(function(){return seq[i++%4]}),2,'mixed dice');
T.eq(L.PATH.length,20,'path has 20 cells');
T.eq(L.ROSETTES.length,3,'three rosettes');
T.ok(L.ROSETTES.length<=4,'at most 4 rosettes');
for(var j=0;j<L.ROSETTES.length;j++)T.ok(L.ROSETTES[j]>=0&&L.ROSETTES[j]<20,'rosette inside path');
T.eq(L.SHARED.length,8,'shared zone 8 cells');
T.ok(L.SHARED[0]===5&&L.SHARED[7]===12,'shared is 5..12');
"""),
("انتصاب فقط در منطقهٔ مشترک", r"""
var s=L.newState();
s.p[1][0]=7;s.p[0][0]=4;
T.ok(L.legalMoves(s,0,3).indexOf(0)>=0,'capture move is legal');
var r1=L.applyMove(s,0,0,3);
T.ok(r1.captured,'captured flag set');
T.eq(s.p[1][0],-1,'enemy sent back to start');
T.eq(s.p[0][0],7,'moved onto captured cell');
var s2=L.newState();s2.p[1][0]=15;s2.p[0][0]=13;
T.eq(L.legalMoves(s2,0,2).indexOf(0),-1,'no capture in private zone');
var s3=L.newState();s3.p[1][0]=8;s3.p[0][0]=6;
T.eq(L.legalMoves(s3,0,2).indexOf(0),-1,'rosette enemy cannot be captured/entered');
var s4=L.newState();s4.p[0][1]=9;s4.p[0][0]=6;
T.eq(L.legalMoves(s4,0,3).indexOf(0),-1,'own piece blocks target');
"""),
("روزت: مسدودی و نوبت اضافه", r"""
var s=L.newState();s.p[0][1]=4;s.p[0][0]=2;
T.eq(L.legalMoves(s,0,2).indexOf(0),-1,'own piece on rosette blocks entry');
var s2=L.newState();s2.p[1][0]=4;s2.p[0][0]=2;
T.eq(L.legalMoves(s2,0,2).indexOf(0),-1,'enemy on rosette blocks');
T.ok(L.legalMoves(s2,0,2).indexOf(1)>=0,'piece standing on rosette can still leave');
var s3=L.newState();s3.p[0][0]=3;
var r3=L.applyMove(s3,0,0,1);
T.ok(r3.extra,'rosette landing grants extra turn');
T.eq(s3.p[0][0],4,'landed on rosette');
var s4=L.newState();s4.p[0][0]=5;
var r4=L.applyMove(s4,0,0,1);
T.ok(!r4.extra,'plain cell gives no extra turn');
T.ok(!r4.captured,'no capture on empty cell');
"""),
("حرکت دقیق، ورود و خروج", r"""
var s=L.newState();
T.eq(L.legalMoves(s,0,0).length,0,'zero roll means no move');
L.applyMove(s,0,2,1);
T.eq(s.p[0][2],0,'entry consumes roll and lands at 0');
L.applyMove(s,0,2,2);
T.eq(s.p[0][2],2,'exact move by two');
var s2=L.newState();s2.p[0][0]=18;
T.eq(L.legalMoves(s2,0,3).indexOf(0),-1,'overshoot off board forbidden');
T.ok(L.legalMoves(s2,0,2).indexOf(0)>=0,'exact landing on 20 borne off');
L.applyMove(s2,0,0,2);
T.eq(s2.p[0][0],20,'piece is borne off');
var s3=L.newState();s3.p[1][0]=0;
T.eq(L.legalMoves(s3,0,1).indexOf(1),-1,'entry blocked by enemy in private cell');
"""),
("یکپارچگی ۷ مهره و برد", r"""
var s=L.newState();
var a=L.pieceStates(s,0),b=L.pieceStates(s,1);
T.eq([a.start,a.path,a.borne],[7,0,0],'P1 starts with 7 in start');
T.eq(b.start+b.path+b.borne,7,'P2 integrity 7 total');
L.applyMove(s,0,0,3);
a=L.pieceStates(s,0);
T.eq([a.start,a.path,a.borne],[6,1,0],'state shifts on entry');
s.p[0][1]=20;s.p[0][2]=20;
T.eq(L.pieceStates(s,0).borne,2,'borne pieces counted');
T.ok(!L.isWin(s,0),'no win before 7 borne');
for(var k=0;k<7;k++)s.p[0][k]=20;
T.ok(L.isWin(s,0),'win at 7 borne off');
T.ok(!L.isWin(s,1),'opponent has not won');
"""),
("بازی کامل: AI در برابر AI", r"""
var s=L.newState(),plies=0,winner=-1;
while(plies<3000){
 var pl=s.t,steps=L.roll4(rng);
 var k=L.aiChoose(s,pl,steps,rng);
 if(k<0){s.t=1-pl;plies++;continue}
 var res=L.applyMove(s,pl,k,steps);
 plies++;
 var a=L.pieceStates(s,0),b2=L.pieceStates(s,1);
 T.ok(a.start+a.path+a.borne===7&&b2.start+b2.path+b2.borne===7,'integrity mid-game');
 if(!res.extra)s.t=1-pl;
 if(L.isWin(s,pl)){winner=pl;break}
}
T.ok(winner===0||winner===1,'game ended with winner, plies='+plies);
T.ok(plies<=3000,'terminated under 3000 plies');
"""),
]

# ============================== BATTLESHIP ==============================
BS_LOGIC = r"""
function emptyGrid(){var g=[],r,c;for(r=0;r<10;r++){var row=[];for(c=0;c<10;c++)row.push({s:0,x:false});g.push(row)}return g}
function canPlace(g,r,c,len,hz){
 if(r<0||c<0||r>9||c>9)return false;
 if(hz&&c+len>10)return false;
 if(!hz&&r+len>10)return false;
 for(var i=0;i<len;i++){var rr=hz?r:r+i,cc=hz?c+i:c;if(g[rr][cc].s!==0)return false}
 return true;
}
function place(g,r,c,len,hz){
 var id=1,y,x;
 for(y=0;y<10;y++)for(x=0;x<10;x++)if(g[y][x].s>=id)id=g[y][x].s+1;
 for(var i=0;i<len;i++){var rr=hz?r:r+i,cc=hz?c+i:c;g[rr][cc].s=id}
 return g;
}
function shipLen(g,id){var n=0,y,x;for(y=0;y<10;y++)for(x=0;x<10;x++)if(g[y][x].s===id)n++;return n}
function shoot(g,r,c){
 var cell=g[r][c];
 if(cell.x)return{hit:cell.s>0,sunk:false,ship:cell.s>0?shipLen(g,cell.s):0,again:true};
 cell.x=true;
 if(cell.s===0)return{hit:false,sunk:false,ship:0};
 var left=0,y,x;
 for(y=0;y<10;y++)for(x=0;x<10;x++)if(g[y][x].s===cell.s&&!g[y][x].x)left++;
 return{hit:true,sunk:left===0,ship:shipLen(g,cell.s)};
}
function isFleetDead(g){var y,x;for(y=0;y<10;y++)for(x=0;x<10;x++)if(g[y][x].s>0&&!g[y][x].x)return false;return true}
function shipsAlive(g){var ids={},y,x,n=0;for(y=0;y<10;y++)for(x=0;x<10;x++){var sc=g[y][x].s;if(sc>0&&!g[y][x].x)ids[sc]=1}for(var k in ids)n++;return n}
function aiNew(g){var t=[],i,j;for(i=0;i<10;i++){t.push([]);for(j=0;j<10;j++)t[i].push(false)}return{g:g,t:t,tg:[]}}
function fire(st,rr,cc){
 st.t[rr][cc]=true;
 var res=shoot(st.g,rr,cc);
 if(res.hit){var nb=[[-1,0],[1,0],[0,-1],[0,1]];for(var i=0;i<4;i++){var y=rr+nb[i][0],x=cc+nb[i][1];if(y>=0&&y<10&&x>=0&&x<10&&!st.t[y][x])st.tg.push([y,x])}}
 return[rr,cc,res];
}
function aiShoot(st,rng){
 var r=rng||Math.random,y,x;
 while(st.tg.length){var t=st.tg.shift();if(!st.t[t[0]][t[1]])return fire(st,t[0],t[1])}
 var par=r()<0.5?0:1,A=[],B=[];
 for(y=0;y<10;y++)for(x=0;x<10;x++)if(!st.t[y][x]){if((y+x)%2===par)A.push([y,x]);else B.push([y,x])}
 var pool=A.length?A:B;
 if(!pool.length)return null;
 var p=pool[(r()*pool.length)|0];
 return fire(st,p[0],p[1]);
}
function autoPlace(g,rng){
 var r=rng||Math.random,lens=[5,4,3,3,2],i,a;
 for(i=0;i<lens.length;i++){
  var len=lens[i],done=false;
  for(a=0;a<400&&!done;a++){
   var hz=r()<0.5,rr=(r()*10)|0,cc=(r()*10)|0;
   if(canPlace(g,rr,cc,len,hz)){place(g,rr,cc,len,hz);done=true}
  }
  if(!done)return false;
 }
 return true;
}
var WOG_LOGIC={emptyGrid:emptyGrid,canPlace:canPlace,place:place,shoot:shoot,isFleetDead:isFleetDead,shipsAlive:shipsAlive,aiNew:aiNew,aiShoot:aiShoot,autoPlace:autoPlace,shipLen:shipLen};
"""

BS_UI = r"""
var FLEET=[{n:'ناو هواپیمابر',l:5},{n:'ناو جنگی',l:4},{n:'ناوشکن',l:3},{n:'ناوشکن دوم',l:3},{n:'زیردریایی',l:2}];
var pg=null,eg=null,pa=null,phase='place',sel=0,hz=true,lock=false,gen=0;
function alive(g){return L.shipsAlive(g)}
function later(ms,fn){var g0=gen;setTimeout(function(){if(g0===gen)fn()},ms)}
function hudUp(){
 if(phase==='place')hud('چیدمان ناوگان — '+fa(FLEET.length-sel)+' ناو مانده');
 else hud('ناوگان ربات: '+fa(alive(eg))+' زنده · ناوگان تو: '+fa(alive(pg))+' زنده');
}
function fresh(){gen++;pg=L.emptyGrid();eg=null;pa=null;phase='place';sel=0;hz=true;lock=false;render();hudUp();toast('ناوها را بچین')}
function startBattle(){
 eg=L.emptyGrid();L.autoPlace(eg,Math.random);
 pa=L.aiNew(pg);phase='battle';lock=false;render();hudUp();
 toast('نبرد آغاز شد! دریای ربات را لمس کن');
}
function boardEl(g,enemy,cb){
 var b=ce('div','bsboard');
 for(var r=0;r<10;r++)for(var c=0;c<10;c++){
  var cell=g[r][c],cls='bcell',sunkShip=false;
  if(cell.s>0&&cell.x){var left=0,y,x;for(y=0;y<10;y++)for(x=0;x<10;x++)if(g[y][x].s===cell.s&&!g[y][x].x)left++;sunkShip=left===0}
  if(!enemy&&cell.s>0)cls+=' shp';
  if(cell.x)cls+=(cell.s>0?(sunkShip?' snk':' hit'):' mis');
  var d=ce('div',cls,cell.x?(cell.s>0?'●':'○'):'');
  if(cb){d.classList.add('act');d.addEventListener('click',function(rr,cc){return function(){cb(rr,cc)}}(r,c))}
  b.appendChild(d);
 }
 return b;
}
function render(){
 var app=$('#app');app.innerHTML='';
 if(phase==='place'){
  var chips=ce('div','bchips');
  var rest=FLEET.slice(sel);
  for(var i=0;i<rest.length;i++){var ch=ce('div','bchip'+(i===0?' selc':''),rest[i].n+' ('+fa(rest[i].l)+')');chips.appendChild(ch)}
  var rb=ce('button','btn','جهت: '+(hz?'افقی':'عمودی'));rb.setAttribute('data-smoke','1');
  rb.addEventListener('click',function(){hz=!hz;render()});
  var ab=ce('button','btn prime','چیدمان خودکار');ab.setAttribute('data-smoke','1');
  ab.addEventListener('click',function(){pg=L.emptyGrid();L.autoPlace(pg,Math.random);sel=FLEET.length;startBattle()});
  var nb=ce('button','btn','بازی جدید');nb.setAttribute('data-smoke','1');nb.addEventListener('click',fresh);
  var bar=ce('div','ubar');bar.appendChild(rb);bar.appendChild(ab);bar.appendChild(nb);
  app.appendChild(ce('div','blabel','ناوگان تو — ناو انتخاب‌شده سرِ فهرست است؛ خانهٔ آغاز را لمس کن'));
  app.appendChild(boardEl(pg,false,placeClick));
  app.appendChild(bar);app.appendChild(chips);
 }else{
  var nb2=ce('button','btn','بازی جدید');nb2.setAttribute('data-smoke','1');nb2.addEventListener('click',fresh);
  var bar2=ce('div','ubar');bar2.appendChild(nb2);
  app.appendChild(ce('div','blabel','دریای ربات — لمس = شلیک'));
  app.appendChild(boardEl(eg,true,(phase==='battle'&&!lock)?shotClick:null));
  app.appendChild(ce('div','blabel','ناوگان تو'));
  app.appendChild(boardEl(pg,false,null));
  app.appendChild(bar2);
 }
 $('#hint').textContent=(phase==='place')?'ناو را از فهرست انتخاب کن، با دکمهٔ جهت افقی/عمودی‌اش کن و خانهٔ آغاز را لمس کن.':'روی دریای ربات شلیک کن؛ پس از هر شلیک، ربات هم شلیک می‌کند. همهٔ ۵ ناو حریف را غرق کن.';
}
function placeClick(r,c){
 if(phase!=='place'||sel>=FLEET.length)return;
 var f=FLEET[sel];
 if(L.canPlace(pg,r,c,f.l,hz)){L.place(pg,r,c,f.l,hz);sel++;render();hudUp();if(sel>=FLEET.length)startBattle()}
 else toast('اینجا جا نمی‌شود؛ جای دیگر یا جهت دیگر را امتحان کن');
}
function shotClick(r,c){
 if(lock||phase!=='battle')return;
 var res=L.shoot(eg,r,c);
 if(res.again){toast('قبلاً این‌جا شلیک کرده‌ای');return}
 if(res.sunk)toast('غرق شد! ناو '+fa(res.ship)+'تایی حریف به قعر رفت');
 else if(res.hit)toast('اصابت!');
 else toast('خیس شدی! خطا رفت');
 if(L.isFleetDead(eg)){phase='over';render();hudUp();ovl('پیروزی کامل!','ناوگان ربات کاملاً غرق شد','بازی دوباره',fresh);return}
 render();hudUp();
 lock=true;
 later(750,robotTurn);
}
function robotTurn(){
 var a=L.aiShoot(pa,Math.random),res=a?a[2]:null;
 if(L.isFleetDead(pg)){phase='over';render();hudUp();ovl('شکست دریایی','ناوگان تو غرق شد','بازی دوباره',fresh);return}
 if(res){
  if(res.sunk)toast('ربات: ناو '+fa(res.ship)+'تایی‌ات غرق شد!');
  else if(res.hit)toast('ربات: اصابت زد!');
  else toast('ربات: خطا رفت');
 }
 lock=false;render();hudUp();
}
fresh();hudUp();
"""

BS_CSS = r"""
body{background:#0b1220;color:#e8e6df;font-family:Tahoma,'Segoe UI',sans-serif;margin:0;padding:12px}
.wog-home{color:#3fb8af;font-size:12px;text-decoration:none}
header h1{color:#d9a441;font-size:20px;margin:6px 0;text-align:center}
#hud{color:#3fb8af;font-size:14px;text-align:center}
.bsboard{display:grid;grid-template-columns:repeat(10,1fr);gap:2px;direction:ltr;max-width:440px;margin:8px auto}
.bcell{min-height:min(8.4vw,34px);background:#14203a;border:1px solid #2a3b5e;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:15px;touch-action:manipulation}
.bcell.act{cursor:pointer}
.bcell.act:hover{border-color:#d9a441}
.shp{background:#1f3357;border-color:#33507e}
.hit{color:#e26d5c;font-weight:bold}
.snk{color:#e26d5c;background:#3a1f24;font-weight:bold}
.mis{color:#8fa3c7}
.bchips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:8px}
.bchip{background:#14203a;border:1px solid #2a3b5e;border-radius:8px;padding:6px 10px;font-size:13px}
.bchip.selc{border-color:#d9a441;color:#d9a441}
.blabel{text-align:center;color:#8fa3c7;font-size:13px;margin-top:10px}
.ubar{display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:8px}
.btn{min-height:44px;min-width:44px;padding:8px 16px;border-radius:10px;border:1px solid #33507e;background:#1b2c4f;color:#e8e6df;font-size:15px;cursor:pointer;touch-action:manipulation}
.btn.prime{background:#d9a441;color:#14203a;border-color:#d9a441;font-weight:bold}
#wog-toast{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);background:#1b2c4f;color:#e8e6df;padding:8px 14px;border-radius:8px;border:1px solid #33507e;font-size:14px;pointer-events:none;z-index:9}
p#hint{color:#8fa3c7;text-align:center;font-size:13px}
"""

BS_TESTS = [
("اعتبارسنجی چیدمان", r"""
var g=L.emptyGrid();
T.ok(L.canPlace(g,0,0,5,true),'horizontal in bounds');
T.ok(L.canPlace(g,5,5,5,false),'vertical in bounds');
T.ok(!L.canPlace(g,0,6,5,true),'horizontal overflow rejected');
T.ok(!L.canPlace(g,6,0,5,false),'vertical overflow rejected');
T.ok(!L.canPlace(g,-1,0,2,true),'negative row rejected');
T.ok(!L.canPlace(g,9,9,2,true),'corner overflow rejected');
L.place(g,0,0,5,true);
T.ok(!L.canPlace(g,0,0,2,true),'overlap head rejected');
T.ok(!L.canPlace(g,0,4,2,true),'overlap tail rejected');
T.ok(L.canPlace(g,1,0,2,true),'adjacent row allowed');
"""),
("اصابت، غرق و ناوگان مرده", r"""
var g=L.emptyGrid();
L.place(g,0,0,2,true);L.place(g,3,3,3,false);
var m=L.shoot(g,9,9);
T.eq([m.hit,m.sunk,m.ship],[false,false,0],'miss report');
var h1=L.shoot(g,0,0);
T.eq([h1.hit,h1.sunk,h1.ship],[true,false,2],'partial hit report');
var h2=L.shoot(g,0,1);
T.eq([h2.hit,h2.sunk,h2.ship],[true,true,2],'sunk report with ship length');
T.ok(!L.isFleetDead(g),'fleet still alive');
L.shoot(g,3,3);L.shoot(g,4,3);
var v3=L.shoot(g,5,3);
T.ok(v3.sunk,'vertical ship sunk');
T.ok(L.isFleetDead(g),'whole fleet dead');
var again=L.shoot(g,0,0);
T.ok(again.again===true,'repeat shot flagged');
"""),
("چیدمان خودکار معتبر", r"""
var g=L.emptyGrid();
T.ok(L.autoPlace(g,rng),'auto place succeeded');
var counts={},total=0,y,x;
for(y=0;y<10;y++)for(x=0;x<10;x++){var sid=g[y][x].s;if(sid){counts[sid]=(counts[sid]||0)+1;total++}}
var lens=[];for(var k in counts)lens.push(counts[k]);
lens.sort(function(a,b){return a-b});
T.eq(lens,[2,3,3,4,5],'five distinct ships 5/4/3/3/2');
T.eq(total,17,'exactly 17 ship cells');
"""),
("هدف‌گیری بعد از اصابت", r"""
var g=L.emptyGrid();L.place(g,0,0,5,true);
var st=L.aiNew(g);st.tg=[[0,2]];
var a1=L.aiShoot(st,rng);
T.eq([a1[0],a1[1]],[0,2],'forced target shot fired');
T.ok(a1[2].hit,'forced shot hits');
var a2=L.aiShoot(st,rng);
T.eq(Math.abs(a2[0]-0)+Math.abs(a2[1]-2),1,'follow-up is adjacent to hit');
if(!a2[2].hit){var a3=L.aiShoot(st,rng);T.ok(a3[2].hit,'next target shot hits the ship line');}
"""),
("پوشش کامل بدون شلیک تکراری", r"""
var g=L.emptyGrid();
L.place(g,0,0,5,true);L.place(g,2,0,4,true);L.place(g,4,0,3,true);L.place(g,6,0,3,true);L.place(g,8,0,2,true);
var st=L.aiNew(g),seen={},n=0;
for(var i=0;i<2000;i++){
 var s1=L.aiShoot(st,rng);
 if(!s1)break;
 var key=s1[0]*10+s1[1];
 T.ok(!seen[key],'no repeated shot');
 T.ok(s1[0]>=0&&s1[0]<10&&s1[1]>=0&&s1[1]<10,'shot in bounds');
 seen[key]=1;n++;
}
T.eq(n,100,'all 100 cells covered uniquely');
var shipCells=[[0,0],[0,1],[0,2],[0,3],[0,4],[2,0],[2,1],[2,2],[2,3],[4,0],[4,1],[4,2],[6,0],[6,1],[6,2],[8,0],[8,1]];
for(var j=0;j<shipCells.length;j++)T.ok(seen[shipCells[j][0]*10+shipCells[j][1]],'ship cell was shot: '+j);
"""),
("بازی کامل تا برنده", r"""
function freshFleet(){var g=L.emptyGrid();if(!L.autoPlace(g,rng))throw new Error('place fail');return g}
var gA=freshFleet(),gB=freshFleet();
var pa=L.aiNew(gB),pb=L.aiNew(gA);
var turn=0,winner=-1;
for(var i=0;i<600;i++){
 var st=turn===0?pa:pb;
 var s1=L.aiShoot(st,rng);
 if(!s1)break;
 var victim=turn===0?gB:gA;
 if(L.isFleetDead(victim)){winner=turn;break}
 turn=1-turn;
}
T.ok(winner===0||winner===1,'a winner was declared');
T.ok(L.isFleetDead(gA)||L.isFleetDead(gB),'one fleet fully sank');
"""),
]

# ============================== PENTAGO ==============================
PG_LOGIC = r"""
function initial(){var b=[],i;for(i=0;i<36;i++)b.push(0);return{b:b,t:1}}
function place(s,r,c,pl){
 if(!(r>=0&&r<6&&c>=0&&c<6))throw new Error('out of board');
 if(s.b[r*6+c]!==0)throw new Error('cell occupied');
 var b=s.b.slice();b[r*6+c]=pl;return{b:b,t:s.t};
}
function rotate(s,q,dir){
 var b=s.b.slice(),qr=q>1?3:0,qc=q%2?3:0,lr,lc;
 for(lr=0;lr<3;lr++)for(lc=0;lc<3;lc++){
  var v=s.b[(qr+lr)*6+(qc+lc)],nr,nc;
  if(dir===1){nr=lc;nc=2-lr}else{nr=2-lc;nc=lr}
  b[(qr+nr)*6+(qc+nc)]=v;
 }
 return{b:b,t:s.t};
}
function winAt(s){
 var b=s.b,r,c,v;
 for(r=0;r<6;r++)for(c=0;c<2;c++){v=b[r*6+c];if(v&&b[r*6+c+1]===v&&b[r*6+c+2]===v&&b[r*6+c+3]===v&&b[r*6+c+4]===v)return v}
 for(c=0;c<6;c++)for(r=0;r<2;r++){v=b[r*6+c];if(v&&b[(r+1)*6+c]===v&&b[(r+2)*6+c]===v&&b[(r+3)*6+c]===v&&b[(r+4)*6+c]===v)return v}
 for(r=0;r<2;r++)for(c=0;c<2;c++){v=b[r*6+c];if(v&&b[(r+1)*6+c+1]===v&&b[(r+2)*6+c+2]===v&&b[(r+3)*6+c+3]===v&&b[(r+4)*6+c+4]===v)return v}
 for(r=4;r<6;r++)for(c=0;c<2;c++){v=b[r*6+c];if(v&&b[(r-1)*6+c+1]===v&&b[(r-2)*6+c+2]===v&&b[(r-3)*6+c+3]===v&&b[(r-4)*6+c+4]===v)return v}
 return 0;
}
function empties(s){var out=[],i;for(i=0;i<36;i++)if(s.b[i]===0)out.push([(i/6)|0,i%6]);return out}
function oppCanWin(s,op){
 var es=empties(s),i,q,d;
 for(i=0;i<es.length;i++){
  var s2=place(s,es[i][0],es[i][1],op);
  for(q=0;q<4;q++)for(d=-1;d<=1;d+=2)if(winAt(rotate(s2,q,d))===op)return true;
 }
 return false;
}
function aiMove(s,rng){
 var r=rng||Math.random,me=s.t,op=-me,es=empties(s),i,q,d;
 if(!es.length)return null;
 for(i=0;i<es.length;i++){
  var s2=place(s,es[i][0],es[i][1],me);
  for(q=0;q<4;q++)for(d=-1;d<=1;d+=2)if(winAt(rotate(s2,q,d))===me)return{r:es[i][0],c:es[i][1],q:q,dir:d};
 }
 var threats=[];
 for(i=0;i<es.length;i++){
  var s3=place(s,es[i][0],es[i][1],op),found=false;
  for(q=0;q<4&&!found;q++)for(d=-1;d<=1;d+=2)if(winAt(rotate(s3,q,d))===op){found=true;break}
  if(found)threats.push(es[i]);
 }
 for(i=0;i<threats.length;i++){
  var s4=place(s,threats[i][0],threats[i][1],me);
  for(q=0;q<4;q++)for(d=-1;d<=1;d+=2){
   var s5=rotate(s4,q,d);
   if(winAt(s5)!==op&&!oppCanWin(s5,op))return{r:threats[i][0],c:threats[i][1],q:q,dir:d};
  }
 }
 var ws=[],tot=0;
 for(i=0;i<es.length;i++){var w=3-Math.max(Math.abs(es[i][0]-2.5),Math.abs(es[i][1]-2.5));ws.push(w);tot+=w}
 var x=r()*tot,idx=es.length-1;
 for(i=0;i<es.length;i++){x-=ws[i];if(x<=0){idx=i;break}}
 return{r:es[idx][0],c:es[idx][1],q:(r()*4)|0,dir:r()<0.5?1:-1};
}
var WOG_LOGIC={initial:initial,place:place,rotate:rotate,winAt:winAt,aiMove:aiMove,empties:empties,oppCanWin:oppCanWin};
"""

PG_UI = r"""
var ps=null,phase='place',selQ=-1,lock=false,gen=0;
function qOf(r,c){return (r<3?0:2)+(c<3?0:1)}
function counts(){var a=0,b=0,i;for(i=0;i<36;i++){if(ps.b[i]===1)a++;if(ps.b[i]===-1)b++}return[a,b]}
function later(ms,fn){var g0=gen;setTimeout(function(){if(g0===gen)fn()},ms)}
function hudUp(){var c=counts();hud('نوبت: <b>'+(ps.t===1?'تو':'ربات')+'</b> · سنگ‌ها — تو: '+fa(c[0])+' / ربات: '+fa(c[1]))}
function fresh(){gen++;ps=L.initial();phase='place';selQ=-1;lock=false;render();hudUp()}
function finishTurn(){
 var w=L.winAt(ps);
 if(w!==0){phase='over';render();hudUp();if(w===1)ovl('بردی!','پنج‌تایی ساختی','بازی دوباره',fresh);else ovl('ربات برد','پنج‌تاییِ ربات کامل شد','بازی دوباره',fresh);return}
 var full=true,i;for(i=0;i<36;i++)if(ps.b[i]===0){full=false;break}
 if(full){phase='over';render();hudUp();ovl('مساوی','صفحه پر شد و پنج‌تایی‌ای شکل نگرفت','بازی دوباره',fresh);return}
 ps.t=-ps.t;
 if(ps.t===-1){lock=true;render();hudUp();later(700,aiGo)}
 else{phase='place';selQ=-1;lock=false;render();hudUp()}
}
function aiGo(){
 var mv=L.aiMove(ps,Math.random);
 if(!mv){lock=false;phase='place';render();hudUp();return}
 ps=L.place(ps,mv.r,mv.c,-1);
 ps=L.rotate(ps,mv.q,mv.dir);
 toast('ربات سنگ گذاشت و ربع '+fa(mv.q+1)+' را چرخاند');
 finishTurn();
}
function doRot(dir){
 if(lock||phase!=='rotate')return;
 if(selQ<0){toast('اول یک ربع را لمس کن');return}
 ps=L.rotate(ps,selQ,dir);
 selQ=-1;
 finishTurn();
}
function cellClick(i){
 if(lock||phase==='over')return;
 var r=(i/6)|0,c=i%6;
 if(phase==='place'&&ps.t===1&&ps.b[i]===0){
  ps=L.place(ps,r,c,1);
  phase='rotate';selQ=-1;
  toast('حالا ربعی را برای چرخش لمس کن');
  render();hudUp();return;
 }
 if(phase==='rotate'){selQ=qOf(r,c);render();return}
 if(ps.b[i]!==0)toast('این خانه پر است');
}
function render(){
 var app=$('#app');app.innerHTML='';
 var bd=ce('div','pboard');
 for(var i=0;i<36;i++){
  var r=(i/6)|0,c=i%6,q=qOf(r,c);
  var d=ce('div','pcell q'+q);
  if(ps.b[i]===1)d.appendChild(ce('span','st s1','●'));
  else if(ps.b[i]===-1)d.appendChild(ce('span','st s2','●'));
  else if(phase==='place'&&ps.t===1&&!lock)d.classList.add('free');
  if(phase==='rotate'&&q===selQ)d.classList.add('qsel');
  d.addEventListener('click',function(ii){return function(){cellClick(ii)}}(i));
  bd.appendChild(d);
 }
 var bar=ce('div','ubar');
 var nb=ce('button','btn','بازی جدید');nb.setAttribute('data-smoke','1');nb.addEventListener('click',fresh);bar.appendChild(nb);
 if(phase==='rotate'){
  var cw=ce('button','btn prime','↻ راست‌گرد');cw.setAttribute('data-smoke','1');
  var ccw=ce('button','btn prime','↺ چپ‌گرد');ccw.setAttribute('data-smoke','1');
  cw.addEventListener('click',function(){doRot(1)});ccw.addEventListener('click',function(){doRot(-1)});
  bar.appendChild(cw);bar.appendChild(ccw);
 }
 app.appendChild(bd);app.appendChild(bar);
 $('#hint').textContent='اول خانهٔ خالی را لمس، بعد ربع دلخواه و جهت چرخش را بزن. پنج سنگ پشت‌سرهم در هر جهتی (حتی روی مرز ربع‌ها) برنده است.';
}
fresh();hudUp();
"""

PG_CSS = r"""
body{background:#0b1220;color:#e8e6df;font-family:Tahoma,'Segoe UI',sans-serif;margin:0;padding:12px}
.wog-home{color:#3fb8af;font-size:12px;text-decoration:none}
header h1{color:#d9a441;font-size:20px;margin:6px 0;text-align:center}
#hud{color:#3fb8af;font-size:14px;text-align:center}
.pboard{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;direction:ltr;max-width:520px;margin:10px auto}
.pcell{min-height:56px;background:#14203a;border:1px solid #2a3b5e;border-radius:8px;display:flex;align-items:center;justify-content:center;touch-action:manipulation}
.q0{background:#14203a}.q1{background:#152845}.q2{background:#101d34}.q3{background:#16294a}
.qsel{outline:3px solid #d9a441}
.free{cursor:pointer;border-color:#33507e}
.free:hover{border-color:#d9a441}
.st{font-size:26px;line-height:1}
.s1{color:#d9a441}.s2{color:#3fb8af}
.ubar{display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:wrap;margin-top:8px}
.btn{min-height:44px;min-width:44px;padding:8px 16px;border-radius:10px;border:1px solid #33507e;background:#1b2c4f;color:#e8e6df;font-size:15px;cursor:pointer;touch-action:manipulation}
.btn.prime{background:#d9a441;color:#14203a;border-color:#d9a441;font-weight:bold}
#wog-toast{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);background:#1b2c4f;color:#e8e6df;padding:8px 14px;border-radius:8px;border:1px solid #33507e;font-size:14px;pointer-events:none;z-index:9}
p#hint{color:#8fa3c7;text-align:center;font-size:13px}
"""

PG_TESTS = [
("چرخش صحیح ربع‌ها", r"""
var s=L.initial();
s.b[0]=1;s.b[1]=1;s.b[6]=1;s.b[7]=1;s.b[8]=1;
var cw=L.rotate(s,0,1);
T.eq(cw.b.slice(0,15),[0,1,1,0,0,0,0,1,1,0,0,0,0,1,0],'clockwise 90 matrix');
var ccw=L.rotate(s,0,-1);
T.eq(ccw.b.slice(0,15),[0,1,0,0,0,0,1,1,0,0,0,0,1,1,0],'counter-clockwise 90 matrix');
var s3=L.initial();s3.b[21]=1;
var rq=L.rotate(s3,3,1);
T.eq(rq.b[23],1,'q3 cw moves stone to (3,5)');
T.eq(rq.b[21],0,'old cell cleared');
T.eq(s3.b[21],1,'rotate is pure (source untouched)');
var half=L.rotate(L.rotate(s,0,1),0,1);
T.eq(half.b.slice(0,15),[0,0,0,0,0,0,1,1,1,0,0,0,0,1,1],'double rotation equals 180');
T.ok(L.rotate(s,1,1).b[0]===1&&L.rotate(s,2,1).b[0]===1,'other quadrants intact');
"""),
("پنج‌تایی روی مرز ربع‌ها", r"""
T.eq(L.winAt(L.initial()),0,'empty board no win');
var s=L.initial();
s.b[13]=1;s.b[14]=1;s.b[15]=1;s.b[16]=1;s.b[17]=1;
T.eq(L.winAt(s),1,'five in row across q0/q1 border');
var s2=L.initial();
s2.b[0]=-1;s2.b[7]=-1;s2.b[14]=-1;s2.b[21]=-1;s2.b[28]=-1;
T.eq(L.winAt(s2),-1,'diagonal across all four quadrants');
var s3=L.initial();
s3.b[0]=1;s3.b[7]=1;s3.b[14]=1;s3.b[21]=1;
T.eq(L.winAt(s3),0,'four in row is not a win');
"""),
("برد فوری ربات", r"""
var s=L.initial();
s.b[13]=-1;s.b[14]=-1;s.b[15]=-1;s.b[16]=-1;s.t=-1;
var mv=L.aiMove(s,rng);
T.ok(mv&&mv.r>=0&&mv.r<6&&mv.c>=0&&mv.c<6&&mv.q>=0&&mv.q<4,'ai move well formed');
var s2=L.rotate(L.place(s,mv.r,mv.c,-1),mv.q,mv.dir);
T.eq(L.winAt(s2),-1,'AI completes five in one move');
"""),
("دفاع ربات در برابر تهدید", r"""
var s=L.initial();
s.b[12]=1;s.b[13]=1;s.b[14]=1;s.b[15]=1;s.t=-1;
var mv=L.aiMove(s,rng);
var s2=L.rotate(L.place(s,mv.r,mv.c,-1),mv.q,mv.dir);
var oppWin=false,i,q,d;
for(i=0;i<36&&!oppWin;i++){
 if(s2.b[i]!==0)continue;
 var s3=L.place(s2,(i/6)|0,i%6,1);
 for(q=0;q<4&&!oppWin;q++)for(d=-1;d<=1;d+=2)if(L.winAt(L.rotate(s3,q,d))===1){oppWin=true;break}
}
T.ok(!oppWin,'human has no immediate win after AI move');
"""),
("بازی AI مقابل AI", r"""
var s=L.initial(),plies=0,w=0,full=false;
while(plies<40&&!full&&w===0){
 var mv=L.aiMove(s,rng);
 if(!mv)break;
 s=L.rotate(L.place(s,mv.r,mv.c,s.t),mv.q,mv.dir);
 s.t=-s.t;plies++;
 w=L.winAt(s);
 full=true;
 for(var i=0;i<36;i++)if(s.b[i]===0){full=false;break}
}
T.ok(plies<=40,'terminated in '+plies+' plies');
T.ok(w!==0||full,'decisive winner or draw on full board');
"""),
("رد حرکت نامعتبر", r"""
var s0=L.initial();
var s=L.place(s0,0,0,1);
T.throws(function(){L.place(s,0,0,-1)},'occupied cell rejected');
T.throws(function(){L.place(s,6,0,1)},'row out of range rejected');
T.throws(function(){L.place(s,0,6,1)},'col out of range rejected');
var s2=L.place(s,0,1,-1);
T.eq(s2.b[1],-1,'valid place works');
T.eq(s0.b[0],0,'original state untouched (pure)');
"""),
]

GAMES = [
    G(slug="game-of-ur", title="بازی سلطنتی اور", cat="board", icon="⚄", g1="#d9a441", g2="#3fb8af",
      desc="نژاد کهن سلطنتی اور بین تو و ربات: با تاس‌های چهارگانه مهره‌ها را از مسیر ۲۰ خانه‌ای عبور بده و زودتر از حریف هر ۷ مهره را بیرون بفرست.",
      hint="تاس بریز و مهره‌ای را لمس که دقیقاً به اندازهٔ تاس جلو می‌رود؛ روزت امن است و نوبت اضافه می‌دهد و در ناحیهٔ مشترک می‌توانی مهرهٔ تک حریف را بگیری.",
      logic=UR_LOGIC, ui=UR_UI, css=UR_CSS, engines=("common",), tests=UR_TESTS),
    G(slug="battleship", title="نبرد دریایی", cat="board", icon="⚑", g1="#4a7fb5", g2="#e26d5c",
      desc="ناوگان پنج‌ناوی‌ات را روی شبکهٔ ۱۰×۱۰ بچین (دستی یا خودکار) و با شلیک خانه‌به‌خانه ناوگان پنهان ربات را یکی‌یکی غرق کن.",
      hint="در چیدمان: ناو را از فهرست انتخاب، جهت را بچرخان و خانهٔ آغاز را لمس کن؛ در نبرد روی دریای ربات شلیک کن تا اصابت/غرق ببینی.",
      logic=BS_LOGIC, ui=BS_UI, css=BS_CSS, engines=("common",), tests=BS_TESTS),
    G(slug="pentago", title="پنتاگو", cat="board", icon="❖", g1="#d9a441", g2="#67b98a",
      desc="پنتاگو روی صفحهٔ ۶×۶ با چهار ربع چرخان: سنگ بگذار، یک ربع را بچرخان؛ اولین پنج‌تاییِ پشت‌سرهم در هر جهت برنده است.",
      hint="خانهٔ خالی را لمس، بعد ربع دلخواه و جهت چرخش را انتخاب کن؛ مراقب پنج‌تاییِ ربات باش.",
      logic=PG_LOGIC, ui=PG_UI, css=PG_CSS, engines=("common",), tests=PG_TESTS),
]
