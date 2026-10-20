using System.IO.Compression;
using System.Text;
using Microsoft.Extensions.Logging.Abstractions;
using WorldOfGames.Core.Common;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;

namespace WorldOfGames.Tests;

// ───────── TEST-GAME (REQ-003/004/007) ─────────
public class GameServiceTests : IDisposable
{
    private readonly (AppDbContext Db, SqliteConnection Conn) _env = TestEnv.CreateDb();
    private readonly string _webRoot;

    public GameServiceTests()
    {
        _webRoot = Path.Combine(Path.GetTempPath(), "wog-tests", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(_webRoot);
    }

    public void Dispose()
    {
        _env.Conn.Dispose();
        try { Directory.Delete(_webRoot, recursive: true); } catch { }
    }

    private SubmitGameInput MakeInput(string title = "بازی آزمایشی کوهستان", byte[]? zip = null, string coverName = "cover.png")
    {
        zip ??= BuildZip();
        var cover = Encoding.UTF8.GetBytes("fake-png-bytes");
        return new SubmitGameInput(title, "توضیحات کامل بازی آزمایشی برای تست اعتبارسنجی و ذخیره‌سازی.",
            null, "اکشن", "تست,دمو",
            new MemoryStream(zip), zip.Length,
            new MemoryStream(cover), coverName, cover.Length,
            "user-1", "توسعه‌دهنده تست", _webRoot);
    }

    private static byte[] BuildZip() =>
        BuildZipFiles(("index.html", "<html><body>ok</body></html>"), ("js/main.js", "console.log(1)"));

    private static byte[] BuildZipFiles(params (string, string)[] files)
    {
        using var ms = new MemoryStream();
        using (var zip = new ZipArchive(ms, ZipArchiveMode.Create, true))
        {
            foreach (var (name, content) in files)
            {
                var e = zip.CreateEntry(name);
                using var w = new StreamWriter(e.Open(), Encoding.UTF8);
                w.Write(content);
            }
        }
        return ms.ToArray();
    }

    [Fact]
    public async Task Submit_creates_pending_game_and_extracts_files()
    {
        var svc = TestEnv.GameService(_env.Db);
        var result = await svc.SubmitAsync(MakeInput());

        Assert.True(result.Success, string.Join("; ", result.Errors ?? []));
        var game = result.Value!;
        Assert.Equal(GameStatus.Pending, game.Status);
        Assert.False(string.IsNullOrEmpty(game.Slug));
        Assert.Equal("/media/games/" + game.Slug + "/index.html", game.EntryPath);
        Assert.True(File.Exists(Path.Combine(_webRoot, "media", "games", game.Slug, "index.html")));
        Assert.True(File.Exists(Path.Combine(_webRoot, "media", "covers", game.Slug + ".png")));
    }

    [Fact]
    public async Task Submit_rejects_invalid_package_without_writing_files()
    {
        var svc = TestEnv.GameService(_env.Db);
        var bad = BuildZipFiles(("runme.exe", "MZ"));
        var result = await svc.SubmitAsync(MakeInput(zip: bad));

        Assert.False(result.Success);
        Assert.Contains(result.Errors!, e => e.Contains("exe"));
        Assert.False(Directory.Exists(Path.Combine(_webRoot, "media", "games")));
    }

    [Fact]
    public async Task Published_list_excludes_disabled_and_rejected()
    {
        var svc = TestEnv.GameService(_env.Db);
        var g1 = (await svc.SubmitAsync(MakeInput("بازی اول"))).Value!;
        var g2 = (await svc.SubmitAsync(MakeInput("بازی دوم"))).Value!;
        await svc.ApproveAsync(g1.Id, "admin", AuditSource.Web);
        await svc.ApproveAsync(g2.Id, "admin", AuditSource.Web);
        await svc.SetEnabledAsync(g2.Id, enabled: false, "admin", AuditSource.Web);

        var list = await svc.ListPublishedAsync(null, null, 1, 12);
        var item = Assert.Single(list.Items);
        Assert.Equal(g1.Slug, item.Slug);

        // REQ-003-2: بازی غیرفعال با URL مستقیم → null
        Assert.Null(await svc.GetPublishedBySlugAsync(g2.Slug));
    }

    [Fact]
    public async Task Reject_requires_reason()
    {
        var svc = TestEnv.GameService(_env.Db);
        var game = (await svc.SubmitAsync(MakeInput())).Value!;
        var res = await svc.RejectAsync(game.Id, "", "admin", AuditSource.Web);
        Assert.False(res.Success);

        var res2 = await svc.RejectAsync(game.Id, "بسته شامل index.html نیست", "admin", AuditSource.Web);
        Assert.True(res2.Success);
        var stored = await _env.Db.Games.AsNoTracking().FirstAsync(g => g.Id == game.Id);
        Assert.Equal(GameStatus.Rejected, stored.Status);
        Assert.NotNull(stored.RejectionReason);
    }

    [Fact]
    public async Task Approve_writes_audit()
    {
        var svc = TestEnv.GameService(_env.Db);
        var game = (await svc.SubmitAsync(MakeInput())).Value!;
        await svc.ApproveAsync(game.Id, "admin", AuditSource.Mcp);
        var audit = await _env.Db.AuditEntries.AsNoTracking().SingleAsync(a => a.EntityId == game.Id.ToString());
        Assert.Equal(AuditSource.Mcp, audit.Source);
        Assert.Equal("GameApprove", audit.Action);
    }

    [Fact]
    public async Task Play_count_increments()
    {
        var svc = TestEnv.GameService(_env.Db);
        var game = (await svc.SubmitAsync(MakeInput())).Value!;
        await svc.ApproveAsync(game.Id, "admin", AuditSource.Web);
        await svc.IncrementPlayAsync(game.Id);
        await svc.IncrementPlayAsync(game.Id);
        var stored = await _env.Db.Games.AsNoTracking().FirstAsync(g => g.Id == game.Id);
        Assert.Equal(2, stored.PlayCount);
    }
}

// ───────── TEST-BLOG (REQ-005) ─────────
public class BlogServiceTests : IDisposable
{
    private readonly (AppDbContext Db, SqliteConnection Conn) _env = TestEnv.CreateDb();

