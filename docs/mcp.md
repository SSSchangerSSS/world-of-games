# سرور MCP مدیریت بازی‌ها

پنل ادمین با **Model Context Protocol** قابل کنترل است (تصمیم D-08: فقط مدیریت بازی‌ها).

## Endpoint

```text
POST {base-url}/mcp
Headers:
  Authorization: Bearer {Mcp:Token}
  Content-Type: application/json
```

- پروتکل: JSON-RPC 2.0 روی Streamable HTTP با **پاس JSON** (بدون SSE)
- پیاده‌سازی دست‌ساز (D-11 — برگشت‌پذیر؛ قابل تعویض با SDK رسمی)
- توکن از `appsettings.json → Mcp:Token` (در پروداکشن حتماً تغییر دهید)
- توکن غلط/خالی → `401`
- هر فراخوانی موفق در Audit Log با `Source=Mcp` ثبت می‌شود

## ابزارها (Tools)

| Tool | ورودی | رفتار |
|---|---|---|
| `list_pending_games` | — | صف درخواست‌های در انتظار (حداکثر ۵۰) |
| `get_game_status` | `id` یا `slug` | وضعیت کامل بازی |
| `approve_game` | `id` | تأیید و انتشار در کاتالوگ |
| `reject_game` | `id`, `reason` (≥۵ نویسه) | رد با دلیل الزامی |
| `set_game_enabled` | `id`, `enabled` (bool) | فعال/غیرفعال‌سازی نمایش |

## نمونه

```bash
# handshake
curl -X POST https://example.ir/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"my-agent","version":"1.0"}}}'

# لیست ابزارها
curl -X POST https://example.ir/mcp -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

# رد بازی با دلیل
curl -X POST https://example.ir/mcp -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"reject_game","arguments":{"id":12,"reason":"بسته شامل index.html در ریشه نیست"}}}'
```

## اتصال از کلاینت‌های MCP (Claude / Cursor و…)

```json
{
  "mcpServers": {
    "world-of-games-admin": {
      "type": "http",
      "url": "https://example.ir/mcp",
      "headers": { "Authorization": "Bearer YOUR_TOKEN" }
    }
  }
}
```

پاس‌خورها: `initialize` (echo protocolVersion شناخته‌شده)، `ping`، `tools/list`، `tools/call`؛ notification بدون id → `202 Accepted`؛ متد ناشناخته → `-32601`.
