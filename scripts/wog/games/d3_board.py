# -*- coding: utf-8 -*-
from lib_mini import G

QUARTO_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
var PIECES=[];
(function(){var a,b;for(a=0;a<2;a++)for(b=0;b<2;b++){PIECES.push({a:a,b:b});PIECES.push({a:a,b:b});}})();
var LINES=[],i2,j2;
for(i2=0;i2<4;i2++)LINES.push([4*i2,4*i2+1,4*i2+2,4*i2+3]);
for(j2=0;j2<4;j2++)LINES.push([j2,j2+4,j2+8,j2+12]);
LINES.push([0,5,10,15],[3,6,9,12]);
function eq(p,q){return !!p&&!!q&&p.a===q.a&&p.b===q.b;}
function cp(p){return p?{a:p.a,b:p.b}:null;}
function clone(st){var b=[],i;for(i=0;i<16;i++)b.push(cp(st.board[i]));var pl=[],j;for(j=0;j<st.pool.length;j++)pl.push(cp(st.pool[j]));return {board:b,toPlace:cp(st.toPlace),pool:pl,turn:st.turn,phase:st.phase,winner:st.winner,draw:st.draw,winLine:st.winLine?st.winLine.slice():null};}
function initial(rng){if(!rng)rng=Math.random;var i=Math.floor(rng()*8),tp=PIECES[i],pool=[],j,b=[],k;for(j=0;j<8;j++)if(j!==i)pool.push(cp(PIECES[j]));for(k=0;k<16;k++)b.push(null);return {board:b,toPlace:cp(tp),pool:pool,turn:0,phase:'place',winner:null,draw:false,winLine:null};}
function winAt(st){var b=st.board,i,k;for(i=0;i<LINES.length;i++){var ln=LINES[i],p0=b[ln[0]];if(!p0)continue;var sa=true,sb=true;for(k=1;k<4;k++){var p=b[ln[k]];if(!p){sa=false;sb=false;break;}if(p.a!==p0.a)sa=false;if(p.b!==p0.b)sb=false;}if(sa||sb)return {win:true,who:st.turn,line:ln.slice()};}return {win:false,who:null,line:null};}
function poolEmpty(st){return st.pool.length===0;}
function place(st,r,c){if(st.phase!=='place')throw new Error('phase');if(!st.toPlace)throw new Error('piece');if(!(r>=0&&r<4&&c>=0&&c<4))throw new Error('range');var idx=4*r+c;if(st.board[idx])throw new Error('occupied');var ns=clone(st);ns.board[idx]=cp(st.toPlace);ns.toPlace=null;var w=winAt({board:ns.board,turn:st.turn});if(w.win){ns.phase='over';ns.winner=st.turn;ns.winLine=w.line;return ns;}if(poolEmpty(ns)){ns.phase='over';ns.draw=true;return ns;}ns.phase='hand';return ns;}
function hand(st,piece){if(st.phase!=='hand')throw new Error('phase');var at=-1,i;for(i=0;i<st.pool.length;i++)if(eq(st.pool[i],piece)){at=i;break;}if(at<0)throw new Error('pool');var ns=clone(st);ns.toPlace=cp(ns.pool[at]);ns.pool.splice(at,1);ns.turn=1-st.turn;ns.phase='place';return ns;}
function winsWith(board,piece){var i;for(i=0;i<16;i++){if(board[i])continue;board[i]=piece;var w=winAt({board:board,turn:0});board[i]=null;if(w.win)return true;}return false;}
function aiMove(st,rng){if(!rng)rng=Math.random;var empt=[],i,k;for(i=0;i<16;i++)if(!st.board[i])empt.push(i);
var tp=cp(st.toPlace);
for(i=0;i<empt.length;i++){var b2=[];for(k=0;k<16;k++)b2.push(cp(st.board[k]));b2[empt[i]]=cp(tp);if(winAt({board:b2,turn:st.turn}).win){var pp=st.pool.length?st.pool[Math.floor(rng()*st.pool.length)]:null;return {r:Math.floor(empt[i]/4),c:empt[i]%4,piece:cp(pp)};}}
var safe=[];
for(i=0;i<empt.length;i++){var b3=[];for(k=0;k<16;k++)b3.push(cp(st.board[k]));b3[empt[i]]=cp(tp);var seen={},j;for(j=0;j<st.pool.length;j++){var pj=st.pool[j],key=pj.a+'-'+pj.b;if(seen[key])continue;seen[key]=1;if(!winsWith(b3,cp(pj)))safe.push({r:Math.floor(empt[i]/4),c:empt[i]%4,piece:cp(pj)});}}
if(safe.length){var s=safe[Math.floor(rng()*safe.length)];return s;}
var e=empt[Math.floor(rng()*empt.length)],p2=st.pool.length?st.pool[Math.floor(rng()*st.pool.length)]:null;
return {r:Math.floor(e/4),c:e%4,piece:cp(p2)};}
return {PIECES:PIECES,LINES:LINES,initial:initial,place:place,hand:hand,winAt:winAt,poolEmpty:poolEmpty,aiMove:aiMove,eq:eq};
})();
"""

QUARTO_UI = r"""
var st=null,busy=false,gen=0,WKEY='wog-quarto-mini-wins';
function wins(){var v=store.get(WKEY);return v===null||v===undefined?0:(+v||0);}
function pieceEl(p,extra){var cls='qp '+(p.a===1?'qp-lg':'qp-sm')+' '+(p.b===1?'qp-gold':'qp-slv');if(extra)cls+=' '+extra;return ce('div',cls);}
function hudUpd(){if(!st)return;var s;
 if(st.phase==='over')s=st.draw?'پایان: مساوی':(st.winner===0?'پایان: برد شما':'پایان: برد حریف');
 else if(busy||st.turn===1)s='نوبت حریف…';
 else if(st.phase==='place')s='نوبت شما: قطعه را بگذارید';
 else s='نوبت شما: قطعه‌ای به حریف بدهید';
 s+=' | قطعه‌های مانده: '+fa(st.pool.length+(st.toPlace?1:0))+' | بردها: '+fa(wins());
 hud(s);
 $('#hint').textContent='چهار قطعه با اندازهٔ یکسان یا رنگ یکسان در یک سطر، ستون یا قطر برنده است؛ در دادن قطعه، حریف را در آستانهٔ برد نیندازید.';}
