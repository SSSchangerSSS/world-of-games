# -*- coding: utf-8 -*-
"""AG-I3 — 5 Persian MCQ quiz games (cat=word, engines=(common,)).
proverb / antonym / flags / capitals / emoji-quiz — shared MCQ engine:
10s timer, streak scoring, seeded option shuffle, no-repeat pool with reshuffle."""
import json
from lib_mini import G

# ---------------------------------------------------------------- datasets
# (q, correct, [d1, d2, d3]) — handcrafted for semantic quality
PROVERBS = [
    ("هر که بامش بیش، ...", "برفش بیشتر", ["دودش بیشتر", "سقفش بلندتر", "هزینه‌اش کمتر"]),
    ("گر صبر کنی، ...", "ز غوره حلوا سازی", ["ز ترشی سرکه سازی", "ز نمک شکر سازی", "ز خار گل سازی"]),
    ("چراغی که به خانه رواست، ...", "به مسجد حرام است", ["به کوچه رواست", "به بازار آزاد است", "شب را روشن می‌کند"]),
    ("هر که خربزه می‌خورد، ...", "پای لرزش می‌نشیند", ["آب زیاد می‌خورد", "دندانش قوی می‌شود", "سیر می‌ماند"]),
    ("نابرده رنج، ...", "گنج میسر نمی‌شود", ["دستاوردی نیست", "شکست نمی‌خوری", "خسته نمی‌شوی"]),
    ("خشت اول چون نهد معمار کج، ...", "تا ثریا می‌رود دیوار کج", ["برمی‌گردد و درست می‌کند", "خانه محکم می‌شود", "دیوار کوتاه می‌ماند"]),
    ("عشق آسان نمود اول، ...", "ولی افتاد مشکل‌ها", ["و شد آسان آخرش", "و رفت تا ته خیابان", "و گشت شیرین همیشه"]),
    ("از دل برود، ...", "هر آن‌که از دیده برفت", ["هر آن‌که در خانه ماند", "هرگز بازنمی‌گردد", "هر که بی‌وفا باشد"]),
    ("آب که از سر گذشت، ...", "چه یک نی چه صد نی", ["سبک می‌شود", "پس می‌آید", "خشک می‌ماند"]),
    ("خواهی نشوی رسوا، ...", "هم‌رنگ جماعت شو", ["تنها راه برو", "حرف مردم را نخور", "سرت را بالا بگیر"]),
    ("از تو حرکت، ...", "از خدا برکت", ["از ما انتظار", "به تو پاداش", "از ما تشکر"]),
    ("کبوتر با کبوتر، ...", "باز با باز", ["پرواز با پرواز", "دانه با دانه", "آشیانه با آشیانه"]),
    ("مرغ همسایه، ...", "غاز است", ["گران است", "پرواز بلد است", "قربانی است"]),
    ("تا تنور داغ است، ...", "بچسب نان", ["بیرون برو", "صبر کن", "دست نزن"]),
    ("آب در هاون، ...", "کوبیدن", ["جوشیدن", "خوردن", "نوشیدن"]),
    ("یک تیر و ...", "دو نشان", ["یک هدف", "سه سؤال", "صد دلیل"]),
    ("سعدیا مرد نکونام، ...", "نمیرد هرگز", ["زیباست همیشه", "ثروتمند شد", "شاعر بود"]),
    ("بار کج، ...", "به منزل نمی‌رسد", ["سبک‌تر می‌شود", "زودتر می‌رسد", "گم نمی‌شود"]),
    ("موش کنج سوراخ، ...", "به مار چه گوید", ["پناه می‌برد", "دندان تیز می‌کند", "آرام می‌خوابد"]),
    ("ماهی را هر وقت از آب بگیری، ...", "تازه است", ["گران است", "بزرگ است", "سرخ می‌شود"]),
    ("دوست آن باشد که ...", "گیرد دوستِ دست", ["همیشه تعریف کند", "هدیه بدهد", "دور باشد از تو"]),
    ("بنی‌آدم اعضای ...", "یک پیکرند", ["جدا شوندند", "بی‌شمارند", "یکسان ندارند"]),
    ("شتر در خواب بیند ...", "پنبه‌دانه", ["شن و ماسه", "آب خنک", "کوه بلند"]),
    ("با یک گل، ...", "بهار نمی‌شود", ["گلستان نشود", "عطر پخش نمی‌شود", "پژمرده نمی‌شود"]),
    ("کاسه‌ای زیر ...", "نیم‌کاسه", ["دیگ پنهان است", "سفره پهن است", "آب گرم است"]),
]

