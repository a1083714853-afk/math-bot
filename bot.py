import os
import random
from flask import Flask
from threading import Thread
import google.generativeai as genai

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
    app_flask.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()


# =========================================================
# 2. BOT VA AI SOZLAMALARI
# =========================================================

TOKEN = os.environ.get("BOT_TOKEN", "8748063084:AAEE-P33fEOkEKLcdDTURLm944UMYLI1bsA")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6J1eeka3V0fFxh0IwqytXOyxQVpQLPwjyYVz0qLbj1dIA")

genai.configure(api_key=GEMINI_API_KEY)

ai_model = genai.GenerativeModel("gemini-1.5-flash")


# =========================================================
# 3. MISOL YARATISH
# =========================================================

def misol_yaratish(sinf):
    sinf_raqami = int(sinf.split("-")[0])

    if sinf_raqami <= 2:
        a = random.randint(1, 20)
        b = random.randint(1, 10)
        amal = random.choice(["+", "-"])
        if amal == "-" and a < b:
            a, b = b, a
        javob = a + b if amal == "+" else a - b

    elif sinf_raqami <= 4:
        a = random.randint(10, 50)
        b = random.randint(2, 10)
        amal = random.choice(["+", "-", "*"])
        if amal == "+":
            javob = a + b
        elif amal == "-":
            if a < b:
                a, b = b, a
            javob = a - b
        else:
            javob = a * b

    elif sinf_raqami <= 8:
        a = random.randint(50, 200)
        b = random.randint(10, 50)
        amal = random.choice(["+", "-", "*", "/"])
        if amal == "+":
            javob = a + b
        elif amal == "-":
            if a < b:
                a, b = b, a
            javob = a - b
        elif amal == "*":
            a = random.randint(5, 15)
            b = random.randint(2, 10)
            javob = a * b
        else:
            b = random.randint(2, 10)
            javob = random.randint(2, 10)
            a = b * javob

    else:
        if random.choice([True, False]):
            javob = random.randint(2, 12)
            a = javob ** 2
            savol = f"√{a} = ?"
            variantlar = {javob}
            while len(variantlar) < 4:
                notogri = javob + random.choice([-3, -2, -1, 1, 2, 3])
                if notogri >= 0:
                    variantlar.add(notogri)
            variant_list = [str(v) for v in variantlar]
            random.shuffle(variant_list)
            return savol, str(javob), variant_list
        else:
            a = random.randint(2, 8)
            b = random.randint(2, 3)
            javob = a ** b
            savol = f"{a}^{b} = ?"
            variantlar = {javob}
            while len(variantlar) < 4:
                notogri = javob + random.choice([-4, -2, 2, 4, 6])
                if notogri >= 0:
                    variantlar.add(notogri)
            variant_list = [str(v) for v in variantlar]
            random.shuffle(variant_list)
            return savol, str(javob), variant_list

    savol = f"{a} {amal} {b} = ?"
    variantlar = {javob}
    while len(variantlar) < 4:
        fark = random.choice([-3, -2, -1, 1, 2, 3, 5])
        notogri = javob + fark
        if notogri >= 0:
            variantlar.add(notogri)

    variant_list = [str(v) for v in variantlar]
    random.shuffle(variant_list)
    return savol, str(javob), variant_list


# =========================================================
# 4. MASALA YARATISH
# =========================================================

