# -*- coding: utf-8 -*-
"""WOG 100-games build library — Design System v2 ("Zartosht" theme).
Every new game = ONE self-contained index.html following games-spec.md:
RTL, offline, sandbox-safe (store shim), no emoji in game UI, Vazirmatn tokens.
Back-to-home button is injected by this template (user requirement).
Testable logic: every game defines `var WOG_LOGIC = {...}` (pure, DOM-free)
between WOG_LOGIC markers so Node tests can run it standalone.

v2: per-game identity colors (g1/g2) injected as CSS vars, layered scene
backgrounds per category, Persian girih pattern, upgraded cards/boards/
buttons/overlays. All class contracts from v1 preserved.
"""
import re
try:
    from themes import THEMES
except ImportError:
    from .themes import THEMES

CATS = {
    "board":  "تخته و استراتژی",
    "cards":  "بازی‌های کارتی",
    "puzzle": "پازل و فکری",
    "arcade": "اکشن و مهارتی",
    "word":   "واژه و دانش",
    "luck":   "شانس و سرگرمی",
}

def _hex2rgba(h, a):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "rgba(%d,%d,%d,%.2f)" % (r, g, b, a)

# Persian girih-style eight-point star lattice (gold, very subtle)
GIRIH_SVG = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='72' height='72' viewBox='0 0 72 72'%3E"
             "%3Cg fill='none' stroke='%23d9a441' stroke-opacity='0.07' stroke-width='1'%3E"
             "%3Cpath d='M36 6l8 14 16-2-2 16 14 8-14 8 2 16-16-2-8 14-8-14-16 2 2-16-14-8 14-8-2-16 16 2z'/%3E"
             "%3Ccircle cx='36' cy='36' r='10'/%3E%3C/g%3E%3C/svg%3E")
# starfield (tiny white dots) for arcade scene
STARS_SVG = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E"
             "%3Cg fill='%23ffffff'%3E"
             "%3Ccircle cx='14' cy='18' r='1'/%3Ccircle cx='64' cy='8' r='0.7'/%3Ccircle cx='102' cy='32' r='1.2'/%3E"
             "%3Ccircle cx='38' cy='52' r='0.8'/%3Ccircle cx='88' cy='72' r='1'/%3Ccircle cx='10' cy='88' r='0.7'/%3E"
             "%3Ccircle cx='56' cy='106' r='1.1'/%3Ccircle cx='112' cy='112' r='0.6'/%3E%3C/g%3E%3C/svg%3E")