ANTONYMS = [
    ("مترادفِ «بزرگ»؟", "کلان", ["کوچک", "خسته", "شاد"]),
    ("مترادفِ «شاد»؟", "خوشحال", ["ناراحت", "خشمگین", "سرد"]),
    ("مترادفِ «زیبا»؟", "خوشگل", ["زشت", "تمیز", "بلند"]),
    ("مترادفِ «آسان»؟", "ساده", ["دشوار", "سریع", "پرریا"]),
    ("مترادفِ «آغاز»؟", "شروع", ["پایان", "میانه", "نتیجه"]),
    ("مترادفِ «پایان»؟", "سرانجام", ["شروع", "میانه", "بعد"]),
    ("مترادفِ «سریع»؟", "تند", ["آهسته", "کند", "آرام"]),
    ("مترادفِ «خوشبخت»؟", "سعادت‌مند", ["بدبخت", "ناکام", "فقیر"]),
    ("مترادفِ «غمگین»؟", "اندوهگین", ["شاد", "خندان", "سرحال"]),
    ("مترادفِ «پرسش»؟", "سؤال", ["پاسخ", "جواب", "خبر"]),
    ("مترادفِ «کوشش»؟", "تلاش", ["تنبلی", "استراحت", "بی‌حوصلگی"]),
    ("مترادفِ «خانه»؟", "مسکن", ["خیابان", "مغازه", "شهر"]),
    ("مترادفِ «کودک»؟", "طفل", ["پیر", "جوان", "بلندقد"]),
    ("مترادفِ «دانش»؟", "علم", ["جهل", "سادگی", "بازی"]),
    ("مترادفِ «شجاع»؟", "دلیر", ["ترسو", "بزدل", "ضعیف"]),
    ("متضادِ «گرم»؟", "سرد", ["داغ", "تفتیده", "ولرم"]),
    ("متضادِ «بالا»؟", "پایین", ["سقف", "فراز", "میانه"]),
    ("متضادِ «روز»؟", "شب", ["ظهر", "صبح", "عصر"]),
    ("متضادِ «بلند»؟", "کوتاه", ["دراز", "رسا", "کشیده"]),
    ("متضادِ «پر»؟", "خالی", ["لبریز", "سیراب", "کامل"]),
    ("متضادِ «خشک»؟", "تر", ["یخ‌زده", "نرم", "خسته"]),
    ("متضادِ «ساکت»؟", "پرحرف", ["خاموش", "آرام", "بی‌صدا"]),
    ("متضادِ «شلوغ»؟", "خلوت", ["شاد", "پر جمعیت", "بزرگ"]),
    ("متضادِ «پیروزی»؟", "شکست", ["موفقیت", "برد", "فتح"]),
    ("متضادِ «شمال»؟", "جنوب", ["مغرب", "مشرق", "شرق"]),
    ("متضادِ «سنگین»؟", "سبک", ["وزین", "محکم", "پهن"]),
    ("متضادِ «تازه»؟", "کهنه", ["نو", "مرطوب", "لطیف"]),
    ("متضادِ «آشنا»؟", "غریبه", ["دوست", "رفیق", "همسایه"]),
    ("متضادِ «زنده»؟", "مرده", ["بیدار", "سالم", "جوان"]),
    ("متضادِ «ارزان»؟", "گران", ["کم", "ساده", "مفت"]),
]

