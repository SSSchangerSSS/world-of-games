# -*- coding: utf-8 -*-
"""Per-game visual themes (slug → CSS). Injected AFTER each game's own css,
so theme colors win on conflicts. Layout untouched.
Each theme gives the game its own scene/props per its world & style."""

THEMES = {}

def _t(slug, css):
    THEMES[slug] = css.strip()

# ============================ BOARD ============================
_t("checkers", """
/* walnut board + glossy men */
.wgrid .cell.light{background:linear-gradient(150deg,#e8d3ae,#c9a86f)}
.wgrid .cell.dark{background:linear-gradient(150deg,#7a4e28,#5b3818)}
.wgrid .cell{font-size:30px;line-height:1;filter:none}
.wgrid .cell.dark{text-shadow:0 2px 3px rgba(0,0,0,.55),0 0 14px rgba(255,220,150,.15)}
.wgrid .cell.light{text-shadow:0 2px 3px rgba(0,0,0,.45)}
""")

_t("gomoku", """
/* kaya wood board, slate stones */
.wgrid{border-color:rgba(160,110,50,.7);box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 0 5px rgba(48,32,16,.9),0 0 0 6px rgba(200,150,80,.3)}
.wgrid .cell.light,.wgrid .cell.dark{background:linear-gradient(160deg,#e3b871,#cf9f4e)}
.wgrid .cell{font-size:26px;color:#10151d;text-shadow:0 2px 4px rgba(0,0,0,.5)}
.wgrid .cell:hover{background:linear-gradient(160deg,#eec07a,#d6a755)}
""")

_t("connect4", """
/* punched blue frame, glossy discs */
.wgrid{background:linear-gradient(160deg,#2a5fd0,#1c3f9a);border-color:rgba(120,170,255,.5);box-shadow:0 12px 34px rgba(0,0,0,.55),0 0 0 5px rgba(16,26,50,.95),0 0 0 6px rgba(120,170,255,.25);padding:6px;gap:5px}
.wgrid .cell{border-radius:50%;background:radial-gradient(circle at 38% 32%,#101c38,#070d1e 70%);box-shadow:inset 0 3px 8px rgba(0,0,0,.8),0 1px 0 rgba(255,255,255,.14)}
.wgrid .cell.light,.wgrid .cell.dark{background:radial-gradient(circle at 38% 32%,#101c38,#070d1e 70%)}
.wgrid .cell{font-size:26px}
""")

_t("reversi", """
/* tournament green felt, lacquer discs */
.wgrid{border-color:rgba(80,180,120,.55);box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 0 5px #1c3a2b,0 0 0 6px rgba(120,200,150,.28)}
.wgrid .cell.light,.wgrid .cell.dark{background:linear-gradient(150deg,#2f6d4d,#225439)}
.cell.light,.cell.dark{background:linear-gradient(150deg,#2f6d4d,#225439)}
.dotc,.dotp{border-radius:50%;box-shadow:0 3px 6px rgba(0,0,0,.55),inset 0 1px 2px rgba(255,255,255,.25)}
.ghost{opacity:.35;filter:drop-shadow(0 0 6px rgba(255,230,150,.6))}
""")

_t("mancala", """
/* carved walnut board, amber gems */
.mboard{background:linear-gradient(165deg,#6b4223,#472a12);border:1px solid rgba(255,210,140,.35);border-radius:22px;box-shadow:0 14px 34px rgba(0,0,0,.55),inset 0 2px 0 rgba(255,220,160,.18),inset 0 -3px 8px rgba(0,0,0,.4);padding:14px}
.pit,.store{background:radial-gradient(circle at 40% 30%,#3a220f,#241404 75%);box-shadow:inset 0 4px 10px rgba(0,0,0,.75),0 1px 0 rgba(255,215,150,.14);border-radius:50%}
.seed{background:radial-gradient(circle at 35% 30%,#ffd98a,#c9873a 60%,#8a5220);box-shadow:0 1px 3px rgba(0,0,0,.6),0 0 6px rgba(255,200,110,.35);border-radius:50%}
.cnt,.plab{color:#ffd98a}
.clickable{cursor:pointer}
.clickable:hover .pit{box-shadow:inset 0 4px 10px rgba(0,0,0,.7),0 0 14px rgba(255,205,120,.45)}
""")

_t("ludo", """
/* vivid quadrants + glossy die */
.ltrack{background:linear-gradient(165deg,#f4ead2,#e2d3ae);border-radius:16px;box-shadow:0 10px 28px rgba(0,0,0,.5),inset 0 0 0 2px rgba(120,85,40,.35);padding:10px}
.die{background:linear-gradient(150deg,#fffdf4,#e8ddc0);border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,.45),inset 0 -2px 4px rgba(0,0,0,.12);color:#20242e;font-weight:800}
.pbase{filter:drop-shadow(0 3px 5px rgba(0,0,0,.4))}
""")

_t("dominoes", """
/* ivory tiles with brass spinners */
.dtile,.btile{background:linear-gradient(155deg,#faf5e6,#e8dfc6);border-radius:9px;box-shadow:0 4px 9px rgba(0,0,0,.5),inset 0 0 0 1px rgba(120,95,50,.25),inset 0 1px 0 rgba(255,255,255,.7);color:#232a38}
.btile{background:linear-gradient(155deg,#2c3a5e,#1b2745);border:1px solid rgba(217,164,65,.5)}
.dline{background:linear-gradient(90deg,transparent,rgba(120,95,50,.6),transparent)}
""")