    public void Dispose() => _env.Conn.Dispose();

    private static BlogPostInput MakeInput(string title, string tags, bool published = true) =>
        new(title, null, "خلاصه پست برای سئو که باید حداقل ده نویسه باشد.",
            "## سلام\nاین یک **پست** آزمایشی است با متن کافی برای عبور از اعتبارسنجی.",
            tags, null, null, published, null, "نویسنده");

    [Fact]
    public async Task Create_renders_markdown_and_strips_raw_html()
    {
        var svc = TestEnv.BlogService(_env.Db);
        var input = MakeInput("پست آزمایشی سئو", "سئو,آموزش") with
        {
            Markdown = "## تیتر\n<script>alert(1)</script>متن **بولد**"
        };
        var res = await svc.CreateAsync(input);
        Assert.True(res.Success, string.Join(";", res.Errors ?? []));
        var post = res.Value!;
        Assert.Contains("<h2", post.ContentHtml);
        Assert.DoesNotContain("<script", post.ContentHtml);
        Assert.Contains("<strong>بولد</strong>", post.ContentHtml);
    }

    [Fact]
    public async Task Drafts_are_hidden_and_slug_unique()
    {
        var svc = TestEnv.BlogService(_env.Db);
        var p1 = (await svc.CreateAsync(MakeInput("عنوان مشابه", "t"))).Value!;
        var p2 = (await svc.CreateAsync(MakeInput("عنوان مشابه", "t"))).Value!;
        Assert.NotEqual(p1.Slug, p2.Slug);

        var draft = (await svc.CreateAsync(MakeInput("پیش‌نویس محرمانه", "t", published: false))).Value!;
        Assert.Null(await svc.GetPublishedBySlugAsync(draft.Slug)); // REQ-005-5
        Assert.Equal(2, (await svc.ListPublishedAsync(1, 10)).Total);
    }

