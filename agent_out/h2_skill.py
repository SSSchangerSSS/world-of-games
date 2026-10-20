# -*- coding: utf-8 -*-
"""AG-H2 batch: 4 skill games (stroop, math-sprint, typing, cups) - cat=arcade, engines=("common",)."""
from lib_mini import G

BASE_CSS = """
body{touch-action:manipulation}
#app{max-width:520px;margin:0 auto;padding:8px}
.panel{background:#14203a;border:1px solid #2a3b5f;border-radius:14px;padding:16px;text-align:center}
.panel h2{margin:4px 0 8px;color:#d9a441}
.dim{color:#9fb0cc;font-size:14px;line-height:1.9}
.row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:12px}
.big{min-width:64px;min-height:52px;font-size:19px;border-radius:12px;border:1px solid #2a3b5f;background:#1b2b4d;color:#eef2f8;padding:10px 16px;touch-action:manipulation;cursor:pointer}
.gold{background:#d9a441;color:#1c1508;font-weight:800;border-color:#b3832f}
.ghost{background:#14203a}
"""

# ============================== stroop ==============================
STROOP_LOGIC = r"""
var WOG_LOGIC={
COLORS:[{fa:"قرمز",hex:"#e0554d"},{fa:"آبی",hex:"#4a7fd6"},{fa:"سبز",hex:"#4fae7a"},{fa:"زرد",hex:"#d9a441"}],
newState:function(){return{score:0,streak:0,hits:0,miss:0,t:45,over:false};},
genTrial:function(rng){rng=rng||Math.random;var n=this.COLORS.length;var word=Math.floor(rng()*n);var ink;var cong=rng()<0.4;if(cong){ink=word;}else{do{ink=Math.floor(rng()*n);}while(ink===word);}return{word:word,ink:ink,ic:ink!==word};},
judge:function(trial,answer){return answer===trial.ink;},
applyAnswer:function(s,ok){if(ok){s.streak++;s.hits++;s.score+=s.streak;}else{s.streak=0;s.miss++;}return s;},
tick:function(s,dt){s.t=Math.max(0,s.t-dt);if(s.t<=0){s.over=true;}return s.over;}
};
"""
STROOP_UI = r"""
var app=$('#app'),s=L.newState(),cur=null,timer=null,lock=false;
function hudUp(){hud('امتیاز <b>'+fa(s.score)+'</b> | زمان <b>'+fa(Math.ceil(s.t))+'</b> | پیاپی <b>'+fa(s.streak)+'</b>');}
function stop(){if(timer){clearInterval(timer);timer=null;}}
function bar(){var r=ce('div','row');var b=ce('button','big ghost');b.textContent='بازی جدید';b.setAttribute('data-smoke','1');b.onclick=start;r.appendChild(b);return r;}
function start(){stop();s=L.newState();lock=false;$('#hint').textContent='رنگِ جوهر کلمه را بزن، نه معنی کلمه را!';hudUp();next();timer=setInterval(function(){L.tick(s,0.1);hudUp();if(s.over)end();},100);}
function end(){stop();var k='wog-stroop-best',b=parseInt(store.get(k)||'0',10),nb=s.score>b;if(nb)store.set(k,''+s.score);ovl('پایان استروپ','امتیاز: '+fa(s.score)+' | درست: '+fa(s.hits)+(nb?' (رکورد جدید!)':''),'دوباره',start);}
function next(){if(s.over)return;lock=false;cur=L.genTrial(Math.random);var ink=L.COLORS[cur.ink];app.innerHTML='';var p=ce('div','panel word');p.style.color=ink.hex;p.style.borderColor=ink.hex;p.textContent=L.COLORS[cur.word].fa;app.appendChild(p);var row=ce('div','row');L.COLORS.forEach(function(c,i){var b=ce('button','big cbtn');b.style.background=c.hex;b.textContent=c.fa;b.setAttribute('data-smoke','1');b.onclick=function(){pick(i);};row.appendChild(b);});app.appendChild(row);app.appendChild(bar());}
function pick(i){if(lock||s.over)return;lock=true;var ok=L.judge(cur,i);L.applyAnswer(s,ok);if(!ok)toast('رنگِ جوهر را بزن!');hudUp();if(s.over){end();return;}setTimeout(next,ok?150:450);}
$('#hint').textContent='۴۵ ثانیه فرصت داری؛ هرچه سریع‌تر بهتر!';
hudUp();app.innerHTML='';
var hp=ce('div','panel');hp.innerHTML='<h2>تست استروپ</h2><p class="dim">کلمه‌ای رنگی می‌بینی؛ دکمه‌ای را بزن که رنگِ «جوهرِ» کلمه است، نه معنی آن. پاسخ درست، امتیازِ پیاپی بیشتری می‌دهد.</p>';
var sb=ce('button','big gold');sb.textContent='شروع';sb.setAttribute('data-smoke','1');sb.onclick=start;hp.appendChild(sb);app.appendChild(hp);app.appendChild(bar());
"""
STROOP_CSS = BASE_CSS + """
.word{font-size:46px;font-weight:800;min-height:88px;line-height:88px}
.cbtn{min-width:74px;color:#10131a;font-weight:800;border:none}
"""