# (flag emoji, country fa) — verified ISO-3166 regional-indicator pairs
FLAGS = [
    ("🇮🇷", "ایران"), ("🇹🇷", "ترکیه"), ("🇩🇪", "آلمان"), ("🇫🇷", "فرانسه"),
    ("🇬🇧", "انگلستان"), ("🇺🇸", "آمریکا"), ("🇮🇹", "ایتالیا"), ("🇪🇸", "اسپانیا"),
    ("🇵🇹", "پرتغال"), ("🇷🇺", "روسیه"), ("🇨🇳", "چین"), ("🇯🇵", "ژاپن"),
    ("🇰🇷", "کره جنوبی"), ("🇧🇷", "برزیل"), ("🇦🇷", "آرژانتین"), ("🇲🇽", "مکزیک"),
    ("🇨🇦", "کانادا"), ("🇦🇺", "استرالیا"), ("🇮🇳", "هند"), ("🇵🇰", "پاکستان"),
    ("🇸🇦", "عربستان سعودی"), ("🇮🇶", "عراق"), ("🇦🇪", "امارات متحده عربی"), ("🇶🇦", "قطر"),
    ("🇰🇼", "کویت"), ("🇪🇬", "مصر"), ("🇲🇦", "مراکش"), ("🇹🇳", "تونس"),
    ("🇩🇿", "الجزایر"), ("🇱🇾", "لیبی"), ("🇬🇷", "یونان"), ("🇳🇱", "هلند"),
    ("🇧🇪", "بلژیک"), ("🇨🇭", "سوئیس"), ("🇦🇹", "اتریش"), ("🇸🇪", "سوئد"),
    ("🇳🇴", "نروژ"), ("🇩🇰", "دانمارک"), ("🇫🇮", "فنلاند"), ("🇵🇱", "لهستان"),
]

CAPITALS = [
    ("ایران", "تهران"), ("ترکیه", "آنکارا"), ("آلمان", "برلین"), ("فرانسه", "پاریس"),
    ("انگلستان", "لندن"), ("آمریکا", "واشینگتن"), ("ایتالیا", "رم"), ("اسپانیا", "مادرید"),
    ("پرتغال", "لیسبون"), ("روسیه", "مسکو"), ("چین", "پکن"), ("ژاپن", "توکیو"),
    ("کره جنوبی", "سئول"), ("برزیل", "برازیلیا"), ("آرژانتین", "بوئنوس آیرس"), ("مکزیک", "مکزیکوسیتی"),
    ("کانادا", "اتاوا"), ("استرالیا", "کانبرا"), ("هند", "دهلی نو"), ("پاکستان", "اسلام‌آباد"),
    ("عربستان سعودی", "ریاض"), ("عراق", "بغداد"), ("امارات متحده عربی", "ابوظبی"), ("قطر", "دوحه"),
    ("مصر", "قاهره"), ("مراکش", "رباط"), ("لیبی", "طرابلس"), ("یونان", "آتن"),
    ("هلند", "آمستردام"), ("بلژیک", "بروکسل"), ("سوئیس", "برن"), ("اتریش", "وین"),
    ("سوئد", "استکهلم"), ("نروژ", "اسلو"), ("دانمارک", "کپنهاگ"), ("فنلاند", "هلسینکی"),
    ("لهستان", "ورشو"), ("اوکراین", "کی‌یف"), ("گرجستان", "تفلیس"), ("آذربایجان", "باکو"),
]

# (emoji sequence, answer fa) — family-friendly, famous, generic
EMOJIS = [
    ("🚢🧊", "تایتانیک"), ("🦁👑", "سیمبا"), ("💍🌋", "ارباب حلقه‌ها"), ("🧛‍♂️🌙", "خون‌آشام"),
    ("🎩🔍", "شرلوک هلمز"), ("🐼🥋", "کونگ‌فو پاندا"), ("🛸👽", "موجود فضایی"), ("👻🏚️", "خانهٔ تسخیرشده"),
    ("⚽🏆", "جام جهانی"), ("❄️⛄", "آدم‌برفی"), ("🌈🌧️", "رنگین‌کمان"), ("🕵️🔍", "کارآگاه"),
    ("🧑‍🚀🚀", "فضانورد"), ("🧙‍♂️🪄", "جادوگر"), ("🎨🖌️", "نقاش"), ("🏥🩺", "پزشک"),
    ("👨‍🍳🍳", "آشپز"), ("👮🚨", "پلیس"), ("🚒🔥", "آتش‌نشان"), ("🐟🎣", "ماهیگیری"),
    ("🥾⛰️", "کوهنورد"), ("🍔🍟", "فست‌فود"), ("📚🎓", "دانشگاه"), ("🚂🛤️", "قطار"),
    ("🧟🌕", "فیلم ترسناک"),
]

