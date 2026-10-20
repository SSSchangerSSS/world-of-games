<div dir="rtl" align="right">

# ⚔️ World of Games

**پلتفرم ایرانی بازی‌های تحت وب** — بازی کن، بساز، حمایت کن.

> 🌐 **پیش‌نمایش زنده (GitHub Pages):** [https://ssschangersss.github.io/world-of-games/](https://ssschangersss.github.io/world-of-games/)
> صفحه معرفی استاتیک + دو بازی دمو («حافظه هخامنشی» و «پرش از البرز») که مستقیم و قابل بازی اجرا می‌شوند.
> منبع این صفحه شاخه [`gh-pages`](https://github.com/SSSchangerSSS/world-of-games/tree/gh-pages) است؛ اپلیکیشن کامل (کاتالوگ، آپلود، وبلاگ، دونیت، ادمین) سرور .NET می‌خواهد — راهنمای استقرار: [docs/deploy-iis.md](docs/deploy-iis.md).

بازی‌های HTML5 ساخته بازی‌سازهای ایرانی، مستقیم در مرورگر؛ بدون نصب، بدون تبلیغات مزاحم. تم سایت الهام از **ایران باستان** (لاجورد شب، زرین هخامنشی، فیروزه)، تماماً **فارسی و RTL** و موبایل‌اول.

</div>

## ✨ قابلیت‌ها (MVP — spec 001)

- 🎮 **کاتالوگ بازی**: جست‌وجو، مرتب‌سازی (جدیدترین/محبوب‌ترین)، صفحه اجرا با `iframe` امن (`sandbox`)
- 📤 **درخواست آپلود بازی**: اعتبارسنجی ماشینی ZIP (استاندارد → [docs/game-upload-standard.md](docs/game-upload-standard.md)) + صف تأیید ادمین
- 📝 **وبلاگ سئومحور**: Markdown (امن‌سازی‌شده)، متا/canonical/OG، JSON-LD، `sitemap.xml`، `robots.txt`، RSS، پست‌های مرتبط (تگ مشترک)
- 💝 **دونیت**: تنها منبع درآمد — لایه انتزاعی + **زرین‌پال v4** + Mock توسعه؛ فهرست حامیان بدون مبلغ فردی
- 🛡️ **پنل ادمین**: داشبورد، تأیید/رد بازی (دلیل اجباری)، CRUD وبلاگ، دونیت‌ها، کاربران، Audit Log
- 🤖 **سرور MCP**: کنترل ادمین با Agent — ۵ ابزار مدیریت بازی ([docs/mcp.md](docs/mcp.md))
- 🔐 **Identity** با نقش‌های Admin/User، ثبت‌نام/ورود فارسی

## 🧱 تکنولوژی

| لایه | انتخاب |
|---|---|
| فریم‌ورک | **ASP.NET Core MVC (Razor Views)** روی **.NET 10 LTS** |
| دیتابیس | EF Core 10 — **SQLite** (توسعه) / **SQL Server** (پروداکشن) با سوئیچ کانفیگ |
| فرانت | CSS دست‌ساز (دیزاین‌سیستم لاجورد/زرین)، فونت **وزیرمتن** self-hosted، JS ~2KB بدون وابستگی |
| تست | xUnit (۳۵ تست: validator، سرویس‌ها، MCP، دونیت، وبلاگ) |
| دیپلوی | **Windows + IIS** ([docs/deploy-iis.md](docs/deploy-iis.md)) |

دارایی‌های ثابت صفحه اصلی: **< ۳۰۰KB** · CSS+JS: **~۲۱KB** — بدون هیچ CDN خارجی.

## 🚀 اجرا (توسعه)

```bash
git clone https://github.com/SSSchangerSSS/world-of-games.git
cd world-of-games
dotnet run --project src/WorldOfGames.Web
# → http://localhost:5000  (اگر پورت متفاوت بود، در خروجی کنسول ببینید)
```

ادمین پیش‌فرض (توسعه — از `appsettings.json`، حتماً در پروداکشن عوض کنید):

```text
admin@worldofgames.ir / Admin#1404
```

دو بازی دمو («حافظه هخامنشی»، «پرش از البرز») و سه پست وبلاگ در اولین اجرا seed می‌شوند.

## 🎮 مجموعه بازی‌های دمو (۱۳ بازی)

| دسته | بازی‌ها |
|---|---|
| تخته‌ای | شطرنج (موتور chess.js + AI) · اوتِلو (ریورسی) · دوز (AI شکست‌ناپذیر) |
| کارتی | پاسور کلایک (با برگردان و خودکار) · بلک‌جک ۲۱ (سکه‌های مجازی) |
| پازل | سودوکو (تولید راه‌حل‌یکتا، ۳ سطح) · ۲۰۴۸ |
| معمایی | مین‌یاب (اولین کلیک امن، ۲ سطح) · حافظه هخامنشی |
| اکشن/کازوال | توپ‌شکن · پرش از البرز · مارِ گرسنه · پینگ‌پنگ |

همه بازی‌ها سلف‌کانتینند، فارسی/RTL، سازگار با لمس و اجرای امن در iframe سندباکس‌شده. پیش‌نمایش زندهٔ همه: [GitHub Pages](https://ssschangersss.github.io/world-of-games/).

**مجوزهای شخص ثالث:** موتور قوانین شطرنج `chess.js` نسخه ۰.۱۰.۳ تحت **BSD-2-Clause** (فایل `LICENSE-chessjs.txt` در پوشهٔ بازی). بقیه بازی‌ها دست‌ساز همین پروژه‌اند؛ مکانیک ۲۰۴۸ الهام‌گرفته از اثر گابریله چیرولی (MIT) است.

## 🤖 کنترل ادمین با MCP

```bash
curl -X POST https://your-host/mcp \
  -H "Authorization: Bearer YOUR_MCP_TOKEN" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

ابزارها: `list_pending_games` · `get_game_status` · `approve_game` · `reject_game` · `set_game_enabled`
راهنمای کامل + تنظیم کلاینت: [docs/mcp.md](docs/mcp.md)

## 📐 روش توسعه — Spec-Driven

این پروژه با **قانون اساسی Spec-Driven** (`.specify/memory/constitution.md`) و ساختار spec-kit پیش می‌رود:

```text
specs/001-mvp-platform/
├── spec.md      ← نیازمندی‌ها REQ-001..010 + Acceptance Criteria
├── plan.md      ← معماری و قراردادهای مشترک
├── tasks.md     ← تجزیه Atomic Task + ماتریس Traceability (REQ→TASK→TEST)
├── data-model.md
└── checklist.md ← Coverage & Consistency Check
```

فیچر جدید: `.specify/scripts/bash/create-new-feature.sh "عنوان"` — چرخه: Clarify → Spec → Plan → Tasks → Coverage → Implement → Verify → Done (ماده ۱۸: بدون Evidence واقعی، Done نیست).

## 📤 ارسال بازی

راهنمای کامل و قواعد سخت: **[docs/game-upload-standard.md](docs/game-upload-standard.md)** — خلاصه: ZIP با `index.html` در ریشه، پسوندهای مجاز، بدون مسیر مطلق، کاور ≤۲MB، سپس تأیید ادمین.

## 🤝 مشارکت

1. Issue/بحث باز کنید
2. فیچر را با چرخه spec-kit مستند کنید (spec → plan → tasks)
3. PR با تست و Evidence (خروجی `dotnet test`)

## 📄 لایسنس

[MIT](LICENSE) — © 2026 SSSchangerSSS (sohrab iranpak)
