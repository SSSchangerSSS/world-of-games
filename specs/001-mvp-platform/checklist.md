# Coverage & Consistency Checklist — 001-mvp-platform

## پوشش
- [x] REQ-001..REQ-010 هرکدام ≥1 TASK دارند (ماتریس tasks.md)
- [x] هر AC مسیر Verification دارد (TEST-* یا smoke/audit مشخص)
- [x] هر TASK والد (FEAT) و Parent REQ دارد
- [x] قراردادهای مشترک (IGameService/IDonationGateway/IGamePackageValidator/MCP tools) در plan.md تعریف شده‌اند — مرز Workerها روشن
- [x] Out of Scope صریح است — REQ خارج از Scope حذف بی‌ردپا ندارد

## سازگاری (Logical Consistency Check)
- [x] تعارض احرازشده: ندارد
- [x] Trade-off ثبت‌شده: sandbox بدون allow-same-origin ↔ بازی‌های نیازمند storage (KI-2) — پذیرش مالک
- [x] Trade-off ثبت‌شده: EnsureCreated ↔ تحول Schema آینده (KI-1، D-13) — پذیرش مالک
- [x] Trade-off ثبت‌شده: MCP دست‌ساز ↔ SDK رسمی (D-11، برگشت‌پذیر)
- [x] با قوانین قانون اساسی تعارضی یافت نشد (ماده ۱۵ NFR → REQ-009/010 پوشش دارد)

## Ready gate
- [x] همه تصمیم‌های مادی D-01..D-10 تأیید مالک (AskUserQuestion)
- [x] فرض‌های D-12 و KI-1..KI-5 ثبت و افشا شده‌اند
- [x] اندازه Taskها بر اساس Semantic Complexity — بدون Mega-Task و بدون خردشدن بی‌معنا

## Definition of Done (Evidence واقعی — تکمیل‌شده)
- [x] dotnet build -c Release — **0 Warning / 0 Error** (با override پکیج‌های آسیب‌پذیر ترانزیتیو)
- [x] dotnet test — **35/35 Passed**
- [x] smoke-run: همه صفحات 200 · dir=rtl · sandbox صحیح · بدون CDN خارجی · sitemap/robots/feed 200 · MCP 401/handshake/tools ✓ · جریان دونیت Mock کامل ✓
- [x] اندازه دارایی‌ها: CSS+JS=۲۱KB<۶۰KB · کل=۲۲۰KB<۳۰۰KB
- [x] dotnet publish → خروجی IIS-ready (۵۲MB)
- [ ] push + CI سبز (پس از push تأیید می‌شود — اقدام بعدی)
