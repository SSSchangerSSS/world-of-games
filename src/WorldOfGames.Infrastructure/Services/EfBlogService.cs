using Markdig;
using Microsoft.EntityFrameworkCore;
using WorldOfGames.Core.Common;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;

namespace WorldOfGames.Infrastructure.Services;

public sealed class EfBlogService(AppDbContext db) : IBlogService
{
    // امن‌سازی: raw HTML ورودی کاملاً غیرفعال (plan.md Contracts)
    private static readonly MarkdownPipeline Pipeline = new MarkdownPipelineBuilder()
        .UseAdvancedExtensions()
        .DisableHtml()
        .Build();

    private const int DefaultPageSize = 9;

    public async Task<PagedResult<BlogPost>> ListPublishedAsync(int page, int pageSize, string? tag = null)
    {
        page = Math.Max(1, page);
        pageSize = pageSize is > 0 and <= 50 ? pageSize : DefaultPageSize;
        var query = db.BlogPosts.AsNoTracking().Where(p => p.IsPublished);
        if (!string.IsNullOrWhiteSpace(tag))
            query = query.Where(p => p.TagsCsv.Contains(tag));
        query = query.OrderByDescending(p => p.PublishedAt).ThenByDescending(p => p.Id);
        var total = await query.CountAsync();
        var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
        return new PagedResult<BlogPost>(items, total, page, pageSize);
    }

    public Task<BlogPost?> GetPublishedBySlugAsync(string slug) =>
        db.BlogPosts.AsNoTracking().FirstOrDefaultAsync(p => p.Slug == slug && p.IsPublished);

    /// <summary>پست‌های مرتبط = تگ مشترک (D-12) — خود پست حذف می‌شود (REQ-005-4).</summary>
    public async Task<IReadOnlyList<BlogPost>> ListRelatedAsync(int postId, string? tagsCsv, int count)
    {
        var tags = ParseTags(tagsCsv);
        if (tags.Count == 0) return [];
        var candidates = await db.BlogPosts.AsNoTracking()
            .Where(p => p.IsPublished && p.Id != postId)
            .OrderByDescending(p => p.PublishedAt)
            .Take(100)
            .ToListAsync();
        return candidates
            .Select(p => (Post: p, Score: ParseTags(p.TagsCsv).Count(tags.Contains)))
            .Where(x => x.Score > 0)
            .OrderByDescending(x => x.Score).ThenByDescending(x => x.Post.PublishedAt)
            .Take(count)
            .Select(x => x.Post)
            .ToList();
    }

    public async Task<IReadOnlyList<BlogPost>> ListPublishedAllAsync() =>
        await db.BlogPosts.AsNoTracking().Where(p => p.IsPublished)
            .OrderByDescending(p => p.PublishedAt).ToListAsync();

    public async Task<IReadOnlyList<string>> ListPublishedTagsAsync(int count)
    {
        var posts = await db.BlogPosts.AsNoTracking().Where(p => p.IsPublished)
            .Select(p => p.TagsCsv).ToListAsync();
        return posts.SelectMany(ParseTags).Distinct().Take(count).ToList();
    }

    public async Task IncrementViewsAsync(int id) =>
        await db.BlogPosts.Where(p => p.Id == id).ExecuteUpdateAsync(s => s.SetProperty(p => p.Views, p => p.Views + 1));

    public async Task<PagedResult<BlogPost>> ListAdminAsync(int page, int pageSize)
    {
        page = Math.Max(1, page);
        pageSize = pageSize is > 0 and <= 50 ? pageSize : 20;
        var query = db.BlogPosts.AsNoTracking().OrderByDescending(p => p.UpdatedAt).ThenByDescending(p => p.Id);
        var total = await query.CountAsync();
        var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
        return new PagedResult<BlogPost>(items, total, page, pageSize);
    }

