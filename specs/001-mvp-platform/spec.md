# Feature Spec: 001-mvp-platform — اسکلت کامل پلتفرم World of Games

Status: **Approved** (مبتنی بر تصمیم‌های تصویب‌شده D-01…D-14 — see worklog/clarification)
Parent Requirement: PR-1 «پلتفرم ایرانی بازی‌های تحت وب با Razor View، پنل ادمین قابل کنترل با MCP، آپلود بازی با تأیید ادمین، وبلاگ سئومحور، درآمد فقط از دونیت، تم ایران باستان»
Owner: SSSchangerSSS (مالک انسانی)

## Problem / Goal
بازی‌سازهای ایرانی به محیطی نیازمندند که بازی‌های HTML5 آن‌ها را با استاندارد مشخص میزبانی و اجرا کند؛ مخاطبان به کاتالوگی سالم و سریع نیازمندند؛ و مالک باید بتواند بدون زیرساخت تبلیغاتی، فقط با دونیت پایدار بماند. این فیچر اسکلت کامل و قابل اجرای این پلتفرم را تحویل می‌دهد تا چرخه‌های بعدی روی آن عمق اضافه کنند.

## In Scope / Out of Scope
- **In:** هوم‌پیج تم ایران‌باستان (RTL فارسی)، احراز هویت Identity با نقش Admin، کاتالوگ بازی + صفحه اجرا (iframe sandbox)، جریان «درخواست آپلود بازی» با اعتبارسنجی ZIP و صف تأیید، وبلاگ با سئو (متا، sitemap.xml، robots.txt، RSS، JSON-LD، پست مرتبط)، جریان کامل دونیت (لایه انتزاعی + زرین‌پال + Mock)، پنل ادمین (داشبورد، تأیید/رد بازی، مدیریت وبلاگ، لیست دونیت‌ها، کاربران، Audit)، سرور MCP برای مدیریت بازی‌ها، Seed داده نمایشی، تست‌های واحد، CI، آرتیفکت‌های IIS.
- **Out (صریح):** پرداخت واقعی بدون مرچنت مالک، ویرایشگر آنلاین بازی، سیستم امتیاز/لایک/کامنت، پنل کاربری پیشرفته، Multi-factor، CDN، Docker (تصمیم D-09 = IIS)، Localisation انگلیسی، Migration-based schema (→ D-13).

## User Stories & Requirements

### REQ-001 — هویت بصری ایران‌باستان و RTL
سایت باید تماماً فارسی و RTL باشد؛ تم «ایران باستان» با پالت لاجوردی-زرینی، نقوش SVG سبک (رزت لوتوس/کتیبه‌مانند) و فونت وزیرمتن (self-hosted) باید در همه صفحات اعمال شود.
- AC-001-1: `<html lang="fa" dir="rtl">` در Layout — Verification: بازرسی HTML تولیدی (smoke)
- AC-001-2: فونت‌ها self-hosted و بدون هیچ درخواست خارجی (بدون Google Fonts/CDN) — Verification: grep در خروجی CSS/HTML
- AC-001-3: مجموعه دارایی‌های استاتیک قابل بارگذاری در صفحه اصلی < 300KB (بدون تصاویر کاربران) — Verification: اندازه‌گیری فایل‌های wwwroot

### REQ-002 — احراز هویت و نقش‌ها
ASP.NET Core Identity با نقش‌های `Admin` و `User`؛ ثبت‌نام/ورود/خروج فارسی.
- AC-002-1: ثبت‌نام با ایمیل+رمز (حداقل ۸ کاراکتر) موفق و لاگین می‌شود — Verification: TEST-AUTH + smoke
- AC-002-2: صفحات ادمین بدون نقش Admin → 403 (AccessDenied) — Verification: TEST-AUTH
- AC-002-3: Seed ادمین اولیه فقط در صورت خالی‌بودن DB و از کانفیگ — Verification: اجرای اولیه + TEST-SEED

