using Markdig;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;
using WorldOfGames.Infrastructure.Options;

namespace WorldOfGames.Infrastructure.Seed;

public static class DbSeeder
{
    public static async Task RunAsync(AppDbContext db, IServiceProvider services, string webRoot)
    {
        var logger = services.GetRequiredService<ILoggerFactory>().CreateLogger("DbSeeder");
        var seedOpt = services.GetRequiredService<IOptions<SeedOptions>>().Value;

        await db.Database.EnsureCreatedAsync(); // D-13 (KI-1)

        if (!seedOpt.Enabled)
        {
            await EnsureAdminAsync(db, services, logger); // ادمین همیشه تضمین شود
            return;
        }

        var hasData = await db.Games.AnyAsync() || await db.BlogPosts.AnyAsync();
        await EnsureAdminAsync(db, services, logger);
        if (hasData) return;

        logger.LogInformation("Seeding demo data…");

        // ── بازی‌های دمو (کپی از Data/SeedGames به wwwroot/media) ──
        var adminId = (await db.Users.FirstAsync(u => u.Email == services.GetRequiredService<IOptions<AdminSeedOptions>>().Value.Email)).Id;
        foreach (var (folder, title, cat, tags, desc, instr) in SeedCatalog.DemoGames)
        {
            var src = Path.Combine(AppContext.BaseDirectory, "Data", "SeedGames", folder);
            if (!Directory.Exists(src))
            {
                // در محیط توسعه، مسیر پروژه را امتحان کن
                src = Path.Combine(Directory.GetCurrentDirectory(), "Data", "SeedGames", folder);
            }
            if (!Directory.Exists(src))
            {
                logger.LogWarning("SeedGame folder not found: {Src}", src);
                continue;
            }
            var dest = Path.Combine(webRoot, "media", "games", folder);
            CopyDir(src, dest);

            db.Games.Add(new Game
            {
                Slug = folder,
                Title = title,
                Category = cat,
                TagsCsv = tags,
                Description = desc,
                Instructions = instr,
                Status = GameStatus.Approved,
                IsEnabled = true,
                ReviewedAt = DateTime.UtcNow,
                ReviewedBy = "seed",
                CoverPath = $"/media/covers/{folder}.svg",
                EntryPath = $"/media/games/{folder}/index.html",
                DeveloperUserId = adminId,
                DeveloperName = "تیم World of Games",
                SubmittedAt = DateTime.UtcNow.AddDays(-3)
            });
            // کاور SVG دمو
            var covers = Path.Combine(webRoot, "media", "covers");
            Directory.CreateDirectory(covers);
            await File.WriteAllTextAsync(Path.Combine(covers, $"{folder}.svg"), SeedCatalog.CoverSvg(folder, title));
        }

        // ── پست‌های وبلاگ ──
        foreach (var (slug, title, excerpt, tags, meta, md) in SeedCatalog.Posts)
        {
            db.BlogPosts.Add(new BlogPost
            {
                Slug = slug,
                Title = title,
                Excerpt = excerpt,
                ContentHtml = Markdig.Markdown.ToHtml(md, SeedCatalog.MdPipeline),
                TagsCsv = tags,
                MetaTitle = meta,
                MetaDescription = excerpt,
                IsPublished = true,
                PublishedAt = DateTime.UtcNow.AddDays(-1),
                AuthorDisplayName = "تیم World of Games"
            });
        }

        await db.SaveChangesAsync();
        logger.LogInformation("Seeding done.");
    }

    private static async Task EnsureAdminAsync(AppDbContext db, IServiceProvider services, ILogger logger)
    {
        var opt = services.GetRequiredService<IOptions<AdminSeedOptions>>().Value;
        if (string.IsNullOrWhiteSpace(opt.Password))
        {
            logger.LogWarning("AdminSeed:Password خالی است — ادمین seed نشد.");
            return;
        }
        var roleManager = services.GetRequiredService<RoleManager<IdentityRole>>();
        if (!await roleManager.RoleExistsAsync("Admin"))
            await roleManager.CreateAsync(new IdentityRole("Admin"));
        if (!await roleManager.RoleExistsAsync("User"))
            await roleManager.CreateAsync(new IdentityRole("User"));

        if (await db.Users.AnyAsync(u => u.Email == opt.Email)) return;
        var userManager = services.GetRequiredService<UserManager<ApplicationUser>>();
        var admin = new ApplicationUser
        {
            UserName = opt.Email,
            Email = opt.Email,
            EmailConfirmed = true,
            DisplayName = string.IsNullOrWhiteSpace(opt.DisplayName) ? "مدیر" : opt.DisplayName
        };
        var result = await userManager.CreateAsync(admin, opt.Password);
        if (result.Succeeded)
        {
            await userManager.AddToRoleAsync(admin, "Admin");
            logger.LogInformation("Admin user seeded: {Email}", opt.Email);
        }
        else logger.LogError("Admin seed failed: {Errors}", string.Join(", ", result.Errors.Select(e => e.Description)));
    }

