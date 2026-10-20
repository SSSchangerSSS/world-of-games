using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.Extensions.Options;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;
using WorldOfGames.Infrastructure.Options;
using WorldOfGames.Infrastructure.Services;

namespace WorldOfGames.Tests;

/// <summary>زیرساخت مشترک تست: SQLite in-memory + سرویس‌های واقعی (Integration-style).</summary>
public static class TestEnv
{
    public static (AppDbContext Db, SqliteConnection Conn) CreateDb()
    {
        var conn = new SqliteConnection("DataSource=:memory:");
        conn.Open();
        var options = new DbContextOptionsBuilder<AppDbContext>().UseSqlite(conn).Options;
        var db = new AppDbContext(options);
        db.Database.EnsureCreated();
        return (db, conn);
    }

    public static IGameService GameService(AppDbContext db) =>
        new EfGameService(db, Validator(), NullLogger<EfGameService>.Instance);

    public static ZipGamePackageValidator Validator() =>
        new(new UploadOptions { MaxZipMB = 5, MaxUncompressedMB = 20, MaxFiles = 500 });

    public static EfBlogService BlogService(AppDbContext db) =>
        new(db);

    public static IDonationService DonationService(AppDbContext db, string gateway = "Mock")
    {
        var factory = new DonationGatewayFactory(BuildProvider(gateway));
        return new EfDonationService(db, factory,
            Options.Create(new DonationGatewayOptions { Gateway = gateway }),
            NullLogger<EfDonationService>.Instance);
    }

    private static IServiceProvider BuildProvider(string gateway)
    {
        // تست‌ها فقط MockGateway لازم دارند (زرین‌پال = KI-3)
        var services = new ServiceCollection();
        services.AddSingleton<MockGateway>();
        return services.BuildServiceProvider();
    }
}