# ============================== math-sprint ==============================
MATH_LOGIC = r"""
var WOG_LOGIC={
newState:function(){return{score:0,streak:0,hits:0,miss:0,t:60,over:false};},
ramp:function(t){return 1+Math.min(3,Math.floor(Math.max(0,t)/15));},
distractors:function(ans,rng){rng=rng||Math.random;var used={},out=[],g=0,d,v;used[ans]=1;while(out.length<3&&g++<300){d=1+Math.floor(rng()*Math.max(3,Math.round(Math.abs(ans)*0.2)+2));if(rng()<0.5)d=-d;v=ans+d;if(v<0)v=ans-d;if(v<0||used[v])continue;used[v]=1;out.push(v);}var w=1;while(out.length<3){if(!used[ans+w]){used[ans+w]=1;out.push(ans+w);}w++;}return out;},
genProblem:function(level,rng){rng=rng||Math.random;var lv=level<1?1:level,k=Math.floor(rng()*4),a,b,ans,text;
if(k===0){a=1+Math.floor(rng()*(10+5*lv));b=1+Math.floor(rng()*(10+5*lv));ans=a+b;text=a+' + '+b;}
else if(k===1){a=5+Math.floor(rng()*(16+6*lv));b=1+Math.floor(rng()*a);ans=a-b;text=a+' - '+b;}
else if(k===2){a=2+Math.floor(rng()*(1+lv));b=2+Math.floor(rng()*(8+lv));ans=a*b;text=a+' × '+b;}
else{b=2+Math.floor(rng()*(2+lv));ans=2+Math.floor(rng()*(3+2*lv));a=b*ans;text=a+' ÷ '+b;}
var ch=this.distractors(ans,rng);ch.push(ans);var i,j,t;for(i=ch.length-1;i>0;i--){j=Math.floor(rng()*(i+1));t=ch[i];ch[i]=ch[j];ch[j]=t;}
return{kind:k,a:a,b:b,text:text,answer:ans,choices:ch};},
answer:function(s,p,i){var ok=p.choices[i]===p.answer;if(ok){s.streak++;s.hits++;s.score+=10+s.streak*2;}else{s.streak=0;s.miss++;s.t=Math.max(0,s.t-2);}if(s.t<=0)s.over=true;return ok;},
tick:function(s,dt){s.t=Math.max(0,s.t-dt);if(s.t<=0){s.over=true;}return s.over;}
};
"""
MATH_UI = r"""
var app=$('#app'),s=L.newState(),p=null,timer=null;
function hudUp(){hud('امتیاز <b>'+fa(s.score)+'</b> | زمان <b>'+fa(Math.ceil(s.t))+'</b> | سطح <b>'+fa(L.ramp(60-s.t))+'</b>');}
function stop(){if(timer){clearInterval(timer);timer=null;}}
function bar(){var r=ce('div','row');var b=ce('button','big ghost');b.textContent='بازی جدید';b.setAttribute('data-smoke','1');b.onclick=start;r.appendChild(b);return r;}
function start(){stop();s=L.newState();$('#hint').textContent='سریع جواب بده؛ اشتباه ۲ ثانیه کم می‌کند!';hudUp();next();timer=setInterval(function(){L.tick(s,0.1);hudUp();if(s.over)end();},100);}
function end(){stop();var k='wog-math-sprint-best',b=parseInt(store.get(k)||'0',10),nb=s.score>b;if(nb)store.set(k,''+s.score);ovl('پایان ریاضی','امتیاز: '+fa(s.score)+' | درست: '+fa(s.hits)+(nb?' (رکورد جدید!)':''),'دوباره',start);}
function next(){if(s.over)return;p=L.genProblem(L.ramp(60-s.t),Math.random);app.innerHTML='';var pn=ce('div','panel mtext');pn.textContent=p.text+' = ?';app.appendChild(pn);var row=ce('div','row');p.choices.forEach(function(v,i){var b=ce('button','big gold2');b.textContent=fa(v);b.setAttribute('data-smoke','1');b.onclick=function(){pick(i);};row.appendChild(b);});app.appendChild(row);app.appendChild(bar());}
function pick(i){if(s.over)return;var ok=L.answer(s,p,i);if(ok)toast('درست! +'+fa(10+s.streak*2));else toast('اشتباه! ۲ ثانیه کم شد');hudUp();if(s.over){end();return;}next();}
$('#hint').textContent='۶۰ ثانیه محاسبهٔ برق‌آسا!';
hudUp();app.innerHTML='';
var hp=ce('div','panel');hp.innerHTML='<h2>ریاضی برق‌آسا</h2><p class="dim">جمع، تفریق، ضرب و تقسیمِ دقیق؛ هر ۱۵ ثانیه سؤال‌ها سخت‌تر می‌شوند و هر اشتباه ۲ ثانیه از وقتت کم می‌کند.</p>';
var sb=ce('button','big gold');sb.textContent='شروع';sb.setAttribute('data-smoke','1');sb.onclick=start;hp.appendChild(sb);app.appendChild(hp);app.appendChild(bar());
"""
MATH_CSS = BASE_CSS + """
.mtext{font-size:42px;font-weight:800;color:#eef2f8;direction:ltr}
.gold2{background:#3fb8af;color:#062220;font-weight:800;border-color:#2f8f88;min-width:72px}
"""

