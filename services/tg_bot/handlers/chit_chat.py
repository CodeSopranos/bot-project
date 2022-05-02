from aiogram import md, types
from aiogram.types import ContentType

from handlers.base import dp, DialogState
from handlers.keyboards import get_offer_start_keyboard


@dp.message_handler(content_types=ContentType.TEXT, state='*')
async def echo(message: types.Message):
    await types.ChatActions.typing()
    await message.answer(f'{message.from_user.first_name} said: {message.text}')


@dp.message_handler(content_types=ContentType.VOICE, state='*')
async def process_some_audio(message: types.Voice):
    await types.ChatActions.typing()
    duration = message.to_python()['voice']['duration']
    await message.reply(md.text(md.text(f"Wow\! {duration} seconds long voice msg\!"),
                                md.text("What are you trying to say?"),
                                sep="\n"))
    DialogState.offer_to_start.set()
    markup = await get_offer_start_keyboard()
    await message.answer("Do you wanna score your english accent?", reply_markup=markup)
