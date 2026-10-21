# -*- coding: utf-8 -*-
"""Screenshot a sample of games (desktop + mobile) for visual assessment."""
import sys, os, json
from playwright.sync_api import sync_playwright

root, port = sys.argv[1], int(sys.argv[2])
site = "http://127.0.0.1:%d" % port
out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/shots"
os.makedirs(out, exist_ok=True)

SAMPLE = ["chess", "backgammon", "solitaire", "spider", "freecell", "hokm", "pasoor",
          "sudoku", "nonogram", "sokoban", "g2048", "minesweeper", "snake", "flappy",
          "breakout", "invaders", "wordle", "word-search", "yahtzee", "slots",
          "mancala", "dominoes", "ludo", "hangman", "wheel", "plinko", "mastermind",
          "8queens", "hanoi", "water-sort"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for slug in SAMPLE:
        pg = browser.new_page(viewport={"width": 430, "height": 900})
        try:
            pg.goto("%s/games/%s/" % (site, slug), wait_until="load", timeout=12000)
            pg.wait_for_timeout(350)
            sm = pg.locator("[data-smoke]")
            if sm.count() > 0:
                sm.first.click(timeout=1200)
                pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(out, "%s.png" % slug))
        except Exception as e:
            print("ERR", slug, str(e)[:120])
        pg.close()
    browser.close()
print("done:", len(SAMPLE))