# ============================== typing ==============================
TYPE_LOGIC = r"""
var WOG_LOGIC={
SENTENCES:["سلام بر همه دوستان خوب","امروز هوا آفتابی و زیباست","آسمان شب پر از ستاره است","من کتاب داستان دوست دارم","کودکان در حیاط بازی کردند","چای داغ در روز سرد لذت دارد","پرندگان بر شاخه ها نشسته اند","دریای خزر زیبا و بزرگ است","تو مهربان و کوشا هستی","خورشید از پشت کوه بالا آمد","یادگیری زبان فارسی آسان است","به سلامتی و شادی دوستان"],
wpm:function(chars,ms){if(!ms||ms<=0)return 0;return Math.round((chars/5)*(60000/ms));},
diff:function(typed,target){var n=Math.max(typed.length,target.length),out=[],i;for(i=0;i<n;i++)out.push(typed.charAt(i)===target.charAt(i));return out;},
accuracy:function(typed,target){if(!typed||!typed.length)return 1;var f=this.diff(typed,target),c=0,i;for(i=0;i<typed.length;i++)if(f[i])c++;return c/typed.length;},
nextSentence:function(i){var n=this.SENTENCES.length;return this.SENTENCES[((i+1)%n+n)%n];}
};
"""
TYPE_UI = r"""
var app=$('#app'),s=null,timer=null,idx=-1,sent='',typed='',hl=0,inp=null;
function stop(){if(timer){clearInterval(timer);timer=null;}}
function elapsed(){return s?(60-s.t)*1000:0;}
function hudUp(){if(!s){hud('');return;}var w=L.wpm(s.chars,elapsed()),a=s.typedAll?s.correctAll/s.typedAll:1;hud('زمان <b>'+fa(Math.ceil(s.t))+'</b> | سرعت <b>'+fa(w)+'</b> | دقت <b>'+fa(Math.round(a*100))+'٪</b>');}
function bar(){var r=ce('div','row');var b=ce('button','big ghost');b.textContent='بازی جدید';b.setAttribute('data-smoke','1');b.onclick=start;r.appendChild(b);var f=ce('button','big ghost');f.textContent='پایان';f.onclick=finish;r.appendChild(f);return r;}
function start(){stop();s={t:60,chars:0,typedAll:0,correctAll:0,over:false};idx=-1;$('#hint').textContent='جمله را دقیق تایپ کن؛ سبز یعنی درست.';nextSent();timer=setInterval(function(){if(!s||s.over)return;s.t=Math.max(0,s.t-0.1);hudUp();if(s.t<=0)finish();},100);}
function nextSent(){sent=L.nextSentence(idx);idx=(idx+1)%L.SENTENCES.length;typed='';hl=0;render();}
function render(){app.innerHTML='';var pn=ce('div','panel tbox');for(var i=0;i<sent.length;i++){var sp=ce('span','ch todo');sp.textContent=sent[i];pn.appendChild(sp);}app.appendChild(pn);inp=ce('input','tinp');inp.setAttribute('type','text');inp.setAttribute('dir','rtl');inp.setAttribute('autocomplete','off');inp.setAttribute('spellcheck','false');inp.setAttribute('placeholder','اینجا تایپ کن...');inp.setAttribute('data-smoke','1');inp.oninput=onType;app.appendChild(inp);app.appendChild(bar());setTimeout(function(){try{inp.focus();}catch(e){}},50);}
function onType(){if(!s||s.over)return;typed=inp.value;if(typed.length>hl){for(var k=hl;k<typed.length;k++){s.typedAll++;if(typed.charAt(k)===sent.charAt(k))s.correctAll++;}}hl=typed.length;paint();hudUp();if(typed===sent){s.chars+=sent.length;toast('درست! جملهٔ بعدی');nextSent();}}
function paint(){var spans=app.querySelectorAll('.ch'),fl=L.diff(typed,sent);for(var i=0;i<spans.length;i++){spans[i].className='ch '+((i<typed.length)?(fl[i]?'ok':'bad'):'todo');}}
function finish(){if(!s||s.over)return;s.over=true;stop();var w=L.wpm(s.chars,Math.max(1,elapsed())),a=s.typedAll?Math.round(100*s.correctAll/s.typedAll):100;var k='wog-typing-best',b=parseInt(store.get(k)||'0',10),nb=w>b;if(nb)store.set(k,''+w);ovl('پایان تایپ','سرعت: '+fa(w)+' کلمه در دقیقه | دقت: '+fa(a)+'٪'+(nb?' (رکورد جدید!)':''),'دوباره',start);}
$('#hint').textContent='۶۰ ثانیه تایپ سریع و دقیق!';
hudUp();app.innerHTML='';
var hp=ce('div','panel');hp.innerHTML='<h2>سرعت تایپ</h2><p class="dim">جمله‌های فارسی را تایپ کن؛ حروف درست سبز و غلط قرمز می‌شوند. سرعت (کلمه در دقیقه) و دقتت زنده نمایش داده می‌شود.</p>';
var sb=ce('button','big gold');sb.textContent='شروع';sb.setAttribute('data-smoke','1');sb.onclick=start;hp.appendChild(sb);app.appendChild(hp);app.appendChild(bar());
"""
TYPE_CSS = BASE_CSS + """
.tbox{font-size:22px;line-height:2.3;word-spacing:2px}
.ch{padding:0 1px;border-radius:4px}
.todo{color:#8ea3c4}
.ok{color:#67b98a}
.bad{color:#e26d5c;background:rgba(226,109,92,.12)}
.tinp{width:96%;min-height:56px;font-size:20px;margin-top:12px;background:#0f1a30;border:1px solid #2a3b5f;border-radius:12px;color:#eef2f8;padding:12px;text-align:right;touch-action:manipulation}
"""