_t("hex", """
/* honeycomb glow */
.hx-svg{filter:drop-shadow(0 6px 14px rgba(0,0,0,.5))}
.hx-pt{transition:.15s}
""")

_t("battleship", """
/* naval ops radar */
.bsboard{background:linear-gradient(160deg,#0a1c30,#07121f);border:1px solid rgba(90,170,230,.4);border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.55),inset 0 0 24px rgba(40,110,180,.18),0 0 0 4px rgba(10,20,34,.9);padding:8px;position:relative}
.bcell{border-radius:6px;background:linear-gradient(150deg,#10263e,#0a1828);box-shadow:inset 0 0 0 1px rgba(90,170,230,.16)}
.hit{background:radial-gradient(circle,#ff8a5c,#c22e12)!important;box-shadow:0 0 14px rgba(255,110,60,.55)!important}
.mis{background:radial-gradient(circle,#29527d,#16324f)!important}
.bchip{background:#10263e;border:1px solid rgba(90,170,230,.4);border-radius:10px}
""")

_t("game-of-ur", """
/* lapis lazuli + shell inlay, gold dice */
.uboard{background:linear-gradient(165deg,#1e3a6e,#122347);border:1px solid rgba(150,190,255,.35);border-radius:14px;box-shadow:0 12px 32px rgba(0,0,0,.55),inset 0 0 0 2px rgba(240,230,200,.14),inset 0 0 30px rgba(30,70,150,.3);padding:10px}
.ucell{background:linear-gradient(150deg,#28497f,#1a3060);border:1px solid rgba(235,220,180,.28);border-radius:9px;box-shadow:inset 0 1px 0 rgba(255,255,255,.1)}
.ucell.canmv{box-shadow:0 0 14px rgba(255,215,120,.5),inset 0 1px 0 rgba(255,255,255,.12);border-color:rgba(255,215,120,.6)}
.die{background:linear-gradient(150deg,#f3e9cd,#d9c9a0);color:#2a2415;border-radius:9px;box-shadow:0 3px 8px rgba(0,0,0,.5)}
""")

_t("backgammon", """
/* leather case, mother-of-pearl points */
.bgb{background:linear-gradient(160deg,#20344f,#15233a);border:1px solid rgba(217,164,65,.4);border-radius:16px;box-shadow:0 14px 36px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.06);padding:10px}
.bpt{border-radius:8px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.3)}
.bch{border-radius:50%;box-shadow:0 2px 5px rgba(0,0,0,.6),inset 0 2px 3px rgba(255,255,255,.28),inset 0 -2px 3px rgba(0,0,0,.3)}
.die{border-radius:9px;box-shadow:0 4px 9px rgba(0,0,0,.5);font-weight:800}
""")

_t("morris9", """
/* parchment + iron ink */
.mv-svg{background:linear-gradient(160deg,#efe4c3,#dfcfa4);border-radius:14px;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 0 0 2px rgba(90,70,40,.25)}
.mv-pt{filter:drop-shadow(0 2px 3px rgba(0,0,0,.4))}
""")

_t("pentago", """
/* marble quadrants */
.pboard{background:linear-gradient(160deg,#24365c,#16233f);border-radius:16px;padding:8px;box-shadow:0 12px 30px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.08)}
.pcell{border-radius:50%;background:radial-gradient(circle at 40% 32%,#2c4370,#182647 75%);box-shadow:inset 0 3px 7px rgba(0,0,0,.6),0 1px 0 rgba(255,255,255,.1)}
.qsel{outline:2px solid rgba(232,192,115,.75);outline-offset:3px;border-radius:14px}
""")

_t("quarto-mini", """
/* slate board + neon pieces */
.qboard{background:linear-gradient(160deg,#1b2942,#111c30);border-radius:16px;box-shadow:0 10px 28px rgba(0,0,0,.5),inset 0 0 0 1px rgba(120,200,230,.22);padding:10px}
.qcell{border-radius:10px;background:#0d1728;box-shadow:inset 0 2px 6px rgba(0,0,0,.6)}
.qchip{filter:drop-shadow(0 2px 4px rgba(0,0,0,.5)) drop-shadow(0 0 7px rgba(90,220,210,.35))}
""")

_t("fox-and-hounds", """
/* frosty midnight forest */
.wgrid .cell.light{background:linear-gradient(150deg,#dfe8f2,#b9c8da)}
.wgrid .cell.dark{background:linear-gradient(150deg,#44587a,#31415f)}
.ffox{filter:drop-shadow(0 0 10px rgba(255,140,70,.75)) drop-shadow(0 2px 3px rgba(0,0,0,.5))}
.fhound{filter:drop-shadow(0 2px 3px rgba(0,0,0,.55))}
.fgoal{box-shadow:inset 0 0 14px rgba(140,220,170,.5)}
""")

