# -*- coding: utf-8 -*-
"""Build the 100-game pages-site from batch definitions.
Full build:  python3 build.py
Self-check:  python3 build.py --only games/a_cards1.py --out /tmp/wogcheck
"""
import os, sys, json, glob, importlib.util, io, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib
from lib import G, CATS

# The complete, final catalog: 13 existing + 87 new = exactly 100
EXISTING13 = [
    ("chess", "شطرنج", "board", "♞", "شطرنج کامل با قوانین رسمی و هوش مصنوعی"),
    ("solitaire", "سولیتر", "cards", "♠", "سولیتر کلاسیک کلایک با undo و برداشتن خودکار"),
    ("blackjack", "بلک‌جک ۲۱", "cards", "🂡", "بلک‌جک با کفش ۴ دسته، دوبرابر و پرداخت ۳ به ۲"),
    ("sudoku", "سودوکو", "puzzle", "🔢", "سودوکو با تولید راه‌حل‌یکتا و سه سطح"),
    ("reversi", "اوتلو", "board", "◐", "ریورسی ۸×۸ با وزن‌دهی موقعیتی"),
    ("snake", "مار گرسنه", "arcade", "🐍", "مار کلاسیک با کنترل لمسی و کیبورد"),
    ("breakout", "توپ‌شکن", "arcade", "🧱", "شکستن آجرها با فیزیک دقیق و لِوِل‌های بی‌پایان"),
    ("pong", "پینگ‌پنگ", "arcade", "🏓", "پینگ‌پنگ دو نفره مقابل هوش مصنوعی"),
    ("tic-tac-toe", "دوز", "board", "✕", "دوز با مینی‌مکس شکست‌ناپذیر"),
    ("minesweeper", "مین‌یاب", "puzzle", "💣", "مین‌یاب با اولین کلیک امن و دو سطح"),
    ("g2048", "۲۰۴۸", "puzzle", "🟨", "پازل عددی ۲۰۴۸ با انیمیشن لغزش"),
    ("akhaemenid-memory", "حافظه هخامنشی", "cards", "🏛", "بازی حافظه با نمادهای ایران‌باستان"),
    ("alborz-jump", "پرش از البرز", "arcade", "⛰", "پرش پلتفرمی عمودی روی قله البرز"),
]
EXPECTED = set(s for s, *_ in EXISTING13) | {
    "pasoor", "hokm", "spider", "freecell", "pyramid", "tripeaks", "golf", "clock", "crazy-eights", "war",
    "higher-lower", "video-poker", "thirty-one", "yahtzee", "pig", "chuck-a-luck", "lcr", "rps", "slots", "wheel",
    "checkers", "gomoku", "connect4", "morris9", "hex", "chomp", "nim", "mancala", "dots-boxes",
    "ludo", "snakes-ladders", "dominoes", "game-of-ur", "battleship", "pentago", "quarto-mini", "fox-and-hounds",
    "backgammon",
    "p15", "sokoban", "rush-hour", "flood", "peg", "blockudoku", "hanoi", "maze", "8queens", "lights-out",
    "nonogram", "mastermind", "simon", "water-sort", "calc24", "kakuro", "memory-grid",
    "flappy", "frogger", "coin-catch", "runner", "meteor", "stacker", "kite", "asteroids", "invaders", "dodge",
    "whack", "reaction", "aim", "digits", "stroop", "math-sprint", "typing", "cups",
    "wordle", "hangman", "word-search", "anagram", "word-chain", "proverb", "antonym", "flags", "capitals", "emoji-quiz",
    "guess-number", "coin-flip", "lotto", "plinko",
}


def load_batch(path):
    sys.modules.setdefault('lib_mini', lib)  # agent batch files import lib_mini
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.GAMES


