import logging
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, RetryAfter

BOT_TOKEN = "YOUR_TOKEN"
SOURCE_CHANNEL_ID = -100xxxxxxxxxx
TARGET_CHANNEL_ID = -100yyyyyyyyyy

logging.basicConfig(level=logging.INFO)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post or update.edited_channel_post
    if not message or message.chat.id != SOURCE_CHANNEL_ID:
        return

    try:
        # استخدام copy_message (أأمن بكثير من forward)
        await context.bot.copy_message(
            chat_id=TARGET_CHANNEL_ID,
            from_chat_id=SOURCE_CHANNEL_ID,
            message_id=message.message_id,
            caption=message.caption,
            parse_mode='HTML'  # أو Markdown
        )
        logging.info(f"✅ تم نسخ الرسالة: {message.message_id}")
        
        # تأخير مهم جداً
        await asyncio.sleep(2.5)   # يمكنك تعديله بين 1.5 - 3.5

    except RetryAfter as e:
        logging.warning(f"⏳ Rate limit، انتظر {e.retry_after} ثانية")
        await asyncio.sleep(e.retry_after + 2)
    except TelegramError as e:
        logging.error(f"❌ Telegram Error: {e.message}")
        if "Flood" in str(e) or "Too Many Requests" in str(e):
            await asyncio.sleep(15)  # انتظار أطول عند Flood
    except Exception as e:
        logging.error(f"خطأ غير متوقع: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, forward_message))
    
    print("🚀 البوت يعمل بوضع الحماية...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
