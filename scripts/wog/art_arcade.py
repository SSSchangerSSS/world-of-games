# -*- coding: utf-8 -*-
"""Canvas scene art for template arcade games — patches batch sources, then rebuild."""
import io, os

def patch_file(path, pairs):
    s = io.open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old not in s:
            raise SystemExit("PATCH MISS in %s: %r" % (path, old[:60]))
        s = s.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8").write(s)
    print("patched", os.path.basename(path), "(%d patches)" % len(pairs))

G1 = "games/g1_arcade.py"
G2 = "games/g2_arcade.py"
G3 = "games/g3_arcade.py"
JL = "games/j_luck.py"

# ---------- flappy: dawn sky, sun glow, gradient pipes, lip highlight ----------
patch_file(G1, [
    ("ctx.fillStyle='#0e1a33';ctx.fillRect(0,0,W,H);",
     "var sk=ctx.createLinearGradient(0,0,0,H);sk.addColorStop(0,'#1d3a5f');sk.addColorStop(.55,'#3a5a80');sk.addColorStop(.85,'#7a6a72');sk.addColorStop(1,'#a87a5c');ctx.fillStyle=sk;ctx.fillRect(0,0,W,H);"
     "var sg=ctx.createRadialGradient(W*.72,H*.24,4,W*.72,H*.24,64);sg.addColorStop(0,'rgba(255,224,160,.85)');sg.addColorStop(.35,'rgba(255,200,120,.28)');sg.addColorStop(1,'rgba(255,200,120,0)');ctx.fillStyle=sg;ctx.fillRect(0,0,W,H);"
     "ctx.fillStyle='rgba(255,255,255,.09)';ctx.beginPath();ctx.ellipse(W*.24,H*.3,34,9,0,0,6.283);ctx.ellipse(W*.32,H*.33,26,7,0,0,6.283);ctx.ellipse(W*.6,H*.16,30,8,0,0,6.283);ctx.fill();"),
    ("ctx.fillStyle='#3fb8af';ctx.fillRect(p.x,0,60,tp);ctx.fillRect(p.x,tp+140,60,H-24-(tp+140));",
     "var pg=ctx.createLinearGradient(p.x,0,p.x+60,0);pg.addColorStop(0,'#2c8f88');pg.addColorStop(.32,'#4fc0b6');pg.addColorStop(.55,'#3fb8af');pg.addColorStop(1,'#20655f');ctx.fillStyle=pg;ctx.fillRect(p.x,0,60,tp);ctx.fillRect(p.x,tp+140,60,H-24-(tp+140));"
     "ctx.fillStyle='rgba(255,255,255,.22)';ctx.fillRect(p.x+5,0,4,tp);ctx.fillRect(p.x+5,tp+140,4,H-24-(tp+140));"),
    ("ctx.fillStyle='#2c8f88';ctx.fillRect(p.x,Math.max(0,tp-16),60,16);ctx.fillRect(p.x,tp+140,60,16);",
     "var lg=ctx.createLinearGradient(p.x,0,p.x+60,0);lg.addColorStop(0,'#2f9a92');lg.addColorStop(.5,'#54c8be');lg.addColorStop(1,'#227068');ctx.fillStyle=lg;ctx.fillRect(p.x-3,Math.max(0,tp-16),66,16);ctx.fillRect(p.x-3,tp+140,66,16);"
     "ctx.fillStyle='rgba(0,0,0,.25)';ctx.fillRect(p.x-3,Math.max(0,tp-3),66,3);ctx.fillRect(p.x-3,tp+140,66,3);"),
    ("ctx.fillStyle='#c69a3a';ctx.fillRect(0,H-24,W,24);",
     "var gr=ctx.createLinearGradient(0,H-24,0,H);gr.addColorStop(0,'#c69a3a');gr.addColorStop(1,'#7a5a22');ctx.fillStyle=gr;ctx.fillRect(0,H-24,W,24);"),
    ("ctx.fillStyle='#d9a441';ctx.beginPath();ctx.arc(70,st.y,14,0,6.283);ctx.fill();",
     "ctx.save();ctx.shadowColor='rgba(255,210,120,.55)';ctx.shadowBlur=12;"
     "var bg2=ctx.createRadialGradient(66,st.y-5,2,70,st.y,15);bg2.addColorStop(0,'#ffe1a0');bg2.addColorStop(.7,'#d9a441');bg2.addColorStop(1,'#b8862f');ctx.fillStyle=bg2;ctx.beginPath();ctx.arc(70,st.y,14,0,6.283);ctx.fill();ctx.restore();"),
])

