#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""بررسی کیفیت بازی‌های staging — syntax، امنیت sandbox، منابع خارجی، RTL"""
import re, subprocess, sys, os

STAGE = '/home/z/my-project/games-staging'
GAMES = ['chess', 'solitaire', 'blackjack', 'sudoku', 'reversi',
         'snake', 'breakout', 'pong', 'tic-tac-toe', 'minesweeper', 'g2048']

issues = []
for g in GAMES:
    path = os.path.join(STAGE, g, 'index.html')
    if not os.path.exists(path):
        issues.append(f'{g}: index.html MISSING')
        continue
    src = open(path, encoding='utf-8').read()

    # 1) external resources
    urls = [u for u in re.findall(r'https?://[^\s"\'<>]+', src)]
    if urls:
        issues.append(f'{g}: external URLs: {urls[:3]}')

    # 2) rtl + viewport + doctype
    if 'dir="rtl"' not in src: issues.append(f'{g}: no dir=rtl')
    if 'user-scalable=no' not in src: issues.append(f'{g}: no viewport')
    if '<!DOCTYPE html>' not in src: issues.append(f'{g}: no doctype')

    # 3) localStorage — فقط از طریق shim (اگر اصلاً استفاده شده باشد)
    uses_ls = 'localStorage' in src
    if uses_ls and not re.search(r'get:\s*function\s*\(k\)\s*\{\s*try\s*\{\s*return localStorage', src):
        issues.append(f'{g}: store shim missing')
    for ln, line in enumerate(src.split('\n'), 1):
        if 'localStorage' in line:
            if not (re.search(r'try\s*\{\s*(return\s+)?localStorage', line) or 'catch' in line or 'try {' in line):
                issues.append(f'{g}:{ln}: bare localStorage: {line.strip()[:70]}')

    # 4) sandbox escape
    for pat in ['window.top', 'window.parent', 'parent.document', 'document.cookie', 'document.domain']:
        if pat in src: issues.append(f'{g}: sandbox escape pattern: {pat}')

    # 5) emoji
    allowed_extra = set('❋✕◯✓')
    for ch in src:
        o = ord(ch)
        if o >= 0x1F300:
            issues.append(f'{g}: emoji char {ch!r} U+{o:04X}')
            break

    # 6) node --check روی اسکریپت‌های inline
    scripts = re.findall(r'<script>(.*?)</script>', src, re.S)
    ok_all = True
    for si, s in enumerate(scripts):
        tmp = f'/tmp/wog-check-{g}-{si}.js'
        open(tmp, 'w', encoding='utf-8').write(s)
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        if r.returncode != 0:
            ok_all = False
            issues.append(f'{g}: JS SYNTAX ERROR in script#{si}: {r.stderr.strip()[:200]}')
    if ok_all and scripts:
        print(f'{g}: JS OK ({len(scripts)} inline block)')

print()
if issues:
    print('=== ISSUES ===')
    for i in issues: print(' -', i)
    sys.exit(1)
print('ALL CHECKS PASSED')
