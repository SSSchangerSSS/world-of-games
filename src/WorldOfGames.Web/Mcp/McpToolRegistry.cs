using System.Text.Encodings.Web;
using System.Text.Json;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;

namespace WorldOfGames.Web.Mcp;

/// <summary>رجیستری ۵ ابزار MCP مدیریت بازی‌ها (D-08) — اسکیمای ثابت، اجرا با Audit Source=Mcp.</summary>
public sealed class McpToolRegistry
{
    // خروجی خوانا برای کلاینت‌های MCP (یونیکد بدون escape)
    private static readonly JsonSerializerOptions JsonOpts = new()
    {
        Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    };
    public static object[] Tools() =>
    [
        Tool("list_pending_games", "لیست بازی‌های در انتظار تأیید ادمین (صف moderation).",
            new { type = "object", properties = new { }, required = Array.Empty<string>() }),
        Tool("get_game_status", "وضعیت کامل یک بازی بر اساس شناسه یا نامک (slug).",
            new
            {
                type = "object",
                properties = new { id = new { type = "integer", description = "شناسه عددی بازی" }, slug = new { type = "string", description = "نامک بازی (جایگزین id)" } },
                required = Array.Empty<string>()
            }),
        Tool("approve_game", "تأیید بازی در انتظار و انتشار آن در کاتالوگ عمومی.",
            new { type = "object", properties = new { id = new { type = "integer", description = "شناسه بازی" } }, required = new[] { "id" } }),
        Tool("reject_game", "رد بازی با ذکر دلیل الزامی (حداقل ۵ نویسه) — دلیل برای توسعه‌دهنده نمایش داده می‌شود.",
            new
            {
                type = "object",
                properties = new { id = new { type = "integer", description = "شناسه بازی" }, reason = new { type = "string", description = "دلیل رد" } },
                required = new[] { "id", "reason" }
            }),
        Tool("set_game_enabled", "فعال یا غیرفعال کردن نمایش بازی تأییدشده در کاتالوگ.",
            new
            {
                type = "object",
                properties = new { id = new { type = "integer", description = "شناسه بازی" }, enabled = new { type = "boolean", description = "true = فعال" } },
                required = new[] { "id", "enabled" }
            })
    ];

    private static object Tool(string name, string description, object inputSchema) =>
        new { name, description, inputSchema };

    public static async Task<object> CallAsync(string? name, JsonElement args, IGameService games, IAuditService audit)
    {
        try
        {
            switch (name)
            {
                case "list_pending_games":
                {
                    var page = await games.ListAdminAsync(GameStatus.Pending, page: 1, pageSize: 50);
                    var payload = page.Items.Select(g => new { g.Id, g.Title, g.Slug, g.Category, g.DeveloperName, g.SubmittedAt });
                    return Text($"{{\"count\":{page.Total},\"games\":{JsonSerializer.Serialize(payload, JsonOpts)}}}");
                }
                case "get_game_status":
                {
                    var game = await ResolveGameAsync(args, games);
                    if (game is null) return Err("بازی یافت نشد — id یا slug را بررسی کنید.");
                    return Text(JsonSerializer.Serialize(new
                    {
                        game.Id, game.Title, game.Slug, game.Category, status = game.Status.ToString(),
                        game.IsEnabled, game.PlayCount, game.DeveloperName, game.SubmittedAt, game.ReviewedAt,
                        game.RejectionReason
                    }, JsonOpts));
                }
                case "approve_game":
                {
                    var game = await ResolveGameAsync(args, games);
                    if (game is null) return Err("بازی یافت نشد.");
                    var res = await games.ApproveAsync(game.Id, "mcp", AuditSource.Mcp);
                    return res.Success ? Text($"بازی «{game.Title}» تأیید و منتشر شد.") : Err(res.Error!);
                }
                case "reject_game":
                {
                    var game = await ResolveGameAsync(args, games);
                    if (game is null) return Err("بازی یافت نشد.");
                    var reason = GetString(args, "reason");
                    var res = await games.RejectAsync(game.Id, reason ?? "", "mcp", AuditSource.Mcp);
                    return res.Success ? Text($"بازی «{game.Title}» با دلیل «{reason}» رد شد.") : Err(res.Error!);
                }
                case "set_game_enabled":
                {
                    var game = await ResolveGameAsync(args, games);
                    if (game is null) return Err("بازی یافت نشد.");
                    var enabled = args.ValueKind == JsonValueKind.Object && args.TryGetProperty("enabled", out var en)
                        ? en.ValueKind switch { JsonValueKind.True => true, JsonValueKind.False => false, _ => (bool?)null }
                        : null;
                    if (enabled is null) return Err("پارامتر enabled (boolean) الزامی است.");
                    var res = await games.SetEnabledAsync(game.Id, enabled.Value, "mcp", AuditSource.Mcp);
                    return res.Success ? Text($"بازی «{game.Title}» {(enabled.Value ? "فعال" : "غیرفعال")} شد.") : Err(res.Error!);
                }
                case null:
                    return Err("نام ابزار (name) الزامی است.");
                default:
                    return Err($"ابزار ناشناخته: {name} — tools/list را ببینید.");
            }
        }
        catch (Exception ex)
        {
            return Err("خطای داخلی: " + ex.Message);
        }

        static object Text(string text) => new { content = new object[] { new { type = "text", text } }, isError = false };
        static object Err(string message) => new { content = new object[] { new { type = "text", text = message } }, isError = true };
    }

    private static async Task<Game?> ResolveGameAsync(JsonElement args, IGameService games)
    {
        if (args.ValueKind == JsonValueKind.Object && args.TryGetProperty("id", out var idEl) && idEl.ValueKind == JsonValueKind.Number)
            return await games.GetByIdAsync(idEl.GetInt32());
        var slug = GetString(args, "slug");
        return slug is null ? null : await games.GetBySlugAsync(slug);
    }

    private static string? GetString(JsonElement args, string prop) =>
        args.ValueKind == JsonValueKind.Object && args.TryGetProperty(prop, out var el) && el.ValueKind == JsonValueKind.String
            ? el.GetString() : null;
}