# ============================== cups ==============================
CUPS_LOGIC = r"""
var WOG_LOGIC={
newState:function(){return{level:1,lives:3,score:0,over:false};},
place:function(rng){return Math.floor((rng||Math.random)()*3);},
levelSwaps:function(level){return 3+(level<1?1:level);},
swapSeq:function(state,n,rng){rng=rng||Math.random;var out=[],prev=-1,i,a,b;for(i=0;i<n;i++){do{a=Math.floor(rng()*3);b=Math.floor(rng()*3);}while(a===b||(a*3+b)===prev);out.push([a,b]);prev=a*3+b;}return out;},
track:function(idx,swaps){var i,s;for(i=0;i<swaps.length;i++){s=swaps[i];if(idx===s[0])idx=s[1];else if(idx===s[1])idx=s[0];}return idx;},
applyResult:function(state,ok){if(ok){state.score+=10*state.level;state.level++;}else{state.lives--;}state.over=state.lives<=0;return state;}
};
"""
CUPS_UI = r"""
var app=$('#app'),s=null,busy=true,ballCup=0,seq=[],step=0,slotOf=[0,1,2],t1=null;
function stopT(){if(t1){clearTimeout(t1);t1=null;}}
function hudUp(){if(!s){hud('');return;}hud('امتیاز <b>'+fa(s.score)+'</b> | جان <b>'+fa(s.lives)+'</b> | مرحله <b>'+fa(s.level)+'</b>');}
function bar(){var r=ce('div','row');var b=ce('button','big ghost');b.textContent='بازی جدید';b.setAttribute('data-smoke','1');b.onclick=start;r.appendChild(b);return r;}
function start(){stopT();s=L.newState();busy=true;$('#hint').textContent='چشم روی توپ بگذار و جابه‌جایی‌ها را دنبال کن.';hudUp();round();}
function board(){app.innerHTML='';var st=ce('div','panel stage');for(var i=0;i<3;i++){var w=ce('div','cupw');var c=ce('button','cupb');c.setAttribute('data-i',''+i);c.onclick=function(){guess(parseInt(this.getAttribute('data-i'),10));};var bl=ce('span','ball');w.appendChild(c);w.appendChild(bl);st.appendChild(w);}app.appendChild(st);app.appendChild(bar());placeAll();}
function placeAll(){var ws=app.querySelectorAll('.cupw');for(var i=0;i<3;i++)ws[i].style.transform='translateX('+((slotOf[i]-1)*96)+'px)';}
function round(){slotOf=[0,1,2];ballCup=L.place(Math.random);busy=true;board();var ws=app.querySelectorAll('.cupw');ws[ballCup].className='cupw lift';t1=setTimeout(function(){var w2=app.querySelectorAll('.cupw');w2[ballCup].className='cupw';t1=setTimeout(shuffle,500);},900);}
function shuffle(){seq=L.swapSeq(s,L.levelSwaps(s.level),Math.random);step=0;var sp=Math.max(260,760-70*s.level);(function stp(){if(step>=seq.length){busy=false;toast('توپ کجاست؟ یک کاسه را بزن!');return;}var sw=seq[step++];var tmp=slotOf[sw[0]];slotOf[sw[0]]=slotOf[sw[1]];slotOf[sw[1]]=tmp;placeAll();t1=setTimeout(stp,sp);})();}
function guess(c){if(busy||!s||s.over)return;busy=true;var ws=app.querySelectorAll('.cupw'),ok=(c===ballCup);ws[ballCup].className=ok?'cupw lift good':'cupw lift';if(!ok)ws[c].className='cupw bad';L.applyResult(s,ok);hudUp();if(ok)toast('درست! +'+fa(10*(s.level-1)));else toast('اشتباه! توپ آنجا نبود');t1=setTimeout(function(){if(s.over)end();else round();},1100);}
function end(){stopT();var k='wog-cups-best',b=parseInt(store.get(k)||'0',10),nb=s.score>b;if(nb)store.set(k,''+s.score);ovl('بازی تمام شد','امتیاز: '+fa(s.score)+' | تا مرحله: '+fa(s.level)+(nb?' (رکورد جدید!)':''),'دوباره',start);}
$('#hint').textContent='توپ زیر کدام کاسه است؟';
hudUp();app.innerHTML='';
var hp=ce('div','panel');hp.innerHTML='<h2>سه‌کاسه</h2><p class="dim">توپ زیر یکی از سه کاسه نشان داده می‌شود؛ سپس کاسه‌ها جابه‌جا می‌شوند. در هر مرحله جابه‌جایی‌ها بیشتر و سریع‌تر می‌شوند. سه جان داری!</p>';
var sb=ce('button','big gold');sb.textContent='شروع';sb.setAttribute('data-smoke','1');sb.onclick=start;hp.appendChild(sb);app.appendChild(hp);app.appendChild(bar());
"""
CUPS_CSS = BASE_CSS + """
.stage{position:relative;height:175px;overflow:hidden;background:#101a30;border-radius:12px}
.cupw{position:absolute;left:50%;width:76px;margin-left:-38px;top:18px;transition:transform .18s ease}
.cupb{width:76px;height:108px;border-radius:12px 12px 16px 16px;background:#3fb8af;border:1px solid #2f8f88;box-shadow:inset 0 -14px 0 #2f8f88;touch-action:manipulation;cursor:pointer}
.ball{position:absolute;left:50%;margin-left:-12px;top:112px;width:24px;height:24px;border-radius:50%;background:#d9a441;display:none}
.cupw.lift .ball{display:block}
.cupw.bad .cupb{background:#e26d5c;border-color:#b34e40;box-shadow:inset 0 -14px 0 #b34e40}
.cupw.good .cupb{background:#67b98a;border-color:#4e9670;box-shadow:inset 0 -14px 0 #4e9670}
"""