function render(){var app=$('#app');app.innerHTML='';
 var ctrl=ce('div','qctrl');var nb=ce('button','btn','بازی جدید');nb.setAttribute('data-smoke','1');nb.addEventListener('click',function(){newGame();});ctrl.appendChild(nb);app.appendChild(ctrl);
 var bd=ce('div','qboard');
 for(var i=0;i<16;i++){(function(i){var r=Math.floor(i/4),c=i%4;var cell=ce('div','qcell');
  if(st.board[i]){cell.appendChild(pieceEl(st.board[i]));if(st.winLine&&st.winLine.indexOf(i)>=0)cell.className+=' qwin';}
  else if(st.phase==='place'&&st.turn===0&&!busy){cell.className+=' qfree';cell.addEventListener('click',function(){onCell(r,c);});}
  bd.appendChild(cell);})(i);}
 app.appendChild(bd);
 var side=ce('div','qside');
 if(st.phase==='over'){side.appendChild(ce('div','qmsg '+(st.draw?'':(st.winner===0?'qok':'qbad')),st.draw?'بازی مساوی شد':(st.winner===0?'چهار قطعهٔ هم‌ویژگی در یک راستا — بردی!':'حریف چارتایی را بست — باختی!')));}
 else if(st.turn===1||busy){side.appendChild(ce('div','qmsg','نوبت حریف…'));}
 else if(st.phase==='place'){side.appendChild(ce('div','qlabel','این قطعه را در خانه‌ای خالی بگذارید:'));var pv=ce('div','qpv');pv.appendChild(pieceEl(st.toPlace));side.appendChild(pv);}
 else{side.appendChild(ce('div','qlabel','یکی از این قطعه‌ها را به حریف بدهید:'));var pool=ce('div','qpool');
  for(var j=0;j<st.pool.length;j++){(function(p){var ch=pieceEl(p,'qchip');ch.addEventListener('click',function(){onHand(p);});pool.appendChild(ch);})(st.pool[j]);}
  side.appendChild(pool);}
 app.appendChild(side);hudUpd();}
function onCell(r,c){if(busy||!st||st.phase!=='place'||st.turn!==0||st.board[4*r+c])return;st=L.place(st,r,c);after();}
function onHand(p){if(busy||!st||st.phase!=='hand'||st.turn!==0)return;st=L.hand(st,p);after();}
function after(){render();if(st.phase==='over'){end();return;}if(st.turn===1)aiTurn();}
function aiTurn(){busy=true;var g=gen;hudUpd();setTimeout(function(){if(g!==gen||!st||st.phase==='over'){busy=false;return;}var m=L.aiMove(st);st=L.place(st,m.r,m.c);render();if(st.phase==='over'){busy=false;end();return;}setTimeout(function(){if(g!==gen||!st||st.phase==='over'){busy=false;return;}if(m.piece)st=L.hand(st,m.piece);busy=false;render();if(st.phase==='over')end();},620);},680);}
function end(){render();if(st.draw)ovl('مساوی','هیچ‌کس چارتایی نساخت.','بازی جدید',function(){newGame();});
 else if(st.winner===0){store.set(WKEY,String(wins()+1));ovl('بردی!','چهار قطعهٔ هم‌ویژگی در یک راستا نشست.','بازی جدید',function(){newGame();});}
 else ovl('باختی!','حریف چهار قطعهٔ هم‌ویژگی ساخت.','بازی جدید',function(){newGame();});}
