import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, RetryAfter

# ================== إعدادات ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")                    # Railway سيأخذها تلقائياً
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID"))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post or update.edited_channel_post
    if not message:
        return
    
    if message.chat.id != SOURCE_CHANNEL_ID:
        return

    try:
        # استخدام copy_message (أأمن من forward)
        await context.bot.copy_message(
            chat_id=TARGET_CHANNEL_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=message.message_id
        )
        logging.info(f"✅ تم نسخ الرسالة: {message.message_id}")
        
        # تأخير للحماية من الحظر
        await asyncio.sleep(2.2)
        
    except RetryAfter as e:
        logging.warning(f"Rate limit - waiting {e.retry_after} seconds")
        await asyncio.sleep(e.retry_after + 3)
    except TelegramError as e:
        logging.error(f"Telegram Error: {e.message}")
        if "Flood" in str(e) or "Too Many" in str(e):
            await asyncio.sleep(20)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def main():
    if not BOT_TOKEN or not SOURCE_CHANNEL_ID or not TARGET_CHANNEL_ID:
        logging.error("Missing environment variables!")
        return
        
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward_message))
    
    logging.info("🚀 البوت يعمل بنجاح على Railway...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