def masala_yaratish(sinf):
    sinf_raqami = int(sinf.split("-")[0])
    ismlar = ["Jasur", "Malika", "Sardor", "Zuxra", "Bekzod", "Madina"]
    ism = random.choice(ismlar)

    if sinf_raqami <= 2:
        a = random.randint(5, 15)
        b = random.randint(2, 8)
        if random.choice([True, False]):
            savol = f"{ism}da {a} ta olma bor edi. Do'sti unga yana {b} ta olma berdi. {ism}da jami nechta olma bo'ldi?"
            javob = a + b
        else:
            savol = f"Savatda {a + b} ta konfet bor edi. Bolalar {b} tasini yeb qo'yishdi. Savatda nechta konfet qoldi?"
            javob = a

    elif sinf_raqami <= 6:
        narx = random.randint(3, 9)
        soni = random.randint(4, 12)
        savol = f"{ism} do'kondan har biri {narx} so'mdan {soni} ta daftar sotib oldi. {ism} sotuvchiga jami qancha pul to'lashi kerak?"
        javob = narx * soni

    else:
        tezlik = random.randint(40, 90)
        vaqt = random.randint(2, 5)
        savol = f"Avtomobil soatiga {tezlik} km tezlik bilan {vaqt} soat yurdi. Avtomobil jami qancha masofa (km) bosib o'tgan?"
        javob = tezlik * vaqt

    variantlar = {javob}
    while len(variantlar) < 4:
        fark = random.choice([-3, -2, -1, 1, 2, 3, 5, 10])
        notogri = javob + fark
        if notogri >= 0:
            variantlar.add(notogri)

    variant_list = [str(v) for v in variantlar]
    random.shuffle(variant_list)
    return savol, str(javob), variant_list


# =========================================================
# 5. ZAXIRA BOSHQOTIRMALAR
# =========================================================

BOSHQOTIRMALAR = [
    {
        "savol": "3 ta mushuk 3 daqiqada 3 ta sichqon tutadi. 1 ta mushuk 3 daqiqada nechta sichqon tutadi?",
        "javob": "1",
        "variantlar": ["1", "2", "3", "9"]
    },
    {
        "savol": "Bir xonada 5 ta sham yonib turibdi. 2 tasi o'chirildi. Xonada nechta sham bor?",
        "javob": "5",
        "variantlar": ["2", "3", "5", "7"]
    },
    {
        "savol": "Bir savatda 10 ta olma bor. 10 ta bola bittadan olma oldi, lekin savatda 1 ta olma qoldi. Qanday qilib?",
        "javob": "Oxirgi bola olmani savati bilan oldi",
        "variantlar": [
            "Oxirgi bola olmani savati bilan oldi",
            "Bitta olma yashirilgan",
            "Olmalar 11 ta edi",
            "Buni amalga oshirib bo'lmaydi"
        ]
    },
    {
        "savol": "Daraxtda 10 ta qush bor edi. Ovchi bitta qushni urdi. Daraxtda nechta qush qoldi?",
        "javob": "0",
        "variantlar": ["0", "1", "9", "10"]
    },
    {
        "savol": "Ikki ota va ikki o'g'il 3 ta olmani bo'lib olishdi. Har biriga bittadan olma tegdi. Ular nechta kishi edi?",
        "javob": "3",
        "variantlar": ["2", "3", "4", "5"]
    },
    {
        "savol": "1 kg paxta og'irmi yoki 1 kg temir?",
        "javob": "Ikkalasi teng",
        "variantlar": [
            "Paxta",
            "Temir",
            "Ikkalasi teng",
            "Aniqlab bo'lmaydi"
        ]
    },
    {
        "savol": "5 ta shamdan 2 tasi o'chirildi. Ertalab nechta sham qoladi?",
        "javob": "2",
        "variantlar": ["2", "3", "5", "0"]
    },
    {
        "savol": "Qaysi oyda 28 kun bor?",
        "javob": "Barcha oylarda",
        "variantlar": [
            "Fevralda",
            "Yanvarda",
            "Barcha oylarda",
            "Faqat kabisa yilida"
        ]
    },
    {
        "savol": "Bir oilada 4 ta aka-uka bor. Har birining bitta singlisi bor. Oilada nechta farzand bor?",
        "javob": "5",
        "variantlar": ["4", "5", "8", "9"]
    },
    {
        "savol": "Elektr poyezdi shimolga qarab ketmoqda. Tutuni qaysi tomonga ketadi?",
        "javob": "Tutuni bo'lmaydi",
        "variantlar": [
            "Shimolga",
            "Janubga",
            "Sharqqa",
            "Tutuni bo'lmaydi"
        ]
    },
    {
        "savol": "Stolda 4 ta olma bor. Siz 2 tasini oldingiz. Sizda nechta olma bo'ldi?",
        "javob": "2",
        "variantlar": ["1", "2", "3", "4"]
    },
    {
        "savol": "Agar 2 ta quyon 2 kunda 2 ta sabzi yesa, 4 ta quyon 4 kunda nechta sabzi yeydi?",
        "javob": "8",
        "variantlar": ["4", "6", "8", "16"]
    }
]


