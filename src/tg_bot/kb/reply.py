from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбор категории", callback_data="choose_category")],
        [InlineKeyboardButton(text="Помощь", callback_data="print_help")]
    ]
)

categories_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Крипто',
                              callback_data="subscribe_Крипто")],
        [InlineKeyboardButton(text='Искусственный интеллект',
                              callback_data="subscribe_Искусственный интеллект")],
        [InlineKeyboardButton(text="ЦВЦБ",
                              callback_data="subscribe_ЦВЦБ")],
        [InlineKeyboardButton(text="Биометрия и идентификация",
                              callback_data="subscribe_Биометрия и идентификация")],
        [InlineKeyboardButton(text="Токенизация",
                              callback_data="subscribe_Токенизация")],
        [InlineKeyboardButton(text="Децентрализованные финансы",
                              callback_data="subscribe_Децентрализованные финансы")],
        [InlineKeyboardButton(text="Открытые API",
                              callback_data="subscribe_Открытые API")],
        [InlineKeyboardButton(text="Прочее",
                              callback_data="subscribe_Прочее")],
        [InlineKeyboardButton(text="finish",
                              callback_data="subscribe_finish")]
    ],
)

restart_categories_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data="restart_yes")],
        [InlineKeyboardButton(text='Нет', callback_data="restart_no")]
    ]
)