BASE_CSS = """*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
@font-face{font-family:Vazirmatn;src:url(../../fonts/Vazirmatn-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:Vazirmatn;src:url(../../fonts/Vazirmatn-Bold.woff2) format('woff2');font-weight:700;font-display:swap}
:root{--gold:#d9a441;--gold2:#e8c073;--turq:#3fb8af;--ink:#f3ead8;--dim:#a8b3c9;--panel:#131f38;--panel2:#0f1930}
html{height:100%}
body{font-family:Vazirmatn,Tahoma,sans-serif;color:var(--ink);min-height:100dvh;user-select:none;display:flex;flex-direction:column;align-items:center;padding:14px;padding-top:64px;overflow-x:hidden;position:relative;
background:
 radial-gradient(900px 420px at 50% -80px,var(--g1a),transparent 68%),
 radial-gradient(720px 480px at 108% 112%,var(--g2a),transparent 60%),
 radial-gradient(560px 320px at -8% 96%,var(--g1a),transparent 62%),
 linear-gradient(168deg,#111c33 0%,#0b1220 58%,#0a0f1d 100%);
background-attachment:fixed}
body:before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;background-image:url("__GIRIH__");background-size:72px 72px}
body:after{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(120% 90% at 50% 30%,transparent 55%,rgba(4,7,14,.55) 100%)}
a.wog-home,header,#app,#hint,.wog-toast,.wovl{position:relative;z-index:1}
a.wog-home{position:fixed;top:12px;inset-inline-start:14px;z-index:99;display:inline-flex;align-items:center;gap:6px;background:linear-gradient(140deg,rgba(217,164,65,.16),rgba(217,164,65,.06));border:1px solid rgba(217,164,65,.5);color:#e8c073;text-decoration:none;padding:7px 14px;border-radius:12px;font-size:.85rem;font-weight:700;box-shadow:0 2px 10px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.06);transition:.18s}
a.wog-home:hover{background:rgba(217,164,65,.3);transform:translateY(-1px)}
header{text-align:center;margin-bottom:12px;width:100%;max-width:720px}
h1{font-size:1.3rem;font-weight:800;letter-spacing:.2px;display:inline-flex;align-items:center;gap:10px;
background:linear-gradient(180deg,#f6d996,var(--g1c,#e8c073) 55%,var(--g1));-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 8px rgba(217,164,65,.22))}
h1:before,h1:after{content:'❋';font-size:.85em;color:var(--g1b);-webkit-text-fill-color:var(--g1b)}
.hud{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:8px;color:var(--dim);font-size:.88rem;min-height:1.4em}
.hud b{color:var(--gold2);font-weight:700}
#hint{color:#96a2ba;font-size:.85rem;margin-top:12px;text-align:center;max-width:660px;line-height:2}
button,.wbtn{font-family:inherit;background:linear-gradient(180deg,#e9bd68,#c8922f);color:#251905;border:0;border-radius:12px;font-weight:800;padding:9px 18px;font-size:.95rem;cursor:pointer;touch-action:manipulation;box-shadow:0 3px 10px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.35),0 0 0 1px rgba(217,164,65,.4);transition:transform .12s,box-shadow .15s,filter .15s}
button:hover,.wbtn:hover{filter:brightness(1.06)}
button:active,.wbtn:active{transform:translateY(1px) scale(.985);box-shadow:0 1px 4px rgba(0,0,0,.4)}
button.sec,.wbtn.sec{background:linear-gradient(180deg,#1a2745,#121d36);color:var(--ink);border:1px solid rgba(217,164,65,.4);box-shadow:0 2px 8px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.05)}
button:disabled{opacity:.4;cursor:default;transform:none}
.wpanel{background:linear-gradient(180deg,rgba(23,35,63,.92),rgba(15,25,48,.92));border:1px solid rgba(217,164,65,.35);border-radius:16px;padding:14px;box-shadow:0 6px 24px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.05)}
.wrow{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;align-items:center;margin:8px 0}
.wovl{position:fixed;inset:0;background:rgba(5,8,16,.72);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);display:flex;align-items:center;justify-content:center;z-index:90;animation:wogfade .22s ease}
@keyframes wogfade{from{opacity:0}to{opacity:1}}
.wovl .box{background:linear-gradient(180deg,#182646,#101a30);border:1px solid rgba(217,164,65,.55);border-radius:20px;padding:26px 30px;text-align:center;max-width:88vw;box-shadow:0 20px 60px rgba(0,0,0,.6),0 0 0 1px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.07);animation:wogpop .26s cubic-bezier(.2,1.4,.4,1)}
@keyframes wogpop{from{transform:scale(.82);opacity:0}to{transform:scale(1);opacity:1}}
.wovl h2{color:var(--gold2);margin-bottom:8px;font-size:1.35rem;text-shadow:0 0 18px rgba(217,164,65,.35)}
.wovl p{color:var(--dim);margin-bottom:16px;line-height:2}
.wog-toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(20,32,58,.94);border:1px solid rgba(217,164,65,.55);color:var(--ink);padding:9px 20px;border-radius:14px;opacity:0;transition:.25s;z-index:95;pointer-events:none;font-size:.9rem;box-shadow:0 8px 24px rgba(0,0,0,.5)}
.wog-toast.on{opacity:1}
.wgrid{display:grid;border-radius:12px;overflow:hidden;direction:ltr;touch-action:manipulation;border:2px solid rgba(217,164,65,.55);outline:1px solid rgba(0,0,0,.6);box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 0 5px rgba(23,35,63,.85),0 0 0 6px rgba(217,164,65,.25),inset 0 0 0 1px rgba(0,0,0,.35)}
.wgrid .cell{display:flex;align-items:center;justify-content:center;cursor:pointer;position:relative;transition:filter .12s}
.cell.light{background:linear-gradient(145deg,#f0e5cb,#dccfae)}
.cell.dark{background:linear-gradient(145deg,#3d4e77,#2c3a5c)}
.wgrid .cell:hover{filter:brightness(1.1)}
.wcard{display:inline-flex;flex-direction:column;justify-content:space-between;width:54px;height:76px;background:linear-gradient(160deg,#fdf9ee,#efe6cf);color:#1c2438;border-radius:8px;padding:4px 6px;font-weight:800;font-size:.92rem;line-height:1;box-shadow:0 3px 7px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,255,255,.6),inset 0 0 0 2px rgba(28,36,56,.08);cursor:pointer;touch-action:manipulation;flex:none;transition:transform .14s,box-shadow .14s}
.wcard:hover{transform:translateY(-2px)}
.wcard.red{color:#bf2f3a}
.wcard.back{background:linear-gradient(150deg,#31406b,#1d2a4a 55%,#2a3a63);border:1px solid rgba(217,164,65,.55)}
.wcard.back:before{content:'❋';color:rgba(232,192,115,.6);align-self:center;font-size:1.35rem;text-shadow:0 0 8px rgba(217,164,65,.4)}
.wcard.small{width:40px;height:57px;font-size:.78rem;border-radius:6px}
.wcard.tiny{width:31px;height:46px;font-size:.68rem;border-radius:5px;padding:2px 3px}
.wcard.sel{outline:3px solid var(--gold2);transform:translateY(-7px);box-shadow:0 10px 22px rgba(0,0,0,.5),0 0 18px rgba(232,192,115,.4)}
.wcard .cn{font-size:.72rem;opacity:.9}.wcard .cv{align-self:flex-start;opacity:.95}
.wcard.back .cn,.wcard.back .cv{display:none}
.wdpad{display:none;grid-template-columns:repeat(3,60px);grid-auto-rows:52px;gap:7px;margin-top:12px}
.wdpad.on{display:grid}
.wdpad button{font-size:1.15rem;border-radius:14px}
@media(pointer:coarse){.wdpad{display:grid}}
canvas{touch-action:none;border-radius:14px;background:#0d1526;box-shadow:0 12px 36px rgba(0,0,0,.55),0 0 0 2px rgba(217,164,65,.4),0 0 0 6px rgba(15,22,40,.9),0 0 26px rgba(217,164,65,.12)}
"""

