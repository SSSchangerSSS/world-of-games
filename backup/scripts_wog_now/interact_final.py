# -*- coding: utf-8 -*-
"""Final universal QA: buttons + ALL pointer elements + canvas animation diff.
Flags games where NOTHING reacts (DOM & canvas both static).
Usage: python3 interact_final.py <site-root> <port>
"""
import sys, os, json, time
from playwright.sync_api import sync_playwright

root, port = sys.argv[1], int(sys.argv[2])
site = "http://127.0.0.1:%d" % port
only = sys.argv[3].split(",") if len(sys.argv) > 3 else None

JS_POINTS = """() => {
  const app = document.getElementById('app') || document.body;
  const out = [];
  const seen = new Set();
  const push = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width < 16 || r.height < 16 || r.width > window.innerWidth + 2) return;
    const key = Math.round(r.x / 8) + ':' + Math.round(r.y / 8) + ':' + Math.round(r.width / 8);
    if (seen.has(key)) return; seen.add(key);
    out.push({x: r.x + Math.min(r.width / 2, 30), y: r.y + r.height / 2});
  };
  // buttons first (most meaningful)
  app.querySelectorAll('button').forEach(push);
  // pointer-cursor elements, deepest-first: leaves then parents
  const all = [...app.querySelectorAll('*')];
  all.sort((a, b) => (b.compareDocumentPosition(a) & Node.DOCUMENT_POSITION_CONTAINED_BY) ? -1 : 1);
  for (const el of all) {
    if (el.tagName === 'BUTTON' || el.tagName === 'CANVAS') continue;
    try { if (getComputedStyle(el).cursor === 'pointer') push(el); } catch (e) {}
    if (out.length >= 50) break;
  }
  return out.slice(0, 50);
}"""

CANVAS_DIFF = """async () => {
  const cvs = [...document.querySelectorAll('canvas')];
  if (!cvs.length) return null;
  const cv = cvs[0];
  const grab = () => { try { const c = document.createElement('canvas');
    c.width = 40; c.height = 40;
    c.getContext('2d').drawImage(cv, 0, 0, 40, 40);
    return c.toDataURL(); } catch (e) { return 'err'; } };
  const a = grab();
  await new Promise(r => setTimeout(r, 500));
  const b = grab();
  await new Promise(r => setTimeout(r, 500));
  const c = grab();
  return {changed: a !== b || b !== c};
}"""

results = []
OUT = "/home/z/my-project/final_qa.json"
def save():
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)

with sync_playwright() as p:
    browser = p.chromium.launch()
    games_root = os.path.join(root, "games")
    slugs = sorted(d for d in os.listdir(games_root) if os.path.isdir(os.path.join(games_root, d)))
    if only: slugs = [s for s in slugs if s in only]
    for slug in slugs:
        errs = []
        pg = browser.new_page(viewport={"width": 430, "height": 880})
        pg.on("pageerror", lambda e, _e=errs: _e.append("PAGEERROR: " + str(e)[:170]))
        try:
            pg.goto("%s/games/%s/" % (site, slug), wait_until="load", timeout=14000)
            pg.wait_for_timeout(300)
            sm = pg.locator("[data-smoke]")
            if sm.count() > 0:
                try: sm.first.click(timeout=1100)
                except Exception: pass
                pg.wait_for_timeout(400)
            state_key = "document.getElementById('app') ? document.getElementById('app').innerHTML : document.body.innerHTML"
            s0 = pg.evaluate(state_key)
            pts = pg.evaluate(JS_POINTS)[:30]
            reacts = 0
            for pt in pts:
                try: pg.mouse.click(pt["x"], pt["y"]); pg.wait_for_timeout(420)
                except Exception: pass
                s1 = pg.evaluate(state_key)
                if s1 != s0:
                    reacts += 1
                    s0 = s1
                # dismiss overlays so we can keep interacting
                sm2 = pg.locator("[data-smoke]")
                if sm2.count() > 0 and sm2.first.is_visible():
                    try: sm2.first.click(timeout=500); pg.wait_for_timeout(250)
                    except Exception: pass
            for k in ["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter"]:
                try: pg.keyboard.press(k); pg.wait_for_timeout(80)
                except Exception: pass
            s1 = pg.evaluate(state_key)
            if s1 != s0: reacts += 1; s0 = s1
            anim = pg.evaluate(CANVAS_DIFF)
            alive = reacts > 0 or (anim and anim.get("changed"))
            results.append({"slug": slug, "reacts": reacts, "anim": bool(anim and anim.get("changed")),
                            "alive": alive, "errs": errs[:3]})
        except Exception as e:
            results.append({"slug": slug, "reacts": 0, "anim": False, "alive": False,
                            "errs": ["NAV: " + str(e)[:130]]})
        try: pg.close()
        except Exception: pass
        save()
        if len(results) % 10 == 0:
            print("... %d" % len(results), flush=True)
        if len(results) % 25 == 0:
            try: browser.close()
            except Exception: pass
            browser = p.chromium.launch()
    try: browser.close()
    except Exception: pass

dead = [r for r in results if not r["alive"]]
print("FINAL-QA: %d games, %d alive, %d flagged" % (len(results), len(results) - len(dead), len(dead)))
for r in dead:
    print("--- FLAG", r["slug"], "reacts=%s anim=%s" % (r["reacts"], r["anim"]), r["errs"])