### REQ-003 — کاتالوگ و اجرای بازی
بازی‌های Approved و Enabled در کاتالوگ عمومی (جست‌وجو بر اساس عنوان، مرتب‌سازی جدیدترین/محبوب‌ترین) دیده می‌شوند؛ صفحه اجرا بازی را در iframe با sandbox اجرا می‌کند.
- AC-003-1: iframe فقط `sandbox="allow-scripts allow-pointer-lock allow-popups allow-modals allow-forms"` دارد (بدون allow-same-origin) — Verification: بازرسی HTML + تست
- AC-003-2: بازی غیرفعال/ردشده با URL مستقیم → 404 — Verification: TEST-GAME
- AC-003-3: PlayCount پس از بازدید صفحه اجرا افزایش یابد — Verification: TEST-GAME

### REQ-004 — درخواست آپلود بازی (استاندارد مشخص)
کاربر لاگین‌شده با ارسال ZIP + متادیتا «درخواست» می‌دهد؛ تا تأیید ادمین منتشر نمی‌شود. استاندارد بسته (docs/game-upload-standard.md) باید ماشینی اعتبارسنجی شود: ZIP شامل `index.html` در ریشه، پسوند مجاز، بدون path traversal، سقف حجم فشرده/نافشرده، سقف تعداد فایل.
- AC-004-1: ZIP معیار → درخواست با Status=Pending ذخیره و فایل‌ها به `wwwroot/media/games/{slug}/` استخراج می‌شود — Verification: TEST-VALIDATOR + TEST-GAME
- AC-004-2: هر تخلف (بدون index.html، پسوند ممنوع، `../`، سقف حجم) → رد با پیام فارسی مشخص، بدون نوشتن فایل — Verification: TEST-VALIDATOR
- AC-004-3: کاور JPG/PNG/WebP ≤ 2MB و الزامی — Verification: TEST-VALIDATOR
- AC-004-4: پس از تأیید ادمین، بازی در کاتالوگ ظاهر می‌شود — Verification: TEST-GAME + smoke ادمین

### REQ-005 — وبلاگ سئومحور
ادمین پست (Markdown) می‌سازد/ویرایش می‌کند/منتشر می‌کند؛ صفحات عمومی دارای متای سئو، پست‌های مرتبط (تگ مشترک)، sitemap.xml، robots.txt، RSS و JSON-LD Article هستند.
- AC-005-1: صفحه پست شامل `<title>`، `meta description`، canonical، OG و JSON-LD Article معتبر ساختاری — Verification: بازرسی smoke + TEST-BLOG
- AC-005-2: `/sitemap.xml` شامل صفحه اصلی، بازی‌های فعال و پست‌های منتشرشده — Verification: smoke + TEST-BLOG
- AC-005-3: `/blog/feed.xml` RSS معتبر — Verification: smoke
- AC-005-4: «پست‌های مرتبط» فقط با تگ مشترک و بدون خود پست — Verification: TEST-BLOG
- AC-005-5: پیش‌نویس با URL مستقیم → 404 — Verification: TEST-BLOG

### REQ-006 — دونیت (تنها منبع درآمد)
صفحه دونیت با مبالغ پیشنهادی + دلخواه (ریال)، نام/پیام اختیاری و گزینه ناشناس؛ جریان: ایجاد Pending → دروازه → callback → Verify → Paid/Failed. هیچ تبلیغ یا فروش دیگری نباید وجود داشته باشد.
- AC-006-1: لایه انتزاعی `IDonationGateway`؛ Mock و Zarinpal هر دو پیاده‌سازی دارند؛ انتخاب با کانفیگ — Verification: TEST-DONATION
- AC-006-2: callback با مبلغ/Authority نامعتبر → Failed و هیچ Paid ثبت نمی‌شود — Verification: TEST-DONATION
- AC-006-3: دونیت‌های Paid در صفحه «حامیان» فقط با نام/ناشناس مطابق ورودی نمایش داده می‌شوند (بدون مبلغ فردی) — Verification: TEST-DONATION
- AC-006-4: زرین‌پال: request/verify مطابق API v4 و آدرس‌ها قابل کانفیگ — Verification: TEST-DONATION (با تست http داخلی/تنظیمات) + بازبینی

### REQ-007 — پنل ادمین
داشبورد (شمارنده‌ها + جمع دونیت Paid)، صف تأیید بازی‌ها (تأیید/رد با دلیل اجباری/فعال-غیرفعال)، CRUD وبلاگ، لیست دونیت‌ها، لیست کاربران، Audit Log.
- AC-007-1: رد بازی بدون دلیل ممکن نیست — Verification: TEST-GAME
- AC-007-2: هر اقدام مدیریتی ردیف Audit (Actor، Source=Web/Mcp، Action، EntityType، EntityId، Detail) ثبت کند — Verification: TEST-AUDIT
- AC-007-3: حذف پست، soft نیست؛ حذف قطعی با تأیید فرم است — Verification: smoke

