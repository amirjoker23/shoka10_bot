import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "1571446410"))

(NAME, PHONE, NATIONAL_ID, MARITAL, ADDRESS, BIRTHDAY, JOB, PLAN, POSTAL, BENEFICIARY_ID, BENEFICIARY_BIRTHDAY) = range(11)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! برای ثبت‌نام نام و نام خانوادگی‌ات را بفرست:"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("شماره تماس:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("کد ملی:")
    return NATIONAL_ID

async def get_national_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['national_id'] = update.message.text
    keyboard = [["متاهل"], ["مجرد"]]
    await update.message.reply_text(
        "وضعیت تاهل؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return MARITAL

async def get_marital(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['marital'] = update.message.text
    await update.message.reply_text("آدرس:")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("تاریخ تولد (مثال: 1370/05/12):")
    return BIRTHDAY

async def get_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['birthday'] = update.message.text
    await update.message.reply_text("شغل:")
    return JOB

async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['job'] = update.message.text
    keyboard = [["ماهانه"], ["سالانه"], ["یکجا"]]
    await update.message.reply_text(
        "طرح مورد نظر؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return PLAN

async def get_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['plan'] = update.message.text
    await update.message.reply_text("کد پستی:")
    return POSTAL

async def get_postal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['postal'] = update.message.text
    await update.message.reply_text("کد ملی ذینفع:")
    return BENEFICIARY_ID

async def get_beneficiary_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['beneficiary_id'] = update.message.text
    await update.message.reply_text("تاریخ تولد ذینفع (مثال: 1390/03/10):")
    return BENEFICIARY_BIRTHDAY

async def get_beneficiary_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['beneficiary_birthday'] = update.message.text
    info = context.user_data
    msg = (
        f"📝 اطلاعات ثبت شده:\n\n"
        f"👤 نام: {info['name']}\n"
        f"📞 شماره تماس: {info['phone']}\n"
        f"🆔 کد ملی: {info['national_id']}\n"
        f"💍 وضعیت تاهل: {info['marital']}\n"
        f"🏠 آدرس: {info['address']}\n"
        f"🎂 تولد: {info['birthday']}\n"
        f"💼 شغل: {info['job']}\n"
        f"📅 طرح: {info['plan']}\n"
        f"📮 کد پستی: {info['postal']}\n"
        f"👨‍👩‍👦‍👦 کد ملی ذینفع: {info['beneficiary_id']}\n"
        f"🎂 تولد ذینفع: {info['beneficiary_birthday']}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await update.message.reply_text("✅ ثبت‌نام انجام شد، ممنون 🙏")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لغو شد.")
    return ConversationHandler.END

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            NATIONAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_national_id)],
            MARITAL: [MessageHandler(filters.Regex("^(متاهل|مجرد)$"), get_marital)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birthday)],
            JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_job)],
            PLAN: [MessageHandler(filters.Regex("^(ماهانه|سالانه|یکجا)$"), get_plan)],
            POSTAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_postal)],
            BENEFICIARY_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_id)],
            BENEFICIARY_BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_birthday)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )
    app.add_handler(conv)

    port = int(os.environ.get("PORT", 8443))
    await app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=os.environ.get("WEBHOOK_URL"),
        stop_signals=None
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
