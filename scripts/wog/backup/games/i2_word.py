# -*- coding: utf-8 -*-
import json
from lib_mini import G

def _norm(w):
    return w.replace("\u064A", "\u06CC").replace("\u0643", "\u06A9").replace(" ", "").replace("\u200c", "")

# واژه‌های پنهان واژه‌یاب (۵ تا ۷ حرف)
WS_WORDS=["سلامتی","موفقیت","دانشجو","دوستی","زندگی","کتابچه","پنجره","خورشید","درختان","آسمان","دریاچه","کوهستان","مهربانی","آزادی","گنجشک","پرندگان","باغبان","باران","نانوا","مدرسه","دوچرخه","نارنجی","پروانه","قناری","سنجاب","خلبان","کشاورز","راهنما","دانشمند","خلاقیت","توانایی","یادگیری","پایداری","شیرینی","گردشگر","تابستان","زمستان","مرغابی","زرافه","ستاره","بلدرچین","سفرنامه","سبزیجات","ماهیگیر","چمدان","مسافر","یخچال","صابون"]

# واژه‌نامهٔ واژه‌سازی (~۱۵۰ واژهٔ ۲ تا ۷ حرفی)
ANA_WORDS=["آب","او","بو","تو","گل","ما","من","نه","نی","یخ","یک","پل","جو","شب","ابر","اسب","باد","بار","برف","پدر","پسر","توپ","تاب","جام","چای","خام","خاک","دست","درس","رود","راه","سرد","سیل","شام","شیر","شتر","فیل","کوه","گاو","ماه","میز","مرغ","بهار","خانه","کتاب","کاغذ","مداد","درخت","چشمه","دریا","زمین","شادی","زیبا","بزرگ","کوچک","شکر","نمک","فلفل","روغن","پنیر","ماست","گوشت","برنج","گندم","لیمو","هویج","گوجه","سبزی","کباب","جاده","جنگل","مسجد","لباس","کلاه","چتر","ساعت","باران","پنجره","ستاره","آسمان","آزادی","دوستی","زندگی","مدرسه","نانوا","انگور","بیمار","پیروز","لبخند","کوتاه","شیرین","سالاد","روستا","میدان","آبشار","جزیره","زنبور","مورچه","خرگوش","روباه","میمون","دریاچه","موفقیت","دانشجو","سلامتی","کتابچه","خورشید","درختان","باغبان","دوچرخه","نارنجی","پروانه","کشاورز","راهنما","خلاقیت","شیرینی","گردشگر","زمستان","مرغابی","خیابان","بیابان","گوسفند","پیراهن","دستکش","موبایل","راننده","کهکشان","مهمانی","موسیقی","بادکنک","گلستان","بوستان","کوهستان","مهربانی","پرندگان","دانشمند","توانایی","یادگیری","پایداری","تابستان","بلدرچین","سفرنامه","سبزیجات","ماهیگیر","رودخانه","هواپیما","پاسپورت","فرودگاه","بادمجان","مارمولک"]

# افزوده‌های واژه‌نامهٔ زنجیره (پوشش حروف آغازین)
CHAIN_EXTRA=["هوا","رعد","زود","بوق","دیو","کبک","کوچه","تلفن","قطار","کشتی","قایق","ساحل","ماهی","نهنگ","بازی","طناب","دختر","خربزه","چمدان","مسافر","یخچال","رادیو","ماشین","تقویم","شلوار","شش","یار","وقت","دل","بز","سر","پا","لب","گوش","چشم","دفتر","چراغ","بازار","برادر","مادر","خواهر","دایی","عمو","پزشک","معلم","هنر","خواب","دندان","زبان","بدن","خون","ابرو","انگشت","بالا","عسل"]

assert len(WS_WORDS) == len(set(WS_WORDS)) and len(WS_WORDS) >= 45
assert all(5 <= len(w) <= 7 for w in WS_WORDS)
assert len(ANA_WORDS) == len(set(ANA_WORDS)) and 140 <= len(ANA_WORDS) <= 170
assert all(2 <= len(_norm(w)) <= 7 and _norm(w) == w for w in ANA_WORDS)
CHAIN_WORDS = ANA_WORDS + [w for w in CHAIN_EXTRA if w not in ANA_WORDS]
assert len(CHAIN_WORDS) == len(set(CHAIN_WORDS)) and 190 <= len(CHAIN_WORDS) <= 220
assert len([w for w in ANA_WORDS if 6 <= len(w) <= 7]) >= 25

def js(x):
    return json.dumps(x, ensure_ascii=False)

