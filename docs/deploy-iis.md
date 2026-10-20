# دیپلوی روی Windows + IIS

هدف پروداکشن طبق تصمیم D-09.

## ۱) پیش‌نیازهای سرور

1. Windows Server 2019+ با IIS (نقش Web Server)
2. **.NET Hosting Bundle 10** (بعد از نصب: `iisreset`) — لینک: dotnet.microsoft.com/download/dotnet/10.0
3. URL Rewrite (اختیاری، برای force-HTTPS)

## ۲) پابلیش

```powershell
dotnet publish src/WorldOfGames.Web -c Release -o publish
```

یا از پروفایل: `dotnet publish -p:PublishProfile=IIS` (آدرس سرور را در `Properties/PublishProfiles/IIS.pubxml` تنظیم کنید).

خروجی CI هم artifact آماده IIS می‌سازد (`.github/workflows/ci.yml`).

## ۳) سایت IIS

1. پوشه `publish` را در `C:\inetpub\worldofgames` کپی کنید
2. Application Pool جدید: **No Managed Code**
3. Site جدید روی پورت ۸۰/۴۳۳ با همان Pool
4. `Web.config` همراه خروجی است (ANCM V2, inprocess, کش استاتیک ۷ روز)

## ۴) تنظیمات محیطی (بجای appsettings)

```powershell
# در Application Pool → Environment Variables یا web.config override:
Database__Provider=SqlServer
ConnectionStrings__SqlServer=Server=.;Database=WorldOfGames;User Id=...;Password=...;TrustServerCertificate=True
Donations__Gateway=Zarinpal
Zarinpal__MerchantId=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Mcp__Token=<توکن قوی تصادفی — تغییر اجباری>
Seed__Enabled=false          # در پروداکشن seed دمو خاموش
AdminSeed__Email=admin@yourdomain.ir
AdminSeed__Password=<رمز قوی — بعد از اولین ورود تغییر دهید>
```

## ۵) نکته دیتابیس (KI-1)

فاز ۱ اسکیما با `EnsureCreated` ساخته می‌شود: اولین اجرا دیتابیس/جداول را می‌سازد.
**در پروداکشن**: دیتابیس را یک بار با اجرای اولیه بسازید و از آن پس تغییر Schema نیازمند Migration است (فاز ۲). بکاپ‌گیری SQL Server را فراموش نکنید.

## ۶) مجوزهای پوشه‌ها

| پوشه | مجوز IIS AppPool |
|---|---|
| `App_Data\` | Modify (دیتابیس SQLite توسعه) |
| `wwwroot\media\` | Modify (آپلود بازی‌سازها + کاورها) |
| بقیه | Read & Execute |

## ۷) چک‌لیست امنیتی قبل از آنلاین

- [ ] `Mcp:Token` تغییر کرده (توکن پیش‌فرض در ریپو عمومی است!)
- [ ] `AdminSeed:Password` تغییر کرده یا `Seed:Enabled=false`
- [ ] HTTPS + ریدایرکت فعال
- [ ] `Donations:Gateway=Zarinpal` و MerchantId واقعی (تا آن لحظه Mock فعال است — KI-3)
- [ ] بکاپ خودکار `App_Data` (اگر SQLite) یا دیتابیس
- [ ] فایروال: فقط 80/443
