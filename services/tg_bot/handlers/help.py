from aiogram import md, types
from handlers.base import bot, dp, FSMContext


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):
    await types.ChatActions.typing()
    await message.answer(md.text(md.bold(f"Hi {message.from_user.first_name}👋!"),
                                 md.text(f"It is", md.underline(f"{(await bot.me).first_name}")),
                                 md.text(md.italic("\nPowered by "),
                                         md.link("aiogram", "https://docs.aiogram.dev/en/latest/index.html")),
                                 sep="\n"))
    await message.answer(md.text("🦋"))
    await message.answer(md.italic("NB: you can type {command} to see all actions".format(command="/help")))


@dp.message_handler(commands=['help'], state='*')
async def process_help_command(message: types.Message):
    await message.reply(md.text(md.bold("The list of my commands:"),
                                md.text("🔸 {command} : Start conversation with bot".format(command="/start")),
                                md.text("🔸 {command} : Get this message".format(command="/help")),
                                md.text("🔸 {command} : Test your accent 🔥".format(command="/accent")),
                                md.text("🔸 {command} : Useful links".format(command="/links")),
                                sep="\n"))