function newGame(){gen++;busy=false;st=L.initial();render();}
newGame();
"""

QUARTO_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0b1424;color:#e8edf5;font-family:Vazirmatn,Tahoma,'Segoe UI',sans-serif;text-align:center}
header h1{color:#d9a441;font-size:22px;margin:8px 0 4px}
#hud{color:#9fb0c8;font-size:13px;min-height:18px;padding:0 8px}
#app{display:flex;flex-direction:column;align-items:center;gap:10px;padding:8px}
.btn{background:#d9a441;color:#101a2e;border:0;border-radius:10px;padding:10px 20px;font-size:15px;font-weight:700;cursor:pointer;min-height:42px;font-family:inherit;touch-action:manipulation}
.btn:hover{filter:brightness(1.08)}
.qctrl{display:flex;gap:10px}
.qboard{direction:ltr;display:grid;grid-template-columns:repeat(4,min(66px,20vw));grid-auto-rows:min(66px,20vw);gap:6px;background:#14203a;padding:10px;border-radius:14px;border:1px solid #24365c}
.qcell{background:#0e1930;border:1px solid #22345a;border-radius:10px;display:flex;align-items:center;justify-content:center}
.qfree{cursor:pointer}
.qfree:hover{border-color:#3fb8af}
.qwin{box-shadow:0 0 0 3px #67b98a inset}
.qp{border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,.5)}
.qp-lg{width:46px;height:46px}
.qp-sm{width:30px;height:30px}
.qp-gold{background:radial-gradient(circle at 35% 30%,#f6d98a,#c9971f 72%)}
.qp-slv{background:radial-gradient(circle at 35% 30%,#e9eff8,#8fa2ba 72%)}
.qside{min-height:92px;display:flex;flex-direction:column;align-items:center;gap:8px}
.qlabel{color:#9fb0c8;font-size:14px}
.qpv{display:flex;align-items:center;justify-content:center;width:64px;height:64px;background:#14203a;border:1px dashed #3fb8af;border-radius:12px}
.qpool{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;max-width:360px}
.qchip{cursor:pointer;padding:5px;border:2px solid #24365c;border-radius:12px;background:#0e1930}
.qchip:hover{border-color:#d9a441}
.qmsg{color:#d9a441;font-size:15px;padding:8px}
.qok{color:#67b98a}
.qbad{color:#e26d5c}
#hint{color:#8fa1b8;font-size:13px;max-width:440px;margin:8px auto;padding:0 10px;line-height:1.7}
"""

FOX_LOGIC = r"""
var WOG_LOGIC=(function(){
'use strict';
function isDark(r,c){return (r+c)%2===1;}
function initial(){return {fox:{r:7,c:4},hounds:[{r:0,c:1},{r:0,c:3},{r:0,c:5},{r:0,c:7}],turn:'fox'};}
function inB(r,c){return r>=0&&r<8&&c>=0&&c<8;}
function occAt(st,r,c){if(st.fox.r===r&&st.fox.c===c)return true;var i;for(i=0;i<4;i++)if(st.hounds[i].r===r&&st.hounds[i].c===c)return true;return false;}
function legalMoves(st,pl){var out=[],i,d;
 if(pl==='fox'){var DD=[[-1,-1],[-1,1],[1,-1],[1,1]];for(d=0;d<4;d++){var nr=st.fox.r+DD[d][0],nc=st.fox.c+DD[d][1];if(inB(nr,nc)&&isDark(nr,nc)&&!occAt(st,nr,nc))out.push({from:{r:st.fox.r,c:st.fox.c},to:{r:nr,c:nc}});}}
 else{var HD=[[1,-1],[1,1]];for(i=0;i<4;i++){var h=st.hounds[i];for(d=0;d<2;d++){var nr2=h.r+HD[d][0],nc2=h.c+HD[d][1];if(inB(nr2,nc2)&&isDark(nr2,nc2)&&!occAt(st,nr2,nc2))out.push({from:{r:h.r,c:h.c},to:{r:nr2,c:nc2}});}}}
 return out;}
function applyMove(st,pl,from,to){if(pl!==st.turn)throw new Error('turn');var ms=legalMoves(st,pl),i,found=null;
 for(i=0;i<ms.length;i++){var m=ms[i];if(m.from.r===from.r&&m.from.c===from.c&&m.to.r===to.r&&m.to.c===to.c){found=m;break;}}
 if(!found)throw new Error('illegal');
 var ns={fox:{r:st.fox.r,c:st.fox.c},hounds:[],turn:pl==='fox'?'hounds':'fox'},j;
 for(j=0;j<4;j++)ns.hounds.push({r:st.hounds[j].r,c:st.hounds[j].c});
 if(pl==='fox')ns.fox={r:to.r,c:to.c};
 else for(j=0;j<4;j++)if(ns.hounds[j].r===from.r&&ns.hounds[j].c===from.c){ns.hounds[j]={r:to.r,c:to.c};break;}
 return ns;}
function winner(st){if(st.fox.r===0)return 1;
 if(st.turn==='fox'&&legalMoves(st,'fox').length===0)return -1;
 if(st.turn==='hounds'&&legalMoves(st,'hounds').length===0)return 1;
 return 0;}
function aiMove(st,rng){if(!rng)rng=Math.random;var ms=legalMoves(st,'hounds');if(!ms.length)return null;
 var i,j,bs=Infinity,cands=[];
 for(i=0;i<ms.length;i++){var m=ms[i],hs=[],s=0;
  for(j=0;j<4;j++)hs.push({r:st.hounds[j].r,c:st.hounds[j].c});
  for(j=0;j<4;j++)if(hs[j].r===m.from.r&&hs[j].c===m.from.c){hs[j].r=m.to.r;hs[j].c=m.to.c;break;}
  for(j=0;j<4;j++)s+=Math.abs(hs[j].c-st.fox.c);
  if(s<bs){bs=s;cands=[m];}else if(s===bs)cands.push(m);}
 return cands[Math.floor(rng()*cands.length)];}
return {isDark:isDark,initial:initial,legalMoves:legalMoves,applyMove:applyMove,winner:winner,aiMove:aiMove};
})();
"""

