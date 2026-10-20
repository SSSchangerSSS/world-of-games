# استاندارد بازی‌های دموی World of Games — برای همه بازی‌های جدید

هر بازی = **یک فایل `index.html` کاملاً سلف‌کانتینند** در مسیر مشخص‌شده. هیچ فایل دیگری مجاز نیست (به‌جز موارد استثنا که خودم می‌سازم).

## قیود سخت (MUST)
1. `<html lang="fa" dir="rtl">` + `<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />`
2. **تماماً آفلاین**: هیچ درخواست شبکه، هیچ CDN، هیچ `http://` یا `https://` در کد اجرایی (فقط کامنت).
3. **sandbox-safe**: بازی داخل iframe با `sandbox="allow-scripts ..."` **بدون allow-same-origin** اجرا می‌شود.
   - `localStorage` مستقیم ممنوع. فقط این shim در ابتدای اسکریپت:
     ```js
     var store = {
       get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
       set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
     };
     ```
   - هیچ دسترسی به `parent`، `window.top`، `document.cookie` ممنوع.
4. **بدون emoji**. حداکثر نویسه‌های تزئینی یونیکد ساده مثل ❋ ✓ ✕ (که در فونت‌های سیستمی هست).
5. کنترل با **لمس + ماوس + کیبورد** (هرجا منطقی است). `touch-action: manipulation` روی عناصر بازی.
6. ذخیره رکورد/بهترین امتیاز با `store` با کلید انگلیسی مثل `wog-snake-best`.
7. جاوااسکریپت ES5/ES6 معمولی بدون module/import؛ همه‌چیز داخل IIFE با 'use strict'.
8. حجم هدف: زیر ~۲۵KB برای هر index.html.

## توکن‌های طراحی (دقیقاً همین‌ها)
```css
body { font-family: Vazirmatn, Tahoma, sans-serif; background: linear-gradient(160deg,#101a2e,#0b1220);
       color: #f3ead8; min-height: 100dvh; user-select: none; }
/* طلایی: #d9a441 (اصلی) ، #e8c073 (روشن) ، فیروزه: #3fb8af ، متن کم‌رنگ: #a8b3c9 */
/* سطح: #14203a ، خط: rgba(217,164,65,.35) ، خطر: #e26d5c ، موفق: #67b98a */
header h1 { color:#d9a441; }  .hud b { color:#e8c073; }
```
- بالای صفحه: `<header>` وسط‌چین با `<h1>` فارسی + خط HUD (امتیاز/وضعیت).
- دکمه‌ها: پس‌زمینه `#d9a441`، متن `#221806`، `border-radius: 10px; font-weight: 700`، بدون تصویر.
- باخت/برد با پنل وسط صفحه (نه alert).

## ساختار HTML مرجع
```html
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<title>[نام فارسی بازی]</title>
<style> ... </style>
</head>
<body>
<header><h1>❋ [نام بازی] ❋</h1><div class="hud">...</div></header>
<!-- بازی -->
<script>
(function () {
  'use strict';
  var store = { ... };
  // ...
})();
</script>
</body>
</html>
```

## متن‌های فارسی استاندارد
- «امتیاز»، «رکورد»، «شروع دوباره»، «بردی!»، «باختی!»، «مساوی»، «راهنما»
- جمله راهنمای کوتاه پایین بازی (`#hint`) به فارسی.
