using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using WorldOfGames.Infrastructure.Data;
using WorldOfGames.Web.Models;

namespace WorldOfGames.Web.Controllers;

public class AccountController(UserManager<ApplicationUser> userManager, SignInManager<ApplicationUser> signIn) : Controller
{
    [HttpGet("Account/Login")]
    public IActionResult Login(string? returnUrl = null) => View(new LoginVm());

    [HttpPost("Account/Login")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Login(LoginVm vm, string? returnUrl = null)
    {
        if (!ModelState.IsValid) return View(vm);
        var user = await userManager.FindByEmailAsync(vm.Email);
        if (user is null)
            return View(vm with { ErrorMessage = "کاربری با این ایمیل یافت نشد." });
        var result = await signIn.PasswordSignInAsync(user, vm.Password, vm.RememberMe, lockoutOnFailure: true);
        if (result.Succeeded)
            return LocalRedirect(string.IsNullOrEmpty(returnUrl) ? "/" : returnUrl);
        if (result.IsLockedOut)
            return View(vm with { ErrorMessage = "حساب شما موقتاً قفل شده است؛ چند دقیقه بعد تلاش کنید." });
        return View(vm with { ErrorMessage = "رمز عبور نادرست است." });
    }

    [HttpGet("Account/Register")]
    public IActionResult Register() => View(new RegisterVm());

    [HttpPost("Account/Register")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Register(RegisterVm vm)
    {
        if (!ModelState.IsValid) return View(vm);
        var user = new ApplicationUser
        {
            UserName = vm.Email,
            Email = vm.Email,
            EmailConfirmed = true, // MVP: بدون ایمیل‌سرویس؛ Known limitation در spec
            DisplayName = vm.DisplayName
        };
        var result = await userManager.CreateAsync(user, vm.Password);
        if (!result.Succeeded)
        {
            var msg = string.Join(" ", result.Errors.Select(e => e.Description));
            ModelState.AddModelError(string.Empty, msg);
            return View(vm);
        }
        await userManager.AddToRoleAsync(user, "User");
        await signIn.SignInAsync(user, isPersistent: false);
        return RedirectToAction("Index", "Home");
    }

    [HttpPost("Account/Logout")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Logout()
    {
        await signIn.SignOutAsync();
        return RedirectToAction("Index", "Home");
    }

    [HttpGet("Account/AccessDenied")]
    public IActionResult AccessDenied() => View();
}
