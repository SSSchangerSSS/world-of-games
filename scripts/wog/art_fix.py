# -*- coding: utf-8 -*-
"""Fix g2 art assignment + finish g3/j_luck patches."""
import io

def patch_file(path, pairs):
    s = io.open(path, encoding="utf-8").read()
    changed = 0
    for old, new in pairs:
        if old not in s:
            print("  SKIP (already applied or missing): %s..." % old[:50])
            continue
        s = s.replace(old, new, 1)
        changed += 1
    io.open(path, "w", encoding="utf-8").write(s)
    print("patched", path, "(%d applied)" % changed)

G2 = "games/g2_arcade.py"
G3 = "games/g3_arcade.py"
JL = "games/j_luck.py"

# meteor (line ~39, uses L.H): give it the nebula treatment
# stacker (currently nebula 'mg'): swap to neon tower
# kite (currently neon 'stg'): swap to day sky
patch_file(G2, [
    # 1) meteor bg -> nebula
    ("ctx.fillStyle='#0b1226';ctx.fillRect(0,0,L.W,L.H);",
     "var mg=ctx.createLinearGradient(0,0,0,L.H);mg.addColorStop(0,'#0a0e24');mg.addColorStop(.6,'#141031');mg.addColorStop(1,'#221233');ctx.fillStyle=mg;ctx.fillRect(0,0,L.W,L.H);"
     "var ng=ctx.createRadialGradient(L.W*.7,110,8,L.W*.7,110,190);ng.addColorStop(0,'rgba(226,109,92,.16)');ng.addColorStop(1,'rgba(226,109,92,0)');ctx.fillStyle=ng;ctx.fillRect(0,0,L.W,L.H);"),
    # 2) stacker: nebula (mg, 440) -> neon tower
    ("var mg=ctx.createLinearGradient(0,0,0,440);mg.addColorStop(0,'#0a0e24');mg.addColorStop(.6,'#141031');mg.addColorStop(1,'#221233');ctx.fillStyle=mg;ctx.fillRect(0,0,L.W,440);",
     "var stg=ctx.createLinearGradient(0,0,0,440);stg.addColorStop(0,'#0c1128');stg.addColorStop(1,'#160f2e');ctx.fillStyle=stg;ctx.fillRect(0,0,L.W,440);"
     "var slg=ctx.createRadialGradient(L.W/2,380,10,L.W/2,380,240);slg.addColorStop(0,'rgba(63,184,175,.15)');slg.addColorStop(1,'rgba(63,184,175,0)');ctx.fillStyle=slg;ctx.fillRect(0,0,L.W,440);"),
    # 3) kite: neon (stg, 500) -> day sky
    ("var stg=ctx.createLinearGradient(0,0,0,500);stg.addColorStop(0,'#0c1128');stg.addColorStop(1,'#160f2e');ctx.fillStyle=stg;ctx.fillRect(0,0,L.W,500);",
     "var ky=ctx.createLinearGradient(0,0,0,500);ky.addColorStop(0,'#274b76');ky.addColorStop(.6,'#4a6a92');ky.addColorStop(1,'#7aa0b8');ctx.fillStyle=ky;ctx.fillRect(0,0,L.W,500);"
     "ctx.fillStyle='rgba(255,255,255,.12)';ctx.beginPath();ctx.ellipse(L.W*.2,90,44,11,0,0,6.283);ctx.ellipse(L.W*.28,96,32,8,0,0,6.283);ctx.ellipse(L.W*.75,60,50,12,0,0,6.283);ctx.ellipse(L.W*.84,66,34,9,0,0,6.283);ctx.fill();"),
])

patch_file(G3, [
    ("function draw(){ctx.fillStyle='#0b1220';ctx.fillRect(0,0,480,640);var i,a;",
     "function draw(){var asg=ctx.createLinearGradient(0,0,0,640);asg.addColorStop(0,'#070a18');asg.addColorStop(1,'#10142a');ctx.fillStyle=asg;ctx.fillRect(0,0,480,640);ctx.fillStyle='rgba(255,255,255,.22)';for(var as2=0;as2<40;as2++){ctx.fillRect((as2*113)%480,(as2*61)%640,1.3,1.3);}var i,a;"),
    ("function draw(){ctx.fillStyle='#0b1220';ctx.fillRect(0,0,360,560);var i,a;",
     "function draw(){var ivg=ctx.createLinearGradient(0,0,0,560);ivg.addColorStop(0,'#080c1c');ivg.addColorStop(1,'#0e1a26');ctx.fillStyle=ivg;ctx.fillRect(0,0,360,560);ctx.fillStyle='rgba(255,255,255,.2)';for(var iv2=0;iv2<26;iv2++){ctx.fillRect((iv2*97)%360,(iv2*53)%560,1.2,1.2);}var i,a;"),
    ("function draw(){ctx.fillStyle='#0b1220';ctx.fillRect(0,0,360,480);var i,b;",
     "function draw(){var ddg=ctx.createLinearGradient(0,0,0,480);ddg.addColorStop(0,'#1a0c14');ddg.addColorStop(1,'#0e101e');ctx.fillStyle=ddg;ctx.fillRect(0,0,360,480);var i,b;"),
])

patch_file(JL, [
    ("ctx.fillStyle = '#0d1526'; ctx.fillRect(0, 0, W, H);",
     "var plg=ctx.createLinearGradient(0,0,0,H);plg.addColorStop(0,'#1c1430');plg.addColorStop(1,'#241636');ctx.fillStyle=plg;ctx.fillRect(0,0,W,H);"),
    ("ctx.fillStyle = '#0d1526'; ctx.font = 'bold 11px Vazirmatn,Tahoma'; ctx.textAlign = 'center';",
     "ctx.fillStyle = 'rgba(255,225,160,.9)'; ctx.font = 'bold 11px Vazirmatn,Tahoma'; ctx.textAlign = 'center';"),
])

print("fixups done")
