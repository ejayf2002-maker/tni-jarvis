# TNI HOLDINGS - WHOLE SYSTEM - CLEAN VERSION - NO EMOJI
# Maya Cars + Aya House + Gadget Hub + Jarvis + Luna

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Keep Render alive - Web Server
def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"TNI Holdings Bot is Running!")
        def log_message(self, *args):
            pass
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()
import asyncio
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= CONFIG - PALITAN MO LANG TO =================
MAYA_TOKEN = "9134421049:AAHT4COYc2ImGfEQd9yN2DAh2UB8fIcMqZk"
AYA_TOKEN = "9083598915:AAHLRizeEVPlzZ3H5LSff4pjmbHndA4t32Q"
GADGET_TOKEN = "PASTE_GADGET_TOKEN_DITO"
JARVIS_TOKEN = "9196373451:AAHkqN-_wUNujUgoW-W2CIcclDr7nxhvA5o"

YOUR_PHONE_DISPLAY = "0951-140-1760"
YOUR_PHONE = "+639511401760"
YOUR_WHATSAPP = "639511401760"
YOUR_EMAIL = "ejayferrer020@gmail.com"
JARVIS_APP_PASSWORD = "znjxsskwoercrkzi"
JARVIS_CHAT_ID = "8831338553"

# ================= DATA =================
leads = []
reservations = []
schedules = []
takeover_mode = False

CARS = {
    "vios": "Toyota Vios 2019 - P385,000 - Good condition, with warranty",
    "wigo": "Toyota Wigo 2020 - P315,000 - Good as new",
    "innova": "Toyota Innova 2018 - P685,000 - Family car, fresh",
    "mirage": "Mitsubishi Mirage 2019 - P325,000 - Tipid sa gas",
    "xpander": "Mitsubishi Xpander 2020 - P685,000 - 7 seater",
}

HOUSES = {
    "sena": "Seña House - P978,500 - P25,500 down - P4,814 monthly - Isabela",
    "casa": "Casa - P1,250,000 - P30,000 down - P6,500 monthly",
}

GADGETS = {
    "iphone 13": "iPhone 13 128GB - P22,500 - Good as New, with warranty",
    "iphone 12": "iPhone 12 128GB - P17,500 - Good as New",
    "iphone 11": "iPhone 11 128GB - P12,500 - Good condition",
    "samsung s21": "Samsung S21 - P14,500 - Good as New",
    "ipad": "iPad 9th Gen - P15,500 - Good as New",
}

CALL_TEXT = "Para kausapin si Sir Ejay, Call/Text mo siya dito: 0951-140-1760. Type 'call me' para tawagan ka ni Sir Ejay!"

def save_lead(source, name, msg):
    leads.append({"source": source, "name": name, "msg": msg, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})

def send_email(to_email, subject, body):
    try:
        if "PASTE" in JARVIS_APP_PASSWORD:
            print("Email skipped - no app password yet")
            return
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = YOUR_EMAIL
        msg["To"] = to_email
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(YOUR_EMAIL, JARVIS_APP_PASSWORD)
        server.sendmail(YOUR_EMAIL, to_email, msg.as_string())
        server.quit()
        print("Email sent to", to_email)
    except Exception as e:
        print("Email failed:", e)

async def notify_jarvis(context, text):
    try:
        if "PASTE" not in JARVIS_CHAT_ID:
            await context.bot.send_message(chat_id=JARVIS_CHAT_ID, text=text)
    except Exception as e:
        print("Notify failed:", e)

# ================= MAYA - CARS =================
async def maya_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello po! Si Maya po from TNI Cars! Anong car hanap niyo? Vios, Wigo, Innova, Mirage, Xpander? Type 'call me' para tawagan kayo ni Sir Ejay!")

async def maya_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global takeover_mode
    text = update.message.text.lower()
    name = update.message.from_user.first_name
    save_lead("Cars", name, update.message.text)
    if takeover_mode:
        await update.message.reply_text("Wait lang po, tatawagin ko si Sir Ejay para sa inyo!")
        await notify_jarvis(context, "TAKEOVER - Cars - " + name + ": " + update.message.text)
        return
    if "call me" in text or "human" in text or "tawag" in text or "call" in text:
        await update.message.reply_text(CALL_TEXT)
        await notify_jarvis(context, "CALL REQUEST - Cars - " + name + " gusto magpa-call! " + update.message.text)
        return
    if "reserve" in text or "pa-reserve" in text or "kunin" in text:
        reservations.append({"source": "Cars", "name": name, "msg": update.message.text})
        await update.message.reply_text("Yown! I-reserve ko na po! For close na natin kay Sir Ejay! Call/Text si Sir Ejay: 0951-140-1760")
        await notify_jarvis(context, "RESERVATION - Cars - " + name + ": " + update.message.text)
        return
    found = False
    for k, v in CARS.items():
        if k in text:
            await update.message.reply_text(v + " Gusto niyo po ba pa-reserve? Type 'reserve' para i-reserve ko! " + CALL_TEXT)
            found = True
    if not found:
        await update.message.reply_text("Hello po! May Vios, Wigo, Innova, Mirage, Xpander po kami! Alin po gusto niyo malaman price? Type 'call me' para kausapin si Sir Ejay!")