# ---------- frogger: water shimmer, grass tufts, car/frog gradients ----------
patch_file(G1, [
    ("var base=(r2===0)?'#123a4a':(r2>=3&&r2<=6)?'#16405c':(r2===7||r2===12||(r2>=1&&r2<=2))?'#1d3527':'#141d31';\n  ctx.fillStyle=base;ctx.fillRect(0,y,W,32);",
     "var base=(r2===0)?'#123a4a':(r2>=3&&r2<=6)?'#16405c':(r2===7||r2===12||(r2>=1&&r2<=2))?'#1d3527':'#141d31';\n  var zg=ctx.createLinearGradient(0,y,0,y+32);zg.addColorStop(0,base);zg.addColorStop(1,'rgba(0,0,0,.42)');ctx.fillStyle=zg;ctx.fillRect(0,y,W,32);"
     "if(r2<8){ctx.strokeStyle='rgba(140,200,230,.08)';ctx.lineWidth=1.5;ctx.beginPath();for(var wv=0;wv<7;wv++){var wx=((r2*67+wv*61)%W);ctx.moveTo(wx,y+9+((r2*13+wv*7)%14));ctx.quadraticCurveTo(wx+8,y+6+((r2*7+wv*5)%16),wx+16,y+9+((r2*13+wv*7)%14));}ctx.stroke();}"
     "if(r2===7||r2===12||(r2>=1&&r2<=2)){ctx.fillStyle='rgba(150,220,150,.1)';for(var tf=0;tf<8;tf++){var tx=(tf*59+r2*23)%W;ctx.fillRect(tx,y+6+((tf*17)%18),2,4);ctx.fillRect(tx+3,y+9+((tf*11)%14),2,4);}}"),
    ("ctx.fillStyle='#e26d5c';ctx.fillRect(c.x+2,y+7,c.w-4,18);\n  ctx.fillStyle='#ffd9a0';ctx.fillRect(c.x+8,y+11,c.w-16,5);}",
     "var cg=ctx.createLinearGradient(0,y+7,0,y+25);cg.addColorStop(0,'#ff8a6c');cg.addColorStop(.5,'#e26d5c');cg.addColorStop(1,'#a83c2c');ctx.fillStyle=cg;ctx.fillRect(c.x+2,y+7,c.w-4,18);"
     "ctx.fillStyle='rgba(255,220,170,.85)';ctx.fillRect(c.x+8,y+11,c.w-16,5);"
     "ctx.fillStyle='rgba(255,240,200,.6)';ctx.beginPath();ctx.arc(c.x+c.w-6,y+10,3,0,6.283);ctx.arc(c.x+c.w-6,y+22,3,0,6.283);ctx.fill();}"),
    ("ctx.fillStyle=st.alive?'#d9a441':'#5c6a80';\n ctx.beginPath();ctx.arc(f.x+16,f.y+16,11,0,6.283);ctx.fill();",
     "ctx.save();ctx.shadowColor=st.alive?'rgba(255,210,120,.55)':'rgba(0,0,0,0)';ctx.shadowBlur=10;"
     "var fg2=ctx.createRadialGradient(f.x+13,f.y+12,2,f.x+16,f.y+16,12);fg2.addColorStop(0,st.alive?'#ffe1a0':'#7a8aa0');fg2.addColorStop(1,st.alive?'#c69a3a':'#4a5670');ctx.fillStyle=fg2;ctx.beginPath();ctx.arc(f.x+16,f.y+16,11,0,6.283);ctx.fill();ctx.restore();"),
])

