using System.Text;
using System.Text.RegularExpressions;

namespace WorldOfGames.Core.Common;

/// <summary>تولید slug لاتین امن برای URL؛ عناوین فارسی به لاتین ترانویسی می‌شوند تا URL تمیز و سازگار با IIS باشد.</summary>
public static partial class SlugHelper
{
    [GeneratedRegex(@"[^a-z0-9\-]+")]
    private static partial Regex NonSlugChars();

    public static string Slugify(string? text)
    {
        var normalized = (text ?? "").Trim().ToLowerInvariant();
        var sb = new StringBuilder(normalized.Length);
        foreach (var ch in normalized)
        {
            if (ch is >= 'a' and <= 'z' or >= '0' and <= '9')
            {
                sb.Append(ch);
                continue;
            }
            var map = ch switch
            {
                'آ' or 'ا' or 'ع' => "a", 'ب' => "b", 'پ' => "p", 'ت' or 'ط' => "t",
                'ث' or 'س' or 'ص' => "s", 'ج' => "j", 'چ' => "ch", 'ح' or 'ه' or 'ة' => "h",
                'خ' => "kh", 'د' => "d", 'ذ' or 'ز' or 'ض' or 'ظ' => "z", 'ر' => "r",
                'ژ' => "zh", 'ش' => "sh", 'غ' or 'ق' => "gh", 'ف' => "f",
                'ک' or 'ك' => "k", 'گ' => "g", 'ل' => "l", 'م' => "m", 'ن' => "n",
                'و' or 'ؤ' => "v", 'ی' or 'ي' or 'ئ' => "i",
                ' ' or '-' or '_' => "-",
                _ => ""
            };
            sb.Append(map);
        }
        var slug = NonSlugChars().Replace(sb.ToString(), "-");
        while (slug.Contains("--")) slug = slug.Replace("--", "-");
        slug = slug.Trim('-');
        if (slug.Length > 70) slug = slug[..70].Trim('-');
        return string.IsNullOrWhiteSpace(slug) ? "item" : slug;
    }

    public static string WithSuffix(string slug) => $"{slug}-{Random.Shared.Next(1000, 9999)}";
}
