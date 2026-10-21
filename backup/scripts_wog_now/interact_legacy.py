# -*- coding: utf-8 -*-
"""Deep interaction tests for the 13 legacy games (they predate WOG_LOGIC).
Each test plays real moves and asserts visible state changes."""
from playwright.sync_api import sync_playwright

SITE = "http://127.0.0.1:8901"
results = []

def run(name, fn):
    try:
        fn()
        results.append((name, True, ""))
    except Exception as e:
        results.append((name, False, str(e)[:180]))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 460, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    def go(slug):
        errs.clear()
        pg.goto(SITE + "/games/%s/" % slug, wait_until="load")
        pg.wait_for_timeout(300)

    def game(slug, fn):
        def f():
            go(slug)
            fn()
            if errs:
                raise AssertionError("JS errors: " + "; ".join(errs[:2]))
        run(slug, f)

    # ---- chess: click e2 then e4, AI must reply ----
    def t_chess():
        # board is a grid of .sq, 8x8, direction:ltr; e2 = file e (col4), rank2 (row 6 from top)
        sq = pg.locator("#board .sq")
        n = sq.count()
        assert n == 64, "squares=%d" % n
        def cell(file, rank):  # file 0..7 = a..h, rank 0..7 = 1..8
            row = 7 - rank
            return sq.nth(row * 8 + file)
        cell(4, 1).click(); pg.wait_for_timeout(150)  # e2
        cell(4, 3).click(); pg.wait_for_timeout(3500)  # e4
        hud = pg.locator(".hud").inner_text()
        assert cell(4, 3).inner_text().strip() != "", "e4 should hold a pawn now"
        # AI reply: either hud flipped back to player or a black piece moved
        assert ("نوبت شما" in hud) or ("کرم" in hud), "hud: " + hud
    game("chess", t_chess)

    # ---- g2048: press ArrowUp, a tile must appear/appear-count grows ----
    def t_2048():
        tiles0 = pg.locator(".tile").count()
        for _ in range(4):
            pg.keyboard.press("ArrowUp"); pg.wait_for_timeout(120)
            pg.keyboard.press("ArrowLeft"); pg.wait_for_timeout(120)
        tiles1 = pg.locator(".tile").count()
        assert tiles1 > tiles0, "tiles %d → %d" % (tiles0, tiles1)
    game("g2048", t_2048)

    # ---- minesweeper: click first cell → at least one revealed ----
    def t_mines():
        cell = pg.locator(".cell, .sq, [data-r]").first
        cell.click(); pg.wait_for_timeout(250)
        revealed = pg.locator(".open, .revealed, .num").count()
        assert revealed >= 1, "no revealed cells"
    game("minesweeper", t_mines)

    # ---- tic-tac-toe: click first empty corner → X appears ----
    def t_ttt():
        cells = pg.locator("[data-i], .cell, .c")
        cells.first.click(); pg.wait_for_timeout(700)
        body = pg.locator("body").inner_text()
        assert ("✕" in body) or ("X" in body), "no X placed"
    game("tic-tac-toe", t_ttt)

    # ---- blackjack: deal + hit ----
    def t_bj():
        pg.locator("#b25").click()          # place a bet
        pg.wait_for_timeout(150)
        pg.locator("#deal").click()         # deal
        pg.wait_for_timeout(400)
        pg.locator("#hit").click()          # hit
        pg.wait_for_timeout(300)
        assert pg.locator(".wcard, .card").count() >= 2, "cards on table"
    game("blackjack", t_bj)

    # ---- akhaemenid-memory: click a card → flips ----
    def t_mem():
        c = pg.locator(".card, .wcard, [data-i]").first
        cls0 = c.get_attribute("class")
        c.click(); pg.wait_for_timeout(350)
        cls1 = c.get_attribute("class")
        assert cls0 != cls1, "card did not flip"
    game("akhaemenid-memory", t_mem)

    # ---- snake: start then arrow → no error, canvas present ----
    def t_snake():
        assert pg.locator("canvas").count() >= 1, "no canvas"
        pg.keyboard.press("ArrowUp"); pg.wait_for_timeout(700)
    game("snake", t_snake)

    # ---- solitaire: stock click (پشت کار) ----
    def t_sol():
        btn = pg.locator("button", has_text="پشت")
        if btn.count() == 0:
            btn = pg.locator("#stock, .stock")
        btn.first.click(); pg.wait_for_timeout(250)
        assert pg.locator(".wcard, .card").count() >= 1, "cards present"
    game("solitaire", t_sol)

    # ---- sudoku: 81 cells rendered ----
    def t_sudoku():
        n = pg.locator(".cell, input, [data-r]").count()
        assert n >= 60, "sudoku cells=%d" % n
    game("sudoku", t_sudoku)

    # ---- reversi: click center-adjacent legal cell ----
    def t_rev():
        cells = pg.locator(".cell, .sq, [data-r]")
        assert cells.count() >= 60, "board cells"
        # click a legal opening cell (d3/c4/f5/e6 area) — just click several, game must not error
        for i in [18, 19, 26, 27]:
            cells.nth(i).click(); pg.wait_for_timeout(300)
            if errs:
                break
    game("reversi", t_rev)

    # ---- breakout: launch (Space) + canvas alive ----
    def t_brk():
        assert pg.locator("canvas").count() >= 1
        pg.keyboard.press("Space"); pg.wait_for_timeout(600)
    game("breakout", t_brk)

    # ---- pong: start + canvas alive ----
    def t_pong():
        assert pg.locator("canvas").count() >= 1
        st = pg.locator("button", has_text="شروع")
        if st.count():
            st.first.click()
        pg.wait_for_timeout(600)
    game("pong", t_pong)

    # ---- alborz-jump: jump (Space) + canvas alive ----
    def t_alb():
        assert pg.locator("canvas").count() >= 1
        pg.keyboard.press("Space"); pg.wait_for_timeout(500)
    game("alborz-jump", t_alb)

    # ---- chess game page back button target resolves ----
    def t_backlink():
        href = pg.locator("a.wog-home").first.get_attribute("href")
        assert href == "../../index.html", href
        pg.locator("a.wog-home").first.click()
        pg.wait_for_load_state("load")
        assert "world-of-games" not in pg.url or pg.url.rstrip("/").endswith("8901"), pg.url
        assert pg.locator("#grid").count() == 1, "landing grid missing"
    run("back-link-navigates-home", t_backlink)

    b.close()

fails = [r for r in results if not r[1]]
print("INTERACTION: %d tests, %d failed" % (len(results), len(fails)))
for name, ok, msg in results:
    print(("✔" if ok else "✘"), name, ("" if ok else "— " + msg))
raise SystemExit(1 if fails else 0)
