using System.Globalization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Localization;
using Microsoft.EntityFrameworkCore;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;
using WorldOfGames.Infrastructure.Options;
using WorldOfGames.Infrastructure.Seed;
using WorldOfGames.Infrastructure.Services;
using WorldOfGames.Web.Mcp;

var builder = WebApplication.CreateBuilder(args);

// ── Database (D-05: SQLite توسعه / SQL Server پروداکشن) ──
var dbOpts = builder.Configuration.GetSection(DatabaseOptions.Section).Get<DatabaseOptions>() ?? new DatabaseOptions();
builder.Services.AddDbContext<AppDbContext>(o =>
{
    if (string.Equals(dbOpts.Provider, "SqlServer", StringComparison.OrdinalIgnoreCase))
        o.UseSqlServer(builder.Configuration.GetConnectionString("SqlServer"));
    else
        o.UseSqlite(builder.Configuration.GetConnectionString("Default"));
});

// ── Identity (REQ-002) ──
builder.Services.AddIdentity<ApplicationUser, IdentityRole>(o =>
    {
        o.Password.RequiredLength = 8;
        o.Password.RequireNonAlphanumeric = false;
        o.Password.RequireUppercase = false;
        o.Password.RequireDigit = true;
        o.User.RequireUniqueEmail = true;
        o.Lockout.MaxFailedAccessAttempts = 5;
        o.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(10);
    })
    .AddEntityFrameworkStores<AppDbContext>()
    .AddDefaultTokenProviders();

builder.Services.ConfigureApplicationCookie(o =>
{
    o.LoginPath = "/Account/Login";
    o.AccessDeniedPath = "/Account/AccessDenied";
    o.ExpireTimeSpan = TimeSpan.FromDays(14);
    o.SlidingExpiration = true;
});

// ── Options ──
builder.Services.Configure<UploadOptions>(builder.Configuration.GetSection(UploadOptions.Section));
builder.Services.AddSingleton(sp =>
    builder.Configuration.GetSection(UploadOptions.Section).Get<UploadOptions>() ?? new UploadOptions());
builder.Services.Configure<ZarinpalOptions>(builder.Configuration.GetSection(ZarinpalOptions.Section));
builder.Services.Configure<DonationGatewayOptions>(builder.Configuration.GetSection(DonationGatewayOptions.Section));
builder.Services.Configure<McpOptions>(builder.Configuration.GetSection(McpOptions.Section));
builder.Services.Configure<SeedOptions>(builder.Configuration.GetSection(SeedOptions.Section));
builder.Services.Configure<AdminSeedOptions>(builder.Configuration.GetSection(AdminSeedOptions.Section));

// ── App services (plan.md Contracts) ──
builder.Services.AddScoped<IGamePackageValidator, ZipGamePackageValidator>();
builder.Services.AddScoped<IGameService, EfGameService>();
builder.Services.AddScoped<IBlogService, EfBlogService>();
builder.Services.AddScoped<IDonationService, EfDonationService>();
builder.Services.AddScoped<IAuditService, EfAuditService>();
builder.Services.AddScoped<MockGateway>();
builder.Services.AddHttpClient<ZarinpalGateway>();
builder.Services.AddSingleton(sp => new DonationGatewayFactory(sp));
builder.Services.AddSingleton<McpToolRegistry>();

// ── MVC + fa-IR (اعداد/تاریخ فارسی — REQ-001) ──
const string fa = "fa-IR";
builder.Services.Configure<RequestLocalizationOptions>(o =>
    o.SetDefaultCulture(fa).AddSupportedCultures(fa).AddSupportedUICultures(fa));
builder.Services.AddControllersWithViews();

var app = builder.Build();

// ── DB init + Seed (D-13) ──
using (var scope = app.Services.CreateScope())
{
    // SQLite مسیر را نمی‌سازد — دایرکتوری دیتا تضمین شود
    Directory.CreateDirectory(Path.Combine(app.Environment.ContentRootPath, "App_Data"));
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    var webRoot = app.Environment.WebRootPath ?? Path.Combine(app.Environment.ContentRootPath, "wwwroot");
    await DbSeeder.RunAsync(db, scope.ServiceProvider, webRoot);
}

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseRequestLocalization();
app.UseStaticFiles(new StaticFileOptions
{
    OnPrepareResponse = ctx =>
        ctx.Context.Response.Headers["Cache-Control"] = "public,max-age=604800" // ۷ روز — REQ-009-4
});
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
McpEndpoints.Map(app); // REQ-008

app.Run();
