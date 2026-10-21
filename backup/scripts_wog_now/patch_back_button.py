# -*- coding: utf-8 -*-
"""Inject the back-to-home button into legacy game pages (idempotent).
Usage: python3 patch_back_button.py <dir-containing-game-folders>"""
import os, sys, io, re

CSS = """a.wog-home{position:fixed;top:10px;inset-inline-start:12px;z-index:99;background:rgba(217,164,65,.12);border:1px solid rgba(217,164,65,.45);color:#e8c073;text-decoration:none;padding:6px 12px;border-radius:10px;font-size:.85rem;font-weight:700;font-family:Vazirmatn,Tahoma,sans-serif}
a.wog-home:hover{background:rgba(217,164,65,.3)}"""
LINK = '<a class="wog-home" href="../../index.html">⌂ خانه</a>'

root = sys.argv[1]
n = 0
for d in sorted(os.listdir(root)):
    p = os.path.join(root, d, "index.html")
    if not os.path.isfile(p):
        continue
    s = io.open(p, encoding="utf-8").read()
    if "wog-home" in s:
        print(d, ": already patched")
        continue
    m = re.search(r"<body[^>]*>", s)
    if not m:
        print(d, ": NO <body> — skipped")
        continue
    s = s[:m.end()] + "\n" + LINK + s[m.end():]
    if "</style>" in s:
        s = s.replace("</style>", CSS + "\n</style>", 1)
    else:
        s = s.replace("</head>", "<style>" + CSS + "</style>\n</head>", 1)
    io.open(p, "w", encoding="utf-8").write(s)
    n += 1
    print(d, ": patched")
print("patched %d files" % n)