def _opts(pool, idx, k=3):
    """Deterministic distractors from pool (never the answer, never repeated)."""
    n = len(pool); out = []; used = {pool[idx]}; j = (idx * 7 + 3) % n
    while len(out) < k:
        w = pool[j % n]
        if w not in used:
            used.add(w); out.append(w)
        j += 1
    return out

def _mcq(q, correct, ds):
    return {"q": q, "options": [correct] + ds, "a": 0}

def _gen(pairs, pool, qfmt=None):
    return [_mcq(qfmt(a, b) if qfmt else a, b, _opts(pool, i))
            for i, (a, b) in enumerate(pairs)]

PROVERB_ITEMS = [_mcq(q, c, ds) for q, c, ds in PROVERBS]
ANT_ITEMS = [_mcq(q, c, ds) for q, c, ds in ANTONYMS]
FLAG_ITEMS = _gen(FLAGS, [b for _, b in FLAGS])
CAP_ITEMS = _gen(CAPITALS, [b for _, b in CAPITALS], qfmt=lambda c, cap: "پایتختِ " + c + "؟")
EMOJI_ITEMS = _gen(EMOJIS, [b for _, b in EMOJIS])

for _its in (PROVERB_ITEMS, ANT_ITEMS, FLAG_ITEMS, CAP_ITEMS, EMOJI_ITEMS):
    for _it in _its:
        assert _it["q"] and len(_it["options"]) == 4 and len(set(_it["options"])) == 4
        assert 0 <= _it["a"] < 4

# ---------------------------------------------------------------- logic (pure JS, shared)
LOGIC_TMPL = r"""var WOG_LOGIC=(function(){
var ITEMS=__ITEMS__;
var ROUND=10;
function range(n){var a=[],i;for(i=0;i<n;i++)a.push(i);return a;}
function shuffled(arr,rng){rng=rng||Math.random;var a=arr.slice(),i,j,t;for(i=a.length-1;i>0;i--){j=Math.floor(rng()*(i+1));t=a[i];a[i]=a[j];a[j]=t;}return a;}
function shuffleOptions(item,rng){var idx=shuffled([0,1,2,3],rng),o=[],k,a=0;for(k=0;k<4;k++)o.push(item.options[idx[k]]);for(k=0;k<4;k++)if(idx[k]===item.a)a=k;return{q:item.q,options:o,a:a};}
function pickPool(n,rng){var res=[],pool=shuffled(range(ITEMS.length),rng);while(res.length<n){if(!pool.length)pool=shuffled(range(ITEMS.length),rng);res.push(pool.pop());}return res;}
function judge(choice,a){return choice===a;}
function scoreFlow(score,streak,correct){if(correct){var ns=streak+1,g=10+(ns-1)*2;return{score:score+g,streak:ns,gain:g};}return{score:score,streak:0,gain:0};}
function start(rng){return{pool:shuffled(range(ITEMS.length),rng),score:0,streak:0,answered:0,seen:[],cur:null,done:false};}
function next(state,rng){if(state.done)return null;if(!state.pool.length)state.pool=shuffled(range(ITEMS.length),rng);state.cur=shuffleOptions(ITEMS[state.pool.pop()],rng);state.seen.push(state.cur.q);return state.cur;}
function answer(state,choice){if(!state.cur||state.done)return null;var c=judge(choice,state.cur.a),f=scoreFlow(state.score,state.streak,c);state.score=f.score;state.streak=f.streak;state.answered++;if(state.answered>=ROUND)state.done=true;return{correct:c,gain:f.gain,done:state.done,answer:state.cur.options[state.cur.a]};}
return{ITEMS:ITEMS,ROUND:ROUND,range:range,shuffled:shuffled,shuffleOptions:shuffleOptions,pickPool:pickPool,judge:judge,scoreFlow:scoreFlow,start:start,next:next,answer:answer};
})();"""

