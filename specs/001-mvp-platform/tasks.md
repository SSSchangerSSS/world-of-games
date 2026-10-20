# Tasks: 001-mvp-platform — ماتریس Traceability کامل

Naming: TASK-FEAT-NN. هر تسک Local Spec کوتاه دارد (Parent/Goal/AC/Verify).

## TASK-DOM-01 — دامنه و قراردادها (Core)
- Parent: FEAT-DOM · Goal: Entityها + Interfaceها + SlugHelper + GamePackageValidator (قرارداد خالص)
- AC: REQ-004-2 (قرارداد اعتبارسنجی) · Depends: — · Verify: کامپایل + TEST-VALIDATOR
- Status: Done (مصرف‌کننده: Infrastructure/Web)

## TASK-INF-01 — Infrastructure: DbContext + سرویس‌های EF
- Parent: FEAT-INF · Goal: AppDbContext (Identity+دامنه)، EfGameService، EfBlogService، EfDonationService، EfAuditService، DbSeeder
- AC: REQ-002-3، REQ-007-2 · Depends: TASK-DOM-01 · Verify: TEST-GAME/TEST-BLOG/TEST-DONATION/TEST-AUDIT
- Status: Done

## TASK-SEC-01 — Validator + Gatewayها
- Parent: FEAT-SEC · Goal: ZipGamePackageValidator (استاندارد REQ-004) + MockGateway + ZarinpalGateway v4 + Factory
- AC: REQ-004-1/2/3، REQ-006-1/2/4 · Depends: TASK-DOM-01 · Verify: TEST-VALIDATOR، TEST-DONATION
- Status: Done

## TASK-WEB-01 — Web scaffold + Identity + Culture + Layout عمومی
- Parent: FEAT-WEB · Goal: Program.cs (fa-IR، static cache headers، Identity، DI)، _Layout RTL با تم ایران‌باستان، CSS design system، fonts self-hosted، Login/Register/Logout فارسی
- AC: REQ-001-1/2، REQ-002-1/2 · Depends: TASK-INF-01 · Verify: build + smoke HTML (dir=rtl، بدون CDN خارجی) + TEST-AUTH
- Status: Done

## TASK-GAME-01 — ماژول عمومی بازی‌ها
- Parent: FEAT-GAME · Goal: Index (جست‌وجو/مرتب‌سازی/صفحه‌بندی)، Details، Play (iframe sandbox + شمارش)، Submit (فرم + آپلود + استخراج امن)
- AC: REQ-003-1/2/3، REQ-004-1/3/4، REQ-009-1 · Depends: TASK-INF-01, TASK-SEC-01 · Verify: TEST-GAME + smoke
- Status: Done

## TASK-BLOG-01 — ماژول وبلاگ + SEO
- Parent: FEAT-BLOG · Goal: Index/Details عمومی، پست مرتبط، متا/canonical/OG/JSON-LD، sitemap.xml، robots.txt، feed.xml
- AC: REQ-005-1..5 · Depends: TASK-INF-01 · Verify: TEST-BLOG + smoke sitemap/rss
- Status: Done

## TASK-DON-01 — جریان دونیت
- Parent: FEAT-DON · Goal: صفحه دونیت، Start → دروازه → Callback → Verify → نتیجه + حامیان
- AC: REQ-006-1/2/3 · Depends: TASK-SEC-01 · Verify: TEST-DONATION + smoke با Mock
- Status: Done

## TASK-ADM-01 — پنل ادمین
- Parent: FEAT-ADM · Goal: Dashboard، صف تأیید (Approve/Reject با دلیل اجباری/Toggle)، CRUD وبلاگ، دونیت‌ها، کاربران، Audit log
- AC: REQ-007-1/2/3 · Depends: TASK-INF-01 · Verify: TEST-AUDIT + TEST-GAME (مدیریت) + smoke
- Status: Done

## TASK-MCP-01 — سرور MCP مدیریت بازی‌ها
- Parent: FEAT-MCP · Goal: POST /mcp (JSON-RPC 2.0، Bearer) با ۵ ابزار D-08 + Audit Source=Mcp
- AC: REQ-008-1..5 · Depends: TASK-INF-01, TASK-ADM-01(سرویس مشترک) · Verify: TEST-MCP
- Status: Done

## TASK-QA-01 — تست‌ها + Seed دمو + CI + IIS + README
- Parent: FEAT-QA · Goal: xUnit (VALIDATOR/GAME/BLOG/DONATION/AUDIT/MCP/AUTH/SEED)، دو بازی HTML5 دمو، ۳ پست seed، CI windows-latest، web.config+pubxml+docs، README فارسی
- AC: REQ-010-1/2، REQ-009-2 · Depends: همه · Verify: dotnet test سبز + اندازه‌گیری دارایی‌ها
- Status: Done

## Traceability Matrix

| REQ | AC | TASK | TEST | Evidence (نتیجه واقعی — بروزرسانی پس از اجرا) |
|---|---|---|---|---|
| REQ-001 | 1,2,3 | TASK-WEB-01 | smoke+audit-assets | dotnet test ✅ / اندازه wwwroot ✅ |
| REQ-002 | 1,2,3 | TASK-WEB-01, INF-01 | TEST-AUTH, TEST-SEED | dotnet test ✅ |
| REQ-003 | 1,2,3 | TASK-GAME-01 | TEST-GAME | dotnet test ✅ |
| REQ-004 | 1,2,3,4 | TASK-SEC-01, GAME-01 | TEST-VALIDATOR, TEST-GAME | dotnet test ✅ |
| REQ-005 | 1..5 | TASK-BLOG-01 | TEST-BLOG | dotnet test ✅ |
| REQ-006 | 1,2,3,4 | TASK-DON-01 | TEST-DONATION | dotnet test ✅ |
| REQ-007 | 1,2,3 | TASK-ADM-01 | TEST-AUDIT, TEST-GAME | dotnet test ✅ |
| REQ-008 | 1..5 | TASK-MCP-01 | TEST-MCP | dotnet test ✅ |
| REQ-009 | 1..4 | TASK-WEB-01, QA-01 | audit-assets + بازرسی | اندازه CSS/JS ✅ |
| REQ-010 | 1,2 | TASK-QA-01 | CI + publish | GitHub Actions ✅ / dotnet publish ✅ |

نکته Governance: وضعیت «Done» فقط پس از Evidence واقعی (build/test/smoke در این نسخه) معتبر است؛ ستون Evidence پس از اجرا پر شده و در worklog ثبت است.
