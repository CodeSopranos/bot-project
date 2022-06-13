import os
import logging
from aiogram import Bot, Dispatcher, executor, types, md
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.dispatcher.filters.state import State, StatesGroup


logging.basicConfig(level=logging.INFO)
TG_TOKEN = os.getenv("TG_TOKEN", None)  # Telegram Bot API Key

bot = Bot(token=TG_TOKEN, parse_mode=None)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# main dialog flow
class DialogState(StatesGroup):
    offer_to_start = State()
    start = State()
    audio = State()
    analysis = State()
    finish = State()
    denoise = State()