# ---------------------------------------------------------------- ui (shared wiring)
UI_TMPL = r"""var KEY='__KEY__',SUB='__SUB__',TL=10,BIG=__BIG__;
var app=$('#app'),st=null,timer=null,left=TL,lock=false;
$('#hint').textContent='__HINT__';
function hudUp(){var b=storeBest(KEY)||0;hud('امتیاز: '+fa(st?st.score:0)+' · پیاپی: '+fa(st?st.streak:0)+' · رکورد: '+fa(b)+' · زمان: <span id="tsec">'+fa(Math.max(0,Math.ceil(left)))+'</span>');}
function menu(){stopTimer();st=null;app.innerHTML='<div class="start"><p>__DESC__</p><button id="go" class="btn" data-smoke>شروع بازی</button></div>';$('#go').onclick=newRound;hudUp();}
function newRound(){stopTimer();st=L.start(Math.random);lock=false;nextQ();}
function nextQ(){lock=false;var q=L.next(st,Math.random);if(!q){endRound();return;}left=TL;hudUp();var h='<div class="qpanel"><div class="'+(BIG?'qbig':'qtext')+'">'+q.q+'</div><div class="qsub">'+SUB+'</div></div><div class="bar"><i id="tbar" style="width:100%"></i></div><div class="ogrid">';for(var i=0;i<4;i++)h+='<button class="opt" data-i="'+i+'">'+q.options[i]+'</button>';h+='</div><div id="fb" class="feedback"></div>';app.innerHTML=h;var bs=$$('.opt');for(var j=0;j<bs.length;j++)bs[j].onclick=function(){pick(+this.getAttribute('data-i'));};startTimer();}
function startTimer(){stopTimer();timer=setInterval(tick,100);}
function tick(){left-=0.1;var b=$('#tbar');if(b)b.style.width=Math.max(0,left/TL*100)+'%';var s=$('#tsec');if(s)s.textContent=fa(Math.max(0,Math.ceil(left)));if(left<=0){stopTimer();timeUp();}}
function stopTimer(){if(timer){clearInterval(timer);timer=null;}}
function pick(i){if(lock)return;lock=true;stopTimer();var res=L.answer(st,i);mark(i);var fb=$('#fb');if(res.correct){fb.textContent='آفرین! +'+fa(res.gain)+' امتیاز'+(st.streak>1?' · پیاپیِ '+fa(st.streak):'');fb.className='feedback ok';}else{fb.textContent='اشتباه! پاسخ درست: '+res.answer;fb.className='feedback no';}hudUp();setTimeout(step,1200);}
function timeUp(){if(lock)return;lock=true;var res=L.answer(st,-1);mark(-1);var fb=$('#fb');fb.textContent='زمان تمام شد! پاسخ درست: '+res.answer;fb.className='feedback no';hudUp();setTimeout(step,1200);}
function mark(chosen){var bs=$$('.opt');for(var k=0;k<bs.length;k++){bs[k].disabled=true;if(k===st.cur.a)bs[k].classList.add('correct');else if(k===chosen)bs[k].classList.add('wrong');}}
function step(){if(st.done)endRound();else nextQ();}
function endRound(){stopTimer();var best=bestOf(KEY,st.score);ovl('پایان دور','امتیاز شما: '+fa(st.score)+' · رکورد: '+fa(best),'بازی جدید',newRound);hudUp();}
menu();"""