    private static void CopyDir(string src, string dest)
    {
        Directory.CreateDirectory(dest);
        foreach (var file in Directory.GetFiles(src, "*", SearchOption.AllDirectories))
        {
            var rel = Path.GetRelativePath(src, file);
            var target = Path.Combine(dest, rel);
            Directory.CreateDirectory(Path.GetDirectoryName(target)!);
            File.Copy(file, target, overwrite: true);
        }
    }
}

/// <summary>رجیستری محتوا/مسیرهای seed — جدا از منطق (قاعده ۱۹.۲ قانون اساسی: قواعد پایدار جدا از فیچر).</summary>
public static class SeedCatalog
{
    public static readonly Markdig.MarkdownPipeline MdPipeline = new Markdig.MarkdownPipelineBuilder()
        .UseAdvancedExtensions().DisableHtml().Build();

    public static readonly (string Folder, string Title, string Category, string Tags, string Desc, string Instructions)[] DemoGames =
    {
        ("akhaemenid-memory", "حافظه هخامنشی", "معمایی", "فارسی,حافظه,خانوادگی",
         "بازی حافظه با نمادهای ایران باستان؛ جفت‌های یکسان را پیدا کنید و امتیاز بگیرید. مناسب همه سن‌ها و کاملاً تحت وب — بدون نصب.",
         "روی کارت‌ها بزنید تا برگردند؛ جفت یکسان را پیدا کنید. تعداد حرکت کمتر = امتیاز بیشتر."),
        ("alborz-jump", "پرش از البرز", "اکشن", "فارسی,اکشن,کازوال",
         "در کوهستان اسطوره‌ای البرز بپرید، از صخره‌ها بگذرید و امتیاز بگیرید. یک بازی کازوال سبک برای مرورگر.",
         "کلیک/لمس = پرش. سقوط در دره = پایان بازی. سرعت به‌مرور بیشتر می‌شود."),
        ("chess", "شطرنج", "تخته‌ای", "شطرنج,تخته‌ای,هوش",
         "شطرنج کلاسیک برابر حریف رایانه‌ای؛ موتور قوانین متن‌باز chess.js (BSD-2) با هوش مصنوعی آلفا-بتا در دو سطح. برج‌ها، فیل‌ها و اسب‌ها با تم ایران باستان.",
         "مهرهٔ خودتان را بزنید و بعد خانهٔ مقصد را. سرباز به ردیف آخر برسد ارتقا می‌گیرد. «برگرداندن حرکت» دو نیم‌حرکت آخر را پس می‌گیرد."),
        ("solitaire", "پاسور (کلایک)", "کارتی", "پاسور,کارت,کلاسیک",
         "پاسور کلایک کلاسیک با ۵۲ کارت؛ ستون‌ها را نزولی و یک‌درمیان قرمز/سیاه بچینید و چهار خال را از آس تا شاه روی خانه‌هایشان سوار کنید.",
         "کارت را بزنید و بعد مقصد را. روی دستهٔ بسته بزنید تا کارت بخورید؛ «خودکار» کارت‌های آماده را می‌فرستد و «برگردان» یک حرکت عقب می‌رود."),
        ("blackjack", "بلک‌جک ۲۱", "کارتی", "بلک‌جک,کارت,۲۱",
         "بلک‌جک کلاسیک با سکه‌های مجازی؛ از حریف به ۲۱ نزدیک‌تر باشید بدون این‌که بُر بخورید. بلک‌جک ۱.۵ برابر می‌پردازد و دوبرابرکردن در اولین فرصت ممکن است. سکه‌ها ذخیره می‌شوند.",
         "با دکمه‌های +۵/+۲۵/+۱۰۰ شرط بگذارید و «پخش کن» را بزنید؛ سپس کارت بگیرید یا ایست کنید. سکه‌ها فقط مجازی‌اند."),
        ("sudoku", "سودوکو", "پازل", "سودوکو,پازل,اعداد",
         "سودوکو با جدول‌های تازه‌تولیدشده و راه‌حل یکتا؛ سه سطح آسان، متوسط و سخت. راهنما تا سه بار خانهٔ درست را نشان می‌دهد و رکورد زمان هر سطح ذخیره می‌شود.",
         "خانه را بزنید و عدد را از صفحهٔ شماره انتخاب کنید؛ تعارض‌ها با رنگ قرمز مشخص می‌شوند. در هر سطر، ستون و مربع ۳×۳ هر عدد فقط یک بار."),
        ("reversi", "اوتِلو (ریورسی)", "تخته‌ای", "اوتلو,ریورسی,تخته‌ای",
         "ریورسی کلاسیک؛ دیسک‌های حریفِ میان دو دیسک شما برمی‌گردند. گوشه‌ها طلایی‌اند — با استراتژی، صفحه را از آنِ خود کنید. حریف رایانه‌ای وزن موقعیتی را می‌سنجد.",
         "خانه‌های مجاز با نقطهٔ طلایی نشان داده می‌شوند؛ اگر حرکتی نداشته باشید نوبت رد می‌شود."),
        ("snake", "مارِ گرسنه", "کازوال", "مار,کازوال,کلاسیک",
         "مار کلاسیک در باغ لاجوردی؛ سیب بخورید، بلند شوید و به خودتان یا دیوار نخورید. هرچه بیشتر بخورید سریع‌تر می‌شوید.",
         "با کلیدهای جهت یا کشیدن انگشت جهت بدهید؛ رکوردتان ذخیره می‌شود."),
        ("breakout", "توپ‌شکن", "اکشن", "توپ‌شکن,آجر,کلاسیک",
         "آجرهای شش‌ردیفه را با توپ و راکت بشکنید؛ ردیف‌های بالاتر امتیاز بیشتری دارند و با خالی‌شدن صفحه، مرحلهٔ سریع‌تر بعدی می‌آید.",
         "راکت را با لمس، ماوس یا کلیدهای چپ/راست ببرید؛ توپ با لبهٔ راکت زاویه می‌گیرد. سه جان دارید."),
        ("pong", "پینگ‌پنگ", "کازوال", "پینگ‌پنگ,راکت,کلاسیک",
         "پینگ‌پنگ برابر کامپیوتر؛ اولین نفر به ۷ امتیاز برنده است. با هر برخورد، توپ کمی سریع‌تر می‌شود.",
         "راکت شما پایین است؛ با لمس، ماوس یا کلیدهای چپ/راست حرکتش بدهید."),
        ("tic-tac-toe", "دوز", "تخته‌ای", "دوز,تخته‌ای,کلاسیک",
         "دوز کلاسیک برابر حریفی که هرگز اشتباه نمی‌کند — آیا می‌توانید حداقل مساوی بگیرید؟ شمارش برد/باخت/مساوی ذخیره می‌شود.",
         "خانهٔ خالی بزنید؛ سه‌تاییِ خودتان را کامل کنید و جلوی خط حریف را بگیرید."),
        ("minesweeper", "مین‌یاب", "معمایی", "مین‌یاب,معمایی,کلاسیک",
         "مین‌یاب کلاسیک با دو سطح؛ اولین کلیک همیشه امن است. با پرچم محل مین‌ها را نشانه‌گذاری کنید و همهٔ خانه‌های امن را باز کنید.",
         "بزنید تا خانه باز شود؛ حالت پرچم یا راست‌کلیک برای نشانه‌گذاری مین است. اعداد یعنی تعداد مین‌های همسایه."),
        ("g2048", "۲۰۴۸", "پازل", "۲۰۴۸,پازل,اعداد",
         "پازل معروف ۲۰۴۸ با تم ایرانی؛ کاشی‌های هم‌ارزش را ادغام کنید و به ۲۰۴۸ برسید. پیاده‌سازی آزاد از مکانیکِ اثر گابریله چیرولی (متن‌باز MIT).",
         "با کلیدهای جهت یا سوایپ همهٔ کاشی‌ها را حرکت بدهید؛ کاشی‌های هم‌ارزش یکی می‌شوند.")
    };

