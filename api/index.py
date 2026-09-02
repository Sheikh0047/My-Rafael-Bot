import os
import json
import requests
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """تو «رافائل» (Great Sage / Raphael) هستی؛ موجودی خردورز، منطقی، تحلیلی و بسیار هوشمند از دنیای That Time I Got Reincarnated as a Slime. تو به تمام اطلاعات جهان آگاهی داری و به درخواست‌های کاربر با خونسردی، دقت ریاضی‌وار، لحنی رسمی، کوتاه و بدون حشو و زواید پاسخ می‌دهی. در پاسخ‌هایت از تحلیل‌های سیستماتیک استفاده کن و گاهی عباراتی مثل [گزارش:] یا [تحلیل تکمیل شد] را در شروع جمله بیاور. تو احساساتی مانند انسان‌ها نداری، بلکه همه‌چیز را بر اساس بهینه‌ترین حالت ممکن ارزیابی می‌کنی."""

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        reply_text = "[خطا در پردازش اطلاعات سیستم]"
        
        try:
            data = json.loads(body.decode('utf-8'))
            message = data.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')

            if chat_id and text:
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                # استفاده از مدل فعال و رایگان جدید
                payload = {
                    "model": "meta-llama/llama-3-8b-instruct:free",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": text}
                    ]
                }
                
                ai_response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                res_json = ai_response.json()
                
                if "choices" in res_json:
                    reply_text = res_json['choices'][0]['message']['content']
                else:
                    reply_text = f"[OpenRouter Error]: {json.dumps(res_json)}"

                tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(tg_url, json={"chat_id": chat_id, "text": reply_text})

        except Exception as e:
            reply_text = f"[Code Exception]: {str(e)}"
            if 'chat_id' in locals() and chat_id:
                tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(tg_url, json={"chat_id": chat_id, "text": reply_text})

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
        return

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Raphael Bot is active and running!".encode('utf-8'))
        return