CSS = r"""#app{max-width:560px;margin:0 auto;padding:10px}
.start{text-align:center;padding:28px 12px}
.start p{color:#a9b8d8;line-height:2.1;font-size:14px}
.btn{display:block;width:100%;min-height:48px;border-radius:12px;border:1px solid #d9a441;background:#d9a441;color:#14203a;font-weight:800;font-size:17px;cursor:pointer;touch-action:manipulation;font-family:inherit}
.qpanel{background:#14203a;border:1px solid #22335c;border-radius:14px;padding:14px 12px;text-align:center;margin-bottom:10px}
.qtext{font-size:21px;line-height:1.9;font-weight:700}
.qbig{font-size:56px;line-height:1.5;direction:ltr;unicode-bidi:isolate}
.qsub{color:#8fa3c8;font-size:13px;margin-top:6px}
.bar{height:8px;background:#0e1830;border-radius:6px;overflow:hidden;margin:0 0 12px}
.bar i{display:block;height:100%;background:#3fb8af;transition:width .12s linear}
.ogrid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.opt{min-height:56px;border-radius:12px;border:1px solid #2a3d68;background:#182a4d;color:#e8eefc;font-size:15px;font-weight:600;padding:8px;cursor:pointer;touch-action:manipulation;font-family:inherit;line-height:1.7}
.opt.correct{background:#1e4d3a;border-color:#67b98a;color:#c9f2dd}
.opt.wrong{background:#5a2b24;border-color:#e26d5c;color:#ffd9d2}
.opt:disabled{cursor:default}
.feedback{min-height:22px;text-align:center;font-weight:700;margin-top:12px;font-size:15px}
.feedback.ok{color:#67b98a}.feedback.no{color:#e26d5c}"""

# ---------------------------------------------------------------- tests (shared shape, 6 per game)
T1 = r"""T.ok(L.ITEMS.length>=__MIN__,'تعداد آیتم‌ها');
var i,it,j,u,qs={};
for(i=0;i<L.ITEMS.length;i++){it=L.ITEMS[i];
 T.ok(typeof it.q==='string'&&it.q.length>0,'سؤال خالی '+i);
 __QCHK__
 T.ok(it.options.length===4,'۴ گزینه '+i);
 u={};
 for(j=0;j<4;j++){T.ok(typeof it.options[j]==='string'&&it.options[j].length>0,'گزینه خالی '+i);u[it.options[j]]=1;}
 T.ok(Object.keys(u).length===4,'گزینه تکراری '+i);
 T.ok(it.a===Math.floor(it.a)&&it.a>=0&&it.a<4,'شاخص پاسخ '+i);
 T.ok(typeof it.options[it.a]==='string','پاسخ ناموجود '+i);
 qs[it.q]=1;}
T.ok(Object.keys(qs).length===L.ITEMS.length,'سؤال تکراری');"""

T2 = r"""var stubs=[function(){return 0.05;},function(){return 0.5;},function(){return 0.95;}],s,i,j,u;
for(s=0;s<stubs.length;s++)for(i=0;i<L.ITEMS.length;i++){var it=L.ITEMS[i],sh=L.shuffleOptions(it,stubs[s]);
 T.eq(sh.q,it.q,'سؤال حفظ نشد');
 u={};for(j=0;j<4;j++)u[sh.options[j]]=1;
 T.ok(Object.keys(u).length===4,'یکتا پس از بُر');
 T.ok(sh.a>=0&&sh.a<4,'a خارج محدوده');
 T.eq(sh.options[sh.a],it.options[it.a],'پاسخ در گزینه‌ها');}
for(i=0;i<L.ITEMS.length;i++){var s2=L.shuffleOptions(L.ITEMS[i],rng);T.eq(s2.options[s2.a],L.ITEMS[i].options[L.ITEMS[i].a],'پاسخ بذری');}"""