_t("nim", """
/* matchsticks on oak table */
.board{background:linear-gradient(160deg,#3a2a18,#241806);border-radius:14px;box-shadow:0 10px 26px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,200,120,.15);padding:14px}
.pip{background:linear-gradient(180deg,#f7c66b 55%,#c98d3f 55%,#8a5a26);border-radius:3px;box-shadow:0 2px 4px rgba(0,0,0,.55)}
.heap .hcount{color:#ffd98a}
""")

_t("chomp", """
/* chocolate bar */
.ch-grid{background:linear-gradient(160deg,#5a3a22,#3c2413);border-radius:12px;padding:8px;box-shadow:0 10px 26px rgba(0,0,0,.5),inset 0 0 0 2px rgba(255,220,170,.12)}
.ch-cell{background:linear-gradient(150deg,#8a5a34,#6b4023);border-radius:6px;box-shadow:inset 0 2px 3px rgba(255,220,170,.2),0 2px 4px rgba(0,0,0,.4)}
.ch-cell:hover{filter:brightness(1.12)}
.ch-gone{background:#150d06!important;box-shadow:inset 0 2px 6px rgba(0,0,0,.8)!important}
.ch-poison{background:radial-gradient(circle,#c8402a,#7a1e0e)!important;box-shadow:0 0 12px rgba(230,80,50,.6)!important}
""")

# ============================ CARDS ============================
_t("spider", """
.tabs{color:#8fb7e8}
.wovl .box{background:linear-gradient(180deg,#1a2540,#121a30)}
""")

_t("freecell", """
.fnd{box-shadow:0 0 0 1px rgba(217,164,65,.5),inset 0 0 14px rgba(217,164,65,.14);border-radius:9px}
.top{background:linear-gradient(160deg,rgba(28,42,70,.85),rgba(18,28,50,.85));border:1px solid rgba(217,164,65,.3);border-radius:14px;padding:10px;box-shadow:0 6px 18px rgba(0,0,0,.35)}
""")

_t("pyramid", """
/* desert dusk */
.pyr{filter:drop-shadow(0 10px 24px rgba(255,170,80,.18))}
.pyr-slot{background:rgba(8,12,24,.55);border:1px dashed rgba(217,164,65,.4);border-radius:9px}
.wcard.back{background:linear-gradient(150deg,#7a5a34,#57401f 55%,#6b4e2a);border-color:rgba(255,220,150,.5)}
""")

_t("tripeaks", """
.tslot{background:rgba(8,12,24,.55);border:1px dashed rgba(217,164,65,.4);border-radius:9px}
.wcard.back{background:linear-gradient(150deg,#2c4a66,#1b3048 55%,#27415c);border-color:rgba(150,200,230,.45)}
""")

_t("golf", """
.golf-empty{border:1px dashed rgba(217,164,65,.4);border-radius:8px}
.playable{box-shadow:0 0 12px rgba(255,225,140,.5)}
""")

_t("clock", """
.cgrid{background:radial-gradient(circle at 50% 42%,#1e2c4c,#121c34 70%);border-radius:50%;box-shadow:0 10px 30px rgba(0,0,0,.5),inset 0 0 0 2px rgba(217,164,65,.4),inset 0 0 24px rgba(0,0,0,.4);padding:12px}
.ccell{border-radius:50%}
.cur{box-shadow:0 0 14px rgba(255,215,120,.6)}
""")

_t("hokm", """
/* Persian tea-house: copper + turquoise */
.hk-hand{background:linear-gradient(165deg,rgba(38,58,66,.85),rgba(22,36,44,.85));border:1px solid rgba(63,184,175,.4);border-radius:16px;padding:12px;box-shadow:0 8px 24px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.06)}
.hk-suit{color:#3fb8af;font-weight:800}
.hk-info{background:rgba(12,22,30,.7);border:1px solid rgba(63,184,175,.35);border-radius:12px;padding:8px 12px}
.hk-slot{border:1px dashed rgba(63,184,175,.4);border-radius:10px}
""")

_t("pasoor", """
.ps-row{background:linear-gradient(165deg,rgba(40,44,72,.8),rgba(24,28,50,.8));border:1px solid rgba(217,164,65,.35);border-radius:16px;padding:12px}
.ps-lbl{color:#e8c073}
.ps-dim{opacity:.45}
""")

_t("thirty-one", """
.t31{background:linear-gradient(165deg,rgba(34,52,44,.85),rgba(20,32,26,.85));border:1px solid rgba(103,185,138,.4);border-radius:16px;padding:14px;box-shadow:0 10px 28px rgba(0,0,0,.45)}
.t31-pile{border:1px dashed rgba(103,185,138,.45);border-radius:10px}
""")

_t("video-poker", """
.vp{background:linear-gradient(165deg,#241a3e,#150f28);border:1px solid rgba(167,139,250,.4);border-radius:16px;padding:14px;box-shadow:0 10px 30px rgba(0,0,0,.5),inset 0 0 26px rgba(120,90,220,.12)}
.vp-cell{border-radius:10px;background:rgba(10,7,20,.5)}
.vp-hold{box-shadow:0 0 14px rgba(167,139,250,.65);outline:2px solid #a78bfa}
""")

