using System.Security.Cryptography;
using System.Text.Json;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Options;

namespace WorldOfGames.Web.Mcp;

/// <summary>
/// سرور MCP مدیریت بازی‌ها (REQ-008 / D-08): JSON-RPC 2.0 روی POST /mcp — Streamable HTTP با پاس JSON.
/// دست‌ساز طبق D-11 (برگشت‌پذیر؛ قابل تعویض با SDK رسمی). احراز: Bearer Token از کانفیگ.
/// </summary>
public static class McpEndpoints
{
    public static void Map(WebApplication app)
    {
        app.MapPost("/mcp", McpServerHandler.HandleAsync);
        app.MapGet("/mcp", async (HttpContext ctx) =>
        {
            ctx.Response.StatusCode = StatusCodes.Status405MethodNotAllowed;
            ctx.Response.ContentType = "application/json; charset=utf-8";
            await ctx.Response.WriteAsync("""{"error":"این سرور MCP فقط POST با JSON-RPC 2.0 می‌پذیرد (JSON response mode)."}""");
        });
    }
}

public static class McpServerHandler
{
    private static readonly string[] SupportedProtocols = ["2025-06-18", "2025-03-26", "2024-11-05"];

    public static async Task HandleAsync(HttpContext ctx, IGameService games, IAuditService audit,
        Microsoft.Extensions.Options.IOptions<McpOptions> options)
    {
        // ── Auth: Bearer (REQ-008-1) ──
        var expected = "Bearer " + options.Value.Token;
        var provided = ctx.Request.Headers.Authorization.ToString();
        if (string.IsNullOrEmpty(options.Value.Token) || !FixedTimeEquals(provided, expected))
        {
            ctx.Response.StatusCode = StatusCodes.Status401Unauthorized;
            ctx.Response.ContentType = "application/json; charset=utf-8";
            await ctx.Response.WriteAsync("""{"jsonrpc":"2.0","id":null,"error":{"code":-32000,"message":"Unauthorized — Bearer token الزامی است."}}""");
            return;
        }

        JsonDocument doc;
        try
        {
            doc = await JsonDocument.ParseAsync(ctx.Request.Body);
        }
        catch (JsonException)
        {
            ctx.Response.StatusCode = StatusCodes.Status400BadRequest;
            ctx.Response.ContentType = "application/json; charset=utf-8";
            await ctx.Response.WriteAsync("""{"jsonrpc":"2.0","id":null,"error":{"code":-32700,"message":"Parse error"}}""");
            return;
        }

        using (doc)
        {
            var root = doc.RootElement;
            var hasId = root.TryGetProperty("id", out var idEl) && idEl.ValueKind is not (JsonValueKind.Null or JsonValueKind.Undefined);
            var method = root.TryGetProperty("method", out var mEl) ? mEl.GetString() : null;
            var hasParams = root.TryGetProperty("params", out var pEl) && pEl.ValueKind == JsonValueKind.Object;
            JsonElement args = default;
            if (hasParams && pEl.TryGetProperty("arguments", out var aEl) && aEl.ValueKind == JsonValueKind.Object)
                args = aEl;

            // notification (بدون id) — پاس لازم نیست
            if (!hasId)
            {
                ctx.Response.StatusCode = StatusCodes.Status202Accepted;
                return;
            }

            object? result = null;
            (int Code, string Message)? error = null;

            switch (method)
            {
                case "initialize":
                    var requested = hasParams && pEl.TryGetProperty("protocolVersion", out var pvEl) && pvEl.GetString() is { } pv
                        ? pv : "2025-06-18";
                    var proto = SupportedProtocols.Contains(requested) ? requested : SupportedProtocols[0];
                    result = new
                    {
                        protocolVersion = proto,
                        capabilities = new { tools = new { listChanged = false } },
                        serverInfo = new { name = "world-of-games-admin", version = "1.0.0", title = "مدیریت بازی‌های World of Games" }
                    };
                    break;

                case "ping":
                    result = new { };
                    break;

                case "tools/list":
                    result = new { tools = McpToolRegistry.Tools() };
                    break;

                case "tools/call":
                    var toolName = hasParams && pEl.TryGetProperty("name", out var nEl) ? nEl.GetString() : null;
                    result = await McpToolRegistry.CallAsync(toolName, args, games, audit);
                    break;

                case null:
                    error = (-32600, "Invalid Request — method الزامی است.");
                    break;

                default:
                    error = (-32601, $"Method not found: {method}");
                    break;
            }

            ctx.Response.StatusCode = StatusCodes.Status200OK;
            ctx.Response.ContentType = "application/json; charset=utf-8";
            if (error.HasValue)
            {
                await ctx.Response.WriteAsync(JsonSerializer.Serialize(new
                {
                    jsonrpc = "2.0", id = idEl.Clone(),
                    error = new { code = error.Value.Code, message = error.Value.Message }
                }));
            }
            else
            {
                await ctx.Response.WriteAsync(JsonSerializer.Serialize(new { jsonrpc = "2.0", id = idEl.Clone(), result }));
            }
        }
    }

    public static bool FixedTimeEquals(string a, string b)
    {
        var ab = System.Text.Encoding.UTF8.GetBytes(a);
        var bb = System.Text.Encoding.UTF8.GetBytes(b);
        return CryptographicOperations.FixedTimeEquals(ab, bb);
    }
}
