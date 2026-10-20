using System.Globalization;

namespace WorldOfGames.Web.Models;

/// <summary>هلپرهای نمایش فارسی — تاریخ تهران و قالب‌بندی ریال/تومان (REQ-001).</summary>
public static class DisplayHelper
{
    private static readonly Lazy<TimeZoneInfo?> Tehran = new(() =>
    {
        try { return TimeZoneInfo.FindSystemTimeZoneById("Asia/Tehran"); }
        catch { try { return TimeZoneInfo.FindSystemTimeZoneById("Iran Standard Time"); } catch { return null; } }
    });

    public static DateTime ToTehran(DateTime utc)
    {
        if (utc.Kind == DateTimeKind.Unspecified) utc = DateTime.SpecifyKind(utc, DateTimeKind.Utc);
        var tz = Tehran.Value;
        return tz is null ? utc : TimeZoneInfo.ConvertTimeFromUtc(utc, tz);
    }

    /// <summary>تاریخ شمسی خوانا: ۲۸ مهر ۱۴۰۵</summary>
    public static string PersianDate(DateTime utc) => ToTehran(utc).ToString("d MMMM yyyy", CultureInfo.GetCultureInfo("fa-IR"));

    /// <summary>تاریخ و ساعت شمسی: ۲۸ مهر ۱۴۰۵، ۱۴:۳۰</summary>
    public static string PersianDateTime(DateTime utc) => ToTehran(utc).ToString("d MMMM yyyy، HH:mm", CultureInfo.GetCultureInfo("fa-IR"));

    /// <summary>ریال با جداکننده و رقم فارسی: ۱٬۵۰۰٬۰۰۰</summary>
    public static string Number(long value) => value.ToString("N0", CultureInfo.GetCultureInfo("fa-IR"));

    /// <summary>مبلغ به تومان خوانا</summary>
    public static string Toman(long amountRial) => $"{Number(amountRial / 10)} تومان";

    public static string PlayCount(long n) => n switch
    {
        0 => "بدون اجرا",
        _ => $"{Number(n)} اجرا"
    };

    public static string StatusFa(Core.Entities.GameStatus s) => s switch
    {
        Core.Entities.GameStatus.Pending => "در انتظار بررسی",
        Core.Entities.GameStatus.Approved => "تأییدشده",
        _ => "ردشده"
    };

    public static string StatusFa(Core.Entities.DonationStatus s) => s switch
    {
        Core.Entities.DonationStatus.Pending => "در انتظار پرداخت",
        Core.Entities.DonationStatus.Paid => "پرداخت‌شده",
        Core.Entities.DonationStatus.Failed => "ناموفق",
        _ => "لغوشده"
    };

    public static readonly string[] Categories =
        ["اکشن", "معمایی", "پازل", "کازوال", "استراتژی", "ورزشی", "خانوادگی", "ماجراجویی", "آموزشی"];

    public static readonly long[] DonationPresetsRial = [500_000, 1_000_000, 2_000_000, 5_000_000];
}