_t("higher-lower", """
.hl{background:linear-gradient(165deg,rgba(36,48,80,.85),rgba(22,30,52,.85));border:1px solid rgba(217,164,65,.35);border-radius:18px;padding:18px;box-shadow:0 12px 30px rgba(0,0,0,.45)}
.hl-msg{color:#e8c073}
""")

_t("crazy-eights", """
.suit{font-size:1.3rem;text-shadow:0 0 12px rgba(255,225,150,.4)}
.tslot{border:1px dashed rgba(217,164,65,.45);border-radius:10px}
""")

_t("war", """
.vs{color:#e26d5c;font-weight:900;text-shadow:0 0 14px rgba(226,109,92,.5)}
.pile{background:rgba(10,14,26,.6);border:1px dashed rgba(217,164,65,.4);border-radius:12px}
""")

# ============================ PUZZLE ============================
_t("hanoi", """
/* brass poles + golden discs on cedar base */
.h-wrap{filter:drop-shadow(0 12px 26px rgba(0,0,0,.5))}
.h-base{background:linear-gradient(180deg,#7a5228,#54371a);border-radius:8px;box-shadow:inset 0 2px 0 rgba(255,220,160,.25),0 4px 10px rgba(0,0,0,.5)}
.h-pole{background:linear-gradient(90deg,#8a6a34,#c9a355 45%,#8a6a34);border-radius:4px;box-shadow:0 0 10px rgba(230,190,110,.25)}
.h-disk{background:linear-gradient(180deg,#f2c979,#c9922f 60%,#a06e1e);border-radius:9px;box-shadow:0 3px 6px rgba(0,0,0,.5),inset 0 2px 0 rgba(255,240,190,.5)}
.h-sel{box-shadow:0 0 16px rgba(255,220,130,.8),0 3px 6px rgba(0,0,0,.5)}
""")

_t("8queens", """
/* marble chessboard */
.q-board{border-radius:12px;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,.55),0 0 0 4px rgba(20,30,52,.95),0 0 0 5px rgba(217,164,65,.35)}
.q-light{background:linear-gradient(150deg,#f2ead6,#ddd2b4)}
.q-dark{background:linear-gradient(150deg,#41527a,#2f3d5e)}
.q-cell{font-size:26px}
.q-ok{text-shadow:0 0 14px rgba(120,230,170,.8),0 2px 3px rgba(0,0,0,.4)}
.q-bad{text-shadow:0 0 14px rgba(255,110,90,.8),0 2px 3px rgba(0,0,0,.4)}
""")

_t("simon", """
/* neon pads */
.sgrid{gap:10px}
.pad{border-radius:16px;box-shadow:0 6px 18px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,255,255,.1);opacity:.55;transition:.15s}
.pad.lit{opacity:1;transform:scale(1.04)}
""")

_t("water-sort", """
/* laboratory glass */
.bw{filter:drop-shadow(0 6px 14px rgba(0,0,0,.45))}
.sg{border-radius:0 0 10px 10px;box-shadow:inset 0 -2px 5px rgba(0,0,0,.25),inset 0 2px 3px rgba(255,255,255,.28)}
.wb{background:linear-gradient(180deg,rgba(210,230,240,.16),rgba(210,230,240,.05));border:1px solid rgba(200,225,240,.45);border-radius:0 0 12px 12px;box-shadow:inset 0 0 10px rgba(255,255,255,.1)}
.lv{transition:.12s}
""")

_t("mastermind", """
/* retro codebreaker console */
.grow,.hrow{background:linear-gradient(160deg,rgba(30,40,66,.9),rgba(20,28,48,.9));border:1px solid rgba(217,164,65,.3);border-radius:14px;padding:8px}
.peg{border-radius:50%;box-shadow:inset 0 -2px 4px rgba(0,0,0,.35),0 1px 3px rgba(0,0,0,.5),inset 0 2px 2px rgba(255,255,255,.3)}
.selc{box-shadow:0 0 12px rgba(255,215,120,.7)!important}
.hnum{color:#e8c073}
""")

_t("sokoban", """
/* warehouse: brick, crates, glowing goals */
.sokboard{background:#1a1410;border:2px solid rgba(217,164,65,.35);border-radius:12px;padding:6px;box-shadow:0 12px 30px rgba(0,0,0,.55),inset 0 0 30px rgba(0,0,0,.5)}
.swall{background:repeating-linear-gradient(0deg,#5a4432 0 14px,#4a3626 14px 16px);box-shadow:inset 0 0 0 1px rgba(0,0,0,.35)}
.sbox{background:linear-gradient(150deg,#b98744,#8a5f2a);border-radius:5px;box-shadow:inset 0 0 0 2px rgba(70,45,15,.6),inset 0 0 8px rgba(255,220,160,.2),0 2px 4px rgba(0,0,0,.5)}
.sboxon{box-shadow:inset 0 0 0 2px rgba(70,45,15,.6),0 0 14px rgba(140,230,170,.6),0 2px 4px rgba(0,0,0,.5)}
.sgoal{background:radial-gradient(circle,rgba(120,230,170,.3),transparent 70%)}
.splayer{filter:drop-shadow(0 0 8px rgba(255,210,120,.7)) drop-shadow(0 2px 3px rgba(0,0,0,.5))}
""")

