using Microsoft.Extensions.DependencyInjection;
using System.Net.Http.Json;
using System.Text.Json.Serialization;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Options;

namespace WorldOfGames.Infrastructure.Services;

/// <summary>دروازه Mock برای توسعه/تست — جریان کامل دونیت بدون پول واقعی (D-07).</summary>
public sealed class MockGateway : IDonationGateway
{
    public string Name => "Mock";

    public Task<GatewayRequestResult> CreatePaymentAsync(long amountRial, string callbackUrl, string description)
    {
        var authority = $"MOCK-{Guid.NewGuid():N}";
        var url = $"~/Donations/MockPay?authority={authority}&amount={amountRial}&cb={Uri.EscapeDataString(callbackUrl)}";
        return Task.FromResult(new GatewayRequestResult(true, url, authority, null));
    }

    public Task<GatewayVerifyResult> VerifyAsync(string authority, long amountRial)
    {
        // در Mock: هر Authority که با FAIL شروع نشود موفق است — برای تست مسیر ناموفق
        return Task.FromResult(authority.StartsWith("FAIL", StringComparison.Ordinal)
            ? new GatewayVerifyResult(false, null, "پرداخت ناموفق (Mock).")
            : new GatewayVerifyResult(true, $"RF{Random.Shared.Next(100000, 999999)}", null));
    }
}

/// <summary>پیاده‌سازی زرین‌پال API v4 (REQ-006-4) — آدرس‌ها کانفیگ‌پذیر.</summary>
public sealed partial class ZarinpalGateway(
    HttpClient http,
    IOptions<ZarinpalOptions> options,
    ILogger<ZarinpalGateway> logger) : IDonationGateway
{
    public string Name => "Zarinpal";

    public async Task<GatewayRequestResult> CreatePaymentAsync(long amountRial, string callbackUrl, string description)
    {
        try
        {
            var payload = new ZpRequest
            {
                MerchantId = options.Value.MerchantId,
                Amount = amountRial,
                CallbackUrl = callbackUrl,
                Description = Truncate(description, 255)
            };
            using var resp = await http.PostAsJsonAsync(options.Value.RequestUrl, payload);
            var body = await resp.Content.ReadFromJsonAsync<ZpResponse>();
            if (body?.Data is null || (body.Data.Code is not (100 or 101)) || string.IsNullOrEmpty(body.Data.Authority))
            {
                var msg = body?.Errors is { Count: > 0 } ? $"{body.Errors[0].Code}: {body.Errors[0].Message}" : "پاسخ نامعتبر درگاه.";
                logger.LogWarning("Zarinpal request failed: {Msg}", msg);
                return new GatewayRequestResult(false, null, null, "ایجاد پرداخت در دروازه ناموفق بود: " + msg);
            }
            var startPay = options.Value.StartPayUrl.TrimEnd('/') + "/" + body.Data.Authority;
            return new GatewayRequestResult(true, startPay, body.Data.Authority, null);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Zarinpal request exception");
            return new GatewayRequestResult(false, null, null, "ارتباط با دروازه پرداخت برقرار نشد.");
        }
    }

    public async Task<GatewayVerifyResult> VerifyAsync(string authority, long amountRial)
    {
        try
        {
            var payload = new ZpVerify { MerchantId = options.Value.MerchantId, Amount = amountRial, Authority = authority };
            using var resp = await http.PostAsJsonAsync(options.Value.VerifyUrl, payload);
            var body = await resp.Content.ReadFromJsonAsync<ZpResponse>();
            if (body?.Data is { Code: 100 or 101 })
                return new GatewayVerifyResult(true, body.Data.RefId?.ToString(), null);

            var msg = body?.Errors is { Count: > 0 } ? $"{body.Errors[0].Code}: {body.Errors[0].Message}" : "پرداخت تأیید نشد.";
            return new GatewayVerifyResult(false, null, msg);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Zarinpal verify exception");
            return new GatewayVerifyResult(false, null, "ارتباط با دروازه برای تأیید پرداخت برقرار نشد.");
        }
    }

    private static string Truncate(string s, int max) => s.Length <= max ? s : s[..max];

    private sealed class ZpRequest
    {
        [JsonPropertyName("merchant_id")] public string MerchantId { get; set; } = "";
        [JsonPropertyName("amount")] public long Amount { get; set; }
        [JsonPropertyName("callback_url")] public string CallbackUrl { get; set; } = "";
        [JsonPropertyName("description")] public string Description { get; set; } = "";
    }

    private sealed class ZpVerify
    {
        [JsonPropertyName("merchant_id")] public string MerchantId { get; set; } = "";
        [JsonPropertyName("amount")] public long Amount { get; set; }
        [JsonPropertyName("authority")] public string Authority { get; set; } = "";
    }

    private sealed class ZpResponse
    {
        [JsonPropertyName("data")] public ZpData? Data { get; set; }
        [JsonPropertyName("errors")] public List<ZpError>? Errors { get; set; }
    }

    private sealed class ZpData
    {
        [JsonPropertyName("code")] public int? Code { get; set; }
        [JsonPropertyName("authority")] public string? Authority { get; set; }
        [JsonPropertyName("ref_id")] public long? RefId { get; set; }
    }

    private sealed class ZpError
    {
        [JsonPropertyName("code")] public int? Code { get; set; }
        [JsonPropertyName("message")] public string? Message { get; set; }
    }
}

/// <summary>انتخاب دروازه فعال از کانفیگ Donations:Gateway = Mock | Zarinpal (D-07).</summary>
public sealed class DonationGatewayFactory(IServiceProvider sp)
{
    public IDonationGateway Resolve(string configuredGateway) => configuredGateway.Trim().ToLowerInvariant() switch
    {
        "zarinpal" => sp.GetRequiredService<ZarinpalGateway>(),
        _ => sp.GetRequiredService<MockGateway>()
    };
}
