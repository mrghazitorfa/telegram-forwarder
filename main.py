from pyrogram import Client, filters
import sys
import time

# ======== ضع قيمك هنا مباشرة ========
BOT_TOKEN = "8926177639:AAH6Fudd-sGfB2_L0DyqcGvvsDEpz167LRA"
API_ID = 33002948
API_HASH = "8af9738f0aae0dd20be073bf75555d2c"
SOURCE_CHAT = -1003662240264
DEST_CHAT = -1004295892893
# ====================================

print("🔍 جاري تشغيل البوت مع المتغيرات المضمنة...")

# ======== إنشاء البوت ========
print("🚀 جاري إنشاء البوت...")
try:
    app = Client("forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    print("✅ تم إنشاء البوت بنجاح")
except Exception as e:
    print(f"❌ فشل إنشاء البوت: {e}")
    sys.exit(1)

# ======== مراقبة قناة المصدر ========
@app.on_message(filters.chat(SOURCE_CHAT) & ~filters.me)
async def forward_to_your_channel(client, message):
    try:
        await message.copy(chat_id=DEST_CHAT, caption=message.caption)
        print(f"✅ تم نسخ رسالة جديدة: {message.id}")
    except Exception as e:
        print(f"❌ خطأ أثناء نسخ الرسالة: {e}")

# ======== أمر التحقق ========
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply(
        "✅ البوت يعمل بنجاح!\n\n"
        "📌 ينسخ تلقائياً من قناة المصدر إلى قناتك.\n"
        "⚡ انتظر الرسائل الجديدة."
    )

# ======== تشغيل البوت ========
if __name__ == "__main__":
    print("\n🌟 البوت جاهز للتشغيل...")
    print("👀 ينتظر الرسائل الجديدة...\n")
    while True:
        try:
            app.run()
        except Exception as e:
            print(f"❌ خطأ: {e}")
            print("🔄 إعادة المحاولة بعد 5 ثواني...")
            time.sleep(5)
