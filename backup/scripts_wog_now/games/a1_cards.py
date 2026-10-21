# -*- coding: utf-8 -*-
# AG-A1: pasoor + hokm - two Persian browser card games in one batch file.
from lib_mini import G

PASOOR_LOGIC = r"""
function pShuffle(a,rng){rng=rng||Math.random;for(var i=a.length-1;i>0;i--){var j=Math.floor(rng()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
function pDeck(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<=13;r++)d.push({s:s,r:r});return d;}
function pKey(c){return c.s*16+c.r;}
function pKhasht(c){return c.s===2&&c.r===10;}
function pVal(c){var v=0;if(c.r===1)v+=1;if(pKhasht(c))v+=3;if(c.s===3&&c.r===2)v+=2;return v;}
function pSubs(tb,rank){
  var out=[],cur=[];
  function dfs(i,sum){
    if(sum===rank&&cur.length>=2)out.push(cur.slice());
    if(i>=tb.length||sum>=rank)return;
    for(var j=i;j<tb.length;j++){
      if(sum+tb[j].r>rank)continue;
      cur.push(tb[j]);dfs(j+1,sum+tb[j].r);cur.pop();
    }
  }
  dfs(0,0);
  out.sort(function(a,b){return b.length-a.length;});
  return out;
}
function pOpts(st,card){
  var tb=st.table,opts=[],i,k,ok,taken={},same=[];
  if(!tb.length)return [];
  if(pKhasht(card))return [{cards:tb.slice(),sweep:true}];
  if(card.r>=11){
    for(i=0;i<tb.length;i++)if(tb[i].r===card.r)same.push(tb[i]);
    return same.length?[{cards:same}]:[];
  }
  var subs=pSubs(tb,card.r);
  for(i=0;i<subs.length;i++){
    ok=true;
    for(k=0;k<subs[i].length;k++){if(taken[pKey(subs[i][k])]){ok=false;break;}}
    if(!ok)continue;
    for(k=0;k<subs[i].length;k++)taken[pKey(subs[i][k])]=1;
    opts.push({cards:subs[i]});
  }
  for(i=0;i<tb.length;i++)if(tb[i].r===card.r)same.push(tb[i]);
  if(same.length){
    ok=true;
    for(k=0;k<same.length;k++){if(taken[pKey(same[k])]){ok=false;break;}}
    if(ok)opts.push({cards:same});
  }
  return opts;
}
function pDeal(st){
  if(st.hands[0].length||st.hands[1].length||!st.deck.length)return;
  st.hands[0]=st.deck.splice(0,4);
  st.hands[1]=st.deck.splice(0,4);
}
function pNewGame(rng){
  rng=rng||Math.random;
  var d=pShuffle(pDeck(),rng);
  var st={table:d.slice(0,4),deck:d.slice(4),hands:[[],[]],piles:[[],[]],lastCapturer:-1,turn:0,over:false};
  pDeal(st);
  return st;
}
function pApplyPlay(st,pi,hi,option){
  if(st.over)return;
  var hand=st.hands[pi],card=hand.splice(hi,1)[0],cap=[],i,j,k;
  if(option&&option.cards&&option.cards.length){
    if(pKhasht(card)){cap=st.table.slice();st.table=[];}
    else{
      for(i=0;i<option.cards.length;i++){
        k=pKey(option.cards[i]);
        for(j=0;j<st.table.length;j++){
          if(pKey(st.table[j])===k){cap.push(st.table.splice(j,1)[0]);break;}
        }
      }
    }
    st.piles[pi].push(card);
    for(i=0;i<cap.length;i++)st.piles[pi].push(cap[i]);
    st.lastCapturer=pi;
  }else{
    st.table.push(card);
  }
  st.turn=1-pi;
  pDeal(st);
  if(!st.hands[0].length&&!st.hands[1].length&&!st.deck.length){
    st.over=true;
    if(st.lastCapturer>=0&&st.table.length){
      var lp=st.piles[st.lastCapturer];
      for(i=0;i<st.table.length;i++)lp.push(st.table[i]);
      st.table=[];
    }
  }
}
function pAi(st){
  var hand=st.hands[st.turn],i,j,k,bi=-1,bo=null,bl=-1,bv=-1;
  if(!hand||!hand.length)return null;
  for(i=0;i<hand.length;i++){
    if(pKhasht(hand[i])&&st.table.length)return {handIdx:i,option:{cards:st.table.slice(),sweep:true}};
  }
  for(i=0;i<hand.length;i++){
    var os=pOpts(st,hand[i]);
    for(j=0;j<os.length;j++){
      var ln=os[j].cards.length,v=0;
      for(k=0;k<os[j].cards.length;k++)v+=pVal(os[j].cards[k]);
      if(ln>bl||(ln===bl&&v>bv)){bi=i;bo=os[j];bl=ln;bv=v;}
    }
  }
  if(bo)return {handIdx:bi,option:bo};
  var di=0,dw=pVal(hand[0])*100+hand[0].r*2+hand[0].s;
  for(i=1;i<hand.length;i++){
    var w=pVal(hand[i])*100+hand[i].r*2+hand[i].s;
    if(w<dw){dw=w;di=i;}
  }
  return {handIdx:di,option:null};
}
function pScore(st){
  function one(pile){
    var c={cards:pile.length,aces:0,khasht:0,khaj2:0,majority:0,total:0},i;
    for(i=0;i<pile.length;i++){
      if(pile[i].r===1)c.aces++;
      if(pKhasht(pile[i]))c.khasht=1;
      if(pile[i].s===3&&pile[i].r===2)c.khaj2=1;
    }
    return c;
  }
  var a=one(st.piles[0]),b=one(st.piles[1]);
  if(a.cards>b.cards)a.majority=1;else if(b.cards>a.cards)b.majority=1;
  a.total=a.aces+3*a.khasht+2*a.khaj2+3*a.majority;
  b.total=b.aces+3*b.khasht+2*b.khaj2+3*b.majority;
  return {p1:a,p2:b};
}
var WOG_LOGIC={
  newGame:pNewGame,
  legalCaptures:pOpts,
  applyPlay:pApplyPlay,
  aiChoose:pAi,
  scoreGame:pScore,
  isRoundOver:function(st){return !!st.over;}
};
"""

