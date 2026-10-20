using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.Extensions.Options;
using WorldOfGames.Core.Entities;
using WorldOfGames.Infrastructure.Options;
using WorldOfGames.Web.Mcp;

namespace WorldOfGames.Tests;

// ───────── TEST-MCP (REQ-008) ─────────
public class McpTests : IDisposable
{
    private readonly (AppDbContext Db, SqliteConnection Conn) _env = TestEnv.CreateDb();

    public void Dispose() => _env.Conn.Dispose();

    [Fact]
    public void Tools_list_has_exactly_five_game_tools()
    {
        var tools = McpToolRegistry.Tools();
        Assert.Equal(5, tools.Length);
        var names = tools.Select(t => (string)t.GetType().GetProperty("name")!.GetValue(t)!).ToArray();
        Assert.Equal(
            ["list_pending_games", "get_game_status", "approve_game", "reject_game", "set_game_enabled"],
            names);
        Assert.All(tools, t =>
            Assert.NotNull(t.GetType().GetProperty("inputSchema")!.GetValue(t)));
    }

    [Fact]
    public async Task Reject_without_reason_returns_tool_error_and_keeps_status()
    {
        var game = await SeedPendingGameAsync();
        var games = TestEnv.GameService(_env.Db);
        var audit = new WorldOfGames.Infrastructure.Services.EfAuditService(_env.Db);

        var args = JsonSerializer.SerializeToElement(new { id = game.Id, reason = "" });
        var result = await McpToolRegistry.CallAsync("reject_game", args, games, audit);

        Assert.True((bool)result.GetType().GetProperty("isError")!.GetValue(result)!);
        var stored = await _env.Db.Games.AsNoTracking().FirstAsync(g => g.Id == game.Id);
        Assert.Equal(GameStatus.Pending, stored.Status); // وضعیت تغییر نکرده (REQ-008-4)
    }

    [Fact]
    public async Task Approve_via_mcp_publishes_and_audits_with_mcp_source()
    {
        var game = await SeedPendingGameAsync();
        var games = TestEnv.GameService(_env.Db);
        var audit = new WorldOfGames.Infrastructure.Services.EfAuditService(_env.Db);

        var args = JsonSerializer.SerializeToElement(new { id = game.Id });
        var result = await McpToolRegistry.CallAsync("approve_game", args, games, audit);
        Assert.False((bool)result.GetType().GetProperty("isError")!.GetValue(result)!);

        var stored = await _env.Db.Games.AsNoTracking().FirstAsync(g => g.Id == game.Id);
        Assert.Equal(GameStatus.Approved, stored.Status);
        Assert.True(stored.IsEnabled);

        var auditRow = await _env.Db.AuditEntries.AsNoTracking()
            .SingleAsync(a => a.EntityType == "Game" && a.EntityId == game.Id.ToString());
        Assert.Equal(AuditSource.Mcp, auditRow.Source); // REQ-008-5
        Assert.Equal("mcp", auditRow.Actor);
    }

    [Fact]
    public async Task List_pending_returns_json_payload()
    {
        await SeedPendingGameAsync();
        var games = TestEnv.GameService(_env.Db);
        var audit = new WorldOfGames.Infrastructure.Services.EfAuditService(_env.Db);

        var result = await McpToolRegistry.CallAsync("list_pending_games", JsonSerializer.SerializeToElement(new { }), games, audit);
        var isError = (bool)result.GetType().GetProperty("isError")!.GetValue(result)!;
        var content = (object[])result.GetType().GetProperty("content")!.GetValue(result)!;
        var text = (string)content[0].GetType().GetProperty("text")!.GetValue(content[0])!;
        Assert.False(isError);
        Assert.Contains("\"games\":", text);
        Assert.Contains("بازی آزمایشی", text);
    }

    [Fact]
    public async Task Handler_requires_bearer_token()
    {
        var games = TestEnv.GameService(_env.Db);
        var audit = new WorldOfGames.Infrastructure.Services.EfAuditService(_env.Db);
        var options = Options.Create(new McpOptions { Token = "secret-token" });

        var (ctx, body) = BuildRequest("""{"jsonrpc":"2.0","id":1,"method":"tools/list"}""", auth: null);
        await McpServerHandler.HandleAsync(ctx, games, audit, options);
        Assert.Equal(401, ctx.Response.StatusCode); // REQ-008-1
    }

