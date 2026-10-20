using Microsoft.Extensions.Logging;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using WorldOfGames.Core.Common;
using WorldOfGames.Core.Entities;
using WorldOfGames.Core.Interfaces;
using WorldOfGames.Infrastructure.Data;
using WorldOfGames.Infrastructure.Options;

namespace WorldOfGames.Infrastructure.Services;

public sealed class EfDonationService(
    AppDbContext db,
    DonationGatewayFactory gatewayFactory,
    IOptions<DonationGatewayOptions> gatewayOptions,
    ILogger<EfDonationService> logger) : IDonationService
{
    private const long MinAmount = 10_000;      // ۱ هزار تومان
    private const long MaxAmount = 2_000_000_000; // سقف ایمن

    public async Task<OpResult<DonationStart>> StartAsync(DonationInput input, string callbackBaseUrl)
    {
        if (input.AmountRial < MinAmount) return OpResult<DonationStart>.Fail("حداقل مبلغ دونیت ۱۰٬۰۰۰ ریال است.");
        if (input.AmountRial > MaxAmount) return OpResult<DonationStart>.Fail("مبلغ واردشده بیش از حد مجاز است.");
        if (!string.IsNullOrWhiteSpace(input.DonorName) && input.DonorName.Trim().Length > 60)
            return OpResult<DonationStart>.Fail("نام حامی حداکثر ۶۰ نویسه است.");
        if (!string.IsNullOrWhiteSpace(input.Message) && input.Message.Trim().Length > 300)
            return OpResult<DonationStart>.Fail("پیام حامی حداکثر ۳۰۰ نویسه است.");

        var gateway = gatewayFactory.Resolve(gatewayOptions.Value.Gateway);
        var donation = new Donation
        {
            Gateway = gateway.Name,
            AmountRial = input.AmountRial,
            DonorName = string.IsNullOrWhiteSpace(input.DonorName) ? null : input.DonorName.Trim(),
            Message = string.IsNullOrWhiteSpace(input.Message) ? null : input.Message.Trim(),
            IsAnonymous = input.IsAnonymous
        };

        var callbackUrl = callbackBaseUrl.TrimEnd('/') + "/Donations/Callback";
        var result = await gateway.CreatePaymentAsync(input.AmountRial, callbackUrl,
            $"حمایت از پلتفرم World of Games — #{donation.CreatedAt:yyyyMMddHHmmss}");
        if (!result.Success || string.IsNullOrEmpty(result.Authority) || string.IsNullOrEmpty(result.RedirectUrl))
            return OpResult<DonationStart>.Fail(result.Error ?? "ایجاد پرداخت ناموفق بود.");

        donation.Authority = result.Authority;
        db.Donations.Add(donation);
        await db.SaveChangesAsync();
        return OpResult<DonationStart>.Ok(new DonationStart(donation, result.RedirectUrl!));
    }

    public async Task<OpResult<Donation>> CompleteFromCallbackAsync(string authority, string? gatewayStatus)
    {
        if (string.IsNullOrWhiteSpace(authority)) return OpResult<Donation>.Fail("شناسه پرداخت نامعتبر است.");
        var donation = await db.Donations.FirstOrDefaultAsync(d => d.Authority == authority);
        if (donation is null) return OpResult<Donation>.Fail("تراکنش یافت نشد."); // REQ-006-2
        if (donation.Status == DonationStatus.Paid) return OpResult<Donation>.Ok(donation); // idempotent

        // کاربر پرداخت را لغو کرد / دروازه NOK برگرداند — بدون Verify (رفتار واقعی زرین‌پال هم همین است)
        if (string.Equals(gatewayStatus, "NOK", StringComparison.OrdinalIgnoreCase))
        {
            donation.Status = DonationStatus.Failed;
            await db.SaveChangesAsync();
            return OpResult<Donation>.Fail("پرداخت ناموفق بود یا لغو شد.");
        }

        var gateway = gatewayFactory.Resolve(donation.Gateway);
        var verify = await gateway.VerifyAsync(authority, donation.AmountRial);
        if (!verify.Success)
        {
            donation.Status = DonationStatus.Failed;
            donation.RefId = verify.RefId;
            await db.SaveChangesAsync();
            logger.LogInformation("Donation {Id} failed: {Msg}", donation.Id, verify.Error);
            return OpResult<Donation>.Fail(verify.Error ?? "پرداخت تأیید نشد.");
        }

        donation.Status = DonationStatus.Paid;
        donation.RefId = verify.RefId;
        donation.PaidAt = DateTime.UtcNow;
        await db.SaveChangesAsync();
        return OpResult<Donation>.Ok(donation);
    }

    public Task<Donation?> GetByAuthorityAsync(string authority) =>
        db.Donations.AsNoTracking().FirstOrDefaultAsync(d => d.Authority == authority);

    public async Task<PagedResult<Donation>> ListAdminAsync(int page, int pageSize)
    {
        page = Math.Max(1, page);
        pageSize = pageSize is > 0 and <= 100 ? pageSize : 20;
        var query = db.Donations.AsNoTracking().OrderByDescending(d => d.CreatedAt).ThenByDescending(d => d.Id);
        var total = await query.CountAsync();
        var items = await query.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
        return new PagedResult<Donation>(items, total, page, pageSize);
    }

    /// <summary>حامیان عمومی — بدون مبلغ فردی؛ ناشناس‌ها «حامی ناشناس» نمایش داده می‌شوند (REQ-006-3).</summary>
    public async Task<IReadOnlyList<Donation>> ListPaidPublicAsync(int count) =>
        await db.Donations.AsNoTracking().Where(d => d.Status == DonationStatus.Paid)
            .OrderByDescending(d => d.PaidAt).Take(Math.Min(count, 50)).ToListAsync();

    public Task<long> SumPaidAsync() =>
        db.Donations.AsNoTracking().Where(d => d.Status == DonationStatus.Paid).SumAsync(d => d.AmountRial);

    public Task<int> CountPaidAsync() =>
        db.Donations.AsNoTracking().CountAsync(d => d.Status == DonationStatus.Paid);
}