# ---------- coin-catch: starfield twilight + coin glow ----------
patch_file(G1, [
    ("ctx.fillStyle='#0d1830';ctx.fillRect(0,0,W,H);",
     "var ccg=ctx.createLinearGradient(0,0,0,H);ccg.addColorStop(0,'#141c3e');ccg.addColorStop(.6,'#1a1838');ccg.addColorStop(1,'#241a30');ctx.fillStyle=ccg;ctx.fillRect(0,0,W,H);"
     "ctx.fillStyle='rgba(255,255,255,.25)';for(var si2=0;si2<30;si2++){ctx.fillRect((si2*83)%W,(si2*47)%H,1.4,1.4);}"),
    ("ctx.fillStyle='#d9a441';ctx.beginPath();ctx.arc(it.x,it.y,11,0,6.283);ctx.fill();",
     "ctx.save();ctx.shadowColor='rgba(255,210,120,.7)';ctx.shadowBlur=12;"
     "var cg2=ctx.createRadialGradient(it.x-3,it.y-3,1,it.x,it.y,12);cg2.addColorStop(0,'#ffe9b8');cg2.addColorStop(.65,'#d9a441');cg2.addColorStop(1,'#9a6e1e');ctx.fillStyle=cg2;ctx.beginPath();ctx.arc(it.x,it.y,11,0,6.283);ctx.fill();ctx.restore();"),
    ("ctx.fillStyle='#e26d5c';ctx.beginPath();ctx.arc(it.x,it.y,11,0,6.283);ctx.fill();",
     "ctx.save();ctx.shadowColor='rgba(255,110,80,.7)';ctx.shadowBlur=12;"
     "var hg2=ctx.createRadialGradient(it.x-3,it.y-3,1,it.x,it.y,12);hg2.addColorStop(0,'#ffb09a');hg2.addColorStop(.65,'#e26d5c');hg2.addColorStop(1,'#9a3424');ctx.fillStyle=hg2;ctx.beginPath();ctx.arc(it.x,it.y,11,0,6.283);ctx.fill();ctx.restore();"),
])

# ---------- runner: desert dusk + sun + dune band ----------
patch_file(G1, [
    ("ctx.fillStyle='#101b31';ctx.fillRect(0,0,W,H);",
     "var rg=ctx.createLinearGradient(0,0,0,H);rg.addColorStop(0,'#2a1e3e');rg.addColorStop(.5,'#6e3e4a');rg.addColorStop(.78,'#c67a4a');rg.addColorStop(1,'#e8a35c');ctx.fillStyle=rg;ctx.fillRect(0,0,W,H);"
     "var rsg=ctx.createRadialGradient(W*.78,H*.62,4,W*.78,H*.62,80);rsg.addColorStop(0,'rgba(255,230,170,.9)');rsg.addColorStop(.4,'rgba(255,200,120,.3)');rsg.addColorStop(1,'rgba(255,200,120,0)');ctx.fillStyle=rsg;ctx.fillRect(0,0,W,H);"),
])

# ---------- meteor: nebula space ----------
patch_file(G2, [
    ("ctx.fillStyle='#0b1226';ctx.fillRect(0,0,L.W,440);",
     "var mg=ctx.createLinearGradient(0,0,0,440);mg.addColorStop(0,'#0a0e24');mg.addColorStop(.6,'#141031');mg.addColorStop(1,'#221233');ctx.fillStyle=mg;ctx.fillRect(0,0,L.W,440);"
     "var ng=ctx.createRadialGradient(L.W*.7,110,8,L.W*.7,110,190);ng.addColorStop(0,'rgba(226,109,92,.16)');ng.addColorStop(1,'rgba(226,109,92,0)');ctx.fillStyle=ng;ctx.fillRect(0,0,L.W,440);"),
])