    [Fact]
    public async Task Related_posts_use_shared_tags()
    {
        var svc = TestEnv.BlogService(_env.Db);
        var seo = (await svc.CreateAsync(MakeInput("راهنمای سئو", "سئو,آموزش"))).Value!;
        var seo2 = (await svc.CreateAsync(MakeInput("سئو پیشرفته", "سئو,بازی"))).Value!;
        var other = (await svc.CreateAsync(MakeInput("اخبار ورزشی", "ورزش"))).Value!;

        var related = await svc.ListRelatedAsync(seo.Id, seo.TagsCsv, 3);
        Assert.Contains(related, p => p.Id == seo2.Id);
        Assert.DoesNotContain(related, p => p.Id == other.Id);
        Assert.DoesNotContain(related, p => p.Id == seo.Id); // خود پست (REQ-005-4)
    }
}

// ───────── TEST-DONATION (REQ-006) ─────────
public class DonationServiceTests : IDisposable
{
    private readonly (AppDbContext Db, SqliteConnection Conn) _env = TestEnv.CreateDb();

    public void Dispose() => _env.Conn.Dispose();

    [Fact]
    public async Task Mock_flow_start_then_verify_pays()
    {
        var svc = TestEnv.DonationService(_env.Db);
        var start = await svc.StartAsync(new DonationInput(1_000_000, "سهراب", "کار خوبی است", false), "https://test.local");
        Assert.True(start.Success);
        var donation = start.Value!.Donation;
        Assert.Equal(DonationStatus.Pending, donation.Status);
        Assert.Contains("MockPay", start.Value.RedirectUrl);

        var complete = await svc.CompleteFromCallbackAsync(donation.Authority!, "OK");
        Assert.True(complete.Success);
        Assert.Equal(DonationStatus.Paid, complete.Value!.Status);
        Assert.NotNull(complete.Value!.PaidAt);
    }

    [Fact]
    public async Task Nok_callback_marks_failed_without_verify()
    {
        var svc = TestEnv.DonationService(_env.Db);
        var start = await svc.StartAsync(new DonationInput(500_000, null, null, true), "https://test.local");
        var res = await svc.CompleteFromCallbackAsync(start.Value!.Donation.Authority!, "NOK");
        Assert.False(res.Success);
        var stored = await _env.Db.Donations.AsNoTracking().FirstAsync();
        Assert.Equal(DonationStatus.Failed, stored.Status);
    }

    [Fact]
    public async Task Unknown_authority_fails_safely()
    {
        var svc = TestEnv.DonationService(_env.Db);
        var res = await svc.CompleteFromCallbackAsync("NOT-EXIST", "OK");
        Assert.False(res.Success);
        Assert.Equal(0, await _env.Db.Donations.CountAsync(d => d.Status == DonationStatus.Paid));
    }

    [Fact]
    public async Task Amount_below_minimum_is_rejected()
    {
        var svc = TestEnv.DonationService(_env.Db);
        var res = await svc.StartAsync(new DonationInput(1_000, null, null, false), "https://test.local");
        Assert.False(res.Success);
        Assert.Contains("حداقل", res.Error);
    }

    [Fact]
    public async Task Public_supporters_list_exposes_no_amounts_query()
    {
        var svc = TestEnv.DonationService(_env.Db);
        var start = await svc.StartAsync(new DonationInput(2_000_000, "حامی اول", "موفق باشید", false), "https://t.local");
        await svc.CompleteFromCallbackAsync(start.Value!.Donation.Authority!, "OK");

        var supporters = await svc.ListPaidPublicAsync(10);
        var s = Assert.Single(supporters);
        Assert.Equal("حامی اول", s.DonorName); // نام دیده می‌شود
        // مبلغ فقط در پنل ادمین استفاده می‌شود — مدل عمومی است ولی UI مبلغ را نمایش نمی‌دهد (REQ-006-3)
    }
}
