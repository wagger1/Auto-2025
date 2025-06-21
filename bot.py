import asyncio
from os import environ
from pyrogram import Client, filters, idle
from pyrogram import utils as pyroutils

# Adjust Pyrogram constants for group/channel ID handling
pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999

# === ENV Variables ===
PORT = environ.get("PORT", "8080")
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
SESSION = environ.get("SESSION")
TIME = int(environ.get("TIME"))

# Load GROUPS and ADMINS from space-separated strings
GROUPS = list(map(int, environ.get("GROUPS", "").split()))
ADMINS = list(map(int, environ.get("ADMINS", "").split()))

START_MSG = "<b>Hai {},\nI'm a simple bot to delete group messages after a specific time</b>"

# === Pyrogram Clients ===
User = Client(
    name="user-session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
    workers=300
)

Bot = Client(
    name="auto-delete",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=300
)

# === Start Command ===
@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(START_MSG.format(message.from_user.mention))

# === Auto Delete Handler ===
@User.on_message(filters.chat(GROUPS))
async def auto_delete(user, message):
    try:
        if message.from_user and message.from_user.id in ADMINS:
            return
        await asyncio.sleep(TIME)
        await Bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
    except Exception as e:
        print(f"[ERROR] {e}")

# === Run Clients ===
async def main():
    await User.start()
    print("[✔] User session started")

    await Bot.start()
    print("[✔] Bot session started")

    await idle()

    await User.stop()
    print("[✖] User session stopped")

    await Bot.stop()
    print("[✖] Bot session stopped")

if __name__ == "__main__":
    asyncio.run(main())
