# -*- coding: utf-8 -*-
"""Syntax-check every built game page: extract inline <script> and node --check it.
Usage: python3 check_syntax.py <games-out-dir>"""
import os, sys, re, subprocess, tempfile

root = sys.argv[1]
bad = 0
n = 0
for d in sorted(os.listdir(root)):
    p = os.path.join(root, d, "index.html")
    if not os.path.isfile(p):
        continue
    n += 1
    html = open(p, encoding="utf-8").read()
    m = re.search(r"<script>(.*)</script>", html, re.S)
    if not m:
        print(d, ": NO SCRIPT"); bad += 1; continue
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(m.group(1)); tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    if r.returncode != 0:
        print(d, ": SYNTAX ERROR\n", r.stderr[:800]); bad += 1
    else:
        os.unlink(tmp)
print("syntax check: %d files, %d bad" % (n, bad))
sys.exit(1 if bad else 0)
