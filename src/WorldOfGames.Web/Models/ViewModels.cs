using System.ComponentModel.DataAnnotations;
using WorldOfGames.Core.Common;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;

namespace WorldOfGames.Web.Models;

// ───────── Account ─────────
public record LoginVm
{
    [Required(ErrorMessage = "ایمیل الزامی است."), EmailAddress(ErrorMessage = "ایمیل معتبر نیست.")]
    public string Email { get; init; } = "";
    [Required(ErrorMessage = "رمز عبور الزامی است.")]
    [DataType(DataType.Password)]
    public string Password { get; init; } = "";
    public bool RememberMe { get; init; }
    public string? ErrorMessage { get; init; }
}

public record RegisterVm
{
    [Required(ErrorMessage = "نام نمایشی الزامی است."), StringLength(60, MinimumLength = 2, ErrorMessage = "نام نمایشی بین ۲ تا ۶۰ نویسه.")]
    [Display(Name = "نام نمایشی")]
    public string DisplayName { get; init; } = "";
    [Required(ErrorMessage = "ایمیل الزامی است."), EmailAddress(ErrorMessage = "ایمیل معتبر نیست.")]
    public string Email { get; init; } = "";
    [Required(ErrorMessage = "رمز عبور الزامی است."), StringLength(100, MinimumLength = 8, ErrorMessage = "رمز عبور حداقل ۸ نویسه.")]
    [DataType(DataType.Password)]
    public string Password { get; init; } = "";
    [Required(ErrorMessage = "تکرار رمز الزامی است."), DataType(DataType.Password)]
    [Compare(nameof(Password), ErrorMessage = "تکرار رمز عبور مطابقت ندارد.")]
    [Display(Name = "تکرار رمز عبور")]
    public string ConfirmPassword { get; init; } = "";
}

// ───────── Games ─────────
public record GameIndexVm(string? Query, string? Sort, PagedResult<GameListItem> Result);

public record GameDetailsVm(Game Game, bool CanEdit);

public record PlayVm(Game Game);

public record SubmitGameVm
{
    [Required(ErrorMessage = "عنوان بازی الزامی است."), StringLength(120, MinimumLength = 3, ErrorMessage = "عنوان بین ۳ تا ۱۲۰ نویسه.")]
    public string Title { get; init; } = "";
    [Required(ErrorMessage = "توضیحات الزامی است."), StringLength(4000, MinimumLength = 20, ErrorMessage = "توضیحات حداقل ۲۰ نویسه.")]
    public string Description { get; init; } = "";
    [StringLength(2000)]
    public string? Instructions { get; init; }
    [Required(ErrorMessage = "دسته‌بندی الزامی است.")]
    public string Category { get; init; } = "";
    [StringLength(200)]
    public string? TagsCsv { get; init; }
    public IReadOnlyList<string> Errors { get; init; } = [];
}

// ───────── Blog ─────────
public record BlogIndexVm(PagedResult<BlogPost> Result, string? Tag);

public record BlogDetailsVm(BlogPost Post, IReadOnlyList<BlogPost> Related);

// ───────── Donations ─────────
public record DonationIndexVm(long SumPaidRial, int SupportersCount, IReadOnlyList<Donation> Recent, string GatewayName)
{
    [Display(Name = "مبلغ (ریال)")]
    public long AmountRial { get; init; }
    [Display(Name = "نام شما (اختیاری)")]
    public string? DonorName { get; init; }
    [Display(Name = "پیام شما (اختیاری)")]
    public string? Message { get; init; }
    [Display(Name = "ناشناس بمانم")]
    public bool IsAnonymous { get; init; }
}

public record DonationResultVm(Donation? Donation, bool Success, string? Message);

// ───────── Admin ─────────
public record AdminDashboardVm(int PendingGames, int ApprovedGames, int RejectedGames, int TotalUsers,
    long SumPaidRial, int PaidDonations, int PublishedPosts, IReadOnlyList<Game> LatestPending);

public record RejectGameVm
{
    public int Id { get; init; }
    [Required(ErrorMessage = "دلیل رد الزامی است (REQ-007)."), StringLength(400, MinimumLength = 5, ErrorMessage = "دلیل رد بین ۵ تا ۴۰۰ نویسه.")]
    public string Reason { get; init; } = "";
}

public record AdminPostFormVm
{
    public int? Id { get; init; }
    [Required(ErrorMessage = "عنوان الزامی است."), StringLength(160, MinimumLength = 3)]
    public string Title { get; init; } = "";
    [StringLength(120)]
    public string? SlugHint { get; init; }
    [Required(ErrorMessage = "خلاصه برای سئو الزامی است."), StringLength(400, MinimumLength = 10)]
    public string Excerpt { get; init; } = "";
    [Required(ErrorMessage = "متن پست الزامی است.")]
    public string Markdown { get; init; } = "";
    [StringLength(200)]
    public string? TagsCsv { get; init; }
    [StringLength(160)]
    public string? MetaTitle { get; init; }
    [StringLength(300)]
    public string? MetaDescription { get; init; }
    public bool IsPublished { get; init; }
    public string? ExistingCoverPath { get; init; }
    public IFormFile? Cover { get; init; }
}