# Category-scoped scene CSS (body[data-cat])
CAT_CSS = {
"board": """body[data-cat="board"]{background:
 radial-gradient(820px 380px at 50% -60px,var(--g1a),transparent 66%),
 radial-gradient(680px 460px at 110% 114%,var(--g2a),transparent 58%),
 linear-gradient(168deg,#131e35,#0b1220 60%,#0a0e1a)}
body[data-cat="board"]:before{background-image:url("__GIRIH__");background-size:84px 84px;opacity:.55}""",
"cards": """body[data-cat="cards"]{background:
 radial-gradient(1100px 520px at 50% 118%,rgba(28,92,84,.4),transparent 62%),
 radial-gradient(760px 380px at 50% -100px,var(--g1a),transparent 68%),
 linear-gradient(170deg,#0f2230,#0b1420 55%,#0a101a)}
body[data-cat="cards"]:after{background:radial-gradient(90% 70% at 50% 38%,transparent 52%,rgba(2,8,10,.6) 100%)}""",
"puzzle": """body[data-cat="puzzle"]{background:
 radial-gradient(880px 420px at 16% -70px,var(--g1a),transparent 64%),
 radial-gradient(720px 480px at 104% 110%,var(--g2a),transparent 60%),
 linear-gradient(165deg,#131a33,#0b1220 58%,#0a0f1c)}
body[data-cat="puzzle"]:before{opacity:.35}""",
"arcade": """body[data-cat="arcade"]{background:
 radial-gradient(880px 400px at 50% -90px,var(--g1a),transparent 66%),
 radial-gradient(700px 460px at 106% 112%,var(--g2a),transparent 58%),
 linear-gradient(180deg,#0a1024,#080d1b 52%,#060a15)}
body[data-cat="arcade"]:before{background-image:url("__STARS__");background-size:130px 130px;opacity:.8}
body[data-cat="arcade"]:after{background:radial-gradient(130% 84% at 50% 118%,var(--g2a),transparent 55%)}""",
"word": """body[data-cat="word"]{background:
 radial-gradient(900px 420px at 84% -70px,var(--g1a),transparent 64%),
 radial-gradient(680px 420px at -6% 106%,var(--g2a),transparent 58%),
 linear-gradient(166deg,#171c2e,#0e1220 56%,#0b0e18)}
body[data-cat="word"]:before{background-image:url("__GIRIH__");background-size:96px 96px;opacity:.3}""",
"luck": """body[data-cat="luck"]{background:
 radial-gradient(1000px 500px at 50% 120%,rgba(84,32,66,.45),transparent 62%),
 radial-gradient(760px 400px at 50% -100px,var(--g1a),transparent 66%),
 linear-gradient(168deg,#181428,#100c1c 55%,#0c0916)}
body[data-cat="luck"]:before{opacity:.45}""",
}

