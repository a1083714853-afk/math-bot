import os
import random
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
TOKEN = "8748063084:AAF9AGc9MFexVX7BteVtAdLDpbPUh_WPKtI"

def misol_yaratish(sinf):
    if sinf in ["1-sinf", "2-sinf"]:
        a = random.randint(1, 20 if sinf == "1-sinf" else 100)
        b = random.randint(1, 20 if sinf == "1-sinf" else 50)
        amal = random.choice(['+', '-'])
        if amal == '-' and a < b: a, b = b, a
        javob = a + b if amal == '+' else a - b
        savol = f"{a} {amal} {b} = ?"

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
        savol = f"{a} {amal} {b} = ?"

    elif sinf in ["5-sinf", "6-sinf", "7-sinf", "8-sinf"]:
        tur = random.choice(["oddiy", "daraja"])
        if tur == "oddiy":
            a, b = random.randint(100, 1000), random.randint(50, 500)
            amal = random.choice(['+', '-'])
            if amal == '-' and a < b: a, b = b, a
            javob = a + b if amal == '+' else a - b
            savol = f"{a} {amal} {b} = ?"
        else:
            a, b = random.randint(2, 10), random.randint(2, 3)
            javob = a ** b
            savol = f"{a}^{b} = ?"

    else:  # 9, 10, 11-sinflar
        tur = random.choice(["ildiz", "tenglama"])
        if tur == "ildiz":
            javob = random.randint(2, 15)
            a = javob ** 2
            savol = f"√{a} = ?"
        else:
            x = random.randint(1, 20)
            a = random.randint(5, 30)
            b = x + a
            javob = x
            savol = f"x + {a} = {b}\nx = ?"

    variantlar = {javob}
    while len(variantlar) < 4:
        fark = random.choice([-3, -2, -1, 1, 2, 3, 4, 5])
        notogri = javob + fark
        if notogri >= 0:
            variantlar.add(notogri)
    
    variant_list = [str(v) for v in variantlar]
    random.shuffle(variant_list)
    
    return savol, str(javob), variant_list

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sinf_tugmalari = [
        ["1-sinf", "2-sinf", "3-sinf"],
        ["4-sinf", "5-sinf", "6-sinf"],
        ["7-sinf", "8-sinf", "9-sinf"],
        ["10-sinf", "11-sinf"]
    ]
    await update.message.reply_text(
        "Salom! O'zingizga mos sinfni tanlang:",
        reply_markup=ReplyKeyboardMarkup(sinf_tugmalari, resize_keyboard=True)
    )

async def misol_yuborish(update: Update, context: ContextTypes.DEFAULT_TYPE, sinf: str):
    savol, javob, variantlar = misol_yaratish(sinf)
    context.user_data["togri_javob"] = javob
    context.user_data["variantlar"] = variantlar
    
    tugmalar = [[v] for v in variantlar]
    tugmalar.append(["Sinfni o'zgartirish 🔄"])

    matn = f"<b>{sinf}</b>\n\nMisolni yeching va to'g'ri variantni tanlang:\n<b>{savol}</b>"
    await update.message.reply_text(
        matn,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
    )

async def javobni_tekshirish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    sinflar = [f"{i}-sinf" for i in range(1, 12)]

    if matn in sinflar:
        context.user_data["sinf"] = matn
        await misol_yuborish(update, context, matn)

    elif matn == "Sinfni o'zgartirish 🔄":
        await start(update, context)

    elif "togri_javob" in context.user_data:
        togri = context.user_data["togri_javob"]
        variantlar = context.user_data.get("variantlar", [])
        sinf = context.user_data.get("sinf", "1-sinf")

        if matn in variantlar:
            if matn == togri:
                await update.message.reply_text("To'g'ri! Barakalla! 🎉")
                # To'g'ri topsagina keyingi misolga o'tadi
                await misol_yuborish(update, context, sinf)
            else:
                # Noto'g'ri bo'lsa qayta urinishni so'raydi
                await update.message.reply_text("Noto'g'ri ❌ Qayta urinib ko'ring!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, javobni_tekshirish))
    app.run_polling()

if __name__ == "__main__":
    main()
