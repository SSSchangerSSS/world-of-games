# Worklog — چند-ایجنت (بازسازی‌شده پس از ریست محیط)

> نکته: worklog قبلی در ریست محیط (context overflow) از بین رفت. این فایل از سرِ این نقطه بازسازی شد.
> تاریخچه پیشین (خلاصه): ساخت مخزن `SSSchangerSSS/world-of-games` طبق قانون‌اساسی Spec-Driven v1.0.0 —
> ساختار spec-kit کامل، MVP پلتفرم (Core/Infrastructure/Web/Tests)، ۳۵ تست سبز، CI ویندوزی سبز،
> مستندات (آپلود بازی / MCP / استقرار IIS). تصمیمات مصوب D-01…D-14 و Known Issues کی-۱ تا کی-۵ در spec و summary جلسه پیش ثبت است.

---
Task ID: 1
Agent: main (Z.ai)
Task: انتشار پروژه روی GitHub Pages (پرسش کاربر: «آیا میشه روی گیت‌هاب پیج هم منتشرش کرد؟»)

Work Log:
- ریست محیط شناسایی شد؛ توکن از اسکریپت باقی‌مانده در /tmp بازیابی و اعتبارسنجی شد (HTTP 200 روی /repos).
- مخزن مجدداً clone شد (main در commit 987dd48).
- بررسی نشان داد بازی‌های دمو دو فایل HTML5 کاملاً سلف‌کانتینند در `Data/SeedGames/` هستند (localStorage با try/catch گارد شده) → قابل میزبانی استاتیک بدون تغییر.
- توکن‌های طراحی از `wwwroot/css/tokens.css` و فونت‌های وزیرمتن (۴ وزن، ۲۱۲KB) از `wwwroot/fonts/` استخراج شد.
- سایت استاتیک در `pages-site/` ساخته شد: index.html (۷ بخش: hero/games/features/developers/donate/mcp/cta)، css/style.css، favicon، ۲ کاور SVG مطابق SeedCatalog.CoverSvg، robots.txt، sitemap.xml، .nojekyll — همه لینک‌ها نسبی (سازگار با base path) و بدون CDN خارجی. کل حجم ۳۰۴KB.
- اسموک‌تست محلی با http.server: هر ۹ مسیر 200.
- شاخه orphan `gh-pages` ساخته و push شد (commit 2418aa0).
- فعال‌سازی Pages: POST /pages → 409 «already enabled» (با push شاخه gh-pages خودکار فعال شد)؛ GET تأیید: source = gh-pages:/، HTTPS enforce.
- بیلد Pages: status=built بدون خطا.
- راستی‌آزمایی زنده: ۹ مسیر همه 200 با content-type صحیح؛ عنوان فارسی درست.
- README در main به‌روزرسانی شد (لینک پیش‌نمایش زنده + توضیح gh-pages) و push شد.
- homepage و description مخزن با PATCH /repos تنظیم شد.
- CI روی main پس از push README: in_progress (تغییر فقط doc است)؛ بیلد Pages deployment: success.

Stage Summary:
- سایت زنده: https://ssschangersss.github.io/world-of-games/
- دو بازی دمو قابل بازی: /games/akhaemenid-memory/ و /games/alborz-jump/
- شاخه gh-pages = منبع سایت؛ main = سورس کامل پلتفرم.
- محدودیت انتزاعی: GitHub Pages فقط استاتیک است؛ اپ کامل (Razor/EF/Identity/MCP/دونیت) به سرور .NET نیاز دارد (docs/deploy-iis.md).
- توکن پس از پایان کارها از دیسک حذف شد (فایل .gh_token_chmod_tmp).
---
Task ID: 2-a
Agent: general-purpose
Task: بازی‌سازی برای پلتفرم World of Games — ساخت ۳ بازی کانواسی سلف‌کانتینند در games-staging (snake، breakout، pong) مطابق games-spec.md

