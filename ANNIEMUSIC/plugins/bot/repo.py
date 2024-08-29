from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ANNIEMUSIC import app
from config import BOT_USERNAME

start_txt = """**
✪ ωεℓ¢σмє ƒσя ɱσσɳ яєρσѕ ✪
 
 ➲ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs ✰
 
 ➲ ʀᴜɴ 24x7 ʟᴀɢ ғʀᴇᴇ ᴡɪᴛʜᴏᴜᴛ sᴛᴏᴘ ✰
 
 ► ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴛʜᴇɴ sᴇɴᴅ ss
**"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
     
            [ 
            InlineKeyboardButton("𝐓ᴀᴘ 𝐓o 𝐒ᴇᴇ 𝐓ʜᴇ 𝐌ᴀɢɪᴄ✨", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
     
            [
             InlineKeyboardButton("𝐌ᴏᴏɴ🌙♡", url="https://t.me/Moonshining2"),
             InlineKeyboardButton("💌 𝐇ᴇʟᴘ 💟", url="https://t.me/Kittyxupdates"),
             ],
     
             [
             InlineKeyboardButton("︎𝐆ʀᴀɴᴅᴍᴀsᴛɪ", url="https://t.me/+fPsCUlG964E5MzY1"),
             ],
     
              ]
 
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://telegra.ph/file/fda6ac428799c5ce53d77.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