GAMES = [
    G("stroop", "تست استروپ", "arcade", "🎨", "#e0554d", "#4a7fd6",
      "کلمهٔ رنگی می‌بینی و باید رنگِ جوهر را انتخاب کنی، نه معنی کلمه را. ۴۵ ثانیه فرصت داری!",
      "رنگِ جوهر کلمه را بزن، نه خودِ کلمه را!",
      logic=STROOP_LOGIC, ui=STROOP_UI, css=STROOP_CSS, engines=("common",),
      tests=[
        ("داوری رنگ جوهر", "T.ok(L.judge({word:0,ink:2},2));T.ok(!L.judge({word:0,ink:2},0));T.ok(!L.judge({word:3,ink:1},2));T.ok(L.judge({word:1,ink:1},1));"),
        ("نسبت ناهمناخت در ۲۰۰ آزمون", "var c=0,i,t;for(i=0;i<200;i++){t=L.genTrial(rng);T.ok(t.word>=0&&t.word<4&&t.ink>=0&&t.ink<4);if(t.ic)c++;}T.ok(c>=100&&c<=140,'ratio='+c);T.near(c/200,0.6,0.1);"),
        ("امتیاز پیاپی و ریست", "var s=L.newState();L.applyAnswer(s,true);L.applyAnswer(s,true);L.applyAnswer(s,true);T.eq([s.score,s.streak,s.hits],[6,3,3]);L.applyAnswer(s,false);T.eq([s.score,s.streak,s.miss],[6,0,1]);"),
        ("ظهور هر ۴ رنگ", "var w={},k={},i,t;for(i=0;i<200;i++){t=L.genTrial(rng);w[t.word]=1;k[t.ink]=1;}T.eq([w[0],w[1],w[2],w[3]],[1,1,1,1]);T.eq([k[0],k[1],k[2],k[3]],[1,1,1,1]);"),
        ("پایان با اتمام زمان", "var s=L.newState();T.ok(!L.tick(s,10));T.near(s.t,35,1e-9);T.ok(L.tick(s,35));T.ok(s.over);T.eq(s.t,0);"),
      ]),
    G("math-sprint", "ریاضی برق‌آسا", "arcade", "🧮", "#d9a441", "#3fb8af",
      "۶۰ ثانیه محاسبهٔ برق‌آسا؛ سؤال‌ها هر ۱۵ ثانیه سخت‌تر می‌شوند و هر اشتباه دو ثانیه از وقتت کم می‌کند.",
      "سریع جواب بده؛ اشتباه ۲ ثانیه جریمه دارد.",
      logic=MATH_LOGIC, ui=MATH_UI, css=MATH_CSS, engines=("common",),
      tests=[
        ("پاسخ درست میان گزینه‌ها", "var i,p,st,j;for(i=0;i<200;i++){p=L.genProblem(1+(i%4),rng);T.eq(p.choices.length,4);st={};for(j=0;j<4;j++){T.ok(typeof p.choices[j]==='number'&&p.choices[j]>=0);st[p.choices[j]]=1;}T.eq(Object.keys(st).length,4);T.ok(p.choices.indexOf(p.answer)>=0);if(p.kind===0)T.eq(p.a+p.b,p.answer);if(p.kind===1)T.eq(p.a-p.b,p.answer);if(p.kind===2)T.eq(p.a*p.b,p.answer);}"),
        ("تقسیم همیشه دقیق", "var i,p;for(i=0;i<300;i++){p=L.genProblem(1+(i%6),rng);if(p.kind===3){T.ok(p.b>1);T.eq(p.a,p.b*p.answer,'exact div');}}"),
        ("مخالف‌ها یکتا و نامنفی", "var i,d,ans,j,st;for(i=0;i<100;i++){ans=7+(i%13)*3;d=L.distractors(ans,rng);T.eq(d.length,3);st={};for(j=0;j<3;j++){T.ok(d[j]>=0);T.ok(d[j]!==ans);st[d[j]]=1;}T.eq(Object.keys(st).length,3);}"),
        ("رامپ یکنوای سطح", "T.eq(L.ramp(0),1);T.eq(L.ramp(14),1);T.eq(L.ramp(15),2);T.eq(L.ramp(59),4);var pr=0,t,lv;for(t=0;t<=60;t+=3){lv=L.ramp(t);T.ok(lv>=pr);pr=lv;}"),
        ("امتیاز و جریمهٔ زمان", "var s=L.newState(),p={answer:7,choices:[7,5,9,2]};T.ok(L.answer(s,p,0));T.eq([s.score,s.streak],[12,1]);T.ok(!L.answer(s,p,1));T.eq([s.score,s.streak,s.miss],[12,0,1]);T.near(s.t,58,1e-9);s.t=1;T.ok(!L.answer(s,p,2));T.ok(s.over);T.eq(s.t,0);"),
        ("جریان ۶۰ ثانیه", "var s=L.newState(),n=0;while(n<200){n++;if(L.tick(s,0.5))break;}T.ok(s.over);T.eq(n,120);T.eq(s.t,0);"),
      ]),
    G("typing", "سرعت تایپ", "arcade", "⌨", "#3fb8af", "#67b98a",
      "جمله‌های فارسی را سریع و دقیق تایپ کن؛ حروف درست سبز و غلط قرمز می‌شوند و سرعت و دقتت زنده نمایش داده می‌شود.",
      "حرف به حرف دقت کن؛ سبز یعنی درست.",
      logic=TYPE_LOGIC, ui=TYPE_UI, css=TYPE_CSS, engines=("common",),
      tests=[
        ("محاسبهٔ wpm", "T.eq(L.wpm(300,60000),60);T.eq(L.wpm(150,30000),60);T.eq(L.wpm(0,60000),0);T.eq(L.wpm(10,0),0);"),
        ("دقت تایپ", "T.approx(L.accuracy('سلام','سلام'),1);T.approx(L.accuracy('سلام','سالم'),0.5);T.eq(L.accuracy('','سلام'),1);T.approx(L.accuracy('سلامم','سلام'),0.8);"),
        ("پرچم‌های اختلاف", "T.eq(L.diff('سلامم','سلام'),[true,true,true,true,false]);T.eq(L.diff('سلام','سلامی'),[true,true,true,true,false]);T.eq(L.diff('سلم','سلام'),[true,true,false,false]);T.eq(L.diff('','سلام'),[false,false,false,false]);"),
        ("جمله‌های معتبر فارسی", "var i;T.ok(L.SENTENCES.length>=12);for(i=0;i<L.SENTENCES.length;i++){var sn=L.SENTENCES[i];T.ok(sn.length>=8,'len');T.ok(/[\\u0600-\\u06FF]/.test(sn),'fa');T.ok(sn.indexOf('\\u200C')<0,'zwnj');T.eq(sn,sn.replace(/^\\s+|\\s+$/g,''),'trim');}"),
        ("جملهٔ بعدی چرخشی", "var n=L.SENTENCES.length;T.eq(L.nextSentence(0),L.SENTENCES[1]);T.eq(L.nextSentence(n-1),L.SENTENCES[0]);T.eq(L.nextSentence(-1),L.SENTENCES[0]);"),
      ]),
    G("cups", "سه‌کاسه", "arcade", "🥤", "#d9a441", "#3fb8af",
      "توپ زیر یکی از سه کاسه نشان داده می‌شود؛ جابه‌جایی‌ها را دنبال کن و حدس بزن. هر مرحله سریع‌تر و شلوغ‌تر است.",
      "چشم روی توپ بگذار و جابه‌جایی‌ها را دنبال کن.",
      logic=CUPS_LOGIC, ui=CUPS_UI, css=CUPS_CSS, engines=("common",),
      tests=[
        ("ردیابی ۲۰۰ دنباله", "var i,st=L.newState(),seq,ball,cups,k,fin,a,b,tmp;for(i=0;i<200;i++){seq=L.swapSeq(st,L.levelSwaps(1+(i%5)),rng);ball=L.place(rng);cups=[0,1,2];for(k=0;k<seq.length;k++){a=seq[k][0];b=seq[k][1];tmp=cups[a];cups[a]=cups[b];cups[b]=tmp;}fin=cups.indexOf(ball);T.eq(L.track(ball,seq),fin);T.ok(fin>=0&&fin<3);}"),
        ("محل توپ مجاز", "var i,v;for(i=0;i<100;i++){v=L.place(rng);T.ok(v===0||v===1||v===2);}"),
        ("تعداد و قالب جابه‌جایی", "var lv,seq,st=L.newState(),k;for(lv=1;lv<=5;lv++){T.eq(L.levelSwaps(lv),3+lv);seq=L.swapSeq(st,L.levelSwaps(lv),rng);T.eq(seq.length,L.levelSwaps(lv));for(k=0;k<seq.length;k++){T.eq(seq[k].length,2);T.ok(seq[k][0]>=0&&seq[k][0]<3&&seq[k][1]>=0&&seq[k][1]<3);T.ok(seq[k][0]!==seq[k][1]);if(k>0)T.ok(seq[k][0]*3+seq[k][1]!==seq[k-1][0]*3+seq[k-1][1]);}}"),
        ("رشد شلوغی با مرحله", "T.ok(L.levelSwaps(1)<L.levelSwaps(2)&&L.levelSwaps(2)<L.levelSwaps(3)&&L.levelSwaps(3)<L.levelSwaps(4));"),
        ("جریان سه جان", "var s=L.newState();L.applyResult(s,false);T.eq(s.lives,2);L.applyResult(s,false);L.applyResult(s,false);T.ok(s.over);T.eq(s.lives,0);var s2=L.newState();L.applyResult(s2,true);T.eq(s2.lives,3);T.eq(s2.level,2);T.ok(s2.score>0);T.ok(!s2.over);"),
      ]),
]
