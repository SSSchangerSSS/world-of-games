# -*- coding: utf-8 -*-
# AG-I1 batch: wordle + hangman (cat="word", engines=("common","word"))
from lib_mini import G

WORDLE_LOGIC = r"""
var FA='ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی';
var WORDS=['برادر','خواهر','خواهش','انسان','سرباز','سرهنگ','خلبان','ملوان','چوپان','نانوا','مهندس','کارگر','شاگرد','غریبه','انگشت','دندان','چشمان','لبخند','شجاعت','سلامت','درمان','بهبود','زندگی','گذشته','تاریخ','امروز','دیروز','دقیقه','ثانیه','سپیده','مهتاب','ستاره','سیاره','طوفان','باران','گرداب','گلزار','گلدان','جزیره','استخر','پلکان','باغچه','ایوان','انبار','میدان','بازار','مغازه','مدرسه','اداره','کلیسا','الفبا','عبارت','حکایت','ترانه','سنتور','پیانو','دایره','سینما','ماشین','رادیو','تاکسی','موتور','شلوار','جوراب','دستکش','چمدان','لیوان','فنجان','چنگال','بشقاب','سماور','قالین','زنجیر','کبریت','سندان','باتری','سنجاق','صابون','شامپو','لوبیا','بادام','انگور','انجیر','گیلاس','نارنج','زیتون','خربزه','طالبی','شکلات','نعناع','خرگوش','سنجاب','زرافه','میمون','دلفین','تمساح','گنجشک','کرگدن','روباه','مورچه','زنبور','گورخر','شاهین','پاییز','بهاری','خوردن','نوشتن','شنیدن','دویدن','پریدن','نشستن','شطرنج','پاسور','حافظه','خاطره','پنجره','دیوار','فریاد','سیمان','زندان'];
function norm(s){return String(s||'').replace(/ي/g,'ی').replace(/ك/g,'ک').replace(/[\s\u200c]+/g,'').trim();}
function feedback(g,a){g=norm(g);a=norm(a);var r=[],i,rem={};for(i=0;i<a.length;i++){rem[a[i]]=(rem[a[i]]||0)+1;}for(i=0;i<g.length;i++){if(g[i]===a[i]){r[i]='g';rem[g[i]]=(rem[g[i]]||0)-1;}}for(i=0;i<g.length;i++){if(r[i])continue;var c=g[i];if(rem[c]>0){r[i]='y';rem[c]--;}else{r[i]='k';}}return r;}
function isWin(fb){if(!fb||!fb.length)return false;for(var i=0;i<fb.length;i++){if(fb[i]!=='g')return false;}return true;}
function isValidGuess(s){return WORDS.indexOf(norm(s))>=0;}
function keyState(gs,a){var m={},i,j;for(i=0;i<gs.length;i++){var fb=feedback(gs[i],a);for(j=0;j<gs[i].length;j++){var c=gs[i][j],v=fb[j]==='g'?3:(fb[j]==='y'?2:1);if((m[c]||0)<v)m[c]=v;}}return m;}
function pickWord(rng){var i=rng?Math.floor(rng()*WORDS.length):Math.floor(Math.random()*WORDS.length);return WORDS[i];}
var WOG_LOGIC={FA:FA,WORDS:WORDS,norm:norm,feedback:feedback,isWin:isWin,isValidGuess:isValidGuess,keyState:keyState,pickWord:pickWord};
"""