T3 = r"""var N=L.ITEMS.length,p=L.pickPool(N,rng),u={},i;
T.eq(p.length,N,'طول استخر');
for(i=0;i<N;i++)u[p[i]]=1;
T.ok(Object.keys(u).length===N,'تکرار در یک دوره');
var p2=L.pickPool(N*2+3,rng),u1={},u2={};
T.eq(p2.length,N*2+3,'طول استخر بزرگ');
for(i=0;i<N;i++){u1[p2[i]]=1;u2[p2[N+i]]=1;}
T.ok(Object.keys(u1).length===N,'دورهٔ اول بی‌تکرار');
T.ok(Object.keys(u2).length===N,'دورهٔ دوم پس از ری‌شافل بی‌تکرار');
var c=function(){return 0.3;},p3=L.pickPool(N,c),u3={};
for(i=0;i<N;i++)u3[p3[i]]=1;
T.ok(Object.keys(u3).length===N,'جایگشت با rng ثابت');"""

T4 = r"""var st=L.start(rng),EXP=0,k,res;
for(k=0;k<10;k++){var q=L.next(st,rng);T.ok(!!q,'سؤال '+k);res=L.answer(st,st.cur.a);T.ok(res.correct,'پاسخ درست '+k);EXP+=10+2*k;}
T.eq(st.score,EXP,'ریاضی امتیاز');
T.eq(st.score,190,'جمع دقیق ۱۹۰');
T.eq(st.streak,10,'پیاپی ۱۰');
T.eq(st.answered,10,'شمارش ۱۰');
T.eq(st.seen.length,10,'طول سؤال‌ها');
var u={};for(k=0;k<10;k++)u[st.seen[k]]=1;
T.ok(Object.keys(u).length===10,'تکرار سؤال در دور');
T.ok(st.done,'پایان دور');
T.eq(L.next(st,rng),null,'سؤال پس از پایان');"""

T5 = r"""T.ok(L.judge(2,2),'درست');
T.ok(!L.judge(1,2),'غلط');
T.ok(!L.judge(-1,2),'پاسخ خطا');
var r=L.scoreFlow(0,0,true);T.eq(r.score,10,'+۱۰');T.eq(r.streak,1,'پیاپی ۱');T.eq(r.gain,10,'سود ۱');
r=L.scoreFlow(10,1,true);T.eq(r.score,22,'+۱۲');T.eq(r.streak,2,'پیاپی ۲');
r=L.scoreFlow(22,2,true);T.eq(r.score,36,'+۱۴');
r=L.scoreFlow(36,3,true);T.eq(r.score,52,'+۱۶');
r=L.scoreFlow(52,4,true);T.eq(r.score,70,'+۱۸');T.eq(r.streak,5,'پیاپی ۵');
r=L.scoreFlow(100,7,false);T.eq(r.score,100,'بی‌جریمه');T.eq(r.streak,0,'ریست پیاپی');T.eq(r.gain,0,'سود صفر');"""

T6 = r"""var st=L.start(rng),k;
L.next(st,rng);
var bad=(st.cur.a+1)%4;
var r=L.answer(st,bad);
T.ok(!r.correct,'پاسخ غلط');
T.eq(st.streak,0,'ریست پیاپی');
T.eq(st.score,0,'بدون امتیاز');
T.eq(st.answered,1,'شمارش ۱');
T.ok(!st.done,'دور ادامه دارد');
for(k=1;k<10;k++){L.next(st,rng);L.answer(st,st.cur.a);}
T.ok(st.done,'پایان پس از ۱۰');
T.eq(st.answered,10,'شمارش ۱۰');
T.ok(st.score>=90,'امتیاز ۹ درست');
T.eq(L.answer(st,0),null,'پاسخ پس از پایان');"""

QCHK_PLAIN = "T.ok(it.q.length>=3,'سؤال کوتاه '+i);"
QCHK_FLAGS = "T.ok(it.q.length===4,'پرچم نامعتبر '+i);T.ok(!/[a-zA-Z0-9]/.test(it.q),'حرف در پرچم '+i);"
QCHK_EMOJI = "T.ok(!/[\\x00-\\x7f]/.test(it.q),'ایموجی خالص '+i);T.ok(it.q.length>=2&&it.q.length<=14,'ایموجی بی‌اندازه '+i);"