PASOOR_UI = r"""
var st=null,pending=null;
var HINT='۱۰ خشت کل میز را جمع می‌کند؛ کارت عددی، کارت هم‌ارزش یا چند کارت با جمع برابر را می‌گیرد.';
function newGame(){
  st=L.newGame();pending=null;render();
  if(st.turn===1)setTimeout(aiTurn,650);
}
function render(){
  var app=$('#app');app.innerHTML='';
  var s=L.scoreGame(st),i;
  var dealt=52-st.deck.length,hn=Math.max(1,Math.ceil((dealt-4)/8));
  hud('دست '+fa(hn)+' از ۶ | امتیاز: شما '+fa(s.p1.total)+' - حریف '+fa(s.p2.total)+' | کارت‌های برده: '+fa(st.piles[0].length)+' / '+fa(st.piles[1].length));
  $('#hint').textContent=st.over?'بازی تمام شد':(st.turn===0?'نوبت شماست؛ روی یک کارت بزنید':'نوبت حریف...');
  var nb=ce('button','ps-btn','بازی جدید');
  nb.setAttribute('data-smoke','new');nb.onclick=function(){newGame();};
  app.appendChild(nb);
  var tb=ce('div','ps-row','');
  for(i=0;i<st.table.length;i++)tb.appendChild(cardEl(st.table[i],true));
  app.appendChild(tb);
  var op=ce('div','ps-row ps-opp','');
  op.appendChild(ce('span','ps-lbl','حریف: '+fa(st.hands[1].length)+' کارت'));
  for(i=0;i<st.hands[1].length;i++)op.appendChild(cardEl({s:0,r:2},false,'tiny'));
  app.appendChild(op);
  var hd=ce('div','ps-row ps-hand','');
  for(i=0;i<st.hands[0].length;i++){
    (function(idx){
      var c=st.hands[0][idx],e=cardEl(c,true);
      if(st.turn===0&&!st.over&&!pending){
        e.setAttribute('data-smoke','card'+idx);
        e.onclick=function(){tapHand(idx);};
      }else{
        e.classList.add('ps-dim');
      }
      hd.appendChild(e);
    })(i);
  }
  app.appendChild(hd);
  if(pending){
    var pr=ce('div','ps-row','');
    pr.appendChild(ce('span','ps-lbl','گزینه‌های گرفتن:'));
    for(i=0;i<pending.opts.length;i++){
      (function(oi){
        var b=ce('button','ps-btn ps-cap','بردن '+fa(pending.opts[oi].cards.length)+' کارت');
        b.setAttribute('data-smoke','cap'+oi);
        b.onclick=function(){pickOpt(oi);};
        pr.appendChild(b);
      })(i);
    }
    var pb=ce('button','ps-btn','بدون گرفتن');
    pb.setAttribute('data-smoke','pass');pb.onclick=pickPass;
    pr.appendChild(pb);
    app.appendChild(pr);
  }
}
function tapHand(idx){
  if(st.over||st.turn!==0)return;
  var c=st.hands[0][idx],os=L.legalCaptures(st,c);
  if(!os.length){L.applyPlay(st,0,idx,null);after();return;}
  if(os.length===1){L.applyPlay(st,0,idx,os[0]);after();return;}
  pending={idx:idx,opts:os};render();
}
function pickOpt(oi){
  if(!pending)return;
  var idx=pending.idx,o=pending.opts[oi];pending=null;
  L.applyPlay(st,0,idx,o);after();
}
function pickPass(){
  if(!pending)return;
  var idx=pending.idx;pending=null;
  L.applyPlay(st,0,idx,null);after();
}
function after(){
  render();
  if(L.isRoundOver(st)){setTimeout(end,600);return;}
  if(st.turn===1)setTimeout(aiTurn,550);
}
function aiTurn(){
  if(st.over||st.turn!==1){render();return;}
  var mv=L.aiChoose(st);
  if(mv)L.applyPlay(st,st.turn,mv.handIdx,mv.option);
  render();
  if(L.isRoundOver(st))setTimeout(end,600);
}
function end(){
  var s=L.scoreGame(st);
  var maj=s.p1.majority?'شما':(s.p2.majority?'حریف':'مساوی');
  var msg='کارت‌ها '+fa(s.p1.cards)+'-'+fa(s.p2.cards)+' | آک '+fa(s.p1.aces)+'-'+fa(s.p2.aces)+' | ۱۰ خشت: '+(s.p1.khasht?'شما':'حریف')+' | ۲ گشنیز: '+(s.p1.khaj2?'شما':'حریف')+' | اکثریت: '+maj;
  hud(msg+' | نتیجه نهایی: '+fa(s.p1.total)+' - '+fa(s.p2.total));
  ovl(s.p1.total>s.p2.total?'شما بردید!':(s.p1.total===s.p2.total?'مساوی شد':'حریف برد'),msg,'بازی جدید',newGame);
}
newGame();
"""

