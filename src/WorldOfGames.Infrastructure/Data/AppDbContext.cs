using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore; // .NET 10: IdentityDbContext به این namespace منتقل شده
using Microsoft.EntityFrameworkCore;
using WorldOfGames.Core.Entities;

namespace WorldOfGames.Infrastructure.Data;

public class ApplicationUser : IdentityUser
{
    public string? DisplayName { get; set; }
}

public class AppDbContext(DbContextOptions<AppDbContext> options) : IdentityDbContext<ApplicationUser>(options)
{
    public DbSet<Game> Games => Set<Game>();
    public DbSet<BlogPost> BlogPosts => Set<BlogPost>();
    public DbSet<Donation> Donations => Set<Donation>();
    public DbSet<AuditEntry> AuditEntries => Set<AuditEntry>();

    protected override void OnModelCreating(ModelBuilder b)
    {
        base.OnModelCreating(b);

        b.Entity<Game>(e =>
        {
            e.Property(x => x.Slug).HasMaxLength(80);
            e.HasIndex(x => x.Slug).IsUnique();
            e.Property(x => x.Title).HasMaxLength(120).IsRequired();
            e.Property(x => x.Category).HasMaxLength(40);
            e.Property(x => x.TagsCsv).HasMaxLength(200);
            e.Property(x => x.CoverPath).HasMaxLength(200);
            e.Property(x => x.EntryPath).HasMaxLength(200);
            e.Property(x => x.RejectionReason).HasMaxLength(400);
            e.Property(x => x.DeveloperName).HasMaxLength(80);
            e.Property(x => x.DeveloperUserId).HasMaxLength(450);
            e.Property(x => x.ReviewedBy).HasMaxLength(450);
            e.HasIndex(x => new { x.Status, x.IsEnabled });
        });

        b.Entity<BlogPost>(e =>
        {
            e.Property(x => x.Slug).HasMaxLength(120);
            e.HasIndex(x => x.Slug).IsUnique();
            e.Property(x => x.Title).HasMaxLength(160).IsRequired();
            e.Property(x => x.Excerpt).HasMaxLength(400);
            e.Property(x => x.TagsCsv).HasMaxLength(200);
            e.Property(x => x.MetaTitle).HasMaxLength(160);
            e.Property(x => x.MetaDescription).HasMaxLength(300);
            e.Property(x => x.AuthorDisplayName).HasMaxLength(80);
            e.HasIndex(x => new { x.IsPublished, x.PublishedAt });
        });

        b.Entity<Donation>(e =>
        {
            e.Property(x => x.Gateway).HasMaxLength(20);
            e.Property(x => x.DonorName).HasMaxLength(60);
            e.Property(x => x.Message).HasMaxLength(300);
            e.Property(x => x.Authority).HasMaxLength(100);
            e.Property(x => x.RefId).HasMaxLength(100);
            // کوتیشن دابل روی هر دو Provider (SQLite و SQL Server با QUOTED_IDENTIFIER ON) معتبر است
            e.HasIndex(x => x.Authority).IsUnique().HasFilter("\"Authority\" IS NOT NULL");
            e.HasIndex(x => new { x.Status, x.PaidAt });
        });

        b.Entity<AuditEntry>(e =>
        {
            e.Property(x => x.Actor).HasMaxLength(80);
            e.Property(x => x.Action).HasMaxLength(40);
            e.Property(x => x.EntityType).HasMaxLength(20);
            e.Property(x => x.EntityId).HasMaxLength(20);
            e.Property(x => x.Detail).HasMaxLength(500);
            e.HasIndex(x => x.CreatedAt);
        });
    }
}