    [Fact]
    public async Task Handler_initialize_handshake_is_standard()
    {
        var games = TestEnv.GameService(_env.Db);
        var audit = new WorldOfGames.Infrastructure.Services.EfAuditService(_env.Db);
        var options = Options.Create(new McpOptions { Token = "secret-token" });

        var (ctx, body) = BuildRequest(
            """{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}""",
            "Bearer secret-token");
        await McpServerHandler.HandleAsync(ctx, games, audit, options);

        var json = await ReadBodyAsync(ctx);
        using var doc = JsonDocument.Parse(json);
        Assert.Equal("2.0", doc.RootElement.GetProperty("jsonrpc").GetString());
        Assert.Equal(1, doc.RootElement.GetProperty("id").GetInt32());
        var result = doc.RootElement.GetProperty("result");
        Assert.Equal("2025-06-18", result.GetProperty("protocolVersion").GetString());
        Assert.True(result.GetProperty("capabilities").TryGetProperty("tools", out _)); // REQ-008-2
        Assert.Equal("world-of-games-admin", result.GetProperty("serverInfo").GetProperty("name").GetString());
    }

    [Fact]
    public async Task Handler_tools_call_roundtrip()
    {
        var game = await SeedPendingGameAsync();
        var games = TestEnv.GameService(_env.Db);
        var audit = new WorldOfGames.Infrastructure.Services.EfAuditService(_env.Db);
        var options = Options.Create(new McpOptions { Token = "secret-token" });

        var callJson = "{\"jsonrpc\":\"2.0\",\"id\":7,\"method\":\"tools/call\",\"params\":{\"name\":\"reject_game\",\"arguments\":{\"id\":" +
                       game.Id + ",\"reason\":\"کاور تصویر نامناسب دارد\"}}}";
        var (ctx, body) = BuildRequest(callJson, "Bearer secret-token");
        await McpServerHandler.HandleAsync(ctx, games, audit, options);
        var json = await ReadBodyAsync(ctx);
        using var doc = JsonDocument.Parse(json);
        var result = doc.RootElement.GetProperty("result");
        Assert.False(result.GetProperty("isError").GetBoolean());
        Assert.Equal("text", result.GetProperty("content")[0].GetProperty("type").GetString());
        Assert.Contains("رد شد", result.GetProperty("content")[0].GetProperty("text").GetString());
    }

    [Fact]
    public void Fixed_time_compare_rejects_wrong_token()
    {
        Assert.True(McpServerHandler.FixedTimeEquals("Bearer abc", "Bearer abc"));
        Assert.False(McpServerHandler.FixedTimeEquals("Bearer abc", "Bearer abd"));
    }

    // ── helpers ──
    private async Task<Game> SeedPendingGameAsync()
    {
        var db = _env.Db;
        db.Games.Add(new Game
        {
            Slug = "test-game-" + Guid.NewGuid().ToString("N")[..6],
            Title = "بازی آزمایشی",
            Description = "توضیحات کافی برای تست",
            Category = "معمایی",
            CoverPath = "/media/covers/x.png",
            EntryPath = "/media/games/x/index.html",
            DeveloperUserId = "u1",
            DeveloperName = "توسعه‌دهنده"
        });
        await db.SaveChangesAsync();
        return await db.Games.AsNoTracking().FirstAsync();
    }

    private static (DefaultHttpContext Ctx, MemoryStream Body) BuildRequest(string json, string? auth)
    {
        var ctx = new DefaultHttpContext();
        ctx.Request.Method = "POST";
        ctx.Request.Path = "/mcp";
        ctx.Request.ContentType = "application/json";
        if (auth is not null) ctx.Request.Headers.Authorization = auth;
        var ms = new MemoryStream(Encoding.UTF8.GetBytes(json));
        ms.Position = 0;
        ctx.Request.Body = ms;
        ctx.Response.Body = new MemoryStream();
        return (ctx, ms);
    }

    private static async Task<string> ReadBodyAsync(HttpContext ctx)
    {
        ctx.Response.Body.Position = 0;
        using var reader = new StreamReader(ctx.Response.Body, Encoding.UTF8, leaveOpen: true);
        return await reader.ReadToEndAsync();
    }
}