FOX_UI = r"""
var st=null,busy=false,gen=0,WKEY='wog-fox-and-hounds-wins';
function wins(){var v=store.get(WKEY);return v===null||v===undefined?0:(+v||0);}
function hudUpd(){if(!st)return;var w=L.winner(st),s;
 if(w!==0)s=w===1?'پایان: روباه نجات یافت — برد شما':'پایان: روباه محاصره شد';
 else if(busy)s='سگ‌ها در حال تعقیب…';
 else s='نوبت شما: روباه را حرکت دهید';
 s+=' | بردها: '+fa(wins());
 hud(s);
 $('#hint').textContent='روباه مورب در هر چهار جهت و سگ‌ها فقط رو به جلو حرکت می‌کنند؛ روباه را به ردیف نخست برسانید — اگر حرکتی نمانید بازنده‌اید.';}
function statusMsg(){var w=L.winner(st);
 if(w!==0)return w===1?(st.fox.r===0?'روباه به ردیف نخست رسید — بردی!':'سگ‌ها بی‌حرکت شدند — بردی!'):'سگ‌ها همهٔ راه‌ها را بستند — باختی!';
 if(busy)return 'سگ‌ها در حال تعقیب…';
 return 'مقصدهای نشان‌شده را انتخاب کنید';}
function render(){var app=$('#app');app.innerHTML='';
 var ctrl=ce('div','fctrl');var nb=ce('button','btn','بازی جدید');nb.setAttribute('data-smoke','1');nb.addEventListener('click',function(){newGame();});ctrl.appendChild(nb);app.appendChild(ctrl);
 var bd=ce('div','fboard');var mv={};
 if(L.winner(st)===0&&st.turn==='fox'&&!busy){var ms=L.legalMoves(st,'fox');for(var i=0;i<ms.length;i++)mv[ms[i].to.r+'-'+ms[i].to.c]=1;}
 for(var r=0;r<8;r++)for(var c=0;c<8;c++){(function(r,c){var cell=ce('div','fcell '+((((r+c)%2)===1)?'fdk':'flt'));
  if(r===0&&((r+c)%2)===1)cell.className+=' fgoal';
  if(st.fox.r===r&&st.fox.c===c)cell.appendChild(ce('div','fp ffox'));
  else{for(var k=0;k<4;k++)if(st.hounds[k].r===r&&st.hounds[k].c===c){cell.appendChild(ce('div','fp fhound'));break;}}
  if(mv[r+'-'+c]){cell.className+=' fmv';cell.addEventListener('click',function(){onMove(r,c);});}
  bd.appendChild(cell);})(r,c);}
 app.appendChild(bd);app.appendChild(ce('div','fmsg',statusMsg()));hudUpd();}
function onMove(r,c){if(busy||!st||L.winner(st)!==0||st.turn!=='fox')return;
 var ms=L.legalMoves(st,'fox'),ok=false,i;for(i=0;i<ms.length;i++)if(ms[i].to.r===r&&ms[i].to.c===c){ok=true;break;}
 if(!ok)return;
 st=L.applyMove(st,'fox',{r:st.fox.r,c:st.fox.c},{r:r,c:c});after();}
function after(){render();var w=L.winner(st);if(w!==0){end(w);return;}
 busy=true;var g=gen;hudUpd();
 setTimeout(function(){if(g!==gen||!st)return;var h=L.aiMove(st);if(h)st=L.applyMove(st,'hounds',h.from,h.to);busy=false;render();var w2=L.winner(st);if(w2!==0)end(w2);},640);}
function end(w){render();
 if(w===1){store.set(WKEY,String(wins()+1));
  if(st.fox.r===0)ovl('بردی! روباه فرار کرد','به ردیف نخست رسیدی و از سگ‌ها گذشتی.','بازی جدید',function(){newGame();});
  else ovl('بردی! سگ‌ها میخکوب شدند','هیچ سگی نتوانست حرکت کند.','بازی جدید',function(){newGame();});}
 else ovl('روباه گرفتار شد','سگ‌ها همهٔ راه‌های مورب را بستند.','بازی جدید',function(){newGame();});}
function newGame(){gen++;busy=false;st=L.initial();render();}
newGame();
"""