_t("rush-hour", """
/* parking lot asphalt */
.rhboard{background:linear-gradient(160deg,#2a2f38,#1d2129);border:2px solid rgba(217,164,65,.35);border-radius:12px;padding:8px;box-shadow:0 12px 30px rgba(0,0,0,.55),inset 0 0 24px rgba(0,0,0,.45)}
.rhveh{border-radius:8px;box-shadow:0 3px 7px rgba(0,0,0,.5),inset 0 2px 0 rgba(255,255,255,.3),inset 0 -3px 5px rgba(0,0,0,.3)}
.rhred{background:linear-gradient(160deg,#ff7a5c,#d23c22)!important;box-shadow:0 3px 9px rgba(0,0,0,.5),inset 0 2px 0 rgba(255,255,255,.35),0 0 14px rgba(255,110,70,.4)!important}
.rhsel{outline:2px solid rgba(255,230,160,.85);outline-offset:2px}
.rhexit{background:repeating-linear-gradient(45deg,#e8c073 0 8px,#b98d3f 8px 16px);border-radius:4px}
""")

_t("lights-out", """
/* neon grid */
.l-grid{background:#05070d;border-radius:14px;padding:10px;box-shadow:0 12px 30px rgba(0,0,0,.6),inset 0 0 20px rgba(0,0,0,.7),0 0 0 1px rgba(90,220,210,.2)}
.l-on{background:radial-gradient(circle,#5ee8d8,#1a9e90)!important;box-shadow:0 0 16px rgba(94,232,216,.75),inset 0 0 6px rgba(255,255,255,.4)!important;border-radius:8px}
.l-off{background:#0c1520;border-radius:8px;box-shadow:inset 0 2px 6px rgba(0,0,0,.7)}
""")

_t("flood", """
.fgrid{border-radius:12px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.5),0 0 0 2px rgba(255,255,255,.12)}
.fpb{border-radius:10px;box-shadow:0 3px 8px rgba(0,0,0,.45),inset 0 2px 0 rgba(255,255,255,.3);transition:transform .1s}
.fpb:active{transform:scale(.94)}
""")

_t("peg", """
/* mahogany board, brass pegs */
.pgrid{background:linear-gradient(160deg,#5a3a22,#3a2412);border-radius:50%;padding:16px;box-shadow:0 14px 32px rgba(0,0,0,.55),inset 0 2px 0 rgba(255,215,150,.2),inset 0 -4px 10px rgba(0,0,0,.4)}
.hole{background:radial-gradient(circle,#1c0f05,#0e0702 75%);box-shadow:inset 0 3px 7px rgba(0,0,0,.85),0 1px 0 rgba(255,215,150,.12);border-radius:50%}
.peg{background:radial-gradient(circle at 35% 30%,#ffd98a,#c9922f 60%,#8a5a20);border-radius:50%;box-shadow:0 2px 5px rgba(0,0,0,.6),0 0 8px rgba(255,205,120,.3)}
.tgt{box-shadow:0 0 14px rgba(255,225,140,.75),inset 0 3px 7px rgba(0,0,0,.8)}
""")

_t("blockudoku", """
/* frosted glass blocks */
.bgrid{background:rgba(10,16,30,.75);border:1px solid rgba(150,200,230,.25);border-radius:14px;padding:6px;box-shadow:0 12px 30px rgba(0,0,0,.5),inset 0 0 18px rgba(0,0,0,.35)}
.bcell{border-radius:5px;background:#0d1626;box-shadow:inset 0 1px 3px rgba(0,0,0,.6)}
.bcell[class*=" b1"],.bfull{filter:saturate(1.15)}
.bfull{box-shadow:0 0 10px rgba(120,200,255,.35)}
.bmini{filter:drop-shadow(0 2px 5px rgba(0,0,0,.5))}
""")

_t("p15", """
/* ivory & walnut sliding tiles */
.p15wrap{background:linear-gradient(160deg,#4a3418,#2e1f0c);border-radius:14px;padding:8px;box-shadow:0 14px 32px rgba(0,0,0,.55),inset 0 0 0 2px rgba(255,215,150,.14)}
.p15tile{background:linear-gradient(160deg,#f6eeda,#e2d4b0);color:#3a2a10;border-radius:9px;box-shadow:0 3px 7px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.7);font-weight:800;transition:transform .12s}
""")

_t("maze", """
/* torch-lit labyrinth */
.m-grid{background:#14100a;border-radius:12px;box-shadow:0 12px 30px rgba(0,0,0,.55),inset 0 0 24px rgba(0,0,0,.6),0 0 0 1px rgba(217,164,65,.3);padding:8px}
.m-w{background:linear-gradient(150deg,#6b5436,#4a3822);box-shadow:inset 0 0 0 1px rgba(0,0,0,.35)}
.m-player{filter:drop-shadow(0 0 10px rgba(255,200,110,.85))}
.m-exit{background:radial-gradient(circle,rgba(140,240,180,.5),transparent 70%);box-shadow:0 0 16px rgba(140,240,180,.6)}
""")

