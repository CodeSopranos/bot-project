# import os
# import logging
# import requests
# from aiogram import Bot, Dispatcher, executor, types, md
# from aiogram.bot.api import TelegramAPIServer
# from aiogram.dispatcher import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.types import ContentType
# from aiogram.dispatcher.filters.state import State, StatesGroup
#
# logging.basicConfig(level=logging.INFO)
# TG_TOKEN = os.getenv("TG_TOKEN", "5220235572:AAHCzRB9h29vHs57kh24_aBI7Q_ouALl0DA")  # Telegram Bot API Key
#
# bot = Bot(token=TG_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
# dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())
#
#
# class Scoring(StatesGroup):
#     offer_to_start = State()
#     start = State()
#     audio = State()
#     analysis = State()
#     finish = State()
#
#
#
#
# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
#     await types.ChatActions.typing()
#     await message.answer(md.text(md.bold(f"Hi {message.from_user.first_name}👋!"),
#                                  md.text(f"It is", md.underline(f"{(await bot.me).first_name}")),
#                                  md.text(md.italic("\nPowered by "),
#                                          md.link("aiogram", "https://docs.aiogram.dev/en/latest/index.html")),
#                                  sep="\n"))
#     await message.answer(md.text("🦋"))
#     await message.answer(md.italic("NB: you can type {command} to see all actions".format(command="/help")))
#
#
# @dp.message_handler(commands=['accent'])
# async def process_accent_command(message: types.Message):
#     # result = await bot.get_me()
#     await Scoring.start.set()
#     await types.ChatActions.typing()
#     await message.answer(md.text("Let's try to score your english accent\!"))
#     await message.answer(md.text("Please, dictate following in a voice message:"))
#     await types.ChatActions.typing(sleep=0.8)
#     await message.answer(md.text("\"London is the capital of Great Britain\""))
#     await Scoring.next()
#
#
# @dp.message_handler(lambda message: message.voice is None, state=Scoring.audio)
# async def process_audio_invalid(message: types.Message):
#     return await message.reply(md.text("Please, send me a voice message",
#                                        md.escape_md('...'), sep=''))
#
#
# @dp.message_handler(content_types=ContentType.VOICE, state=Scoring.audio)
# async def process_audio(message: types.Voice):
#     await types.ChatActions.typing()
#     file = await bot.get_file(message.voice.file_id)
#     await bot.download_file(file.file_path, destination_dir='audio/')
#     await message.answer(md.text(md.text(f"Great\! Your english accent analysis started"),
#                                  md.escape_md("..."),
#                                  sep=''))
#     await message.answer("🕐")
#     response = requests.post("http://server:8000/api/predict/?audio=audio").json()
#     await message.answer(f"Your score is {response['score']} points, heal yeah")
#     await Scoring.reset_state()
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     markup.add("Finish", "Continue")
#     await message.answer("Finish?", reply_markup=markup)
#
#
# @dp.message_handler(content_types=ContentType.VOICE, state='*')
# async def process_some_audio(message: types.Voice):
#     await types.ChatActions.typing()
#     duration = message.to_python()['voice']['duration']
#     await message.reply(md.text(md.text(f"Wow\! {duration} seconds of voice\!"),
#                                 md.text("What are you trying to say?"),
#                                 md.text(f"{message.content_type}"),
#                                 sep="\n"))
#     Scoring.offer_to_start.set()
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     markup.add("Yes", "No")
#     markup.add("Next time :)")
#     await message.answer("Do you wanna score your english accent?", reply_markup=markup)
#
#
# @dp.message_handler(lambda message: message.text.lower() != 'yes', state=Scoring.offer_to_start)
# async def process_offer_to_start_no(message: types.Message):
#     # result = await bot.get_me()
#     await Scoring.finish()
#     await types.ChatActions.typing()
#     await message.answer(md.text("Fine, next time\!"))
#
#
# @dp.message_handler(lambda message: message.text.lower() == 'yes', state=Scoring.offer_to_start)
# async def process_offer_to_start_yes(message: types.Message):
#     # result = await bot.get_me()
#     await process_accent_command(message)
#
#
# @dp.message_handler(content_types=ContentType.TEXT)
# async def echo(message: types.Message):
#     await types.ChatActions.typing()
#     await message.answer(f'{message.from_user.first_name} said: {message.text}')
from handlers import bot, dp, executor

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
