# -*- coding: utf-8 -*-
# AG-E2: 3 puzzle games (flood-it, peg solitaire, blockudoku) - WOG mini-kit batch
from lib_mini import G

FLOOD_LOGIC = r"""
var WOG_LOGIC=(function(){
function genBoard(n,colors,rng){var R=rng||Math.random,b=[],i,j,c;
 for(i=0;i<n;i++){var row=[];for(j=0;j<n;j++){c=Math.floor(R()*colors);
  if(i>0&&R()<0.6)c=b[i-1][j];else if(j>0&&R()<0.6)c=row[j-1];
  row.push(c);}b.push(row);}
 return b;}
function region(b){var n=b.length,t=b[0][0],seen={},out=[],st=[[0,0]];
 while(st.length){var p=st.pop(),r=p[0],c=p[1];
  if(r<0||c<0||r>=n||c>=n||b[r][c]!==t)continue;
  var k=r+'_'+c;if(seen[k])continue;seen[k]=1;out.push([r,c]);
  st.push([r-1,c],[r+1,c],[r,c-1],[r,c+1]);}
 return out;}
function regionSize(b){return region(b).length;}
function applyColor(b,color){var reg=region(b),nb=b.map(function(x){return x.slice();}),i;
 for(i=0;i<reg.length;i++)nb[reg[i][0]][reg[i][1]]=color;
 return nb;}
function isWin(b){var t=b[0][0],i,j;
 for(i=0;i<b.length;i++)for(j=0;j<b[i].length;j++)if(b[i][j]!==t)return false;
 return true;}
function greedySteps(b,colors){var g=b.map(function(x){return x.slice();}),steps=0;
 while(!isWin(g)&&steps<200){var cur=g[0][0],best=-1,bs=-1,c;
  for(c=0;c<colors;c++){if(c===cur)continue;
   var sz=regionSize(applyColor(g,c));if(sz>bs){bs=sz;best=c;}}
  g=applyColor(g,best);steps++;}
 return steps;}
return{genBoard:genBoard,region:region,regionSize:regionSize,applyColor:applyColor,isWin:isWin,greedySteps:greedySteps};
})();
"""

FLOOD_UI = r"""
var N=14,COLORS=6,BUDGET=25;
var COL=['#e26d5c','#d9a441','#67b98a','#3fb8af','#5b7bd5','#b06ad4'];
var board,moves,over;
var app=$('#app');app.innerHTML='';
var grid=ce('div','fgrid'),pal=ce('div','fpal'),foot=ce('div','ffoot');
var bNew=ce('button','wbtn','بازی جدید');bNew.setAttribute('data-smoke','1');
foot.appendChild(bNew);
app.appendChild(grid);app.appendChild(pal);app.appendChild(foot);
$('#hint').textContent='رنگی را انتخاب کن تا ناحیهٔ گوشهٔ بالا-چپ همرنگ و بزرگ شود؛ یک‌رنگ شدن کل صفحه یعنی برد.';
var cells=[],i,r,c;
for(i=0;i<N*N;i++){var d=ce('div','fc');cells.push(d);grid.appendChild(d);}
for(c=0;c<COLORS;c++)(function(cc){var b=ce('button','fpb');b.style.background=COL[cc];
 b.addEventListener('click',function(){move(cc);});pal.appendChild(b);})(c);
function paint(){for(r=0;r<N;r++)for(c=0;c<N;c++)cells[r*N+c].style.background=COL[board[r][c]];}
function hudUp(){var pc=Math.round(L.regionSize(board)*100/(N*N));
 hud('منطقه: <b>'+fa(pc)+'٪</b> · حرکت باقی‌مانده: <b>'+fa(moves)+'</b>');}
function move(cc){if(over)return;
 if(board[0][0]===cc){toast('ناحیهٔ فعال همین رنگ است');return;}
 board=L.applyColor(board,cc);moves--;
 if(L.isWin(board)){over=true;paint();hudUp();finish(true);return;}
 if(moves<=0){over=true;paint();hudUp();finish(false);return;}
 paint();hudUp();}
function finish(w){var used=BUDGET-Math.max(moves,0),best=store.get('wog-flood-best'),msg='';
 if(w&&(best===null||used<parseInt(best,10))){store.set('wog-flood-best',used);msg=' رکورد جدید!';}
 ovl(w?'بردی!':'باختی!',w?'کل صفحه در '+fa(used)+' حرکت یک‌رنگ شد.'+msg:'حرکت‌ها تمام شد و صفحه یک‌رنگ نشد.','بازی جدید',function(){newGame();});}
function newGame(){board=L.genBoard(N,COLORS);moves=BUDGET;over=false;paint();hudUp();}
bNew.addEventListener('click',newGame);
newGame();
"""