_t("calc24", """
/* chalkboard math */
.trow,.solbox{background:linear-gradient(160deg,#20362e,#142620);border:1px solid rgba(120,220,170,.3);border-radius:14px;padding:10px;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 0 20px rgba(0,0,0,.3)}
.tile{background:linear-gradient(160deg,#f2ecd8,#ddd4b8);color:#1e2a24;border-radius:9px;box-shadow:0 3px 6px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.6);font-weight:800}
.op{color:#8fe8c0;font-weight:800}
""")

_t("kakuro", """
/* newsprint puzzle */
.kg{background:linear-gradient(160deg,#f2efe4,#e3dfc9);border-radius:10px;padding:8px;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 0 0 1px rgba(90,85,60,.3)}
.kb{background:#fbf9f0;color:#20242e;box-shadow:inset 0 0 0 1px rgba(60,60,50,.35)}
.kc{color:#20242e}
""")

_t("memory-grid", """
/* Persian card backs */
.mc{border-radius:10px;background:linear-gradient(150deg,#31406b,#1d2a4a);border:1px solid rgba(217,164,65,.5);box-shadow:0 3px 7px rgba(0,0,0,.5),inset 0 0 12px rgba(217,164,65,.12);transition:transform .18s}
.mc:hover{transform:translateY(-3px)}
""")

_t("nonogram", """
/* graph paper */
.ngrid{background:linear-gradient(160deg,#f0ecdb,#e0dcc6);border-radius:10px;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 0 0 1px rgba(90,85,60,.3);padding:6px}
.ncell{box-shadow:inset 0 0 0 1px rgba(90,85,60,.28);border-radius:3px;background:#fbf9f0}
""")

# ============================ WORD ============================
_t("wordle", """
/* classic tiles */
.wboard{gap:6px}
.wcell{border-radius:8px;box-shadow:inset 0 0 0 2px rgba(140,150,175,.4);font-weight:800;transition:.18s}
.wcell.kb-g{background:linear-gradient(160deg,#67b98a,#3f8f62)!important;box-shadow:none!important;color:#0d2015!important}
.wcell.kb-y{background:linear-gradient(160deg,#e2b95c,#c2922e)!important;box-shadow:none!important;color:#241a04!important}
.wcell.kb-k{background:linear-gradient(160deg,#3a4460,#2a3248)!important;box-shadow:none!important}
.kbwrap .sec{min-height:46px}
""")

_t("hangman", """
/* chalkboard */
body[data-slug="hangman"]{background:
 radial-gradient(760px 380px at 50% -70px,rgba(46,84,66,.5),transparent 66%),
 linear-gradient(168deg,#1b2b24,#12211b 58%,#0d1713)}
.hm{filter:drop-shadow(0 0 4px rgba(220,240,230,.25))}
.hl{border-bottom:3px solid rgba(232,192,115,.65);min-width:20px;text-align:center;font-weight:800;font-size:1.25rem;color:#f3ead8}
.hl.lost{color:#e26d5c;border-color:rgba(226,109,92,.7)}
.chip{background:rgba(20,32,28,.85);border:1px solid rgba(103,185,138,.4);border-radius:10px;padding:5px 10px;color:#a8d8be}
""")

_t("word-search", """
/* letter-cube grid */
.wgrid{border-color:rgba(217,164,65,.6);box-shadow:0 10px 28px rgba(0,0,0,.5),0 0 0 5px rgba(70,45,15,.9),0 0 0 6px rgba(217,164,65,.3)}
.wgrid .cell{background:linear-gradient(160deg,#f2ead6,#ddd2b4)!important;color:#2c2414;font-weight:800;border-radius:3px;box-shadow:inset 0 -2px 3px rgba(120,90,40,.3)}
.wgrid .cell.sel{background:linear-gradient(160deg,#ffe3a0,#eec36a)!important}
.wgrid .cell.fnd{background:linear-gradient(160deg,#a8dcb8,#6cb98a)!important;color:#0d2015}
.chip.fnd{background:rgba(103,185,138,.2);border-color:rgba(103,185,138,.55);color:#a8dcb8}
.chip.danger{background:rgba(226,109,92,.16);border-color:rgba(226,109,92,.5);color:#eba292}
""")

_t("anagram", """
/* wooden scrabble tiles */
.tile{background:linear-gradient(160deg,#efdca8,#cfb070);color:#3a2a10;border-radius:8px;box-shadow:0 3px 6px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.55),inset 0 -2px 3px rgba(120,85,30,.4);font-weight:800;transition:transform .12s}
.tile:hover{transform:translateY(-3px)}
.tile.used{opacity:.35;transform:none}
.achip{background:rgba(20,32,58,.85);border:1px solid rgba(217,164,65,.4);border-radius:10px}
""")

_t("word-chain", """
/* dialogue bubbles */
.prevw{background:rgba(18,28,50,.85);border:1px solid rgba(63,184,175,.35);border-radius:14px;padding:8px 14px;box-shadow:0 4px 12px rgba(0,0,0,.35)}
.typed{background:linear-gradient(160deg,#22406a,#16294a);border:1px solid rgba(90,170,230,.45);border-radius:14px;padding:10px 14px;box-shadow:inset 0 2px 8px rgba(0,0,0,.4)}
.scor{color:#e8c073}
""")

