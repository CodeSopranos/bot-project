from aiogram import md, types
from aiogram.types import ContentType

from handlers.base import bot, dp, DialogState
from handlers.keyboards import get_offer_start_keyboard


@dp.message_handler(commands=['play'], state='*')
async def process_play_command(message: types.Message):
    await bot.send_dice(emoji='🏀', chat_id=message.chat.id)


@dp.message_handler(content_types=ContentType.TEXT, state='*')
async def echo(message: types.Message):
    await types.ChatActions.typing()
    # Get a response to the input text 'I would like to book a flight.'
    response = chit_chat.get_response(message)
    print(response)
    await message.answer(str(response))


@dp.message_handler(content_types=ContentType.VOICE, state='*')
async def process_some_audio(message: types.Voice):
    await types.ChatActions.typing()
    duration = message.to_python()['voice']['duration']
    await message.reply(md.text(md.text(f"Wow\! {duration} seconds long voice msg\!"),
                                md.text("What are you trying to say?"),
                                sep="\n"), parse_mode=types.ParseMode.MARKDOWN_V2)
    DialogState.offer_to_start.set()
    markup = await get_offer_start_keyboard()
    await message.answer("Do you wanna score your english accent?", reply_markup=markup)


from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chat bot named Charlie
chit_chat = ChatBot('Small-Talker',
                    read_only=True,
                    storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    logic_adapters=[
                        'chatterbot.logic.BestMatch',
                        'chatterbot.logic.MathematicalEvaluation',
                    ]
                    )
# trainer = ChatterBotCorpusTrainer(chit_chat.storage)
# trainer.train(
#     "chatterbot.corpus.english.conversations",
#     "chatterbot.corpus.english.emotion",
    # "chatterbot.corpus.english.greetings",
    # "chatterbot.corpus.english.humor",
    # "chatterbot.corpus.english.movies",
    # "chatterbot.corpus.english.trivia",
    # "chatterbot.corpus.english.botprofile",
    # "chatterbot.corpus.english.ai",
# )