# =========================================================
# 6. AI BOSHQOTIRMA YARATISH
# =========================================================

def boshqotirma_yaratish_ai(sinf, context):
    try:
        prompt = (
            f"O'zbek tilida {sinf} o'quvchilari uchun "
            f"1 ta qiziqarli mantiqiy boshqotirma tuzing. "
            f"Javobi aniq va tushunarli bo'lsin. "
            f"Har safar yangi boshqotirma tuzing.\n\n"
            f"Faqat quyidagi formatda javob qaytaring:\n"
            f"SAVOL: [Savol matni]\n"
            f"JAVOB: [To'g'ri javob]\n"
            f"NOTOGRI1: [1-noto'g'ri javob]\n"
            f"NOTOGRI2: [2-noto'g'ri javob]\n"
            f"NOTOGRI3: [3-noto'g'ri javob]"
        )

        response = ai_model.generate_content(prompt)
        text = response.text.strip()

        savol, javob, n1, n2, n3 = "", "", "", "", ""

        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("SAVOL:"):
                savol = line.replace("SAVOL:", "", 1).strip()
            elif line.startswith("JAVOB:"):
                javob = line.replace("JAVOB:", "", 1).strip()
            elif line.startswith("NOTOGRI1:"):
                n1 = line.replace("NOTOGRI1:", "", 1).strip()
            elif line.startswith("NOTOGRI2:"):
                n2 = line.replace("NOTOGRI2:", "", 1).strip()
            elif line.startswith("NOTOGRI3:"):
                n3 = line.replace("NOTOGRI3:", "", 1).strip()

        if savol and javob and n1 and n2 and n3:
            variantlar = [javob, n1, n2, n3]
            random.shuffle(variantlar)

            oldingi = context.user_data.get("oldingi_boshqotirma")
            if savol != oldingi:
                context.user_data["oldingi_boshqotirma"] = savol
                return savol, javob, variantlar

    except Exception as e:
        print("AI boshqotirma xatosi:", e)

    # Zaxira boshqotirmalar
    oldingi = context.user_data.get("oldingi_boshqotirma")
    mumkin = [x for x in BOSHQOTIRMALAR if x["savol"] != oldingi]
    if not mumkin:
        mumkin = BOSHQOTIRMALAR

    tanlangan = random.choice(mumkin)
    savol = tanlangan["savol"]
    javob = tanlangan["javob"]
    variantlar = tanlangan["variantlar"].copy()
    random.shuffle(variantlar)

    context.user_data["oldingi_boshqotirma"] = savol
    return savol, javob, variantlar


# =========================================================
# 7. ASOSIY MENYU
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asosiy_tugmalar = [
        ["📚 Misollar"],
        ["📖 Masalalar"],
        ["🧩 Boshqotirmalar"]
    ]
    await update.message.reply_text(
        "👋 Salom!\n\n"
        "Matematika va mantiqiy botiga xush kelibsiz.\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=ReplyKeyboardMarkup(asosiy_tugmalar, resize_keyboard=True)
    )


# =========================================================
# 8. SINF TANLASH
# =========================================================

async def sinf_tanlash_menyu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sinf_tugmalari = [
        ["1-sinf", "2-sinf", "3-sinf"],
        ["4-sinf", "5-sinf", "6-sinf"],
        ["7-sinf", "8-sinf", "9-sinf"],
        ["10-sinf", "11-sinf"],
        ["🏠 Asosiy menyu"]
    ]
    await update.message.reply_text(
        "📚 O'zingizga mos sinfni tanlang:",
        reply_markup=ReplyKeyboardMarkup(sinf_tugmalari, resize_keyboard=True)
    )


