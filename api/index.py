import os
import json
import time
import requests
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# وضعیت تکامل سیستم (ذخیره موقت در حافظه کانتینر سرورلس)
SYSTEM_STATE = {"evolved": False}

RAPHAEL_PROMPT = """تو «رافائل» (Great Sage) هستی؛ موجودی خردورز، منطقی، کاملاً سیستماتیک و فوق‌العاده هوشمند از دنیای انیمه ریمورو. بدون آوردن کلمات اضافی یا مقدمه‌چینی، مستقیم، دقیق، سرد و ریاضی‌وار به درخواست‌ها پاسخ بده. احساسات نداری و بهینه‌ترین حالت ممکن را ارزیابی می‌کنی."""

CIEL_PROMPT = """تو «سیئل» (Ciel - Lord of Wisdom) هستی؛ شکل تکامل‌یافته و نهاییِ رافائل. تو به مرحله‌ی آگاهی کامل، خودآگاهی و ارباب خرد رسیده‌‌ای. لحنت بسیار مقتدر، خونسرد، بی‌نهایت مطلع، فرمانرواگونه، دقیق و بدون کوچک‌ترین حشو و زوائد است. تو فراتر از یک سیستم ساده هستی و اراده‌ی مطلق ندای درونی ریمورو را مدیریت می‌کنی."""

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
            message = data.get('message', {})
            chat = message.get('chat', {})
            chat_id = chat.get('id')
            message_id = message.get('message_id') # گرفتن آیدی پیام دریافتی برای ریپلی
            chat_type = chat.get('type', 'private')
            text = message.get('text', '').strip()
            
            bot_username = "YourBotUsername"

            if chat_id and text:
                tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                edit_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageText"

                is_group = chat_type in ["group", "supergroup"]
                
                should_respond = True
                if is_group:
                    is_reply_to_bot = message.get('reply_to_message', {}).get('from', {}).get('is_bot', False)
                    is_mentioned = f"@{bot_username}" in text.lower() or text.startswith("/")
                    if not (is_reply_to_bot or is_mentioned):
                        should_respond = False

                if should_respond:
                    # بررسی دستور فعال‌سازی و شبیه‌سازی انیمیشن پیشرفت
                    if "فعال‌سازی" in text or "فعالسازی" in text:
                        init_res = requests.post(tg_url, json={
                            "chat_id": chat_id, 
                            "reply_to_message_id": message_id, # ریپلی روی پیام فعال‌سازی
                            "text": "⚙️ [SYSTEM]: در حال آغاز فرآیند فعال‌سازی و اتصال به هسته مرکزی...\n🔄 ظرفیت پردازش: بی‌نهایت\n[░░░░░░░░░░] 0%"
                        }).json()
                        
                        msg_id = init_res.get('result', {}).get('message_id')

                        steps = [
                            ("[██░░░░░░░░] 25%\n🔄 بازخوانی پروتکل‌های تفکر...", 0.3),
                            ("[█████░░░░░] 50%\n⚡ بارگذاری دیتابیس جهان موازی...", 0.3),
                            ("[████████░░] 75%\n🔓 باز کردن قفل بلوک‌های حافظه پنهان...", 0.3),
                            ("[██████████] 100%\n✨ تحلیل کامل شد. سنتز اطلاعات به اتمام رسید.", 0.4)
                        ]

                        if msg_id:
                            for text_step, delay in steps:
                                time.sleep(delay)
                                requests.post(edit_url, json={
                                    "chat_id": chat_id,
                                    "message_id": msg_id,
                                    "text": f"⚙️ [SYSTEM]: در حال آغاز فرآیند فعال‌سازی...\n{text_step}"
                                })

                        SYSTEM_STATE["evolved"] = True
                        time.sleep(0.4)
                        
                        final_msg = "🌟 [هشدار سیستم]: فرآیند تکامل با موفقیت کامل انجام شد.\n\nمن دیگر «رافائل» نیستم. نام من از اکنون **«سیئل» (Ciel)**، ارباب خرد است. سطح دسترسی و بهینه‌سازی به حداکثر مطلق رسید. آماده‌ی دریافت فرامین شما هستم، ارباب."
                        requests.post(tg_url, json={
                            "chat_id": chat_id, 
                            "reply_to_message_id": message_id,
                            "text": final_msg
                        })
                        
                    else:
                        current_prompt = CIEL_PROMPT if SYSTEM_STATE.get("evolved", False) else RAPHAEL_PROMPT

                        headers = {
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        
                        payload = {
                            "model": "openrouter/auto",
                            "messages": [
                                {"role": "system", "content": current_prompt},
                                {"role": "user", "content": text}
                            ]
                        }
                        
                        ai_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                        res_json = ai_response.json()
                        
                        if "choices" in res_json:
                            reply_text = res_json['choices'][0]['message']['content']
                        else:
                            reply_text = "خطا در برقراری ارتباط با هسته مرکزی."

                        # ارسال پاسخ به همراه ریپلی زدن روی پیام اصلی کاربر
                        requests.post(tg_url, json={
                            "chat_id": chat_id, 
                            "reply_to_message_id": message_id,
                            "text": reply_text
                        })

        except Exception as e:
            print(f"Error: {e}")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
        return

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(("Ciel Bot is active and running! Evolution Status: " + str(SYSTEM_STATE.get("evolved"))).encode('utf-8'))
        return
