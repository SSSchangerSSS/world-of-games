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

## Definition of Done (پیش از اعلام Done)
- [ ] dotnet build -c Release بدون error
- [ ] dotnet test همه سبز (Evidence در worklog)
- [ ] smoke-run: صفحات اصلی 200 و dir=rtl
- [ ] اندازه دارایی‌ها داخل سقف REQ-001/009
- [ ] push + CI سبز
