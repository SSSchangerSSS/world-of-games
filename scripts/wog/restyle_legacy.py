# -*- coding: utf-8 -*-
"""Restyle the 13 legacy games to Design System v2.
Appends v2 CSS (wins by order) + injects identity vars on <body>.
Canvas art upgrades for snake/breakout/pong/alborz-jump done separately."""
import io, os, re

ROOT = "/home/z/my-project/pages-site/games"

def rgba(h, a):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "rgba(%d,%d,%d,%.2f)" % (r, g, b, a)

GIRIH = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='72' height='72' viewBox='0 0 72 72'%3E"
         "%3Cg fill='none' stroke='%23d9a441' stroke-opacity='0.07' stroke-width='1'%3E"
         "%3Cpath d='M36 6l8 14 16-2-2 16 14 8-14 8 2 16-16-2-8 14-8-14-16 2 2-16-14-8 14-8-2-16 16 2z'/%3E"
         "%3Ccircle cx='36' cy='36' r='10'/%3E%3C/g%3E%3C/svg%3E")

# shared v2 chrome for legacy pages (vars come from body style)
COMMON = """
/* ===== WOG Design System v2 ===== */
body:before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;background-image:url("__GIRIH__");background-size:72px 72px}
body:after{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(120% 90% at 50% 30%,transparent 55%,rgba(4,7,14,.55) 100%)}
a.wog-home,header,#app,.stage,.panel,.bar,.toast{position:relative;z-index:1}
a.wog-home{position:fixed;top:12px;inset-inline-start:14px;z-index:99;display:inline-flex;align-items:center;gap:6px;background:linear-gradient(140deg,rgba(217,164,65,.16),rgba(217,164,65,.06));border:1px solid rgba(217,164,65,.5);color:#e8c073;text-decoration:none;padding:7px 14px;border-radius:12px;font-size:.85rem;font-weight:700;box-shadow:0 2px 10px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.06);transition:.18s}
a.wog-home:hover{background:rgba(217,164,65,.3);transform:translateY(-1px)}
h1{font-size:1.3rem;font-weight:800;display:inline-flex;align-items:center;gap:10px;background:linear-gradient(180deg,#f6d996,var(--g1b) 55%,var(--g1));-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 8px rgba(217,164,65,.22))}
h1:before,h1:after{content:'❋';font-size:.85em;color:var(--g2);-webkit-text-fill-color:var(--g2)}
button{font-weight:800;border-radius:12px;transition:transform .12s,box-shadow .15s,filter .15s}
button:active{transform:translateY(1px)}
.panel{border:1px solid rgba(217,164,65,.4);border-radius:18px;background:linear-gradient(180deg,#182646,#101a30);box-shadow:0 20px 60px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.07)}
.hud{color:#a8b3c9}
.hud b{color:#e8c073}
"""

# per-legacy-game identity + scene + component overrides
GAMES = {}

def game(slug, cat, g1, g2, css):
    GAMES[slug] = dict(cat=cat, g1=g1, g2=g2, css=css.strip())

game("chess", "board", "#b98a3c", "#4a3620", """
.sq{transition:filter .12s}
.sq.light{background:linear-gradient(145deg,#f0e5cb,#d8cba6)}
.sq.dark{background:linear-gradient(145deg,#6d5330,#4e3820)}
.sq .pc{filter:drop-shadow(0 3px 4px rgba(0,0,0,.45))}
.sq.w .pc{color:#f7f2e2;text-shadow:0 1px 0 rgba(0,0,0,.5),0 0 12px rgba(255,250,230,.25)}
.sq.b .pc{color:#20242e;text-shadow:0 1px 0 rgba(255,255,255,.15),0 0 10px rgba(10,10,20,.4)}
.sq.sel::after{box-shadow:0 0 14px rgba(232,192,115,.9)}
.sq.chk::after{box-shadow:inset 0 0 16px rgba(255,90,60,.9)}
.panel{background:linear-gradient(160deg,#2a2013,#1a1409);border-color:rgba(217,164,65,.45)}
""")

