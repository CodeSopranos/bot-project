import os
import requests

from aiogram import md, types
from aiogram.types import ContentType, InputFile

from handlers.base import bot, dp, DialogState
from handlers.keyboards import *

FILE_BASE = 'audio/'
FILE_BASE_DENOISE = 'audio/denoise/'
ACCENT_API = "http://server:8000/api/audio/accent-recognition/"
DENOISE_API = "http://server:8000/api/audio/denoise/"
DUMMY_API = "http://server:8000/api/predict/?audio=audio"


@dp.message_handler(commands=['denoise'], state='*')
async def process_denoise_command(message: types.Message):
    await types.ChatActions.typing()
    await message.answer(md.text("Please, send me some noisy voice audio..."))
    await DialogState.denoise.set()


@dp.message_handler(content_types=ContentType.VOICE, state=DialogState.denoise)
async def denoise_audio(message: types.Voice):
    await types.ChatActions.typing()
    file = await bot.get_file(message.voice.file_id)
    filename = file.file_path.replace('file', get_username(message))
    filepath = os.path.join(FILE_BASE_DENOISE, filename)
    await bot.download_file(file.file_path, destination=filepath)
    await message.answer(md.text(f"Very fast! Denoising started..."))
    await message.answer("🕐")
    file = {'file': open(filepath, 'rb')}
    response = requests.post(DENOISE_API, files=file)
    open(filepath, "wb").write(response.content)
    await message.answer(md.text(f"...And here is cleaned version!"))
    await bot.send_audio(message.from_user.id, InputFile(filepath))


@dp.message_handler(commands=['accent'], state='*')
async def process_accent_command(message: types.Message):
    await DialogState.start.set()
    await types.ChatActions.typing()
    await message.answer(md.text("Let's try to score your english accent\!"), parse_mode=types.ParseMode.MARKDOWN_V2)
    await message.answer(md.text("Please, dictate following in a voice message:"),
                         parse_mode=types.ParseMode.MARKDOWN_V2)
    await types.ChatActions.typing(sleep=0.8)
    response = requests.get("http://server:8000/api/get_sample/").json()
    await message.answer(md.text(response['sample']))
    await DialogState.next()


@dp.message_handler(lambda message: message.voice is None, state=DialogState.audio)
async def process_audio_invalid(message: types.Message):
    return await message.reply(md.text("Please, send me a voice message",
                                       md.escape_md('...'), sep=''), parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(content_types=ContentType.VOICE, state=DialogState.audio)
async def process_audio(message: types.Voice):
    await types.ChatActions.typing()
    file = await bot.get_file(message.voice.file_id)
    filename = file.file_path.replace('file', get_username(message))
    filepath = os.path.join(FILE_BASE, filename)
    await bot.download_file(file.file_path, destination=filepath)
    await message.answer(md.text(md.text(f"Great\! Your english accent analysis started"),
                                 md.escape_md("..."),
                                 sep=''), parse_mode=types.ParseMode.MARKDOWN_V2)
    await message.answer("🕐")

    file = {'file': open(filepath, 'rb')}
    response = requests.post(ACCENT_API, files=file).json()

    await message.answer(f"Your score is {response['score']} points  (from 100), heal yeah!")
    await message.answer(f"Most similar accents:")
    await message.answer(response['pretty_print'])

    await DialogState.finish.set()
    markup = await get_finish_keyboard()
    await message.answer("What's next?", reply_markup=markup)


@dp.message_handler(lambda message: message.text.lower() != 'yes', state=DialogState.offer_to_start)
async def process_offer_to_start_no(message: types.Message):
    await DialogState.finish()
    await types.ChatActions.typing()
    await message.answer(md.text("Fine, next time\!"), parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(lambda message: message.text.lower() == 'yes', state=DialogState.offer_to_start)
async def process_offer_to_start_yes(message: types.Message):
    await process_accent_command(message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('finish'), state='*')
async def process_finish_callback(callback_query: types.CallbackQuery):
    code = callback_query.data.split('_')[-1]
    _command = '/links'
    if code == 'try':
        await process_accent_command(callback_query.message)
    else:
        await types.ChatActions.typing()
        await bot.send_message(callback_query.from_user.id, "Alright 🤙")
        await types.ChatActions.typing()
        await bot.send_message(callback_query.from_user.id, f"Type {_command} if you want to get useful materials 🧠")


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('offer'), state='*')
async def process_offer_callback(callback_query: types.CallbackQuery):
    code = callback_query.data.split('_')[-1]
    if code == 'yes':
        await process_accent_command(callback_query.message)
    else:
        await bot.send_message(callback_query.from_user.id, f"You say {code} I say OK 😐")


def get_username(message):
    if message.from_user.username is None:
        return str(message.from_user.id)
    return message.from_user.username
