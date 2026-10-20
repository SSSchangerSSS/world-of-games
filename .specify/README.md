# Spec Kit — World of Games

این مخزن با روش **Spec-Driven Development** و مطابق `specs/` و `.specify/` پیش می‌رود.

## ساختار

```text
.specify/
  memory/constitution.md      ← قانون اساسی (قرارداد بالادست — تغییر آن فقط با تأیید مالک)
  templates/                  ← قالب‌های spec / plan / tasks / checklist
  scripts/bash/               ← اسکریپت‌های کمکی
specs/
  001-mvp-platform/           ← Feature فعلی: اسکلت کامل MVP
    spec.md                   ← نیازمندی‌ها و Acceptance Criteria (قرارداد اجرا)
    plan.md                   ← معماری و تصمیم‌های فنی
    tasks.md                  ← تجزیه کار + ماتریس Traceability
    data-model.md             ← مدل داده
    checklist.md              ← Coverage & Consistency Check
```

## چرخه یک Feature جدید

1. **Clarify** — ابهام‌های مادی با مالک حل می‌شود.
2. **Specify** — `specs/<NNN>-<name>/spec.md` با REQ-xxx و AC قابل بررسی.
3. **Plan** — معماری، قراردادها، NFRها.
4. **Tasks** — تجزیه به Atomic Task با Local Spec + Traceability.
5. **Coverage Check** — هر REQ پوشش دارد؟ هر AC مسیر Verification دارد؟
6. **Implement → Verify → Review** — با Evidence واقعی (build/test/smoke).

## استفاده از GitHub Spec Kit CLI (اختیاری)

اگر [`github/spec-kit`](https://github.com/github/spec-kit) نصب باشد:

```bash
specify init --here
specify specify "عنوان فیچر"   # بعد از بازبینی، فایل‌های این پوشه را با خروجی CLI هم‌تراز کنید
```

نکته: این مخزن بدون CLI هم کاملاً کار می‌کند؛ قالب‌های همین پوشه مرجع هستند.