### REQ-008 — سرور MCP برای مدیریت بازی‌ها (D-08)
Endpoint `POST /mcp` (Streamable HTTP، JSON-RPC 2.0) با Bearer Token اختصاصی از کانفیگ؛ ابزارها: `list_pending_games`، `get_game_status`، `approve_game`، `reject_game`، `set_game_enabled`. پاس‌ها JSON (بدون SSE در فاز ۱).
- AC-008-1: درخواست بدون/با توکن غلط → 401 — Verification: TEST-MCP
- AC-008-2: `initialize` handshake استاندارد پاسخ دهد (protocolVersion، capabilities.tools، serverInfo) — Verification: TEST-MCP
- AC-008-3: `tools/list` دقیقاً ۵ ابزار فوق را با inputSchema معتبر معرفی کند — Verification: TEST-MCP
- AC-008-4: `tools/call → reject_game` بدون reason خطای اعتبارسنجی بدهد و وضعیت تغییر نکند — Verification: TEST-MCP
- AC-008-5: هر فراخوانی موفق، Audit با Source=Mcp بنویسد — Verification: TEST-MCP

### REQ-009 — NFR: عملکرد و موبایل (مطابق ماده ۱۵)
سایت باید روی موبایل کاملاً usable باشد (چیدمان موبایل-اول، اهداف لمسی ≥44px، بدون اسکرول افقی) و سبک باشد.
- AC-009-1: هیچ صفحه‌ای overflow-x داشته باشد (بدون المان عریض‌تر از viewport) — Verification: smoke بازرسی + CSS audit
- AC-009-2: CSS+JS سایت (بدون بازی‌ها) جمعاً < 60KB و بدون هیچ کتابخانه فرانت سنگین (بدون jQuery/React) — Verification: اندازه‌گیری فایل
- AC-009-3: فرم‌ها و جدول‌های ادمین روی عرض 360px بدون سرریز کار کنند (responsive tables) — Verification: بازرسی CSS + smoke
- AC-009-4: هدرهای کش استاتیک (Cache-Control) برای wwwroot در IIS/kestrel تنظیم شود — Verification: بازرسی web.config + Program.cs

### REQ-010 — CI و دیپلوی IIS
GitHub Actions روی windows-latest: restore/build/test. آرتیفکت IIS: web.config + PublishProfile + docs/deploy-iis.md.
- AC-010-1: CI سبز شود (build+test بدون error) — Verification: اجرای Actions پس از push
- AC-010-2: `dotnet publish -c Release` بدون هشدار خطای مرگبار و خروجی قابل کپی به IIS — Verification: build محلی (evidence در worklog)

## Decisions Referenced
D-01…D-14 (worklog Task 1). اجرای MCP دست‌ساز = D-11 (برگشت‌پذیر). EnsureCreated = D-13 (Known Issue زیر).

## Known Issues / Accepted Limitations (پذیرش مالک)
- KI-1: اسکیمای فاز ۱ با `EnsureCreated` ساخته می‌شود؛ برای تحول Schema در آینده باید Migration فعال شود (D-13).
- KI-2: sandbox بدون allow-same-origin یعنی `localStorage` داخل بازی در دسترس نیست؛ بازی‌ها باید مقاوم باشند (در استاندارد مستند شد؛ shim در استاندارد توصیه می‌شود).
- KI-3: زرین‌پال واقعی بدون MerchantId مالک قابل تست پایان‌به‌پوت نیست؛ تا آن زمان Mock مرجع Verification است (D-07).
- KI-4: ضدویروس/اسکن محتوای ZIP در فاز ۱ وجود ندارد؛ whitelist پسوندها + سقف‌ها جایگزین موقت‌اند (پیشنهاد فاز ۲: ClamAV).
- KI-5: «مدارم پست‌های مرتبط» به‌صورت «پست‌های مرتبط بر اساس تگ + پیوست تصویر/فایل در پست» تفسیر شد (D-12 فرض ثبت‌شده).