COMMON_JS = """function $(s){return document.querySelector(s)}
function $$(s){return Array.prototype.slice.call(document.querySelectorAll(s))}
function ce(tag,cls,html){var e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;return e}
var FA_D='۰۱۲۳۴۵۶۷۸۹';
function fa(n){return String(n).replace(/\\d/g,function(d){return FA_D[+d]})}
function shuffle(a,rng){a=a.slice();rng=rng||Math.random;for(var i=a.length-1;i>0;i--){var j=Math.floor(rng()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
function rint(a,b,rng){rng=rng||Math.random;return a+Math.floor(rng()*(b-a+1))}
function pick(arr,rng){rng=rng||Math.random;return arr[Math.floor(rng()*arr.length)]}
function clamp(v,a,b){return v<a?a:v>b?b:v}
var _toastT=0;
function toast(msg,ms){var t=$('#wog-toast');if(!t)return;t.textContent=msg;t.classList.add('on');clearTimeout(_toastT);_toastT=setTimeout(function(){t.classList.remove('on')},ms||1800)}
function hud(html){var h=$('#hud');if(h)h.innerHTML=html}
function ovl(title,sub,btn,cb){var o=ce('div','wovl');var b=ce('div','box');b.appendChild(ce('h2',null,title));if(sub)b.appendChild(ce('p',null,sub));var bt=ce('button',null,btn);bt.setAttribute('data-smoke','');bt.addEventListener('click',function(){o.remove();cb&&cb()});b.appendChild(bt);o.appendChild(b);document.body.appendChild(o);return o}
function bestOf(key,val){var b=parseInt(store.get(key)||'0',10)||0;if(val>b)store.set(key,String(val));return Math.max(b,val)}
function storeBest(key){return parseInt(store.get(key)||'0',10)||0}
"""