_t("proverb", """
/* spotlight quiz stage */
.qpanel{background:linear-gradient(165deg,rgba(44,36,72,.9),rgba(26,22,46,.9));border:1px solid rgba(217,164,65,.45);border-radius:18px;padding:16px;box-shadow:0 12px 32px rgba(0,0,0,.5),0 0 40px rgba(120,90,220,.12)}
.opt{background:linear-gradient(160deg,#1c2a4c,#142038);border:1px solid rgba(217,164,65,.4);border-radius:13px;transition:.14s}
.opt:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,.45)}
.opt.correct{background:linear-gradient(160deg,#2c6b4a,#1c4a32)!important;border-color:rgba(120,230,170,.7)!important}
.feedback.ok{color:#8fe0b0}
.feedback.no{color:#eba292}
""")

# ============================ LUCK ============================
_t("yahtzee", """
/* craps table + glossy dice */
.sheet{background:linear-gradient(160deg,rgba(22,50,40,.9),rgba(14,34,26,.9));border:1px solid rgba(103,185,138,.4);border-radius:14px;padding:10px;box-shadow:0 10px 28px rgba(0,0,0,.5),inset 0 0 24px rgba(0,0,0,.3)}
.die{background:linear-gradient(150deg,#fffdf4,#e2d7b8);border-radius:11px;box-shadow:0 4px 9px rgba(0,0,0,.5),inset 0 -3px 5px rgba(0,0,0,.14),inset 0 2px 2px rgba(255,255,255,.8);color:#20242e;font-weight:800}
.die.hold{outline:3px solid rgba(232,192,115,.8);box-shadow:0 0 14px rgba(232,192,115,.5)}
.row.best{background:rgba(232,192,115,.12);border-radius:8px}
""")

_t("slots", """
/* neon cabinet */
.machine{background:linear-gradient(165deg,#3a1840,#220e28);border:2px solid rgba(255,110,180,.5);border-radius:20px;padding:14px;box-shadow:0 16px 40px rgba(0,0,0,.6),0 0 30px rgba(255,110,180,.18),inset 0 1px 0 rgba(255,255,255,.1)}
.reels{background:#0c0612;border-radius:12px;box-shadow:inset 0 4px 14px rgba(0,0,0,.8);padding:10px}
.reel{background:linear-gradient(180deg,#f6efd8,#e0d4b0);color:#2c2038;border-radius:8px;font-weight:800;box-shadow:inset 0 -2px 4px rgba(0,0,0,.2)}
.pline{background:linear-gradient(90deg,transparent,rgba(255,110,180,.9),transparent);box-shadow:0 0 12px rgba(255,110,180,.8)}
.paytable{color:#d8a8c8}
""")

_t("wheel", """
/* carnival wheel */
.wheel{filter:drop-shadow(0 14px 30px rgba(0,0,0,.55)) drop-shadow(0 0 22px rgba(255,180,80,.2))}
.seg{stroke:rgba(10,8,16,.55);stroke-width:1}
.hchip{background:rgba(30,22,48,.9);border:1px solid rgba(217,164,65,.4);border-radius:10px}
""")

_t("chuck-a-luck", """
.dice3{background:linear-gradient(160deg,rgba(30,22,48,.9),rgba(18,14,30,.9));border:1px solid rgba(217,164,65,.45);border-radius:16px;padding:12px;box-shadow:0 10px 28px rgba(0,0,0,.5),inset 0 0 22px rgba(0,0,0,.4)}
.face,.faces{background:linear-gradient(150deg,#fffdf4,#e2d7b8);color:#20242e;border-radius:10px;box-shadow:0 3px 7px rgba(0,0,0,.5),inset 0 2px 2px rgba(255,255,255,.75)}
""")

_t("pig", """
/* warm barnyard */
.diebig{background:linear-gradient(150deg,#fffdf4,#e6dabc);border-radius:16px;box-shadow:0 6px 14px rgba(0,0,0,.5),inset 0 -4px 6px rgba(0,0,0,.15),inset 0 3px 3px rgba(255,255,255,.8);color:#262a34;font-weight:800}
.pcard{background:linear-gradient(160deg,rgba(50,38,26,.9),rgba(32,24,16,.9));border:1px solid rgba(232,192,115,.35);border-radius:14px;padding:12px}
""")

_t("lcr", """
.chip{border-radius:50%;box-shadow:0 3px 6px rgba(0,0,0,.5),inset 0 2px 2px rgba(255,255,255,.35),inset 0 -2px 3px rgba(0,0,0,.3)}
.die{background:linear-gradient(150deg,#fffdf4,#e6dabc);border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,.5);color:#22262e;font-weight:800}
.pcard.active{outline:2px solid rgba(232,192,115,.8);box-shadow:0 0 14px rgba(232,192,115,.4)}
""")

_t("rps", """
/* arena faceoff */
.faceoff{background:radial-gradient(circle at 50% 40%,rgba(60,44,90,.55),transparent 70%);border-radius:20px;padding:14px}
.dot,.side{filter:drop-shadow(0 4px 8px rgba(0,0,0,.5))}
.mid{color:#e8c073;font-weight:900}
.trail{opacity:.85}
""")

