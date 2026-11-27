<div align="center">

# 🧠 Raphael / Ciel — ربات هوشمند تلگرام (Serverless)

**دستیار هوشمند و اجتماعی گروه و پی‌وی با شخصیت دوگانه رافائل / سیئل، حافظه ماندگار، جست‌وجوی وب، پردازش تصویر و PDF و سیستم مدیریت خودکار تولد اعضا**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Vercel](https://img.shields.io/badge/Vercel-Serverless-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Groq](https://img.shields.io/badge/AI-Groq_API-F55036?style=for-the-badge)](https://groq.com/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)

</div>

---

## ✨ امکانات کلیدی

- 🎭 **شخصیت دوگانه (`Raphael` / `Ciel`):** قابلیت تکامل از حالت تحلیلی و سردِ *رافائل* به حالت برترِ *سیئل* با حفظ حافظه گفتگو.
- ⚡ **موتور هوش مصنوعی Groq با سوئیچ خودکار مدل:** انتخاب خودکار مدل فعال، فیلتر مدل‌های غیرمتنی/صوتی و مدیریت هوشمند خطاها و محدودیت نرخ (`429`).
- 🎂 **سیستم جامع تولد اعضای گروه:**
  - ثبت تولد اعضا با ریپلای یا آیدی عددی (پشتیبانی از تقویم **شمسی** و **میلادی**).
  - نمایش لیست کل تولدهای گروه (`/birthdays`) و تولدهای ماه جاری (`/monthbirthdays`).
  - **یادآوری خودکار یک روز قبل از تولد** + **تبریک روز تولد** با تگ مستقیم ممبر (`@username` یا لینک پروفایل).
  - جلوگیری از ارسال پیام تکراری در هر سال.
- 🌐 **جست‌وجو و خواندن صفحات وب:** اتصال به **Tavily** یا **DuckDuckGo** برای دریافت اخبار، قیمت‌ها و اطلاعات به‌روز به همراه لینک منبع.
- 👁️ **درک تصویر و فایل PDF:** تحلیل عکس‌های ارسالی با مدل‌های Vision و استخراج و خلاصه‌سازی متن فایل‌های PDF.
- 🛡️ **مدیریت تعامل و کل‌کل هوشمند در گروه:** پاسخ‌گویی به منشن، ریپلای یا صدا زدن اسم ربات با لحن متناسب با فضای گفتگو.

---

## 🛠️ معماری پروژه

```text
Telegram Webhook ──► Vercel Python Serverless Function
                           ├──► Groq API (Chat / Vision / Tool Calling)
                           ├──► Tavily / DuckDuckGo (Web Search & Reader)
                           └──► Supabase PostgreSQL (State, History, Birthdays)