# ================= AYA - HOUSE =================
async def aya_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello po! Si Aya po from TNI House! May Seña House po kami - P978,500! Type 'call me' para tawagan kayo ni Sir Ejay!")

async def aya_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global takeover_mode
    text = update.message.text.lower()
    name = update.message.from_user.first_name
    save_lead("House", name, update.message.text)
    if takeover_mode:
        await update.message.reply_text("Wait lang po, tatawagin ko si Sir Ejay!")
        await notify_jarvis(context, "TAKEOVER - House - " + name + ": " + update.message.text)
        return
    if "call me" in text or "human" in text or "tawag" in text or "call" in text:
        await update.message.reply_text(CALL_TEXT)
        await notify_jarvis(context, "CALL REQUEST - House - " + name)
        return
    if "reserve" in text or "schedule" in text or "meetup" in text or "viewing" in text:
        schedules.append({"source": "House", "name": name, "msg": update.message.text})
        await update.message.reply_text("Yown! Naka-schedule na po! For close na natin kay Sir Ejay! Call/Text: 0951-140-1760")
        await notify_jarvis(context, "SCHEDULE - House - " + name + ": " + update.message.text)
        return
    found = False
    for k, v in HOUSES.items():
        if k in text:
            await update.message.reply_text(v + " Gusto niyo po ba magpa-schedule ng viewing? " + CALL_TEXT)
            found = True
    if not found:
        await update.message.reply_text("May Seña House po kami - P978,500 - P25,500 down - P4,814 monthly! Gusto niyo po ba details? Type 'call me' para kausapin si Sir Ejay!")

# ================= GADGET BOT =================
async def gadget_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello po! Si Gadget Bot po from TNI Gadget Hub! May iPhone 13, iPhone 12, iPhone 11, Samsung S21, iPad! Alin po hanap niyo? Type 'call me' para tawagan kayo ni Sir Ejay!")

async def gadget_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global takeover_mode
    text = update.message.text.lower()
    name = update.message.from_user.first_name
    save_lead("Gadget", name, update.message.text)
    if takeover_mode:
        await update.message.reply_text("Wait lang po, tatawagin ko si Sir Ejay!")
        await notify_jarvis(context, "TAKEOVER - Gadget - " + name + ": " + update.message.text)
        return
    if "call me" in text or "human" in text or "tawag" in text or "call" in text:
        await update.message.reply_text(CALL_TEXT)
        await notify_jarvis(context, "CALL REQUEST - Gadget - " + name)
        return
    if "reserve" in text or "kunin" in text or "buy" in text:
        reservations.append({"source": "Gadget", "name": name, "msg": update.message.text})
        await update.message.reply_text("Yown! I-reserve ko na po! For close na natin kay Sir Ejay! Call/Text: 0951-140-1760")
        await notify_jarvis(context, "RESERVATION - Gadget - " + name + ": " + update.message.text)
        return
    found = False
    for k, v in GADGETS.items():
        if k in text:
            await update.message.reply_text(v + " Gusto niyo po ba pa-reserve ko na? Type 'reserve'! " + CALL_TEXT)
            found = True
    if "hm" in text or "price" in text or "magkano" in text:
        await update.message.reply_text("iPhone 13 - P22,500, iPhone 12 - P17,500, iPhone 11 - P12,500, Samsung S21 - P14,500, iPad - P15,500! Alin po gusto niyo?")
        found = True
    if not found:
        await update.message.reply_text("May iPhone 13, 12, 11, Samsung S21, iPad po kami! Alin po hanap niyo? Type 'call me' para kausapin si Sir Ejay!")

# ================= JARVIS - ADMIN =================
async def jarvis_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Sir Ejay! Si Jarvis po! Type /help para makita commands!")

async def jarvis_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = "/help - Help\n/status - Status\n/report - Daily Report\n/leads - All Leads\n/takeover - Ikaw na sasagot\n/resume - Balik sa bot\n/reply [id] [msg] - Reply sa buyer"
    await update.message.reply_text(txt)