    public Task<BlogPost?> GetByIdAsync(int id) => db.BlogPosts.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id);

    public async Task<OpResult<BlogPost>> CreateAsync(BlogPostInput input)
    {
        var errors = ValidateInput(input);
        if (errors.Count > 0) return OpResult<BlogPost>.Fail(errors);

        var slug = await UniqueSlugAsync(SlugHelper.Slugify(string.IsNullOrWhiteSpace(input.SlugHint) ? input.Title : input.SlugHint));
        var post = new BlogPost
        {
            Slug = slug,
            Title = input.Title.Trim(),
            Excerpt = (input.Excerpt ?? "").Trim(),
            ContentHtml = Markdown.ToHtml(input.Markdown ?? "", Pipeline),
            CoverPath = input.CoverPath,
            TagsCsv = (input.TagsCsv ?? "").Trim(),
            MetaTitle = input.MetaTitle?.Trim(),
            MetaDescription = input.MetaDescription?.Trim(),
            IsPublished = input.IsPublished,
            PublishedAt = input.IsPublished ? DateTime.UtcNow : null,
            AuthorDisplayName = string.IsNullOrWhiteSpace(input.AuthorName) ? "تیم World of Games" : input.AuthorName.Trim()
        };
        db.BlogPosts.Add(post);
        await db.SaveChangesAsync();
        return OpResult<BlogPost>.Ok(post);
    }

    public async Task<OpResult<BlogPost>> UpdateAsync(int id, BlogPostInput input)
    {
        var post = await db.BlogPosts.FirstOrDefaultAsync(p => p.Id == id);
        if (post is null) return OpResult<BlogPost>.Fail("پست یافت نشد.");
        var errors = ValidateInput(input);
        if (errors.Count > 0) return OpResult<BlogPost>.Fail(errors);

        var newSlug = SlugHelper.Slugify(string.IsNullOrWhiteSpace(input.SlugHint) ? input.Title : input.SlugHint);
        if (newSlug != post.Slug) post.Slug = await UniqueSlugAsync(newSlug, excludeId: id);

        post.Title = input.Title.Trim();
        post.Excerpt = (input.Excerpt ?? "").Trim();
        post.ContentHtml = Markdown.ToHtml(input.Markdown ?? "", Pipeline);
        post.CoverPath = input.CoverPath;
        post.TagsCsv = (input.TagsCsv ?? "").Trim();
        post.MetaTitle = input.MetaTitle?.Trim();
        post.MetaDescription = input.MetaDescription?.Trim();
        post.UpdatedAt = DateTime.UtcNow;
        if (input.IsPublished && !post.IsPublished)
        {
            post.IsPublished = true;
            post.PublishedAt = DateTime.UtcNow;
        }
        else if (!input.IsPublished) post.IsPublished = false;
        await db.SaveChangesAsync();
        return OpResult<BlogPost>.Ok(post);
    }

    public async Task<OpResult> SetPublishedAsync(int id, bool published, string actor)
    {
        var post = await db.BlogPosts.FirstOrDefaultAsync(p => p.Id == id);
        if (post is null) return OpResult.Fail("پست یافت نشد.");
        post.IsPublished = published;
        post.PublishedAt ??= published ? DateTime.UtcNow : null;
        post.UpdatedAt = DateTime.UtcNow;
        await db.SaveChangesAsync();
        await db.AuditEntries.AddAsync(new AuditEntry
        {
            Source = AuditSource.Web, Actor = actor, Action = published ? "PostPublish" : "PostUnpublish",
            EntityType = "BlogPost", EntityId = id.ToString(), Detail = $"«{post.Title}»"
        });
        await db.SaveChangesAsync();
        return OpResult.Ok();
    }

    public async Task<OpResult> DeleteAsync(int id, string actor)
    {
        var post = await db.BlogPosts.FirstOrDefaultAsync(p => p.Id == id);
        if (post is null) return OpResult.Fail("پست یافت نشد.");
        db.BlogPosts.Remove(post);
        await db.SaveChangesAsync();
        await db.AuditEntries.AddAsync(new AuditEntry
        {
            Source = AuditSource.Web, Actor = actor, Action = "PostDelete",
            EntityType = "BlogPost", EntityId = id.ToString(), Detail = $"«{post.Title}» حذف شد"
        });
        await db.SaveChangesAsync();
        return OpResult.Ok();
    }

    // ── helpers ──
    private static List<string> ValidateInput(BlogPostInput input)
    {
        var errors = new List<string>();
        if (string.IsNullOrWhiteSpace(input.Title) || input.Title.Trim().Length < 3) errors.Add("عنوان پست الزامی است (حداقل ۳ نویسه).");
        if (string.IsNullOrWhiteSpace(input.Markdown) || input.Markdown.Trim().Length < 30) errors.Add("متن پست باید حداقل ۳۰ نویسه باشد.");
        if (string.IsNullOrWhiteSpace(input.Excerpt)) errors.Add("خلاصه پست برای سئو الزامی است.");
        return errors;
    }

    private async Task<string> UniqueSlugAsync(string baseSlug, int? excludeId = null)
    {
        var slug = baseSlug;
        var i = 2;
        while (await db.BlogPosts.AnyAsync(p => p.Slug == slug && (excludeId == null || p.Id != excludeId)))
            slug = $"{baseSlug}-{i++}";
        return slug;
    }

    internal static List<string> ParseTags(string? tagsCsv) =>
        (tagsCsv ?? "").Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Select(t => t.ToLowerInvariant()).Where(t => t.Length > 0).Distinct().ToList();
}