game("solitaire", "cards", "#3fb8af", "#144a44", """
body{background:
 radial-gradient(1100px 520px at 50% 118%,rgba(28,92,84,.45),transparent 62%),
 radial-gradient(760px 380px at 50% -100px,rgba(63,184,175,.3),transparent 68%),
 linear-gradient(170deg,#0f2230,#0b1420 55%,#0a101a)!important}
.card{background:linear-gradient(160deg,#fdf9ee,#efe6cf);border-radius:8px;box-shadow:0 3px 7px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,255,255,.6),inset 0 0 0 2px rgba(28,36,56,.08);transition:transform .14s}
.card:hover{transform:translateY(-2px)}
.card.down{background:linear-gradient(150deg,#31406b,#1d2a4a 55%,#2a3a63);border:1px solid rgba(217,164,65,.55)}
.card.sel{outline:3px solid #e8c073;transform:translateY(-7px);box-shadow:0 10px 22px rgba(0,0,0,.5),0 0 18px rgba(232,192,115,.4)}
.slot{border:1px dashed rgba(63,184,175,.4);border-radius:9px;background:rgba(10,20,18,.4)}
""")

game("blackjack", "cards", "#4caf6d", "#1c4a2c", """
body{background:
 radial-gradient(1100px 520px at 50% 120%,rgba(30,90,50,.5),transparent 62%),
 radial-gradient(760px 380px at 50% -100px,rgba(76,175,109,.25),transparent 68%),
 linear-gradient(170deg,#0d2318,#0a1810 55%,#08120b)!important}
.card{background:linear-gradient(160deg,#fdf9ee,#efe6cf);border-radius:9px;box-shadow:0 4px 8px rgba(0,0,0,.55),inset 0 0 0 1px rgba(255,255,255,.6);transition:transform .15s}
.card.down{background:linear-gradient(150deg,#7a1f2b,#4e1219 55%,#6b1a24);border:1px solid rgba(255,220,150,.4)}
.val{color:#e8c073}
.row-label{color:#a8b3c9;letter-spacing:.4px}
""")

game("sudoku", "puzzle", "#a78bfa", "#4a3b78", """
.cell{transition:background .12s}
.cell.fixed{color:#e8dcc0;text-shadow:0 1px 2px rgba(0,0,0,.4)}
.cell.user{color:#bfa8ff}
.cell.hl{background:rgba(167,139,250,.16)!important}
.cell.on{background:rgba(167,139,250,.32)!important;outline:2px solid rgba(167,139,250,.7)}
.cell.bad{color:#ff9a86!important}
""")

game("reversi", "board", "#67b98a", "#2c5a3f", """
body{background:
 radial-gradient(900px 460px at 50% 118%,rgba(24,80,50,.45),transparent 62%),
 radial-gradient(720px 380px at 50% -90px,rgba(103,185,138,.25),transparent 66%),
 linear-gradient(168deg,#0f1f18,#0b1410 58%,#090f0b)!important}
.cell{background:linear-gradient(150deg,#2f6d4d,#225439)!important;box-shadow:inset 0 0 0 1px rgba(0,0,0,.3),inset 0 2px 6px rgba(0,0,0,.25)}
.disc{border-radius:50%;box-shadow:0 3px 6px rgba(0,0,0,.55),inset 0 2px 3px rgba(255,255,255,.3),inset 0 -2px 4px rgba(0,0,0,.35)}
.cell.mv::after{box-shadow:0 0 12px rgba(255,225,150,.8)}
""")

game("snake", "arcade", "#67b98a", "#2c5a3f", """
.stage{border-radius:14px;overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(103,185,138,.45),0 0 0 6px rgba(10,18,14,.95)}
""")

game("breakout", "arcade", "#e26d5c", "#6e2c24", """
.stage{border-radius:14px;overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(226,109,92,.45),0 0 0 6px rgba(14,10,10,.95)}
""")

game("pong", "arcade", "#3fb8af", "#164a46", """
.stage{border-radius:14px;overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(63,184,175,.5),0 0 0 6px rgba(8,16,16,.95),0 0 26px rgba(63,184,175,.15)}
""")

game("tic-tac-toe", "board", "#e8c073", "#6b5426", """
.cell{background:linear-gradient(150deg,#1c2a4c,#142038);border-radius:14px;border:1px solid rgba(217,164,65,.35);box-shadow:0 4px 10px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.06);transition:.14s}
.cell:hover{transform:translateY(-2px);box-shadow:0 8px 18px rgba(0,0,0,.5),0 0 14px rgba(217,164,65,.2)}
.cell.x{color:#e8c073;text-shadow:0 0 16px rgba(232,192,115,.55)}
.cell.o{color:#3fb8af;text-shadow:0 0 16px rgba(63,184,175,.55)}
.cell.win{background:linear-gradient(150deg,#2c4a3a,#1c3628);box-shadow:0 0 20px rgba(103,185,138,.5)}
.ring{filter:drop-shadow(0 4px 8px rgba(0,0,0,.5))}
""")

