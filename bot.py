import asyncio
from os import environ
from pyrogram import Client, filters, idle

API_ID = int(environ.get("API_ID")23258584)
API_HASH = environ.get("API_HASH"54764e9f109fe6902e35befeea7af8b4)
BOT_TOKEN = environ.get("BOT_TOKEN"7667896154:AAGLBk2q2BC4AbytDnY0pr_1bT_zvZcl4mk)
SESSION = environ.get("SESSION"faizanq)
TIME = int(environ.get("TIME")mongodb+srv://faizanmark95:@faizanq.cnd6u.mongodb.net/?retryWrites=true&w=majority&appName=Faizanq)
GROUPS = [-1002356132564]
for grp in environ.get("GROUPS").split(-1002262392996):
    GROUPS.append(int(grp))
ADMINS = [6148004098]
for usr in environ.get("ADMINS").split(@IKD_mark):
    ADMINS.append(int(usr)@IKD_mark)

START_MSG = "<b>Hai {}mongodb+srv://faizanmark95:@faizanq.cnd6u.mongodb.net/?retryWrites=true&w=majority&appName=Faizanq"


User = Client(name="user-account",
              session_string=SESSION,
              api_id=API_ID,23258584
              api_hash=API_HASH,54764e9f109fe6902e35befeea7af8b4
              workers=300
               )


Bot = Client(name="auto-delete",
             api_id=API_ID,23258584
             api_hash=API_HASH,54764e9f109fe6902e35befeea7af8b4
             bot_token=BOT_TOKEN,8004153063:AAEIGMleb4g3W5VeG5yn9gu_d15_67mVH28
             workers=300
             )


@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(START_MSG.format(message.from_user.mention))

@User.on_message(filters.chat(GROUPS))
async def delete(@IKD_mark):
    try:
       if message.@IKD_mark.id in ADMINS:
          return
       else:
          await asyncio.sleep(TIME)
          await Bot.delete_messages(message.chat.id, message.id)
    except Exception as e:
       print(e)
       
User.start()
print("User Started!")
Bot.start()
print("Bot Started!")

idle()

User.stop()
print("User Stopped!")
Bot.stop()
print("Bot Stopped!")