FLOOD_CSS = r"""
.fgrid{display:grid;grid-template-columns:repeat(14,1fr);gap:2px;width:min(94vw,430px);margin:0 auto;touch-action:manipulation}
.fc{aspect-ratio:1;border-radius:3px}
.fpal{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:12px}
.fpb{width:46px;height:46px;border:none;border-radius:10px;cursor:pointer;box-shadow:0 2px 0 rgba(0,0,0,.45);touch-action:manipulation}
.ffoot{display:flex;justify-content:center;margin-top:12px}
.wbtn{background:#d9a441;color:#14203a;border:none;border-radius:10px;padding:10px 18px;font-weight:700;cursor:pointer;min-height:40px;touch-action:manipulation;font-size:15px}
"""

FLOOD_TESTS=[
("region و applyColor روی تختهٔ ۳×۳",
r"""
var b=[[0,0,1],[0,1,1],[2,2,1]];
var reg=L.region(b);
T.eq(reg.length,3,'region size 3');
T.ok(JSON.stringify(reg).indexOf('[0,0]')>=0,'origin included');
var b2=L.applyColor(b,2);
T.eq(b2,[[2,2,1],[2,1,1],[2,2,1]],'region recolored');
T.eq(b,[[0,0,1],[0,1,1],[2,2,1]],'input board untouched');
T.ok(!L.isWin(b2),'not won yet');
T.ok(L.isWin(L.applyColor(b2,1)),'second color merges to monochrome');
"""),
("تشخیص برد isWin",
r"""
T.ok(L.isWin([[3,3],[3,3]]),'monochrome true');
T.ok(!L.isWin([[3,3],[3,1]]),'mixed false');
T.ok(!L.isWin([[0,0],[0,1]]),'one different cell false');
T.ok(L.isWin(L.genBoard(1,6,rng)),'1x1 board always win');
"""),
("سی تختهٔ seed شده: ساخت درست و گریزی ≤ ۲۵",
r"""
var bad=0,maxS=0;
for(var i=0;i<30;i++){var b=L.genBoard(14,6,rng);
 T.ok(b.length===14&&b[0].length===14&&b[13][13]!==undefined,'14x14 board '+i);
 var okv=true,r,c;
 for(r=0;r<14;r++)for(c=0;c<14;c++)if(!(b[r][c]>=0&&b[r][c]<6))okv=false;
 T.ok(okv,'palette range board '+i);
 var s=L.greedySteps(b,6);
 if(s>25)bad++;
 if(s>maxS)maxS=s;
 T.ok(L.regionSize(b)>=1,'region at least origin');}
T.eq(bad,0,'all 30 boards solvable within 25 greedy moves');
T.ok(maxS>0&&maxS<=25,'max greedy steps seen: '+maxS);
"""),
("حسابداری حرکت: رشد یکنوای ناحیه و بودجهٔ ۲۵",
r"""
var seed=987654321;
function lcg(){seed=(seed*48271)%2147483647;return (seed-1)/2147483646;}
var g=L.genBoard(14,6,lcg),budget=25,used=0,sz=L.regionSize(g);
while(!L.isWin(g)){var cur=g[0][0],best=-1,bs=-1,c;
 for(c=0;c<6;c++){if(c===cur)continue;
  var z=L.regionSize(L.applyColor(g,c));if(z>bs){bs=z;best=c;}}
 g=L.applyColor(g,best);used++;
 var ns=L.regionSize(g);
 T.ok(ns>=sz,'region never shrinks');
 T.ok(used<=budget,'never exceeds 25 moves');
 sz=ns;}
T.ok(L.isWin(g),'ends monochrome');
T.ok(budget-used>=0,'moves left non-negative');
seed=987654321;
var b0=L.genBoard(14,6,lcg);
T.eq(used,L.greedySteps(b0,6),'replay matches greedySteps on same seed');
"""),
]

PEG_LOGIC = r"""
var WOG_LOGIC=(function(){
var VALID=[],i,j;
for(i=0;i<7;i++)for(j=0;j<7;j++)if((i>=2&&i<=4)||(j>=2&&j<=4))VALID.push([i,j]);
function ok(r,c){return r>=0&&r<7&&c>=0&&c<7&&((r>=2&&r<=4)||(c>=2&&c<=4));}
function initial(){var s=[],r,c;
 for(r=0;r<7;r++){var row=[];
  for(c=0;c<7;c++)row.push(ok(r,c)?((r===3&&c===3)?0:1):-1);
  s.push(row);}
 return s;}
var DIRS=[[-1,0],[1,0],[0,-1],[0,1]];
function P(p){return (p&&p.length===2)?p:[p.r,p.c];}
function jumpsFrom(s,r,c){var out=[],d;
 if(!ok(r,c)||s[r][c]!==1)return out;
 for(d=0;d<4;d++){var mr=r+DIRS[d][0],mc=c+DIRS[d][1],tr=r+2*DIRS[d][0],tc=c+2*DIRS[d][1];
  if(ok(mr,mc)&&ok(tr,tc)&&s[mr][mc]===1&&s[tr][tc]===0)out.push([tr,tc]);}
 return out;}
function applyJump(s,from,to){var f=P(from),t=P(to),fr=f[0],fc=f[1],tr=t[0],tc=t[1];
 if(!ok(fr,fc)||!ok(tr,tc)||s[fr][fc]!==1||s[tr][tc]!==0)return false;
 var dr=tr-fr,dc=tc-fc;
 if(!((Math.abs(dr)===2&&dc===0)||(Math.abs(dc)===2&&dr===0)))return false;
 var mr=fr+dr/2,mc=fc+dc/2;
 if(s[mr][mc]!==1)return false;
 s[fr][fc]=0;s[mr][mc]=0;s[tr][tc]=1;return true;}
function pegCount(s){var n=0,r,c;for(r=0;r<7;r++)for(c=0;c<7;c++)if(s[r][c]===1)n++;return n;}
function hasMoves(s){var i;
 for(i=0;i<VALID.length;i++)if(jumpsFrom(s,VALID[i][0],VALID[i][1]).length)return true;
 return false;}
function isWin(s){return pegCount(s)===1;}
return{VALID:VALID,initial:initial,jumpsFrom:jumpsFrom,applyJump:applyJump,pegCount:pegCount,hasMoves:hasMoves,isWin:isWin};
})();
"""

