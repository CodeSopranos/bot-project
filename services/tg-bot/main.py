import os
import logging
from aiogram import Bot, Dispatcher, executor, types, md
from aiogram.bot.api import TelegramAPIServer
from aiogram.types import ContentType
from aiogram.utils.markdown import hbold, hlink, quote_html


logging.basicConfig(level=logging.INFO)
TG_TOKEN = os.getenv("TG_TOKEN", None)  # Telegram Bot API Key

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot, )


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # result = await bot.get_me()
    await types.ChatActions.typing()
    await message.reply(md.text(md.text('Hi!'),
                                md.text('*Tell me something!*'),
                                sep='\n'))


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(md.text(md.text('*The list of my commands:*'),
                                md.text("🔸 {command} - Start conversation with bot".format(command="/start")),
                                md.text("🔸 {command} - Get this message".format(command="/help")),
                                sep='\n'))


@dp.message_handler(content_types=ContentType.TEXT)
async def echo(message: types.Message):
    await types.ChatActions.typing()
    await message.answer(f'{message.from_user.first_name} said: {message.text}')


@dp.message_handler(content_types=ContentType.VOICE)
async def audio(message: types.Voice):
    await types.ChatActions.typing()
    file = await bot.get_file(message.voice.file_id)
    await bot.download_file(file.file_path, destination_dir='audio/')
    duration = message.to_python()['voice']['duration']
    await message.answer(f'Duration: {duration} seconds')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