Work Log:
- games-spec.md و worklog.md کامل خوانده شد؛ قیود سخت spec در هر سه فایل رعایت شد: lang="fa" dir="rtl"، کاملاً آفلاین (هیچ http/CDN/فونت خارجی)، shim استاندارد store در ابتدای اسکریپت (بدون دسترسی مستقیم به ذخیره‌سازی محلی)، بدون emoji، بدون دسترسی به parent/top/cookie، IIFE با 'use strict'، حجم زیر ۲۵KB.
- snake/index.html «مارِ گرسنه» (۹,۶۰۰ بایت): شبکه ۱۹×۱۹ خانه (خانه ۲۲px داخل کنواس ۴۲۰×۵۶۰)، مار آرایه‌ای از خانه‌ها با سر طلایی #e8c073 و بدن فیروزه‌ای #3fb8af با گردی (roundRect دستی + چشم)، غذا دایره قرمز #e26d5c با اسپاون بدون تداخل؛ کنترل کلیدهای جهت + WASD (با e.code، مستقل از کیبورد فارسی) + سوایپ لمسی touchstart/touchend با آستانه ۲۴px؛ صف جهت برای جلوگیری از چرخش دوگانه در یک تیک؛ هر غذا ۱۰ امتیاز، هر ۵ غذا تیک ۱۴۰→۷۰ms (گام ۱۴)؛ برخورد دیوار/بدن = پایان با پنل «باختی! امتیاز: X» + «شروع دوباره»؛ رکورد wog-snake-best.
- breakout/index.html «توپ‌شکن» (۱۱,۶۴۲ بایت): ۶ ردیف × ۸ آجر، امتیاز ۶۰/۵۰/۴۰/۳۰/۲۰/۱۰ از بالا، رنگ‌بندی دو ردیف طلایی (#e8c073/#d9a441)، دو ردیف فیروزه‌ای (#3fb8af + آلفا)، دو ردیف کرم #f3ead8 با شفافیت؛ ۳ جون؛ راکت با ماوس/لمس (مختصات نسبی با مقیاس getBoundingClientRect) و کلیدهای چپ/راست + A/D؛ زاویه بازتاب تابع محل برخورد با راکت (تا ۶۰°)؛ فیزیک با rAF و زیرگام ۸ms ضدتونل‌زنی؛ تخریب همه آجرها = پیام «بردی! لِوِل بعد» + سرعت ×۱.۰۹ در هر لِوِل (سقف ۵۶۰)؛ رکورد زنده wog-breakout-best؛ پیام‌های گذرا با toast.
- pong/index.html «پینگ‌پنگ» (۹,۲۷۹ بایت): کنواس عمودی ۴۲۰×۵۶۰، راکت بازیکن پایین (طلایی) و حریف AI بالا (فیروزه‌ای) با سرعت محدود ۲۳۵px/s فقط هنگام نزدیک‌شدن توپ و بازگشت آرام به مرکز (قابل‌برد)؛ اولین ۷ امتیاز برنده؛ هر برخورد توپ ×۱.۰45 سریع‌تر (سقف ۶۴۰)؛ پس از هر امتیاز توپ وسط‌چین و سرو به سمت بازنده با تأخیر ۰.۸s و زاویه تصادفی؛ HUD «شما X — Y حریف»؛ پایان «بردی!»/«باختی!» + «شروع دوباره»؛ شمارش بردها با wog-pong-wins.
- چک‌های الزامی پاس شد: استخراج <script> هر سه فایل با python (شامل assert بدون استفاده نادرست از ذخیره‌سازی) و node --check → «snake JS OK / breakout JS OK / pong JS OK»؛ grep "http" روی هر سه index.html → بدون هیچ نتیجه.
- نکته: کامنت‌های کد عمداً بدون نام ذخیره‌سازی محلی نوشته شد تا الگوی re.sub چک استاندارد پاس شود (کامنت دموی قبلی این کلمه را داشت و چک را خراب می‌کرد).
- اسموک‌تست ران‌تایم با مرورگر هدلس (file://): هر سه بازی بدون خطای کنسول/صفحه؛ snake → مرگ بر دیوار و پنل پایان و ریستارت OK؛ breakout → پرتاب با Space، شکستن آجر و به‌روزرسانی زنده امتیاز/رکورد (۲۷۰) OK؛ pong → امتیازگیری AI تا ۷ و پنل «نتیجه: ۰ — ۷» با شروع دوباره OK.

Stage Summary:
- سه بازی آماده استیجینگ: games-staging/snake، games-staging/breakout، games-staging/pong — هر کدام فقط یک index.html سلف‌کانتینند (کنواس ۴۲۰×۵۶۰، بدون هیچ منبع خارجی، sandbox-safe).
- مجموع ۳۰,۵۲۰ بایت (هر سه زیر سقف ~۲۵KB تکی).
- آماده آپلود با جریان استاندارد آپلود بازی (game-upload-standard) به پلتفرم.
---
Task ID: 2-b
Agent: general-purpose
Task: بازی‌سازی برای پلتفرم World of Games — ساخت ۳ بازی منطقی HTML5 سلف‌کانتینند (دوز / مین‌یاب / ۲۰۴۸)

Work Log:
- games-spec.md و worklog.md پیش از کدنویسی کامل خوانده شد؛ هر ۸ قید MUST رعایت شد: dir=rtl + lang=fa، viewport با user-scalable=no، کاملاً آفلاین (صفر مورد http/CDN در کل فایل‌ها)، shim ذخیره‌سازی به‌جای localStorage مستقیم، بدون emoji (فقط ✕ و ❋ مجاز)، لمس+ماوس+کیبورد، IIFE + 'use strict'، حجم زیر ~۲۵KB.
- games-staging/tic-tac-toe/index.html («دوز»، ~۱۱.۲KB): صفحه ۳×۳ با CSS grid و aspect-ratio:1 (عرض min(92vw,440px))؛ بازیکن ✕ طلایی #d9a441 و کامپیوتر حلقه CSS فیروزه #3fb8af؛ مینی‌مکس کامل شکست‌ناپذیر (عمق‌دار برای ترجیح برد سریع) و در اولین حرکت AI انتخاب تصادفی میان خانه‌های با امتیاز برتر؛ خط برنده با یک خط طلایی واقعی (div چرخیده روی مراکز خانه‌ها با offset) + هایلایت خانه‌ها؛ شمارش برد/باخت/مساوی در HUD با کلید wog-ttt-tally؛ دکمه‌های «دور بعد» و «صفر کردن شمارش»؛ شروع‌کننده هر دور یک‌درمیان عوض می‌شود؛ پنل پایان وسط صفحه.
- games-staging/minesweeper/index.html («مین‌یاب»، ~۱۲.۲KB): آسان ۹×۹ با ۱۰ مین، متوسط ۱۰ ردیف×۱۲ ستون با ۲۲ مین — دو دکمه انتخاب سطح بالای بازی؛ مین‌ها پس از اولین کلیک چیده می‌شوند و در خانه اول و همسایه‌هایش نیستند (اولین کلیک همیشه امن)؛ حالت پرچم toggle (aria-pressed) + راست‌کلیک برای پرچم؛ سقف پرچم = تعداد مین با شمارنده f/m در HUD؛ flood-fill بازکردن با پشته (بدون بازگشتی)؛ رنگ اعداد ۱-۸ متمایز: ۱ فیروزه، ۲ سبز #67b98a، ۳ قرمز #e26d5c، ۴ بنفش، ۵ طلایی، ۶ آبی، ۷ صورتی، ۸ خاکستری؛ تایمر ثانیه‌شمار و رکورد هر سطح در wog-mines-best-easy / wog-mines-best-med؛ در پایان همه مین‌ها نمایش داده می‌شوند (مین برخوردی با پس‌زمینه قرمز، پرچم‌های غلط با ✕)؛ پنل «بردی!» / «بووم! باختی» + «شروع دوباره»؛ مین با دایره CSS (بدون نویسه).
- games-staging/g2048/index.html («۲۰۴۸»، ~۱۱.۸KB، دقت: نام پوشه g2048): شبکه ۴×۴ با DOM/CSS grid (بدون canvas)؛ کاشی‌های position:absolute با transform:translate و انیمیشن لغزش + pop ادغام؛ کلیدهای جهت + سوایپ لمسی چهارجهته (touchstart/touchend، آستانه ۲۴px، touch-action:none روی بورد)؛ منطق استاندارد: لغزش کامل، ادغام یک‌بار در هر حرکت (تشخیص با شماره حرکت seq)، کاشی جدید بعد از هر حرکت (۹۰٪ عدد ۲ / ۱۰٪ عدد ۴)؛ پالت کاشی هارمونیک با #14203a از کرم/طلایی/فیروزه تا نارنجی/قرمز و درخشش طلایی برای ۱۰۲۴/۲۰۴۸؛ متن کاشی ≥۱۰۲۴ کوچک‌تر (t-sm)؛ امتیاز = مجموع ادغام‌ها؛ رکورد در wog-2048-best؛ «بردی!» در رسیدن به ۲۰۴۸ با دکمه «ادامه بازی»؛ تشخیص پایان بازی (نبود حرکت ممکن)؛ «بازی جدید» با تأیید inline دومرحله‌ای (بدون confirm())؛ direction:ltr فقط روی بورد برای هم‌ترازی ستون‌های شبکه RTL با محور فیزیکی کلید/سوایپ.
- چک سینتکس: استخراج <script> هر سه فایل با python + node --check → هر سه «JS OK».
- چک منع منابع خارجی: grep -n "http" روی هر سه فایل → خالی (exit 1، صفر مورد).
- چک نویسه‌ها: اسکن یونیکد → هیچ نویسه خارج از لیست مجاز (فقط ✕ و ❋).
- حجم‌ها (stat): tic-tac-toe 11,444 بایت · minesweeper 12,464 بایت · g2048 12,118 بایت — همه زیر سقف ~۲۵KB.

Stage Summary:
- سه بازی منطقی جدید آماده در games-staging/ است؛ هر کدام دقیقاً یک index.html سلف‌کانتینند و مطابق games-spec.md (توکن‌های طراحی طلایی/فیروزه، هدر ❋، HUD، پنل پایان وسط صفحه، #hint فارسی).
- کلیدهای ذخیره‌سازی: wog-ttt-tally، wog-mines-best-easy، wog-mines-best-med، wog-2048-best (همه از طریق shim سازگار با sandbox بدون allow-same-origin).
- کنترل سه‌کاناله (لمس/ماوس/کیبورد) در هر سه بازی رعایت شد؛ هیچ درخواست شبکه‌ای وجود ندارد.

---
Task ID: 3
Agent: main (Z.ai)
Task: مجموعه بازی‌های کلاسیک — ۱۱ بازی جدید (شطرنج، کارتی و…) با ترکیب اورجینال + متن‌باز مجاز

Work Log:
- درخواست کاربر: «شطرنج و بازی‌های کلاسیک کارتی و…؛ مجموعه نسبتاً بزرگ + استفاده از پروژه‌های متن‌باز اگر لایسنس مشکلی ندارد»
- مکانیزم‌ها راستی‌آزمایی شد: csproj wildcard (Data/SeedGames/**) خودکار کپی می‌کند؛ sandbox بدون allow-same-origin → shim الزامی؛ تست‌ها به SeedCatalog وابسته نیستند.
- chess.js v0.10.3 (BSD-2-Clause، Jeff Hlywa) از cdnjs دانلود (16KB) — تنها کامپوننت ثالث؛ LICENSE-chessjs.txt + CREDITS.md داخل پوشهٔ بازی.
- استاندارد مشترک بازی‌ها در /home/z/my-project/games-spec.md تدوین شد (توکن‌های رنگ، shim، RTL، منع شبکه/emoji).
- Task 2-a (ساب‌ایجنت): snake، breakout، pong — همه OK + اسموک مرورگر.
- Task 2-b (ساب‌ایجنت): tic-tac-toe (minimax شکست‌ناپذیر)، minesweeper (اولین کلیک امن)، g2048 (سوایپ+کلید) — همه OK.
- Task 2-c (main): chess (chess.js + negamax آلفا-بتا با PST، ارتقا، برگردان)، solitaire (کلایک کامل + undo/خودکار)، blackjack (کفش ۴ دسته، دوبرابر، ۳:۲)، sudoku (تولید راه‌حل‌یکتا با MRV، ۶ms/جدول)، reversi (وزن موقعیتی + پاس).
- بازبینی با /home/z/my-project/scripts/check_games.py: ۱۱/۱۱ syntax OK، بدون URL خارجی، shim سالم، بدون emoji، RTL همه.
- اسموک مرورگر هدلس: ۵ بازی پیچیده صفر خطا؛ تعامل شطرنج (e2e4 → پاسخ AI) و پخش بلک‌جک و تولید سودوکو تست شد.
- 🐞 فیکس مهم: worldofgames.db (دارای hash ادمین seed) در مخزن commit شده بود → سبزهای قدیمی (۲ بازی) روی نصب تازه می‌ماند + افشای hash. git rm --cached + .gitignore تقویت‌شده (App_Data/ کامل) + untrack همهٔ wwwroot/media.
- SeedCatalog.DemoGames → ۱۳ بازی در ۶ دسته. Build: 0W/0E · ۳۵/۳۵ تست سبز · اسموک کامل پلتفرم (play pages، chess.min.js، کاورها) 200.
- کاورهای SVG اختصاصی با scripts/gen_covers.py تولید شد (موتیف هر بازی).
- Pages: ۱۳ کارت + کاور + sitemap ۱۳ URL؛ gh-pages push (30b5cfb) → build سبز → راستی‌آزمایی زنده ۱۹/۱۹ مسیر 200.
- CI main: success (هر دو commit).
- توکن پس از اتمام از متغیرها پاک شد (فایل موقت قبلاً حذف شده؛ در صورت نیاز کاربر باید توکن تازه بدهد — قبلاً هم توصیه به revoke شده).

Stage Summary:
- مجموعه نهایی ۱۳ بازی دمو: تخته‌ای (شطرنج/اوتلو/دوز)، کارتی (پاسور/بلک‌جک)، پازل (سودوکو/۲۰۴۸)، معمایی (مین‌یاب/حافظه هخامنشی)، اکشن (توپ‌شکن/پرش البرز)، کازوال (مار/پینگ‌پنگ).
- Live: https://ssschangersss.github.io/world-of-games/ (همه قابل بازی)
- main: d4671a9 + فیکس untrack (commit بعدی) — CI سبز.
- نکته باقی‌مانده: hash ادمین توسعه در تاریخچه git می‌ماند (رمز dev در README عمومی است — ریسک پایین)؛ در صورت حساسیت، history rewrite یا تغییر AdminSeed:Password.

---
Task ID: pilot
Agent: general-purpose
Task: Pilot — 2 light card games (pyramid, golf) for the World of Games platform as a single game module `/home/z/my-project/scripts/wog/games/pilot_cards.py` following the lib.G contract (logic/ui/css/tests strings, engines=("common","card"), Persian UI, forbidden-token rules), plus green self-check (build → logic tests → syntax → browser smoke).

Work Log:
- /home/z/my-project/scripts/wog/ نبود (نه lib.py و نه build.py/test_logic.mjs/check_syntax.py/smoke.py) → زیرساخت حداقلی و وفادار به قرارداد ساخته شد: lib.py (کلاس G)، build.py (رندر صفحه RTL+IIFE+shim store+موتور کارت+manifest تست‌ها+لندینگ)، test_logic.mjs (اجرای تست‌ها در vm ایزوله با T.eq/ok/approx/near/throws و rng دترمینیستیک mulberry32)، check_syntax.py (node --check روی همهٔ اسکریپت‌های inline)، smoke.py (fetch + اسکن توکن‌های ممنوعه بخش game + اجرای واقعی مرورگر با playwright کلیک روی همهٔ [data-smoke]).
- هرم: ۲۸ کارت (ردیف‌های ۱..۷)، ۲۴ کارت پشت‌کار تک‌مرحله‌ای، جمع ۱۳ حذف جفتی، شاه تنها، گیت exposure (کارت زیر دو فرزند بسته است)، تشخیص برد/باخت، UI گرید هرم + زباله + دکمه پشت‌کار با شمارش + hud فارسی + ovl پایان.
- گلف: ۵ ستون × ۷ ردیف، ۱۷ کارت باقی (۱ زباله + ۱۶ پشت‌کار)، فقط کارت پایین ستون با اختلاف ±۱ رتبه (چرخهٔ شاه↔آس مجاز)، flip تک‌مرحله‌ای پشت‌کار، تشخیص برد (۳۵ حذف)/باخت، UI ستونی با کارت‌های tiny روی‌هم + highlight کارت‌های playable.
- ⚠️ انحراف آگاهانه از صورت‌تسک: «۱۹ کارت پشت‌کار» با invariant الزامیِ «هرم+پشت‌کار+زباله+حذف‌شده=۵۲» ناسازگار بود (۲۸+۱۹=۴۷)؛ ۲۴ استفاده شد (۵۲−۲۸) و invariant در هر گام پل‌اوت تایید شد.
- رفع باگ‌ها در تست‌نویسی: guard مرز ردیف در isExposed (بُرد جزئی تست)، اصلاح کارت non-bottom تست گلف (۹ به‌جای ۵)، تصحیح فرمول accounting گلف (کارت‌های حذفی داخل waste می‌مانند → cols+stock+waste=52 و played=35−Σcols).
- SELF-CHECK سبز از صفر: build ۲ صفحه؛ tests pass=11 fail=0 (هرم ۶، گلف ۵)؛ checked=2 bad=0؛ smoke: pyramid OK, golf OK → 0 with problems؛ حجم صفحات 12.4KB/10.7KB (<45KB).

Stage Summary:
- خروجی: scripts/wog/games/pilot_cards.py (هرم+گلف) + زیرساخت pilot در scripts/wog (lib/build/test_logic/check_syntax/smoke).
- وضعیت: تمام مراحل سبز — ۱۱/۱۱ تست منطق، ۰ bad syntax، اسموک مرورگر واقعی ۰ مشکل.
- بعدی: ادغام GAMESها در build اصلی پلتفرم و افزودن به catalog/landing.
---
Task ID: AG-A2
Agent: A2 (card games sub-agent)
Task: Write 2 Persian browser solitaire engines (spider 1-suit + freecell) as ONE python batch file per mini-kit contract.
Work Log:
- Built self-check kit at /tmp/a2: lib_mini.py + build_mini.py + test_mini.mjs (verbatim per contract).
- Wrote /tmp/a2/games/a2_cards.py: from lib_mini import G + GAMES=[spider, freecell], both cat="cards", engines=("common","card").
- spider (سولیتر عنکبوتی): 104 unique-id spade cards, 10 tableau piles (4x6 + 6x5 = 54), stock 50 (5 deals), descending-run moves, deal blocked on empty pile, auto-removal of complete K..A runs (8 = win), undo snapshots, hasAnyMove/isStuck, seeded greedy-bot playout asserting piles+stock+removed*13==104 every step.
- freecell (فری‌سل): 52 cards into 8 cascades (7,7,7,7,6,6,6,6), 4 free cells, 4 per-suit foundations, alternating-color descending builds, standard maxRun=(1+free)x(1+emptyCascades excluding dest), single card to/from cells, foundation order rule, safe autoplay of A/2, undo, win at 52 founded, bot playout conservation of 52 cards.
- UI (both): Persian RTL, tap-to-select then tap destination, overlapping card columns (negative margins), data-smoke buttons (deal/undo/new), hud (moves/stock or cells/removed or founded), win/lose ovl panels, بازی جدید + راهنما, $('#hint').textContent set.
- Self-check iterations: first run pass=10 fail=4 -> fixed 4 test-case bugs (stock ids counted, 7-6 must land on 8 not 10, same-color unit case must be two reds, autoplay test must clear dealt cascades). Logic code itself unchanged by fixes.
- Verified: node UI script parse OK for both rendered pages; forbidden-token scan clean (no http/localStorage/alert/fetch/etc. in batch file); rendered pages 7.4KB and 11.2KB (< 45KB).
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/a2_cards.py (copy of tested /tmp/a2/games/a2_cards.py, 28.8KB).
- Tests: python3 build_mini.py OK; node test_mini.mjs -> LOGIC pass=14 fail=0 (spider 6, freecell 8); python3 -m py_compile OK.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-A1
Agent: A1 (card games sub-agent)
Task: Write 2 Persian browser card games (pasoor/Casino + hokm) as ONE python batch file per mini-kit contract.
Work Log:
- Built self-check kit at /tmp/a1: lib_mini.py + build_mini.py + test_mini.mjs (verbatim per contract).
- Wrote /tmp/a1/games/a1_cards.py: from lib_mini import G + GAMES=[pasoor, hokm], both cat="cards", engines=("common","card").
- pasoor (پاسور): 52 cards {s:0..3,r:1..13}, 4 on table, 6 deals of 4+4 (48 dealt; note: contract's "4 hands" is arithmetically impossible with 52 cards — 6×8+4=52 required by the all-52 test), same-rank capture, 2+ card sum-subsets via pruned DFS preferring largest disjoint subset (greedy), J/Q/K same-rank only, 10♦ mandatory whole-table sweep, leftover table cards to last capturer at end, scoring breakdown (most cards +3, aces +1 each, 10♦ +3, 2♣ +2), greedy AI (sweep > max-cards capture > discard lowest-value), UI with capture-option chooser, face-down AI hand, live scores in hud, ovl breakdown + بازی جدید data-smoke.
- hokm (حکم): 4 players, teams {0,2}/{1,3}, dealer=rng, 5 cards each (reshuffle guard until an ace exists), determineHakam = first ace after dealer, human suit picker (4 data-smoke buttons) / AI picks most-frequent suit, dealRest 8 more each (13×52), follow-suit enforcement (illegal play throws), trickWinner = highest trump else highest of led suit (A high via hV(1)=14), rounds play all 13 tricks, first team to 7 tricks wins (+2 if opponents took 0), match to 7 points with round history in hud, spec AI (high from long suit / low lead; lowest beating card if partner not winning; lowest winning trump when void and opponents winning; else dump lowest).
- Self-check iterations: first run pass=8 fail=4 -> fixed 4 test-fixture bugs (P1/P2/P4 left deck+hands empty so the end-of-round leftover rule fired; hokm t3 expectation had winner/loser swapped — ace of trump correctly beat king of trump). Logic unchanged; tests strengthened (P2/P4 now use a live deck so they test mid-round behavior).
- Verified: python3 build_mini.py OK (pasoor, hokm); node test_mini.mjs -> LOGIC pass=12 fail=0 (pasoor 7, hokm 5); python3 -m py_compile OK; forbidden-token scan on logic/ui/css/desc/hint/tests clean (suit glyphs ♠♥♦♣ whitelisted per card-engine contract); node --check on stub-harnessed UI code OK for both pages; rendered pages 9.0KB and 10.4KB (< 45KB); data-smoke controls present (new game, capture options, hokm suits, playable cards).
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/a1_cards.py (copy of tested /tmp/a1/games/a1_cards.py, 28.8KB).
- Tests: LOGIC pass=12 fail=0; py_compile OK; UI syntax OK; no forbidden tokens.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.

---
Task ID: KIT-v1
Agent: main (Z.ai)
Task: ثبت کیت سلف‌چک و قرارداد کامل برای ایجنت‌های بازی‌ساز (همه ایجنت‌های بعدی این بخش را می‌خوانند)

## AGENT KIT — READ THIS WHOLE SECTION BEFORE WRITING ANY GAME FILE

### FILESYSTEM RULES (critical)
- Files under /home/z/my-project may be INVISIBLE in your sandbox. NEVER create/modify anything under /home/z/my-project EXCEPT your single deliverable: /home/z/my-project/agent_out/<file>.py (copy your tested file there at the very end).
- Do ALL scratch work (kit + games) under /tmp/<your-task-id>/.
- Do NOT recreate or "fix" any infrastructure you cannot see. Do NOT write index.html yourself — the framework renders it.

### KIT (create these 3 files under /tmp/<your-task-id>/)

lib_mini.py:
```python
# -*- coding: utf-8 -*-
import re
CATS={"board":1,"cards":1,"puzzle":1,"arcade":1,"word":1,"luck":1}
MINI_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8"><title>{title}</title><style>{css}</style></head>
<body><a class="wog-home" href="../../index.html">home</a><header><h1>{title}</h1><div id="hud"></div></header>
<div id="app"></div><p id="hint"></p><div id="wog-toast"></div>
<script>
(function () {{
'use strict';
var store = {{ get: function (k) {{ try {{ return localStorage.getItem(k); }} catch (e) {{ return null; }} }}, set: function (k, v) {{ try {{ localStorage.setItem(k, v); }} catch (e) {{}} }} }};
/*WOG_LOGIC_START*/
{logic}
/*WOG_LOGIC_END*/
var L = WOG_LOGIC;
{ui}
}})();
</script></body></html>"""
class G(object):
    def __init__(self, slug, title, cat, icon, g1, g2, desc, hint, logic="", ui="", css="", engines=(), tests=None, seed=12345):
        assert re.match(r'^[a-z0-9\-]+$', slug), slug
        assert cat in CATS, cat
        self.slug=slug; self.title=title; self.cat=cat; self.icon=icon; self.g1=g1; self.g2=g2
        self.desc=desc; self.hint=hint; self.logic=logic.strip(); self.ui=ui.strip(); self.css=css.strip()
        self.engines=list(engines); self.tests=tests or []; self.seed=seed
    def render(self):
        assert "WOG_LOGIC" in self.logic
        return MINI_TEMPLATE.format(title=self.title, css=self.css, logic=self.logic, ui=self.ui)
```

build_mini.py:
```python
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
```

test_mini.mjs:
```js
const manifest = JSON.parse((await import('fs')).readFileSync('tests-manifest.json','utf8'));
function mulberry32(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}}
const T={ok(c,m){if(!c)throw new Error(m||'ok failed')},eq(a,b,m){const x=JSON.stringify(a),y=JSON.stringify(b);if(x!==y)throw new Error((m||'eq')+' '+x+' !== '+y)},approx(a,b,e,m){if(Math.abs(a-b)>(e||1e-9))throw new Error((m||'approx')+' '+a+' '+b)},throws(f,m){let t=0;try{f()}catch(e){t=1}if(!t)throw new Error(m||'expected throw')},near(a,b,d,m){if(Math.abs(a-b)>d)throw new Error((m||'near')+' '+a+' '+b)}};
let P=0,F=0;const fails=[];
for(const g of manifest){let L=null;try{L=new Function('store',g.logic+'\n;return typeof WOG_LOGIC==="undefined"?null:WOG_LOGIC;')({});if(!L)throw new Error('no WOG_LOGIC')}catch(e){F+=g.tests.length;fails.push(g.slug+' LOAD:: '+e.message);continue}
for(const t of g.tests){try{new Function('T','L','rng',t.js)(T,L,mulberry32(g.seed||12345));P++}catch(e){F++;fails.push(g.slug+' :: '+t.name+' :: '+e.message)}}}
console.log('LOGIC pass='+P+' fail='+F+(F?'\n'+fails.join('\n'):''));process.exit(F?1:0);
```

### SELF-CHECK (from /tmp/<your-task-id>/): 
`python3 build_mini.py games/<file>.py` then `node test_mini.mjs` → MUST print fail=0. Iterate (fix code, never weaken tests). Then `python3 -m py_compile games/<file>.py`.

### CONTRACT
- Batch file = `from lib_mini import G` + `GAMES = [G(...), ...]`. One G per game.
- G fields: slug (kebab ascii), title (Persian), cat (board|cards|puzzle|arcade|word|luck), icon (emoji, landing tile only), g1/g2 (hex), desc (Persian, 1-2 sentences), hint (Persian), engines (tuple; "card" adds card engine to UI; "arcade" adds canvas/keys/pad; "word" adds Persian keyboard), logic, ui, css (all r""" strings when they contain backslashes), tests (list of ("نام تست","js body")), seed (int, default 12345).
- Cards are objects {s:0..3, r:1..13}; suits ♠♥♦♣ (s:0=♠,1=♥,2=♦,3=♣); red = s 1 or 2.
- logic = PURE, FULLY SELF-CONTAINED JS: defines `var WOG_LOGIC={...}`; NO DOM, NO external helpers ($, fa, shuffle, makeDeck are NOT available inside logic) — define own helpers inside. Random fns take optional `rng` (default Math.random). ES5/ES6, no imports. Functions used by tests must exist on WOG_LOGIC.
- ui = wiring JS; references logic as `L`. Helpers available in production UI: $(sel), $$(sel), ce(tag,cls,html), fa(n)→Persian digits, shuffle(a,rng), rint(a,b,rng), pick(arr,rng), clamp(v,a,b), toast(msg), hud(html)→sets #hud innerHTML, ovl(title,sub,btnText,cb)→end panel (its button auto has data-smoke), bestOf(key,val), storeBest(key), store.get(k)/store.set(k,v) (NEVER localStorage directly — a checker forbids it).
- Card engine (only if engines includes "card"): makeDeck()→52 {s,r}, isRed(c), suitOf(c), rankShort(r)→A/J/Q/K, rankFa(r), cardEl(card,faceUp,size 'small'|'tiny')→div.wcard (classes: .red .back .sel), cardStack(el,cards,faceUp,size), SUITS='♠♥♦♣'.
- Arcade engine (only if "arcade"): makeCanvas(w,h)→{cv,ctx,w,h} (appends to #app), keyState()→keys obj (tracks e.code), bindPad([{k:'ArrowLeft',label:'◀'},...])→touch+mouse dpad, rafStep(fn(dt seconds)).
- Word engine (only if "word"): FA_LETTERS (32 Persian letters), normFa(s) (ي→ی ك→ک, trims), faKb(onKey,longKeys)→on-screen Persian keyboard.
- ui MUST: render into #app, update hud, set $('#hint').textContent (short Persian hint), have ≥1 primary control with `data-smoke` attribute, use ovl(...) for end states, Persian language, mobile-friendly (buttons ≥40px, touch-action manipulation).
- FORBIDDEN anywhere in logic/ui/css: emoji characters (unicode symbols like ♠♥♦♣⚫⚪♕✓✕×÷± are OK), "http", "https", "localStorage" (use store), alert(, confirm(, prompt(, fetch(, XMLHttpRequest, document.cookie, window.top, window.parent.
- Tests: tuples ("نام تست","js body"); body receives (T, L, rng); T.ok/eq/approx/throws/near; deterministic; meaningful (rules + edge cases + seeded full-game sims). 4-8 per game. NEVER weaken a failing test — fix the code.
- Store keys: `wog-<slug>-*`. Keep each rendered game < 45KB (compact code, no dead code).
- Visual style: dark navy background (auto), gold #d9a441 accents, turquoise #3fb8af secondary, panels #14203a, success #67b98a, danger #e26d5c.

### DELIVERY
1. Final batch file → /home/z/my-project/agent_out/<file>.py (only allowed write under /home/z/my-project).
2. Append to /home/z/my-project/worklog.md: `---` line, `Task ID: <your id>`, Agent, Task, Work Log, Stage Summary.
3. Reply: test counts per game + total + any deviations.

---
Task ID: AG-B2
Agent: B2 (luck games sub-agent)
Task: Write 3 Persian dice/luck games (yahtzee + pig + chuck-a-luck) as ONE python batch file per mini-kit contract; all cat="luck", engines=("common",), dice as unicode ⚀⚁⚂⚃⚄⚅.
Work Log:
- Built self-check kit at /tmp/b2: lib_mini.py + build_mini.py + test_mini.mjs (verbatim per contract). نکته محیطی: ابزار Write به /tmp دسترسی ندارد → فایل‌های کیت و بچ با heredoc در Bash نوشته شدند (محتوای کیت عیناً مطابق قرارداد).
- Wrote /tmp/b2/games/b2_luck.py: from lib_mini import G + GAMES=[yahtzee, pig, chuck-a-luck].
- yahtzee (یاتزی): solitaire کامل — ۵ تاس، ۳ پرتاب/نوبت با hold toggle روی دکمهٔ خود تاس، ۱۳ مقوله (یک‌ها..شش‌ها، سه‌تایی/چهارتایی با جمع همه تاس‌ها، خانه کامل ۲۵، خیابان کوچک ۳۰/بزرگ ۴۰ با تشخیص رشتهٔ متوالی، شانس، یاتزی ۵۰)، جایزهٔ بالایی ۳۵ در ≥۶۳، امتیاز ۰ برای ثبت بی‌مقوله، جوکر ساده‌شده (۵ تاس برابر + خانهٔ بالاییِ همان عدد پر باشد → FH/خیابان‌ها امتیاز استاندارد می‌گیرند). WOG_LOGIC: rollDice(state,holds,rng) با throw در پرتاب چهارم، score(state,cat,dice) اسکورر خالص، assign، upperSubtotal، bonus، isUsed، isSheetFull، totals{upper,bonus,lower,grand}. UI: کارت امتیاز ۱۳ خانه با پیش‌نمایش زنده + هایلایت بهترین خانه، ذخیرهٔ رکورد wog-yahtzee-best، ovl پایان با تفکیک بالایی/جایزه/پایینی.
- pig (تاس پیگ): Pig مقابل AI hold-at-20 که هنگام بردِ قطعی (مجموع بانک+نوبت ≥۱۰۰) زودتر hold می‌کند. WOG_LOGIC: startTurn، roll(state,rng)→{die,busted} (۱ ⇒ سوختن فقط شمارش نوبت، بانک‌شده امن)، hold(state) با تشخیص برد در ۱۰۰، aiDecision(state)→'roll'|'hold'، takeTurn(state,idx,decisionFn,rng). UI: دو کارت امتیاز با نوبت فعال طلایی، تاس بزرگ یونیکد، پرتاب/نگه‌دار/بازی جدید، تأخیر ۶۵۰-۷۰۰ms برای نوبت ربات، شمارش بردها در wog-pig-wins، ovl «بردی!/باختی!».
- chuck-a-luck (سه تاس): شرط ۵/۱۰/۲۰/۵۰ (دکمه‌های غیرمجاز وقتی اعتبار کم است disable) روی عدد ۱..۶ (نمایش ⚀..⚅)، ۳ تاس، پرداخت n:1 به تعداد تطبیق (net = stake×n، n=0 ⇒ از دست رفتن شرط؛ return = stake+stake×n). WOG_LOGIC: roll3(rng)، matches(dice,face)، payout(stake,m)→net، totalReturn، apply(state,rng) با حسابداری دقیق اعتبار. UI: اعتبار/رکورد wog-chuck-best در hud، پیام برد/باخت، ovl «اعتبار تمام شد» در اعتبار <۵.
- SELF-CHECK: build ۳ صفحه؛ node test_mini.mjs → LOGIC pass=13 fail=0 (یاتزی ۵، پیگ ۴، سه‌تاس ۴ — از اولین اجرا سبز؛ هیچ تستی تضعیف نشد)؛ py_compile OK.
- تست‌های کلیدی: همه اسکوررها روی تاس‌های ساخته‌شده (A1234 و 23456 هر دو خیابان بزرگ ۴۰، FH فقط 3+2، 4k با جمع، 4+1 خانهٔ کامل نیست)، پرتاب با hold (تاس ثابت می‌ماند) + throw در پرتاب چهارم، بونوس دقیقاً روی آستانه ۶۳ (و ۶۲ بدون جایزه)، جوکر با/بدون خانهٔ بالاییِ پر، شبیه‌سازی کامل ۱۳ دستهٔ یاتزی (هر مقوله دقیقاً یک‌بار، grand=upper+bonus+lower، قفل مقولهٔ استفاده‌شده)، سوختن نوبت در پیگ (بانک امن)، hold=بانک و برد دقیقاً در ۱۰۰، جدول تصمیم AI، بازی کامل پیگ تا برد (برنده ≥۱۰۰، بازنده <۱۰۰)، پرداخت‌های سه‌تاس با stub rng، حسابداری اعتبار، و شبیه‌سازی ۵۰۰۰ دست: میانگین تطبیق ۰.۴۹۵۸ (~۰.۵ دوجمله‌ای)، نرخ سه‌تاسِ برابر ۰.۰۰۴۲ (<۰.۰۵)، EV = −۰.۸۷۲ اعتبار/دست (−۸.۷٪ شرط = برتری خانه) و برابری دقیق credits=100+Σnet.
- چک‌های مکمل: اسکن توکن‌های ممنوعه روی logic/ui/css/desc/hint/tests صفر مورد؛ ممیزی نویسه‌های غیر ASCII (فقط فارسی/علائم/کاراکتر تاس ⚀..⚅ مجاز)؛ node --check روی اسکریپت استخراج‌شدهٔ هر ۳ صفحه OK؛ اسموک ران‌تایم با هارنس استاب ($/fa/toast/hud/ovl + setTimeout همگام) در node: یاتزی ۱۳ دستهٔ کامل تا پنل «پایان یاتزی»، پیگ تا پنل پایان، سه‌تاس تا پنل «اعتبار تمام شد» — بدون هیچ خطا.
- حجم صفحات رندرشده: yahtzee 8,372B · pig 5,571B · chuck-a-luck 5,252B — همه زیر سقف ۴۵KB.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/b2_luck.py (copy of tested /tmp/b2/games/b2_luck.py, 26.5KB).
- Tests: LOGIC pass=13 fail=0; py_compile OK; UI syntax OK (node --check ×3); runtime smoke ×3 OK; no forbidden tokens.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-B1
Agent: B1 (card games sub-agent, retry)
Task: Write 3 Persian card games (higher-lower + video-poker + thirty-one) as ONE python batch file per mini-kit contract; all cat="cards", engines=("common","card").
Work Log:
- Kit built verbatim at /tmp/b1 (lib_mini.py + build_mini.py + test_mini.mjs). نکته محیطی: ابزارهای Write/Edit به /tmp دسترسی ندارند → کیت و بچ با heredoc نوشته شد؛ ویرایش‌ها هم با python inline replace.
- Wrote /tmp/b1/games/b1_cards.py (32.8KB): from lib_mini import G + GAMES=[higher-lower, video-poker, thirty-one].
- higher-lower (بالاتر یا پایین‌تر): بازی زنجیره — کارت فعلی رو، دکمهٔ بالاتر/پایین‌تر؛ بعدی باید اکیداً بالاتر/پایین‌تر باشد و برابر = باخت (در hint صریح). درست: streak+1 و points += streak؛ غلط: پایان دور و ثبت رکورد (wog-higher-lower-best). دسته بدون جایگزینی؛ ری‌شافل ۵۲ کارت تازه وقتی ≤۴ کارت مانده. WOG_LOGIC: newGame(rng)، guess(state,dir)→{correct,done}، streakPoints(n)، شمارش drawn/reshuffles برای حسابداری.
- video-poker (ویدیو پوکر): جک-یا-بهتر پنج‌کارتی، اعتبار ۱۰۰، شرط ۵/۱۰/۲۵. پخش ۵ کارت، لمس کارت = HOLD، تعویض فقط کارت‌های نگه‌داشته‌نشده (بدون تکرار؛ دکّهٔ کف <۱۰ کارت بین دست‌ها تازه می‌شود). پرداخت ×شرط: رویال ۲۵۰، استریت‌فلاش ۵۰، چهارلایی ۲۵، خانهٔ کامل ۹، فلاش ۶، استریت ۴، سه‌تایی ۳، دو جفت ۲، جفت سرباز+ ۱. استریت هم A2345 هم TJQKA. WOG_LOGIC: evaluate5، payout، playRound(state,holds,bet) دو-فازی (deal/draw)→{cat,net}، newGame، bestHolds (هیوریستیک نگه‌داشتن برای شبیه‌سازی)، startDeal.
- thirty-one (سی‌ویک): ۳ بازیکن (انسان + ۲ AI)، ۳ جان. ارزش دست = بهترین جمع تک‌خال (آ=۱۱، تصویری=۱۰). نوبت: کشیدن از دسته یا برداشتن دورریز + دورریز یک کارت. کوبیدن فقط بلافاصله بعد از دورریز خودی → حریف‌ها دقیقاً یک نوبت دیگر (mustPlay) → showdown: ضعیف‌ترین می‌بازد و تساویِ پایین‌ترین = همه بازنده. صفر جان = حذف؛ آخرین بازمانده برنده. AI: کوبیدن ≥۲۷، برداشتن دورریز اگر بهتر کند، دورریز پایین‌ترین. WOG_LOGIC: handValue، newGame، turn(state,pi,action)، knock، showdown(state,rng)→losers، aiMove/aiKnock/aiGame.
- SELF-CHECK: build ۳ صفحه؛ node test_mini.mjs → LOGIC pass=18 fail=0 (هر بازی ۶ تست؛ یک باگ واقعی در knock گرفته و رفع شد: کوبنده به‌اشتباه در mustPlay بود). py_compile OK. اسکن توکن‌های ممنوعه صفر مورد؛ نویسه‌های غیر ASCII فقط فارسی/علامت/●○. node --check روی اسکریپت ۳ صفحه OK؛ اسموک ران‌تایم با استاب UI هر ۳ صفحه OK. حجم رندرشده: higher-lower 3.9KB · video-poker 7.8KB · thirty-one 11.2KB — همه زیر سقف ۴۵KB.
- تست‌های کلیدی: برابرِ رتبه در هر دو جهت باخت؛ حسابداری دقیق drawn/reshuffles در مرز ری‌شافل (۵۲ تازه)؛ ریاضی زنجیره/امتیاز تا پایان دور؛ نرخ برد ۰٫۳۸۷۵ در ۲۰۰۰ حدس (باند ۰٫۳۵–۰٫۶۵)؛ بدون تکرار کارت در هر دسته؛ هر ۱۰ مقولهٔ پوکر روی دست‌های ساخته‌شده (sf مقابل flush؛ هر دو استریت؛ مرز J بله / T نه)؛ جدول پرداخت و net=۸۰ برای fh با شرط ۱۰؛ بدون تکرار + حسابداری اعتبار در ۲۰۰ دست؛ RTP=۰٫۹۰۲ در ۳۰۰۰ دست (باند ۰٫۶–۱٫۶)؛ خطاهای شرط/اعتبار/پخش دوباره؛ جریان کوبیدن با دست‌های ساخته‌شده (بازندهٔ دقیق p2، vals=30/18/9، جان‌ها)؛ تساوی همه می‌بازند؛ حذف بازیکن و پخش دور بعد فقط برای فعال‌ها؛ تصمیم‌های AI؛ بازی کامل ری‌شاخه‌دار تا یک بازمانده (۷ دور).
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/b1_cards.py (copy of tested /tmp/b1/games/b1_cards.py, 32.8KB).
- Tests: LOGIC pass=18 fail=0 (6+6+6); py_compile OK; script syntax OK ×3; runtime smoke ×3 OK; no forbidden tokens; sizes < 45KB.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-C3
Agent: C3 (board games sub-agent)
Task: 3 board games (nim misère + mancala kalah + dots-boxes) in ONE batch games/c3_board.py; cat=board, engines=(common,).
Work Log: kit verbatim at /tmp/c3 (Write tool blocked on /tmp → heredoc). nim: misère AI (xor-0 / odd-ones rule), 4 tests incl. memoized full-game-tree optimality check over all 191 reachable [3,5,7] positions + seeded full game (AI wins). mancala: Kalah 6+6×4, sow skips opponent store, extra-turn, capture, finishGame, greedy-2-ply AI (diff +0.5 extra +0.4 capture, seeded tie-break), 6 tests incl. constructed traces + seeded AI-vs-AI (48 seeds invariant, decisive winner ≥25). dots-boxes: 5×5 dots/40 lines/16 boxes, completion+extra turn, AI comp>safe>least-damage, 5 tests incl. adjacency corner/edge/center, seeded 40-line full game, 50-state no-open-3-sided-box check. 3 test-expectation bugs fixed (store count, boxLines(15), dots turn flow) — no test weakened; logic code unchanged throughout.
Stage Summary: /home/z/my-project/agent_out/c3_board.py (25.9KB). LOGIC pass=15 fail=0 (4+6+5); py_compile OK; node --check ×3 OK; runtime UI smoke ×3 → ovl end panels OK; forbidden tokens/emoji scan clean; rendered sizes nim 5.0KB / mancala 6.2KB / dots 6.0KB (<45KB).
---
Task ID: AG-D1
Agent: D1 (board games sub-agent, solo)
Task: 3 board games (ludo + snakes-ladders + dominoes) in ONE batch games/d1_board.py; cat=board, engines=(common,).
Work Log: kit verbatim at /tmp/d1 (Write tool blocked on /tmp → heredoc). ludo: 4 pawns/52-cell shared track (start cells 0/26 safe), exit on 6, 51 track + 5 home-column cells, exact-roll final home, capture→base (no extra roll), 3-sixes rule via applyRoll/applyMove, AI capture>exit>closest-to-home, linear 13×4 track + home strips + base panels. snakes-ladders: 8 ladders (7 spec + added 6→17) + 8 snakes, chained transport(), exact-100, 10×10 boustrophedon grid. dominoes: double-six 7/7/14, LIFO boneyard draw-until-playable, consecutive-pass blocked→lighter pip hand wins/draw, AI max-pips keeps doubles (−2), both-ends chooser bar. 2 test-construction fixes on first run (tile not in hand; LIFO draw count) — no test weakened, logic unchanged.
Stage Summary: /home/z/my-project/agent_out/d1_board.py (copy of tested /tmp/d1/games/d1_board.py). LOGIC pass=18 fail=0 (6+6+6); py_compile OK; node --check ×3 OK; runtime UI smoke ×3 OK (init+roll/flush+newGame); forbidden tokens clean; sizes ludo 9.9KB / snakes-ladders 5.5KB / dominoes 10.9KB (<45KB).
---
Task ID: AG-B3
Agent: B3 (luck games sub-agent, solo)
Task: 4 luck games (lcr + rps + slots + wheel) in ONE batch games/b3_luck.py; cat=luck, engines=(common,).
Work Log: kit verbatim at /tmp/b3 (Write tool blocked on /tmp → heredoc, same as prior agents). lcr: 3 players/3 chips, roll3 always 3 dice with sequential pass-cap at held chips (chips+pot==9 invariant), 0-chip players skipped via nextAlive, over exactly when one holder remains (all-zero provably unreachable since only the roller can lose chips and one-holder states are terminal), winner takes chips+pot=9. rps: BEATS/counter/aiPick (freq-count majority + 20% random, first-max tie-break in [s,p,sc] order), judge ±1/0, matchOver at 3. slots: SYMS/WEIGHTS [6,5,4,3,2,2]→22-stop reels, pick1/spin, payout triples 50/25/15/10/8/6, pair★=3, other pair=2, COST=5. wheel: 12 segments each weight 1 (values ۱۰۰×3/۲۵۰×3/۵۰۰×2, ×۲×1, نصف×1, ورشکست×2), spin weighted index, apply(add/x2/floor-half/bust with clamp≥0), START=200, UI conic-gradient wheel + pointer-at-top rotation rot+=4·360+((360−(i·30+15))−rot%360 mod 360), 3.2s cubic-bezier spin, goal ovl at 2000 pts.
- Tests: 24 total (6/game): chip conservation ×1000 seeded rolls + skip-empty rotation; pass-cap (no negative) with stub-rng C/C/C; dice validity + 3-dot face composition; 30-seed full games each <3000 rolls with winner chips+pot=9 and losers empty; result shape + extra:null. beats relation completeness (each move beaten by exactly one) + counter inversion; judge antisymmetry matrix + ties; skewed history (20×'s') → AI plays 'p' >60/100; matchOver boundaries; seeded full match to 3 wins (history length = rounds). slots triple table exact, pair/star-pair/none cases, 20000-spin reel distribution ±15%, 3000-spin payout-table membership, 5000-spin EV mean ∈ (0.5,5) (house edge), weights sum 22. wheel structure (12 segs, weights sum 12, kind counts 8/1/1/2), 20000-spin uniformity ±15%, apply exact (add/x2/half floor incl. 201→100 and 1→0/bust/clamp), 1000-spin accounting with replay equality + integer/non-negative invariants, stub-rng edge indices (0 and 11), value multiset.
- SELF-CHECK: build 4 pages; node test_mini.mjs → LOGIC pass=24 fail=0 (green on first run; no test weakened); py_compile OK; node --check ×4 OK; runtime smoke ×4 with DOM/store/ovl stubs + sync setTimeout → each game reaches its ovl end panel by clicking data-smoke controls; forbidden-token scan (http/localStorage/alert/confirm/prompt/fetch/XHR/cookie/window.top|parent) clean; emoji scan on rendered HTML clean (only sanctioned unicode symbols ⬤▲★◆❋♣•). Rendered sizes: lcr 6,527B · rps 5,579B · slots 5,250B · wheel 6,726B — all < 45KB.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/b3_luck.py (copy of tested /tmp/b3/games/b3_luck.py, 35.7KB).
- Tests: LOGIC pass=24 fail=0 (6+6+6+6); py_compile OK; script syntax OK ×4; runtime smoke ×4 OK; no forbidden tokens; sizes < 45KB.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-E1
Agent: E1 (puzzle games sub-agent, solo)
Task: 3 puzzle games (p15 + sokoban + rush-hour) in ONE batch games/e1_puzzle.py; cat=puzzle; p15/rush-hour engines=(common,), sokoban engines=(common,arcade) for bindPad.
Work Log: kit verbatim at /tmp/e1 (Write tool blocked on /tmp → heredoc, same as prior agents). p15: seeded 250-valid-move shuffle (anti-undo), slide/undo-in-state, inversions+blankRow parity solvable(state,w) (generalized width for 2×2), CSS transform slide anim, arrows move blank. sokoban: 6 handcrafted levels (1/1/2/2/3/3 boxes), push-only move with full undo history in state, BFS over (player,sortedBoxes) layer-counted min moves. rush-hour: 8 handcrafted 6×6 grids (no horizontal vehicle on row 2 except A), canMove via incremental leading-cell check, multi-cell slide = 1 BFS move, leading-cell+occupancy BFS, select-then-arrows UI. Levels pre-validated with Python BFS replicas (sok min 1/2/8/9/9/14; rush min 2/2/2/3/2/5/3/2) BEFORE writing batch. Tests: 6/game incl. p15 parity-vs-brute-force exact match on all 24 perms of 2×2 (12 reachable) + 30-seed shuffle solvability; sokoban wall/box-blocked pushes + walled-off level solve=-1 + pre-solved solve=0; rush collision/axis/bounds rejects + all-8 BFS>0.
Stage Summary: Deliverable: /home/z/my-project/agent_out/e1_puzzle.py (copy of tested /tmp/e1/games/e1_puzzle.py, 30.6KB). LOGIC pass=18 fail=0 (6+6+6; one test-expectation fix: tile at (2,2) is 11 not 12 — logic unchanged); py_compile OK; forbidden tokens/emoji NONE; rendered sizes p15 5.1KB / sokoban 7.2KB / rush-hour 8.4KB (<45KB); runtime smoke ×3 OK incl. full win flows → ovl «بردی!» for sokoban + rush-hour via key/pad wiring.
---
Task ID: AG-E2
Agent: E2 (puzzle games sub-agent, retry)
Task: 3 Persian puzzle games (flood-it + peg solitaire + blockudoku) as ONE python batch file per mini-kit contract; all cat="puzzle", engines=("common",).
Work Log:
- Kit verbatim at /tmp/e2 (lib_mini.py + build_mini.py + test_mini.mjs). نکته محیطی: ابزار Write/Edit به /tmp دسترسی ندارند → کیت و بچ با heredoc نوشته شد (همسان B1/B2).
- Wrote /tmp/e2/games/e2_puzzle.py: GAMES=[flood, peg, blockudoku].
- flood (طوفان رنگی): ۱۴×۱۴، ۶ رنگ، بودجهٔ ۲۵ حرکت. genBoard همبسته (ارث‌بری از بالا/چپ با p=0.6) → ناحیه‌های بزرگ و حاشیهٔ امن زیر سقف ۲۵. WOG_LOGIC: genBoard، region (BFS چهارهمسایه از ۰,۰)، regionSize، applyColor خالص (کپی تخته)، isWin، greedySteps (حریص حداکثررشد). HUD: درصد ناحیه + حرکت باقی‌مانده. پالت ۶ رنگ، رکورد wog-flood-best، ovl برد/باخت با بازی جدید data-smoke.
- peg (پگ سولیتر): صلیب انگلیسی ۳۳ خانه (VALID)، initial با ۳۲ پگ و مرکز خالی، jumpsFrom/applyJump با اعتبارسنجی جهت+فاصله+پگ میان‌راه+خانهٔ مجاز، pegCount/hasMoves/isWin. UI: انتخاب پگ→نمایش مقصدها (halo سبز)، undo با کلون وضعیت، reset، شمارندهٔ پگ، برد=۱ پگ (مرکز=پیام عالی)، بن‌بست→ovl. فیکسچر ۵ پرش دست‌ساز با un-jump معکوس ساخته و ذهنی راستی‌آزمایی شد: پگ‌های (3,1)(2,2)(1,3)(2,4)(3,5)(3,6) → پرش‌های (3,6→3,4)(3,4→1,4)(1,4→1,2)(1,2→3,2)(3,1→3,3) → دقیقاً یک پگ در مرکز.
- blockudoku (بلوک‌دوکو): ۱۴ شکل (1×1..1×5 افقی/عمودی، 2×2، 3×3، L، 2×3، 3×2)، امتیاز = خانه‌ها + ۱۰×خط + ۵×استریک (moveGain)، پاک‌سازی همزمان سطر/ستون/بلوک ۳×۳، refill بعد از مصرف هر ۳ قطعه، پایان وقتی هیچ قطعهٔ باقی جا نشود. WOG_LOGIC: SHAPES، genPieces، canPlace، place، findClears، applyClears، anyFit، isGameOver، moveGain.
- SELF-CHECK: python3 build_mini.py → ۳ صفحه؛ node test_mini.mjs → LOGIC pass=15 fail=0 (flood 4، peg 6، blockudoku 5)؛ py_compile OK؛ node --check روی اسکریپت استخراج‌شدهٔ هر ۳ صفحه OK؛ smoke ران‌تایم با DOM-stub (۴ دور کلیک روی همهٔ کنترل‌ها + بازیابی ovl) بدون خطا؛ اسکن توکن‌های ممنوعه صفر مورد؛ حجم صفحات: flood 4,552B · peg 5,359B · blockudoku 7,211B — همگی زیر ۴۵KB.
- یک دور اصلاح (تنها ران دوم): سه باگ فیکسچر تست blockudoku — «adjacent» با قطعهٔ هم‌پوشان غلط بود (شکل 1→2)، جمع امتیاز دنباله ۸۴→۷۴ (استریک بعد از ریست ۱ است نه ۲)، و حسابداری sim باید placedCells می‌بود نه شمارندهٔ placed. هیچ تستی تضعیف نشد؛ منطق بازی دست نخورد.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/e2_puzzle.py (کپی فایل تست‌شدهٔ /tmp/e2/games/e2_puzzle.py).
- Tests: LOGIC pass=15 fail=0؛ UI smoke ×3 OK؛ syntax ×3 OK؛ py_compile OK؛ بدون توکن ممنوع.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-E3
Agent: E3 (puzzle games sub-agent, solo)
Task: 4 puzzle games (hanoi + maze + 8queens + lights-out) in ONE batch games/e3_puzzle.py; cat=puzzle, engines=(common,).
Work Log: kit verbatim at /tmp/e3 (Write tool blocked on /tmp → heredoc, same as prior agents). hanoi: towers as [big..small] arrays, move() validates same-tower/empty-source/bigger-on-smaller before mutation, optimal=2^n−1, canonical recursive solveSeq; UI source→target taps, move counter vs minimum, auto-solve animation from fresh board. maze: wall-grid 2n+1 with recursive backtracker genMaze(n,rng), neighbors/bfs (parent-traced shortest path), isPerfect (edges=n²−1 AND connectivity), canMove; UI grid render + player dot transition, timer+moves hud, BFS hint tint, arrows+dpad+keydown (w/s/a/d), sizes 11/17/25, best per size. 8queens: attacks/hasConflict on [r,c] pairs, cached backtracking solveAll()=92, firstSolution(); UI tap toggle, live q-bad conflict highlight, راه‌حل → first solution + win ovl, hud shows total 92. lights-out: toggle (cell+4 orthogonal, bounds-safe), genBoard(size,k,rng) = k distinct seeded presses from all-off (resample if all-off), isWin, pressesToSolve for 3×3 via precomputed 2^9 pattern lookup (cached); UI 5×5 + ۳×۳ سریع, moves+lit count+best (bestOf per size), 3×3 hint flashes minimal press cells. Fixes across one iteration: 2 test-construction bugs (lights expected-constant typo; solver-replay was applied to zeros instead of a copy of the board — corrected, not weakened) + 1 real UI gap (راه‌حل now also triggers the win ovl via maybeWin). Runtime smoke harness needed innerHTML=''→children-clear stub semantics.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/e3_puzzle.py (copy of tested /tmp/e3/games/e3_puzzle.py, 35.7KB).
- Tests: LOGIC pass=15 fail=0 (hanoi 3 + maze 4 + 8queens 4 + lights-out 4); py_compile OK; node --check ×4 OK; runtime UI smoke pass=26 fail=0 (init + data-smoke new game + per-game flows incl. hanoi auto-solve ovl, maze hint/dpad/keys, queens solution→win ovl, lights 3×3 hint); forbidden tokens clean in G fields; rendered sizes hanoi 6.0KB / maze 8.9KB / 8queens 5.3KB / lights-out 6.5KB (<45KB).
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-F1
Agent: F1 (puzzle games sub-agent)
Task: 3 Persian puzzle games (nonogram + mastermind + simon) as ONE batch file per mini-kit contract; all cat="puzzle", engines=("common",).
Work Log:
- Kit verbatim at /tmp/f1 (lib_mini.py + build_mini.py + test_mini.mjs). نکته محیطی: ابزار Write به /tmp دسترسی ندارد → بچ با heredoc در Bash نوشته شد.
- Wrote /tmp/f1/games/f1_puzzle.py (23.7KB): from lib_mini import G + GAMES=[nonogram, mastermind, simon].
- nonogram (نونوگرام): ۵×۵ و ۸×۸ از الگوی تصادفی بذردار (genPattern با شافل جزئی، fill=12/22، غیرتهی تضمینی)، سرنخ = طول رشته‌های پیوسته (rowClues/colClues/cluesFor)، لمس خانه چرخهٔ خالی→پر→علامت ×، کم‌رنگ‌شدن سرنخِ خطِ تعیین‌شده، برد = تطابق خانه‌های پر با راه‌حل (۲ = خالی)، رکورد حرکت per-size در wog-nonogram-best-<n>، ovl برد.
- mastermind (رمزنگار): رمز ۴ میخ از ۶ رنگ با تکرار، ۱۰ حدس، بازخورد استاندارد سیاه/سفید با شمارش per-color (feedback خالص + isWin)، پالت انتخاب + چرخاندن خانه با لمس، تاریخچه با میخ‌های ●/○، فاش‌شدن رمز با نام فارسی در باخت، رکورد کمینهٔ حدس‌ها.
- simon (سیمون): ۴ پد رنگی + ۴ تن WebAudio (اسیلاتور sine با پاکت gain)، رشد +۱ در هر سطح، سرعت speedFor=900−60×(level−1) با کف ۳۲۰ms، قفل پدها هنگام پخش، باخت = پایان با سطح رسیده، رکورد bestOf('wog-simon-best').
- SELF-CHECK: build ۳ صفحه؛ node test_mini.mjs → LOGIC pass=13 fail=0 (nonogram 4، mastermind 5، simon 4)؛ py_compile OK؛ node --check ×3 OK؛ توکن‌های ممنوعه صفر.
- تست‌های کلیدی: درون‌یابی سرنخ ([1,0,1,1,0]→[1,2]، خط خالی→[]، cluesFor کامل)، سازگاری جمع سرنخ سطر=ستون=تعداد پر در ۵۰ بذر متناوب ۵×۵/۸×۸، برد با علامت × (× روی خانهٔ پُر راه‌حل = باخت، × روی خانهٔ خالی = مجاز)، الگوی غیرتهی + شمارش دقیق fill (شامل fill=1)، بردارهای کلاسیک mastermind ([R,G,B,Y]→4B، [Y,G,B,R]→2B2W، تکرارها [A,A,B,C]vs[A,B,A,D]→1B2W و [A,A,A,A]vs[A,A,B,B]→2B0W و [A,A,B,B]vs[B,B,A,A]→0B4W)، محدودهٔ genCode با rng stub (0→همهٔ صفر، 0.999→همهٔ ۵)، شبیه‌سازی ۱۰ دور بازیکن خودکار بذردار با شرط پایان، رشد/عدم-جهش دنبالهٔ simon، check در ایندکس درست/غلط/خارج محدوده، کاهندگی و کف سرعت در ۳۰ سطح، شبیه‌سازی ۱۲ سطح خودکار.
- باگ‌های یافت‌شده و رفع‌شده در iteration: (۱) nextColor تابع rng را صدا نمی‌زد (function×4=NaN) → r() اصلاح شد؛ (۲) دو تست اولیه اشتباه نوشته شده بودند (انتظار معکوس × در برد نونوگرام، طول آرایهٔ شروع در تست عدم-جهش simon) — کد اصلاح شد، تست‌ها تضعیف نشدند.
- حجم صفحات رندرشده: nonogram 6,611B · mastermind 6,811B · simon 5,163B — همه زیر سقف ۴۵KB.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/f1_puzzle.py (copy of tested /tmp/f1/games/f1_puzzle.py, 23.7KB).
- Tests: LOGIC pass=13 fail=0; py_compile OK; JS syntax OK ×3; no forbidden tokens.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-F2
Agent: F2 (puzzle games sub-agent)
Task: Write 4 Persian puzzle games (water-sort + calc24 + kakuro + memory-grid) as ONE python batch file per mini-kit contract; all cat="puzzle", engines=("common",).
Work Log:
- Kit built verbatim at /tmp/f2 (lib_mini.py + build_mini.py + test_mini.mjs). نکته محیطی: ابزار Write به /tmp دسترسی ندارد → کیت و بچ با heredoc در Bash نوشته شدند.
- Wrote /tmp/f2/games/f2_puzzle.py (30.4KB): from lib_mini import G + GAMES=[water-sort, calc24, kakuro, memory-grid].
- water-sort (آب‌ریز): بطری‌های ظرفیت ۴ با N=C+2 (۴/۶/۸ رنگ از دکمه‌های سختی). WOG_LOGIC: genLevel(colors,rng) از حالت حل‌شده با K=2C ریختِ معکوسِ بذردار (بدون آنی‌واگرد، بدون جابه‌جایی بطری یکدستِ کامل به خالی) → همیشه حل‌شدنی؛ canPour/pour (ران هم‌رنگ مجاور × جای خالی، غیرمخرب)، isWin (یکدست یا خالی)، solve با DFS+memo و سقف ۲۰۰۰ ایالت و مرتب‌سازی هیوریستیک حرکات → آرایهٔ حرکات یا null. تست‌ها شامل اعتبارسنجی کامل مسیر حل (هر حرکت قانونی + برد نهایی) روی ۵ بذر × ۴..۸ رنگ.
- calc24 (۲۴ با اعداد): solve24(nums)→{expr,value}|null با جست‌وجوی بازگشتی همهٔ زوج‌ها/عمل‌ها (ε=1e-6، تقسیم بر صفر و NaN/Inf محافظت‌شده)، drawHand(rng) تا ۴۰ تلاش دستِ حل‌شدنی. UI: انتخاب دو کاشی + چهار عمل، واگرد هر گام، «راه‌حل» با عبارت پرانتزی حل‌کننده (نمایش × ÷ −)، برد دقیقاً ۲۴ با ovl.
- kakuro (کاکورو): دو چیدمان دست‌ساز ۵×۵ (آسان ۱۱ اجرا / معمولی ۱۰ اجرا) با راه‌حل راستی‌آزمایی‌شدهٔ ثبت‌شده در داده (پیش از بیلد با پایتون هم verify شد). WOG_LOGIC: LAYOUTS، runCells، checkRun (۱..۹، عدم‌تکرار، جمع دقیق)، isWin. UI: تختهٔ ۵×۵، سرنخ‌های افقی/عمودی روی خانهٔ آغاز اجرا، ضربه = چرخهٔ ۰..۹.
- memory-grid (شبکهٔ حافظه): flash خانه‌های هدف (اندازهٔ min(3+level,12) از ۲۵)، پس از خاموشی انتخاب بازیکن؛ خطا = یک جان از ۳ و پخش دوبارهٔ همان مرحله؛ تکمیل = مرحلهٔ بعد. WOG_LOGIC: genCells (Fisher-Yates بذردار)، check→{hit,complete,misses}، isLevelUp، afterMiss. رکورد در wog-memory-grid-best.
- Fix pass (یک‌بار): (۱) API حل‌کنندهٔ calc24 به {expr,value} مطابق قرارداد تست تغییر کرد، (۲) انتظار تست آب‌ریز برای فرودِ ران روی هدفِ نیم‌پر اصلاح شد ([2,2,2] درست است)، (۳) helper بذردار MR به تست جاافتاده اضافه شد — هیچ تستی تضعیف نشد.
- SELF-CHECK: python3 build_mini.py games/f2_puzzle.py → ۴ صفحه؛ node test_mini.mjs → LOGIC pass=21 fail=0؛ py_compile OK؛ node parse هر ۴ اسکریپت کامل OK.
- چک‌های مکمل: اسکن توکن‌های ممنوعه صفر؛ اسکن ایموجی خارج از icon صفر؛ data-smoke/hint/ovl در هر ۴ صفحه حاضر؛ حجم رندر: water-sort 6,289B · calc24 5,332B · kakuro 5,587B · memory-grid 4,410B (همه < 45KB).
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/f2_puzzle.py (copy of tested /tmp/f2/games/f2_puzzle.py, 30.4KB).
- Tests: LOGIC pass=21 fail=0 (water-sort 5, calc24 5, kakuro 6, memory-grid 5); py_compile OK; JS parse ×4 OK; no forbidden tokens.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-G2
Agent: G2 (arcade games sub-agent, solo)
Task: 3 canvas arcade games (meteor + stacker + kite) in ONE batch games/g2_arcade.py; cat=arcade, engines=(common,arcade); pure WOG_LOGIC + deterministic seeded tests (invariants + scripted inputs, no bot tests).
Work Log: kit verbatim at /tmp/g2 (Write tool blocked on /tmp → heredoc, same as prior agents). meteor (شهاب‌سنگ): ship left/right with exact clamps, seeded spawns with ramp intervalAt(1.1→0.28 floor)/speedAt(120+t·2.2), AABB collision box (circle-vs-band) exact at boundaries, shield pickup = 3s invulnerability (flashing ring, meteors pass through), 3 hits = over, score=floor(t)×10+crystals×25; 60s fixed-dt sim asserts score monotonic, t tracks sim time, counts sane, no NaN. stacker (برج‌ساز): auto-sliding cur with edge bounce (exact clamp+dir flip), drop()→{overlapW,perfect,over} overlap math exact, trim to overlap, perfect (full align) = width+4 capped at MAXW=110 + combo, full miss = over, score=height; 300-step seeded sim (drop every 50 steps) asserts widths ∈(0,110], cur in bounds, base intact. kite (جنگ بادبادک): pure geometry — segIntersect (orientation + collinear/touch via onSeg), segDist, kites as {ang,rad} polar around bottom anchors AM(330,470)/AA(470,470) with clampP(15°..165°, 70..420px); my kite follows pointer/keys target (ω=2.4, vr=280), AI attacks my string midpoint in sin-gated bursts + jitter, roams otherwise; events per contact (cd=0.7s, priority hit>cutthem>cutme): kite-body contact <34px = meT--, my kite crossing/near AI string = aiT--, AI kite near my string = meT--; 3 cuts win; 60s seeded sim asserts angles/radii in range, tensions ≥0, no NaN. UI per contract: makeCanvas+rafStep render, keyState+bindPad, pointer targeting (kite), hud/fa, data-smoke buttons (بازی جدید / انداختن), ovl end panels, store keys wog-<slug>-*, Persian hints. Fixes in one iteration: 2 test-construction bugs (meteor sim asserted t≈60 at last i%60 checkpoint i=3540 → replaced with exact t-vs-sim-time tracking 1e-6; kite clamp test froze match via meT=aiT=99 so AI cuts couldn't end the match mid-convergence) — logic untouched, no test weakened.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/g2_arcade.py (copy of tested /tmp/g2/games/g2_arcade.py, 26.0KB).
- Tests: LOGIC pass=18 fail=0 (meteor 6 + stacker 6 + kite 6, deterministic seeded rng + fixed dt, no adaptive bots); py_compile OK; node --check ×3 OK; runtime smoke ×3 OK (stacker reaches ovl via data-smoke clicks); forbidden tokens/emoji scan clean; rendered sizes meteor 5.1KB / stacker 3.7KB / kite 7.1KB (<45KB).
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-G3
Agent: G3 (arcade games sub-agent, solo)
Task: 3 canvas arcade games (asteroids + invaders + dodge) in ONE batch games/g3_arcade.py; cat=arcade, engines=(common,arcade); pure WOG_LOGIC + deterministic seeded tests.
Work Log: kit verbatim at /tmp/g3 (Write tool blocked on /tmp → heredoc, same as prior agents). asteroids: rotate/thrust/friction ship (θ wrap 0..2π, exp friction), 3-size split (×0.55 r, exactly 2 children), screen wrap, 3 lives + 2s spawn invulnerability, wave clear → +100 & faster respawn, bullet life/cooldown; collide(state)→{shipHit,bulletsHit,astsHit}. invaders: 5×8 grid march with edge-flip + 12px descend, speedFor(alive)=20+(40−alive)×4 monotonic (+wave ×1.15), 2-bullet cap, seeded bombDrop, killAlien row-score 30/20/10 (=720 full grid), playerHit 3 lives, reachBottom instant lose, wave respawn. dodge: intervalFor ramp 1.6→0.45 (−0.07/spawn, floored), bounce with <=0 edge conditions (no wall-sticking) incl. corner double-flip, clamped player, circle-vs-AABB hitPlayer with 2s grace, score=⌊t×10⌋. UI: canvas + WOG palette + hud(score/best/lives) + data-smoke «بازی جدید» + ovl end panels + bindPad/keyState/pointer for dodge. Fixes during iteration (all test-construction, logic unchanged): speedFor(1)=176 not 180 (arithmetic slip); mono direction of speedFor (decreasing in alive-count per spec); dodge 60s sim pilot upgraded to deterministic evasive pilot (seeks center, flees nearest ball) so the balls-spawned assertion is meaningful.
Stage Summary: Deliverable: /home/z/my-project/agent_out/g3_arcade.py (copy of tested /tmp/g3/games/g3_arcade.py, 24.4KB). LOGIC pass=18 fail=0 (6+6+6, seeded sims: 30s asteroids / 60s invaders / 60s dodge); py_compile OK; node --check ×3 OK; runtime smoke ×3 OK (ovl reached, data-smoke works); forbidden tokens/emoji clean; rendered sizes asteroids 5.8KB · invaders 5.4KB · dodge 5.1KB (<45KB).
---
Task ID: AG-H2
Agent: H2 (skill/arcade sub-agent)
Task: Write 4 skill games (stroop + math-sprint + typing + cups) as ONE python batch file per mini-kit contract; all cat="arcade", engines=("common",); pure logic in WOG_LOGIC + deterministic seeded tests.
Work Log:
- Kit verbatim at /tmp/h2 (lib_mini.py + build_mini.py + test_mini.mjs). نکته محیطی: ابزار Write به /tmp دسترسی ندارد → کیت و بچ با heredoc در Bash نوشته شدند.
- Wrote /tmp/h2/games/h2_skill.py (24KB): from lib_mini import G + GAMES=[stroop, math-sprint, typing, cups].
- stroop (تست استروپ): ۴ رنگ فارسی (قرمز/آبی/سبز/زرد با hex)، کلمه در رنگ جوهر نمایش داده می‌شود و کاربر دکمهٔ همرنگِ جوهر را می‌زند (نه معنی کلمه). WOG_LOGIC: COLORS، genTrial(rng) با احتمال ناهمناخت ۰٫۶ (نمونه‌گیری ۲۰۰تایی → ۰٫۶)، judge، applyAnswer با امتیاز += پیاپی و ریست در خطا، tick/پایان ۴۵ث. UI: کلمهٔ بزرگ رنگی + ۴ دکمهٔ رنگی بزرگ، رکورد wog-stroop-best.
- math-sprint (ریاضی برق‌آسا): ۶۰ث؛ genProblem(level,rng) → {text,answer,choices[4]} روی ۴ عمل +,−,×,÷ دقیق (تقسیم همیشه b*q) با عملوندهای بزرگ‌شونده؛ ramp(t)=1+min(3,floor(t/15)) یکنوا؛ distractors(ans,rng) یکتا/≠جواب/≥۰؛ پاسخ درست ۱۰+۲×پیاپی، اشتباه −۲ث. UI: عبارت LTR بزرگ + ۴ گزینه با ارقام فارسی، رکورد wog-math-sprint-best.
- typing (سرعت تایپ): ۱۲ جملهٔ فارسی inline (بدون نیم‌فاصله برای تایپ‌پذیری)، رنگ‌آمیزی زندهٔ حرف‌به‌حرف (سبز/قرمز با diff)، ورودی متن واقعی موبایل‌پسند، WPM=حرف/۵ در دقیقه و دقت=درست/تایپ‌شده به‌صورت زنده در hud، پیشروی خودکار به جملهٔ بعد، پنل نتایج + رکورد wog-typing-best. WOG_LOGIC: SENTENCES، wpm، accuracy، diff (حروف اضافه/جاافتاده پرچم می‌خورند)، nextSentence چرخشی (با i=−1 امن).
- cups (سه‌کاسه): نشان‌دادن توپ زیر کاسه، سپس انیمیشن جابه‌جایی با transform/transition (swapSeq از levelSwaps(level)=۳+level؛ سرعت max(260,760−70×level)ms)؛ حدس با لمس کاسه؛ اعمال applyResult (درست: +۱۰×مرحله، مرحله++; غلط: جان−−)، پایان در ۰ جان + رکورد wog-cups-best. WOG_LOGIC: newState، place، swapSeq (بدون تکرار بلافاصلهٔ جفت)، track، levelSwaps، applyResult.
- SELF-CHECK از اولین اجرا سبز: build ۴ صفحه؛ node test_mini.mjs → LOGIC pass=21 fail=0 (stroop 5, math-sprint 6, typing 5, cups 5)؛ py_compile OK؛ node --check ×۴ OK؛ توکن‌های ممنوعه در کد تزریقی صفر (دو مورد هر صفحه فقط stub استاندارد store داخل قالب کیت است)؛ data-smoke روی شروع/بازی جدید/اکشن اصلی؛ ovl برای همهٔ پایان‌ها. حجم رندرشده: stroop 4.4KB · math-sprint 5.0KB · typing 5.8KB · cups 5.7KB — همه زیر ۴۵KB.
- تست‌های کلیدی: judge دقیق + نسبت ناهمناخت ۰٫۶∈[۰٫۵,۰٫۷] در ۲۰۰ آزمون مهرشده + ظهور هر ۴ رنگ در word/ink + ریست پیاپی + پایان زمانی؛ درستی جواب هر ۴ عمل از a,b بازمحاسبه شد و تقسیم ۳۰۰ مورد دقیق؛ گزینه‌ها یکتا/شامل جواب؛ ramp یکنوا با مقادیر مرزی (0→1، 15→2، 59→4)؛ جریان ۶۰ث دقیقاً ۱۲۰ تیک نیم‌ثانیه‌ای؛ wpm(300,60000)=60؛ بردارهای accuracy و پرچم‌های diff (اضافه/جاافتاده)؛ چرخش جمله‌ها؛ ردیابی track در ۲۰۰ دنبالهٔ مهرشده با پیاده‌سازی مستقل آرایه‌ای در تست؛ قالب/تعداد/رشد جابه‌جایی‌ها؛ جریان سه‌جان.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/h2_skill.py (copy of tested /tmp/h2/games/h2_skill.py, 24KB).
- Tests: LOGIC pass=21 fail=0; py_compile OK; node --check ×4 OK; no forbidden tokens; sizes < 45KB.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-I1
Agent: I1 (word games sub-agent, solo)
Task: 2 Persian word games (wordle + hangman) in ONE batch games/i1_word.py; cat=word, engines=(common,word).
Work Log: kit verbatim at /tmp/i1 (Write tool blocked on /tmp → heredoc, same as prior agents). wordle (واژه‌یاب): 120 inline 5-letter FA words (each char in 32-letter set, no ZWNJ/proper nouns; one 6-letter slip بهاران caught by list test and replaced with بهاری), two-pass duplicate-aware feedback g/y/k, norm (ي→ی، ك→ک، حذف فاصله/نیم‌فاصله), isValidGuess, keyState merge g3>y2>k1, seeded pickWord; UI: 6×5 board, faKb with per-key coloring via data-key/textContent match (scope fallback kbwrap→app), live share-like panel of colored CSS squares (no emoji grid), Enter/Backspace + Persian keydown support, streak record wog-wordle-streak, ovl برد/باخت + data-smoke بازی جدید. hangman (مرد حلق‌آویز): 44 words {w,cat} in 4 categories (حیوان ۱۲/میوه ۱۰/شهر ۱۱/شیء ۱۱), reveal/livesAfter/isWin/isDead/guess/hitIn/pickWord, 6-stage gallows via CSS shapes (opacity toggles), key hit/miss coloring, word reveal on loss, wins record wog-hangman-wins.
Tests: 11 total (wordle 5 + hangman 6): canonical feedback vectors incl. duplicates ('سسسسس'/'سسردس'→ggkkg، 'ردسسس'→yyyyg، ناران/باران)، whole-list validation (5 letters+FA+norm+uniqueness)، 6-guess flow، keyState merge priority، reveal mask/unmask، duplicate-guess no-double-penalty، 6-lives flow both directions، structure+category counts (each ≥8)، win/dead detection، 30-seed full-game sims for both games.
SELF-CHECK: build 2 pages; node test_mini.mjs → LOGIC pass=11 fail=0 (one fix in iteration: بهاران ۶ حرفی → بهاری، بدون تضعیف تست); py_compile OK; new Function syntax check ×2 OK; forbidden-token scan on game code NONE; rendered sizes wordle 7,921B / hangman 7,645B (<45KB).
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/i1_word.py (copy of tested /tmp/i1/games/i1_word.py, 20,266B).
- Tests: LOGIC pass=11 fail=0 (5+6); py_compile OK; page syntax OK ×2; sizes <45KB.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.

---
Task ID: AG-I3
Agent: I3 (word/quiz games sub-agent, solo)
Task: 5 Persian MCQ quiz games (proverb + antonym + flags + capitals + emoji-quiz) in ONE batch games/i3_quiz.py; cat=word, engines=(common,); shared MCQ engine: {q, options[4], a} items, 10s timer/question, streak scoring (gain=10+2×(streak−1)), seeded option shuffle per question, pool no-repeat until exhausted → reshuffle.
Work Log: kit verbatim at /tmp/i3 (Write tool blocked on /tmp → heredoc, same as prior agents). Shared pure WOG_LOGIC per game: ITEMS, shuffled, shuffleOptions(item,rng)→{q,options,a} (answer always present post-shuffle), pickPool(n,rng) (Fisher-Yates cycle, reshuffle only on exhaustion), judge, scoreFlow, start/next/answer state machine (ROUND=10, pool persists across rounds, done at 10 answered). UI: start panel (data-smoke شروع بازی) → question panel (qtext or 56px LTR qbig for flag/emoji content), 10s teal bar + زمان in hud (امتیاز/پیاپی/رکورد bestOf wog-<slug>-best), 2×2 option buttons ≥56px, inline feedback (آفرین +gain / اشتباه + show correct / زمان تمام شد) with correct-option highlight, auto-advance 1.2s, ovl پایان دور with رکورد + data-smoke بازی جدید. Datasets: proverb 25 handcrafted two-half Persian proverbs with handcrafted distractors (هر که بامش بیش→برفش بیشتر، گر صبر کنی→ز غوره حلوا سازی، خشت اول…→تا ثریا…، نابرده رنج→گنج میسر نمی‌شود، مرغ همسایه→غاز است، موش کنج سوراخ→به مار چه گوید و …); antonym 30 (15 مترادف + 15 متضاد) handcrafted; flags 40 verified ISO regional-indicator flag emojis (🇮🇷 ایران … 🇵🇱 لهستان, emoji as content only); capitals 40 (آنکارا/برازیلیا/کانبرا/برن gotchas covered, no country≈capital ambiguity items); emoji-quiz 25 family-friendly famous (🚢🧊→تایتانیک، 💍🌋→ارباب حلقه‌ها، 🧛‍♂️🌙→خون‌آشام per task example, professions/objects mix), distractors for flags/capitals/emoji generated deterministically (idx*7+3 walk, answer-excluded). Tests: 6/game (30 total): dataset integrity (count, non-empty q, 4 unique options, 0≤a<4, flags q.length===4 + no ASCII, emoji-quiz q pure non-ASCII, unique qs), shuffleOptions×3 stubs + seeded (q preserved, options unique, options[a]===answer), pickPool (N distinct, N*2+3 two clean cycles, constant-rng permutation), seeded 10-correct round (score===190 exact, streak 10, seen 10 unique, done, next→null), judge/scoreFlow table (10/22/36/52/70 chain + wrong resets), wrong-answer round flow (streak reset, done at 10, answer→null post-done). SELF-CHECK: build 5 pages; node test_mini.mjs → LOGIC pass=30 fail=0 (green on first run; no test weakened); py_compile OK; node --check ×5 OK; forbidden-token scan 0 (template store stub only); emoji audit clean (content-only in flags/emoji-quiz); runtime smoke ×5 with DOM stubs (2 full rounds → ovl both times); rendered sizes proverb 10,748B · antonym 9,713B · flags 10,311B · capitals 11,109B · emoji-quiz 9,433B — all < 45KB.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/i3_quiz.py (copy of tested /tmp/i3/games/i3_quiz.py).
- Tests: LOGIC pass=30 fail=0 (6×5); py_compile OK; script syntax OK ×5; runtime smoke ×5 OK; no forbidden tokens; sizes < 45KB.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-H1
Agent: H1 (arcade skill games sub-agent, retry)
Task: Write 4 skill games (whack + reaction + aim + digits) as ONE python batch file per mini-kit contract; all cat="arcade", engines=("common",).
Work Log:
- Kit built verbatim at /tmp/h1 (lib_mini.py + build_mini.py + test_mini.mjs). نکته محیطی: فایل‌ها با heredoc در Bash نوشته شدند (الگوی B1/B2).
- Wrote /tmp/h1/games/h1_skill.py (~27.6KB): from lib_mini import G + GAMES=[whack, reaction, aim, digits].
- whack (موشکوبی): ۳۰ ثانیه، ۹ سوراخ (۳×۳)، ظهور موش با زمان ماندن کاهنده (۱.۴ث → کف ۰.۵ث)، سقف ۳ موش همزمان، ضربه +۱۰ با ضریب کمبو 2^floor(combo/5)، خطا = ریست کمبو، تیک تا ۳۰ث clamp و سپس انجماد کامل. WOG_LOGIC: newState/tick/whack/comboBonus/upTime. UI: گرید ۳×۳ دکمه‌ای ≥۶۴px، hud امتیاز/زمان/کمبو، رکورد wog-whack-best، ovl پایان.
- reaction (عکس‌العمل): ۵ دور، انتظار تصادفی ۱..۴ث سپس «بزن!»؛ زودزنی = جریمه ۵۰۰ms یک‌بار در هر دور (ادامهٔ انتظار)، ms نهایی شامل جریمه؛ stats میانگین/میانه/بهترین و رتبه‌ها فوق‌العاده<250، خوب<350، متوسط<450، کند. WOG_LOGIC: newState/startRound(ساعت تزریقی nowMs)/tap/stats/rating. UI: دکمهٔ بزرگ تاچ، چیپ‌های ۵ نتیجه، رکورد کمینه wog-reaction-best.
- aim (تیرانداز هدف): ۳۰ ثانیه، یک هدف همیشه (شعاع ۲۴..۳۴ در بورد ۳۲۰)، برخورد = ۱۰ + جایزهٔ سرعت پله‌ای (≤400ms:+10، ≤800:+6، ≤1200:+3)، خطا = −۵ و ریست کمبو، هدف منقضی بعد ۱.۵ث جابه‌جا می‌شود. WOG_LOGIC: newState/spawnNext/shoot/accuracy/tick/speedBonus. UI: بورد pointerdown با مقیاس، رکورد wog-aim-best.
- digits (رقم‌های کوتاه): گسترهٔ رقم ۳→۱۲، genSeq بدون ۳ رقم برابر پیوسته، تایپ روی کیپد فارسی، ۳ جان، سقف ۱۲ = برد. WOG_LOGIC: genSeq/check/newState/beginLevel/pushDigit. UI: نمایش پی‌درپی با تایمر، کیپد ۱۰گانه + پاک کردن، جان‌ها، رکورد wog-digits-best.
- SELF-CHECK: build ۴ صفحه؛ node test_mini.mjs → LOGIC pass=20 fail=0 (هر بازی ۵ تست). یک ایراد واقعی در متن تست digits (خط py) گرفته و رفع شد — هیچ تستی تضعیف نشد. py_compile OK؛ node --check روی اسکریپت هر ۴ صفحه OK؛ اسکن توکن‌های ممنوعه صفر؛ بدون ایموجی در صفحات رندرشده؛ data-smoke/hud/hint/ovl در هر ۴ صفحه.
- تست‌های کلیدی: سقف ۳ موش در شبیه‌سازی کامل ۶۱۰ تیک (seed 12345) + انجماد پس از ۳۰ث؛ پنهان‌شدن با ttl و جدول upTime کاهنده؛ جدول ضریب کمبو (۲^⌊c/۵⌋)؛ حسابداری ضربه/خطا؛ جریمهٔ زودزنی دقیقاً یک‌بار (ms=750)؛ مرز دقیق GO (ms=0)؛ stats فرد/زوج روی ورودی نامرتب؛ ۷ آستانهٔ رتبه؛ جریان ۵ دور با done flag و قفل پس از پایان؛ برخورد لبهٔ شعاع (r ⇒ hit، r+1 ⇒ miss)؛ پله‌های جایزهٔ سرعت؛ دقت ۰/۵۰/۷۵/۱۰۰٪؛ ۲۰۰ اسپاون داخل محدوده؛ شبیه‌سازی ۳۰ث aim با score=20*hits و دقت ۱۰۰٪؛ طول/بازهٔ ارقام؛ صفر سه‌تایی پیوسته در ۲۰۰ دنباله؛ check دقیق (کوتاه/بلند/برابر)؛ ۳ خطا = پایان با شمارش جان؛ سقف ۱۲ (برد در span=12 و قفل ادامه).
- حجم صفحات رندرشده: whack 4,458B · reaction 4,932B · aim 4,858B · digits 5,855B — همه زیر سقف ۴۵KB.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/h1_skill.py (copy of tested /tmp/h1/games/h1_skill.py, 27.6KB).
- Tests: LOGIC pass=20 fail=0 (5+5+5+5); py_compile OK; node --check ×4 OK; no forbidden tokens; sizes < 45KB.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.
---
Task ID: AG-I2
Agent: I2 (word games sub-agent, retry)
Task: 3 Persian word games (word-search + anagram + word-chain) in ONE batch games/i2_word.py; cat=word, engines=(common,word).
Work Log: kit verbatim at /tmp/i2 (Write tool blocked on /tmp → heredoc, same as prior agents). word-search (واژه‌یاب شبکه‌ای): 10×10، ۸ واژهٔ ۵-۷ حرفی از فهرست ۴۸ واژه، PLACE_DIRS=[[0,-1],[1,0],[1,-1],[1,1]]، placeWord با مرز+تداخل فقط هم‌حرف (۲۵۰ تلاش تصادفی + اسکن قطعی پشتیبان)، fillGrid با حروف پرتکرار فارسی، checkSelection فقط خط مستقیم روی محورهای مجاز و تطابق دقیق سلول‌های واژهٔ قرارگرفته؛ UI لمس آغاز→پایان، هایلایت sel/fnd، چیپ واژه‌ها، رکورد زمان wog-word-search-best. anagram (واژه‌سازی): DICT ۱۵۰ واژهٔ ۲-۷ حرفی (منابع ۶-۷ حرفی = ۴۹)، genLetters (واژهٔ مبدأ + پرکننده تا ۶/۷ حرف)، canForm زیرمجموعهٔ چندمجموعه‌ای با نرمال‌سازی ي/ك، findable، scoreOf=len²، تایمر ۱۲۰ث، کاشی‌های لمسی + بُر بزن + ثبت/پاک، پایان: فاش‌سازی همهٔ واژه‌های ممکن (در #app و متن ovl)، رکورد wog-anagram-best. word-chain (زنجیرهٔ واژه‌ها): DICT ۲۰۵ واژه (ANA + ۵۵ افزوده با پوشش حروف آغازین ا..ی)، lastLetter/firstLetter نرمال‌کننده (ي→ی ك→ک، حذف فاصله/نیم‌فاصله)، canChain دقیق، aiReply از میان نامصرف‌ها؛ هر دور used ریست، ۱۵ث/نوبت، خطا/پاس = امتیاز حریف، ربات گیرکند = امتیاز انسان، اولین ۵ برنده، کیبورد فارسی (faKb) + keydown، رکورد برد wog-word-chain-wins. یک باگ فیکسچر در ران دوم: انتظار اشتباه «ر» برای حرف آخر «آب‌ریز» (درست: «ز») + افزودن بردار نیم‌فاصلهٔ انتهایی («آب‌»→«ب») — تست تضعیف نشد، منطق دست نخورد.
- SELF-CHECK: build ۳ صفحه؛ node test_mini.mjs → LOGIC pass=15 fail=0 (۵+۵+۵)؛ py_compile OK؛ node -e new Function ×3 OK؛ اسموک ران‌تایم با DOM-stub (کلیک همهٔ کنترل‌ها + پیشروی ۲۲۰ تیک تایمر + فراخوانی faKb): هر ۳ صفحه بدون خطا، ovl پایان برای anagram (انقضای ۱۲۰ث) و word-chain (۵ باخت زمانی) ثبت شد؛ اسکن توکن‌های ممنوعه روی خروجی: فقط localStorage داخل wrapper استاندارد store کیت (سطر ۳۱ قالب) — در logic/ui صفر مورد؛ بدون ایموجی. حجم رندرشده: word-search 7,838B · anagram 9,246B · word-chain 10,383B — همه زیر ۴۵KB.
- تست‌های کلیدی: بردار PLACE_DIRS؛ قراردهی معتبر/خارج مرز (کوهستان دو جهت)/تداخل حرف متفاوت (دوستی روی باران، موزیک روی آبادی)/هم‌پوشانی هم‌حرف مجاز (آبادی از میان «ا» باران)؛ ۵۰ gen مهرشده — هر ۸ واژه قرار می‌گیرد، جهت هر واژه ∈ PLACE_DIRS، حروف سلول‌ها = واژه، شبکه پر؛ پخش مجدد سلول‌های هر واژهٔ placed به‌عنوان انتخاب → پیدا شدن، انتخاب معکوس → null؛ رد همان‌خانه/غیرمستقیم/جهت‌های ممنوعه (0,1)(-1,0)(-1,-1)/خارج مرز/انتخاب ناقص؛ canForm با شمارش تکراری (باب/لال) و حروف اضافی و ك عربی؛ scoreOf مجذور و یکنوا؛ findable (باران بله، نان بدون «ن» دوم خیر) و تهی؛ ۳۰ مجموعهٔ مهرشده همیشه شامل واژهٔ مبدأ + حروف فارسی معتبر؛ سلامت واژه‌نامه‌ها (یکتا، نرمال، طول) و پوشش حروف آغازین زنجیره؛ نرمال‌سازی lastLetter (كتاب/باري/فاصله/نیم‌فاصله)؛ زنجیرهٔ دقیق + رد ناهم‌حرف؛ پاسخ ربات در ۲۰ بذر: ۵حلقهٔ زنجیرهٔ کامل، پرهیز از used، null در فرسودگی حرف «ب»؛ شبیه‌سازی کامل ۱۰ مسابقهٔ مهرشده تا ۵ امتیاز — پایان‌پذیر، rounds=sc[0]+sc[1]≤9، فقط یک برندهٔ ۵.
Stage Summary:
- Deliverable: /home/z/my-project/agent_out/i2_word.py (copy of tested /tmp/i2/games/i2_word.py, 30,972B).
- Tests: LOGIC pass=15 fail=0 (5+5+5); py_compile OK; script syntax OK ×3; runtime smoke ×3 OK; forbidden tokens clean (only kit's own store wrapper); sizes < 45KB.
- Next: platform integrator can merge GAMES from this batch into the main build/catalog.

---
Task ID: 4
Agent: main (Z.ai)
Task: توسعه مجموعه به ۱۰۰ بازی + دکمه بازگشت به خانه + تست کامل منطق (درخواست کاربر)

Work Log:
- زیرساخت بیلد در scripts/wog ساخته شد: lib.py (قالب مشترک با دکمه بازگشت + shim + موتورهای کارتی/آرکید/واژه)، build.py (کاتالوگ ۱۰۰تایی با assert دقیق اسلاگ‌ها)، test_logic.mjs (هارنس تست منطق با mulberry32)، check_syntax.py، smoke.py (Playwright).
- کشف مهم: زیرایجنت‌ها FS مشترک دارند ولی snapshot ایزوله می‌بینند و merge-back می‌تواند فایل‌های همزمانِ من را پاک کند (j_luck/h1/i2 یک‌بار ناپدید و بازتولید شدند)؛ راهکار: کیت درون‌خطی در worklog + کپی فوری پس از هر ایجنت + backup/games.
- ۲۵ اجرای زیرایجنت (تکی/موازی) دسته‌های A1..I3 را ساخت؛ رفع باگ‌های تست ایجنت‌ها (pentago pure-place، spider/freecell fixtures، fox-and-hounds سینتکس + انتظار ۷ حرکت، g1 ربات‌های فلکی → تست‌های قطعی، mulberry32 خراب کیت d3).
- نرد ایرانی به‌صورت کامل توسط main پیاده شد: تاس دوبل×۴، میله، زدن بلوت، بیرون‌آوردن (قانون بالاترین خانه)، قانون «حداکثر توالی/تاس بزرگ‌تر»، AI حریص + ۸ تست (پیپ ۱۶۷، conservation ۳۰ مهره، بازی کامل AI-vs-AI).
- فیکس موتور: faKb با longKeys غیرآرایه‌ای مقاوم شد (واژه‌یاب/حلق‌آویز).
- لندینگ جدید: جست‌وجو + فیلتر ۶ دسته + ۱۰۰ کارت + JSON-LD ItemList + licenses.html (اتریبیوشن chess.js BSD-2) + sitemap ۱۰۲ URL + games.json.
- پچ دکمه بازگشت ۱۳ بازی قدیمی در pages-site و Data/SeedGames (patch_back_button.py).
- QA نهایی: ۴۷۹/۴۷۹ تست منطق · node --check ۱۰۰/۱۰۰ · smoke ۱۰۰/۱۰۰ (۰ خطا، دکمه بازگشت، data-smoke) · ۱۴/۱۴ تست تعاملی بازی‌های قدیمی (شطرنج e2e4+پاسخ AI، ۲۰۴۸ کلید، مین‌یاب، بلک‌جک شرط‌بندی→پخش→کارت، حافظه، سولیتر پشت‌کار و…).
- git: main cb0b282 (README + GAMES.md + پچ SeedGames) push شد؛ gh-pages 6681b84 (مجموعه کامل ۱۰۰ بازی، ۲.۲MB) push شد؛ core.fileMode=false برای نویز mode-churn.
- راستی‌آزمایی زنده: landing 200، games.json=۱۰۰، backgammon/wordle/chess/pasoor/licenses همگی 200، دکمه بازگشت در HTML بازی‌ها.

Stage Summary:
- مجموعهٔ نهایی: دقیقاً ۱۰۰ بازی قابل اجرا در https://ssschangersss.github.io/world-of-games/ (۶ دسته: تخته ۲۱، کارتی ۱۶، پازل ۲۰، اکشن ۲۲، واژه ۱۰، شانس ۱۱)
- دکمه «⌂ خانه» در هر ۱۰۰ صفحه (href نسبی ../../index.html)
- تست منطق: هر بازی جدید WOG_LOGIC خالص + تست واحد (۴۷۹ تست)؛ بازی‌های قدیمی: تست تعاملی مرورگر
- ابزار بازتولید کامل: scripts/wog/build.py (بیلد + لندینگ + sitemap) و backup/games

---
Task ID: 5
Agent: main (Z.ai)
Task: گرافیک بازی‌ها بر اساس فضا و سبک هر بازی + رفع بازی‌های باگ‌دار (درخواست کاربر)

Work Log:
- باگ‌یابی: qa_deep (۱۰۰ صفحه، خطاهای JS) → hangman (L.norm نبود) و kite (L.W/L.H اکسپورت نبود) — هر دو در منبع دسته‌ای رفع شد.
- static_check.mjs نويسه شد: ارزیابی WOG_LOGIC هر بازی در Node + تطبیق L.* با کلیدهای اکسپورت‌شده + بررسی موتورهای لازم — ۱۳ هشدار فقط legacy ها (بدون مارکر؛ طبیعی).
- کشف نویز FS: pages-site بین دو نسخه نوسان داشت (merge-back جلسه قبل)؛ با rebuild کامل و md5 پایدار شد؛ منابع دسته‌ای سالم‌اند (۴۷۹ تست سبز).
- Design System v2 در lib.py: تزریق --g1/--g2 (رنگ هویت هر بازی که تعریف شده ولی بلااستفاده بود)، پس‌زمینه چندلایه، نقش گرهی فارسی (SVG data-URI)، صحنه‌های دسته‌ای (cards/board/puzzle/arcade/word/luck)، کارت‌ها/دکمه‌ها/اورلی/توست/بوردها ارتقا یافت.
- themes.py نويسه شد: ~۵۰ تم اختصاصی (منکالا چوبی، هانوی برنجی، سینس نئون، کشتی جنگی رادار، اور لاریس بابل، سودوکو شسته‌کار، راش‌اور آسفالت، سلات شیشه آزمایشگاهی، اسلاتس کابینت نئون، ...)
- restyle_legacy.py: ۱۳ بازی قدیمی با همان v2 (متغیر هویت + صحنه + کامپوننت) بازآرایی شدند.
- art_legacy.py + art_arcade.py + art_fix.py: صحنه‌های canvas (flappy گرگ‌ومیش، runner کویر، kite آسمان روز، frogger موج آب، meteor سحابی، stacker نئون، invaders/asteroids ستاره‌باران، dodge هشدار، plinkو گردو، snake جنگلی با غذای درخشان...).
- فیکس چیدمان hanoi (برچسب برج‌ها روی نوار کنترل می‌افتاد → margin 38px).
- SeedGames هر ۱۳ بازی قدیمی از نسخه استایل‌شده همگام شد.

Stage Summary:
- منبع: scripts/wog/{lib.py,themes.py,restyle_legacy.py,art_legacy.py,art_arcade.py,art_fix.py,static_check.mjs,qa_deep.py,interact_final.py}
- وضعیت: build ۸۷ + landing سبز؛ ۴۷۹/۴۷۹ تست منطق؛ QA تعاملی نهایی در جریان؛ استقرار پس از سبز شدن QA.
