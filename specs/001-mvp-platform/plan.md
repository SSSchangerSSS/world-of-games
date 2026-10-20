# Plan: 001-mvp-platform

Feature Spec: specs/001-mvp-platform/spec.md (قرارداد اجرا)

## Architecture Overview

```text
┌──────────────────────────── Browser (RTL, mobile-first) ────────────────────────────┐
│  Razor Views + CSS Design System (لاجورد/زرین) + JS ~2KB (drawer/confirm)           │
└───────────────┬──────────────────────────────┬──────────────────────────────────────┘
                │ HTML                          │ POST /mcp (JSON-RPC 2.0, Bearer)
┌───────────────▼──────────────────────────────▼──────────────────────────────────────┐
│ WorldOfGames.Web (ASP.NET Core MVC, .NET 10)                                        │
│  Controllers: Home, Games, Blog, Donations, Account, Admin                          │
│  McpEndpoints (دست‌ساز، D-11) → McpToolRegistry → IGameService + IAuditService       │
│  Identity (Admin/User) + ProblemDetails + fa-IR culture                             │
└───────────────┬─────────────────────────────────────────────────────────────────────┘
                │
┌───────────────▼───────────────────────────────┐   ┌─────────────────────────────────┐
│ WorldOfGames.Core (Entities, Interfaces,      │   │ WorldOfGames.Infrastructure     │
│ SlugHelper, GamePackageValidator(قرارداد),    │◄──┤ AppDbContext (Identity + دامنه) │
│ DTOها)                                        │   │ EfGameService/EfBlogService/... │
└───────────────────────────────────────────────┘   │ ZarinpalGateway/MockGateway     │
                                                    │ DbSeeder (دو بازی دمو + ۳ پست)  │
                                                    └───────────┬─────────────────────┘
                                                                │ EF Core 10
                                                    SQLite (توسعه) / SQL Server (پروداکشن، D-05)
```

فایل‌های بازی کاربران: `wwwroot/media/games/{slug}/…` (استاتیک، iframe با sandbox). کاورها: `wwwroot/media/covers/`.

## Stack & Approved Decisions
| تصمیم | مقدار | منبع |
|---|---|---|
| D-01..D-10 | ریپو world-of-games، Public، MIT، .NET 10 LTS، SQLite+SQL Server، ZIP+sandbox، زرین‌پال+انتزاعی، MCP فقط بازی‌ها، IIS، MVP کامل | کارگاه رفع ابهام (worklog Task-1) |
| D-11 | MCP: JSON-RPC 2.0 دست‌ساز روی POST /mcp، پاس JSON، احراز Bearer از کانفیگ — عمداً بدون وابستگی SDK (برگشت‌پذیر) | Agent (implementation-level) |
| D-12 | پست مرتبط = تگ مشترک؛ پیوست تصویر/فایل در پست | فرض ثبت‌شده |
| D-13 | Schema فاز ۱: EnsureCreated | ثبت‌شده/KI-1 |
| D-14 | قانون اساسی عیناً در .specify/memory/constitution.md | مالک |

## Contracts (قراردادهای مشترک)
- `IGameService`: لیست/جزئیات/SubmitRequest/ListByStatus/Approve/Reject/SetEnabled/IncrementPlay — همه تغییرات مدیریتی باید Audit بنویسند.
- `IBlogService`: Markdown→HTML (Markdig با امن‌سازی: raw HTML غیرفعال)، Slug یکتا، لیست مرتبط با تگ مشترک.
- `IDonationGateway`: `Name`, `RequestAsync(CreateDonation) → (RedirectUrl, Authority)`, `VerifyAsync(Authority, Amount) → (Success, RefId, Message)` — هیچ پیاده‌سازی نباید DB لمس کند.
- `IGamePackageValidator`: خروجی `PackageValidationResult(Success, Errors[])` — machine-checkable استاندارد REQ-004.
- MCP tools (5): نام/اسکیمای ورودی ثابت در `McpToolRegistry`؛ پاس همیشه `content:[{type:"text",text:"<json>"}]`.
- جریان زرین‌پال v4: `POST {Base}/pg/v4/payment/request.json` → `authority` → ریدایرکت `{Base}/pg/StartPay/{authority}` → callback → `POST {Base}/pg/v4/payment/verify.json`.

## Non-Functional Targets
- دارایی‌های ثابت صفحه اصلی < 300KB (REQ-001)، CSS+JS < 60KB (REQ-009)؛ بدون فونت/CDN خارجی؛ اهداف لمسی ≥44px؛ بدون overflow-x؛ cache headers استاتیک.
- Security: sandbox بدون allow-same-origin، امن‌سازی Markdown، CSRF (antiforgery) روی همه فرم‌های POST، Bearer توکن MCP، اعتبارسنجی سمت سرور همه ورودی‌ها، عدم نمایش مبلغ فردی حامیان.
- Maintainability: لایه‌بندی Core/Infra/Web، بدون منطق دامنه در Controller.

## Risks & Mitigations
- ریسک تغییر API زرین‌پال → BaseUrl/مسیرها کانفیگ‌پذیر + Mock مرجع توسعه.
- ریسک ZIP مخرب → whitelist پسوند + مسیر مطلق/`..` + سقف فایل/تعداد + استخراج در مسیر ایزوله (KI-4 ثبت است).
- ریسک EnsureCreated در پروداکشن → مستند در deploy-iis (فاز ۲: Migration).
