using System.Globalization;
using System.Text;
using System.Xml.Linq;
using Microsoft.AspNetCore.Mvc;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Web.Models;

namespace WorldOfGames.Web.Controllers;

public class HomeController(IGameService games, IBlogService blog, IDonationService donations) : Controller
{
    [Route("")]
    public async Task<IActionResult> Index()
    {
        var featured = await games.ListPublishedAsync(q: null, sort: "popular", page: 1, pageSize: 6);
        var latest = await blog.ListPublishedAsync(page: 1, pageSize: 3);
        var sum = await donations.SumPaidAsync();
        var supporters = await donations.CountPaidAsync();
        ViewBag.SumPaidToman = DisplayHelper.Toman(sum);
        ViewBag.Supporters = DisplayHelper.Number(supporters);
        return View((featured, latest));
    }

    [HttpGet("sitemap.xml")]
    public async Task<IActionResult> Sitemap()
    {
        var base_ = Request.Scheme + "://" + Request.Host;
        var gamesAll = await games.ListPublishedAsync(null, null, 1, 48);
        var posts = await blog.ListPublishedAllAsync();

        var ns = XNamespace.Get("http://www.sitemaps.org/schemas/sitemap/0.9");
        var urls = new List<XElement>
        {
            new(ns + "url", new XElement(ns + "loc", base_ + "/"), new XElement(ns + "priority", "1.0")),
            new(ns + "url", new XElement(ns + "loc", base_ + "/games"), new XElement(ns + "priority", "0.9")),
            new(ns + "url", new XElement(ns + "loc", base_ + "/blog"), new XElement(ns + "priority", "0.8")),
            new(ns + "url", new XElement(ns + "loc", base_ + "/donations"), new XElement(ns + "priority", "0.5")),
            new(ns + "url", new XElement(ns + "loc", base_ + "/games/submit"), new XElement(ns + "priority", "0.5")),
        };
        foreach (var g in gamesAll.Items)
            urls.Add(new XElement(ns + "url", new XElement(ns + "loc", base_ + "/games/" + g.Slug), new XElement(ns + "priority", "0.8")));
        foreach (var p in posts)
            urls.Add(new XElement(ns + "url", new XElement(ns + "loc", base_ + "/blog/" + p.Slug),
                new XElement(ns + "lastmod", p.UpdatedAt.ToString("yyyy-MM-dd")), new XElement(ns + "priority", "0.7")));

        var doc = new XDocument(new XDeclaration("1.0", "utf-8", null), new XElement(ns + "urlset", urls));
        return Content(doc.Declaration + Environment.NewLine + doc, "application/xml", Encoding.UTF8);
    }

    [HttpGet("robots.txt")]
    public IActionResult Robots() =>
        Content("User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /Account\n\nSitemap: " +
                Request.Scheme + "://" + Request.Host + "/sitemap.xml", "text/plain");

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    [Route("Home/Error")]
    public IActionResult Error() => View();
}
