# -*- coding: utf-8 -*-
"""Renders landing index.html + licenses.html for the 100-game site."""
import io, os, json, html

CAT_LABEL = {
    "board": "تخته و استراتژی", "cards": "بازی‌های کارتی", "puzzle": "پازل و فکری",
    "arcade": "اکشن و مهارتی", "word": "واژه و دانش", "luck": "شانس و سرگرمی",
}
CAT_COLOR = {
    "board": "#d9a441", "cards": "#3fb8af", "puzzle": "#a78bfa",
    "arcade": "#e26d5c", "word": "#67b98a", "luck": "#e8c073",
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
@font-face{font-family:Vazirmatn;src:url(fonts/Vazirmatn-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:Vazirmatn;src:url(fonts/Vazirmatn-Medium.woff2) format('woff2');font-weight:500;font-display:swap}
@font-face{font-family:Vazirmatn;src:url(fonts/Vazirmatn-Bold.woff2) format('woff2');font-weight:700;font-display:swap}
@font-face{font-family:Vazirmatn;src:url(fonts/Vazirmatn-Black.woff2) format('woff2');font-weight:900;font-display:swap}
:root{--bg:#0b1220;--bg2:#101a2e;--panel:#14203a;--gold:#d9a441;--gold2:#e8c073;--turq:#3fb8af;--txt:#f3ead8;--dim:#a8b3c9;--line:rgba(217,164,65,.3)}
html{scroll-behavior:smooth}
body{font-family:Vazirmatn,Tahoma,sans-serif;background:linear-gradient(160deg,var(--bg2),var(--bg));color:var(--txt);min-height:100dvh}
a{color:inherit;text-decoration:none}
.nav{position:sticky;top:0;z-index:50;display:flex;gap:14px;align-items:center;justify-content:space-between;padding:12px clamp(14px,4vw,42px);background:rgba(11,18,32,.88);backdrop-filter:blur(9px);border-bottom:1px solid var(--line)}
.brand{font-weight:900;font-size:1.12rem;color:var(--gold)}
.brand span{color:var(--turq)}
.nav .links{display:flex;gap:16px;font-size:.9rem;color:var(--dim)}
.nav .links a:hover{color:var(--gold2)}
@media(max-width:700px){.nav .links{display:none}}
.hero{max-width:1080px;margin:0 auto;padding:64px 20px 40px;text-align:center}
.hero .kicker{display:inline-block;background:rgba(63,184,175,.12);border:1px solid rgba(63,184,175,.4);color:var(--turq);padding:6px 14px;border-radius:99px;font-size:.82rem;margin-bottom:18px}
.hero h1{font-size:clamp(1.7rem,5vw,3rem);font-weight:900;line-height:1.5}
.hero h1 b{color:var(--gold)}
.hero p{color:var(--dim);max-width:640px;margin:16px auto 0;line-height:2.1;font-size:.98rem}
.stats{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px 22px;min-width:120px}
.stat b{display:block;font-size:1.35rem;color:var(--gold2)}
.stat span{font-size:.8rem;color:var(--dim)}
.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.btn{background:var(--gold);color:#221806;font-weight:700;border:0;border-radius:12px;padding:12px 26px;font-size:.98rem;font-family:inherit;cursor:pointer;transition:.15s}
.btn:hover{filter:brightness(1.08)}
.btn.ghost{background:transparent;color:var(--gold2);border:1px solid var(--line)}
section{max-width:1180px;margin:0 auto;padding:46px 18px}
.sec-title{text-align:center;margin-bottom:8px}
.sec-title h2{font-size:1.5rem;color:var(--gold);font-weight:800}
.sec-title p{color:var(--dim);font-size:.92rem;margin-top:6px}
.tools{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;align-items:center;margin:20px 0 6px}
.search{background:var(--panel);border:1px solid var(--line);border-radius:12px;color:var(--txt);font-family:inherit;padding:10px 16px;width:min(360px,86vw);font-size:.95rem}
.chip{background:var(--panel);border:1px solid var(--line);color:var(--dim);border-radius:99px;padding:8px 15px;font-size:.85rem;font-family:inherit;cursor:pointer}
.chip.on{background:rgba(217,164,65,.16);color:var(--gold2);border-color:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:13px;margin-top:20px}
.tile{position:relative;background:var(--panel);border:1px solid rgba(217,164,65,.18);border-radius:16px;padding:16px 14px 14px;display:flex;flex-direction:column;gap:8px;transition:.16s;overflow:hidden}
.tile:hover{transform:translateY(-4px);border-color:var(--gold)}
.tile .ico{width:52px;height:52px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:1.65rem}
.tile h3{font-size:1rem;color:var(--txt)}
.tile p{font-size:.78rem;color:var(--dim);line-height:1.9;flex:1}
.tile .cat{align-self:flex-start;font-size:.68rem;padding:3px 10px;border-radius:99px;border:1px solid}
.count{color:var(--dim);font-size:.8rem;text-align:center;margin-top:14px}
.feats{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.feat{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px}
.feat .fi{font-size:1.5rem;margin-bottom:8px}
.feat h3{color:var(--gold2);font-size:1.02rem;margin-bottom:8px}
.feat p{color:var(--dim);font-size:.85rem;line-height:2}
.mcp-list{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px;max-width:640px;margin:0 auto}
.mcp-list code{display:block;background:#0d1526;border:1px solid rgba(63,184,175,.3);color:var(--turq);border-radius:9px;padding:9px 14px;margin:7px 0;font-size:.86rem;direction:ltr;text-align:left}
.donate{background:linear-gradient(140deg,rgba(217,164,65,.13),rgba(63,184,175,.08));border:1px solid var(--line);border-radius:20px;padding:34px 24px;text-align:center;max-width:720px;margin:0 auto}
.donate p{color:var(--dim);line-height:2.1;margin:12px 0 20px;font-size:.94rem}
footer{border-top:1px solid var(--line);margin-top:40px;padding:26px 18px;text-align:center;color:var(--dim);font-size:.85rem;line-height:2.2}
footer a{color:var(--gold2)}
.lic{max-width:860px;margin:0 auto;padding:40px 20px;line-height:2.2}
.lic h1{color:var(--gold);font-size:1.6rem;margin-bottom:18px}
.lic h2{color:var(--gold2);font-size:1.15rem;margin:26px 0 10px}
.lic p,.lic li{color:var(--dim);font-size:.94rem}
.lic ul{padding-inline-start:22px}
.lic .ok{color:var(--turq)}
.lic table{width:100%;border-collapse:collapse;margin-top:12px;font-size:.88rem}
.lic td,.lic th{border:1px solid var(--line);padding:9px 12px;text-align:right}
.lic th{color:var(--gold2)}
"""

TPL = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>دنیای بازی‌ها — ۱۰۰ بازی ایرانی تحت وب</title>
<meta name="description" content="مجموعه کامل ۱۰۰ بازی مرورگری ایرانی: شطرنج، نرد، حکم، پاسور، سودوکو، ۲۰۴۸ و بازی‌های کلاسیک — همه رایگان، آفلاین و بدون تبلیغات.">
<meta property="og:title" content="دنیای بازی‌ها — ۱۰۰ بازی ایرانی تحت وب">
<meta property="og:description" content="شطرنج، نرد، حکم، پاسور، سولیتر و ۹۵ بازی دیگر — رایگان و بدون تبلیغات.">
<meta property="og:type" content="website">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>__CSS__</style>
<script type="application/ld+json">__JSONLD__</script>
</head>
<body>
<nav class="nav">
  <div class="brand">دنیای <span>بازی‌ها</span> ❋</div>
  <div class="links">
    <a href="#games">بازی‌ها</a><a href="#features">ویژگی‌ها</a><a href="#developers">توسعه‌دهندگان</a><a href="#mcp">MCP</a><a href="#donate">حمایت</a><a href="licenses.html">مجوزها</a>
  </div>
  <a class="btn ghost" style="padding:8px 18px;font-size:.85rem" href="#games">شروع بازی</a>
</nav>

<header class="hero">
  <span class="kicker">نسخهٔ پیش‌نمایش عمومی — میزبانی GitHub Pages</span>
  <h1>۱۰۰ بازی کلاسیک و ایرانی،<br><b>همین‌جا توی مرورگرت</b></h1>
  <p>از شطرنج و نرد و حکم تا سودوکو، ۲۰۴۸، مار و سولیتر — همه با رابط فارسی و راست‌به‌چپ، طراحی الهام‌گرفته از هنر ایران‌باستان، بدون تبلیغات، بدون ثبت‌نام و کاملاً رایگان. روی گوشی و کامپیوتر بازی کن؛ همه‌چیز آفلاین اجرا می‌شود.</p>
  <div class="stats">
    <div class="stat"><b>۱۰۰</b><span>بازی قابل اجرا</span></div>
    <div class="stat"><b>۶</b><span>دستهٔ موضوعی</span></div>
    <div class="stat"><b>۰ تومان</b><span>هزینه، برای همیشه</span></div>
    <div class="stat"><b>۱۰۰٪</b><span>فارسی و RTL</span></div>
  </div>
  <div class="cta-row">
    <a class="btn" href="#games">ورود به گالری بازی‌ها</a>
    <a class="btn ghost" href="https://github.com/SSSchangerSSS/world-of-games" rel="noopener">سورس در گیت‌هاب</a>
  </div>
</header>

<section id="games">
  <div class="sec-title"><h2>گالری بازی‌ها</h2><p>جست‌وجو کن یا دسته‌ات را انتخاب کن — ۱۰۰ بازی منتظر تو هستند</p></div>
  <div class="tools">
    <input class="search" id="q" type="search" placeholder="جست‌وجوی بازی… (مثلاً شطرنج)">
    <button class="chip on" data-cat="all">همه (۱۰۰)</button>
    __CHIPS__
  </div>
  <div class="grid" id="grid">
    __TILES__
  </div>
  <p class="count" id="count"></p>
</section>

<section id="features">
  <div class="sec-title"><h2>چرا دنیای بازی‌ها؟</h2></div>
  <div class="feats">
    <div class="feat"><div class="fi">🏛</div><h3>هویت ایرانی</h3><p>رابط کاربری راست‌به‌چپ با فونت وزیرمتن و پالت رنگی الهام‌گرفته از طلایی هخامنشی و فیروزهٔ اصفهان؛ حکم، پاسور، نرد و منقله کنار کلاسیک‌های جهانی.</p></div>
    <div class="feat"><div class="fi">📴</div><h3>کاملاً آفلاین</h3><p>هر بازی یک فایل مستقل است؛ بعد از اولین بازدید، بدون اینترنت هم اجرا می‌شود. هیچ CDN، تبلیغ یا ردیابی وجود ندارد.</p></div>
    <div class="feat"><div class="fi">📱</div><h3>لمسی + کیبورد + ماوس</h3><p>همهٔ بازی‌ها برای هر سه حالت کنترل طراحی شده‌اند؛ روی موبایل دکمه‌های لمسی و سوایپ، روی دسکتاپ کیبورد.</p></div>
    <div class="feat"><div class="fi">🧪</div><h3>منطقِ تست‌شده</h3><p>منطق هر بازی به‌صورت ماژول خالص نوشته شده و با صدها تست واحد (قوانین، لبه‌ها و شبیه‌سازی کامل بازی) اعتبارسنجی شده است.</p></div>
  </div>
</section>

<section id="developers">
  <div class="sec-title"><h2>توسعه‌دهندگان</h2><p>بازی خودت را به پلتفرم اضافه کن</p></div>
  <div class="feats">
    <div class="feat"><div class="fi">📦</div><h3>استاندارد آپلود بازی</h3><p>یک فایل index.html مستقل در ریشهٔ ZIP، مسیرهای نسبی، حداکثر ۵۰ مگابایت فشرده — بدون exe/dll و منابع خارجی. سازگار با sandbox امن.</p></div>
    <div class="feat"><div class="fi">✅</div><h3>بازبینی ادمین</h3><p>بازی آپلودشده پس از تأیید مدیر (از طریق پنل Razor یا ابزارهای MCP) برای عموم فعال می‌شود؛ تضمین کیفیت و امنیت.</p></div>
  </div>
</section>

<section id="mcp">
  <div class="sec-title"><h2>کنترل با MCP</h2><p>پنل مدیریت با پروتکل Model Context Protocol (JSON-RPC 2.0) قابل اتوماسیون است</p></div>
  <div class="mcp-list">
    <code>list_pending_games</code>
    <code>get_game_status</code>
    <code>approve_game</code>
    <code>reject_game</code>
    <code>set_game_enabled</code>
  </div>
</section>

<section id="donate">
  <div class="donate">
    <h2 style="color:var(--gold)">☕ فقط با تشویقت زنده می‌مانیم</h2>
    <p>هیچ تبلیغ و فروشی در کار نیست — تنها درآمد پروژه، حمایت داوطلبانهٔ شماست. درگاه زرین‌پال برای نسخهٔ سرور فعال می‌شود؛ در نسخهٔ Pages می‌توانید پروژه را در گیت‌هاب ستاره بدهید و در گسترشش سهیم شوید.</p>
    <div class="cta-row">
      <a class="btn" href="https://github.com/SSSchangerSSS/world-of-games" rel="noopener">⭐ ستاره در گیت‌هاب</a>
      <a class="btn ghost" href="#games">ادامهٔ بازی</a>
    </div>
  </div>
</section>

<footer>
  دنیای بازی‌ها — ساخته‌شده با ♥ برای گیمرهای فارسی‌زبان ·
  <a href="licenses.html">مجوزها و اعتبارها</a> ·
  <a href="https://github.com/SSSchangerSSS/world-of-games" rel="noopener">گیت‌هاب</a> ·
  <a href="sitemap.xml">نقشهٔ سایت</a>
</footer>

<script>
(function(){
  var TILES = __TILESJSON__;
  var q = document.getElementById('q'), grid = document.getElementById('grid'), count = document.getElementById('count');
  var cat = 'all';
  var chips = document.querySelectorAll('.chip');
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(x){x.classList.remove('on')});c.classList.add('on');cat=c.getAttribute('data-cat');apply();
  });});
  q.addEventListener('input',apply);
  function apply(){
    var s=q.value.trim(), shown=0;
    TILES.forEach(function(t){
      var ok=(cat==='all'||t.cat===cat)&&(!s||t.title.indexOf(s)>=0||t.desc.indexOf(s)>=0);
      var el=document.getElementById('tile-'+t.slug);
      if(el){el.style.display=ok?'':'none';if(ok)shown++;}
    });
    count.textContent='نمایش '+shown.toLocaleString('fa-IR')+' بازی از ۱۰۰';
  }
  apply();
})();
</script>
</body>
</html>
"""

TILE = """<a class="tile" id="tile-{slug}" href="games/{slug}/" data-cat="{cat}">
  <div class="ico" style="background:linear-gradient(140deg,{g1},{g2})">{icon}</div>
  <h3>{title}</h3>
  <p>{desc}</p>
  <span class="cat" style="color:{ccolor};border-color:{ccolor}">{catlabel}</span>
</a>"""

LICENSES = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مجوزها و اعتبارها — دنیای بازی‌ها</title>
<meta name="description" content="مجوزها و اعتبارهای مجموعه ۱۰۰ بازی دنیای بازی‌ها">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>__CSS__</style>
</head>
<body>
<nav class="nav"><div class="brand">دنیای <span>بازی‌ها</span> ❋</div>
<div class="links"><a href="index.html">خانه</a><a href="index.html#games">بازی‌ها</a></div>
<a class="btn ghost" style="padding:8px 18px;font-size:.85rem" href="index.html">بازگشت</a></nav>
<main class="lic">
  <h1>مجوزها و اعتبارها</h1>
  <p>تمام ۱۰۰ بازی این مجموعه <b>از پایه و به‌صورت اختصاصی</b> برای «دنیای بازی‌ها» نوشته شده‌اند؛ هیچ کد یا دارایی گرافیکی از پروژه‌های ثالث کپی نشده است. قواعد بازی‌های کلاسیک (شطرنج، نرد، سولیتر، سودوکو، مار، پینگ‌پنگ و…) مالکیت خصوصی ندارند و به‌عنوان میراث مشترک بازی‌ها آزادانه قابل پیاده‌سازی‌اند.</p>

  <h2>کد ثالث</h2>
  <p>تنها مؤلفهٔ ثالثِ مستعار، موتور قوانین شطرنج است:</p>
  <table>
    <tr><th>مؤلفه</th><th>استفاده</th><th>مجوز</th><th>منبع</th></tr>
    <tr><td>chess.js ۰.۱۰.۳</td><td>اعتبارسنجی حرکات شطرنج در بازی «شطرنج»</td><td>BSD-2-Clause</td><td>github.com/jhlywa/chess.js (Jeff Hlywa و مشارکت‌کنندگان)</td></tr>
  </table>
  <p>متن کامل مجوز در <code>games/chess/LICENSE-chessjs.txt</code> و یادداشت اعتبار در <code>games/chess/CREDITS.md</code> موجود است.</p>

  <h2>الهام‌های طراحی (فقط مکانیک، بدون کد)</h2>
  <ul>
    <li><b>آجرچین (تتریس‌گونه)، ۲۰۴۸، مین‌یاب، سوکوبان، رمزنگار (مسترمایند)، سیمون، واژه‌یاب (وردل‌گونه):</b> مکانیک‌های عمومی و شناخته‌شده که با پیاده‌سازی کاملاً اورجینال بازآفرینی شده‌اند. نام‌های تجاری مربوط به دارندگان خودشان است و این پروژه وابستگی به آن‌ها ندارد.</li>
    <li><b>سولیتر خانوادهٔ کلایک/عنکبوت/فری‌سل/هرم/سه‌قله/گلف/ساعت:</b> قواعد سنتی پازل‌های کارتی که مالکیت خصوصی ندارند.</li>
    <li><b>نرد، حکم، پاسور، منقله، مار و پله، لیدو، بازی سلطنتی اور:</b> بازی‌های سنتی و تاریخی با قواعد در دسترس عموم.</li>
    <li><b>کلاسیک‌های آرکید (مار، پینگ‌پنگ، توپ‌شکن، تهاجم فضایی، سیارک‌ها، قورباغهٔ عبوری):</b> بازآفرینی مفاهیم دهه‌های ۷۰-۸۰ با کد و گرافیک اورجینال.</li>
  </ul>

  <h2>دارایی‌ها</h2>
  <ul>
    <li>فونت <b>وزیرمتن</b> — طراحی صابر راستی‌کردار — مجوز آزاد (OFL) · میزبانی خودکار در همین مخزن.</li>
    <li>کدها، کاورها و آیکون‌های SVG و متن‌های فارسی این سایت: اثر اختصاصی پروژه «دنیای بازی‌ها».</li>
  </ul>

  <h2>سورس باز</h2>
  <p class="ok">✔ کل پلتفرم (بک‌اند .NET، پنل مدیریت Razor، ابزارهای MCP، استاندارد آپلود بازی و همین مجموعه بازی‌ها) به‌صورت عمومی در گیت‌هاب نگهداری می‌شود و خوشحال می‌شویم در بهبودش مشارکت کنید.</p>
</main>
<footer>دنیای بازی‌ها · <a href="index.html">بازگشت به خانه</a></footer>
</body>
</html>
"""


def render(out_dir, tiles):
    chips = []
    for cat, label in CAT_LABEL.items():
        n = sum(1 for t in tiles if t["cat"] == cat)
        chips.append('<button class="chip" data-cat="%s">%s (%s)</button>' % (cat, label, str(n).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))))
    tile_html = []
    for t in tiles:
        g1 = CAT_COLOR.get(t["cat"], "#d9a441")
        tile_html.append(TILE.format(slug=html.escape(t["slug"]), cat=t["cat"], icon=t["icon"],
                                     title=html.escape(t["title"]), desc=html.escape(t["desc"]),
                                     g1=g1, g2="#22304f", ccolor=CAT_COLOR.get(t["cat"], "#d9a441"),
                                     catlabel=CAT_LABEL[t["cat"]]))
    itemlist = [{"type": "ListItem", "position": i + 1, "name": t["title"],
                 "url": "https://ssschangersss.github.io/world-of-games/games/%s/" % t["slug"]}
                for i, t in enumerate(tiles)]
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "ItemList",
                         "name": "بازی‌های دنیای بازی‌ها", "numberOfItems": len(tiles),
                         "itemListElement": itemlist}, ensure_ascii=False)
    page = (TPL.replace('__CSS__', CSS)
               .replace('__JSONLD__', jsonld)
               .replace('__CHIPS__', "\n    ".join(chips))
               .replace('__TILES__', "\n    ".join(tile_html))
               .replace('__TILESJSON__', json.dumps(tiles, ensure_ascii=False)))
    with io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    lic = LICENSES.replace("{css}", CSS)
    with io.open(os.path.join(out_dir, "licenses.html"), "w", encoding="utf-8") as f:
        f.write(lic)
    return True