PEG_UI = r"""
var st,sel=null,hist=[],over=false,cells=[];
var app=$('#app');app.innerHTML='';
var grid=ce('div','pgrid'),bar=ce('div','pbar');
var bUndo=ce('button','wbtn','برگردان'),bNew=ce('button','wbtn','بازی جدید');
bNew.setAttribute('data-smoke','1');
bar.appendChild(bUndo);bar.appendChild(bNew);
app.appendChild(grid);app.appendChild(bar);
$('#hint').textContent='یک پگ را لمس کن، سپس خانهٔ مقصد دو خانهٔ دورتر؛ پگ بین راه حذف می‌شود. هدف: فقط یک پگ، ترجیحاً مرکز.';
function build(){grid.innerHTML='';cells=[];var r,c;
 for(r=0;r<7;r++){cells.push([]);
  for(c=0;c<7;c++)(function(rr,cc){var d=ce('div','pcell');
   d.addEventListener('click',function(){tap(rr,cc);});
   cells[rr].push(d);grid.appendChild(d);})(r,c);}}
function paint(){var r,c,i,ts;
 for(r=0;r<7;r++)for(c=0;c<7;c++){var v=st[r][c];
  cells[r][c].className='pcell'+(v===-1?' pdead':(v===1?' peg':' hole'));}
 if(sel){cells[sel[0]][sel[1]].className+=' sel';
  ts=L.jumpsFrom(st,sel[0],sel[1]);
  for(i=0;i<ts.length;i++)cells[ts[i][0]][ts[i][1]].className+=' tgt';}}
function hudUp(){hud('پگ‌ها: <b>'+fa(L.pegCount(st))+'</b>'+(over?' · پایان':''));}
function tap(r,c){if(over)return;
 if(st[r][c]===1){var ts=L.jumpsFrom(st,r,c);
  if(!ts.length){toast('این پگ پرش ندارد');return;}
  sel=(sel&&sel[0]===r&&sel[1]===c)?null:[r,c];paint();return;}
 if(st[r][c]===0&&sel){var ts2=L.jumpsFrom(st,sel[0],sel[1]),hit=null,i;
  for(i=0;i<ts2.length;i++)if(ts2[i][0]===r&&ts2[i][1]===c)hit=ts2[i];
  if(!hit){toast('مقصد پرش معتبر نیست');return;}
  hist.push(st.map(function(x){return x.slice();}));
  L.applyJump(st,sel,hit);sel=null;paint();hudUp();
  if(L.isWin(st)){over=true;var perfect=st[3][3]===1;
   ovl('بردی!','فقط یک پگ باقی ماند'+(perfect?' و در مرکز است؛ عالی!':'.'),'بازی جدید',function(){newGame();});return;}
  if(!L.hasMoves(st)){over=true;
   ovl('گرفتار شدی','هیچ پرشی نمانده و '+fa(L.pegCount(st))+' پگ روی صفحه است.','بازی جدید',function(){newGame();});}
  return;}}
function newGame(){st=L.initial();sel=null;hist=[];over=false;build();paint();hudUp();}
bUndo.addEventListener('click',function(){if(over){toast('بازی تمام شده');return;}
 if(!hist.length){toast('چیزی برای برگرداندن نیست');return;}
 st=hist.pop();sel=null;paint();hudUp();});
bNew.addEventListener('click',newGame);
newGame();
"""

PEG_CSS = r"""
.pgrid{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;width:min(94vw,400px);margin:0 auto}
.pcell{aspect-ratio:1;border-radius:50%;touch-action:manipulation;cursor:pointer}
.pdead{visibility:hidden}
.hole{background:#14203a;box-shadow:inset 0 2px 5px rgba(0,0,0,.65)}
.peg{background:radial-gradient(circle at 35% 30%,#ecc672,#d9a441 55%,#8a5a2b);box-shadow:0 2px 4px rgba(0,0,0,.5)}
.peg.sel{outline:3px solid #3fb8af}
.hole.tgt{box-shadow:inset 0 2px 5px rgba(0,0,0,.65),0 0 0 3px #67b98a}
.pbar{display:flex;gap:10px;justify-content:center;margin-top:12px}
.wbtn{background:#d9a441;color:#14203a;border:none;border-radius:10px;padding:10px 18px;font-weight:700;cursor:pointer;min-height:40px;touch-action:manipulation;font-size:15px}
"""