async def jarvis_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = "TNI HOLDINGS STATUS\nTakeover: " + str(takeover_mode) + "\nLeads: " + str(len(leads)) + "\nReservations: " + str(len(reservations)) + "\nSchedules: " + str(len(schedules)) + "\nCall/Text: 0951-140-1760"
    await update.message.reply_text(txt)

async def jarvis_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cars = len([x for x in leads if x["source"] == "Cars"])
    house = len([x for x in leads if x["source"] == "House"])
    gadget = len([x for x in leads if x["source"] == "Gadget"])
    txt = "DAILY REPORT\nCars Leads: " + str(cars) + "\nHouse Leads: " + str(house) + "\nGadget Leads: " + str(gadget) + "\nTotal Leads: " + str(len(leads)) + "\nReservations: " + str(len(reservations)) + "\nSchedules: " + str(len(schedules))
    await update.message.reply_text(txt)

async def jarvis_leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(leads) == 0:
        await update.message.reply_text("Wala pang leads, Sir.")
        return
    txt = "LEADS:\n"
    for i, l in enumerate(leads[-10:]):
        txt += str(i+1) + ". [" + l["source"] + "] " + l["name"] + ": " + l["msg"] + "\n"
    await update.message.reply_text(txt)

async def jarvis_takeover(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global takeover_mode
    takeover_mode = True
    await update.message.reply_text("Takeover ON, Sir. Ikaw na sasagot ngayon.")

async def jarvis_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global takeover_mode
    takeover_mode = False
    await update.message.reply_text("Takeover OFF, Sir. Balik na sa bot - Maya, Aya, Gadget.")

async def jarvis_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sir, type /help para makita commands!")

# ================= LUNA - DAILY =================
async def luna_loop():
    sent_morning = False
    sent_evening = False
    sent_report = False
    while True:
        now = datetime.now()
        h = now.hour
        m = now.minute
        if h == 7 and m == 30 and not sent_morning:
            print("LUNA 7:30AM - Good morning Sir Ejay! Ready na si Maya, Aya, Gadget!")
            sent_morning = True
        if h == 19 and m == 0 and not sent_evening:
            print("LUNA 7PM - Sir, leads today: " + str(len(leads)))
            sent_evening = True
        if h == 21 and m == 0 and not sent_report:
            print("LUNA 9PM REPORT - Leads: " + str(len(leads)) + " Reservations: " + str(len(reservations)))
            sent_report = True
        if h == 0:
            sent_morning = False
            sent_evening = False
            sent_report = False
        await asyncio.sleep(30)
# ================= RUN ALL - FIXED =================
async def run_all():
    print("==========================================")
    print("TNI HOLDINGS - WHOLE SYSTEM IS RUNNING!")
    print("Maya_cars_bot is running...")
    print("Aya_house_bot is running...")
    print("Gadget Bot is running...")
    print("Jarvis is running... Assistant of Sir Ejay")
    print("Call/Text: 0951-140-1760")
    print("Luna - 7:30AM + 7PM + 9PM Report")
    print("==========================================")

    apps = []

    if "PASTE" not in MAYA_TOKEN:
        maya_app = ApplicationBuilder().token(MAYA_TOKEN).build()
        maya_app.add_handler(CommandHandler("start", maya_start))
        maya_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, maya_msg))
        apps.append(maya_app)

    if "PASTE" not in AYA_TOKEN:
        aya_app = ApplicationBuilder().token(AYA_TOKEN).build()
        aya_app.add_handler(CommandHandler("start", aya_start))
        aya_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, aya_msg))
        apps.append(aya_app)

    if "PASTE" not in GADGET_TOKEN:
        gadget_app = ApplicationBuilder().token(GADGET_TOKEN).build()
        gadget_app.add_handler(CommandHandler("start", gadget_start))
        gadget_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gadget_msg))
        apps.append(gadget_app)

    if "PASTE" not in JARVIS_TOKEN:
        jarvis_app = ApplicationBuilder().token(JARVIS_TOKEN).build()
        jarvis_app.add_handler(CommandHandler("start", jarvis_start))
        jarvis_app.add_handler(CommandHandler("help", jarvis_help))
        jarvis_app.add_handler(CommandHandler("status", jarvis_status))
        jarvis_app.add_handler(CommandHandler("report", jarvis_report))
        jarvis_app.add_handler(CommandHandler("leads", jarvis_leads))
        jarvis_app.add_handler(CommandHandler("takeover", jarvis_takeover))
        jarvis_app.add_handler(CommandHandler("resume", jarvis_resume))
        jarvis_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, jarvis_msg))
        apps.append(jarvis_app)

    # Start all bots - FIXED: hindi na run_polling, start_polling na!
    for app in apps:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

    asyncio.create_task(luna_loop())
    print("All bots are now polling! Ready to reply!")
    # Keep running forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_all())