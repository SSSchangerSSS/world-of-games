namespace WorldOfGames.Core.Common;

/// <summary>نتیجه استاندارد عملیات سرویس — خطاها فارسی برای نمایش مستقیم.</summary>
public record OpResult(bool Success, string? Error = null, IReadOnlyList<string>? Errors = null)
{
    public static OpResult Ok() => new(true);
    public static OpResult Fail(string error) => new(false, error);
    public static OpResult Fail(IReadOnlyList<string> errors) => new(false, errors.FirstOrDefault(), errors);
}

public record OpResult<T>(bool Success, T? Value = default, string? Error = null, IReadOnlyList<string>? Errors = null)
{
    public static OpResult<T> Ok(T value) => new(true, value);
    public static OpResult<T> Fail(string error) => new(false, default, error);
    public static OpResult<T> Fail(IReadOnlyList<string> errors) => new(false, default, errors.FirstOrDefault(), errors);
}

/// <summary>نتیجه اعتبارسنجی بسته بازی — قرارداد machine-checkable استاندارد آپلود.</summary>
public record PackageValidationResult(bool Success, IReadOnlyList<string> Errors)
{
    public static PackageValidationResult Valid => new(true, Array.Empty<string>());
    public static PackageValidationResult Invalid(params string[] errors) => new(false, errors);
}

public record PagedResult<T>(IReadOnlyList<T> Items, int Total, int Page, int PageSize)
{
    public int TotalPages => Math.Max(1, (int)Math.Ceiling(Total / (double)PageSize));
}