BASE_CSS=r"""*{box-sizing:border-box}
body{font-family:Tahoma,'Segoe UI',sans-serif;margin:0;background:#0b1428;color:#eef2f7}
header{padding:10px 14px 0}
h1{font-size:18px;margin:0 0 6px;color:#d9a441}
#hud{font-size:13px;color:#9fb3d1;min-height:18px}
#app{padding:10px;max-width:540px;margin:0 auto}
#hint{padding:8px 14px;color:#7f93b3;font-size:12px;margin:0}
.panel{background:#14203a;border:1px solid #1f3160;border-radius:10px;padding:10px;margin:8px 0}
button{font-family:inherit;font-size:15px;min-height:42px;min-width:44px;border-radius:8px;border:1px solid #2a4a7a;background:#1b2c4f;color:#eef2f7;padding:8px 14px;cursor:pointer;touch-action:manipulation}
button.gold{background:#d9a441;color:#14203a;border-color:#d9a441;font-weight:700}
button.danger{background:#e26d5c;color:#14203a;border-color:#e26d5c;font-weight:700}
button:disabled{opacity:.45}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;justify-content:center}
.chip{background:#14203a;border:1px solid #1f3160;border-radius:14px;padding:4px 10px;font-size:13px;color:#9fb3d1}
.chip.on{background:#67b98a;color:#0b1428;border-color:#67b98a;text-decoration:line-through}
.small{font-size:12px;color:#7f93b3;text-align:center;margin:4px 0}"""

WS_CSS=BASE_CSS+r"""
.wgrid{display:grid;grid-template-columns:repeat(10,1fr);gap:3px}
.wcell{aspect-ratio:1;display:flex;align-items:center;justify-content:center;background:#14203a;border:1px solid #1f3160;border-radius:5px;font-size:15px;cursor:pointer;user-select:none;-webkit-user-select:none}
.wcell.sel{background:#d9a441;color:#14203a;font-weight:700}
.wcell.fnd{background:#3fb8af;color:#0b1428;font-weight:700}"""

WS_LOGIC=r"""var WOG_LOGIC=(function(){
var N=10;
var PLACE_DIRS=[[0,-1],[1,0],[1,-1],[1,1]];
var FILL="الیمنورتهدسکبشچپگفقحز";
var WORDS=@@WORDS@@;
function emptyGrid(){var g=[],r,c;for(r=0;r<N;r++){g.push([]);for(c=0;c<N;c++)g[r].push("");}return g;}
function placeWord(grid,word,r,c,dir){var cells=[],i,rr,cc;
for(i=0;i<word.length;i++){rr=r+dir[0]*i;cc=c+dir[1]*i;
if(rr<0||rr>=N||cc<0||cc>=N)return null;
if(grid[rr][cc]!==""&&grid[rr][cc]!==word[i])return null;
cells.push([rr,cc]);}
for(i=0;i<word.length;i++)grid[cells[i][0]][cells[i][1]]=word[i];
return cells;}
function tryPlace(grid,word,rng){var t,d,r,c,cs,dir;
for(t=0;t<250;t++){dir=PLACE_DIRS[Math.floor(rng()*PLACE_DIRS.length)];
r=Math.floor(rng()*N);c=Math.floor(rng()*N);
cs=placeWord(grid,word,r,c,dir);if(cs)return cs;}
for(d=0;d<PLACE_DIRS.length;d++)for(r=0;r<N;r++)for(c=0;c<N;c++){cs=placeWord(grid,word,r,c,PLACE_DIRS[d]);if(cs)return cs;}
return null;}
function fillGrid(grid,rng){for(var r=0;r<N;r++)for(var c=0;c<N;c++)if(grid[r][c]==="")grid[r][c]=FILL[Math.floor(rng()*FILL.length)];}
function gen(words,rng){var grid=emptyGrid(),placed=[];
for(var i=0;i<words.length;i++){var cells=tryPlace(grid,words[i],rng);
if(!cells)throw new Error("cannot place: "+words[i]);
placed.push({word:words[i],cells:cells});}
fillGrid(grid,rng);
return {grid:grid,placed:placed};}
function checkSelection(placed,r1,c1,r2,c2){
var dr=r2-r1,dc=c2-c1;
if(dr===0&&dc===0)return null;
if(Math.abs(dr)!==Math.abs(dc)&&dr!==0&&dc!==0)return null;
var sr=dr===0?0:(dr>0?1:-1),sc=dc===0?0:(dc>0?1:-1);
var ok=false;
for(var i=0;i<PLACE_DIRS.length;i++)if(PLACE_DIRS[i][0]===sr&&PLACE_DIRS[i][1]===sc){ok=true;break;}
if(!ok)return null;
var len=Math.max(Math.abs(dr),Math.abs(dc)),cells=[];
for(var j=0;j<=len;j++){var rr=r1+sr*j,cc=c1+sc*j;
if(rr<0||rr>=N||cc<0||cc>=N)return null;
cells.push([rr,cc]);}
for(var k=0;k<placed.length;k++){var pc=placed[k].cells;
if(pc.length!==cells.length)continue;
var same=true;
for(var m=0;m<cells.length;m++)if(pc[m][0]!==cells[m][0]||pc[m][1]!==cells[m][1]){same=false;break;}
if(same)return placed[k].word;}
return null;}
return {N:N,PLACE_DIRS:PLACE_DIRS,WORDS:WORDS,FILL:FILL,placeWord:placeWord,fillGrid:fillGrid,gen:gen,checkSelection:checkSelection};
})();""".replace("@@WORDS@@",js(WS_WORDS))

