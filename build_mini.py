# -*- coding: utf-8 -*-
import sys, os, json, importlib.util, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_mini
spec = importlib.util.spec_from_file_location("batch", os.path.abspath(sys.argv[1]))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
os.makedirs("games", exist_ok=True); manifest = []
for g in m.GAMES:
    os.makedirs(os.path.join("games", g.slug), exist_ok=True)
    io.open(os.path.join("games", g.slug, "index.html"), "w", encoding="utf-8").write(g.render())
    manifest.append({"slug": g.slug, "seed": g.seed, "logic": g.logic,
                     "tests": [{"name": n, "js": j} for n, j in g.tests]})
json.dump(manifest, io.open("tests-manifest.json", "w", encoding="utf-8"), ensure_ascii=False)
print("MINI BUILD OK:", [g.slug for g in m.GAMES])
