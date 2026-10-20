using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;
using WorldOfGames.Web.Models;

namespace WorldOfGames.Web.Controllers;

[Route("admin")]
[Authorize(Roles = "Admin")]
public class AdminController(IGameService games, IBlogService blog, IDonationService donations,
    IAuditService audit, UserManager<ApplicationUser> users) : Controller
{
    private string Actor => User.Identity?.Name ?? "admin";

    // ── Dashboard (REQ-007) ──
    [HttpGet("")]
    public async Task<IActionResult> Dashboard()
    {
        var vm = new AdminDashboardVm(
            PendingGames: await games.CountByStatusAsync(GameStatus.Pending),
            ApprovedGames: await games.CountByStatusAsync(GameStatus.Approved),
            RejectedGames: await games.CountByStatusAsync(GameStatus.Rejected),
            TotalUsers: await users.Users.CountAsync(),
            SumPaidRial: await donations.SumPaidAsync(),
            PaidDonations: await donations.CountPaidAsync(),
            PublishedPosts: (await blog.ListPublishedAllAsync()).Count,
            LatestPending: (await games.ListAdminAsync(GameStatus.Pending, 1, 5)).Items);
        return View(vm);
    }

    // ── Games moderation ──
    [HttpGet("games")]
    public async Task<IActionResult> Games(string? status, int page = 1)
    {
        var parsed = status?.ToLowerInvariant() switch
        {
            "pending" => GameStatus.Pending,
            "approved" => GameStatus.Approved,
            "rejected" => GameStatus.Rejected,
            _ => (GameStatus?)null
        };
        var result = await games.ListAdminAsync(parsed, page, 20);
        ViewBag.Filter = status;
        return View(result);
    }

    [HttpPost("games/{id:int}/approve")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Approve(int id)
    {
        var res = await games.ApproveAsync(id, Actor, AuditSource.Web);
        TempData[res.Success ? "Ok" : "Err"] = res.Success ? "بازی تأیید شد." : res.Error;
        return RedirectToAction("Games");
    }

    [HttpPost("games/{id:int}/reject")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Reject(int id, RejectGameVm vm)
    {
        // حتی اگر ModelState نامعتبر، دلیل اجباری است (REQ-007-1)
        if (!ModelState.IsValid)
        {
            TempData["Err"] = string.Join(" ", ModelState.Values
                .SelectMany(v => v.Errors).Select(e => e.ErrorMessage));
            return RedirectToAction("Games");
        }
        var res = await games.RejectAsync(id, vm.Reason, Actor, AuditSource.Web);
        TempData[res.Success ? "Ok" : "Err"] = res.Success ? "بازی با دلیل رد شد." : res.Error;
        return RedirectToAction("Games");
    }

    [HttpPost("games/{id:int}/toggle")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Toggle(int id, bool enabled)
    {
        var res = await games.SetEnabledAsync(id, enabled, Actor, AuditSource.Web);
        TempData[res.Success ? "Ok" : "Err"] = res.Success
            ? (enabled ? "بازی فعال شد." : "بازی غیرفعال شد.") : res.Error;
        return RedirectToAction("Games");
    }

    // ── Blog management ──
    [HttpGet("posts")]
    public async Task<IActionResult> Posts(int page = 1) => View(await blog.ListAdminAsync(page, 20));

    [HttpGet("posts/create")]
    public IActionResult PostCreate() => View("PostForm", new AdminPostFormVm());

    [HttpPost("posts/create")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> PostCreate(AdminPostFormVm vm)
    {
        if (!ModelState.IsValid) return View("PostForm", vm);
        var coverPath = await SaveCoverIfAnyAsync(vm);
        var res = await blog.CreateAsync(new BlogPostInput(vm.Title, vm.SlugHint, vm.Excerpt, vm.Markdown,
            vm.TagsCsv, vm.MetaTitle, vm.MetaDescription, vm.IsPublished, coverPath, Actor));
        if (!res.Success)
        {
            foreach (var e in res.Errors ?? [res.Error ?? ""]) ModelState.AddModelError(string.Empty, e);
            return View("PostForm", vm);
        }
        TempData["Ok"] = "پست ساخته شد.";
        return RedirectToAction("Posts");
    }

    [HttpGet("posts/{id:int}/edit")]
    public async Task<IActionResult> PostEdit(int id)
    {
        var post = await blog.GetByIdAsync(id);
        if (post is null) return NotFound();
        return View("PostForm", new AdminPostFormVm
        {
            Id = post.Id, Title = post.Title, SlugHint = post.Slug, Excerpt = post.Excerpt,
            TagsCsv = post.TagsCsv, MetaTitle = post.MetaTitle, MetaDescription = post.MetaDescription,
            IsPublished = post.IsPublished, ExistingCoverPath = post.CoverPath,
            Markdown = await DecodeHtmlToMarkdownAsync(post.ContentHtml)
        });
    }

    [HttpPost("posts/{id:int}/edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> PostEdit(int id, AdminPostFormVm vm)
    {
        if (!ModelState.IsValid) return View("PostForm", vm);
        var existing = await blog.GetByIdAsync(id);
        if (existing is null) return NotFound();
        var coverPath = await SaveCoverIfAnyAsync(vm) ?? vm.ExistingCoverPath;
        var res = await blog.UpdateAsync(id, new BlogPostInput(vm.Title, vm.SlugHint, vm.Excerpt, vm.Markdown,
            vm.TagsCsv, vm.MetaTitle, vm.MetaDescription, vm.IsPublished, coverPath, existing.AuthorDisplayName));
        if (!res.Success)
        {
            foreach (var e in res.Errors ?? [res.Error ?? ""]) ModelState.AddModelError(string.Empty, e);
            return View("PostForm", vm);
        }
        TempData["Ok"] = "پست به‌روزرسانی شد.";
        return RedirectToAction("Posts");
    }

    [HttpPost("posts/{id:int}/toggle")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> PostToggle(int id, bool published)
    {
        var res = await blog.SetPublishedAsync(id, published, Actor);
        TempData[res.Success ? "Ok" : "Err"] = res.Success ? "وضعیت انتشار تغییر کرد." : res.Error;
        return RedirectToAction("Posts");
    }

    [HttpPost("posts/{id:int}/delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> PostDelete(int id)
    {
        var res = await blog.DeleteAsync(id, Actor);
        TempData[res.Success ? "Ok" : "Err"] = res.Success ? "پست حذف شد." : res.Error;
        return RedirectToAction("Posts");
    }

    // ── Donations / Users / Audit ──
    [HttpGet("donations")]
    public async Task<IActionResult> Donations(int page = 1) => View(await donations.ListAdminAsync(page, 20));

    [HttpGet("users")]
    public IActionResult Users(int page = 1)
    {
        var items = users.Users.AsNoTracking().OrderByDescending(u => u.Id)
            .Skip((Math.Max(1, page) - 1) * 20).Take(20).ToList();
        return View(items);
    }

    [HttpGet("audit")]
    public async Task<IActionResult> Audit(int page = 1) => View(await audit.ListAsync(page, 30));

    // ── helpers ──
    private async Task<string?> SaveCoverIfAnyAsync(AdminPostFormVm vm)
    {
        if (vm.Cover is null || vm.Cover.Length == 0) return null;
        if (vm.Cover.Length > 2 * 1024 * 1024)
        {
            ModelState.AddModelError(string.Empty, "کاور حداکثر ۲ مگابایت است.");
            return null;
        }
        var ext = Path.GetExtension(vm.Cover.FileName).ToLowerInvariant();
        if (ext is not (".jpg" or ".jpeg" or ".png" or ".webp"))
        {
            ModelState.AddModelError(string.Empty, "کاور فقط JPG/PNG/WebP است.");
            return null;
        }
        var webRoot = HttpContext.RequestServices.GetRequiredService<IWebHostEnvironment>().WebRootPath
                      ?? Path.Combine(AppContext.BaseDirectory, "wwwroot");
        var covers = Path.Combine(webRoot, "media", "blog");
        Directory.CreateDirectory(covers);
        var name = $"post-{Guid.NewGuid():N}{(ext == ".jpeg" ? ".jpg" : ext)}";
        await using var fs = System.IO.File.Create(Path.Combine(covers, name));
        await vm.Cover.CopyToAsync(fs);
        return $"/media/blog/{name}";
    }

    /// <summary>برای ویرایش: HTML امن ذخیره‌شده را به Markdown برگردان — ساده: متن خام استخراج می‌شود تا نویسنده بازنویسی کند.</summary>
    private static Task<string> DecodeHtmlToMarkdownAsync(string html)
    {
        // MVP: برچسب‌های ساده به Markdown تبدیل می‌شوند؛ فاز بعد: ذخیره Markdown اصلی
        var md = html
            .Replace("<h2>", "## ").Replace("</h2>", "\n")
            .Replace("<h3>", "### ").Replace("</h3>", "\n")
            .Replace("<strong>", "**").Replace("</strong>", "**")
            .Replace("<em>", "*").Replace("</em>", "*")
            .Replace("<li>", "- ").Replace("</li>", "\n")
            .Replace("</ul>", "\n").Replace("</ol>", "\n")
            .Replace("<p>", "").Replace("</p>", "\n")
            .Replace("<br />", "\n").Replace("<br/>", "\n")
            .Replace("&amp;", "&").Replace("&lt;", "<").Replace("&gt;", ">").Replace("&quot;", "\"");
        return Task.FromResult(md.Trim());
    }
}