WS_UI=r"""var app=$('#app');
var st=null,sel=null,fc={},t0=0,timer=null;
function shuffleCopy(a){var b=a.slice(),i,j,t;for(i=b.length-1;i>0;i--){j=Math.floor(Math.random()*(i+1));t=b[i];b[i]=b[j];b[j]=t;}return b;}
function key(r,c){return r+'_'+c;}
function isFound(w){for(var k in fc)if(fc[k]===w)return true;return false;}
function newGame(){
var pool=shuffleCopy(L.WORDS).slice(0,8);
st=L.gen(pool,Math.random);
sel=null;fc={};t0=Date.now();
if(timer)clearInterval(timer);
timer=setInterval(paintHud,1000);
render();paintHud();
}
function paintHud(){
var f=0,k;for(k in fc)f++;
var el=Math.floor((Date.now()-t0)/1000);
hud('یافته: '+fa(f)+' از '+fa(st?st.placed.length:8)+' · زمان: '+fa(el)+' ثانیه');
}
function render(){
app.innerHTML='';
var g=st.grid;
var grid=ce('div','wgrid');
for(var r=0;r<10;r++)for(var c=0;c<10;c++)(function(r,c){
var d=ce('div','wcell');
d.textContent=g[r][c];
if(sel&&sel[0]===r&&sel[1]===c)d.className+=' sel';
if(fc[key(r,c)])d.className+=' fnd';
d.onclick=function(){tap(r,c);};
grid.appendChild(d);
})(r,c);
app.appendChild(grid);
var chips=ce('div','row');
for(var i=0;i<st.placed.length;i++){
var ch=ce('div','chip'+(isFound(st.placed[i].word)?' on':''));
ch.textContent=st.placed[i].word;
chips.appendChild(ch);
}
app.appendChild(chips);
var row=ce('div','row');
var nb=ce('button','gold');
nb.textContent='بازی جدید';
nb.setAttribute('data-smoke','1');
nb.onclick=newGame;
row.appendChild(nb);
app.appendChild(row);
}
function tap(r,c){
if(!st)return;
if(!sel){sel=[r,c];render();return;}
if(sel[0]===r&&sel[1]===c){sel=null;render();return;}
var w=L.checkSelection(st.placed,sel[0],sel[1],r,c);
if(w&&!isFound(w)){
var p=null,i;
for(i=0;i<st.placed.length;i++)if(st.placed[i].word===w)p=st.placed[i];
for(i=0;i<p.cells.length;i++)fc[key(p.cells[i][0],p.cells[i][1])]=w;
toast('پیدا شد: '+w);
sel=null;
var f=0,k;for(k in fc)f++;
if(f===st.placed.length){win();return;}
render();paintHud();
}else{
if(w)toast('این واژه قبلاً پیدا شده بود');
else toast('این خط واژه‌ای ندارد');
sel=[r,c];render();
}
}
function win(){
if(timer){clearInterval(timer);timer=null;}
var el=Math.floor((Date.now()-t0)/1000);
var best=parseInt(store.get('wog-word-search-best')||'0',10);
var rec;
if(!best||el<best){store.set('wog-word-search-best',String(el));rec=' — رکورد جدید!';}
else rec=' — رکورد: '+fa(best)+' ثانیه';
render();
ovl('همهٔ واژه‌ها پیدا شد!','زمان: '+fa(el)+' ثانیه'+rec,'بازی جدید',newGame);
}
newGame();"""