FOX_CSS = r"""
*{box-sizing:border-box}
body{margin:0;background:#0b1424;color:#e8edf5;font-family:Vazirmatn,Tahoma,'Segoe UI',sans-serif;text-align:center}
header h1{color:#d9a441;font-size:22px;margin:8px 0 4px}
#hud{color:#9fb0c8;font-size:13px;min-height:18px;padding:0 8px}
#app{display:flex;flex-direction:column;align-items:center;gap:10px;padding:8px}
.btn{background:#d9a441;color:#101a2e;border:0;border-radius:10px;padding:10px 20px;font-size:15px;font-weight:700;cursor:pointer;min-height:42px;font-family:inherit;touch-action:manipulation}
.btn:hover{filter:brightness(1.08)}
.fctrl{display:flex;gap:10px}
.fboard{direction:ltr;display:grid;grid-template-columns:repeat(8,min(44px,11.5vw));grid-auto-rows:min(44px,11.5vw);border:2px solid #24365c;border-radius:12px;overflow:hidden;background:#14203a}
.fcell{display:flex;align-items:center;justify-content:center}
.flt{background:#0d1830}
.fdk{background:#1c2d52}
.fgoal{box-shadow:0 -3px 0 #d9a441 inset}
.fmv{cursor:pointer;box-shadow:0 0 0 3px #3fb8af inset}
.fmv:hover{box-shadow:0 0 0 3px #67b98a inset}
.fp{border-radius:50%}
.ffox{width:72%;height:72%;background:radial-gradient(circle at 35% 30%,#f2a25c,#c4571f 74%);box-shadow:0 2px 5px rgba(0,0,0,.55)}
.fhound{width:56%;height:56%;background:radial-gradient(circle at 35% 30%,#9fb3cf,#46597c 74%);box-shadow:0 2px 5px rgba(0,0,0,.55)}
.fmsg{color:#9fb0c8;font-size:14px;min-height:20px}
#hint{color:#8fa1b8;font-size:13px;max-width:440px;margin:8px auto;padding:0 10px;line-height:1.7}
"""

