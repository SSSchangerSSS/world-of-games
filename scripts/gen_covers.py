#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تولید کاورهای SVG برای بازی‌های Pages — هم‌سبک با SeedCatalog.CoverSvg پلتفرم"""
import os

OUT = '/home/z/my-project/pages-site/covers'
os.makedirs(OUT, exist_ok=True)

HEAD = '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#16213e"/><stop offset="1" stop-color="#0b1220"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#g)"/>
'''
TAIL = '''  <text x="300" y="312" text-anchor="middle" font-family="Vazirmatn, sans-serif" font-size="30" fill="#f3ead8" direction="rtl">{title}</text>
  <text x="300" y="352" text-anchor="middle" font-family="Vazirmatn, sans-serif" font-size="15" fill="#d9a441" direction="rtl">World of Games</text>
</svg>
'''

# هر موتیف در ناحیه مرکزی (حدود 180..420 عرضی، 60..250 ارتفاعی)
MOTIFS = {
    'chess': '<g fill="#d9a441"><path d="M300 70 c-14 0 -24 10 -24 23 c0 8 4 15 10 19 c-14 7 -22 20 -24 36 l-8 52 l92 0 l-8 -52 c-2 -16 -10 -29 -24 -36 c6 -4 10 -11 10 -19 c0 -13 -10 -23 -24 -23 z"/><rect x="236" y="204" width="128" height="16" rx="5"/></g>',
    'solitaire': '<g><rect x="238" y="84" width="96" height="134" rx="10" fill="#1a2848" stroke="#d9a441" stroke-width="3" transform="rotate(-14 286 151)"/><rect x="258" y="78" width="96" height="134" rx="10" fill="#f3ead8" stroke="#b7ab8e"/><text x="306" y="120" font-family="serif" font-size="26" fill="#c65445" text-anchor="middle">♥</text><text x="306" y="185" font-family="serif" font-size="52" fill="#23283b" text-anchor="middle">A</text></g>',
    'blackjack': '<g><rect x="240" y="80" width="120" height="150" rx="12" fill="#f3ead8" stroke="#b7ab8e"/><text x="300" y="178" font-family="Vazirmatn, sans-serif" font-size="58" font-weight="bold" fill="#23283b" text-anchor="middle">21</text><text x="300" y="120" font-family="serif" font-size="30" fill="#c65445" text-anchor="middle">♠</text></g>',
    'sudoku': '<g stroke="#d9a441" stroke-width="4" fill="none"><rect x="228" y="78" width="144" height="144" rx="8"/><path d="M276 78 v144 M324 78 v144 M228 126 h144 M228 174 h144" stroke-width="2" opacity=".7"/></g><g fill="#3fb8af" font-family="Vazirmatn, sans-serif" font-size="30" text-anchor="middle"><text x="252" y="116">۵</text><text x="348" y="116">۳</text><text x="300" y="164">۷</text><text x="252" y="212">۱</text><text x="348" y="212">۹</text></g>',
    'reversi': '<g><circle cx="268" cy="150" r="52" fill="#f3ead8" stroke="#b7ab8e" stroke-width="2"/><path d="M268 98 a52 52 0 0 0 0 104 z" fill="#1c2438"/><circle cx="332" cy="150" r="52" fill="#1c2438"/><path d="M332 98 a52 52 0 0 0 0 104 z" fill="#f3ead8"/></g>',
    'snake': '<g><path d="M230 200 q0 -44 44 -44 t88 0 q44 0 44 -44 t-44 -44" fill="none" stroke="#3fb8af" stroke-width="22" stroke-linecap="round"/><circle cx="406" cy="68" r="17" fill="#e26d5c"/></g>',
    'breakout': '<g><rect x="222" y="76" width="72" height="24" rx="5" fill="#d9a441"/><rect x="306" y="76" width="72" height="24" rx="5" fill="#d9a441"/><rect x="222" y="112" width="72" height="24" rx="5" fill="#3fb8af"/><rect x="306" y="112" width="72" height="24" rx="5" fill="#3fb8af"/><circle cx="300" cy="180" r="13" fill="#f3ead8"/><rect x="252" y="216" width="96" height="14" rx="7" fill="#e8c073"/></g>',
    'pong': '<g stroke="#d9a441" stroke-width="3" stroke-dasharray="4 10"><line x1="300" y1="70" x2="300" y2="234"/></g><g fill="#e8c073"><rect x="236" y="96" width="14" height="60" rx="6"/><rect x="350" y="150" width="14" height="60" rx="6"/></g><circle cx="300" cy="152" r="12" fill="#f3ead8"/>',
    'tic-tac-toe': '<g stroke="#d9a441" stroke-width="5" fill="none" opacity=".8"><rect x="230" y="80" width="140" height="140" rx="10"/><path d="M277 80 v140 M323 80 v140 M230 127 h140 M230 173 h140"/></g><g stroke-width="8" fill="none"><path d="M245 95 l30 30 M275 95 l-30 30" stroke="#3fb8af"/><circle cx="322" cy="196" r="17" stroke="#e26d5c"/></g>',
    'minesweeper': '<g><circle cx="300" cy="150" r="46" fill="#1c2438" stroke="#e26d5c" stroke-width="3"/><g stroke="#e26d5c" stroke-width="6" stroke-linecap="round"><path d="M300 84 v-14 M300 216 v14 M234 150 h-14 M366 150 h14 M255 105 l-10 -10 M345 105 l10 -10 M255 195 l-10 10 M345 195 l10 10"/></g><circle cx="284" cy="134" r="10" fill="#46536f"/></g>',
    'g2048': '<g><rect x="228" y="88" width="62" height="62" rx="10" fill="#e8c073"/><rect x="310" y="88" width="62" height="62" rx="10" fill="#3fb8af"/><rect x="228" y="162" width="62" height="62" rx="10" fill="#14203a" stroke="#d9a441" stroke-width="2"/><rect x="310" y="162" width="62" height="62" rx="10" fill="#e26d5c"/></g><g font-family="Vazirmatn, sans-serif" font-weight="bold" text-anchor="middle" fill="#221806" font-size="26"><text x="259" y="128">۲</text><text x="341" y="128">۴</text></g><text x="341" y="203" font-family="Vazirmatn, sans-serif" font-weight="bold" text-anchor="middle" fill="#221806" font-size="26">۸</text><text x="259" y="203" font-family="Vazirmatn, sans-serif" font-weight="bold" text-anchor="middle" fill="#d9a441" font-size="26">?</text>',
}

TITLES = {
    'chess': 'شطرنج', 'solitaire': 'پاسور (کلایک)', 'blackjack': 'بلک‌جک ۲۱',
    'sudoku': 'سودوکو', 'reversi': 'اوتِلو', 'snake': 'مارِ گرسنه',
    'breakout': 'توپ‌شکن', 'pong': 'پینگ‌پنگ', 'tic-tac-toe': 'دوز',
    'minesweeper': 'مین‌یاب', 'g2048': '۲۰۴۸',
}

for slug, title in TITLES.items():
    svg = HEAD + MOTIFS[slug] + TAIL.replace('{title}', title)
    with open(os.path.join(OUT, f'{slug}.svg'), 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'cover: {slug}.svg ({len(svg)} bytes)')
print('DONE')
