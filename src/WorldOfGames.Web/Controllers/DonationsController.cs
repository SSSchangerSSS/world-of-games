using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Options;
using WorldOfGames.Infrastructure.Services;
using WorldOfGames.Web.Models;

namespace WorldOfGames.Web.Controllers;

[Route("donations")]
public class DonationsController(IDonationService donations, DonationGatewayFactory factory,
    IOptions<DonationGatewayOptions> gatewayOptions) : Controller
{
    [HttpGet("")]
    public async Task<IActionResult> Index()
    {
        var sum = await donations.SumPaidAsync();
        var count = await donations.CountPaidAsync();
        var recent = await donations.ListPaidPublicAsync(12); // بدون مبلغ فردی (REQ-006-3)
        var gatewayName = factory.Resolve(gatewayOptions.Value.Gateway).Name;
        return View(new DonationIndexVm(sum, count, recent, gatewayName));
    }

    [HttpPost("start")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Start(long? amountRial, long? amountCustom, string? donorName, string? message, bool isAnonymous)
    {
        // فیلد دلخواه (تومان) در صورت ورود، بر پیش‌فرض‌های ریالی اولویت دارد
        var effectiveRial = amountCustom is > 0 ? amountCustom.Value * 10 : amountRial ?? 0;
        var baseUrl = Request.Scheme + "://" + Request.Host.ToString();
        var result = await donations.StartAsync(new DonationInput(effectiveRial, donorName, message, isAnonymous), baseUrl);
        if (!result.Success || result.Value is null)
        {
            TempData["DonationError"] = result.Error ?? "ایجاد پرداخت ناموفق بود.";
            return RedirectToAction("Index");
        }
        // Mock → ~/ محلی؛ Zarinpal → URL مطلق دروازه
        var url = result.Value.RedirectUrl;
        return Redirect(url.StartsWith("~/", StringComparison.Ordinal) ? Url.Content(url) : url);
    }

    /// <summary>صفحه پرداخت آزمایشی Mock — فقط جریان توسعه/تست (D-07/KI-3)؛ فقط برای Authorityهای MOCK*.</summary>
    [HttpGet("mockpay")]
    public IActionResult MockPay(string? authority, long amount)
    {
        if (string.IsNullOrEmpty(authority) || !authority.StartsWith("MOCK", StringComparison.Ordinal))
            return NotFound();
        ViewBag.Authority = authority;
        ViewBag.AmountToman = DisplayHelper.Toman(amount);
        return View();
    }

    [HttpPost("mockpay/complete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> MockPayComplete(string? authority, bool succeed)
    {
        if (string.IsNullOrEmpty(authority) || !authority.StartsWith("MOCK", StringComparison.Ordinal))
            return NotFound();
        var result = await donations.CompleteFromCallbackAsync(authority, succeed ? "OK" : "NOK");
        return RedirectToAction("Result", new { authority, ok = result.Success });
    }

    /// <summary>callback زرین‌پال: ?Authority=…&amp;Status=OK|NOK</summary>
    [HttpGet("callback")]
    public async Task<IActionResult> Callback(string? authority, string? status)
    {
        if (string.IsNullOrWhiteSpace(authority))
            return RedirectToAction("Index");
        var result = await donations.CompleteFromCallbackAsync(authority, status);
        return RedirectToAction("Result", new { authority, ok = result.Success });
    }

    [HttpGet("result")]
    public async Task<IActionResult> Result(string? authority, bool ok = false)
    {
        var donation = string.IsNullOrWhiteSpace(authority) ? null : await donations.GetByAuthorityAsync(authority);
        var paid = donation?.Status == DonationStatus.Paid;
        return View(new DonationResultVm(donation, paid, paid ? null : "پرداخت ناموفق بود یا لغو شد."));
    }
}