PEG_TESTS=[
("قوانین پرش: جهت، فاصله، پگ میان‌راه",
r"""
function mk(pegs){var s=L.initial(),r,c,i;
 for(r=0;r<7;r++)for(c=0;c<7;c++)if(s[r][c]===1)s[r][c]=0;
 for(i=0;i<pegs.length;i++)s[pegs[i][0]][pegs[i][1]]=1;
 return s;}
var s=L.initial();
T.eq(L.jumpsFrom(s,3,1),[[3,3]],'only jump from (3,1) is into center');
var total=0,i;
for(i=0;i<L.VALID.length;i++)total+=L.jumpsFrom(s,L.VALID[i][0],L.VALID[i][1]).length;
T.eq(total,4,'exactly 4 opening jumps, all into center');
T.ok(L.applyJump(mk([[3,1],[3,2]]),[3,1],[3,3]),'legal jump accepted');
T.ok(!L.applyJump(mk([[3,1],[4,2]]),[3,1],[5,3]),'diagonal rejected');
T.ok(!L.applyJump(mk([[3,1],[3,2]]),[3,1],[3,2]),'distance 1 rejected');
T.ok(!L.applyJump(mk([[3,1],[3,2],[3,3]]),[3,1],[3,4]),'distance 3 rejected');
T.ok(!L.applyJump(mk([[3,1]]),[3,1],[3,3]),'empty middle rejected');
T.ok(!L.applyJump(mk([[3,1],[3,2],[3,3]]),[3,1],[3,3]),'occupied target rejected');
T.ok(!L.applyJump(mk([[3,1],[2,1]]),[3,1],[1,1]),'landing on dead cell rejected');
T.ok(!L.applyJump(mk([[3,2]]),[3,3],[3,1]),'empty source rejected');
"""),
("وضعیت اولیه: ۳۳ خانه، ۳۲ پگ، مرکز خالی",
r"""
var s=L.initial(),r,c,dead=0,live=0;
T.eq(L.VALID.length,33,'33 cross cells');
for(r=0;r<7;r++)for(c=0;c<7;c++){if(s[r][c]===-1)dead++;else live++;}
T.eq(dead,16,'16 dead corner cells');
T.eq(live,33,'33 playable cells');
T.eq(L.pegCount(s),32,'32 pegs');
T.ok(s[3][3]===0,'center empty');
T.ok(s[0][0]===-1&&s[1][1]===-1&&s[6][6]===-1,'corners dead');
T.ok(s[6][2]===1&&s[0][4]===1,'cross arms populated');
T.ok(L.hasMoves(s),'opening moves exist');
"""),
("هر پرش دقیقاً یک پگ کم می‌کند",
r"""
var s=L.initial(),p0=L.pegCount(s);
T.ok(L.applyJump(s,[1,3],[3,3]),'jump down into center');
T.eq(L.pegCount(s),p0-1,'peg count -1');
T.ok(s[1][3]===0&&s[2][3]===0&&s[3][3]===1,'source+middle emptied, target filled');
var before=L.pegCount(s);
T.ok(!L.applyJump(s,[3,3],[5,3]),'illegal jump rejected');
T.eq(L.pegCount(s),before,'rejected jump changes nothing');
T.ok(L.hasMoves(s),'game continues');
"""),
("فیکسچر دست‌ساز: پنج پرش تا یک پگ در مرکز",
r"""
var s=L.initial(),r,c,i;
for(r=0;r<7;r++)for(c=0;c<7;c++)if(s[r][c]===1)s[r][c]=0;
var pegs=[[3,1],[2,2],[1,3],[2,4],[3,5],[3,6]];
for(i=0;i<pegs.length;i++)s[pegs[i][0]][pegs[i][1]]=1;
T.eq(L.pegCount(s),6,'fixture has 6 pegs');
var seq=[[[3,6],[3,4]],[[3,4],[1,4]],[[1,4],[1,2]],[[1,2],[3,2]],[[3,1],[3,3]]];
for(i=0;i<seq.length;i++){T.ok(L.applyJump(s,seq[i][0],seq[i][1]),'jump '+(i+1)+' legal');
 T.eq(L.pegCount(s),5-i,'count after jump '+(i+1));}
T.ok(L.isWin(s),'exactly one peg remains');
T.ok(s[3][3]===1,'final peg at center');
"""),
("دویست پلیم تصادفی تا بن‌بست",
r"""
var i,j,k,okAll=true,minP=99,maxJ=0;
for(i=0;i<200&&okAll;i++){var s=L.initial(),jumps=0;
 while(L.hasMoves(s)){var opts=[];
  for(j=0;j<L.VALID.length;j++){var rr=L.VALID[j][0],cc=L.VALID[j][1];
   if(s[rr][cc]===1){var ts=L.jumpsFrom(s,rr,cc);
    for(k=0;k<ts.length;k++)opts.push([[rr,cc],ts[k]]);}}
  if(!opts.length)break;
  var o=opts[Math.floor(rng()*opts.length)],pc=L.pegCount(s);
  if(!L.applyJump(s,o[0],o[1])){okAll=false;break;}
  if(L.pegCount(s)!==pc-1){okAll=false;break;}
  jumps++;
  if(jumps>40){okAll=false;break;}}
 if(!L.hasMoves(s)){var p=L.pegCount(s);
  if(p<1)okAll=false;
  if(p<minP)minP=p;
  if(jumps>maxJ)maxJ=jumps;}}
T.ok(okAll,'all 200 playouts terminated cleanly');
T.ok(minP>=1,'final peg count never below 1 (min seen '+minP+')');
T.ok(maxJ>0&&maxJ<=31,'jump counts bounded (max '+maxJ+')');
"""),
("تشخیص بن‌بست بدون پرش",
r"""
function mk(pegs){var s=L.initial(),r,c,i;
 for(r=0;r<7;r++)for(c=0;c<7;c++)if(s[r][c]===1)s[r][c]=0;
 for(i=0;i<pegs.length;i++)s[pegs[i][0]][pegs[i][1]]=1;
 return s;}
var m=mk([[3,2],[3,4]]);
T.eq(L.hasMoves(m),false,'two separated pegs: stuck');
T.eq(L.isWin(m),false,'stuck but not a win');
var one=mk([[3,3]]);
T.eq(L.hasMoves(one),false,'single peg: no moves');
T.eq(L.isWin(one),true,'single peg: win');
T.eq(L.hasMoves(L.initial()),true,'fresh board has moves');
"""),
]