WORDLE_UI = r"""
var app=$('#app'),N=5,TRIES=6,cells=[],kbwrap=null,share=null,ans='',rows=[],cur='',over=false;
var streak=parseInt(store.get('wog-wordle-streak')||'0',10)||0;
function hudUp(){var t=rows.length+(over?0:1);if(t>TRIES)t=TRIES;hud('برد پیاپی: '+fa(streak)+' · تلاش: '+fa(t)+' از '+fa(TRIES));}
function buildBoard(){var b=ce('div','wboard'),r,c;cells=[];for(r=0;r<TRIES;r++){var row=[];for(c=0;c<N;c++){var d=ce('div','wcell','');b.appendChild(d);row.push(d);}cells.push(row);}app.appendChild(b);}
function draw(){var r,c;for(r=0;r<TRIES;r++)for(c=0;c<N;c++){var el=cells[r][c],ch='';el.className='wcell';if(r<rows.length){ch=rows[r].g[c];el.classList.add(rows[r].fb[c]);}else if(r===rows.length&&c<cur.length){ch=cur[c];el.classList.add('pend');}el.textContent=ch;}}
function keyScope(){return (kbwrap&&kbwrap.children.length)?kbwrap:app;}
function colorKeys(){var m=L.keyState(rows.map(function(x){return x.g;}),ans),btns=keyScope().querySelectorAll('button,[data-key]'),i;for(i=0;i<btns.length;i++){var b=btns[i],t=(b.getAttribute('data-key')||b.textContent||'').trim();if(t.length===1&&m[t])b.classList.add('kb-'+m[t]);}}
function drawShare(){var h='',r,c;for(r=0;r<rows.length;r++){h+='<div class="sgrow">';for(c=0;c<N;c++)h+='<span class="sg '+rows[r].fb[c]+'"></span>';h+='</div>';}share.innerHTML=h;}
function addChar(ch){if(over)return;ch=L.norm(ch);if(ch.length!==1||L.FA.indexOf(ch)<0)return;if(cur.length>=N)return;cur+=ch;draw();}
function delChar(){if(over)return;if(!cur.length)return;cur=cur.slice(0,-1);draw();}
function submit(){if(over)return;if(cur.length<N){toast('واژه باید '+fa(N)+' حرف باشد');return;}if(!L.isValidGuess(cur)){toast('این واژه در فهرست نیست');return;}var fb=L.feedback(cur,ans);rows.push({g:cur,fb:fb});cur='';draw();colorKeys();drawShare();hudUp();if(L.isWin(fb)){over=true;streak++;store.set('wog-wordle-streak',String(streak));hudUp();ovl('آفرین! بردی','واژه: '+ans+' — تلاش '+fa(rows.length)+' از '+fa(TRIES),'بازی جدید',init);}else if(rows.length>=TRIES){over=true;streak=0;store.set('wog-wordle-streak','0');hudUp();ovl('باختی!','واژه درست: '+ans,'بازی جدید',init);}}
function init(){app.innerHTML='';ans=L.pickWord();rows=[];cur='';over=false;share=ce('div','wshare');buildBoard();app.appendChild(share);var bar=ce('div','wbar'),bd=ce('button','wbtn','پاک'),bg=ce('button','wbtn wgo','تایید'),bn=ce('button','wbtn wnew','بازی جدید');bd.onclick=delChar;bg.onclick=submit;bn.setAttribute('data-smoke','1');bn.onclick=init;bar.appendChild(bd);bar.appendChild(bg);bar.appendChild(bn);app.appendChild(bar);kbwrap=ce('div','kbwrap');app.appendChild(kbwrap);var kel=faKb(function(ch){addChar(ch);},{});if(kel&&kel.nodeType===1)kbwrap.appendChild(kel);draw();hudUp();}
document.addEventListener('keydown',function(e){if(e.key==='Enter'){submit();}else if(e.key==='Backspace'){e.preventDefault();delChar();}else{var k=L.norm(e.key||'');if(k.length===1)addChar(k);}});
init();
$('#hint').textContent='واژهٔ ۵ حرفی را در ۶ تلاش پیدا کن: سبز یعنی جای درست، طلایی یعنی حرف هست ولی جای دیگر، خاکستری یعنی نیست.';
"""

WORDLE_CSS = r"""
.wboard{display:grid;grid-template-columns:repeat(5,48px);gap:6px;justify-content:center;margin:12px auto}
.wcell{width:48px;height:48px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;background:#14203a;border:2px solid #2a3a5a;border-radius:8px;color:#eef2fb;transition:background .25s,border-color .25s}
.wcell.pend{border-color:#d9a441}
.wcell.g{background:#67b98a;border-color:#67b98a;color:#0b2a1c}
.wcell.y{background:#d9a441;border-color:#d9a441;color:#2a1c03}
.wcell.k{background:#3a4a66;border-color:#3a4a66;color:#93a5c4}
.wbar{display:flex;gap:8px;justify-content:center;margin:10px 0;flex-wrap:wrap}
.wbtn{min-width:64px;min-height:42px;padding:6px 14px;font-size:15px;font-weight:700;border:0;border-radius:8px;background:#2a3a5a;color:#eef2fb;cursor:pointer;touch-action:manipulation}
.wgo{background:#3fb8af;color:#062423}
.wnew{background:#d9a441;color:#2a1c03}
.wshare{min-height:16px;margin:6px auto;text-align:center}
.sgrow{display:flex;gap:3px;justify-content:center;margin:3px 0}
.sg{width:16px;height:16px;border-radius:3px;display:inline-block}
.sg.g{background:#67b98a}.sg.y{background:#d9a441}.sg.k{background:#3a4a66}
.kb-g{background:#67b98a!important;color:#0b2a1c!important}
.kb-y{background:#d9a441!important;color:#2a1c03!important}
.kb-k{background:#3a4a66!important;color:#7d90b5!important}
"""