PASOOR_CSS = r"""
.ps-row{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;align-items:center;margin:10px 0}
.ps-btn{padding:7px 16px;border-radius:9px;border:1px solid #567;cursor:pointer;font-family:inherit;font-size:14px;background:#fff}
.ps-cap{border-color:#2a9d8f;background:#e8f6f3}
.ps-dim{opacity:.45}
.ps-lbl{font-size:13px;opacity:.85}
.ps-hand{min-height:86px;padding:4px}
"""

HOKM_LOGIC = r"""
function hShuffle(a,rng){rng=rng||Math.random;for(var i=a.length-1;i>0;i--){var j=Math.floor(rng()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
function hDeck(){var d=[],s,r;for(s=0;s<4;s++)for(r=1;r<=13;r++)d.push({s:s,r:r});return d;}
function hV(r){return r===1?14:r;}
function hT(p){return p%2;}
function hNewGame(rng){
  rng=rng||Math.random;
  var st={hands:[[],[],[],[]],deck:[],trick:[],turn:0,dealer:Math.floor(rng()*4),hokm:-1,hakam:-1,phase:'hokm',roundTricks:[0,0],trickNo:0,scores:[0,0],history:[],matchOver:false,roundWinner:-1,_rng:rng};
  hDeal5(st);
  return st;
}
function hDeal5(st){
  var rng=st._rng||Math.random,ok=false,tries=0,d,i,j;
  do{
    d=hShuffle(hDeck(),rng);
    for(i=0;i<4;i++)st.hands[i]=d.slice(i*5,i*5+5);
    st.deck=d.slice(20);
    ok=false;
    for(i=0;i<4;i++){for(j=0;j<5;j++){if(st.hands[i][j].r===1){ok=true;break;}}if(ok)break;}
    tries++;
  }while(!ok&&tries<40);
}
function hHakam(st){
  for(var i=0;i<4;i++){
    var p=(st.dealer+1+i)%4;
    for(var j=0;j<st.hands[p].length;j++)if(st.hands[p][j].r===1)return p;
  }
  return (st.dealer+1)%4;
}
function hAiHokm(st,pi){
  var cnt=[0,0,0,0],i;
  for(i=0;i<st.hands[pi].length;i++)cnt[st.hands[pi][i].s]++;
  var b=0;
  for(i=1;i<4;i++)if(cnt[i]>cnt[b])b=i;
  return b;
}
function hDealRest(st,suit){
  st.hokm=suit;
  for(var i=0;i<4;i++){
    var more=st.deck.splice(0,8);
    for(var j=0;j<more.length;j++)st.hands[i].push(more[j]);
  }
  if(st.hakam<0)st.hakam=hHakam(st);
  st.phase='play';st.turn=st.hakam;
}
function hLegal(st,pi){
  if(st.phase!=='play')return [];
  var hand=st.hands[pi],out=[],i;
  if(!st.trick.length)return hand.slice();
  var led=st.trick[0].c.s;
  for(i=0;i<hand.length;i++)if(hand[i].s===led)out.push(hand[i]);
  return out.length?out:hand.slice();
}
function hWinner(trick,hokm){
  var best=trick[0],i;
  for(i=1;i<trick.length;i++){
    var bc=best.c,ec=trick[i].c;
    if(ec.s===hokm&&bc.s!==hokm)best=trick[i];
    else if(bc.s===ec.s&&hV(ec.r)>hV(bc.r))best=trick[i];
  }
  return best.p;
}
function hPlay(st,pi,card){
  if(st.phase!=='play')throw new Error('round not active');
  if(pi!==st.turn)throw new Error('not your turn');
  var legal=hLegal(st,pi),idx=-1,ok=false,i;
  for(i=0;i<st.hands[pi].length;i++){
    if(st.hands[pi][i].s===card.s&&st.hands[pi][i].r===card.r){idx=i;break;}
  }
  if(idx<0)throw new Error('card not in hand');
  for(i=0;i<legal.length;i++){
    if(legal[i].s===card.s&&legal[i].r===card.r){ok=true;break;}
  }
  if(!ok)throw new Error('must follow suit');
  st.hands[pi].splice(idx,1);
  st.trick.push({p:pi,c:{s:card.s,r:card.r}});
  if(st.trick.length===4){
    var w=hWinner(st.trick,st.hokm),t=hT(w);
    st.roundTricks[t]++;st.trickNo++;
    if(st.roundTricks[t]>=7&&st.roundWinner<0)st.roundWinner=t;
    st.trick=[];st.turn=w;
  }else{
    st.turn=(pi+1)%4;
  }
}
function hOver(st){return st.trickNo>=13;}
function hPoints(st){
  if(st.trickNo<13)return st;
  var w=st.roundTricks[0]>=7?0:1,pts=st.roundTricks[1-w]===0?2:1;
  st.scores[w]+=pts;
  st.history.push({hokm:st.hokm,tricks:[st.roundTricks[0],st.roundTricks[1]],winner:w,points:pts});
  st.roundWinner=-1;
  if(st.scores[w]>=7){st.matchOver=true;st.phase='matchover';return st;}
  st.dealer=(st.dealer+1)%4;
  st.hokm=-1;st.hakam=-1;st.phase='hokm';st.trick=[];st.trickNo=0;st.roundTricks=[0,0];
  st.turn=(st.dealer+1)%4;
  hDeal5(st);
  return st;
}
function hMn(a,f){var b=a[0];for(var i=1;i<a.length;i++)if(f(a[i])<f(b))b=a[i];return b;}
function hMx(a,f){var b=a[0];for(var i=1;i<a.length;i++)if(f(a[i])>f(b))b=a[i];return b;}
function hAi(st,pi){
  var legal=hLegal(st,pi),i,i2;
  if(!legal.length)return null;
  if(!st.trick.length){
    var cnt=[0,0,0,0],best=0,sc=[];
    for(i=0;i<legal.length;i++)cnt[legal[i].s]++;
    for(i=1;i<4;i++)if(cnt[i]>cnt[best])best=i;
    for(i=0;i<legal.length;i++)if(legal[i].s===best)sc.push(legal[i]);
    if(cnt[best]>=3)return hMx(sc,function(c){return hV(c.r);});
    return hMn(legal,function(c){return hV(c.r);});
  }
  var led=st.trick[0].c.s,w=hWinner(st.trick,st.hokm),pw=hT(w)===hT(pi),wc=null;
  for(i=0;i<st.trick.length;i++)if(st.trick[i].p===w)wc=st.trick[i].c;
  var follow=[];
  for(i=0;i<legal.length;i++)if(legal[i].s===led)follow.push(legal[i]);
  if(follow.length){
    var beat=[];
    if(wc.s===led)for(i2=0;i2<follow.length;i2++)if(hV(follow[i2].r)>hV(wc.r))beat.push(follow[i2]);
    if(!pw&&beat.length)return hMn(beat,function(c){return hV(c.r);});
    return hMn(follow,function(c){return hV(c.r);});
  }
  var tr=[];
  for(i=0;i<legal.length;i++)if(legal[i].s===st.hokm)tr.push(legal[i]);
  if(!pw&&tr.length){
    var bt=[];
    for(i2=0;i2<tr.length;i2++)if(wc.s!==st.hokm||hV(tr[i2].r)>hV(wc.r))bt.push(tr[i2]);
    if(bt.length)return hMn(bt,function(c){return hV(c.r);});
  }
  return hMn(legal,function(c){return hV(c.r);});
}
var WOG_LOGIC={
  newGame:hNewGame,
  determineHakam:hHakam,
  aiPickHokm:hAiHokm,
  dealRest:hDealRest,
  legalPlays:hLegal,
  playCard:hPlay,
  trickWinner:hWinner,
  aiChoose:hAi,
  isRoundOver:hOver,
  applyRoundPoints:hPoints
};
"""