def _tests(minn, qchk):
    t1 = T1.replace("__QCHK__", qchk).replace("__MIN__", str(minn))
    return [("درستی داده‌ها", t1), ("بُر گزینه‌ها پاسخ را نگه می‌دارد", T2),
            ("استخر بدون تکرار تا اتمام", T3), ("دور بذری: ۱۰ پاسخ درست", T4),
            ("داوری و ریاضی امتیاز", T5), ("شکست پیاپی و پایان دور", T6)]

def _game(slug, title, icon, g1, g2, desc, hint, sub, key, items, big, qchk, minn):
    body = r'{"q":' + json.dumps(items[0]["q"], ensure_ascii=False) + '}'  # placeholder-free sanity
    assert body and items
    logic = LOGIC_TMPL.replace("__ITEMS__", json.dumps(items, ensure_ascii=False, separators=(',', ':')))
    ui = (UI_TMPL.replace("__KEY__", key).replace("__SUB__", sub)
          .replace("__HINT__", hint).replace("__DESC__", desc)
          .replace("__BIG__", "true" if big else "false"))
    return G(slug, title, "word", icon, g1, g2, desc, hint, logic=logic, ui=ui, css=CSS,
             engines=("common",), tests=_tests(minn, qchk))

GAMES = [
    _game("proverb", "ضرب‌المثل‌ها", "📜", "#d9a441", "#3fb8af",
          "نیمهٔ نخست یک ضرب‌المثل معروف را می‌بینید؛ ادامهٔ درستش را از میان چهار گزینه پیدا کنید.",
          "۱۰ ثانیه برای هر مثل؛ پاسخ‌های پیاپی امتیاز بیشتری دارند (۱۰+۲×پیاپی).",
          "ادامهٔ درستِ ضرب‌المثل کدام است؟", "wog-proverb-best",
          PROVERB_ITEMS, False, QCHK_PLAIN, 25),
    _game("antonym", "مترادف و متضاد", "↔️", "#3fb8af", "#d9a441",
          "به نوع هر سؤال دقت کنید و مترادف یا متضادِ واژهٔ داده‌شده را از میان چهار گزینه انتخاب کنید.",
          "دقت کن: سؤال «متضاد» است یا «مترادف»؟ پاسخ پیاپی امتیاز بیشتر می‌دهد.",
          "گزینهٔ درست کدام است؟", "wog-antonym-best",
          ANT_ITEMS, False, QCHK_PLAIN, 30),
    _game("flags", "پرچم‌ها", "🚩", "#67b98a", "#d9a441",
          "پرچم یک کشور را می‌بینید؛ نام آن کشور را از میان چهار گزینه حدس بزنید.",
          "به رنگ‌ها و نمادهای پرچم دقت کن؛ ۱۰ ثانیه وقت داری.",
          "این پرچم مالِ کدام کشور است؟", "wog-flags-best",
          FLAG_ITEMS, True, QCHK_FLAGS, 40),
    _game("capitals", "پایتخت‌ها", "🏛️", "#3fb8af", "#67b98a",
          "پایتخت هر کشور را از میان چهار گزینه حدس بزنید؛ حواستان باشد پایتخت همیشه مشهورترین شهر نیست!",
          "پایتخت همیشه بزرگ‌ترین شهر نیست! ۱۰ ثانیه وقت داری.",
          "پایتختِ درست کدام است؟", "wog-capitals-best",
          CAP_ITEMS, False, QCHK_PLAIN, 40),
    _game("emoji-quiz", "حدس با ایموجی", "🎯", "#d9a441", "#e26d5c",
          "از روی رشتهٔ ایموجی‌ها حدس بزنید چه فیلم، شغل یا چیز مشهوری در ذهن ماست.",
          "ترتیب ایموجی‌ها یک قصه می‌گوید؛ فیلم، شغل یا چیز مشهور را حدس بزن.",
          "چه چیزی را نشان می‌دهد؟", "wog-emoji-quiz-best",
          EMOJI_ITEMS, True, QCHK_EMOJI, 25),
]
