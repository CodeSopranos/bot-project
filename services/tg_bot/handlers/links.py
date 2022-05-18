from aiogram import md, types
from handlers.base import bot, dp, FSMContext


@dp.message_handler(commands=['links'], state='*')
async def process_help_command(message: types.Message):
    await message.reply(md.text(md.bold("The list of useful links:"),
                                md.text("🔸", md.link("google", "https://www.google.com/"), ":  just google"),
                                md.text("🔸", md.link("duolingo", "https://www.duolingo.com/"), ":  just duolingo"),
                                sep="\n"), parse_mode=types.ParseMode.MARKDOWN_V2)
