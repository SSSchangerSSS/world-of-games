using System.IO.Compression;
using Microsoft.Extensions.Logging;
using Microsoft.EntityFrameworkCore;
using WorldOfGames.Core.Common;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;

namespace WorldOfGames.Infrastructure.Services;

public sealed class EfGameService(AppDbContext db, IGamePackageValidator validator, ILogger<EfGameService> logger) : IGameService
{
    private const int DefaultPageSize = 12;

    public async Task<PagedResult<GameListItem>> ListPublishedAsync(string? q, string? sort, int page, int pageSize)
    {
        page = Math.Max(1, page);
        pageSize = pageSize is > 0 and <= 48 ? pageSize : DefaultPageSize;
        var query = db.Games.AsNoTracking()
            .Where(g => g.Status == GameStatus.Approved && g.IsEnabled);
        if (!string.IsNullOrWhiteSpace(q))
            query = query.Where(g => g.Title.Contains(q) || g.Category.Contains(q) || g.TagsCsv.Contains(q));
        query = sort == "popular" ? query.OrderByDescending(g => g.PlayCount).ThenByDescending(g => g.Id)
                                  : query.OrderByDescending(g => g.SubmittedAt).ThenByDescending(g => g.Id);
        var total = await query.CountAsync();
        var items = await query.Skip((page - 1) * pageSize).Take(pageSize)
            .Select(g => new GameListItem(g.Id, g.Slug, g.Title, g.Category, g.TagsCsv, g.CoverPath,
                g.DeveloperName, g.PlayCount, g.SubmittedAt))
            .ToListAsync();
        return new PagedResult<GameListItem>(items, total, page, pageSize);
    }

    public Task<Game?> GetPublishedBySlugAsync(string slug) =>
        db.Games.AsNoTracking().FirstOrDefaultAsync(g => g.Slug == slug && g.Status == GameStatus.Approved && g.IsEnabled);

    public Task<Game?> GetBySlugAsync(string slug) => db.Games.AsNoTracking().FirstOrDefaultAsync(g => g.Slug == slug);
    public Task<Game?> GetByIdAsync(int id) => db.Games.AsNoTracking().FirstOrDefaultAsync(g => g.Id == id);

    public async Task IncrementPlayAsync(int id)
    {
        await db.Games.Where(g => g.Id == id).ExecuteUpdateAsync(s => s.SetProperty(g => g.PlayCount, g => g.PlayCount + 1));
    }

    public async Task<OpResult<Game>> SubmitAsync(SubmitGameInput input)
    {
        var errors = new List<string>();

        // ۱) اعتبارسنجی متادیتا
        if (string.IsNullOrWhiteSpace(input.Title) || input.Title.Trim().Length < 3 || input.Title.Trim().Length > 120)
            errors.Add("عنوان بازی باید بین ۳ تا ۱۲۰ نویسه باشد.");
        if (string.IsNullOrWhiteSpace(input.Description) || input.Description.Trim().Length < 20)
            errors.Add("توضیحات بازی باید حداقل ۲۰ نویسه باشد.");
        if (string.IsNullOrWhiteSpace(input.Category)) errors.Add("دسته‌بندی بازی الزامی است.");
        if (string.IsNullOrWhiteSpace(input.DeveloperUserId)) errors.Add("برای ارسال بازی باید وارد حساب خود شوید.");
        if (input.ZipLength <= 0) errors.Add("فایل ZIP بازی الزامی است.");
        if (input.CoverStream is null || input.CoverLength <= 0) errors.Add("تصویر کاور الزامی است.");

        // ۲) اعتبارسنجی کاور
        var coverExt = Path.GetExtension(input.CoverFileName ?? "").ToLowerInvariant();
        if (input.CoverStream is not null && input.CoverLength > 0)
        {
            if (coverExt is not (".jpg" or ".jpeg" or ".png" or ".webp"))
                errors.Add("کاور فقط JPG/PNG/WebP است.");
        }

        // ۳) اعتبارسنجی بسته ZIP (استاندارد آپلود)
        PackageValidationResult? pkg = null;
        if (input.ZipStream is not null && input.ZipLength > 0)
        {
            pkg = validator.Validate(input.ZipStream, input.ZipLength);
            if (!pkg.Success) errors.AddRange(pkg.Errors);
        }

        if (errors.Count > 0) return OpResult<Game>.Fail(errors);

        // ۴) slug یکتا + ذخیره کاور + استخراج امن
        var slug = SlugHelper.Slugify(input.Title);
        if (await db.Games.AnyAsync(g => g.Slug == slug)) slug = SlugHelper.WithSuffix(slug);

        try
        {
            var gamesRoot = Path.Combine(input.WebRootPath, "media", "games", slug);
            Directory.CreateDirectory(gamesRoot);
            var coversRoot = Path.Combine(input.WebRootPath, "media", "covers");
            Directory.CreateDirectory(coversRoot);

            var coverExt2 = coverExt is ".jpeg" ? ".jpg" : coverExt;
            var coverName = $"{slug}{coverExt2}";
            input.CoverStream!.Position = 0;
            await using (var fs = File.Create(Path.Combine(coversRoot, coverName)))
                await input.CoverStream.CopyToAsync(fs);

            input.ZipStream!.Position = 0;
            ExtractSecurely(input.ZipStream, gamesRoot);

            var game = new Game
            {
                Slug = slug,
                Title = input.Title.Trim(),
                Description = input.Description.Trim(),
                Instructions = input.Instructions?.Trim(),
                Category = input.Category.Trim(),
                TagsCsv = (input.TagsCsv ?? "").Trim(),
                CoverPath = $"/media/covers/{coverName}",
                EntryPath = $"/media/games/{slug}/index.html",
                Status = GameStatus.Pending,
                DeveloperUserId = input.DeveloperUserId,
                DeveloperName = string.IsNullOrWhiteSpace(input.DeveloperName) ? "توسعه‌دهنده" : input.DeveloperName.Trim()
            };
            db.Games.Add(game);
            await db.SaveChangesAsync();
            return OpResult<Game>.Ok(game);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Game submit failed for {Title}", input.Title);
            try { Directory.Delete(Path.Combine(input.WebRootPath, "media", "games", slug), recursive: true); } catch { }
            return OpResult<Game>.Fail("در ذخیره‌سازی بسته بازی خطایی رخ داد. لطفاً دوباره تلاش کنید.");
        }
    }