HANGMAN_LOGIC = r"""
var FA='ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی';
var WORDS=[{w:'خرگوش',cat:'حیوان'},{w:'سنجاب',cat:'حیوان'},{w:'زرافه',cat:'حیوان'},{w:'میمون',cat:'حیوان'},{w:'دلفین',cat:'حیوان'},{w:'تمساح',cat:'حیوان'},{w:'گنجشک',cat:'حیوان'},{w:'کرگدن',cat:'حیوان'},{w:'روباه',cat:'حیوان'},{w:'زنبور',cat:'حیوان'},{w:'شترمرغ',cat:'حیوان'},{w:'عنکبوت',cat:'حیوان'},{w:'انگور',cat:'میوه'},{w:'انجیر',cat:'میوه'},{w:'نارنج',cat:'میوه'},{w:'زیتون',cat:'میوه'},{w:'بادام',cat:'میوه'},{w:'گیلاس',cat:'میوه'},{w:'خربزه',cat:'میوه'},{w:'طالبی',cat:'میوه'},{w:'هندوانه',cat:'میوه'},{w:'نارنگی',cat:'میوه'},{w:'تبریز',cat:'شهر'},{w:'شیراز',cat:'شهر'},{w:'اصفهان',cat:'شهر'},{w:'کاشان',cat:'شهر'},{w:'سمنان',cat:'شهر'},{w:'قزوین',cat:'شهر'},{w:'همدان',cat:'شهر'},{w:'کرمان',cat:'شهر'},{w:'سنندج',cat:'شهر'},{w:'بوشهر',cat:'شهر'},{w:'زاهدان',cat:'شهر'},{w:'ماشین',cat:'شیء'},{w:'رادیو',cat:'شیء'},{w:'لیوان',cat:'شیء'},{w:'فنجان',cat:'شیء'},{w:'چمدان',cat:'شیء'},{w:'جوراب',cat:'شیء'},{w:'شلوار',cat:'شیء'},{w:'دستکش',cat:'شیء'},{w:'چنگال',cat:'شیء'},{w:'بشقاب',cat:'شیء'},{w:'سماور',cat:'شیء'}];
var MAXL=6;
function norm(s){return String(s||'').replace(/ي/g,'ی').replace(/ك/g,'ک').replace(/[\s\u200c]+/g,'');}
function reveal(w,g){var o='',i;for(i=0;i<w.length;i++){o+=(g.indexOf(w[i])>=0?w[i]:'_');}return o;}
function livesAfter(l,hit){return hit?l:l-1;}
function isWin(w,g){if(!w||!w.length)return false;for(var i=0;i<w.length;i++){if(g.indexOf(w[i])<0)return false;}return true;}
function isDead(l){return l<=0;}
function guess(g,ch){return g.indexOf(ch)>=0?g:g+ch;}
function hitIn(w,ch){return w.indexOf(ch)>=0;}
function pickWord(rng){var i=rng?Math.floor(rng()*WORDS.length):Math.floor(Math.random()*WORDS.length);return WORDS[i];}
var WOG_LOGIC={FA:FA,WORDS:WORDS,MAXL:MAXL,norm:norm,reveal:reveal,livesAfter:livesAfter,isWin:isWin,isDead:isDead,guess:guess,hitIn:hitIn,pickWord:pickWord};
"""

