import asyncio
import logging
from os import environ
from pyrogram import Client, filters, idle
from pyrogram import utils as pyroutils

pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999
from aiohttp import web
from webcode import web_server  
logging.getLogger("asyncio").setLevel(logging.CRITICAL -1)

PORT = environ.get("PORT", "8080")
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
SESSION = environ.get("SESSION")
TIME = int(environ.get("TIME"))
GROUPS = []
for grp in environ.get("GROUPS").split():
    GROUPS.append(int(grp))
ADMINS = []
for usr in environ.get("ADMINS").split():
    ADMINS.append(int(usr))

START_MSG = "<b>Hai {},\nI'm a private bot of @CinemaxpressTM to delete group messages after a specific time</b>"


User = Client(name="user-account",
              session_string=SESSION,
              api_id=API_ID,
              api_hash=API_HASH,
              workers=300
              )


class Bot(Client):

    def __init__(self):
        super().__init__(
             name="auto-delete",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=300
             )
    async def start(self):
        await super().start()
        print("Bot oombi!")
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(START_MSG.format(message.from_user.mention))

@User.on_message(filters.chat(GROUPS))
async def delete(user, message):
    chat = message.chat.id
    m = message.id
    try:
       if message.from_user.id in ADMINS:
          return
       else:
          await asyncio.sleep(TIME)
          await user.delete_messages(chat_id=chat, message_ids=m)
    except Exception as e:
       print(e)
       
User.start()
print("User oombi 🖕🏿")
Bot.start()
print("Bot oombi 🖕🏿")

idle()

User.stop()
print("User Stopped!😑")
Bot.stop()
print("Bot Stopped!🥵")
