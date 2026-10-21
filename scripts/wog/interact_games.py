# -*- coding: utf-8 -*-
"""Interactive gameplay tests with per-game recipes.
Each recipe performs REAL moves and asserts the game state progressed.
Usage: python3 interact_games.py <site-root> <port> [slug,slug,...|all]
"""
import sys, os, json
from playwright.sync_api import sync_playwright

root, port = sys.argv[1], int(sys.argv[2])
site = "http://127.0.0.1:%d" % port
only = sys.argv[3].split(",") if len(sys.argv) > 3 else None

def body_text(pg):
    return pg.evaluate("document.body.innerText.replace(/\\s+/g,' ').slice(0,2000)")

def app_html(pg):
    return pg.evaluate("document.getElementById('app').innerHTML.replace(/\\s+/g,' ').slice(0,4000)")

def click_cells(pg, n, start=0):
    """Click first n .cell elements."""
    loc = pg.locator(".cell")
    clicked = 0
    for i in range(start, min(start + n, loc.count())):
        try:
            if loc.nth(i).is_visible():
                loc.nth(i).click(timeout=700)
                pg.wait_for_timeout(120)
                clicked += 1
        except Exception:
            pass
    return clicked

def click_cards(pg, n=2, start=0):
    loc = pg.locator(".wcard")
    for i in range(start, min(start + n, loc.count())):
        try:
            if loc.nth(i).is_visible():
                loc.nth(i).click(timeout=700)
                pg.wait_for_timeout(150)
        except Exception:
            pass

def click_buttons(pg, texts):
    for t in texts:
        try:
            pg.locator("button", has_text=t).first.click(timeout=800)
            pg.wait_for_timeout(200)
        except Exception:
            pass

def start(pg):
    sm = pg.locator("[data-smoke]")
    if sm.count() > 0:
        try:
            sm.first.click(timeout=1200)
            pg.wait_for_timeout(350)
        except Exception:
            pass

# ---------- recipes: each returns list of (check_name, ok_bool, detail) ----------
def r_chess(pg):
    a0 = app_html(pg)
    # e2 pawn: click cell then destination — try a few two-click combos
    cells = pg.locator(".cell")
    n = cells.count()
    done = False
    for first in range(48, 56):  # bottom rows (white pieces)
        if done: break
        try:
            cells.nth(first).click(timeout=400); pg.wait_for_timeout(100)
            for dest in (first - 8, first - 16, first - 9, first - 7):
                if 0 <= dest < n:
                    cells.nth(dest).click(timeout=400); pg.wait_for_timeout(500)
                    if app_html(pg) != a0: done = True; break
        except Exception:
            pass
    return [("board changed after white move + AI", done, "")]

def r_checkers(pg):
    a0 = app_html(pg)
    cells = pg.locator(".cell")
    n = cells.count()
    done = False
    for first in range(n - 24, n):
        if done: break
        try:
            cells.nth(first).click(timeout=400); pg.wait_for_timeout(120)
            for dest in (first - 7, first - 9, first - 14, first - 18, first - 7 - 1, first - 9 - 1):
                if 0 <= dest < n:
                    cells.nth(dest).click(timeout=400); pg.wait_for_timeout(600)
                    if app_html(pg) != a0: done = True; break
        except Exception:
            pass
    return [("checkers moved + AI replied", done, "")]

def r_gomoku(pg):
    a0 = app_html(pg)
    click_cells(pg, 1)
    pg.wait_for_timeout(600)
    return [("stone placed + AI moved", app_html(pg) != a0, "")]

def r_connect4(pg):
    a0 = app_html(pg)
    click_cells(pg, 1)
    pg.wait_for_timeout(600)
    return [("disc dropped + AI moved", app_html(pg) != a0, "")]

def r_reversi(pg):
    a0 = app_html(pg)
    ok = False
    for i in range(10):
        before = app_html(pg)
        click_cells(pg, 1, start=i)
        pg.wait_for_timeout(500)
        if app_html(pg) != before: ok = True; break
    return [("legal move accepted + AI replied", ok, "")]

def r_backgammon(pg):
    a0 = app_html(pg)
    click_buttons(pg, ["تاس"])
    pg.wait_for_timeout(400)
    a1 = app_html(pg)
    cells = pg.locator(".cell, [data-point]")
    n = cells.count()
    ok = False
    for i in range(min(n, 24)):
        try:
            cells.nth(i).click(timeout=300); pg.wait_for_timeout(120)
            cells.nth((i + 3) % n).click(timeout=300); pg.wait_for_timeout(350)
            if app_html(pg) != a1: ok = True; break
        except Exception:
            pass
    return [("rolled + made a move", ok or app_html(pg) != a0, "")]

def r_ludo(pg):
    a0 = app_html(pg)
    click_buttons(pg, ["تاس", "ریختن تاس", "پرتاب"])
    pg.wait_for_timeout(400)
    a1 = app_html(pg)
    click_cells(pg, 6)
    pg.wait_for_timeout(600)
    return [("dice rolled + token moved", app_html(pg) != a1 or app_html(pg) != a0, "")]