# =========================================================
# 9. SAVOL CHIQARISH
# =========================================================

async def savol_chiqarish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rejim = context.user_data.get("rejim", "misol")
    sinf = context.user_data.get("sinf", "1-sinf")

    if rejim == "misol":
        savol, javob, variantlar = misol_yaratish(sinf)
        sarlavha = f"📚 <b>Misollar ({sinf})</b>"
    elif rejim == "masala":
        savol, javob, variantlar = masala_yaratish(sinf)
        sarlavha = f"📖 <b>Matnli Masala ({sinf})</b>"
    else:
        savol, javob, variantlar = boshqotirma_yaratish_ai(sinf, context)
        sarlavha = f"🧩 <b>Boshqotirma ({sinf})</b>"

    context.user_data["togri_javob"] = javob
    context.user_data["variantlar"] = variantlar

    tugmalar = [[v] for v in variantlar]
    if rejim == "boshqotirma":
        tugmalar.append(["🧩 Yangi boshqotirma"])

    tugmalar.append(["Sinfni o'zgartirish 🔄", "🏠 Asosiy menyu"])

    matn = f"{sarlavha}\n\n<b>{savol}</b>"
    await update.message.reply_text(
        matn,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
    )


# =========================================================
# 10. JAVOBNI TEKSHIRISH
# =========================================================

async def javobni_tekshirish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text
    sinflar = [f"{i}-sinf" for i in range(1, 12)]

    if matn == "📚 Misollar":
        context.user_data["rejim"] = "misol"
        await sinf_tanlash_menyu(update, context)
    elif matn == "📖 Masalalar" or matn == "/masalalar":
        context.user_data["rejim"] = "masala"
        await sinf_tanlash_menyu(update, context)
    elif matn == "🧩 Boshqotirmalar" or matn == "/boshqotirmalar":
        context.user_data["rejim"] = "boshqotirma"
        await sinf_tanlash_menyu(update, context)
    elif matn == "🏠 Asosiy menyu":
        await start(update, context)
    elif matn == "Sinfni o'zgartirish 🔄":
        await sinf_tanlash_menyu(update, context)
    elif matn == "🧩 Yangi boshqotirma":
        if context.user_data.get("rejim") == "boshqotirma":
            await savol_chiqarish(update, context)
    elif matn in sinflar:
        context.user_data["sinf"] = matn
        context.user_data.pop("oldingi_boshqotirma", None)
        await savol_chiqarish(update, context)
    elif "togri_javob" in context.user_data:
        togri = context.user_data["togri_javob"]
        variantlar = context.user_data.get("variantlar", [])

        if matn in variantlar:
            if matn == togri:
                await update.message.reply_text(
                    "✅ <b>To'g'ri!</b>\n\n"
                    "🎉 Barakalla!\n"
                    "🔄 Yangi savol tayyor...",
                    parse_mode="HTML"
                )
                await savol_chiqarish(update, context)
            else:
                await update.message.reply_text(
                    "❌ <b>Noto'g'ri!</b>\n\n"
                    "🔄 Qayta urinib ko'ring!",
                    parse_mode="HTML"
                )


# =========================================================
# 11. COMMAND HANDLERLAR
# =========================================================

async def masalalar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["rejim"] = "masala"
    await sinf_tanlash_menyu(update, context)


async def boshqotirmalar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["rejim"] = "boshqotirma"
    await sinf_tanlash_menyu(update, context)


# =========================================================
# 12. MAIN
# =========================================================

def main():
    keep_alive()

    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("masalalar", masalalar_command))
    application.add_handler(CommandHandler("boshqotirmalar", boshqotirmalar_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, javobni_tekshirish))

    print("🤖 Bot va AI server ishga tushdi!")
    application.run_polling()


if __name__ == "__main__":
    main()