# ============================ ARCADE (canvas frames) ============================
_t("flappy", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(140,190,255,.4),0 0 0 6px rgba(15,22,40,.9)}""")
_t("invaders", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.6),0 0 0 2px rgba(63,184,175,.5),0 0 0 6px rgba(10,16,30,.95),0 0 30px rgba(63,184,175,.18)}""")
_t("asteroids", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.6),0 0 0 2px rgba(150,170,210,.45),0 0 0 6px rgba(8,12,24,.95)}""")
_t("meteor", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.6),0 0 0 2px rgba(255,140,90,.45),0 0 0 6px rgba(10,8,16,.95),0 0 30px rgba(255,120,60,.15)}""")
_t("runner", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(232,192,115,.45),0 0 0 6px rgba(20,14,8,.95)}""")
_t("frogger", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(103,185,138,.45),0 0 0 6px rgba(10,18,14,.95)}""")
_t("coin-catch", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(255,215,120,.45),0 0 0 6px rgba(16,14,8,.95),0 0 26px rgba(255,200,90,.15)}""")
_t("kite", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.55),0 0 0 2px rgba(140,200,255,.45),0 0 0 6px rgba(12,18,32,.95)}""")
_t("stacker", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.6),0 0 0 2px rgba(167,139,250,.5),0 0 0 6px rgba(12,10,24,.95),0 0 30px rgba(167,139,250,.2)}""")
_t("dodge", """canvas{box-shadow:0 14px 36px rgba(0,0,0,.6),0 0 0 2px rgba(226,109,92,.45),0 0 0 6px rgba(14,10,14,.95)}""")
_t("whack", """
.wgrid{border-color:rgba(103,185,138,.5);box-shadow:0 10px 28px rgba(0,0,0,.5),0 0 0 5px rgba(24,40,30,.95),0 0 0 6px rgba(103,185,138,.3);background:linear-gradient(160deg,#2c4434,#1a2c20);gap:8px;padding:8px}
.wgrid .cell{border-radius:50%;background:radial-gradient(circle at 45% 35%,#3a5844,#22362a 75%);box-shadow:inset 0 4px 9px rgba(0,0,0,.7),0 1px 0 rgba(255,255,255,.1)}
.gbtn{border-radius:14px}
""")
_t("aim", """
.aboard{background:radial-gradient(circle at 50% 42%,#16324a,#0b1c2c 75%);border-radius:50%;box-shadow:0 12px 30px rgba(0,0,0,.55),inset 0 0 0 2px rgba(140,200,230,.3),inset 0 0 40px rgba(0,0,0,.5)}
.atgt{filter:drop-shadow(0 0 10px rgba(255,140,90,.6)) drop-shadow(0 3px 4px rgba(0,0,0,.5))}
""")
_t("reaction", """
.rscreen{background:linear-gradient(160deg,#10263e,#0a1828);border:1px solid rgba(90,170,230,.4);border-radius:16px;box-shadow:inset 0 0 30px rgba(0,0,0,.5),0 8px 22px rgba(0,0,0,.4)}
.rchip{background:#10263e;border:1px solid rgba(90,170,230,.4);border-radius:10px}
""")
_t("cups", """
/* velvet table */
body[data-slug="cups"]{background:
 radial-gradient(900px 460px at 50% 115%,rgba(90,30,50,.5),transparent 62%),
 linear-gradient(168deg,#171126,#0e0a18 58%,#0a0712)}
.cupw{filter:drop-shadow(0 6px 10px rgba(0,0,0,.55));transition:transform .2s}
.cupb{background:linear-gradient(160deg,#8a2f2f,#5c1c1c);border-radius:8px 8px 12px 12px;box-shadow:inset 0 2px 3px rgba(255,255,255,.2),inset 0 -4px 8px rgba(0,0,0,.4)}
.ball{background:radial-gradient(circle at 35% 30%,#ffe6a8,#d9a441 65%,#8a5a20);border-radius:50%;box-shadow:0 0 10px rgba(255,210,120,.5),0 2px 4px rgba(0,0,0,.5)}
""")
_t("typing", """
.tbox{background:linear-gradient(160deg,#1a2440,#121a30);border:1px solid rgba(90,170,230,.35);border-radius:14px;padding:14px;box-shadow:0 8px 24px rgba(0,0,0,.45),inset 0 2px 8px rgba(0,0,0,.4)}
.tinp{background:#0d1526;border:1px solid rgba(90,170,230,.4);border-radius:10px;color:#f3ead8;font-family:inherit}
.tinp:focus{outline:2px solid rgba(63,184,175,.6)}
.ch.todo{color:#7285a8}
.ch.bad{color:#e26d5c;background:rgba(226,109,92,.12);border-radius:4px}
""")
_t("stroop", """
.word{text-shadow:0 0 22px rgba(255,255,255,.14);font-weight:900;letter-spacing:1px}
.cbtn{border-radius:14px}
""")
_t("math-sprint", """
.mtext{font-weight:900;letter-spacing:.5px;text-shadow:0 0 18px rgba(232,192,115,.25)}
""")
_t("digits", """
.ddisp{background:linear-gradient(160deg,#1a2440,#121a30);border:1px solid rgba(232,192,115,.4);border-radius:14px;box-shadow:inset 0 2px 10px rgba(0,0,0,.5);letter-spacing:8px;font-weight:800;color:#ffe1a0}
.dkey{border-radius:11px}
""")