BLOCK_LOGIC = r"""
var WOG_LOGIC=(function(){
var SHAPES=[
 [[0,0]],
 [[0,0],[0,1]],[[0,0],[1,0]],
 [[0,0],[0,1],[0,2]],[[0,0],[1,0],[2,0]],
 [[0,0],[0,1],[0,2],[0,3]],[[0,0],[1,0],[2,0],[3,0]],
 [[0,0],[0,1],[0,2],[0,3],[0,4]],[[0,0],[1,0],[2,0],[3,0],[4,0]],
 [[0,0],[0,1],[1,0],[1,1]],
 [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]],
 [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1]],
 [[0,0],[1,0],[1,1]],
 [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
];
function cellsOf(sh){return (typeof sh==='number')?SHAPES[sh]:sh;}
function genPieces(n,rng){var R=rng||Math.random,out=[],i;
 for(i=0;i<n;i++)out.push(Math.floor(R()*SHAPES.length));
 return out;}
function canPlace(b,sh,r,c){var cs=cellsOf(sh),i;
 for(i=0;i<cs.length;i++){var rr=r+cs[i][0],cc=c+cs[i][1];
  if(rr<0||cc<0||rr>8||cc>8||b[rr][cc])return false;}
 return true;}
function place(b,sh,r,c){if(!canPlace(b,sh,r,c))return false;
 var cs=cellsOf(sh),i;
 for(i=0;i<cs.length;i++)b[r+cs[i][0]][c+cs[i][1]]=1;
 return true;}
function findClears(b){var rows=[],cols=[],blocks=[],r,c,k;
 for(r=0;r<9;r++){var f=1;for(c=0;c<9;c++)if(!b[r][c]){f=0;break;}if(f)rows.push(r);}
 for(c=0;c<9;c++){var g=1;for(r=0;r<9;r++)if(!b[r][c]){g=0;break;}if(g)cols.push(c);}
 for(k=0;k<9;k++){var br=(k/3|0)*3,bc=(k%3)*3,f2=1;
  for(r=0;r<3;r++)for(c=0;c<3;c++)if(!b[br+r][bc+c])f2=0;
  if(f2)blocks.push(k);}
 return {rows:rows,cols:cols,blocks:blocks};}
function applyClears(b,cl){var i,r,c;
 for(i=0;i<cl.rows.length;i++)for(c=0;c<9;c++)b[cl.rows[i]][c]=0;
 for(i=0;i<cl.cols.length;i++)for(r=0;r<9;r++)b[r][cl.cols[i]]=0;
 for(i=0;i<cl.blocks.length;i++){var br=(cl.blocks[i]/3|0)*3,bc=(cl.blocks[i]%3)*3;
  for(r=0;r<3;r++)for(c=0;c<3;c++)b[br+r][bc+c]=0;}
 return b;}
function anyFit(b,sh){var r,c;
 for(r=0;r<9;r++)for(c=0;c<9;c++)if(canPlace(b,sh,r,c))return true;
 return false;}
function isGameOver(b,pieces){var i;
 if(!pieces||!pieces.length)return false;
 for(i=0;i<pieces.length;i++)if(anyFit(b,pieces[i]))return false;
 return true;}
function moveGain(cells,lines,streak){return cells+10*lines+5*streak;}
return{SHAPES:SHAPES,genPieces:genPieces,canPlace:canPlace,place:place,findClears:findClears,applyClears:applyClears,anyFit:anyFit,isGameOver:isGameOver,moveGain:moveGain};
})();
"""

