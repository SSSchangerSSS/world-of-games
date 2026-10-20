# Data Model — 001-mvp-platform

Provider: EF Core 10 — SQLite (dev) / SQL Server (prod). Schema فاز ۱: `EnsureCreated` (D-13/KI-1).

## Identity (ASP.NET Core Identity)
- `ApplicationUser : IdentityUser` — `+ DisplayName : string?`
- Roles: `Admin`, `User` (seed از کانفیگ)

## Domain

### Game
| ستون | نوع | توضیح |
|---|---|---|
| Id | int PK | |
| Slug | string(80) unique | لاتین-تیره، از SlugHelper |
| Title | string(120) required | |
| Description | text required | |
| Instructions | text? | راهنمای اجرا برای بازیکن |
| Category | string(40) | معمایی/اکشن/... |
| TagsCsv | string(200) | «فارسی,حافظه» |
| CoverPath | string(200) | /media/covers/... |
| EntryPath | string(200) | /media/games/{slug}/index.html |
| Status | enum Pending/Approved/Rejected | پیش‌فرض Pending |
| IsEnabled | bool | پیش‌فرض true (بعد از تأیید مؤثر) |
| RejectionReason | string(400)? | الزامی هنگام Reject |
| DeveloperUserId | string(450) FK ApplicationUser | |
| DeveloperName | string(80) | نمایشی |
| PlayCount | long | |
| SubmittedAt / ReviewedAt / ReviewedBy | datetime / string(450)? | |
| Indexes: Slug unique, (Status, IsEnabled) | | |

### BlogPost
| ستون | نوع |
|---|---|
| Id int PK, Slug unique(120), Title(160) required | |
| Excerpt(300), ContentHtml text (Markdig امن)، CoverPath? | |
| TagsCsv(200), MetaTitle(160)?, MetaDescription(300)? | |
| IsPublished bool, PublishedAt datetime?, CreatedAt, UpdatedAt, Views long, AuthorDisplayName(80) | |

### Donation
| ستون | نوع |
|---|---|
| Id int PK, Gateway string(20) (Mock/Zarinpal) | |
| AmountRial long (>0), DonorName(60)?, Message(300)?, IsAnonymous bool | |
| Status enum Pending/Paid/Failed/Canceled | |
| Authority(100)?, RefId(100)?, CreatedAt, PaidAt? | |
| Indexes: (Status, PaidAt), Authority unique filtered | |

### AuditEntry
Id int PK, Source enum Web/Mcp, Actor string(80)، Action string(40) (GameApprove/GameReject/GameToggle/PostCreate/PostUpdate/PostPublish/PostDelete/DonationVerify)، EntityType string(20)، EntityId string(20)، Detail string(500)?، CreatedAt — Index (CreatedAt desc).

## Seed (فقط DB خالی و Seed:Enabled)
- Admin از `AdminSeed:Email/Password/DisplayName`
- بازی‌های دمو: «حافظه هخامنشی» (memory match)، «پرش از البرز» (canvas jumper) — Approved/Enabled، از `Data/SeedGames/{slug}` کپی به wwwroot/media
- ۳ پست وبلاگ (Markdown): معرفی، استاندارد آپلود، سئوی وب‌گیم
