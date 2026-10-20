namespace WorldOfGames.Core.Entities;

public enum GameStatus { Pending = 0, Approved = 1, Rejected = 2 }
public enum DonationStatus { Pending = 0, Paid = 1, Failed = 2, Canceled = 3 }
public enum AuditSource { Web = 0, Mcp = 1 }

/// <summary>بازی ارائه‌شده توسط کاربران — چرخه: Pending → (تأیید/رد ادمین) → نمایش عمومی</summary>
public class Game
{
    public int Id { get; set; }
    public string Slug { get; set; } = "";
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    public string? Instructions { get; set; }
    public string Category { get; set; } = "";
    public string TagsCsv { get; set; } = "";
    public string CoverPath { get; set; } = "";
    public string EntryPath { get; set; } = "";
    public GameStatus Status { get; set; } = GameStatus.Pending;
    public bool IsEnabled { get; set; } = true;
    public string? RejectionReason { get; set; }
    public string DeveloperUserId { get; set; } = "";
    public string DeveloperName { get; set; } = "";
    public long PlayCount { get; set; }
    public DateTime SubmittedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ReviewedAt { get; set; }
    public string? ReviewedBy { get; set; }
}

public class BlogPost
{
    public int Id { get; set; }
    public string Slug { get; set; } = "";
    public string Title { get; set; } = "";
    public string Excerpt { get; set; } = "";
    public string ContentHtml { get; set; } = "";
    public string? CoverPath { get; set; }
    public string TagsCsv { get; set; } = "";
    public string? MetaTitle { get; set; }
    public string? MetaDescription { get; set; }
    public bool IsPublished { get; set; }
    public DateTime? PublishedAt { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    public long Views { get; set; }
    public string AuthorDisplayName { get; set; } = "";
}

public class Donation
{
    public int Id { get; set; }
    public string Gateway { get; set; } = "";
    public long AmountRial { get; set; }
    public string? DonorName { get; set; }
    public string? Message { get; set; }
    public bool IsAnonymous { get; set; }
    public DonationStatus Status { get; set; } = DonationStatus.Pending;
    public string? Authority { get; set; }
    public string? RefId { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? PaidAt { get; set; }
}

/// <summary>ردپای اقدامات مدیریتی (ماده ۱۰ قانون اساسی — Traceability)</summary>
public class AuditEntry
{
    public int Id { get; set; }
    public AuditSource Source { get; set; }
    public string Actor { get; set; } = "";
    public string Action { get; set; } = "";
    public string EntityType { get; set; } = "";
    public string EntityId { get; set; } = "";
    public string? Detail { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
