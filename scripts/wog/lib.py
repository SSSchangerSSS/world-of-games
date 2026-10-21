# -*- coding: utf-8 -*-
"""WOG 100-games build library.
Every new game = ONE self-contained index.html following games-spec.md:
RTL, offline, sandbox-safe (store shim), no emoji in game UI, Vazirmatn tokens.
Back-to-home button is injected by this template (user requirement).
Testable logic: every game defines `var WOG_LOGIC = {...}` (pure, DOM-free)
between WOG_LOGIC markers so Node tests can run it standalone.
"""
import re

CATS = {
    "board":  "تخته و استراتژی",
    "cards":  "بازی‌های کارتی",
    "puzzle": "پازل و فکری",
    "arcade": "اکشن و مهارتی",
    "word":   "واژه و دانش",
    "luck":   "شانس و سرگرمی",
}

BASE_CSS = """*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
@font-face{font-family:Vazirmatn;src:url(../../fonts/Vazirmatn-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:Vazirmatn;src:url(../../fonts/Vazirmatn-Bold.woff2) format('woff2');font-weight:700;font-display:swap}
body{font-family:Vazirmatn,Tahoma,sans-serif;background:linear-gradient(160deg,#101a2e,#0b1220);color:#f3ead8;min-height:100dvh;user-select:none;display:flex;flex-direction:column;align-items:center;padding:12px;padding-top:56px;overflow-x:hidden}
a.wog-home{position:fixed;top:10px;inset-inline-start:12px;z-index:99;background:rgba(217,164,65,.12);border:1px solid rgba(217,164,65,.45);color:#e8c073;text-decoration:none;padding:6px 12px;border-radius:10px;font-size:.85rem;font-weight:700}
a.wog-home:hover{background:rgba(217,164,65,.3)}
header{text-align:center;margin-bottom:8px}
h1{font-size:1.2rem;color:#d9a441}
.hud{color:#a8b3c9;font-size:.9rem;margin-top:2px;min-height:1.4em}
.hud b{color:#e8c073}
button,.wbtn{font-family:inherit;background:#d9a441;color:#221806;border:0;border-radius:10px;font-weight:700;padding:8px 16px;font-size:.95rem;cursor:pointer;touch-action:manipulation}
button.sec,.wbtn.sec{background:#14203a;color:#f3ead8;border:1px solid rgba(217,164,65,.35)}
button:disabled{opacity:.45;cursor:default}
#hint{color:#a8b3c9;font-size:.85rem;margin-top:10px;text-align:center;max-width:680px;line-height:1.9}
.wpanel{background:#14203a;border:1px solid rgba(217,164,65,.35);border-radius:14px;padding:14px}
.wrow{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;align-items:center;margin:8px 0}
.wovl{position:fixed;inset:0;background:rgba(5,9,18,.85);display:flex;align-items:center;justify-content:center;z-index:90}
.wovl .box{background:#14203a;border:2px solid rgba(217,164,65,.5);border-radius:16px;padding:22px 28px;text-align:center;max-width:88vw}
.wovl h2{color:#e8c073;margin-bottom:8px}
.wovl p{color:#a8b3c9;margin-bottom:14px}
.wog-toast{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#14203a;border:1px solid rgba(217,164,65,.5);color:#f3ead8;padding:8px 18px;border-radius:12px;opacity:0;transition:.25s;z-index:95;pointer-events:none;font-size:.9rem}
.wog-toast.on{opacity:1}
.wgrid{display:grid;border:2px solid rgba(217,164,65,.5);border-radius:10px;overflow:hidden;direction:ltr;touch-action:manipulation}
.wgrid .cell{display:flex;align-items:center;justify-content:center;cursor:pointer;position:relative}
.cell.light{background:#e8dcc0}.cell.dark{background:#41527a}
.wcard{display:inline-flex;flex-direction:column;justify-content:space-between;width:52px;height:74px;background:#f6efe0;color:#1c2438;border-radius:7px;padding:3px 5px;font-weight:700;font-size:.9rem;line-height:1;box-shadow:0 2px 5px rgba(0,0,0,.45);cursor:pointer;touch-action:manipulation;flex:none}
.wcard.red{color:#c0392b}
.wcard.back{background:linear-gradient(135deg,#2c3a5e,#41527a);border:2px solid rgba(217,164,65,.5)}
.wcard.back:before{content:'❋';color:rgba(232,192,115,.55);align-self:center;font-size:1.3rem}
.wcard.small{width:38px;height:54px;font-size:.75rem;border-radius:5px}
.wcard.tiny{width:30px;height:44px;font-size:.65rem;border-radius:4px;padding:2px 3px}
.wcard.sel{outline:3px solid #e8c073;transform:translateY(-6px)}
.wcard .cn{font-size:.7rem;opacity:.85}.wcard .cv{align-self:flex-start}
.wcard.back .cn,.wcard.back .cv{display:none}
.wdpad{display:none;grid-template-columns:repeat(3,58px);grid-auto-rows:50px;gap:6px;margin-top:12px}
.wdpad.on{display:grid}
.wdpad button{font-size:1.15rem}
@media(pointer:coarse){.wdpad{display:grid}}
canvas{touch-action:none;border-radius:10px;border:2px solid rgba(217,164,65,.35);background:#0d1526}
"""

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
<title>{title} | دنیای بازی‌ها</title>
<meta name="description" content="{desc}">
<style>{base_css}{css}
</style>
</head>
<body>
<a class="wog-home" href="../../index.html">⌂ خانه</a>
<header><h1>❋ {title} ❋</h1><div class="hud" id="hud"></div></header>
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
        return TEMPLATE.format(
            title=self.title, desc=self.desc.replace('"', "'"),
            base_css=BASE_CSS, css=self.css, logic=self.logic, ui=js + "\n" + self.ui)

    def logic_export(self):
        return self.logic


def check_spec_violations(html, slug):
    """Return list of spec violations for a rendered game html."""
    errs = []
    if re.search(r'https?://', html):
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