quarto = G(
    slug="quarto-mini",
    title="کواترو مینی",
    cat="board",
    icon="◈",
    g1="#d9a441",
    g2="#3fb8af",
    desc="کواتروی مینی روی صفحهٔ ۴×۴ با ۸ قطعه در دو اندازه (کوچک/بزرگ) و دو رنگ (نقره‌ای/طلایی). قطعه‌ای را که حریف دست می‌دهد بگذارید و بعد قطعهٔ بعدی را خودتان به او بدهید.",
    hint="چهار قطعه با اندازهٔ یکسان یا رنگ یکسان در یک سطر، ستون یا قطر برنده است؛ در دادن قطعه، حریف را در آستانهٔ برد نیندازید.",
    logic=QUARTO_LOGIC, ui=QUARTO_UI, css=QUARTO_CSS,
    engines=("common",), seed=12345,
    tests=[
        ("ساختار قطعه‌ها و وضعیت آغازین", r"""
var i,cnt={};
T.eq(L.PIECES.length,8,'8 pieces');
for(i=0;i<8;i++){var p=L.PIECES[i];T.ok(p.a===0||p.a===1,'a binary');T.ok(p.b===0||p.b===1,'b binary');var k=p.a+'-'+p.b;cnt[k]=(cnt[k]||0)+1;}
var keys=Object.keys(cnt);T.eq(keys.length,4,'4 distinct combos');
for(i=0;i<keys.length;i++)T.eq(cnt[keys[i]],2,'combo twice '+keys[i]);
var st=L.initial(rng);
T.eq(st.board.length,16,'16 cells');
var empt=0;for(i=0;i<16;i++)if(st.board[i]===null)empt++;
T.eq(empt,16,'board empty');
T.eq(st.pool.length,7,'pool of 7');
var all=st.pool.concat([st.toPlace]);T.eq(all.length,8,'pool+toPlace=8');
var cnt2={};for(i=0;i<8;i++){var q=all[i];cnt2[q.a+'-'+q.b]=(cnt2[q.a+'-'+q.b]||0)+1;}
for(i=0;i<keys.length;i++)T.eq(cnt2[keys[i]],cnt[keys[i]],'multiset '+keys[i]);
T.ok(st.turn===0,'human first');T.eq(st.phase,'place','phase place');
T.ok(!!st.toPlace&&st.toPlace.a!==undefined&&st.toPlace.b!==undefined,'toPlace set');
"""),
        ("برد سطر و ستون با هر دو ویژگی", r"""
function mk(o){var b=[],i;for(i=0;i<16;i++)b.push(null);for(var k in o)b[k]=o[k];return {board:b,turn:0,toPlace:null,pool:[],phase:'place',winner:null,draw:false,winLine:null};}
function P(a,b){return {a:a,b:b};}
var w=L.winAt(mk({0:P(1,0),1:P(1,1),2:P(1,0),3:P(1,1)}));
T.ok(w.win,'row a-win');T.eq(w.line,[0,1,2,3],'row line');T.eq(w.who,0,'who=turn');
var w2=L.winAt(mk({4:P(0,0),5:P(1,0),6:P(0,0),7:P(1,0)}));
T.ok(w2.win,'row b-win');T.eq(w2.line,[4,5,6,7],'row line 2');
var w3=L.winAt(mk({2:P(0,1),6:P(1,1),10:P(0,1),14:P(1,1)}));
T.ok(w3.win,'col b-win');T.eq(w3.line,[2,6,10,14],'col line');
var w4=L.winAt(mk({1:P(0,0),5:P(0,1),9:P(0,0),13:P(0,1)}));
T.ok(w4.win,'col a-win');T.eq(w4.line,[1,5,9,13],'col line 2');
T.ok(!L.winAt(mk({0:P(1,0),1:P(1,1),2:P(1,0),3:P(0,1)})).win,'3+1 not win');
T.ok(!L.winAt(mk({4:P(0,0),5:P(1,1),6:P(0,1),7:P(1,0)})).win,'no shared attr');
T.ok(!L.winAt(mk({0:P(1,0),1:P(1,1),2:P(1,0)})).win,'3 pieces not enough');
"""),
        ("برد قطرها و راستاهای از پیش ساخته", r"""
function mk(o){var b=[],i;for(i=0;i<16;i++)b.push(null);for(var k in o)b[k]=o[k];return {board:b,turn:1,toPlace:null,pool:[],phase:'place',winner:null,draw:false,winLine:null};}
function P(a,b){return {a:a,b:b};}
var w=L.winAt(mk({0:P(0,0),5:P(0,1),10:P(0,1),15:P(0,0)}));
T.ok(w.win,'main diag a-win');T.eq(w.line,[0,5,10,15],'diag line');T.eq(w.who,1,'who=turn 1');
var w2=L.winAt(mk({3:P(1,1),6:P(0,1),9:P(1,1),12:P(0,1)}));
T.ok(w2.win,'anti diag b-win');T.eq(w2.line,[3,6,9,12],'anti line');
T.ok(!L.winAt(mk({0:P(1,0),5:P(1,1),10:P(1,0)})).win,'incomplete diag');
T.ok(!L.winAt(mk({3:P(0,0),6:P(0,0),9:P(0,0),12:P(1,1)})).win,'3 same a on anti diag');
T.eq(L.LINES.length,10,'10 lines');
var seen={},i;for(i=0;i<10;i++){var ln=L.LINES[i];T.eq(ln.length,4,'len 4');seen[ln.join('-')]=1;}
T.eq(Object.keys(seen).length,10,'lines distinct');
"""),
        ("AI قطعهٔ برددهنده دست نمی‌دهد", r"""
function mk(o,toPlace,pool){var b=[],i;for(i=0;i<16;i++)b.push(null);for(var k in o)b[k]=o[k];return {board:b,toPlace:toPlace,pool:pool,turn:1,phase:'place',winner:null,draw:false,winLine:null};}
function P(a,b){return {a:a,b:b};}
// دو تهدید جدا: سطر ۰ با ویژگی a=1 (خانهٔ (0,3)) و ستون ۱ با ویژگی b=1 (خانهٔ (3,1))؛ یک مهره نمی‌تواند هر دو را ببندد
var s=mk({0:P(1,0),1:P(1,1),2:P(1,0),5:P(0,1),9:P(0,1)},P(0,0),[P(0,0),P(1,1)]);
var m=L.aiMove(s,rng);
T.ok(!!m&&m.r>=0&&m.r<4&&m.c>=0&&m.c<4,'valid move');
T.ok(s.board[4*m.r+m.c]===null,'empty target');
T.ok(!!m.piece&&m.piece.a===0&&m.piece.b===0,'hands the only safe piece (0,0)');
// اثبات تهدید: حریف با قطعه (1,1) در (3,1) فوراً برنده می‌شود
var sp=L.place(s,0,3);
T.eq(sp.phase,'hand','placed, now hand phase');
var sh=L.hand(sp,{a:1,b:1});
T.ok(!!sh.toPlace&&sh.toPlace.a===1&&sh.toPlace.b===1,'opponent holds (1,1)');
var m2=L.aiMove(sh,rng);
T.ok(m2.r===3&&m2.c===1,'threat at (3,1) is real');
// برد فوری گرفته می‌شود
var s3=mk({0:P(0,0),1:P(0,1),2:P(0,0)},P(0,1),[P(1,0),P(1,1),P(1,0),P(1,1)]);
var m3=L.aiMove(s3,rng);
T.ok(m3.r===0&&m3.c===3,'takes immediate win');
// استخر خالی: piece=null و خانهٔ تصادفی خالی
var s4=mk({0:P(1,1),1:P(0,1),2:P(1,0),5:P(1,1),6:P(0,1),9:P(1,0),10:P(0,0)},P(0,0),[]);
var m4=L.aiMove(s4,rng);
T.ok(m4.piece===null,'null piece when pool empty');
T.ok(s4.board[4*m4.r+m4.c]===null,'random empty cell');
"""),
        ("جریان جای‌گذاری/دادن و خطاهای ورودی", r"""
var st=L.initial(rng);
var tp={a:st.toPlace.a,b:st.toPlace.b};
var st2=L.place(st,1,2);
T.ok(!!st2.board[6]&&st2.board[6].a===tp.a&&st2.board[6].b===tp.b,'piece placed at (1,2)');
T.ok(st.board[6]===null,'original state untouched (pure)');
T.ok(st2.toPlace===null,'toPlace cleared');
T.eq(st2.phase,'hand','hand phase');
T.eq(st2.turn,0,'same turn');
var pc=st2.pool[0];
var st3=L.hand(st2,pc);
T.eq(st3.pool.length,6,'pool shrunk');
T.ok(!!st3.toPlace&&st3.toPlace.a===pc.a&&st3.toPlace.b===pc.b,'handed piece is next toPlace');
T.eq(st3.turn,1,'turn flipped');
T.eq(st3.phase,'place','place phase');
T.throws(function(){L.place(st2,1,2);},'occupied rejected');
T.throws(function(){L.place(st2,0,0);},'place during hand phase');
T.throws(function(){L.place(st,-1,0);},'out of range');
T.throws(function(){L.hand(st,{a:0,b:0});},'hand during place phase');
T.throws(function(){L.hand(st2,{a:5,b:5});},'piece not in pool');
"""),
        ("شبیه‌سازی کامل AI مقابل AI", r"""
var st=L.initial(rng),steps=0,places=0;
while(st.phase!=='over'&&steps<16){
 if(st.phase==='place'){var m=L.aiMove(st,rng);st=L.place(st,m.r,m.c);places++;}
 else{var pc=st.pool[Math.floor(rng()*st.pool.length)];st=L.hand(st,pc);}
 steps++;
}
T.ok(st.phase==='over','game over');
T.ok(steps<=16,'short game: '+steps);
T.eq(places,8,'8 placements');
var filled=0,i;for(i=0;i<16;i++)if(st.board[i])filled++;
if(st.draw){T.eq(filled,8,'draw: 8 pieces on board');T.ok(st.winner===null,'no winner on draw');}
else{T.ok(st.winner===0||st.winner===1,'winner set');T.ok(!!st.winLine&&st.winLine.length===4,'win line of 4');T.ok(filled>=4,'pieces present');}
"""),
    ],
)