CARD_JS = """var SUITS='♠♥♦♣';
function makeDeck(){var d=[];for(var s=0;s<4;s++)for(var r=1;r<=13;r++)d.push({s:s,r:r});return d}
function isRed(c){return c.s===1||c.s===2}
function suitOf(c){return SUITS[c.s]}
function rankShort(r){return r===1?'A':r===11?'J':r===12?'Q':r===13?'K':String(r)}
function rankFa(r){return r===1?'آس':r===11?'سرباز':r===12?'بی‌بی':r===13?'شاه':fa(r)}
function cardEl(c,faceUp,size){var e=ce('div','wcard'+(faceUp?(isRed(c)?' red':''):' back')+(size?' '+size:''));if(faceUp)e.innerHTML='<span class="cn">'+rankShort(c.r)+suitOf(c)+'</span><span class="cv">'+suitOf(c)+'</span>';return e}
function cardStack(el,cs,faceUp,size){cs.forEach(function(c){el.appendChild(cardEl(c,faceUp,size))});return el}
"""

ARCADE_JS = """function makeCanvas(w,h){var cv=document.createElement('canvas');cv.width=w;cv.height=h;cv.style.width='min(96vw,'+w+'px)';cv.style.height='auto';document.getElementById('app').appendChild(cv);return{cv:cv,ctx:cv.getContext('2d'),w:w,h:h}}
function keyState(){var k={};addEventListener('keydown',function(e){k[e.code]=1;if(/^(Arrow|Space)/.test(e.code))e.preventDefault()});addEventListener('keyup',function(e){k[e.code]=0});return k}
function bindPad(defs){var d=ce('div','wdpad');var grid={};defs.forEach(function(x){grid[x.k]=x});var cell=function(k){var b;if(k&&grid[k]){b=ce('button',null,grid[k].label);b.setAttribute('data-k',k)}else{b=ce('span');b.style.visibility='hidden'}d.appendChild(b)};cell(defs.length>2?defs[1].k:null);defs.forEach(function(x){cell(x.k)});cell(null);document.getElementById('app').appendChild(d);$$('[data-k]').forEach(function(b){var k=b.getAttribute('data-k');function on(e){e.preventDefault();ks[k]=1}function off(e){e.preventDefault();ks[k]=0}b.addEventListener('touchstart',on,{passive:false});b.addEventListener('touchend',off);b.addEventListener('mousedown',on);b.addEventListener('mouseup',off);b.addEventListener('mouseleave',off)})}
function rafStep(fn){var last=performance.now();function f(t){var dt=Math.min(.05,(t-last)/1000);last=t;fn(dt);requestAnimationFrame(f)}requestAnimationFrame(f)}
"""

WORD_JS = """var FA_LETTERS=['آ','ا','ب','پ','ت','ث','ج','چ','ح','خ','د','ذ','ر','ز','ژ','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ک','گ','ل','م','ن','و','ه','ی'];
function normFa(s){return (s||'').replace(/ي/g,'ی').replace(/ك/g,'ک').replace(/\\u200c/g,' ').replace(/\\s+/g,' ').trim()}
function faKb(onKey,longKeys){var kb=ce('div');kb.style.cssText='display:flex;flex-wrap:wrap;gap:5px;justify-content:center;max-width:560px;margin-top:12px;direction:rtl';FA_LETTERS.forEach(function(ch){var b=ce('button','sec',ch);b.style.cssText='min-width:40px;padding:8px 4px';b.addEventListener('click',function(){onKey(ch)});kb.appendChild(b)});var lk=(longKeys&&longKeys.length&&typeof longKeys.forEach==='function')?longKeys:[];lk.forEach(function(x){var b=ce('button',null,x.label);b.addEventListener('click',function(){onKey(x.k)});kb.appendChild(b)});document.getElementById('app').appendChild(kb);return kb}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<meta name="theme-color" content="#0b1220">
<title>{title} | دنیای بازی‌ها</title>
<meta name="description" content="{desc}">
<style>{base_css}{cat_css}{css}
</style>
</head>
<body data-cat="{cat}" data-slug="{slug}" style="--g1:{g1};--g2:{g2};--g1a:{g1a};--g2a:{g2a};--g1b:{g1b}">
<a class="wog-home" href="../../index.html">⌂ خانه</a>
<header><h1>{title}</h1><div class="hud" id="hud"></div></header>
<div id="app"></div>
<p id="hint"></p>
<div class="wog-toast" id="wog-toast"></div>
<script>
(function () {{
'use strict';
var store = {{
  get: function (k) {{ try {{ return localStorage.getItem(k); }} catch (e) {{ return null; }} }},
  set: function (k, v) {{ try {{ localStorage.setItem(k, v); }} catch (e) {{}} }}
}};
/*WOG_LOGIC_START*/
{logic}
/*WOG_LOGIC_END*/
var L = WOG_LOGIC;
{ui}
}})();
</script>
</body>
</html>
"""


