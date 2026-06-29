from pyrogram import Client, filters
import os
import sys

# ======== قراءة البيانات من البيئة ========
def get_env_var(var_name, required=True):
    """دالة لقراءة المتغيرات البيئية مع رسائل خطأ واضحة"""
    value = os.environ.get(var_name)
    if required and not value:
        print(f"❌ خطأ: المتغير البيئي '{var_name}' غير موجود أو فارغ!")
        print(f"⚠️  يرجى إضافته في إعدادات Railway > Variables")
        sys.exit(1)
    return value

# قراءة المتغيرات مع التحقق
print("🔍 جاري قراءة المتغيرات البيئية...")

BOT_TOKEN = get_env_var("BOT_TOKEN")
API_ID_str = get_env_var("API_ID")
API_HASH = get_env_var("API_HASH")
SOURCE_CHAT_str = get_env_var("SOURCE_CHAT")
DEST_CHAT_str = get_env_var("DEST_CHAT")

# تحويل الأرقام إلى int
try:
    API_ID = int(API_ID_str)
    SOURCE_CHAT = int(SOURCE_CHAT_str)
    DEST_CHAT = int(DEST_CHAT_str)
except ValueError as e:
    print(f"❌ خطأ: تأكد من أن API_ID, SOURCE_CHAT, DEST_CHAT هي أرقام صحيحة")
    print(f"   التفاصيل: {e}")
    sys.exit(1)

# عرض ملخص للمتغيرات (مع إخفاء التوكن جزئياً للأمان)
print("✅ تم قراءة المتغيرات بنجاح:")
print(f"   📌 BOT_TOKEN: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")
print(f"   📌 API_ID: {API_ID}")
print(f"   📌 API_HASH: {API_HASH[:10]}...")
print(f"   📌 SOURCE_CHAT: {SOURCE_CHAT}")
print(f"   📌 DEST_CHAT: {DEST_CHAT}")

# ======== إنشاء البوت ========
print("\n🚀 جاري إنشاء البوت...")
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
        # ننسخ الرسالة بكل محتوياتها
        await message.copy(
            chat_id=DEST_CHAT,
            caption=message.caption
        )
        print(f"✅ تم نسخ رسالة جديدة: {message.id} من {message.chat.title}")
    except Exception as e:
        print(f"❌ خطأ أثناء نسخ الرسالة {message.id}: {e}")

# ======== أمر التحقق من أن البوت يعمل ========
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply(
        "✅ البوت يعمل بنجاح!\n\n"
        "📌 ينسخ تلقائياً من:\n"
        f"   {SOURCE_CHAT}\n"
        "📌 إلى:\n"
        f"   {DEST_CHAT}\n\n"
        "⚡ انتظر الرسائل الجديدة من قناة المصدر."
    )

# ======== تشغيل البوت ========
if __name__ == "__main__":
    print("\n🌟 البوت جاهز للتشغيل...")
    print("👀 ينتظر الرسائل الجديدة...\n")
    try:
        app.run()
    except Exception as e:
        print(f"❌ خطأ أثناء تشغيل البوت: {e}")
        sys.exit(1)