def build_games(games, out_games):
    os.makedirs(out_games, exist_ok=True)
    manifest = []
    for g in games:
        html = g.render()
        errs = lib.check_spec_violations(html, g.slug)
        if errs:
            for e in errs:
                print("SPEC-ERROR:", e)
            raise SystemExit(1)
        d = os.path.join(out_games, g.slug)
        os.makedirs(d, exist_ok=True)
        with io.open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        manifest.append({
            "slug": g.slug, "title": g.title, "cat": g.cat, "icon": g.icon,
            "desc": g.desc,
            "tests": [{"name": n, "js": js} for n, js in g.tests],
            "logic": g.logic_export(), "seed": g.seed,
            "enginesJs": (lambda ee: "".join({"common": lib.COMMON_JS, "card": lib.CARD_JS,
                                              "arcade": lib.ARCADE_JS, "word": lib.WORD_JS}[e] for e in ee))(g.engines),
        })
    return manifest


def write_tests_manifest(manifest, out):
    with io.open(os.path.join(out, "tests-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)


def main():
    args = sys.argv[1:]
    only = None
    out = os.path.join(os.path.dirname(os.path.dirname(HERE)), "pages-site")  # /home/z/my-project/pages-site
    if "--only" in args:
        only = args[args.index("--only") + 1]
    if "--out" in args:
        out = args[args.index("--out") + 1]

    batch_files = sorted(glob.glob(os.path.join(HERE, "games", "*.py")))
    if only:
        batch_files = [os.path.join(HERE, only) if not os.path.isabs(only) else only]
    games = []
    seen = set()
    for bf in batch_files:
        for g in load_batch(bf):
            if g.slug in seen:
                raise SystemExit("duplicate slug: " + g.slug)
            seen.add(g.slug)
            games.append(g)

    full = out.endswith("pages-site") and not only
    if full:
        new_expected = EXPECTED - set(s for s, *_ in EXISTING13)
        missing = new_expected - seen
        if missing:
            raise SystemExit("MISSING slugs (%d): %s" % (len(missing), ", ".join(sorted(missing))))
        extra = seen - new_expected
        if extra:
            raise SystemExit("EXTRA slugs: %s" % ", ".join(sorted(extra)))
        print("catalog OK: %d new games (total %d with existing)" % (len(games), len(games) + 13))

    out_games = os.path.join(out, "games")
    manifest = build_games(games, out_games)
    os.makedirs(out, exist_ok=True)
    write_tests_manifest(manifest, out)
    print("built %d games into %s" % (len(games), out_games))
    if only:
        return
    build_site_extra(games, out)


def game_tile(g):
    return {"slug": g.slug, "title": g.title, "cat": g.cat, "icon": g.icon, "desc": g.desc}


def build_site_extra(new_games, out):
    """landing index.html + games.json + sitemap.xml + licenses.html"""
    tiles = [dict(slug=s, title=t, cat=c, icon=i, desc=d) for s, t, c, i, d in EXISTING13]
    tiles += [game_tile(g) for g in new_games]
    tiles.sort(key=lambda x: x["title"])
    all_slugs = [t["slug"] for t in tiles]
    assert len(all_slugs) == 100, len(all_slugs)
    with io.open(os.path.join(out, "games.json"), "w", encoding="utf-8") as f:
        json.dump(tiles, f, ensure_ascii=False, indent=1)

    base = "https://ssschangersss.github.io/world-of-games/"
    urls = ["", "licenses.html"] + ["games/%s/" % s for s in all_slugs]
    today = "2026-10-20"
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("<url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>"
                  % (base, u, today, "1.0" if u == "" else "0.7"))
    sm.append("</urlset>")
    with io.open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm))

    here = os.path.dirname(os.path.abspath(__file__))
    tpl_path = os.path.join(here, "landing_template.py")
    spec = importlib.util.spec_from_file_location("landing_template", tpl_path)
    lt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lt)
    lt.render(out, tiles)  # writes index.html + licenses.html into `out`
    print("landing + sitemap + licenses written")


if __name__ == "__main__":
    main()