BLOCK_UI = r"""
var board,cells=[],trayEls=[],pieces,used,score,streak,over,sel,placedCells,linesTotal,streakSum;
var app=$('#app');app.innerHTML='';
var grid=ce('div','bgrid'),tray=ce('div','btray'),bar=ce('div','bbar');
var bNew=ce('button','wbtn','بازی جدید');bNew.setAttribute('data-smoke','1');
bar.appendChild(bNew);
app.appendChild(grid);app.appendChild(tray);app.appendChild(bar);
$('#hint').textContent='اول قطعه را انتخاب کن، بعد خانهٔ مقصد؛ لبهٔ بالا-چپ قطعه روی خانهٔ لمس‌شده می‌نشیند. سطر، ستون و بلوک ۳×۳ کامل پاک می‌شوند.';
function build(){grid.innerHTML='';cells=[];var r,c;
 for(r=0;r<9;r++){cells.push([]);
  for(c=0;c<9;c++)(function(rr,cc){var d=ce('div','bcell');
   d.addEventListener('click',function(){tap(rr,cc);});
   cells[rr].push(d);grid.appendChild(d);})(r,c);}}
function drawTray(){tray.innerHTML='';trayEls=[];
 for(var i=0;i<pieces.length;i++){var sh=L.SHAPES[pieces[i]];
  var card=ce('div','bcard'+(used[i]?' bused':'')+(sel===i?' bsel':''));
  var mr=0,mc=0,k;
  for(k=0;k<sh.length;k++){if(sh[k][0]>mr)mr=sh[k][0];if(sh[k][1]>mc)mc=sh[k][1];}
  var mini=ce('div','bmini');
  mini.style.gridTemplateColumns='repeat('+(mc+1)+',1fr)';
  for(var r2=0;r2<=mr;r2++)for(var c2=0;c2<=mc;c2++){var on=false;
   for(k=0;k<sh.length;k++)if(sh[k][0]===r2&&sh[k][1]===c2)on=true;
   mini.appendChild(ce('div','bdot'+(on?' on':'')));}
  card.appendChild(mini);
  (function(ii){card.addEventListener('click',function(){pick(ii);});})(i);
  tray.appendChild(card);trayEls.push(card);}}
function paint(){var r,c;
 for(r=0;r<9;r++)for(c=0;c<9;c++)cells[r][c].className='bcell'+(board[r][c]?' bfull':'');
 drawTray();hudUp();}
function pick(i){if(over)return;
 if(used[i]){toast('این قطعه استفاده شده');return;}
 sel=(sel===i)?-1:i;drawTray();}
function tap(r,c){if(over)return;
 if(sel<0){toast('اول یک قطعه انتخاب کن');return;}
 var sh=pieces[sel],size=L.SHAPES[sh].length;
 if(!L.canPlace(board,sh,r,c)){toast('اینجا جا نمی‌شود');return;}
 L.place(board,sh,r,c);used[sel]=1;sel=-1;placedCells+=size;
 var cl=L.findClears(board),nl=cl.rows.length+cl.cols.length+cl.blocks.length;
 if(nl>0){L.applyClears(board,cl);streak++;streakSum+=streak;linesTotal+=nl;
  toast(fa(nl)+' خط پاک شد!');}
 else streak=0;
 score+=L.moveGain(size,nl,streak);
 if(used[0]&&used[1]&&used[2]){pieces=L.genPieces(3);used=[0,0,0];}
 var rem=[],i;
 for(i=0;i<3;i++)if(!used[i])rem.push(pieces[i]);
 if(L.isGameOver(board,rem)){over=true;paint();finish();return;}
 paint();}
function finish(){var best=store.get('wog-blockudoku-best'),msg='';
 if(best===null||score>parseInt(best,10)){store.set('wog-blockudoku-best',score);msg=' رکورد جدید!';}
 ovl('پایان بازی','امتیاز تو: '+fa(score)+'؛ هیچ قطعه‌ای دیگر جا نشد.'+msg,'بازی جدید',function(){newGame();});}
function hudUp(){hud('امتیاز: <b>'+fa(score)+'</b> · استریک: <b>'+fa(streak)+'</b> · قطعه‌ها: <b>'+fa(used[0]+used[1]+used[2])+'/۳</b>');}
function newGame(){var r,c;board=[];
 for(r=0;r<9;r++){board.push([]);for(c=0;c<9;c++)board[r].push(0);}
 pieces=L.genPieces(3);used=[0,0,0];score=0;streak=0;over=false;sel=-1;
 placedCells=0;linesTotal=0;streakSum=0;
 build();paint();}
bNew.addEventListener('click',newGame);
newGame();
"""

