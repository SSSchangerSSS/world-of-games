using System.Globalization;
using System.Text;
using System.Xml.Linq;
using Microsoft.AspNetCore.Mvc;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Web.Models;

namespace WorldOfGames.Web.Controllers;

[Route("blog")]
public class BlogController(IBlogService blog) : Controller
{
    [HttpGet("")]
    public async Task<IActionResult> Index(int page = 1, string? tag = null)
    {
        var result = await blog.ListPublishedAsync(page, 9, tag);
        return View(new BlogIndexVm(result, tag));
    }

    [HttpGet("{slug}")]
    public async Task<IActionResult> Details(string slug)
    {
        var post = await blog.GetPublishedBySlugAsync(slug);
        if (post is null) return NotFound();
        var related = await blog.ListRelatedAsync(post.Id, post.TagsCsv, 3);
        await blog.IncrementViewsAsync(post.Id);
        return View(new BlogDetailsVm(post, related));
    }

    /// <summary>RSS feed (REQ-005-3)</summary>
    [HttpGet("feed.xml")]
    public async Task<IActionResult> Feed()
    {
        var base_ = Request.Scheme + "://" + Request.Host;
        var posts = await blog.ListPublishedAsync(1, 20);
        var channel = new XElement("channel",
            new XElement("title", "وبلاگ World of Games"),
            new XElement("link", base_ + "/blog"),
            new XElement("description", "اخبار و آموزش‌های پلتفرم بازی‌های تحت وب ایران"),
            new XElement("language", "fa"));
        foreach (var p in posts.Items)
        {
            channel.Add(new XElement("item",
                new XElement("title", p.Title),
                new XElement("link", base_ + "/blog/" + p.Slug),
                new XElement("guid", base_ + "/blog/" + p.Slug),
                new XElement("pubDate", (p.PublishedAt ?? p.CreatedAt).ToString("r", CultureInfo.InvariantCulture)),
                new XElement("description", p.Excerpt)));
        }
        var rss = new XDocument(new XDeclaration("1.0", "utf-8", null),
            new XElement("rss", new XAttribute("version", "2.0"), channel));
        return Content(rss.Declaration + Environment.NewLine + rss, "application/rss+xml", Encoding.UTF8);
    }
}
