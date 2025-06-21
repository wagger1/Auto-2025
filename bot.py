import asyncio
import logging
from os import environ
from pyrogram import Client, filters, idle
from pyrogram import utils as pyroutils
import threading
from webcode import app
from waitress import serve

if __name__ == "__main__":
    threading.Thread(target=lambda: serve(app, host="0.0.0.0", port=8000)).start()
    asyncio.run(main())

# === Logging ===
logging.basicConfig(level=logging.INFO)

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

# === Handlers ===
@Bot.on_message(filters.command("start") & filters.private)
async def start_handler(bot, message):
    logging.info(f"/start called by {message.from_user.id}")
    await message.reply(START_MSG.format(message.from_user.mention))


@User.on_message(filters.chat(GROUPS))
async def auto_delete(user, message):
    try:
        if message.from_user and message.from_user.id in ADMINS:
            return
        await asyncio.sleep(TIME)
        await Bot.delete_messages(chat_id=message.chat.id, message_ids=message.id)
    except Exception as e:
        logging.error(f"Error deleting message: {e}")

# === Run App ===
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

    await idle()

    await User.stop()
    logging.info("[✖] User session stopped")
    await Bot.stop()
    logging.info("[✖] Bot session stopped")
