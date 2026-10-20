namespace WorldOfGames.Infrastructure.Options;

public class UploadOptions
{
    public const string Section = "Uploads";
    public int MaxZipMB { get; set; } = 50;
    public int MaxUncompressedMB { get; set; } = 300;
    public int MaxFiles { get; set; } = 3000;
    public int MaxCoverMB { get; set; } = 2;
}

public class ZarinpalOptions
{
    public const string Section = "Zarinpal";
    public string MerchantId { get; set; } = "";
    public string RequestUrl { get; set; } = "https://payment.zarinpal.com/pg/v4/payment/request.json";
    public string VerifyUrl { get; set; } = "https://payment.zarinpal.com/pg/v4/payment/verify.json";
    public string StartPayUrl { get; set; } = "https://payment.zarinpal.com/pg/StartPay/";
}

public class DonationGatewayOptions
{
    public const string Section = "Donations";
    /// <summary>Mock | Zarinpal — تصمیم D-07</summary>
    public string Gateway { get; set; } = "Mock";
}

public class McpOptions
{
    public const string Section = "Mcp";
    public string Token { get; set; } = "";
}

public class SeedOptions
{
    public const string Section = "Seed";
    public bool Enabled { get; set; } = true;
}

public class AdminSeedOptions
{
    public const string Section = "AdminSeed";
    public string Email { get; set; } = "admin@worldofgames.ir";
    public string Password { get; set; } = "";
    public string DisplayName { get; set; } = "مدیر";
}

public class DatabaseOptions
{
    public const string Section = "Database";
    /// <summary>Sqlite | SqlServer — تصمیم D-05</summary>
    public string Provider { get; set; } = "Sqlite";
}