# ---------- stacker: neon tower hall ----------
patch_file(G2, [
    ("ctx.fillStyle='#0b1226';ctx.fillRect(0,0,L.W,500);",
     "var stg=ctx.createLinearGradient(0,0,0,500);stg.addColorStop(0,'#0c1128');stg.addColorStop(1,'#160f2e');ctx.fillStyle=stg;ctx.fillRect(0,0,L.W,500);"
     "var slg=ctx.createRadialGradient(L.W/2,430,10,L.W/2,430,240);slg.addColorStop(0,'rgba(63,184,175,.14)');slg.addColorStop(1,'rgba(63,184,175,0)');ctx.fillStyle=slg;ctx.fillRect(0,0,L.W,500);"),
])

# ---------- kite: daylight meadow sky ----------
patch_file(G2, [
    ("ctx.fillStyle='#0b1226';ctx.fillRect(0,0,L.W,500);",
     "var kg2=ctx.createLinearGradient(0,0,0,500);kg2.addColorStop(0,'#274b76');kg2.addColorStop(.6,'#4a6a92');kg2.addColorStop(1,'#7aa0b8');ctx.fillStyle=kg2;ctx.fillRect(0,0,L.W,500);"
     "ctx.fillStyle='rgba(255,255,255,.12)';ctx.beginPath();ctx.ellipse(L.W*.2,90,44,11,0,0,6.283);ctx.ellipse(L.W*.28,96,32,8,0,0,6.283);ctx.ellipse(L.W*.75,60,50,12,0,0,6.283);ctx.ellipse(L.W*.84,66,34,9,0,0,6.283);ctx.fill();"),
])

# ---------- g3: asteroids / invaders / dodge ----------
patch_file(G3, [
    ("function draw(){ctx.fillStyle='#0b1220';ctx.fillRect(0,0,480,640);var i,a;",
     "function draw(){var asg=ctx.createLinearGradient(0,0,0,640);asg.addColorStop(0,'#070a18');asg.addColorStop(1,'#10142a');ctx.fillStyle=asg;ctx.fillRect(0,0,480,640);ctx.fillStyle='rgba(255,255,255,.22)';for(var as2=0;as2<40;as2++){ctx.fillRect((as2*113)%480,(as2*61)%640,1.3,1.3);}var i,a;"),
    ("function draw(){ctx.fillStyle='#0b1220';ctx.fillRect(0,0,360,560);var i,a;",
     "function draw(){var ivg=ctx.createLinearGradient(0,0,0,560);ivg.addColorStop(0,'#080c1c');ivg.addColorStop(1,'#0e1a26');ctx.fillStyle=ivg;ctx.fillRect(0,0,360,560);ctx.fillStyle='rgba(255,255,255,.2)';for(var iv2=0;iv2<26;iv2++){ctx.fillRect((iv2*97)%360,(iv2*53)%560,1.2,1.2);}var i,a;"),
    ("function draw(){ctx.fillStyle='#0b1220';ctx.fillRect(0,0,360,480);var i,b;",
     "function draw(){var ddg=ctx.createLinearGradient(0,0,0,480);ddg.addColorStop(0,'#1a0c14');ddg.addColorStop(1,'#0e101e');ctx.fillStyle=ddg;ctx.fillRect(0,0,360,480);var i,b;"),
])

# ---------- plinko: warm walnut board ----------
patch_file(JL, [
    ("ctx.fillStyle = '#0d1526'; ctx.fillRect(0, 0, W, H);",
     "var plg=ctx.createLinearGradient(0,0,0,H);plg.addColorStop(0,'#1c1430');plg.addColorStop(1,'#241636');ctx.fillStyle=plg;ctx.fillRect(0,0,W,H);"),
    ("ctx.fillStyle = '#0d1526'; ctx.font = 'bold 11px Vazirmatn,Tahoma'; ctx.textAlign = 'center';",
     "ctx.fillStyle = 'rgba(255,225,160,.9)'; ctx.font = 'bold 11px Vazirmatn,Tahoma'; ctx.textAlign = 'center';"),
])

print("arcade art done")