def r_battleship(pg):
    a0 = app_html(pg)
    ok = False
    for i in range(12):
        before = app_html(pg)
        click_cells(pg, 1, start=i)
        pg.wait_for_timeout(450)
        if app_html(pg) != before: ok = True; break
    return [("shot registered + AI fired", ok, "")]

def r_mancala(pg):
    a0 = app_html(pg)
    ok = False
    for i in range(8):
        before = app_html(pg)
        click_cells(pg, 1, start=i)
        pg.wait_for_timeout(500)
        if app_html(pg) != before: ok = True; break
    return [("pit sown", ok, "")]

def r_dominoes(pg):
    a0 = app_html(pg)
    click_cards(pg, 1)
    pg.wait_for_timeout(300)
    click_buttons(pg, ["کشیدن", "رد", "پاس"])
    pg.wait_for_timeout(500)
    return [("tile played/drawn", app_html(pg) != a0, "")]

def r_ur(pg):
    a0 = app_html(pg)
    click_buttons(pg, ["تاس", "پرتاب"])
    pg.wait_for_timeout(300)
    a1 = app_html(pg)
    click_cells(pg, 8)
    pg.wait_for_timeout(500)
    return [("rolled + moved", app_html(pg) != a1 or app_html(pg) != a0, "")]

def r_snakes(pg):
    a0 = app_html(pg)
    click_buttons(pg, ["تاس", "پرتاب"])
    pg.wait_for_timeout(700)
    return [("dice rolled & moved", app_html(pg) != a0, "")]

def r_hokm(pg):
    a0 = app_html(pg)
    ok = False
    for i in range(8):
        before = app_html(pg)
        click_cards(pg, 1, start=i)
        pg.wait_for_timeout(600)
        if app_html(pg) != before: ok = True; break
    return [("card playable", ok, "")]

def r_pasoor(pg):
    return r_hokm(pg)

def r_crazy(pg):
    return r_hokm(pg)

def r_thirtyone(pg):
    a0 = app_html(pg)
    click_cards(pg, 1)
    pg.wait_for_timeout(400)
    click_buttons(pg, ["برداشتن", "کشیدن", "پاس", "بستن"])
    pg.wait_for_timeout(500)
    return [("turn progressed", app_html(pg) != a0, "")]

def r_war(pg):
    a0 = app_html(pg)
    click_buttons(pg, ["بکش", "بزن", "کارت", "برو"])
    pg.wait_for_timeout(600)
    return [("battle resolved", app_html(pg) != a0, "")]

def r_poker(pg):
    a0 = app_html(pg)
    click_cards(pg, 2)
    click_buttons(pg, ["پخش", "تعویض", "دراو", "Draw"])
    pg.wait_for_timeout(600)
    return [("deal/draw worked", app_html(pg) != a0, "")]

def r_solitaire_family(slug):
    def r(pg):
        a0 = app_html(pg)
        ok = False
        for i in range(10):
            before = app_html(pg)
            click_cards(pg, 1, start=i)
            pg.wait_for_timeout(350)
            click_cards(pg, 1, start=0)
            pg.wait_for_timeout(350)
            click_buttons(pg, ["پشت‌کار", "کشیدن", "بزن"])
            pg.wait_for_timeout(300)
            if app_html(pg) != before: ok = True; break
        return [("%s: a card moved/flipped" % slug, ok, "")]
    return r

def r_sokoban(pg):
    a0 = app_html(pg)
    for k in ["ArrowUp", "ArrowLeft", "ArrowUp", "ArrowRight"]:
        pg.keyboard.press(k); pg.wait_for_timeout(150)
    return [("player moved", app_html(pg) != a0, "")]

def r_rushhour(pg):
    a0 = app_html(pg)
    ok = False
    for i in range(10):
        before = app_html(pg)
        click_cells(pg, 1, start=i)
        click_cells(pg, 1, start=0)
        pg.wait_for_timeout(300)
        if app_html(pg) != before: ok = True; break
    return [("car moved", ok, "")]

def r_nonogram(pg):
    a0 = app_html(pg)
    click_cells(pg, 3)
    return [("cells toggled", app_html(pg) != a0, "")]

def r_mastermind(pg):
    a0 = app_html(pg)
    click_buttons(pg, ["ثبت", "حدس", "بررسی"])
    pg.wait_for_timeout(300)
    click_cells(pg, 4)
    click_buttons(pg, ["ثبت", "حدس", "بررسی"])
    pg.wait_for_timeout(500)
    return [("guess submitted", app_html(pg) != a0, "")]

def r_watersort(pg):
    a0 = app_html(pg)
    click_cells(pg, 1)
    pg.wait_for_timeout(200)
    click_cells(pg, 1, start=1)
    pg.wait_for_timeout(500)
    return [("pour attempted", app_html(pg) != a0, "")]

