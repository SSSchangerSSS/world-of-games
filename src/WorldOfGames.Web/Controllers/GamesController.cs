using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Web.Models;

namespace WorldOfGames.Web.Controllers;

[Route("games")]
public class GamesController(IGameService games) : Controller
{
    [HttpGet("")]
    public async Task<IActionResult> Index(string? q, string? sort, int page = 1)
    {
        var result = await games.ListPublishedAsync(q, sort, page, 12);
        return View(new GameIndexVm(q, sort, result));
    }

    [HttpGet("{slug}")]
    public async Task<IActionResult> Details(string slug)
    {
        var game = await games.GetPublishedBySlugAsync(slug); // REQ-003-2: غیرفعال/ردشده → 404
        if (game is null) return NotFound();
        var canEdit = User.IsInRole("Admin");
        return View(new GameDetailsVm(game, canEdit));
    }

    [HttpGet("{slug}/play")]
    public async Task<IActionResult> Play(string slug)
    {
        var game = await games.GetPublishedBySlugAsync(slug);
        if (game is null) return NotFound();
        await games.IncrementPlayAsync(game.Id);
        return View(new PlayVm(game));
    }

    // ── درخواست آپلود (REQ-004) ──
    [HttpGet("submit")]
    [Authorize]
    public IActionResult Submit() => View(new SubmitGameVm());

    [HttpPost("submit")]
    [Authorize]
    [ValidateAntiForgeryToken]
    [RequestSizeLimit(55_000_000)]
    public async Task<IActionResult> Submit(SubmitGameVm vm, IFormFile? zip, IFormFile? cover)
    {
        if (zip is null || zip.Length == 0)
            return View(vm with { Errors = ["فایل ZIP بازی الزامی است."] });
        if (cover is null || cover.Length == 0)
            return View(vm with { Errors = ["تصویر کاور الزامی است."] });

        var webRoot = HttpContext.RequestServices.GetRequiredService<IWebHostEnvironment>().WebRootPath
                      ?? Path.Combine(AppContext.BaseDirectory, "wwwroot");

        await using var zipStream = zip.OpenReadStream();
        await using var coverStream = cover.OpenReadStream();
        var input = new SubmitGameInput(
            vm.Title, vm.Description, vm.Instructions, vm.Category, vm.TagsCsv ?? "",
            zipStream, zip.Length, coverStream, cover.FileName, cover.Length,
            User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "",
            User.Identity?.Name ?? "توسعه‌دهنده",
            webRoot);

        var result = await games.SubmitAsync(input);
        if (!result.Success)
            return View(vm with { Errors = result.Errors ?? [result.Error ?? "خطای نامشخص."] });

        TempData["Ok"] = "درخواست انتشار بازی شما ثبت شد و پس از بررسی ادمین در کاتالوگ قرار می‌گیرد.";
        return RedirectToAction("Index");
    }
}
