from pyrogram import Client, filters
import os
import sys
import asyncio
import time

# ======== قراءة البيانات من البيئة ========
def get_env_var(var_name, required=True):
    value = os.environ.get(var_name)
    if required and not value:
        print(f"❌ خطأ: المتغير البيئي '{var_name}' غير موجود أو فارغ!")
        sys.exit(1)
    return value

print("🔍 جاري قراءة المتغيرات البيئية...")

BOT_TOKEN = get_env_var("BOT_TOKEN")
API_ID = int(get_env_var("API_ID"))
API_HASH = get_env_var("API_HASH")
SOURCE_CHAT = int(get_env_var("SOURCE_CHAT"))
DEST_CHAT = int(get_env_var("DEST_CHAT"))

print("✅ تم قراءة المتغيرات بنجاح:")
print(f"   📌 BOT_TOKEN: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")
print(f"   📌 API_ID: {API_ID}")
print(f"   📌 API_HASH: {API_HASH[:10]}...")
print(f"   📌 SOURCE_CHAT: {SOURCE_CHAT}")
print(f"   📌 DEST_CHAT: {DEST_CHAT}")

# ======== إنشاء البوت ========
print("\n🚀 جاري إنشاء البوت...")
try:
    app = Client(
        "forward_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        sleep_threshold=60  # إضافة هذا لتجنب انقطاع الاتصال
    )
    print("✅ تم إنشاء البوت بنجاح")
except Exception as e:
    print(f"❌ فشل إنشاء البوت: {e}")
    sys.exit(1)

# ======== مراقبة قناة المصدر ========
@app.on_message(filters.chat(SOURCE_CHAT) & ~filters.me)
async def forward_to_your_channel(client, message):
    try:
        # نسخ الرسالة بكل محتوياتها
        await message.copy(
            chat_id=DEST_CHAT,
            caption=message.caption
        )
        print(f"✅ تم نسخ رسالة جديدة: {message.id} من {message.chat.title}")
    except Exception as e:
        print(f"❌ خطأ أثناء نسخ الرسالة {message.id}: {e}")

# ======== أمر التحقق ========
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply(
        "✅ البوت يعمل بنجاح!\n\n"
        f"📌 ينسخ تلقائياً من قناة المصدر إلى قناتك.\n"
        f"📌 SOURCE_CHAT: {SOURCE_CHAT}\n"
        f"📌 DEST_CHAT: {DEST_CHAT}\n\n"
        "⚡ انتظر الرسائل الجديدة."
    )

# ======== تشغيل البوت مع إعادة المحاولة ========
if __name__ == "__main__":
    print("\n🌟 البوت جاهز للتشغيل...")
    print("👀 ينتظر الرسائل الجديدة...\n")
    
    # تشغيل البوت مع محاولات إعادة الاتصال
    while True:
        try:
            app.run()
        except Exception as e:
            print(f"❌ خطأ: {e}")
            print("🔄 إعادة المحاولة بعد 5 ثواني...")
            time.sleep(5)
            continue
        break
