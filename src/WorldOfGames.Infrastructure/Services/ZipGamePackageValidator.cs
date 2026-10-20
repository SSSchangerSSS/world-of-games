using System.IO.Compression;
using WorldOfGames.Core.Common;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Options;

namespace WorldOfGames.Infrastructure.Services;

/// <summary>اعتبارسنج ماشینی «استاندارد آپلود بازی» (REQ-004 / docs/game-upload-standard.md).</summary>
public sealed class ZipGamePackageValidator(UploadOptions options) : IGamePackageValidator
{
    // فایل‌های مجاز بسته — هر چیز دیگر رد می‌شود (KI-4: جایگزین موقت اسکن آنتی‌ویروس)
    internal static readonly HashSet<string> AllowedExtensions = new(StringComparer.OrdinalIgnoreCase)
    {
        ".html", ".htm", ".css", ".js", ".mjs", ".json", ".txt", ".csv", ".xml", ".md",
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".bmp",
        ".woff", ".woff2", ".ttf", ".otf",
        ".mp3", ".ogg", ".wav", ".m4a", ".mp4", ".webm",
        ".atlas", ".tmx", ".tmj", ".fnt", ".bin", ".pak"
    };

    private static readonly HashSet<string> BlockedNames = new(StringComparer.OrdinalIgnoreCase)
    { ".exe", ".dll", ".bat", ".cmd", ".sh", ".ps1", ".msi", ".so", ".dylib", ".php", ".aspx", ".jar" };

    public PackageValidationResult Validate(Stream zipStream, long compressedLength)
    {
        var errors = new List<string>();
        var maxZip = (long)options.MaxZipMB * 1024 * 1024;
        var maxUncompressed = (long)options.MaxUncompressedMB * 1024 * 1024;

        if (compressedLength <= 0) errors.Add("فایل بسته بازی خالی است.");
        else if (compressedLength > maxZip)
            errors.Add($"حجم بسته {compressedLength / (1024 * 1024)} مگابایت است؛ سقف مجاز {options.MaxZipMB} مگابایت.");

        if (errors.Count > 0) return PackageValidationResult.Invalid(errors.ToArray());

        ZipArchive? archive = null;
        try
        {
            archive = new ZipArchive(zipStream, ZipArchiveMode.Read, leaveOpen: true);
        }
        catch (InvalidDataException)
        {
            return PackageValidationResult.Invalid("فایل ارسالی یک بسته ZIP معتبر نیست.");
        }

        using (archive)
        {
            var entries = archive.Entries.Where(e => !IsJunk(e.FullName)).ToList();
            if (entries.Count == 0)
                errors.Add("بسته خالی است یا فقط شامل فایل‌های سیستمی (مثل __MACOSX) است.");

            var index = entries.FirstOrDefault(e =>
                e.FullName.Equals("index.html", StringComparison.OrdinalIgnoreCase));
            if (index is null)
                errors.Add("فایل «index.html» باید در ریشه بسته وجود داشته باشد (استاندارد آپلود).");

            long totalUncompressed = 0;
            var fileCount = 0;

            foreach (var entry in entries)
            {
                var name = entry.FullName;
                if (name.Length > 260) { errors.Add($"مسیر فایل بیش از حد طولانی است: {name[..60]}…"); continue; }

                // مسیر مطلق و traversal ممنوع
                var normalized = name.Replace('\\', '/');
                if (normalized.StartsWith('/') || Path.IsPathRooted(name) ||
                    name.Contains("..") || name.Contains(':'))
                {
                    errors.Add($"مسیر ناامن در بسته ممنوع است: {name}");
                    continue;
                }

                var ext = Path.GetExtension(name);
                if (BlockedNames.Contains(ext))
                    errors.Add($"پسوند «{ext}» در بسته بازی مجاز نیست: {name}");
                else if (!AllowedExtensions.Contains(ext))
                    errors.Add($"پسوند «{(string.IsNullOrEmpty(ext) ? "(بدون پسوند)" : ext)}» مجاز نیست: {name}");

                totalUncompressed += entry.Length;
                fileCount++;
                if (fileCount > options.MaxFiles)
                {
                    errors.Add($"تعداد فایل‌های بسته از سقف {options.MaxFiles} بیشتر است.");
                    break;
                }
            }

            if (totalUncompressed > maxUncompressed)
                errors.Add($"حجم نافشرده بسته ({totalUncompressed / (1024 * 1024)}MB) از سقف {options.MaxUncompressedMB}MB بیشتر است.");
        }

        return errors.Count == 0 ? PackageValidationResult.Valid : new PackageValidationResult(false, errors);
    }

    /// <summary>فایل‌های زائد macOS/ویندوز که نباید در سقف‌ها لحاظ شوند.</summary>
    internal static bool IsJunk(string entryName)
    {
        var n = entryName.Replace('\\', '/');
        if (n.EndsWith('/') || n.EndsWith("/.") || n.EndsWith("/..")) return true;
        var parts = n.Split('/', StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length == 0) return true;
        if (parts[0].Equals("__MACOSX", StringComparison.OrdinalIgnoreCase)) return true;
        var fileName = parts[^1];
        return fileName.StartsWith("._", StringComparison.Ordinal) ||
               fileName.Equals(".DS_Store", StringComparison.OrdinalIgnoreCase) ||
               fileName.Equals("Thumbs.db", StringComparison.OrdinalIgnoreCase);
    }
}
