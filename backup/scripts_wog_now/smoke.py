# -*- coding: utf-8 -*-
"""Playwright smoke test: load every game page, catch JS errors, click [data-smoke].
Usage: python3 smoke.py <site-root> <port> [slug1,slug2,...|all]
Requires: a http server serving site-root on <port>.
"""
import sys, json, urllib.request
from playwright.sync_api import sync_playwright

root, port = sys.argv[1], int(sys.argv[2])
slugs_arg = sys.argv[3] if len(sys.argv) > 3 else "all"
site = "http://127.0.0.1:%d" % port

if slugs_arg == "all":
    try:
        tiles = json.load(urllib.request.urlopen(site + "/games.json"))
    except Exception:
        import os
        tiles = [{"slug": d} for d in sorted(os.listdir(os.path.join(root, "games")))
                 if os.path.isdir(os.path.join(root, "games", d))]
else:
    tiles = [{"slug": s} for s in slugs_arg.split(",")]

bad = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for t in tiles:
        slug = t["slug"]
        errs = []
        pg = browser.new_page(viewport={"width": 440, "height": 900})
        pg.on("pageerror", lambda e, _e=errs: _e.append("pageerror: " + str(e)))
        pg.on("console", lambda m, _e=errs: _e.append("console: " + m.text)
              if m.type == "error" and "Failed to load resource" not in m.text else None)
        try:
            pg.goto("%s/games/%s/" % (site, slug), wait_until="load", timeout=15000)
            pg.wait_for_timeout(350)
            smoke = pg.locator("[data-smoke]")
            if smoke.count() > 0:
                smoke.first.click(timeout=2000)
                pg.wait_for_timeout(280)
                if smoke.count() > 0 and smoke.first.is_visible():
                    try:
                        smoke.first.click(timeout=1200)
                        pg.wait_for_timeout(200)
                    except Exception:
                        pass
            n = pg.evaluate("document.getElementById('app') ? document.getElementById('app').children.length : -1")
            if n == 0:
                errs.append("empty #app")
            home = pg.locator("a.wog-home")
            if home.count() == 0:
                errs.append("missing back button")
        except Exception as e:
            errs.append("nav: " + str(e)[:200])
        if errs:
            bad.append((slug, errs[:6]))
        pg.close()
    browser.close()

print("SMOKE: %d pages, %d with problems" % (len(tiles), len(bad)))
for slug, errs in bad:
    print("---", slug)
    for e in errs:
        print("   ", e)
sys.exit(1 if bad else 0)
