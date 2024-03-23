from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбор категории", callback_data="choose_category")],
        [InlineKeyboardButton(text="Помощь", callback_data="print_help")]
    ]
)

categories_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='cr', callback_data="subscribe_cr")],
        [InlineKeyboardButton(text='ai', callback_data="subscribe_ai")],
        [InlineKeyboardButton(text="cbdc", callback_data="subscribe_cbdc")],
        [InlineKeyboardButton(text="bid", callback_data="subscribe_bid")],
        [InlineKeyboardButton(text="tok", callback_data="subscribe_tok")],
        [InlineKeyboardButton(text="defi", callback_data="subscribe_defi")],
        [InlineKeyboardButton(text="api", callback_data="subscribe_api")],
        [InlineKeyboardButton(text="other", callback_data="subscribe_oth")],
        [InlineKeyboardButton(text="finish", callback_data="subscribe_finish")]
    ]
)

restart_categories_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data="restart_yes")],
        [InlineKeyboardButton(text='Нет', callback_data="restart_no")]
    ]
)