game("minesweeper", "puzzle", "#a8b3c9", "#44506a", """
.cell{border-radius:7px;background:linear-gradient(150deg,#3d4e77,#2c3a5c);box-shadow:0 2px 5px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.14);transition:.1s}
.cell:hover{filter:brightness(1.15)}
.cell.open{background:linear-gradient(150deg,#18213a,#101828);box-shadow:inset 0 2px 5px rgba(0,0,0,.6)}
.cell.boom{background:radial-gradient(circle,#c8402a,#7a1e0e)!important;box-shadow:0 0 16px rgba(255,90,50,.7)!important}
.flag{filter:drop-shadow(0 1px 2px rgba(0,0,0,.5))}
.n1{color:#8fb7e8}.n2{color:#8fe0b0}.n3{color:#ff9a86}.n4{color:#bfa8ff}.n5{color:#e8c073}.n6{color:#5ee8d8}.n7{color:#f3ead8}.n8{color:#a8b3c9}
""")

game("g2048", "puzzle", "#d9a441", "#7a5a20", """
.tile{border-radius:10px;box-shadow:0 4px 9px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.28),inset 0 -3px 5px rgba(0,0,0,.18);transition:transform .12s}
.cellbg{border-radius:10px;background:rgba(10,16,30,.65);box-shadow:inset 0 2px 6px rgba(0,0,0,.4)}
""")

game("akhaemenid-memory", "cards", "#d9a441", "#7a4e20", """
/* Persepolis: gold on lapis */
body{background:
 radial-gradient(880px 440px at 50% -80px,rgba(217,164,65,.32),transparent 66%),
 radial-gradient(700px 440px at 108% 112%,rgba(122,78,32,.5),transparent 60%),
 linear-gradient(168deg,#151d33,#0d1322 58%,#0a0e18)!important}
.card{background:linear-gradient(150deg,#31406b,#1d2a4a);border:1px solid rgba(217,164,65,.55);border-radius:11px;box-shadow:0 6px 14px rgba(0,0,0,.5),inset 0 0 14px rgba(217,164,65,.14);transition:transform .18s}
.card:hover{transform:translateY(-3px)}
.card.open{background:linear-gradient(160deg,#f6eeda,#e2d4b0);border-color:rgba(217,164,65,.8)}
.card.open span{text-shadow:0 2px 4px rgba(120,85,30,.4)}
.card.done{border-color:rgba(103,185,138,.7);box-shadow:0 0 16px rgba(103,185,138,.4)}
button.restart{box-shadow:0 3px 10px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.35)}
""")

game("alborz-jump", "arcade", "#7ab3e8", "#2c4a6e", """
.stage{border-radius:14px;overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(122,179,232,.45),0 0 0 6px rgba(8,12,20,.95)}
""")

def restyle(slug, cfg):
    p = os.path.join(ROOT, slug, "index.html")
    s = io.open(p, encoding="utf-8").read()
    g1, g2 = cfg["g1"], cfg["g2"]
    body_attrs = ('<body data-cat="%s" data-slug="%s" style="--g1:%s;--g2:%s;--g1a:%s;--g2a:%s;--g1b:%s">'
                  % (cfg["cat"], slug, g1, g2, rgba(g1, .30), rgba(g2, .42), g2))
    s2 = re.sub(r'<body[^>]*>', body_attrs, s, count=1)
    # scene background + v2 chrome + per-game css appended (wins by order)
    css = COMMON.replace("__GIRIH__", GIRIH) + "\n" + cfg["css"]
    # legacy bodies use plain gradient; give them the layered scene unless game css sets !important bg
    scene = ("\nbody{background:"
             "radial-gradient(900px 420px at 50% -80px,var(--g1a),transparent 68%),"
             "radial-gradient(720px 480px at 108% 112%,var(--g2a),transparent 60%),"
             "linear-gradient(168deg,#111c33 0%,#0b1220 58%,#0a0f1d 100%);background-attachment:fixed}")
    css = css + scene if "!important" in cfg["css"] else scene + "\n" + css
    s2 = s2.replace("</style>", css + "\n</style>", 1)
    io.open(p, "w", encoding="utf-8").write(s2)
    return len(s2) - len(s)

total = 0
for slug, cfg in GAMES.items():
    d = restyle(slug, cfg)
    total += 1
    print("restyled", slug, "+%dB" % d)
print("done:", total)