WS_TESTS=[
("جهت‌های مجاز قراردهی",r"""T.eq(L.PLACE_DIRS,[[0,-1],[1,0],[1,-1],[1,1]]);T.eq(L.N,10);"""),
("قواعد قراردهی: مرز و تداخل",r"""
var g=[],i,j;
for(i=0;i<10;i++){g.push([]);for(j=0;j<10;j++)g[i].push("");}
var c1=L.placeWord(g,"باران",2,9,[0,-1]);
T.ok(c1);T.eq(c1,[[2,9],[2,8],[2,7],[2,6],[2,5]]);
T.eq(g[2][9],"ب");T.eq(g[2][5],"ن");
T.eq(L.placeWord(g,"کوهستان",9,2,[1,0]),null);
T.eq(L.placeWord(g,"کوهستان",2,9,[0,1]),null);
T.eq(L.placeWord(g,"دوستی",2,9,[0,-1]),null);
var c2=L.placeWord(g,"آبادی",0,8,[1,0]);
T.ok(c2);T.eq(g[2][8],"ا");
T.eq(L.placeWord(g,"موزیک",2,8,[0,-1]),null);
"""),
("۵۰ تولید مهرشده: هر ۸ واژه قرار می‌گیرد",r"""
function mb(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
for(var s=0;s<50;s++){
var r=mb(s*13+7);
var ws=L.WORDS.slice((s*3)%37,(s*3)%37+8);
var o=L.gen(ws,r);
T.eq(o.placed.length,8);
T.eq(o.grid.length,10);
for(var i=0;i<10;i++)T.eq(o.grid[i].length,10);
for(var p=0;p<o.placed.length;p++){
var pl=o.placed[p],w=pl.word;
T.ok(ws.indexOf(w)>=0);
T.eq(pl.cells.length,w.length);
var d0=[pl.cells[1][0]-pl.cells[0][0],pl.cells[1][1]-pl.cells[0][1]];
var okd=false;
for(var d=0;d<L.PLACE_DIRS.length;d++)if(L.PLACE_DIRS[d][0]===d0[0]&&L.PLACE_DIRS[d][1]===d0[1])okd=true;
T.ok(okd);
for(var k=0;k<pl.cells.length;k++){
var rc=pl.cells[k];
T.ok(rc[0]>=0&&rc[0]<10&&rc[1]>=0&&rc[1]<10);
T.eq(o.grid[rc[0]][rc[1]],w[k]);}
}
var empty=0;
for(var rr=0;rr<10;rr++)for(var cc=0;cc<10;cc++)if(o.grid[rr][cc]==="")empty++;
T.eq(empty,0);
}
"""),
("پخش سلول‌های واژه به‌عنوان انتخاب",r"""
function mb(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
var o=L.gen(L.WORDS.slice(0,8),mb(777));
for(var p=0;p<o.placed.length;p++){
var pl=o.placed[p],cs=pl.cells;
var got=L.checkSelection(o.placed,cs[0][0],cs[0][1],cs[cs.length-1][0],cs[cs.length-1][1]);
T.eq(got,pl.word);
var rev=L.checkSelection(o.placed,cs[cs.length-1][0],cs[cs.length-1][1],cs[0][0],cs[0][1]);
T.eq(rev,null);
}
"""),
("رد انتخاب نامعتبر و جهت غلط",r"""
function mb(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
var o=L.gen(L.WORDS.slice(0,8),mb(42));
var cs=o.placed[0].cells;
T.eq(L.checkSelection(o.placed,cs[0][0],cs[0][1],cs[0][0],cs[0][1]),null);
T.eq(L.checkSelection(o.placed,3,3,5,4),null);
T.eq(L.checkSelection(o.placed,0,0,0,3),null);
T.eq(L.checkSelection(o.placed,5,5,2,5),null);
T.eq(L.checkSelection(o.placed,4,4,2,2),null);
T.eq(L.checkSelection(o.placed,10,0,10,4),null);
T.eq(L.checkSelection(o.placed,cs[1][0],cs[1][1],cs[cs.length-1][0],cs[cs.length-1][1]),null);
"""),
]

ANA_CSS=BASE_CSS+r"""
.tiles{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.tile{width:46px;height:52px;font-size:20px;font-weight:700;background:#1b2c4f;border:2px solid #2a4a7a;border-radius:8px}
.tile.used{opacity:.25}
.ansrow{min-height:56px;display:flex;gap:6px;flex-wrap:wrap;justify-content:center;align-items:center;background:#101a2e;border:1px dashed #2a4a7a;border-radius:8px;padding:6px}
.achip{min-width:40px;height:44px;font-size:18px;font-weight:700;background:#3fb8af;border:none;color:#0b1428;border-radius:6px}
.wlist{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.wf{background:#67b98a;color:#0b1428;border-radius:12px;padding:3px 10px;font-size:13px;text-decoration:line-through}
.wm{color:#7f93b3;border:1px solid #1f3160;border-radius:12px;padding:3px 10px;font-size:13px}"""

ANA_LOGIC=r"""var WOG_LOGIC=(function(){
var DICT=@@DICT@@;
var FILL="الیمنورتهدسکبشچپگفقحز";
function norm(w){return String(w).replace(/ي/g,"ی").replace(/ك/g,"ک").replace(/[\s\u200c]+/g,"");}
function lettersOf(w){return norm(w).split("");}
function canForm(word,letters){
var need={},wl=lettersOf(word),i;
for(i=0;i<wl.length;i++)need[wl[i]]=(need[wl[i]]||0)+1;
for(i=0;i<letters.length;i++){var ch=norm(letters[i]);if(need[ch])need[ch]--;}
for(var k in need)if(need[k]>0)return false;
return true;}
function findable(letters){
var out=[];
for(var i=0;i<DICT.length;i++){var w=DICT[i];if(w.length>=2&&canForm(w,letters))out.push(w);}
return out;}
function scoreOf(n){return n*n;}
var SOURCES=[];
for(var i=0;i<DICT.length;i++)if(DICT[i].length>=6&&DICT[i].length<=7)SOURCES.push(DICT[i]);
function sourceWord(rng){return SOURCES[Math.floor(rng()*SOURCES.length)];}
function genLetters(word,rng){
var ls=lettersOf(word),target=6+(rng()<0.5?0:1),i;
if(target<ls.length)target=ls.length;
while(ls.length<target)ls.push(FILL[Math.floor(rng()*FILL.length)]);
for(i=ls.length-1;i>0;i--){var j=Math.floor(rng()*(i+1)),t=ls[i];ls[i]=ls[j];ls[j]=t;}
return ls;}
return {DICT:DICT,SOURCES:SOURCES,FILL:FILL,norm:norm,lettersOf:lettersOf,canForm:canForm,findable:findable,scoreOf:scoreOf,sourceWord:sourceWord,genLetters:genLetters};
})();""".replace("@@DICT@@",js(ANA_WORDS))

