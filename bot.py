import os
import random
from flask import Flask
from threading import Thread

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)


# =========================================================
# 1. FLASK SERVER - RENDER UCHUN
# =========================================================

app_flask = Flask(__name__)


@app_flask.route("/")
def home():
    return "Matematika boti ishlayapti! 🤖"


def run_flask():
    port = int(os.environ.get("PORT", 8080))

    app_flask.run(
        host="0.0.0.0",
        port=port
    )


def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()


# =========================================================
# 2. BOT SOZLAMALARI
# =========================================================

TOKEN = "8748063084:AAEE-P33fEOkEKLcdDTURLm944UMYLI1bsA"


# =========================================================
# 3. MATEMATIK MISOL YARATISH
# =========================================================

def misol_yaratish(sinf):

    # -------------------------
    # 1-2 SINFLAR
    # -------------------------

    if sinf in ["1-sinf", "2-sinf"]:

        a = random.randint(
            1,
            20 if sinf == "1-sinf" else 100
        )

        b = random.randint(
            1,
            20 if sinf == "1-sinf" else 50
        )

        amal = random.choice(["+", "-"])

        if amal == "-" and a < b:
            a, b = b, a

        if amal == "+":
            javob = a + b
        else:
            javob = a - b

        savol = f"{a} {amal} {b} = ?"


    # -------------------------
    # 3-4 SINFLAR
    # -------------------------

    elif sinf in ["3-sinf", "4-sinf"]:

        amal = random.choice(["+", "-", "*", "/"])

        if amal in ["+", "-"]:

            a = random.randint(20, 200)
            b = random.randint(10, 100)

            if amal == "-" and a < b:
                a, b = b, a

            if amal == "+":
                javob = a + b
            else:
                javob = a - b

        elif amal == "*":

            a = random.randint(2, 10)
            b = random.randint(2, 12)

            javob = a * b

        else:

            b = random.randint(2, 10)
            javob = random.randint(2, 10)

            a = b * javob

        savol = f"{a} {amal} {b} = ?"


    # -------------------------
    # 5-8 SINFLAR
    # -------------------------

    elif sinf in [
        "5-sinf",
        "6-sinf",
        "7-sinf",
        "8-sinf"
    ]:

        tur = random.choice([
            "oddiy",
            "daraja"
        ])

        if tur == "oddiy":

            a = random.randint(100, 1000)
            b = random.randint(50, 500)

            amal = random.choice(["+", "-"])

            if amal == "-" and a < b:
                a, b = b, a

            if amal == "+":
                javob = a + b
            else:
                javob = a - b

            savol = f"{a} {amal} {b} = ?"

        else:

            a = random.randint(2, 10)
            b = random.randint(2, 3)

            javob = a ** b

            savol = f"{a}^{b} = ?"


    # -------------------------
    # 9-11 SINFLAR
    # -------------------------

    else:

        tur = random.choice([
            "ildiz",
            "tenglama"
        ])

        if tur == "ildiz":

            javob = random.randint(2, 15)

            a = javob ** 2

            savol = f"√{a} = ?"

        else:

            x = random.randint(1, 20)

            a = random.randint(5, 30)

            b = x + a

            javob = x

            savol = (
                f"x + {a} = {b}\n"
                f"x = ?"
            )


    # =====================================================
    # 4 TA JAVOB VARIANTI
    # =====================================================

    variantlar = {javob}

    while len(variantlar) < 4:

        fark = random.choice([
            -3,
            -2,
            -1,
            1,
            2,
            3,
            4,
            5
        ])

        notogri = javob + fark

        if notogri >= 0:
            variantlar.add(notogri)

    variant_list = [
        str(v)
        for v in variantlar
    ]

    random.shuffle(variant_list)

    return (
        savol,
        str(javob),
        variant_list
    )


# =========================================================
# 4. /START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    sinf_tugmalari = [

        [
            "1-sinf",
            "2-sinf",
            "3-sinf"
        ],

        [
            "4-sinf",
            "5-sinf",
            "6-sinf"
        ],

        [
            "7-sinf",
            "8-sinf",
            "9-sinf"
        ],

        [
            "10-sinf",
            "11-sinf"
        ]

    ]

    await update.message.reply_text(

        "👋 Salom!\n\n"
        "📚 O'zingizga mos sinfni tanlang:",

        reply_markup=ReplyKeyboardMarkup(
            sinf_tugmalari,
            resize_keyboard=True
        )
    )


# =========================================================
# 5. MISOL YUBORISH
# =========================================================

async def misol_yuborish(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    sinf: str
):

    savol, javob, variantlar = misol_yaratish(sinf)

    # To'g'ri javobni saqlash
    context.user_data["togri_javob"] = javob

    # Variantlarni saqlash
    context.user_data["variantlar"] = variantlar

    # Tugmalar
    tugmalar = [
        [v]
        for v in variantlar
    ]

    tugmalar.append([
        "Sinfni o'zgartirish 🔄"
    ])

    matn = (
        f"📚 <b>{sinf}</b>\n\n"
        "🧮 Misolni yeching va "
        "to'g'ri variantni tanlang:\n\n"
        f"<b>{savol}</b>"
    )

    await update.message.reply_text(

        matn,

        parse_mode="HTML",

        reply_markup=ReplyKeyboardMarkup(
            tugmalar,
            resize_keyboard=True
        )
    )


# =========================================================
# 6. JAVOBNI TEKSHIRISH
# =========================================================

async def javobni_tekshirish(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    matn = update.message.text

    # Sinflar
    sinflar = [
        f"{i}-sinf"
        for i in range(1, 12)
    ]


    # =====================================================
    # SINFLARDAN BIRINI TANLASH
    # =====================================================

    if matn in sinflar:

        context.user_data["sinf"] = matn

        await misol_yuborish(
            update,
            context,
            matn
        )


    # =====================================================
    # SINFNI O'ZGARTIRISH
    # =====================================================

    elif matn == "Sinfni o'zgartirish 🔄":

        await start(
            update,
            context
        )


    # =====================================================
    # JAVOBNI TEKSHIRISH
    # =====================================================

    elif "togri_javob" in context.user_data:

        togri = context.user_data[
            "togri_javob"
        ]

        variantlar = context.user_data.get(
            "variantlar",
            []
        )

        sinf = context.user_data.get(
            "sinf",
            "1-sinf"
        )


        # Faqat variantlardan biri tanlangan bo'lsa
        if matn in variantlar:

            # -------------------------
            # TO'G'RI JAVOB
            # -------------------------

            if matn == togri:

                await update.message.reply_text(
                    "✅ <b>To'g'ri!</b>\n\n"
                    "🎉 Barakalla!",
                    parse_mode="HTML"
                )

                # Keyingi misol
                await misol_yuborish(
                    update,
                    context,
                    sinf
                )


            # -------------------------
            # NOTO'G'RI JAVOB
            # -------------------------

            else:

                await update.message.reply_text(
                    "❌ <b>Noto'g'ri!</b>\n\n"
                    "🔄 Qayta urinib ko'ring!",
                    parse_mode="HTML"
                )


# =========================================================
# 7. BOTNI ISHGA TUSHIRISH
# =========================================================

def main():

    # Flask serverni ishga tushirish
    keep_alive()

    # Telegram bot
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    # /start
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # Oddiy matn va tugmalar
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            javobni_tekshirish
        )
    )

    print("🤖 Telegram bot ishga tushdi!")
    print("🌐 Flask server ham ishga tushdi!")

    application.run_polling()


# =========================================================
# 8. START
# =========================================================

if __name__ == "__main__":
    main()
