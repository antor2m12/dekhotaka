"""
DekhoTaka Bot - Telegram Bot
Opens the Web App (Mini App) where users watch ads and earn money.

SETUP INSTRUCTIONS:
1. Replace BOT_TOKEN below with your own token from @BotFather (use environment variable, see bottom).
2. Replace WEBAPP_URL with your hosted index.html URL (GitHub Pages / Firebase Hosting).
3. Replace CHANNEL_USERNAME with your Telegram channel (without @), used for join verification (optional).
4. Deploy this on Render.com as a "Background Worker" or "Web Service".
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════
# CONFIG — environment variables ব্যবহার করুন, কখনো সরাসরি টোকেন এখানে লিখবেন না
# ════════════════════════════════════════
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Render এর Environment tab এ BOT_TOKEN সেট করুন
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://your-username.github.io/dekhotaka/index.html")  # ⚠️ আপনার hosted URL দিন
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/your_channel_here")
ADMIN_ID = os.environ.get("ADMIN_ID", "")  # আপনার নিজের Telegram ID (notifications এর জন্য, optional)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🚀 Open DekhoTaka App", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"👋 স্বাগতম, {user.first_name}!\n\n"
        f"🤖 *DekhoTaka Bot* এ আপনাকে স্বাগতম।\n\n"
        f"👁️ বিজ্ঞাপন দেখুন এবং প্রতিদিন *৳15* পর্যন্ত আয় করুন!\n"
        f"💸 bKash/Nagad এ সরাসরি উইথড্র করুন।\n"
        f"👥 বন্ধুদের রেফার করে বোনাস পান।\n\n"
        f"নিচের বাটনে ক্লিক করে শুরু করুন 👇"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *সাহায্য*\n\n"
        "/start - বট শুরু করুন এবং App ওপেন করুন\n"
        "/balance - আপনার balance চেক করুন (App এ দেখুন)\n"
        "/help - এই মেসেজ দেখুন\n\n"
        "❓ কোনো সমস্যা হলে আমাদের চ্যানেলে যোগাযোগ করুন।"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💰 Check Balance in App", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text(
        "আপনার balance দেখতে App ওপেন করুন 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    if not BOT_TOKEN:
        raise SystemExit("❌ BOT_TOKEN environment variable সেট করা নেই! Render এর Environment settings এ যোগ করুন।")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("balance", balance))

    logger.info("🤖 DekhoTaka Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