ANA_UI=r"""var app=$('#app');
var letters=[],ans=[],found={},score=0,tleft=120,timer=null,ended=false;
var DSET={};
(function(){var i;for(i=0;i<L.DICT.length;i++)DSET[L.DICT[i]]=1;})();
function newGame(){
var rng=Math.random;
var w=L.sourceWord(rng);
letters=L.genLetters(w,rng);
ans=[];found={};score=0;tleft=120;ended=false;
if(timer)clearInterval(timer);
timer=setInterval(function(){tleft--;paintHud();if(tleft<=0)end();},1000);
render();paintHud();
}
function paintHud(){
var f=0,k;for(k in found)if(found[k])f++;
hud('امتیاز: '+fa(score)+' · زمان: '+fa(Math.max(0,tleft))+' ثانیه · واژه‌ها: '+fa(f));
}
function tapTile(i){if(!ended&&ans.indexOf(i)<0){ans.push(i);render();}}
function tapAns(k){if(!ended){ans.splice(k,1);render();}}
function clearAns(){if(!ended){ans=[];render();}}
function shuffleTiles(){
if(ended)return;
var i,j,t;
for(i=letters.length-1;i>0;i--){j=Math.floor(Math.random()*(i+1));t=letters[i];letters[i]=letters[j];letters[j]=t;}
ans=[];render();
}
function submit(){
if(ended)return;
var w=ans.map(function(i){return letters[i];}).join('');
if(w.length<2){toast('حداقل ۲ حرف لازم است');return;}
if(found[w]){toast('این واژه را قبلاً گفتی');return;}
if(!DSET[w]){toast('در فهرست واژه‌ها نیست');return;}
var p=L.scoreOf(w.length);
found[w]=p;score+=p;
toast('آفرین! +'+fa(p));
ans=[];render();paintHud();
}
function end(){
ended=true;
if(timer){clearInterval(timer);timer=null;}
var all=L.findable(letters);
var best=parseInt(store.get('wog-anagram-best')||'0',10);
if(score>best){best=score;store.set('wog-anagram-best',String(best));}
render(all);
paintHud();
ovl('پایان بازی!','امتیاز: '+fa(score)+' — واژه‌های ممکن: '+all.join('، '),'بازی جدید',newGame);
}
function render(all){
app.innerHTML='';
var tr=ce('div','tiles'),i;
for(i=0;i<letters.length;i++)(function(i){
var b=ce('button','tile'+(ans.indexOf(i)>=0?' used':''));
b.textContent=letters[i];
b.onclick=function(){tapTile(i);};
tr.appendChild(b);
})(i);
app.appendChild(tr);
var ar=ce('div','ansrow');
if(!ans.length){var ph=ce('span');ph.textContent='واژه‌ات را بساز...';ph.style.color='#7f93b3';ar.appendChild(ph);}
for(i=0;i<ans.length;i++)(function(i){
var b=ce('button','achip');
b.textContent=letters[ans[i]];
b.onclick=function(){tapAns(i);};
ar.appendChild(b);
})(i);
app.appendChild(ar);
var row=ce('div','row');
var sub=ce('button','gold');sub.textContent='ثبت';sub.onclick=submit;row.appendChild(sub);
var cl=ce('button');cl.textContent='پاک';cl.onclick=clearAns;row.appendChild(cl);
var sh=ce('button');sh.textContent='بُر بزن';sh.onclick=shuffleTiles;row.appendChild(sh);
var ng=ce('button','danger');ng.textContent='بازی جدید';ng.setAttribute('data-smoke','1');ng.onclick=newGame;row.appendChild(ng);
app.appendChild(row);
var wl=ce('div','wlist');
if(ended){
for(i=0;i<all.length;i++){
var w2=ce('div',found[all[i]]?'wf':'wm');
w2.textContent=all[i];
wl.appendChild(w2);
}
}else{
for(var k in found){
var w3=ce('div','wf');
w3.textContent=k+' (+'+fa(found[k])+')';
wl.appendChild(w3);
}
}
app.appendChild(wl);
}
document.addEventListener('keydown',function(e){
if(e.key==='Enter')submit();
else if(e.key==='Backspace'&&!ended){ans.pop();render();}
});
newGame();"""

