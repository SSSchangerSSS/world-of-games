# -*- coding: utf-8 -*-
"""Canvas scene art upgrades for legacy arcade games (snake, breakout, pong, alborz-jump).
Targeted string patches on index.html — fail loudly if a patch doesn't apply."""
import io, os

ROOT = "/home/z/my-project/pages-site/games"

def patch(slug, pairs):
    p = os.path.join(ROOT, slug, "index.html")
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        if old not in s:
            raise SystemExit("PATCH MISS in %s: %r" % (slug, old[:70]))
        s = s.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8").write(s)
    print("patched", slug)

# ---------------- SNAKE: jungle scene + glowing food ----------------
patch("snake", [
    ("""    ctx.clearRect(0, 0, 420, 560);
    ctx.fillStyle = '#14203a';
    rr(BX, BY, COLS * CELL, ROWS * CELL, 10);
    ctx.fill();
    ctx.strokeStyle = 'rgba(217,164,65,.07)';""",
     """    ctx.clearRect(0, 0, 420, 560);
    var bg = ctx.createLinearGradient(0, 0, 0, 560);
    bg.addColorStop(0, '#16301f');
    bg.addColorStop(.55, '#0f2317');
    bg.addColorStop(1, '#0a1810');
    ctx.fillStyle = bg;
    rr(BX, BY, COLS * CELL, ROWS * CELL, 10);
    ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.03)';
    for (var si = 0; si < 26; si++) {
      var sx = (si * 97) % (COLS * CELL), sy = (si * 53) % (ROWS * CELL);
      ctx.fillRect(BX + sx, BY + sy, 1.6, 1.6);
    }
    ctx.strokeStyle = 'rgba(103,185,138,.09)';"""),
    ("""    if (food) {
      ctx.fillStyle = '#e26d5c';
      ctx.beginPath();
      ctx.arc(BX + food.x * CELL + CELL / 2, BY + food.y * CELL + CELL / 2, CELL * .32, 0, Math.PI * 2);
      ctx.fill();
    }""",
     """    if (food) {
      var fx = BX + food.x * CELL + CELL / 2, fy = BY + food.y * CELL + CELL / 2;
      var fg = ctx.createRadialGradient(fx, fy, 1, fx, fy, CELL * 1.15);
      fg.addColorStop(0, 'rgba(255,140,90,.5)');
      fg.addColorStop(1, 'rgba(255,140,90,0)');
      ctx.fillStyle = fg;
      ctx.beginPath(); ctx.arc(fx, fy, CELL * 1.15, 0, Math.PI * 2); ctx.fill();
      var fgr = ctx.createRadialGradient(fx - 2, fy - 3, 1, fx, fy, CELL * .34);
      fgr.addColorStop(0, '#ffb08a');
      fgr.addColorStop(.6, '#e26d5c');
      fgr.addColorStop(1, '#a83c2c');
      ctx.fillStyle = fgr;
      ctx.beginPath(); ctx.arc(fx, fy, CELL * .32, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.55)';
      ctx.beginPath(); ctx.arc(fx - 2.5, fy - 3, 1.6, 0, Math.PI * 2); ctx.fill();
    }"""),
    ("""      ctx.fillStyle = i === 0 ? '#e8c073' : '#3fb8af';
      rr(BX + s.x * CELL + inset, BY + s.y * CELL + inset, CELL - inset * 2, CELL - inset * 2, 6);
      ctx.fill();""",
     """      if (i === 0) { ctx.fillStyle = '#f2cf82'; }
      else {
        var sg = ctx.createLinearGradient(0, 0, CELL, CELL);
        var sh = 165 + Math.round(28 * t);
        sg.addColorStop(0, 'hsl(' + sh + ',52%,46%)');
        sg.addColorStop(1, 'hsl(' + sh + ',58%,32%)');
        ctx.fillStyle = sg;
      }
      ctx.shadowColor = i === 0 ? 'rgba(232,192,115,.6)' : 'rgba(63,184,175,.35)';
      ctx.shadowBlur = i === 0 ? 10 : 5;
      rr(BX + s.x * CELL + inset, BY + s.y * CELL + inset, CELL - inset * 2, CELL - inset * 2, 6);
      ctx.fill();
      ctx.shadowBlur = 0;"""),
])

# ---------------- BREAKOUT: neon bricks with shine + starfield ----------------
patch("breakout", [
    ("ctx.fillStyle = '#0b1220';", "var bg=ctx.createLinearGradient(0,0,0,560);bg.addColorStop(0,'#1a1030');bg.addColorStop(.6,'#0f1526');bg.addColorStop(1,'#0a0e1a');ctx.fillStyle=bg;"),
])

# ---------------- PONG: neon court ----------------
patch("pong", [
    ("ctx.fillStyle = '#0b1220';", "var bg=ctx.createLinearGradient(0,0,0,560);bg.addColorStop(0,'#0e2226');bg.addColorStop(.5,'#0b1a20');bg.addColorStop(1,'#081114');ctx.fillStyle=bg;"),
])

# ---------------- ALBORZ-JUMP: mountain sky ----------------
patch("alborz-jump", [
    ("ctx.fillStyle = '#1a2848';", "var bg=ctx.createLinearGradient(0,0,0,560);bg.addColorStop(0,'#27476e');bg.addColorStop(.5,'#1a3352');bg.addColorStop(1,'#101f36');ctx.fillStyle=bg;"),
])

print("canvas patches done")