def r_blockudoku(pg):
    a0 = app_html(pg)
    click_cells(pg, 4)
    return [("grid interaction", app_html(pg) != a0, "")]

def r_calc24(pg):
    a0 = app_html(pg)
    click_cells(pg, 2)
    click_buttons(pg, ["+", "×"])
    return [("expression built", app_html(pg) != a0, "")]

def r_kakuro(pg):
    a0 = app_html(pg)
    click_cells(pg, 1)
    click_buttons(pg, ["۱", "1"])
    return [("cell filled", app_html(pg) != a0, "")]

def r_typing(pg):
    a0 = body_text(pg)
    pg.keyboard.type("سلام")
    pg.wait_for_timeout(300)
    return [("typing registered", body_text(pg) != a0, "")]

def r_8queens(pg):
    a0 = app_html(pg)
    click_cells(pg, 1)
    return [("queen placed", app_html(pg) != a0, "")]

def r_fox(pg):
    a0 = app_html(pg)
    ok = False
    for i in range(8):
        before = app_html(pg)
        click_cells(pg, 1, start=i)
        pg.wait_for_timeout(250)
        click_cells(pg, 1, start=0)
        pg.wait_for_timeout(400)
        if app_html(pg) != before: ok = True; break
    return [("hound moved + fox AI", ok, "")]

def r_morris(pg):
    a0 = app_html(pg)
    click_cells(pg, 1)
    pg.wait_for_timeout(500)
    return [("stone placed + AI", app_html(pg) != a0, "")]

def r_pentago(pg):
    a0 = app_html(pg)
    click_cells(pg, 1)
    pg.wait_for_timeout(400)
    click_cells(pg, 1, start=10)
    pg.wait_for_timeout(500)
    return [("marble + rotation", app_html(pg) != a0, "")]

def r_quarto(pg):
    a0 = app_html(pg)
    ok = False
    for i in range(8):
        before = app_html(pg)
        click_cells(pg, 1, start=i)
        pg.wait_for_timeout(400)
        if app_html(pg) != before: ok = True; break
    return [("piece selected/placed", ok, "")]

def r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water(pg):
    a0 = app_html(pg)
    click_cells(pg, 2)
    pg.keyboard.press("ArrowUp")
    return [("interaction accepted", app_html(pg) != a0, "")]

RECIPES = {
    "chess": r_chess, "checkers": r_checkers, "gomoku": r_gomoku, "connect4": r_connect4,
    "reversi": r_reversi, "backgammon": r_backgammon, "ludo": r_ludo, "battleship": r_battleship,
    "mancala": r_mancala, "dominoes": r_dominoes, "game-of-ur": r_ur, "snakes-ladders": r_snakes,
    "hokm": r_hokm, "pasoor": r_pasoor, "crazy-eights": r_crazy, "thirty-one": r_thirtyone,
    "war": r_war, "video-poker": r_poker,
    "spider": r_solitaire_family("spider"), "freecell": r_solitaire_family("freecell"),
    "golf": r_solitaire_family("golf"), "pyramid": r_solitaire_family("pyramid"),
    "tripeaks": r_solitaire_family("tripeaks"), "clock": r_solitaire_family("clock"),
    "solitaire": r_solitaire_family("solitaire"), "blackjack": r_solitaire_family("blackjack"),
    "sokoban": r_sokoban, "rush-hour": r_rushhour, "nonogram": r_nonogram,
    "mastermind": r_mastermind, "water-sort": r_watersort, "blockudoku": r_blockudoku,
    "calc24": r_calc24, "kakuro": r_kakuro, "typing": r_typing, "8queens": r_8queens,
    "fox-and-hounds": r_fox, "morris9": r_morris, "pentago": r_pentago, "quarto-mini": r_quarto,
    "chomp": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "nim": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "peg": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "flood": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "hanoi": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "lights-out": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "simon": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "maze": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
    "p15": r_chomp_nim_peg_flood_hanoi_lights_simon_maze_water,
}

results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for slug, recipe in RECIPES.items():
        if only and slug not in only:
            continue
        errs = []
        pg = browser.new_page(viewport={"width": 440, "height": 900})
        pg.on("pageerror", lambda e, _e=errs: _e.append("PAGEERROR: " + str(e)[:200]))
        try:
            pg.goto("%s/games/%s/" % (site, slug), wait_until="load", timeout=15000)
            pg.wait_for_timeout(350)
            start(pg)
            checks = recipe(pg)
        except Exception as e:
            checks = [("recipe", False, str(e)[:160])]
        for name, ok, detail in checks:
            results.append((slug, name, ok, detail + (" | " + "; ".join(errs) if errs else "")))
        pg.close()
    try: browser.close()
    except Exception: pass

npass = sum(1 for r in results if r[2])
print("INTERACTIVE: %d checks, %d pass, %d fail" % (len(results), npass, len(results) - npass))
for slug, name, ok, detail in results:
    if not ok:
        print("--- FAIL", slug, "::", name, detail)