ANA_TESTS=[
("canForm با شمارش تکراری",r"""
T.ok(L.canForm("باب",["ب","ا","ب"]));
T.ok(!L.canForm("باب",["ب","ا"]));
T.ok(!L.canForm("باب",["ب","ا","ت"]));
T.ok(L.canForm("باب",["ب","ا","ب","ت"]));
T.ok(L.canForm("لال",["ا","ل","ل"]));
T.ok(!L.canForm("لال",["ا","ل","ت"]));
T.ok(L.canForm("كتاب",["ک","ت","ا","ب"]));
T.ok(L.canForm("کتاب",["ک","ت","ا","ب","ن","و"]));
T.ok(!L.canForm("کتاب",["ک","ت","ا"]));
"""),
("امتیاز مجذور طول",r"""
T.eq(L.scoreOf(2),4);T.eq(L.scoreOf(3),9);T.eq(L.scoreOf(5),25);T.eq(L.scoreOf(7),49);
for(var n=2;n<8;n++)T.ok(L.scoreOf(n+1)>L.scoreOf(n));
"""),
("پیداگر واژه‌های قابل ساخت",r"""
var ls=["ب","ا","ر","ا","ن","ت"];
var f=L.findable(ls);
T.ok(f.indexOf("باران")>=0);
T.ok(f.indexOf("نان")<0);
for(var i=0;i<f.length;i++){T.ok(f[i].length>=2);T.ok(L.DICT.indexOf(f[i])>=0);T.ok(L.canForm(f[i],ls));}
T.eq(L.findable([]).length,0);
"""),
("۳۰ مجموعهٔ مهرشده شامل واژهٔ مبدأ",r"""
function mb(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
var FA="آاأإئءابتثجحخدذرزسشصضطظعغفقکلمنهویپچژگ";
for(var s=1;s<=30;s++){
var r=mb(s*13+5);
var w=L.sourceWord(r);
T.ok(w.length>=6&&w.length<=7);
var ls=L.genLetters(w,r);
T.ok(ls.length>=6&&ls.length<=7);
T.ok(L.canForm(w,ls));
T.ok(L.findable(ls).indexOf(w)>=0);
for(var i=0;i<ls.length;i++)T.ok(FA.indexOf(ls[i])>=0);
}
"""),
("درستی واژه‌نامه",r"""
var seen={};
for(var i=0;i<L.DICT.length;i++){
var w=L.DICT[i];
T.ok(w.length>=2&&w.length<=7);
T.ok(L.norm(w)===w);
T.ok(!seen[w]);seen[w]=1;
}
T.ok(L.DICT.length>=140);
T.ok(L.SOURCES.length>=25);
"""),
]

CH_CSS=BASE_CSS+r"""
.scores{display:flex;gap:10px;justify-content:center}
.scor{flex:1;max-width:160px;text-align:center;padding:8px;border-radius:8px;background:#14203a;border:1px solid #1f3160}
.scor.act{border-color:#d9a441}
.scor b{display:block;font-size:22px;color:#d9a441}
.prevw{font-size:26px;text-align:center;letter-spacing:1px;margin:10px 0 2px;color:#eef2f7}
.prevw span{color:#e26d5c;font-weight:700}
.tbar{height:10px;background:#101a2e;border-radius:5px;overflow:hidden;margin:6px 0}
.tbar div{height:100%;background:#3fb8af}
.typed{min-height:36px;text-align:center;font-size:20px;color:#eef2f7;border-bottom:1px solid #2a4a7a;padding:4px}"""

CH_LOGIC=r"""var WOG_LOGIC=(function(){
var DICT=@@DICT@@;
function norm(w){return String(w).replace(/ي/g,"ی").replace(/ك/g,"ک").replace(/[\s\u200c]+/g,"");}
function lastLetter(w){var s=norm(w);return s.charAt(s.length-1);}
function firstLetter(w){return norm(w).charAt(0);}
function canChain(prev,next){return lastLetter(prev)===firstLetter(next);}
function aiReply(prev,used,rng){
var last=lastLetter(prev),cands=[],i;
rng=rng||Math.random;
for(i=0;i<DICT.length;i++){var w=DICT[i];
if(firstLetter(w)===last&&used.indexOf(w)<0)cands.push(w);}
if(!cands.length)return null;
return cands[Math.floor(rng()*cands.length)];}
return {DICT:DICT,norm:norm,lastLetter:lastLetter,firstLetter:firstLetter,canChain:canChain,aiReply:aiReply};
})();""".replace("@@DICT@@",js(CHAIN_WORDS))