fox = G(
    slug="fox-and-hounds",
    title="روباه و سگ‌ها",
    cat="board",
    icon="◉",
    g1="#d9a441",
    g2="#3fb8af",
    desc="روباه و سگ‌ها روی خانه‌های تیرهٔ صفحهٔ شطرنجی: شما روباه هستید و چهار سگ فقط رو به جلو حرکت می‌کنند. خود را به ردیف نخست برسانید و از محاصره بگریزید.",
    hint="روباه مورب در هر چهار جهت حرکت می‌کند و سگ‌ها فقط رو به جلو؛ اگر حرکتی برایتان نماند می‌بازید و اگر سگ‌ها بی‌حرکت شوند یا به ردیف اول برسید برنده‌اید.",
    logic=FOX_LOGIC, ui=FOX_UI, css=FOX_CSS,
    engines=("common",), seed=12345,
    tests=[
        ("خانه‌های تیره و چیدمان آغازین", r"""
T.ok(L.isDark(0,1),'dark (0,1)');T.ok(L.isDark(7,4),'dark (7,4)');T.ok(L.isDark(3,2),'dark (3,2)');T.ok(L.isDark(6,5),'dark (6,5)');
T.ok(!L.isDark(0,0),'light (0,0)');T.ok(!L.isDark(7,7),'light (7,7)');T.ok(!L.isDark(4,2),'light (4,2)');
var st=L.initial();
T.eq(st.fox.r,7,'fox row');T.eq(st.fox.c,4,'fox col');
T.eq(st.hounds.length,4,'4 hounds');
var got=[],i;for(i=0;i<4;i++)got.push(st.hounds[i].r+','+st.hounds[i].c);
T.eq(got.join('|'),'0,1|0,3|0,5|0,7','hounds placement');
T.eq(st.turn,'fox','fox moves first');
T.eq(L.winner(st),0,'ongoing');
for(i=0;i<4;i++)T.ok(L.isDark(st.hounds[i].r,st.hounds[i].c),'hound on dark');
T.ok(L.isDark(st.fox.r,st.fox.c),'fox on dark');
"""),
        ("حرکت مجاز روباه و سگ‌ها", r"""
function S(f,hs,turn){return {fox:{r:f[0],c:f[1]},hounds:hs.map(function(h){return {r:h[0],c:h[1]};}),turn:turn||'fox'};}
var fm=L.legalMoves(S([3,4],[[0,1],[0,3],[0,5],[0,7]]),'fox');
T.eq(fm.length,4,'fox has 4 diagonals');
var d=fm.map(function(m){return m.to.r+','+m.to.c;}).sort().join('|');
T.eq(d,'2,3|2,5|4,3|4,5','fox destinations');
var hm=L.legalMoves(S([7,4],[[0,1],[0,3],[0,5],[0,7]],'hounds'),'hounds');
T.eq(hm.length,7,'7 hound moves (corner has 1)');
var i;for(i=0;i<hm.length;i++)T.ok(hm[i].to.r===1,'hounds forward only');
var hm2=L.legalMoves(S([7,4],[[0,1],[0,3],[1,2],[0,7]],'hounds'),'hounds');
var dd={};for(i=0;i<hm2.length;i++)dd[hm2[i].to.r+','+hm2[i].to.c]=1;
T.ok(!dd['1,2'],'blocked destination excluded');
T.ok(!!dd['1,0']&&!!dd['1,4']&&!!dd['1,6']&&!!dd['2,1']&&!!dd['2,3'],'open destinations present');
T.eq(hm2.length,5,'5 moves remain');
T.eq(L.legalMoves(S([7,0],[[0,1],[0,3],[0,5],[0,7]]),'fox').length,1,'corner fox has 1 move');
"""),
        ("رسیدن روباه به ردیف نخست", r"""
var st={fox:{r:1,c:2},hounds:[{r:0,c:5},{r:2,c:5},{r:4,c:1},{r:6,c:3}],turn:'fox'};
var st2=L.applyMove(st,'fox',{r:1,c:2},{r:0,c:1});
T.eq(st2.fox.r,0,'fox at row 0');
T.eq(st2.turn,'hounds','turn rotated');
T.eq(L.winner(st2),1,'fox wins');
T.eq(L.winner({fox:{r:0,c:3},hounds:[{r:2,c:1},{r:2,c:3},{r:4,c:1},{r:4,c:3}],turn:'hounds'}),1,'static row-0 win');
"""),
        ("محاصرهٔ کامل روباه", r"""
var st={fox:{r:7,c:0},hounds:[{r:6,c:1},{r:0,c:3},{r:0,c:5},{r:0,c:7}],turn:'fox'};
T.eq(L.legalMoves(st,'fox').length,0,'no fox moves');
T.eq(L.winner(st),-1,'trapped fox: hounds win');
T.eq(L.winner({fox:{r:7,c:0},hounds:[{r:6,c:1},{r:0,c:3},{r:0,c:5},{r:0,c:7}],turn:'hounds'}),0,'not decided on hounds turn');
var st2={fox:{r:4,c:3},hounds:[{r:3,c:2},{r:3,c:4},{r:5,c:2},{r:5,c:4}],turn:'fox'};
T.eq(L.winner(st2),-1,'four-side encirclement');
"""),
        ("بی‌حرکتی سگ‌ها", r"""
var st={fox:{r:5,c:4},hounds:[{r:7,c:0},{r:7,c:2},{r:7,c:4},{r:7,c:6}],turn:'hounds'};
T.eq(L.legalMoves(st,'hounds').length,0,'hounds cannot move');
T.eq(L.winner(st),1,'stuck hounds: fox wins');
var st2={fox:{r:5,c:4},hounds:[{r:7,c:0},{r:7,c:2},{r:6,c:3},{r:7,c:6}],turn:'hounds'};
T.ok(L.legalMoves(st2,'hounds').length>0,'one hound still moves');
T.eq(L.winner(st2),0,'game ongoing');
"""),
        ("رد شدن حرکت‌های نامعتبر", r"""
var st=L.initial();
T.throws(function(){L.applyMove(st,'hounds',{r:0,c:1},{r:1,c:2});},'wrong turn');
T.throws(function(){L.applyMove(st,'fox',{r:7,c:4},{r:6,c:4});},'not diagonal');
T.throws(function(){L.applyMove(st,'fox',{r:7,c:4},{r:5,c:2});},'two-square jump');
T.throws(function(){L.applyMove(st,'fox',{r:5,c:5},{r:4,c:4});},'unknown piece');
T.throws(function(){L.applyMove(st,'fox',{r:7,c:4},{r:8,c:5});},'off board');
var st2={fox:{r:7,c:4},hounds:[{r:6,c:5},{r:0,c:3},{r:0,c:5},{r:0,c:7}],turn:'hounds'};
T.throws(function(){L.applyMove(st2,'hounds',{r:6,c:5},{r:7,c:4});},'occupied target');
var bad={fox:{r:0,c:0},hounds:[{r:0,c:1},{r:0,c:3},{r:0,c:5},{r:0,c:7}],turn:'fox'};
T.throws(function(){L.applyMove(bad,'fox',{r:0,c:0},{r:1,c:1});},'light target');
var st3=L.applyMove(st2,'hounds',{r:6,c:5},{r:7,c:6});
T.eq(st3.hounds[0].r,7,'hound advanced');
T.eq(st3.turn,'fox','turn rotated');
T.eq(st3.fox.r,7,'fox untouched');
"""),
        ("بازی کامل AI مقابل AI", r"""
function foxAI(s,r){var ms=L.legalMoves(s,'fox');if(!ms.length)return null;var best=-9,p=[],i;for(i=0;i<ms.length;i++){var sc=7-ms[i].to.r;if(sc>best){best=sc;p=[ms[i]];}else if(sc===best)p.push(ms[i]);}return p[Math.floor(r()*p.length)];}
var st0=L.initial();st0.turn='hounds';
var h0=L.aiMove(st0,rng);
T.ok(!!h0&&!!h0.from&&!!h0.to,'hounds AI returns a move');
var ok=false,ms0=L.legalMoves(st0,'hounds'),i;
for(i=0;i<ms0.length;i++){var mm=ms0[i];if(mm.from.r===h0.from.r&&mm.from.c===h0.from.c&&mm.to.r===h0.to.r&&mm.to.c===h0.to.c)ok=true;}
T.ok(ok,'AI move is a legal move');
var st=L.initial(),plies=0,w=0;
while((w=L.winner(st))===0&&plies<120){
 if(st.turn==='fox'){var m=foxAI(st,rng);if(!m){w=-1;break;}st=L.applyMove(st,'fox',m.from,m.to);}
 else{var h=L.aiMove(st,rng);if(!h){w=1;break;}st=L.applyMove(st,'hounds',h.from,h.to);}
 plies++;
 T.ok(L.isDark(st.fox.r,st.fox.c),'fox stays on dark');
}
T.ok(w!==0,'decisive result');
T.ok(w===1||w===-1,'valid winner');
T.ok(plies<=120,'game length: '+plies);
"""),
    ],
)

GAMES = [quarto, fox]