HANGMAN_UI = r"""
var app=$('#app'),MAXL=6,w='',cat='',guessed='',lives=6,over=false,kbwrap=null;
var wins=parseInt(store.get('wog-hangman-wins')||'0',10)||0;
function hudUp(){hud('تلاش: '+fa(guessed.length)+' · جان: '+fa(lives)+' · رکورد برد: '+fa(wins));}
function buildStage(){var s=ce('div','hmstage'),order=['hm-base','hm-pole','hm-beam','hm-rope','hm-head','hm-body','hm-arm-l','hm-arm-r','hm-leg-l','hm-leg-r'],i;for(i=0;i<order.length;i++)s.appendChild(ce('div','hm '+order[i]));app.appendChild(s);}
function drawParts(){var wrong=MAXL-lives,parts=app.querySelectorAll('.hm'),i;for(i=0;i<parts.length;i++){if(i>=4)parts[i].classList.toggle('on',wrong>=(i-3));}}
function drawWord(){var show=(over&&L.isDead(lives)),h='',i;for(i=0;i<w.length;i++){var got=guessed.indexOf(w[i])>=0;if(got)h+='<span class="hl">'+w[i]+'</span>';else h+='<span class="hl hid'+(show?' lost':'')+'">'+(show?w[i]:'\u00a0')+'</span>';}$('#hwordbox').innerHTML=h;drawParts();}
function keyScope(){return (kbwrap&&kbwrap.children.length)?kbwrap:app;}
function paintKey(ch,cls){var btns=keyScope().querySelectorAll('button,[data-key]'),i;for(i=0;i<btns.length;i++){var b=btns[i],t=(b.getAttribute('data-key')||b.textContent||'').trim();if(t===ch){b.classList.add(cls);b.classList.add('kb-off');}}}
function onKey(ch){if(over)return;ch=L.norm(String(ch));if(ch.length!==1||L.FA.indexOf(ch)<0)return;if(guessed.indexOf(ch)>=0){toast('این حرف را گفته‌ای');return;}var hit=L.hitIn(w,ch);guessed=L.guess(guessed,ch);lives=L.livesAfter(lives,hit);paintKey(ch,hit?'kb-hit':'kb-miss');drawWord();hudUp();if(L.isWin(w,guessed)){over=true;wins++;store.set('wog-hangman-wins',String(wins));hudUp();ovl('بردی!','واژه: '+w+' — جان باقی‌مانده: '+fa(lives),'بازی جدید',init);}else if(L.isDead(lives)){over=true;drawWord();hudUp();ovl('مرد حلق‌آویز شد!','واژه: '+w+' — دسته: '+cat,'بازی جدید',init);}}
function init(){app.innerHTML='';var e=L.pickWord();w=e.w;cat=e.cat;guessed='';lives=MAXL;over=false;var top=ce('div','hmtop'),chip=ce('span','chip','دسته: '+cat);top.appendChild(chip);app.appendChild(top);buildStage();var wrd=ce('div','hword');wrd.id='hwordbox';app.appendChild(wrd);var bar=ce('div','wbar'),bn=ce('button','wbtn wnew','بازی جدید');bn.setAttribute('data-smoke','1');bn.onclick=init;bar.appendChild(bn);app.appendChild(bar);kbwrap=ce('div','kbwrap');app.appendChild(kbwrap);var kel=faKb(function(ch){onKey(ch);},{});if(kel&&kel.nodeType===1)kbwrap.appendChild(kel);drawWord();hudUp();}
document.addEventListener('keydown',function(e){var k=L.norm(e.key||'');if(k.length===1)onKey(k);});
init();
$('#hint').textContent='دسته را ببین و حرف حدس بزن؛ هر پاسخ اشتباه یک اندام به مرد اضافه می‌کند — ۶ جان داری.';
"""

HANGMAN_CSS = r"""
.hmtop{display:flex;justify-content:center;margin:6px 0}
.chip{background:#1c2b4a;border:1px solid #3fb8af;color:#bfe9e6;border-radius:999px;padding:6px 16px;font-size:14px;font-weight:700}
.hmstage{position:relative;width:180px;height:190px;margin:8px auto;background:#14203a;border-radius:12px;border:1px solid #223354}
.hm{position:absolute;background:#8a94ad}
.hm-base{bottom:12px;left:20px;width:130px;height:6px}
.hm-pole{bottom:18px;left:46px;width:6px;height:154px}
.hm-beam{top:18px;left:46px;width:88px;height:6px}
.hm-rope{top:18px;left:128px;width:6px;height:22px;background:#d9a441}
.hm-head{top:38px;left:115px;width:32px;height:32px;border-radius:50%;background:transparent;border:5px solid #e26d5c;opacity:0}
.hm-body{top:75px;left:128px;width:6px;height:42px;opacity:0}
.hm-arm-l{top:82px;left:108px;width:6px;height:30px;transform:rotate(28deg);opacity:0}
.hm-arm-r{top:82px;left:148px;width:6px;height:30px;transform:rotate(-28deg);opacity:0}
.hm-leg-l{top:117px;left:112px;width:6px;height:32px;transform:rotate(20deg);opacity:0}
.hm-leg-r{top:117px;left:144px;width:6px;height:32px;transform:rotate(-20deg);opacity:0}
.hm.on{opacity:1}
.hword{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:12px auto;max-width:420px}
.hl{min-width:36px;height:46px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;background:#14203a;border:2px solid #2a3a5a;border-radius:8px;color:#eef2fb;padding:0 6px}
.hl.hid{color:transparent}
.hl.lost{border-color:#e26d5c;color:#e26d5c}
.wbar{display:flex;gap:8px;justify-content:center;margin:10px 0;flex-wrap:wrap}
.wbtn{min-width:64px;min-height:42px;padding:6px 14px;font-size:15px;font-weight:700;border:0;border-radius:8px;background:#2a3a5a;color:#eef2fb;cursor:pointer;touch-action:manipulation}
.wnew{background:#d9a441;color:#2a1c03}
.kb-hit{background:#67b98a!important;color:#0b2a1c!important}
.kb-miss{background:#52303a!important;color:#d8a3ad!important}
.kb-off{opacity:.85}
"""