CH_UI=r"""var app=$('#app');
var me=0,ai=0,used=[],prev='',turn='me',tleft=15,timer=null,typed='',over=true,round=0;
var DSET={};
(function(){var i;for(i=0;i<L.DICT.length;i++)DSET[L.DICT[i]]=1;})();
function newGame(){me=0;ai=0;round=0;over=false;startRound();}
function startRound(){
used=[];typed='';round++;
var w=L.DICT[Math.floor(Math.random()*L.DICT.length)];
while(w.length<3)w=L.DICT[Math.floor(Math.random()*L.DICT.length)];
prev=w;turn='me';tleft=15;
if(timer)clearInterval(timer);
timer=setInterval(function(){
if(over||turn!=='me')return;
tleft--;paintTimer();
if(tleft<=0)fail('زمان تمام شد');
},1000);
render();paintHud();paintTimer();
}
function paintHud(){hud('من '+fa(me)+' — ربات '+fa(ai)+' · دور '+fa(round));}
function paintTimer(){
var bar=$('#tbarin');
if(bar){bar.style.width=Math.max(0,tleft/15*100)+'%';bar.style.background=tleft<=5?'#e26d5c':'#3fb8af';}
var tv=$('#tval');
if(tv)tv.textContent=fa(Math.max(0,tleft))+' ثانیه';
}
function fail(msg){
if(over||turn!=='me')return;
ai++;
toast(msg+' — امتیاز برای ربات');
paintHud();
if(ai>=5){end(false);return;}
setTimeout(startRound,900);
}
function okHuman(w){
used.push(w);prev=w;turn='ai';typed='';
render();paintHud();
setTimeout(function(){
if(over)return;
var rep=L.aiReply(prev,used,Math.random);
if(!rep){
me++;
toast('ربات جواب نداد! امتیاز برای تو');
paintHud();
if(me>=5){end(true);return;}
setTimeout(startRound,900);
return;
}
used.push(rep);prev=rep;turn='me';tleft=15;
render();paintHud();paintTimer();
},700);
}
function submit(){
if(over||turn!=='me')return;
var w=normFa(typed);
if(w.length<2){toast('واژهٔ بلندتری بنویس');return;}
if(!DSET[w]){toast('واژه در فهرست نیست');return;}
if(!L.canChain(prev,w)){toast('باید با «'+L.lastLetter(prev)+'» شروع شود');return;}
if(used.indexOf(w)>=0){toast('در این دور قبلاً گفته شده');return;}
okHuman(w);
}
function end(win){
over=true;
if(timer){clearInterval(timer);timer=null;}
if(win){
var w1=parseInt(store.get('wog-word-chain-wins')||'0',10)+1;
store.set('wog-word-chain-wins',String(w1));
}
ovl(win?'بردی!':'باختی!',fa(me)+' – '+fa(ai),'بازی جدید',newGame);
}
function render(){
app.innerHTML='';
var sc=ce('div','scores');
var s1=ce('div','scor'+(turn==='me'&&!over?' act':''));
var b1=ce('b');b1.textContent=fa(me);s1.appendChild(b1);
var l1=ce('div');l1.textContent='من';s1.appendChild(l1);
sc.appendChild(s1);
var s2=ce('div','scor'+(turn==='ai'&&!over?' act':''));
var b2=ce('b');b2.textContent=fa(ai);s2.appendChild(b2);
var l2=ce('div');l2.textContent='ربات';s2.appendChild(l2);
sc.appendChild(s2);
app.appendChild(sc);
var pw=ce('div','prevw');
pw.textContent=prev.slice(0,-1);
var sp=ce('span');sp.textContent=prev.charAt(prev.length-1);pw.appendChild(sp);
app.appendChild(pw);
var pv=ce('div','small');
pv.textContent='واژهٔ بعدی باید با «'+prev.charAt(prev.length-1)+'» شروع شود';
app.appendChild(pv);
var ty=ce('div','typed');ty.textContent=typed||'...';app.appendChild(ty);
var tb=ce('div','tbar');var ti=ce('div');ti.id='tbarin';tb.appendChild(ti);app.appendChild(tb);
var tv=ce('div','small');tv.id='tval';tv.textContent=fa(Math.max(0,tleft))+' ثانیه';app.appendChild(tv);
var uv=ce('div','small');uv.textContent='واژه‌های گفته‌شدهٔ این دور: '+fa(used.length);app.appendChild(uv);
var row=ce('div','row');
var sub=ce('button','gold');sub.textContent='ثبت';sub.onclick=submit;row.appendChild(sub);
var del=ce('button');del.textContent='پاک';del.onclick=function(){if(turn==='me'&&!over){typed=typed.slice(0,-1);render();}};row.appendChild(del);
var ps=ce('button','danger');ps.textContent='پاس';ps.onclick=function(){fail('پاس زدی');};row.appendChild(ps);
var ng=ce('button','danger');ng.textContent='بازی جدید';ng.setAttribute('data-smoke','1');ng.onclick=newGame;row.appendChild(ng);
app.appendChild(row);
var kbwrap=ce('div','row');
var kb=faKb(function(ch){
if(over||turn!=='me')return;
if(ch==='\u232B'||ch==='Backspace'){typed=typed.slice(0,-1);render();return;}
if(ch==='\u21B5'||ch==='Enter'){submit();return;}
if(ch&&ch.length===1){typed+=ch;render();}
});
if(kb&&kb.nodeType)kbwrap.appendChild(kb);
app.appendChild(kbwrap);
}
document.addEventListener('keydown',function(e){
if(e.key==='Enter')submit();
else if(e.key==='Backspace'){if(turn==='me'&&!over){typed=typed.slice(0,-1);render();}}
else if(e.key&&e.key.length===1&&turn==='me'&&!over){typed+=e.key;render();}
});
newGame();"""

