import asyncio
import logging
import threading
from os import environ
from pyrogram import Client, filters, idle
from pyrogram import utils as pyroutils
from webcode import app
from waitress import serve

# === Logging ===
logging.basicConfig(level=logging.INFO)

# Pyrogram constants
pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999

# ENV variables
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
SESSION = environ.get("SESSION")
TIME = int(environ.get("TIME"))
GROUPS = list(map(int, environ.get("GROUPS", "").split()))
ADMINS = list(map(int, environ.get("ADMINS", "").split()))

START_MSG = "<b>Hai {},\nI'm a simple bot to delete group messages after a specific time</b>"

# Pyrogram clients
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

@Bot.on_message(filters.command("start") & filters.private)
async def start_handler(bot, message):
    logging.info(f"/start from {message.from_user.id}")
    await message.reply(START_MSG.format(message.from_user.mention))

@Bot.on_message(filters.private)
async def debug_pm(bot, message):
    print(f"📩 Got private message: {message.text} from {message.from_user.id}")
    await message.reply("✅ I received your message!")

@User.on_message(filters.chat(GROUPS))
async def auto_delete(user, message):
    try:
        if message.from_user and message.from_user.id in ADMINS:
            return
        await asyncio.sleep(TIME)
        await Bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
    except Exception as e:
        logging.error(f"Error deleting message: {e}")

# ✅ THIS is the main function
async def main():
    try:
        await User.start()
        logging.info("[✔] User session started")
    except Exception as e:
        logging.error(f"[✖] User failed to start: {e}")

    try:
        await Bot.start()
        logging.info("[✔] Bot session started")
    except Exception as e:
        logging.error(f"[✖] Bot failed to start: {e}")

    logging.info("🔥 Bot is live and waiting for commands")
    await idle()

    await User.stop()
    await Bot.stop()
    logging.info("🔴 Bot and user sessions stopped")

# ✅ Dummy web server thread to keep Koyeb happy
if __name__ == "__main__":
    threading.Thread(target=lambda: serve(app, host="0.0.0.0", port=8000)).start()
    asyncio.run(main())
