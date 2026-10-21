# -*- coding: utf-8 -*-
"""Universal interactive test: click ALL pointer-cursor elements in #app,
press arrows, and assert the game UI changed. Flags games where NOTHING reacts.
Usage: python3 interact_universal.py <site-root> <port>
"""
import sys, os, json
from playwright.sync_api import sync_playwright

root, port = sys.argv[1], int(sys.argv[2])
site = "http://127.0.0.1:%d" % port
only = sys.argv[3].split(",") if len(sys.argv) > 3 else None

JS_COLLECT = """() => {
  const app = document.getElementById('app') || document.body;
  const els = [];
  const all = app.querySelectorAll('*');
  for (const el of all) {
    if (el.children.length > 0 && el.tagName !== 'CANVAS') continue;
    const cs = getComputedStyle(el);
    if (cs.cursor === 'pointer' || el.tagName === 'BUTTON' || el.tagName === 'CANVAS') {
      const r = el.getBoundingClientRect();
      if (r.width > 14 && r.height > 14 && r.width < window.innerWidth)
        els.push({x: r.x + r.width / 2, y: r.y + r.height / 2, w: r.width, h: r.height});
    }
  }
  // dedupe near-identical points
  const out = [];
  for (const p of els) {
    if (!out.some(q => Math.abs(q.x - p.x) < 6 && Math.abs(q.y - p.y) < 6)) out.push(p);
    if (out.length >= 40) break;
  }
  return out;
}"""

SKIP_LEGACY13 = set()  # test everything

results = []
OUT_JSON = "/home/z/my-project/universal_qa.json"

def save():
    with open(OUT_JSON, "w") as f:
        json.dump([{"slug": s, "reactions": n, "ok": ok, "errs": e} for s, n, ok, e in results], f, indent=1)

with sync_playwright() as p:
    browser = p.chromium.launch()
    games_root = os.path.join(root, "games")
    slugs = sorted(d for d in os.listdir(games_root)
                   if os.path.isdir(os.path.join(games_root, d)))
    if only: slugs = [s for s in slugs if s in only]
    for slug in slugs:
        errs = []
        pg = browser.new_page(viewport={"width": 430, "height": 880})
        pg.on("pageerror", lambda e, _e=errs: _e.append("PAGEERROR: " + str(e)[:180]))
        try:
            pg.goto("%s/games/%s/" % (site, slug), wait_until="load", timeout=15000)
            pg.wait_for_timeout(300)
            sm = pg.locator("[data-smoke]")
            if sm.count() > 0:
                try: sm.first.click(timeout=1200)
                except Exception: pass
                pg.wait_for_timeout(350)
            snap0 = pg.evaluate("document.getElementById('app') ? document.getElementById('app').innerHTML.length : document.body.innerHTML.length")
            pts = pg.evaluate(JS_COLLECT)
            reacted = 0
            for pt in pts:
                before = pg.evaluate("document.getElementById('app') ? document.getElementById('app').innerHTML.length : document.body.innerHTML.length")
                try:
                    pg.mouse.click(pt["x"], pt["y"])
                    pg.wait_for_timeout(140)
                except Exception:
                    continue
                after = pg.evaluate("document.getElementById('app') ? document.getElementById('app').innerHTML.length : document.body.innerHTML.length")
                if after != before:
                    reacted += 1
                # dismiss any overlay that opened (keep playing)
                sm2 = pg.locator("[data-smoke]")
                if sm2.count() > 0 and sm2.first.is_visible():
                    try: sm2.first.click(timeout=600); pg.wait_for_timeout(250)
                    except Exception: pass
            for k in ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]:
                try: pg.keyboard.press(k); pg.wait_for_timeout(100)
                except Exception: pass
            snap1 = pg.evaluate("document.getElementById('app') ? document.getElementById('app').innerHTML.length : document.body.innerHTML.length")
            reacted_any = reacted > 0 or snap1 != snap0
            results.append((slug, reacted, reacted_any, errs[:3]))
        except Exception as e:
            results.append((slug, 0, False, ["NAV: " + str(e)[:150]]))
        try: pg.close()
        except Exception: pass
        results_done = len(results)
        if results_done % 10 == 0:
            print("... %d done" % results_done, flush=True)
        save()
        # relaunch browser every 25 games to avoid driver crashes
        if results_done % 25 == 0:
            try: browser.close()
            except Exception: pass
            browser = p.chromium.launch()
    try: browser.close()
    except Exception: pass

dead = [r for r in results if not r[2]]
print("UNIVERSAL-INTERACT: %d games, %d reacted, %d DEAD" % (len(results), len(results) - len(dead), len(dead)))
for slug, n, ok, errs in dead:
    print("--- DEAD", slug, "reacted=%s" % n, errs)
save()
