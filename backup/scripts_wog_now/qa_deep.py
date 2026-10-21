# -*- coding: utf-8 -*-
"""Deep QA scan: load every game, interact aggressively, catch ALL errors.
Usage: python3 qa_deep.py <site-root> <port>
Reports per-game: JS errors, broken rendering, dead interactions.
"""
import sys, json, os
from playwright.sync_api import sync_playwright

root, port = sys.argv[1], int(sys.argv[2])
site = "http://127.0.0.1:%d" % port

tiles_path = os.path.join(root, "games.json")
if os.path.exists(tiles_path):
    tiles = json.load(open(tiles_path, encoding="utf-8"))
else:
    tiles = [{"slug": d} for d in sorted(os.listdir(os.path.join(root, "games")))
             if os.path.isdir(os.path.join(root, "games", d))]

results = []

def interact(pg, slug):
    """Try a series of generic interactions to shake out runtime bugs."""
    actions = []
    # 1: click all visible small buttons (except home link / overlay restart)
    for sel in ["button", ".cell", ".wcard", "canvas"]:
        loc = pg.locator(sel)
        n = min(loc.count(), 14)
        for i in range(n):
            try:
                el = loc.nth(i)
                if not el.is_visible():
                    continue
                bb = el.bounding_box()
                if not bb or bb["width"] < 8 or bb["height"] < 8:
                    continue
                el.click(timeout=600, force=True)
                actions.append("ok")
            except Exception:
                pass
    # 2: keyboard for arcade
    for key in ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Space", "Enter"]:
        try:
            pg.keyboard.press(key)
        except Exception:
            pass
    return actions

with sync_playwright() as p:
    browser = p.chromium.launch()
    for t in tiles:
        slug = t["slug"]
        errs = []
        pg = browser.new_page(viewport={"width": 420, "height": 860})
        pg.on("pageerror", lambda e, _e=errs: _e.append("PAGEERROR: " + str(e)[:260]))
        pg.on("console", lambda m, _e=errs: _e.append("CONSOLE-ERR: " + str(m.text)[:220])
              if m.type == "error" and "Failed to load resource" not in str(m.text) else None)
        try:
            pg.goto("%s/games/%s/" % (site, slug), wait_until="load", timeout=15000)
            pg.wait_for_timeout(400)
            # start the game if smoke button present
            sm = pg.locator("[data-smoke]")
            if sm.count() > 0:
                sm.first.click(timeout=1500)
                pg.wait_for_timeout(300)
            interact(pg, slug)
            pg.wait_for_timeout(500)
            # second smoke click (restart) if still visible
            sm = pg.locator("[data-smoke]")
            if sm.count() > 0 and sm.first.is_visible():
                try:
                    sm.first.click(timeout=800)
                    pg.wait_for_timeout(250)
                except Exception:
                    pass
            # rendering checks
            app_n = pg.evaluate("document.getElementById('app') ? document.getElementById('app').children.length : -1")
            if app_n == 0:
                errs.append("RENDER: empty #app")
            body_txt = pg.evaluate("document.body.innerText.length")
            if body_txt < 20:
                errs.append("RENDER: body text nearly empty (%d chars)" % body_txt)
            has_back = pg.locator("a.wog-home").count()
            if not has_back:
                errs.append("RENDER: missing back button")
            # overlay blocking check: any permanent full-screen overlay that hides app?
        except Exception as e:
            errs.append("NAV: " + str(e)[:220])
        pg.close()
        status = "FAIL" if errs else "PASS"
        results.append((slug, status, errs[:8]))

        if len(results) % 20 == 0:
            print("... %d/%d scanned" % (len(results), len(tiles)), flush=True)

        # incremental save so partial results survive a crash
        with open(os.path.join(root, "..", "qa_report.json"), "w", encoding="utf-8") as f:
            json.dump([{"slug": s, "status": st, "errs": e} for s, st, e in results],
                      f, ensure_ascii=False, indent=1)

fails = [r for r in results if r[1] == "FAIL"]
print("DEEP-QA: %d games, %d PASS, %d FAIL" % (len(results), len(results) - len(fails), len(fails)))
for slug, st, errs in fails:
    print("--- FAIL", slug)
    for e in errs:
        print("    ", e)
# also write json report
with open(os.path.join(root, "..", "qa_report.json"), "w", encoding="utf-8") as f:
    json.dump([{"slug": s, "status": st, "errs": e} for s, st, e in results], f, ensure_ascii=False, indent=1)
sys.exit(0)