CH_TESTS=[
("نرمال‌سازی حرف آخر",r"""
T.eq(L.lastLetter("كتاب"),"ب");
T.eq(L.lastLetter("باري"),"ی");
T.eq(L.lastLetter(" دانش "),"ش");
T.eq(L.lastLetter("آب\u200cریز"),"ز");
T.eq(L.lastLetter("آب\u200c"),"ب");
T.eq(L.lastLetter("کتاب"),"ب");
"""),
("زنجیرهٔ دقیق",r"""
T.ok(L.canChain("کتاب","بار"));
T.ok(L.canChain("كتاب","بار"));
T.ok(!L.canChain("کتاب","آب"));
T.ok(L.canChain("بار","رود"));
T.ok(!L.canChain("بار","دشت"));
T.eq(L.firstLetter("ياس"),"ی");
"""),
("پاسخ ربات: زنجیر و پرهیز از تکرار",r"""
function mb(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
for(var s=0;s<20;s++){
var r=mb(s+31);
var used=[],prev="کتاب",k=0,tries=0;
while(k<5&&tries<80){
var rep=L.aiReply(prev,used,r);
if(!rep){used=[];prev="کتاب";k=0;tries++;continue;}
T.ok(L.canChain(prev,rep));
T.ok(L.DICT.indexOf(rep)>=0);
T.ok(used.indexOf(rep)<0);
used.push(rep);prev=rep;k++;
}
T.ok(k===5);
}
var bs=[];
for(var i=0;i<L.DICT.length;i++)if(L.firstLetter(L.DICT[i])==="ب")bs.push(L.DICT[i]);
T.ok(bs.length>0);
T.eq(L.aiReply("کتاب",bs,mb(1)),null);
"""),
("بازی کامل مهرشده تا ۵ امتیاز",r"""
function mb(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
for(var s=0;s<10;s++){
var r=mb(s*7+3);
var used=[],sc=[0,0],rounds=0;
while(sc[0]<5&&sc[1]<5&&rounds<60){
rounds++;used=[];
var prev=L.DICT[Math.floor(r()*L.DICT.length)];
var cur=0,guard=0,done=false;
while(!done){
guard++;
T.ok(guard<300);
var mv=L.aiReply(prev,used,r);
if(!mv){sc[cur^1]++;done=true;}else{used.push(mv);prev=mv;cur=cur^1;}
}
}
T.ok(sc[0]===5||sc[1]===5);
T.ok(sc[0]<5||sc[1]<5);
T.eq(rounds,sc[0]+sc[1]);
T.ok(rounds<=9);
}
"""),
("واژه‌نامهٔ زنجیره",r"""
T.ok(L.DICT.length>=180);
var seen={},starts={};
for(var i=0;i<L.DICT.length;i++){
var w=L.DICT[i];
T.ok(w.length>=2);
T.ok(L.norm(w)===w);
T.ok(!seen[w]);seen[w]=1;
starts[L.firstLetter(w)]=1;
}
var need="ابپتجچدرخسشعفکگلمنهوی";
for(var k=0;k<need.length;k++)T.ok(starts[need[k]],"starter "+need[k]);
"""),
]

GAMES=[
G("word-search","واژه‌یاب شبکه‌ای","word","🔍","#d9a441","#3fb8af",
  "هشت واژهٔ پنج تا هفت‌حرفی در شبکهٔ ۱۰×۱۰ پنهان شده‌اند. خانهٔ آغاز و پایان هر واژه را لمس کن تا خط آن روشن شود.",
  "واژه‌ها راست‌به‌چپ، از بالا به پایین و مورب قرار دارند؛ اول آغاز، بعد پایان را لمس کن.",
  logic=WS_LOGIC, ui=WS_UI, css=WS_CSS, engines=("common","word"), tests=WS_TESTS),
G("anagram","واژه‌سازی","word","🔤","#3fb8af","#67b98a",
  "با حروف داده‌شده واژه‌سازی کن؛ هر واژهٔ درست به اندازهٔ مجذور طولش امتیاز دارد. ۱۲۰ ثانیه وقت داری و در پایان همهٔ واژه‌های ممکن فاش می‌شود.",
  "روی حروف بزن تا واژه ساخته شود، بعد ثبت بزن؛ دکمهٔ بُر بزن ترتیب حروف را عوض می‌کند.",
  logic=ANA_LOGIC, ui=ANA_UI, css=ANA_CSS, engines=("common","word"), tests=ANA_TESTS),
G("word-chain","زنجیرهٔ واژه‌ها","word","🔗","#d9a441","#e26d5c",
  "با ربات زنجیرهٔ واژه بساز: هر واژه باید با حرف آخر واژهٔ قبلی شروع شود و در هر دور تکراری نباشد. ۱۵ ثانیه وقت داری؛ اولین ۵ امتیاز برنده است.",
  "از صفحه‌کلید فارسی تایپ کن و ثبت بزن؛ اگر ربات گیر کرد امتیاز برای توست.",
  logic=CH_LOGIC, ui=CH_UI, css=CH_CSS, engines=("common","word"), tests=CH_TESTS),
]