HOKM_UI = r"""
var st=null;
var SN=['پیک','دل','خشت','گشنیز'];
var PN=['شما','حریف راست','یار شما','حریف چپ'];
function newMatch(){st=L.newGame();phaseHokm();}
function phaseHokm(){
  st.hakam=L.determineHakam(st);
  if(st.hakam===0){render();return;}
  L.dealRest(st,L.aiPickHokm(st,st.hakam));
  render();
  if(st.turn!==0)setTimeout(aiStep,500);
}
function pickSuit(su){
  if(!st||st.phase!=='hokm')return;
  L.dealRest(st,su);
  render();
  if(st.turn!==0)setTimeout(aiStep,500);
}
function tapCard(c){
  if(st.phase!=='play'||st.turn!==0)return;
  var legal=L.legalPlays(st,0),ok=false,i;
  for(i=0;i<legal.length;i++)if(legal[i].s===c.s&&legal[i].r===c.r){ok=true;break;}
  if(!ok){toast('باید خال '+SN[st.trick[0].c.s]+' بازی کنید');return;}
  L.playCard(st,0,c);
  post();
}
function post(){
  render();
  if(L.isRoundOver(st)){setTimeout(roundEnd,800);return;}
  if(st.turn!==0)setTimeout(aiStep,430);
}
function aiStep(){
  if(st.phase!=='play'||st.turn===0){render();return;}
  var before=st.trick.length;
  var c=L.aiChoose(st,st.turn);
  if(c)L.playCard(st,st.turn,c);
  render();
  if(L.isRoundOver(st)){setTimeout(roundEnd,850);return;}
  setTimeout(aiStep,(before===3&&st.trick.length===0)?950:430);
}
function roundEnd(){
  L.applyRoundPoints(st);
  render();
  if(st.matchOver){
    ovl(st.scores[0]>=7?'برد تیم شما!':'برد تیم حریف','نتیجه نهایی: تیم شما '+fa(st.scores[0])+' - حریف '+fa(st.scores[1]),'بازی جدید',newMatch);
    return;
  }
  toast('امتیاز این دست ثبت شد؛ دست بعد...');
  phaseHokm();
}
function render(){
  if(!st)return;
  var app=$('#app');app.innerHTML='';
  var i,q;
  hud('دور '+fa(st.history.length+1)+' | امتیاز: ما '+fa(st.scores[0])+' - حریف '+fa(st.scores[1])+' | ترفندها: '+fa(st.roundTricks[0])+' - '+fa(st.roundTricks[1])+' | حکم: '+(st.hokm>=0?SUITS[st.hokm]:'؟'));
  $('#hint').textContent=st.phase==='hokm'?(st.hakam===0?'شما حاکم هستید؛ خال حکم را انتخاب کنید':'در حال تعیین حاکم...'):(st.turn===0?'نوبت شماست':'نوبت '+PN[st.turn]);
  var nb=ce('button','hk-btn','بازی جدید');
  nb.setAttribute('data-smoke','new');nb.onclick=newMatch;
  app.appendChild(nb);
  if(st.phase==='hokm'){
    var hd=ce('div','hk-row','');
    for(i=0;i<st.hands[0].length;i++)hd.appendChild(cardEl(st.hands[0][i],true));
    app.appendChild(hd);
    if(st.hakam===0){
      var pk=ce('div','hk-row','');
      for(i=0;i<4;i++){
        (function(su){
          var b=ce('button','hk-suit',SUITS[su]+' '+SN[su]);
          b.setAttribute('data-smoke','suit'+su);
          b.onclick=function(){pickSuit(su);};
          pk.appendChild(b);
        })(i);
      }
      app.appendChild(pk);
    }
    return;
  }
  if(st.phase==='matchover'){
    app.appendChild(ce('div','hk-row hk-info','بازی تمام شد'));
    return;
  }
  var opp=ce('div','hk-row','');
  for(q=1;q<4;q++){
    var box=ce('div','hk-ai-box',PN[q]+' ('+fa(st.hands[q].length)+') ');
    box.appendChild(cardEl({s:0,r:2},false,'tiny'));
    opp.appendChild(box);
  }
  app.appendChild(opp);
  var tr=ce('div','hk-row','');
  var slots=[null,null,null,null];
  for(i=0;i<st.trick.length;i++)slots[st.trick[i].p]=st.trick[i].c;
  for(i=0;i<4;i++){
    var cell=ce('div','hk-slot',PN[i]);
    if(slots[i])cell.appendChild(cardEl(slots[i],true));
    tr.appendChild(cell);
  }
  app.appendChild(tr);
  var hd2=ce('div','hk-row hk-hand','');
  var legal=st.turn===0?L.legalPlays(st,0):[];
  for(i=0;i<st.hands[0].length;i++){
    (function(c){
      var e=cardEl(c,true),isL=false,q2;
      for(q2=0;q2<legal.length;q2++)if(legal[q2].s===c.s&&legal[q2].r===c.r){isL=true;break;}
      if(isL){
        e.setAttribute('data-smoke','play');
        e.onclick=function(){tapCard(c);};
      }else{
        e.classList.add('hk-dim');
      }
      hd2.appendChild(e);
    })(st.hands[0][i]);
  }
  app.appendChild(hd2);
}
newMatch();
"""