BLOCK_CSS = r"""
.bgrid{display:grid;grid-template-columns:repeat(9,1fr);gap:2px;width:min(94vw,400px);margin:0 auto;background:#14203a;padding:6px;border-radius:10px}
.bcell{aspect-ratio:1;background:#0d1526;border-radius:3px;touch-action:manipulation}
.bcell.bfull{background:#3fb8af}
.btray{display:flex;gap:10px;justify-content:center;margin-top:12px;flex-wrap:wrap}
.bcard{background:#14203a;border:2px solid #24365c;border-radius:10px;padding:8px;min-width:52px;min-height:52px;display:flex;align-items:center;justify-content:center;cursor:pointer;touch-action:manipulation}
.bcard.bsel{border-color:#d9a441}
.bcard.bused{opacity:.25}
.bmini{display:grid;gap:2px}
.bdot{width:11px;height:11px;border-radius:2px}
.bdot.on{background:#d9a441}
.bbar{display:flex;justify-content:center;margin-top:12px}
.wbtn{background:#d9a441;color:#14203a;border:none;border-radius:10px;padding:10px 18px;font-weight:700;cursor:pointer;min-height:40px;touch-action:manipulation;font-size:15px}
"""

BLOCK_TESTS=[
("قراردهی: مرزها و برخورد",
r"""
function z(){var b=[],r,c;for(r=0;r<9;r++){b.push([]);for(c=0;c<9;c++)b[r].push(0);}return b;}
var b=z();
T.ok(L.canPlace(b,13,0,0),'3x3 at corner');
T.ok(!L.canPlace(b,13,7,7),'3x3 overflow rejected');
T.ok(!L.canPlace(b,8,5,0),'5x1 vertical overflow rejected');
T.ok(!L.canPlace(b,7,8,8),'1x5 horizontal overflow rejected');
T.ok(!L.canPlace(b,0,9,0),'row 9 rejected');
T.ok(L.canPlace(b,0,8,8),'1x1 at last cell ok');
T.ok(L.place(b,0,4,4),'place 1x1 at center');
T.ok(b[4][4]===1,'cell filled');
T.ok(!L.canPlace(b,0,4,4),'same spot rejected');
T.ok(!L.canPlace(b,1,4,4),'overlap rejected');
T.ok(L.canPlace(b,2,4,3),'adjacent ok');
T.ok(!L.place(b,13,8,8),'illegal place returns false');
T.ok(L.canPlace(b,13,0,0),'board unchanged after failed place');
"""),
("پاک‌سازی همزمان سطر، ستون و بلوک",
r"""
function z(){var b=[],r,c;for(r=0;r<9;r++){b.push([]);for(c=0;c<9;c++)b[r].push(0);}return b;}
var b=z(),r,c;
for(c=1;c<9;c++)b[0][c]=1;
for(r=1;r<9;r++)b[r][0]=1;
for(r=0;r<3;r++)for(c=0;c<3;c++)if(!(r===0&&c===0))b[r][c]=1;
var n=0;for(r=0;r<9;r++)for(c=0;c<9;c++)if(b[r][c])n++;
T.eq(n,20,'20 cells prefilled');
T.ok(L.place(b,0,0,0),'pivot placed at (0,0)');
var cl=L.findClears(b);
T.eq(cl.rows,[0],'row 0 full');
T.eq(cl.cols,[0],'col 0 full');
T.eq(cl.blocks,[0],'block 0 full');
L.applyClears(b,cl);
n=0;for(r=0;r<9;r++)for(c=0;c<9;c++)if(b[r][c])n++;
T.eq(n,0,'all 21 union cells cleared');
var b2=z();b2[4][4]=1;var cl2=L.findClears(b2);
T.eq(cl2.rows,[],'no full row');
T.eq(cl2.cols,[],'no full col');
T.eq(cl2.blocks,[],'no full block');
"""),
("ریاضی امتیاز: خانه‌ها + ۱۰×خط + ۵×استریک",
r"""
T.eq(L.moveGain(5,2,1),30,'5 cells + 2 lines + streak 1');
T.eq(L.moveGain(1,0,0),1,'plain placement');
T.eq(L.moveGain(4,1,1),19,'single line');
T.eq(L.moveGain(4,1,2),24,'streak 2 doubles bonus');
T.eq(L.moveGain(9,3,3),54,'triple clear with streak 3');
var seq=[[4,1],[3,1],[2,0],[5,2]],st=0,tot=0,i;
for(i=0;i<seq.length;i++){st=seq[i][1]>0?st+1:0;tot+=L.moveGain(seq[i][0],seq[i][1],st);}
T.eq(tot,74,'streak builds then resets: 19+23+2+30');
"""),
("تشخیص پایان بازی ساختگی",
r"""
function z(){var b=[],r,c;for(r=0;r<9;r++){b.push([]);for(c=0;c<9;c++)b[r].push(0);}return b;}
var b=z(),r,c;
for(r=0;r<9;r++)for(c=0;c<9;c++)b[r][c]=1;
T.ok(L.isGameOver(b,[0,9,13]),'full board: nothing fits');
T.ok(!L.isGameOver(b,[]),'no pieces: not over yet');
b[8][8]=0;
T.ok(L.isGameOver(b,[8,9,13]),'single hole too small for big pieces');
T.ok(!L.isGameOver(b,[0]),'1x1 still fits');
b[8][7]=0;
T.ok(!L.isGameOver(b,[1]),'1x2 fits horizontally');
"""),
("شبیه‌سازی صد قراردهی با حسابداری کامل",
r"""
var seed=424242;
function lcg(){seed=(seed*48271)%2147483647;return (seed-1)/2147483646;}
function z(){var b=[],r,c;for(r=0;r<9;r++){b.push([]);for(c=0;c<9;c++)b[r].push(0);}return b;}
var b=z(),pieces=L.genPieces(3,lcg),used=[false,false,false],gens=1;
var score=0,streak=0,streakSum=0,placed=0,placedCells=0,linesTotal=0,cleared=0,filled=0,ended=false;
function cf(){var n=0,r,c;for(r=0;r<9;r++)for(c=0;c<9;c++)if(b[r][c])n++;return n;}
for(var step=0;step<100;step++){
 if(used[0]&&used[1]&&used[2]){pieces=L.genPieces(3,lcg);used=[false,false,false];gens++;}
 var rem=[],i;
 for(i=0;i<3;i++)if(!used[i])rem.push(pieces[i]);
 if(L.isGameOver(b,rem)){ended=true;break;}
 var opts=[];
 for(i=0;i<3;i++){if(used[i])continue;
  for(var r=0;r<9;r++)for(var c=0;c<9;c++)if(L.canPlace(b,pieces[i],r,c))opts.push([i,r,c]);}
 T.ok(opts.length>0,'options exist when not game over (step '+step+')');
 var o=opts[Math.floor(lcg()*opts.length)],sh=pieces[o[0]],size=L.SHAPES[sh].length;
 T.ok(L.place(b,sh,o[1],o[2]),'placement '+step+' legal');
 used[o[0]]=true;placed++;placedCells+=size;
 var before=cf(),cl=L.findClears(b);
 var nl=cl.rows.length+cl.cols.length+cl.blocks.length;
 if(nl>0){L.applyClears(b,cl);streak++;streakSum+=streak;linesTotal+=nl;}
 else streak=0;
 score+=L.moveGain(size,nl,streak);
 var after=cf();
 cleared+=before-after;filled=after;
 T.eq(filled,placedCells-cleared,'filled == placedCells - cleared (step '+step+')');
 T.ok(filled>=0&&filled<=81,'cell count sane');}
T.ok(placed>=10&&placed<=100,'sim placements: '+placed+(ended?' (game over)':' (100 done)'));
T.eq(filled,placedCells-cleared,'final accounting');
var usedNow=0,i;
for(i=0;i<3;i++)if(used[i])usedNow++;
T.eq(placed,(gens-1)*3+usedNow,'piece consumption accounting');
T.eq(score,placedCells+10*linesTotal+5*streakSum,'score identity');
T.ok(score>0,'positive score');
"""),
]

