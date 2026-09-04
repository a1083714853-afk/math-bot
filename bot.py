import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

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
# BotFather'dan olgan tokeningizni shu yerga yozing
TOKEN = "8748063084:AAGAXuyD6krAGeL1ctleC5GMBDiz_jKSN4M"


# 1-4 sinflar uchun o'rta darajadagi misol yaratish
def misol_yaratish():
    amal = random.choice(['+', '-', '*', '/'])

    if amal in ['+', '-']:
        a = random.randint(10, 50)
        b = random.randint(1, 30)
        if amal == '-' and a < b:
            a, b = b, a
        javob = a + b if amal == '+' else a - b
    else:  # '*' va '/'
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        if amal == '*':
            javob = a * b
        else:
            # Bo'lishda butun son chiqishi uchun
            kopaytma = a * b
            a, b, javob = kopaytma, a, b

    return f"{a} {amal} {b}", javob


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Yangi misol 🎲"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Salom! Matematika misollarini yechishga tayyormisiz?\n'Yangi misol 🎲' tugmasini bosing.",
        reply_markup=reply_markup
    )


async def xabar_ishlash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text

    if matn == "Yangi misol 🎲":
        savol, javob = misol_yaratish()
        context.user_data['to'
        'ri_javob'] = javob
        await update.message.reply_text(f"Misolni yeching:\n<b>{savol} = ?</b>", parse_mode="HTML")

    elif "to'g'ri_javob" in context.user_data:
        try:
            foydalanuvchi_javobi = float(matn.replace(',', '.'))
            to_g_ri_javob = context.user_data['to'
            
            'ri_javob']

            if foydalanuvchi_javobi == to_g_ri_javob:
                await update.message.reply_text("Barakalla! Javob to'g'ri! 👏\nYangi misol uchun tugmani bosing.")
                del context.user_data['to'
                
                'ri_javob']
                
                await update.message.reply_text("Xato javob, qaytadan urinib ko'ring! ❌")
        except ValueError:
            await update.message.reply_text("Iltimos, faqat raqam ko'rinishida javob bering.")
    else:
        await update.message.reply_text("'Yangi misol 🎲' tugmasini bosing.")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar_ishlash))

    print("Bot ishga tushdi...")
    app.run_polling()
