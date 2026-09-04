import os
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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
    if sinf == "1-sinf":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        amal = random.choice(['+', '-'])
        if amal == '-' and a < b:
            a, b = b, a
        javob = a + b if amal == '+' else a - b
    elif sinf == "2-sinf":
        a = random.randint(10, 50)
        b = random.randint(1, 30)
        amal = random.choice(['+', '-'])
        if amal == '-' and a < b:
            a, b = b, a
        javob = a + b if amal == '+' else a - b
    elif sinf == "3-sinf":
        amal = random.choice(['+', '-', '*'])
        if amal in ['+', '-']:
            a, b = random.randint(20, 100), random.randint(10, 50)
            if amal == '-' and a < b: a, b = b, a
            javob = a + b if amal == '+' else a - b
        else:
            a, b = random.randint(2, 9), random.randint(2, 9)
            javob = a * b
    else:  # 4-sinf
        amal = random.choice(['+', '-', '*', '/'])
        if amal in ['+', '-']:
            a, b = random.randint(100, 500), random.randint(50, 200)
            if amal == '-' and a < b: a, b = b, a
            javob = a + b if amal == '+' else a - b
        elif amal == '*':
            a, b = random.randint(5, 15), random.randint(2, 10)
            javob = a * b
        else:
            b = random.randint(2, 10)
            javob = random.randint(2, 10)
            a = b * javob

    return f"{a} {amal} {b} = ?", str(javob)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sinf_tugmalari = [
        ["1-sinf", "2-sinf"],
        ["3-sinf", "4-sinf"]
    ]
    await update.message.reply_text(
        "Salom! Matematika test botiga xush kelibsiz.\nIltimos, sinfni tanlang:",
        reply_markup=ReplyKeyboardMarkup(sinf_tugmalari, resize_keyboard=True)
    )

async def javobni_tekshirish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text

    # Sinf tanlangan bo'lsa
    if matn in ["1-sinf", "2-sinf", "3-sinf", "4-sinf"]:
        context.user_data["sinf"] = matn
        savol, javob = misol_yaratish(matn)
        context.user_data["togri_javob"] = javob
        
        menyu = [["Sinfni o'zgartirish"]]
        await update.message.reply_text(
            f"Sinf: {matn}\n\nMisolni yeching:\n{savol}",
            reply_markup=ReplyKeyboardMarkup(menyu, resize_keyboard=True)
        )

    # Sinfni o'zgartirish tugmasi bosilsa
    elif matn == "Sinfni o'zgartirish":
        await start(update, context)

    # Foydalanuvchi javob yuborganda
    elif "togri_javob" in context.user_data:
        togri = context.user_data["togri_javob"]
        sinf = context.user_data.get("sinf", "1-sinf")

        if matn.strip() == togri:
            await update.message.reply_text("To'g'ri! Barakalla! 🎉")
        else:
            await update.message.reply_text(f"Noto'g'ri. To'g'ri javob: {togri}")
        
        del context.user_data["togri_javob"]

        # Yangi misol berish
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
