using WorldOfGames.Core.Common;
using WorldOfGames.Core.Entities;

namespace WorldOfGames.Core.Interfaces;

// ─────────────────────────── بسته آپلود بازی ───────────────────────────

/// <summary>اعتبارسنجی machine-checkable استاندارد آپلود (REQ-004). هیچ I/O فایل سیستم انجام نمی‌دهد.</summary>
public interface IGamePackageValidator
{
    /// <summary>بسته ZIP را از روی Stream بررسی می‌کند: index.html ریشه، whitelist پسوند، ممنوعیت path traversal، سقف حجم فشرده/نافشرده و تعداد فایل.</summary>
    PackageValidationResult Validate(Stream zipStream, long compressedLength);
}

public record SubmitGameInput(
    string Title,
    string Description,
    string? Instructions,
    string Category,
    string TagsCsv,
    Stream ZipStream,
    long ZipLength,
    Stream? CoverStream,
    string? CoverFileName,
    long CoverLength,
    string DeveloperUserId,
    string DeveloperName,
    string WebRootPath);

// ─────────────────────────── بازی‌ها ───────────────────────────

public interface IGameService
{
    /// <summary>لیست عمومی: فقط Approved && IsEnabled؛ جست‌وجوی عنوان؛ sort: newest | popular.</summary>
    Task<PagedResult<GameListItem>> ListPublishedAsync(string? q, string? sort, int page, int pageSize);
    Task<Game?> GetPublishedBySlugAsync(string slug);
    Task<Game?> GetBySlugAsync(string slug);
    Task<Game?> GetByIdAsync(int id);
    Task IncrementPlayAsync(int id);
    /// <summary>اعتبارسنجی کامل + ذخیره کاور + استخراج امن ZIP → ثبت درخواست Pending.</summary>
    Task<OpResult<Game>> SubmitAsync(SubmitGameInput input);
    Task<PagedResult<Game>> ListAdminAsync(GameStatus? status, int page, int pageSize);
    Task<OpResult> ApproveAsync(int id, string actor, AuditSource source);
    /// <summary>رد بدون دلیل مجاز نیست (REQ-007-1).</summary>
    Task<OpResult> RejectAsync(int id, string reason, string actor, AuditSource source);
    Task<OpResult> SetEnabledAsync(int id, bool enabled, string actor, AuditSource source);
    Task<int> CountByStatusAsync(GameStatus status);
}

public record GameListItem(int Id, string Slug, string Title, string Category, string TagsCsv,
    string CoverPath, string DeveloperName, long PlayCount, DateTime SubmittedAt);

// ─────────────────────────── وبلاگ ───────────────────────────

public record BlogPostInput(string Title, string? SlugHint, string Excerpt, string Markdown,
    string? TagsCsv, string? MetaTitle, string? MetaDescription, bool IsPublished,
    string? CoverPath, string AuthorName);

public interface IBlogService
{
    Task<PagedResult<BlogPost>> ListPublishedAsync(int page, int pageSize, string? tag = null);
    Task<BlogPost?> GetPublishedBySlugAsync(string slug);
    Task<IReadOnlyList<BlogPost>> ListRelatedAsync(int postId, string? tagsCsv, int count);
    Task<IReadOnlyList<BlogPost>> ListPublishedAllAsync(); // sitemap
    Task<IReadOnlyList<string>> ListPublishedTagsAsync(int count);
    Task IncrementViewsAsync(int id);
    Task<PagedResult<BlogPost>> ListAdminAsync(int page, int pageSize);
    Task<BlogPost?> GetByIdAsync(int id);
    /// <summary>Markdown → HTML امن (raw HTML غیرفعال) + slug یکتا.</summary>
    Task<OpResult<BlogPost>> CreateAsync(BlogPostInput input);
    Task<OpResult<BlogPost>> UpdateAsync(int id, BlogPostInput input);
    Task<OpResult> SetPublishedAsync(int id, bool published, string actor);
    Task<OpResult> DeleteAsync(int id, string actor);
}

// ─────────────────────────── دونیت ───────────────────────────

public record GatewayRequestResult(bool Success, string? RedirectUrl, string? Authority, string? Error);
public record GatewayVerifyResult(bool Success, string? RefId, string? Error);

/// <summary>قرارداد دروازه پرداخت — پیاده‌سازی‌ها DB را لمس نمی‌کنند (plan.md Contracts).</summary>
public interface IDonationGateway
{
    string Name { get; }
    Task<GatewayRequestResult> CreatePaymentAsync(long amountRial, string callbackUrl, string description);
    Task<GatewayVerifyResult> VerifyAsync(string authority, long amountRial);
}

public record DonationInput(long AmountRial, string? DonorName, string? Message, bool IsAnonymous);

public record DonationStart(Donation Donation, string RedirectUrl);

public interface IDonationService
{
    /// <summary>ایجاد Pending + گرفتن لینک پرداخت از دروازه فعال کانفیگ.</summary>
    Task<OpResult<DonationStart>> StartAsync(DonationInput input, string callbackBaseUrl);
    /// <summary>callback دروازه: gatewayStatus=«NOK» → Failed بدون Verify؛ در غیر این‌صورت Verify سمت سرور؛ مبلغ/Authority نامعتبر → Failed (REQ-006-2).</summary>
    Task<OpResult<Donation>> CompleteFromCallbackAsync(string authority, string? gatewayStatus);
    Task<Donation?> GetByAuthorityAsync(string authority);
    Task<PagedResult<Donation>> ListAdminAsync(int page, int pageSize);
    /// <summary>حامیان برای نمایش عمومی — بدون مبلغ فردی (REQ-006-3).</summary>
    Task<IReadOnlyList<Donation>> ListPaidPublicAsync(int count);
    Task<long> SumPaidAsync();
    Task<int> CountPaidAsync();
}

// ─────────────────────────── Audit ───────────────────────────

public interface IAuditService
{
    Task LogAsync(AuditSource source, string actor, string action, string entityType, string entityId, string? detail = null);
    Task<PagedResult<AuditEntry>> ListAsync(int page, int pageSize);
}