    /// <summary>استخراج با دفاع دوم در برابر zip-slip (اعتبارسنج اول دفاع اول است) — مستقیم از Stream بدون فایل موقت.</summary>
    private static void ExtractSecurely(Stream zipSource, string targetRoot)
    {
        using var archive = new ZipArchive(zipSource, ZipArchiveMode.Read, leaveOpen: true);
        var root = Path.GetFullPath(targetRoot);
        foreach (var entry in archive.Entries)
        {
            if (ZipGamePackageValidator.IsJunk(entry.FullName)) continue;
            var destPath = Path.GetFullPath(Path.Combine(root, entry.FullName.Replace('\\', '/')));
            if (!destPath.StartsWith(root + Path.DirectorySeparatorChar, StringComparison.Ordinal) &&
                !string.Equals(destPath, root, StringComparison.Ordinal))
                throw new IOException($"مسیر ناامن در بسته: {entry.FullName}");
            if (string.IsNullOrEmpty(entry.Name)) // فقط دایرکتوری
            {
                Directory.CreateDirectory(destPath);
                continue;
            }
            Directory.CreateDirectory(Path.GetDirectoryName(destPath)!);
            entry.ExtractToFile(destPath, overwrite: true);
        }
    }

    public async Task<PagedResult<Game>> ListAdminAsync(GameStatus? status, int page, int pageSize)
    {
        page = Math.Max(1, page);
        pageSize = pageSize is > 0 and <= 100 ? pageSize : 20;
        var query = db.Games.AsNoTracking().AsQueryable();
        if (status.HasValue) query = query.Where(g => g.Status == status.Value);
        query = query.OrderByDescending(g => g.SubmittedAt).ThenByDescending(g => g.Id);
        var total = await query.CountAsync();
        var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
        return new PagedResult<Game>(items, total, page, pageSize);
    }

    public async Task<OpResult> ApproveAsync(int id, string actor, AuditSource source)
    {
        var game = await db.Games.FirstOrDefaultAsync(g => g.Id == id);
        if (game is null) return OpResult.Fail("بازی یافت نشد.");
        if (game.Status == GameStatus.Approved) return OpResult.Fail("این بازی قبلاً تأیید شده است.");
        game.Status = GameStatus.Approved;
        game.IsEnabled = true;
        game.RejectionReason = null;
        game.ReviewedAt = DateTime.UtcNow;
        game.ReviewedBy = actor;
        await db.SaveChangesAsync();
        await LogAudit(source, actor, "GameApprove", id, $"«{game.Title}» تأیید شد");
        return OpResult.Ok();
    }

    public async Task<OpResult> RejectAsync(int id, string reason, string actor, AuditSource source)
    {
        if (string.IsNullOrWhiteSpace(reason) || reason.Trim().Length < 5)
            return OpResult.Fail("ذکر دلیل رد (حداقل ۵ نویسه) الزامی است."); // REQ-007-1
        var game = await db.Games.FirstOrDefaultAsync(g => g.Id == id);
        if (game is null) return OpResult.Fail("بازی یافت نشد.");
        game.Status = GameStatus.Rejected;
        game.IsEnabled = false;
        game.RejectionReason = reason.Trim();
        game.ReviewedAt = DateTime.UtcNow;
        game.ReviewedBy = actor;
        await db.SaveChangesAsync();
        await LogAudit(source, actor, "GameReject", id, $"«{game.Title}» رد شد: {reason.Trim()}");
        return OpResult.Ok();
    }

    public async Task<OpResult> SetEnabledAsync(int id, bool enabled, string actor, AuditSource source)
    {
        var game = await db.Games.FirstOrDefaultAsync(g => g.Id == id);
        if (game is null) return OpResult.Fail("بازی یافت نشد.");
        if (game.Status != GameStatus.Approved) return OpResult.Fail("فقط بازی‌های تأییدشده قابل فعال/غیرفعال‌سازی هستند.");
        game.IsEnabled = enabled;
        await db.SaveChangesAsync();
        await LogAudit(source, actor, "GameToggle", id, $"«{game.Title}» {(enabled ? "فعال" : "غیرفعال")} شد");
        return OpResult.Ok();
    }

    public Task<int> CountByStatusAsync(GameStatus status) =>
        db.Games.AsNoTracking().CountAsync(g => g.Status == status);

    private async Task LogAudit(AuditSource source, string actor, string action, int gameId, string detail)
    {
        await db.AuditEntries.AddAsync(new AuditEntry
        {
            Source = source, Actor = actor, Action = action,
            EntityType = "Game", EntityId = gameId.ToString(), Detail = detail
        });
        await db.SaveChangesAsync();
    }
}