HOKM_CSS = r"""
.hk-row{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;align-items:center;margin:10px 0}
.hk-btn{padding:7px 16px;border-radius:9px;border:1px solid #567;cursor:pointer;font-family:inherit;background:#fff}
.hk-suit{font-size:18px;padding:10px 18px;border-radius:10px;border:2px solid #8899aa;cursor:pointer;background:#fff;font-family:inherit}
.hk-dim{opacity:.4}
.hk-ai-box{display:flex;align-items:center;gap:4px;font-size:13px;border:1px solid #ccd;border-radius:8px;padding:4px 8px}
.hk-slot{min-width:72px;min-height:98px;border:1px dashed #99a;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px;padding:4px;gap:4px}
.hk-hand{min-height:102px}
.hk-info{font-size:15px}
"""

TESTS_PASOOR = [
("تک خشت کل میز را جمع می‌کند", r"""
var st=L.newGame(rng);
st.table=[{s:0,r:3},{s:1,r:5},{s:3,r:9},{s:0,r:11}];
st.hands[0]=[{s:2,r:10}];st.hands[1]=[];st.deck=[];
var opts=L.legalCaptures(st,{s:2,r:10});
T.eq(opts.length,1,'one sweep option');
T.eq(opts[0].cards.length,4,'sweep covers whole table');
L.applyPlay(st,0,0,opts[0]);
T.eq(st.table.length,0,'table empty after sweep');
T.eq(st.piles[0].length,5,'played card + 4 captured');
T.eq(st.lastCapturer,0,'capturer recorded');
T.ok(L.isRoundOver(st),'round over after last cards');
"""),
("گرفتن کارت هم‌ارزش", r"""
var st=L.newGame(rng);
st.table=[{s:1,r:7},{s:2,r:4},{s:0,r:13}];
st.hands[0]=[{s:3,r:7}];st.hands[1]=[];
st.deck=[{s:1,r:9},{s:2,r:9},{s:3,r:9},{s:0,r:9},{s:1,r:10},{s:2,r:11},{s:3,r:12},{s:0,r:6}];
var opts=L.legalCaptures(st,{s:3,r:7});
T.eq(opts.length,1,'single option');
T.eq(opts[0].cards.length,1,'one card captured');
T.eq(opts[0].cards[0].s,1,'it is the 7 of hearts');
L.applyPlay(st,0,0,opts[0]);
T.eq(st.piles[0].length,2,'2 cards in pile');
T.eq(st.table.length,2,'2 cards left on table');
T.eq(st.lastCapturer,0,'capturer recorded');
"""),
("گرفتن با مجموع کارت‌ها و ترجیح بزرگ‌ترین زیرمجموعه", r"""
var st=L.newGame(rng);
st.table=[{s:0,r:3},{s:1,r:4}];
st.hands[0]=[{s:2,r:7}];st.hands[1]=[];st.deck=[];
var opts=L.legalCaptures(st,{s:2,r:7});
T.eq(opts.length,1,'one subset option');
T.eq(opts[0].cards.length,2,'takes 3+4');
T.eq(opts[0].cards[0].r+opts[0].cards[1].r,7,'subset sums to 7');
L.applyPlay(st,0,0,opts[0]);
T.eq(st.table.length,0,'table emptied by capture');
T.eq(st.piles[0].length,3,'3 cards gained');
var st2=L.newGame(rng);
st2.table=[{s:0,r:1},{s:1,r:2},{s:2,r:3},{s:3,r:4}];
st2.hands[0]=[{s:1,r:6}];st2.hands[1]=[];st2.deck=[];
var o2=L.legalCaptures(st2,{s:1,r:6});
T.eq(o2.length,1,'largest disjoint subset kept');
T.eq(o2[0].cards.length,3,'prefers 1+2+3 over 2+4');
var st3=L.newGame(rng);
st3.table=[{s:0,r:1},{s:1,r:2},{s:2,r:3},{s:3,r:6}];
st3.hands[0]=[{s:1,r:6}];st3.hands[1]=[];st3.deck=[];
var o3=L.legalCaptures(st3,{s:1,r:6});
T.eq(o3.length,2,'subset and same-rank both offered');
"""),
("اسلیم فقط هم‌ارزش می‌گیرد", r"""
var st=L.newGame(rng);
st.table=[{s:0,r:5},{s:1,r:6}];
st.hands[0]=[{s:2,r:11}];st.hands[1]=[];st.deck=[];
T.eq(L.legalCaptures(st,{s:2,r:11}).length,0,'J cannot sum-capture 5+6');
L.applyPlay(st,0,0,null);
T.eq(st.table.length,3,'J stays on table');
T.eq(st.piles[0].length,0,'nothing captured');
var st2=L.newGame(rng);
st2.table=[{s:2,r:12},{s:0,r:12},{s:1,r:5}];
st2.hands[0]=[{s:3,r:12}];st2.hands[1]=[];
st2.deck=[{s:1,r:9},{s:2,r:9},{s:3,r:9},{s:0,r:9},{s:1,r:10},{s:2,r:11},{s:3,r:12},{s:0,r:6}];
var o=L.legalCaptures(st2,{s:3,r:12});
T.eq(o.length,1,'Q captures same rank');
T.eq(o[0].cards.length,2,'both queens');
L.applyPlay(st2,0,0,o[0]);
T.eq(st2.piles[0].length,3,'3 cards to pile');
T.eq(st2.table.length,1,'only the 5 left');
"""),
("امتیازدهی پایانی با وضعیت معلوم", r"""
var st=L.newGame(rng);
st.over=true;st.table=[];st.lastCapturer=1;
var p0=[{s:0,r:1},{s:1,r:1},{s:2,r:10},{s:3,r:2}],p1=[{s:3,r:1}],i;
for(i=0;i<16;i++)p0.push({s:i%4,r:5+(i%4)});
for(i=0;i<31;i++)p1.push({s:(i+1)%4,r:(i%2)?9:11});
st.piles=[p0,p1];
var s=L.scoreGame(st);
T.eq(s.p1.cards,20,'p1 count');
T.eq(s.p2.cards,32,'p2 count');
T.eq(s.p1.aces,2,'p1 aces');
T.eq(s.p2.aces,1,'p2 aces');
T.eq(s.p1.khasht,1,'p1 has 10d');
T.eq(s.p2.khasht,0,'p2 no 10d');
T.eq(s.p1.khaj2,1,'p1 has 2c');
T.eq(s.p2.khaj2,0,'p2 no 2c');
T.eq(s.p2.majority,1,'p2 majority');
T.eq(s.p1.majority,0,'p1 no majority');
T.eq(s.p1.total,7,'p1 total 2+3+2');
T.eq(s.p2.total,4,'p2 total 3+1');
var st2=L.newGame(rng);
st2.over=true;st2.table=[];
var a=[],b=[];
for(i=0;i<26;i++){a.push({s:i%4,r:5+(i%4)});b.push({s:(i+2)%4,r:(i%2)?9:11});}
st2.piles=[a,b];
var s2=L.scoreGame(st2);
T.eq(s2.p1.majority,0,'tie: no majority');
T.eq(s2.p2.majority,0,'tie: no majority');
T.eq(s2.p1.total,0,'no points on tie');
"""),
("گزینه‌های گرفتن مجزا و مجموع درست", r"""
var st=L.newGame(rng);
st.table=[{s:0,r:1},{s:1,r:6},{s:2,r:2},{s:3,r:5},{s:0,r:13}];
st.hands[0]=[{s:1,r:7},{s:3,r:13}];st.hands[1]=[];st.deck=[];
var o7=L.legalCaptures(st,{s:1,r:7});
T.eq(o7.length,2,'two disjoint sum options');
var i,j,a,b;
for(i=0;i<o7.length;i++){
  var sm=0;
  for(j=0;j<o7[i].cards.length;j++)sm+=o7[i].cards[j].r;
  T.eq(sm,7,'option sums to 7');
  for(a=0;a<o7[i].cards.length;a++){
    for(j=0;j<o7.length;j++){
      if(j===i)continue;
      for(b=0;b<o7[j].cards.length;b++)T.ok(o7[i].cards[a]!==o7[j].cards[b],'options are disjoint');
    }
  }
}
var ok=L.legalCaptures(st,{s:3,r:13});
T.eq(ok.length,1,'K option');
T.eq(ok[0].cards.length,1,'single king');
"""),
("شبیه‌سازی کامل هوش مصنوعی در برابر حریف", r"""
var st=L.newGame(rng),steps=0;
while(!L.isRoundOver(st)&&steps<200){
  steps++;
  var mv=L.aiChoose(st);
  T.ok(mv&&mv.handIdx>=0&&mv.handIdx<st.hands[st.turn].length,'ai move valid');
  L.applyPlay(st,st.turn,mv.handIdx,mv.option);
}
T.ok(L.isRoundOver(st),'round finished');
T.eq(steps,48,'exactly 48 card plays');
T.eq(st.piles[0].length+st.piles[1].length+st.table.length,52,'all 52 cards in piles+table');
var s=L.scoreGame(st);
T.eq(s.p1.total,s.p1.aces+3*s.p1.khasht+2*s.p1.khaj2+3*s.p1.majority,'p1 breakdown consistent');
T.eq(s.p2.total,s.p2.aces+3*s.p2.khasht+2*s.p2.khaj2+3*s.p2.majority,'p2 breakdown consistent');
T.eq(s.p1.cards+s.p2.cards+st.table.length,52,'score cards match piles');
"""),
]

