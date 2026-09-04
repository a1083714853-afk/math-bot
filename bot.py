import os
import random
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. Render uyg'otib turuvchi Veb-server ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_health_check_server, daemon=True).start()

# --- 2. Bot Sozlamalari ---
TOKEN = "8748063084:AAGAXuyD6krAGeL1ctleC5GMBDiz_jKSN4M"

def misol_yaratish(sinf):
    if sinf in ["1-sinf", "2-sinf"]:
        a = random.randint(1, 20 if sinf == "1-sinf" else 100)
        b = random.randint(1, 20 if sinf == "1-sinf" else 50)
        amal = random.choice(['+', '-'])
        if amal == '-' and a < b: a, b = b, a
        javob = a + b if amal == '+' else a - b
        return f"{a} {amal} {b} = ?", str(javob)

    elif sinf in ["3-sinf", "4-sinf"]:
        amal = random.choice(['+', '-', '*', '/'])
        if amal in ['+', '-']:
            a, b = random.randint(20, 200), random.randint(10, 100)
            if amal == '-' and a < b: a, b = b, a
            javob = a + b if amal == '+' else a - b
        elif amal == '*':
            a, b = random.randint(2, 10), random.randint(2, 12)
            javob = a * b
        else:
            b = random.randint(2, 10)
            javob = random.randint(2, 10)
            a = b * javob
        return f"{a} {amal} {b} = ?", str(javob)

    elif sinf in ["5-sinf", "6-sinf", "7-sinf", "8-sinf"]:
        tur = random.choice(["oddiy", "daraja"])
        if tur == "oddiy":
            a, b = random.randint(100, 1000), random.randint(50, 500)
            amal = random.choice(['+', '-'])
            if amal == '-' and a < b: a, b = b, a
            javob = a + b if amal == '+' else a - b
            return f"{a} {amal} {b} = ?", str(javob)
        else:
            a = random.randint(2, 10)
            b = random.randint(2, 3)
            javob = a ** b
            return f"{a}^{b} = ?", str(javob)

    else:  # 9, 10, 11-sinflar
        tur = random.choice(["ildiz", "tenglama"])
        if tur == "ildiz":
            javob = random.randint(2, 15)
            a = javob ** 2
            return f"√{a} = ?", str(javob)
        else:
            # x + a = b
            x = random.randint(1, 20)
            a = random.randint(5, 30)
            b = x + a
            return f"x + {a} = {b}\nx = ?", str(x)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sinf_tugmalari = [
        ["1-sinf", "2-sinf", "3-sinf"],
        ["4-sinf", "5-sinf", "6-sinf"],
        ["7-sinf", "8-sinf", "9-sinf"],
        ["10-sinf", "11-sinf"]
    ]
    await update.message.reply_text(
        "Salom! Matematika test botiga xush kelibsiz.\nSinfni tanlang:",
        reply_markup=ReplyKeyboardMarkup(sinf_tugmalari, resize_keyboard=True)
    )

async def javobni_tekshirish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    sinflar = [f"{i}-sinf" for i in range(1, 12)]

    if matn in sinflar:
        context.user_data["sinf"] = matn
        savol, javob = misol_yaratish(matn)
        context.user_data["togri_javob"] = javob
        
        menyu = [["Sinfni o'zgartirish"]]
        await update.message.reply_text(
            f"Sinf: {matn}\n\nMisolni yeching:\n{savol}",
            reply_markup=ReplyKeyboardMarkup(menyu, resize_keyboard=True)
        )

    elif matn == "Sinfni o'zgartirish":
        await start(update, context)

    elif "togri_javob" in context.user_data:
        togri = context.user_data["togri_javob"]
        sinf = context.user_data.get("sinf", "1-sinf")

        if matn.strip() == togri:
            await update.message.reply_text("To'g'ri! Barakalla! 🎉")
        else:
            await update.message.reply_text(f"Noto'g'ri. To'g'ri javob: {togri}")
        
        del context.user_data["togri_javob"]

        savol, javob = misol_yaratish(sinf)
        context.user_data["togri_javob"] = javob
        await update.message.reply_text(f"Keyingi misol:\n\n{savol}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, javobni_tekshirish))
    app.run_polling()

if __name__ == "__main__":
    main()
