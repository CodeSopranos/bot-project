from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton


async def get_offer_start_keyboard() -> ReplyKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    btn_1 = InlineKeyboardButton('Yes 🤩', callback_data='offer_yes')
    btn_2 = InlineKeyboardButton('Next time 😅', callback_data='offer_no')
    markup.row(btn_1, btn_2)
    return markup


async def get_finish_keyboard() -> ReplyKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    btn_1 = InlineKeyboardButton('Finish ✌️', callback_data='finish_yes')
    btn_2 = InlineKeyboardButton('One more try 🙏', callback_data='finish_try')
    markup.row(btn_1, btn_2)
    return markup