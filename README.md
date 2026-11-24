# Raphael / Ciel v2 (Vercel + Telegram)

نسخه ارتقایافته ربات با شخصیت رافائل/سیئل، حافظه مکالمه، جست‌وجوی وب، خواندن PDF و تحلیل تصویر.

## ساختار
- `api/index.py`: وبهوک تلگرام و هسته هوش مصنوعی
- `requirements.txt`: وابستگی‌ها
- `vercel.json`: تنظیمات تابع
- `supabase.sql`: ساخت جداول حافظه
- `.env.example`: نام متغیرهای محیطی

## 1) نصب روی GitHub / Vercel
1. از پروژه فعلی یک کپی یا Branch پشتیبان بگیر.
2. فایل `api/index.py` را با نسخه این بسته جایگزین کن.
3. `requirements.txt` و `vercel.json` را در ریشه پروژه قرار بده.
4. پروژه را در Vercel دوباره Deploy کن.

## 2) متغیرهای محیطی Vercel
در Project Settings > Environment Variables موارد زیر را تنظیم کن:

ضروری:
- `TELEGRAM_TOKEN`: توکن BotFather
- `OPENROUTER_API_KEY`: کلید OpenRouter

پیشنهادی:
- `OPENROUTER_MODEL`: مقدار `openrouter/free`
- `BOT_USERNAME`: نام ربات بدون @
- `TELEGRAM_WEBHOOK_SECRET`: یک رشته تصادفی طولانی (فقط حروف/عدد/underscore)
- `PUBLIC_APP_URL`: آدرس Deployment، مثل `https://your-project.vercel.app`
- `MAX_HISTORY`: تعداد پیام‌های قبلی، پیش‌فرض 16

برای حافظه دائمی:
- `SUPABASE_URL`: آدرس پروژه Supabase
- `SUPABASE_SERVICE_ROLE_KEY`: کلید service_role پروژه (فقط در Vercel، هرگز در کد یا GitHub قرار نده)

برای جست‌وجوی بهتر:
- `TAVILY_API_KEY`: کلید Tavily. در صورت نبود این کلید، کد از fallback ساده DuckDuckGo HTML استفاده می‌کند که تضمین پایداری ندارد.

## 3) ساخت دیتابیس حافظه در Supabase
در Supabase > SQL Editor محتوای `supabase.sql` را اجرا کن.
سپس `SUPABASE_URL` و `SUPABASE_SERVICE_ROLE_KEY` را در Vercel تنظیم کن.
کلید service_role محرمانه است و نباید در کلاینت یا مخزن عمومی باشد.

بدون Supabase، ربات همچنان کار می‌کند اما حافظه پایدار و وضعیت مستقل هر چت فعال نخواهد بود.

## 4) تنظیم Webhook تلگرام
بعد از Deploy، آدرس تابع معمولاً این است:
`https://YOUR-PROJECT.vercel.app/api`

در مرورگر یا با curl، وبهوک را تنظیم کن (مقادیر را جایگزین کن):
`https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://YOUR-PROJECT.vercel.app/api&secret_token=<TELEGRAM_WEBHOOK_SECRET>`

اگر `TELEGRAM_WEBHOOK_SECRET` تنظیم نکردی، پارامتر `secret_token` را هم حذف کن.
توکن واقعی را در لینک یا پیام عمومی منتشر نکن.

## 5) فرمان‌ها
- `/start` شروع و راهنما
- `/status` وضعیت سیستم
- `/evolve` تکامل به سیئل
- `/raphael` بازگشت به رافائل
- `/shutdown` توقف پاسخ‌گویی
- `/reset` پاک‌کردن تاریخچه مکالمه همان چت

در گروه، ربات به فرمان‌ها، منشن یا پاسخ به پیام خودش واکنش نشان می‌دهد. برای منشن، `BOT_USERNAME` را تنظیم کن.

## قابلیت‌ها و محدودیت‌ها
- حافظه مکالمه و وضعیت رافائل/سیئل: با Supabase پایدار می‌شود.
- جست‌وجو: با Tavily بهتر و پایدارتر است؛ fallback رایگان DuckDuckGo ممکن است تغییر کند یا محدود شود.
- تصویر: عکس تلگرام به مدل ارسال می‌شود؛ مدل انتخاب‌شده باید بینایی داشته باشد.
- PDF: استخراج متن از PDFهای متنی؛ PDF اسکن‌شده نیازمند OCR جداگانه است.
- ابزارها: جست‌وجو و خواندن صفحات HTTPS. اجرای کد دلخواه، shell، ارسال پیام به دیگران یا دسترسی نامحدود به اینترنت عمداً پیاده‌سازی نشده است.
- `openrouter/free` رایگان است اما محدودیت سهمیه و دسترس‌پذیری مدل‌ها دارد. پشتیبانی ابزار/تصویر به مدل انتخاب‌شده بستگی دارد.
- تابع Vercel زمان اجرای محدود دارد؛ جست‌وجوهای خیلی طولانی یا فایل‌های بزرگ ممکن است timeout شوند.

## امنیت
- هیچ API key یا توکن را در GitHub commit نکن.
- از کلید Supabase `service_role` فقط به‌عنوان Environment Variable در سرور استفاده کن.
- برای استفاده عمومی، بهتر است دسترسی فرمان‌های مدیریتی را با `OWNER_TELEGRAM_ID` محدود کنی و محدودیت نرخ درخواست اضافه کنی.