GAMES=[
    G(slug='wordle', title='واژه‌یاب', cat='word', icon='▦', g1='#3fb8af', g2='#8a5f1e',
      desc='واژهٔ پنج‌حرفی فارسی را در شش تلاش حدس بزن؛ رنگ هر خانه پس از هر حدس راهنمای توست.',
      hint='سبز یعنی حرف سر جایش است، طلایی یعنی حرف در واژه هست ولی جای دیگر، خاکستری یعنی نیست.',
      logic=WORDLE_LOGIC, ui=WORDLE_UI, css=WORDLE_CSS, engines=('common','word'),
      tests=[
        ('بازخورد سبز و خاکستری',
         "T.eq(L.feedback('ستاره','ستاره'),['g','g','g','g','g']);T.ok(L.isWin(L.feedback('ستاره','ستاره')));T.eq(L.feedback('ظظظظظ','باران'),['k','k','k','k','k']);T.ok(!L.isWin(L.feedback('ظظظظظ','باران')));T.ok(!L.isWin([]));"),
        ('الگوریتم دومرحله‌ای و حروف تکراری',
         "T.eq(L.feedback('ناران','باران'),['k','g','g','g','g']);T.eq(L.feedback('رابان','باران'),['y','g','y','g','g']);T.eq(L.feedback('سسسسس','سسردس'),['g','g','k','k','g']);T.eq(L.feedback('ردسسس','سسردس'),['y','y','y','y','g']);T.eq(L.feedback('سسردس','سسردس'),['g','g','g','g','g']);"),
        ('فهرست واژه‌ها معتبر است',
         "var W=L.WORDS,FA=L.FA,bad='',seen={},i,j;for(i=0;i<W.length;i++){var s=W[i];if(s.length!==5)bad+='len:'+s+';';for(j=0;j<s.length;j++)if(FA.indexOf(s[j])<0)bad+='fa:'+s+';';if(L.norm(s)!==s)bad+='norm:'+s+';';if(seen[s])bad+='dup:'+s+';';seen[s]=1;}T.eq(bad,'');T.ok(W.length>=110,'count='+W.length);T.ok(L.isValidGuess(W[0]));T.ok(L.isValidGuess(' برادر '));T.ok(!L.isValidGuess('ثثثثث'));T.ok(!L.isValidGuess('برادرا'));"),
        ('جریان شش تلاش',
         "var ans=L.pickWord(rng),wrongs=[],i;for(i=0;i<L.WORDS.length&&wrongs.length<6;i++)if(L.WORDS[i]!==ans)wrongs.push(L.WORDS[i]);T.eq(wrongs.length,6);var fbs=[],early=false;for(i=0;i<6;i++){var f=L.feedback(wrongs[i],ans);fbs.push(f);if(L.isWin(f))early=true;}T.ok(!early);T.ok(fbs.every(function(f){return f.length===5;}));T.ok(L.isWin(L.feedback(ans,ans)));T.ok(!L.isWin(fbs[0]));"),
        ('رنگ کلیدهای صفحه‌کلید',
         "var m=L.keyState(['باران'],'برادر');T.eq(m['ب'],3);T.eq(m['ا'],2);T.eq(m['ر'],2);T.eq(m['ن'],1);T.ok(m['د']===undefined);var m2=L.keyState(['باران','ددددد','ظظظدظ'],'برادر');T.eq(m2['د'],3);T.eq(m2['ظ'],1);T.eq(m2['ا'],2);T.eq(m2['ب'],3);"),
      ]),
    G(slug='hangman', title='مرد حلق‌آویز', cat='word', icon='☉', g1='#e26d5c', g2='#7a3b30',
      desc='واژهٔ پنهان را با حدس حرف‌ها پیدا کن؛ هر پاسخ اشتباه یک اندام به مرد اضافه می‌کند.',
      hint='اول حرف‌های پرتکرار مثل «ا»، «ر» و «ن» را امتحان کن و به دستهٔ واژه دقت کن.',
      logic=HANGMAN_LOGIC, ui=HANGMAN_UI, css=HANGMAN_CSS, engines=('common','word'),
      tests=[
        ('ماسک و آشکارسازی واژه',
         "T.eq(L.reveal('خرگوش',''),'_____');T.eq(L.reveal('خرگوش','خش'),'خ___ش');T.eq(L.reveal('خرگوش','خرگوش'),'خرگوش');T.eq(L.reveal('دلفین','لف'),'_لف__');"),
        ('حدس تکراری جریمه ندارد',
         "T.eq(L.guess('س','س'),'س');T.eq(L.guess('','س'),'س');var l2=6;l2=L.livesAfter(l2,L.hitIn('دلفین','ظ'));T.eq(l2,5,'first wrong');var g2=L.guess('ظ','ظ');T.eq(g2,'ظ');var l3=5;if(L.guess('ظ','ظ')!=='ظ')l3=L.livesAfter(l3,L.hitIn('دلفین','ظ'));T.eq(l3,5,'no double penalty');T.eq(L.livesAfter(5,true),5,'hit no loss');T.eq(L.livesAfter(1,false),0,'miss at 1');"),
        ('جریان شش جان',
         "var w='دلفین',g='',l=6,wr=['ب','ت','س','ک','م','ر'],i;for(i=0;i<wr.length;i++){g=L.guess(g,wr[i]);l=L.livesAfter(l,L.hitIn(w,wr[i]));}T.eq(l,0);T.ok(L.isDead(l));T.ok(!L.isWin(w,g));g='';l=6;var ls=['د','ل','ف','ی','ن'],hits=0;for(i=0;i<ls.length;i++){g=L.guess(g,ls[i]);var h=L.hitIn(w,ls[i]);l=L.livesAfter(l,h);if(h)hits++;}T.eq(hits,5);T.eq(l,6);T.ok(L.isWin(w,g));T.ok(!L.isDead(l));"),
        ('ساختار فهرست و دسته‌ها',
         "var W=L.WORDS,FA=L.FA,bad='',cats={},seen={},i,j;for(i=0;i<W.length;i++){var e=W[i];if(!e.w||!e.w.length)bad+='empty;';if(!e.cat)bad+='nocat;';cats[e.cat]=(cats[e.cat]||0)+1;var u={},un=0;for(j=0;j<e.w.length;j++){var c=e.w[j];if(FA.indexOf(c)<0)bad+='fa:'+e.w+';';if(!u[c]){u[c]=1;un++;}}if(un<1)bad+='nounique:'+e.w+';';if(seen[e.w])bad+='dup:'+e.w+';';seen[e.w]=1;}T.eq(bad,'');T.ok(W.length>=38,'count='+W.length);T.ok(cats['حیوان']>=8&&cats['میوه']>=8&&cats['شهر']>=8&&cats['شیء']>=8,'cats');"),
        ('تشخیص برد و باخت',
         "T.ok(L.isWin('شیراز','شیراز'));T.ok(L.isWin('شیراز','اشیروزی'));T.ok(!L.isWin('شیراز','شی'));T.ok(!L.isWin('','شیراز'));T.ok(L.isDead(0));T.ok(L.isDead(-2));T.ok(!L.isDead(1));T.ok(!L.isDead(6));"),
        ('شبیه‌سازی بذردار بازی کامل',
         "var letters=L.FA.split(''),bad='',n=30,i;for(i=0;i<n;i++){var e=L.pickWord(rng),w=e.w,g='',l=L.MAXL,k;for(k=letters.length-1;k>0;k--){var j2=Math.floor(rng()*(k+1)),tmp=letters[k];letters[k]=letters[j2];letters[j2]=tmp;}for(k=0;k<letters.length;k++){if(L.isWin(w,g)||L.isDead(l))break;var ch=letters[k];g=L.guess(g,ch);l=L.livesAfter(l,L.hitIn(w,ch));}if(l<0||l>6)bad+='lives;';if(!L.isWin(w,g)&&!L.isDead(l))bad+='stuck;';if(L.isWin(w,g)&&L.isDead(l))bad+='both;';}T.eq(bad,'');"),
      ]),
]
