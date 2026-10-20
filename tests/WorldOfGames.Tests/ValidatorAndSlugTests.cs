using System.IO.Compression;
using System.Text;
using WorldOfGames.Core.Common;
using WorldOfGames.Infrastructure.Options;
using WorldOfGames.Infrastructure.Services;

namespace WorldOfGames.Tests;

// ───────── TEST-VALIDATOR (REQ-004) ─────────
public class ZipGamePackageValidatorTests
{
    private static ZipGamePackageValidator Create() =>
        new(new UploadOptions { MaxZipMB = 1, MaxUncompressedMB = 2, MaxFiles = 50 });

    private static byte[] BuildZip(params (string Name, string Content)[] files)
    {
        using var ms = new MemoryStream();
        using (var zip = new ZipArchive(ms, ZipArchiveMode.Create, leaveOpen: true))
        {
            foreach (var (name, content) in files)
            {
                var entry = zip.CreateEntry(name);
                using var writer = new StreamWriter(entry.Open(), Encoding.UTF8);
                writer.Write(content);
            }
        }
        return ms.ToArray();
    }

    private static PackageValidationResult Validate(byte[] bytes)
    {
        var validator = Create();
        using var ms = new MemoryStream(bytes);
        return validator.Validate(ms, ms.Length);
    }

    [Fact]
    public void Valid_package_passes()
    {
        var result = Validate(BuildZip(
            ("index.html", "<html><body>game</body></html>"),
            ("js/main.js", "console.log(1)"),
            ("assets/sprites.png", "PNGDATA")));
        Assert.True(result.Success, string.Join("; ", result.Errors));
    }

    [Fact]
    public void Missing_index_html_is_rejected()
    {
        var result = Validate(BuildZip(("game/main.html", "<html></html>")));
        Assert.False(result.Success);
        Assert.Contains(result.Errors, e => e.Contains("index.html"));
    }

    [Fact]
    public void Path_traversal_is_rejected()
    {
        var result = Validate(BuildZip(("index.html", "x"), ("../evil.txt", "hacked")));
        Assert.False(result.Success);
        Assert.Contains(result.Errors, e => e.Contains("ناامن"));
    }

    [Fact]
    public void Executable_extension_is_rejected()
    {
        var result = Validate(BuildZip(("index.html", "x"), ("loader.exe", "MZ")));
        Assert.False(result.Success);
        Assert.Contains(result.Errors, e => e.Contains("exe"));
    }

    [Fact]
    public void Unknown_extension_is_rejected()
    {
        var result = Validate(BuildZip(("index.html", "x"), ("data.xyz", "mystery")));
        Assert.False(result.Success);
        Assert.Contains(result.Errors, e => e.Contains("xyz"));
    }

    [Fact]
    public void Macosx_junk_is_ignored()
    {
        var result = Validate(BuildZip(
            ("index.html", "x"),
            ("__MACOSX/._index.html", "junk"),
            (".DS_Store", "junk")));
        Assert.True(result.Success, string.Join("; ", result.Errors));
    }

    [Fact]
    public void Oversize_compressed_is_rejected_without_parsing()
    {
        var validator = new ZipGamePackageValidator(new UploadOptions { MaxZipMB = 1, MaxUncompressedMB = 2, MaxFiles = 50 });
        using var ms = new MemoryStream(new byte[2 * 1024 * 1024]);
        var result = validator.Validate(ms, ms.Length);
        Assert.False(result.Success);
        Assert.Contains(result.Errors, e => e.Contains("سقف مجاز"));
    }

    [Fact]
    public void Uncompressed_total_limit_is_enforced()
    {
        // 1MB نافشرده × ۳ فایل > سقف 2MB? => 3MB > 2MB
        var big = new string('a', 1024 * 1024);
        var result = Validate(BuildZip(("index.html", "x"), ("a.txt", big), ("b.txt", big), ("c.txt", big)));
        Assert.False(result.Success);
        Assert.Contains(result.Errors, e => e.Contains("نافشرده"));
    }

    [Fact]
    public void Invalid_zip_stream_is_rejected()
    {
        var validator = Create();
        using var ms = new MemoryStream(new byte[] { 1, 2, 3, 4, 5 });
        var result = validator.Validate(ms, ms.Length);
        Assert.False(result.Success);
        Assert.Contains(result.Errors, e => e.Contains("ZIP معتبر"));
    }
}

// ───────── SlugHelper ─────────
public class SlugHelperTests
{
    [Theory]
    [InlineData("حافظه هخامنشی", "hafzh-hkhamnshi")]  // ترانویسی حرفی (بدون مصوت) — کافی برای URL یکتا
    [InlineData("Alborz Jump", "alborz-jump")]
    [InlineData("پرش از البرز!", "prsh-az-albrz")]
    public void Persian_titles_transliterate(string input, string expected)
    {
        Assert.Equal(expected, WorldOfGames.Core.Common.SlugHelper.Slugify(input));
    }

    [Fact]
    public void Empty_input_falls_back()
    {
        Assert.Equal("item", WorldOfGames.Core.Common.SlugHelper.Slugify("؟؟؟"));
    }
}