flood=G(slug="flood",title="طوفان رنگی",cat="puzzle",icon="🌊",
 g1="#3fb8af",g2="#1b6e8f",
 desc="صفحهٔ ۱۴×۱۴ با شش رنگ؛ ناحیهٔ گوشهٔ بالا-چپ را با انتخاب رنگ‌ها بزرگ کن و در حداکثر ۲۵ حرکت کل صفحه را یک‌رنگ کن.",
 hint="رنگی بزن تا ناحیهٔ فعال همرنگ شود؛ حرکت‌ها را برای رنگ‌های پُرتکرار نگه دار.",
 engines=("common",),seed=42,logic=FLOOD_LOGIC,ui=FLOOD_UI,css=FLOOD_CSS,tests=FLOOD_TESTS)

peg=G(slug="peg",title="پگ سولیتر",cat="puzzle",icon="🔴",
 g1="#d9a441",g2="#8a5a2b",
 desc="پگ سولیتر کلاسیک روی صفحهٔ صلیبی ۳۳ خانه‌ای؛ با پرش از روی یک پگ آن را حذف کن تا در پایان فقط یک پگ — ترجیحاً در مرکز — بماند.",
 hint="پگ را لمس کن و دو خانهٔ دورتر روی خانهٔ خالی فرود بیا؛ برگردان و شروع دوباره داری.",
 engines=("common",),seed=77,logic=PEG_LOGIC,ui=PEG_UI,css=PEG_CSS,tests=PEG_TESTS)

blockudoku=G(slug="blockudoku",title="بلوک‌دوکو",cat="puzzle",icon="🧩",
 g1="#67b98a",g2="#2e6e5a",
 desc="قطعه‌ها را روی شبکهٔ ۹×۹ بچین؛ سطر، ستون یا بلوک ۳×۳ کامل پاک می‌شود و زنجیرهٔ پاک‌سازی امتیاز اضافه می‌دهد.",
 hint="اول قطعه را انتخاب کن، بعد خانهٔ مقصد؛ لبهٔ بالا-چپ قطعه روی خانهٔ لمس‌شده می‌نشیند.",
 engines=("common",),seed=99,logic=BLOCK_LOGIC,ui=BLOCK_UI,css=BLOCK_CSS,tests=BLOCK_TESTS)

GAMES=[flood,peg,blockudoku]
