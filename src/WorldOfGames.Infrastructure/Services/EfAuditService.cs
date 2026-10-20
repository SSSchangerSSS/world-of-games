using Microsoft.EntityFrameworkCore;
using WorldOfGames.Core.Common;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;

namespace WorldOfGames.Infrastructure.Services;

public sealed class EfAuditService(AppDbContext db) : IAuditService
{
    public async Task LogAsync(AuditSource source, string actor, string action, string entityType, string entityId, string? detail = null)
    {
        db.AuditEntries.Add(new AuditEntry
        {
            Source = source,
            Actor = string.IsNullOrWhiteSpace(actor) ? "unknown" : actor,
            Action = action,
            EntityType = entityType,
            EntityId = entityId,
            Detail = detail?.Length > 500 ? detail[..500] : detail
        });
        await db.SaveChangesAsync();
    }

    public async Task<PagedResult<AuditEntry>> ListAsync(int page, int pageSize)
    {
        page = Math.Max(1, page);
        pageSize = pageSize is > 0 and <= 100 ? pageSize : 30;
        var query = db.AuditEntries.AsNoTracking().OrderByDescending(a => a.CreatedAt).ThenByDescending(a => a.Id);
        var total = await query.CountAsync();
        var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
        return new PagedResult<AuditEntry>(items, total, page, pageSize);
    }
}