TESTS_HOKM = [
("حاکم نخستین آک بعد از دیلر است", r"""
var st=L.newGame(rng);
var exp=-1,i,j;
for(i=0;i<4;i++){
  var p=(st.dealer+1+i)%4;
  for(j=0;j<st.hands[p].length;j++){if(st.hands[p][j].r===1){exp=p;break;}}
  if(exp>=0)break;
}
T.ok(exp>=0,'an ace exists in the first 20 cards');
T.eq(L.determineHakam(st),exp,'hakam is first ace after dealer');
var s=L.aiPickHokm(st,exp);
T.ok(s>=0&&s<4,'ai hokm pick valid 0..3');
"""),
("توزیع ۵۲ برگ یکتا", r"""
var st=L.newGame(rng);
T.ok(st.hands.every(function(h){return h.length===5;}),'5 cards each at start');
var hk=L.determineHakam(st);
T.ok(hk>=0&&hk<4,'hakam is a player');
st.hakam=hk;
var suit=L.aiPickHokm(st,hk);
T.ok(suit>=0&&suit<4,'suit 0..3');
L.dealRest(st,suit);
T.eq(st.hokm,suit,'hokm stored');
T.eq(st.phase,'play','play phase');
T.eq(st.turn,hk,'hakam leads');
T.eq(st.deck.length,0,'deck empty');
var all=[],i,j;
for(i=0;i<4;i++){
  T.eq(st.hands[i].length,13,'13 cards each');
  for(j=0;j<st.hands[i].length;j++)all.push(st.hands[i][j]);
}
T.eq(all.length,52,'52 dealt');
var seen={};
for(i=0;i<52;i++){
  var k=all[i].s+'-'+all[i].r;
  T.ok(!seen[k],'unique card '+k);
  seen[k]=1;
}
"""),
("برنده ترفند: حکم و رتبه‌ها", r"""
var t1=[{p:0,c:{s:0,r:1}},{p:1,c:{s:0,r:13}},{p:2,c:{s:0,r:12}},{p:3,c:{s:1,r:9}}];
T.eq(L.trickWinner(t1,2),0,'ace is highest of led suit');
var t2=[{p:0,c:{s:0,r:1}},{p:1,c:{s:0,r:13}},{p:2,c:{s:2,r:2}},{p:3,c:{s:0,r:12}}];
T.eq(L.trickWinner(t2,2),2,'low trump beats ace of led suit');
var t3=[{p:3,c:{s:2,r:5}},{p:0,c:{s:2,r:1}},{p:1,c:{s:2,r:13}},{p:2,c:{s:3,r:9}}];
T.eq(L.trickWinner(t3,2),0,'ace of trump beats king of trump');
var t4=[{p:0,c:{s:3,r:7}},{p:1,c:{s:2,r:13}},{p:2,c:{s:2,r:5}},{p:3,c:{s:0,r:1}}];
T.eq(L.trickWinner(t4,2),1,'higher trump wins, off-suit ignored');
var t5=[{p:0,c:{s:1,r:2}},{p:1,c:{s:3,r:13}}];
T.eq(L.trickWinner(t5,0),0,'off-suit card cannot win');
"""),
("الزام تبعیت از خال", r"""
var st=L.newGame(rng);
st.phase='play';st.hokm=2;st.turn=0;
st.hands[0]=[{s:0,r:3},{s:1,r:5},{s:2,r:7},{s:3,r:9},{s:0,r:12}];
st.trick=[{p:1,c:{s:0,r:4}}];
var legal=L.legalPlays(st,0);
T.eq(legal.length,2,'only spades legal');
T.ok(legal.every(function(c){return c.s===0;}),'led suit enforced');
T.throws(function(){L.playCard(st,0,{s:1,r:5});},'illegal play throws');
L.playCard(st,0,{s:0,r:12});
T.eq(st.trick.length,2,'card on trick');
T.eq(st.turn,1,'turn advances');
st.hands[1]=[{s:1,r:2},{s:2,r:4},{s:1,r:8}];
T.eq(L.legalPlays(st,1).length,3,'void in led suit: all cards legal');
L.playCard(st,1,{s:2,r:4});
T.eq(st.trick.length,3,'trump discard accepted');
"""),
("مسابقه کامل هوش مصنوعی تا ۷ امتیاز", r"""
var st=L.newGame(rng),guard=0;
while(!st.matchOver&&guard<5000){
  guard++;
  if(st.phase==='hokm'){
    st.hakam=L.determineHakam(st);
    L.dealRest(st,L.aiPickHokm(st,st.hakam));
  }else{
    var pi=st.turn,card=L.aiChoose(st,pi);
    T.ok(card,'ai produces a card');
    L.playCard(st,pi,card);
    if(L.isRoundOver(st))L.applyRoundPoints(st);
  }
}
T.ok(st.matchOver,'match reached 7 points');
T.ok(st.scores[0]>=7||st.scores[1]>=7,'winner team at 7+');
T.ok(st.scores[0]<7||st.scores[1]<7,'loser under 7');
T.ok(st.history.length>=7,'at least 7 rounds played');
for(var i=0;i<st.history.length;i++){
  var h=st.history[i];
  T.eq(h.tricks[0]+h.tricks[1],13,'13 tricks in round '+(i+1));
  T.ok(h.tricks[0]>=7||h.tricks[1]>=7,'winner has 7+ tricks');
  T.ok(h.tricks[0]<=6||h.tricks[1]<=6,'loser below 7');
  var loser=h.tricks[h.winner===0?1:0];
  T.eq(h.points,loser===0?2:1,'points follow sweep rule');
}
"""),
]

GAMES = [
    G("pasoor", "پاسور", "cards", "🃏", "#0ea5e9", "#f59e0b",
      "پاسور ایرانی سبک کازینو؛ گرفتن کارت‌های میز با برابری، مجموع یا تک خشت.",
      "تک خشت کل میز را جمع می‌کند؛ آک، ۲ گشنیز و اکثریت کارت امتیاز دارند.",
      logic=PASOOR_LOGIC, ui=PASOOR_UI, css=PASOOR_CSS,
      engines=("common", "card"), tests=TESTS_PASOOR),
    G("hokm", "حکم", "cards", "🎴", "#7c3aed", "#22c55e",
      "حکم چهارنفره تیمی؛ تعیین حاکم با آک، تبعیت از خال و گرفتن ترفندها.",
      "اگر خال حکم را ندارید هر کارتی می‌توانید بازی کنید؛ تیم به ۷ امتیاز برنده است.",
      logic=HOKM_LOGIC, ui=HOKM_UI, css=HOKM_CSS,
      engines=("common", "card"), tests=TESTS_HOKM),
]