class G(object):
    def __init__(self, slug, title, cat, icon, g1, g2, desc, hint,
                 logic="", ui="", css="", engines=(), tests=None, seed=12345):
        assert slug and re.match(r'^[a-z0-9\-]+$', slug), slug
        assert cat in CATS, (slug, cat)
        self.slug = slug; self.title = title; self.cat = cat; self.icon = icon
        self.g1 = g1; self.g2 = g2; self.desc = desc; self.hint = hint
        self.logic = logic.strip(); self.ui = ui.strip(); self.css = css.strip()
        self.engines = list(engines); self.tests = tests or []; self.seed = seed

    def render(self):
        engines = {"common": COMMON_JS, "card": CARD_JS, "arcade": ARCADE_JS, "word": WORD_JS}
        js = "".join(engines[e] for e in self.engines) if self.engines else COMMON_JS
        if not self.logic:
            raise ValueError("game %s has no logic" % self.slug)
        if "WOG_LOGIC" not in self.logic:
            raise ValueError("game %s logic must define WOG_LOGIC" % self.slug)
        if "localStorage" in self.ui or "localStorage" in self.logic:
            raise ValueError("game %s must use store, not localStorage directly" % self.slug)
        base_css = BASE_CSS.replace("__GIRIH__", GIRIH_SVG).replace("__STARS__", STARS_SVG)
        cat_css = CAT_CSS.get(self.cat, "").replace("__GIRIH__", GIRIH_SVG).replace("__STARS__", STARS_SVG)
        theme_extra = THEMES.get(self.slug, "")
        return TEMPLATE.format(
            title=self.title, desc=self.desc.replace('"', "'"),
            cat=self.cat, slug=self.slug,
            g1=self.g1, g2=self.g2,
            g1a=_hex2rgba(self.g1, 0.30), g2a=_hex2rgba(self.g2, 0.42), g1b=self.g2,
            base_css=base_css, cat_css=cat_css, css=self.css + "\n" + theme_extra,
            logic=self.logic, ui=js + "\n" + self.ui)

    def logic_export(self):
        return self.logic


def check_spec_violations(html, slug):
    """Return list of spec violations for a rendered game html."""
    errs = []
    stripped = re.sub(r'data:[a-z]+/[a-z+.-]+[,;][^"]*', '', html)  # strip whole data URI (double-quoted)
    if re.search(r'https?://', stripped):
        errs.append("%s: contains http(s) URL" % slug)
    for bad in ["alert(", "confirm(", "prompt(", "document.cookie", "window.top", "window.parent", "fetch(", "XMLHttpRequest"]:
        if bad in html:
            errs.append("%s: forbidden token %r" % (slug, bad))
    if "localStorage" in html:
        allowed = html.count("localStorage")
        shim_uses = len(re.findall(r'localStorage\.(getItem|setItem)', html))
        if allowed > shim_uses:
            errs.append("%s: direct localStorage use outside shim" % slug)
        if re.search(r'localStorage\s*\[', html):
            errs.append("%s: bracket localStorage access" % slug)
    return errs