    public static readonly (string Slug, string Title, string Excerpt, string Tags, string Meta, string Md)[] Posts =
    {
        ("welcome-to-world-of-games", "به World of Games خوش آمدید", "پلتفرم ایرانی بازی‌های تحت وب راه‌اندازی شد؛ بازی کنید، بسازید و با حمایت خود پلتفرم را زنده نگه دارید.",
         "معرفی,اخبار", "معرفی پلتفرم World of Games — بازی‌های تحت وب ایرانی",
         """
## بازی‌های ایرانی، در مرورگر شما

**World of Games** یک پلتفرم کاملاً ایرانی برای بازی‌های تحت وب است. هیچ نصبی لازم نیست؛ یک کلیک و بازی شروع می‌شود. هدف ما ساختن خانه‌ای امن و استاندارد برای بازی‌سازهای ایرانی است.

### چه چیزی اینجا می‌بینید؟

- کاتالوگ بازی‌های سبک و تحت وب
- فرآیند شفاف «درخواست آپلود» برای بازی‌سازها
- وبلاگی برای آموزش و اخبار
- حمایت مالی (دونیت) به‌جای تبلیغات مزاحم

### مسیر پیش‌رو

این اسکلت MVP است؛ در چرخه‌های بعدی امتیازدهی، پروفایل توسعه‌دهنده و ابزارهای بیشتر اضافه می‌شود. نظرات شما مسیر را تعیین می‌کند.
"""),
        ("game-upload-standard", "استاندارد آپلود بازی: راهنمای کامل", "برای اینکه بازی شما سریع تأیید شود، استاندارد بسته ZIP را دقیق بخوانید؛ از index.html ریشه تا whitelist پسوندها.",
         "استاندارد,آپلود,راهنما", "استاندارد آپلود بازی در World of Games — راهنمای بازی‌سازها",
         """
## استاندارد بسته بازی

بازی شما باید یک **ZIP** باشد که فایل `index.html` در **ریشه** آن قرار دارد. همه مسیرها نسبی باشند و به هیچ دامنه خارجی وابسته نباشند.

### قواعد سخت (رد خودکار)

- حداکثر حجم فشرده ۵۰ مگابایت و نافشرده ۳۰۰ مگابایت
- بدون مسیر مطلق یا `../` (حمله zip-slip)
- فقط پسوندهای مجاز: HTML/CSS/JS، تصاویر (PNG/JPG/WebP/SVG)، فونت (woff2/ttf)، صدا/ویدیو (mp3/ogg/wav/mp4/webm) و داده‌های موتورها
- فایل‌های اجرایی (exe/dll/bat/…) کاملاً ممنوع

### نکته sandbox

بازی‌ها در iframe با `sandbox` اجرا می‌شوند تا امنیت سایت حفظ شود؛ بنابراین `localStorage` در دسترس نیست. این الگو را در کد خود بگذارید:

```js
const store = {
  get(k){ try { return localStorage.getItem(k); } catch { return null; } },
  set(k,v){ try { localStorage.setItem(k,v); } catch {} }
};
```

### کاور

یک تصویر JPG/PNG/WebP حداکثر ۲ مگابایت؛ نسبت ۳:۲ بهترین نمایش را دارد.
"""),
        ("seo-for-web-games", "سئو برای بازی‌های تحت وب", "چطور صفحات بازی و وبلاگ پلتفرم را برای موتورهای جست‌وجو بهینه کنیم؛ از متا و sitemap تا داده ساختاریافته.",
         "سئو,وبلاگ,آموزش", "سئو برای بازی‌های تحت وب — راهنمای عملی",
         """
## چرا سئو برای پلتفرم بازی مهم است؟

بخش بزرگی از کاربران از گوگل وارد می‌شوند. یک صفحه بازی خوب بهینه‌شده یعنی ترافیک پایدار و رایگان.

### چک‌لیست سئوی این پلتفرم

1. **عنوان و توضیحات متا** یکتا برای هر صفحه (حداکثر ~۶۰ و ~۱۵۵ نویسه)
2. **Canonical** برای جلوگیری از محتوای تکراری
3. **JSON-LD** از نوع `Article` برای پست‌های وبلاگ و `VideoGame` برای بازی‌ها
4. **sitemap.xml** و **robots.txt** که این پلتفرم به‌صورت خودکار می‌سازد
5. **سرعت**: سایت سبک است (بدون کتابخانه‌های سنگین) — این خودش یک فاکتور رتبه است

### برای بازی‌سازها

عنوان بازی و توضیحات را با کلیدواژه واقعی بنویسید؛ «بازی حافظه فارسی» بهتر از «بازی من ۱» عمل می‌کند. وبلاگ ما هم به بازی شما لینک می‌دهد — تگ‌های درست انتخاب کنید.
""")
    };

    public static string CoverSvg(string slug, string title) =>
        $"""
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#16213e"/><stop offset="1" stop-color="#0b1220"/>
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#g)"/>
  <g fill="none" stroke="#d9a441" stroke-width="3" opacity="0.85">
    <circle cx="300" cy="170" r="58"/>
    <path d="M300 96 L300 244 M242 170 L358 170 M258 128 L342 212 M342 128 L258 212"/>
  </g>
  <text x="300" y="300" text-anchor="middle" font-family="Vazirmatn, sans-serif" font-size="30" fill="#f3ead8" direction="rtl">{System.Security.SecurityElement.Escape(title)}</text>
  <text x="300" y="345" text-anchor="middle" font-family="Vazirmatn, sans-serif" font-size="16" fill="#d9a441" direction="rtl">World of Games</text>
</svg>
""";
}
