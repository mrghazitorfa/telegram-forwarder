from pyrogram import Client, filters
import os
import asyncio

# ======== قراءة البيانات من البيئة (آمن) ========
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SOURCE_CHAT = int(os.environ.get("SOURCE_CHAT", 0))  # معرف قناة المصدر
DEST_CHAT = int(os.environ.get("DEST_CHAT", 0))      # معرف قناتك الخاصة

# ======== إنشاء البوت ========
app = Client("forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ======== مراقبة قناة المصدر ========
@app.on_message(filters.chat(SOURCE_CHAT) & ~filters.me)
async def forward_to_your_channel(client, message):
    try:
        # ننسخ الرسالة بكل محتوياتها (نص، صور، فيديو، الخ)
        await message.copy(
            chat_id=DEST_CHAT,
            caption=message.caption  # يحتفظ بالوصف إن وجد
        )
        print(f"✅ تم نسخ رسالة جديدة: {message.id}")
    except Exception as e:
        print(f"❌ خطأ: {e}")

# ======== تشغيل البوت ========
print("🚀 البوت يعمل الآن ويراقب القناة...")
app.run()
