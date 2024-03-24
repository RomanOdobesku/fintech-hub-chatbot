from aiogram.types import BotCommand

command_for_private_channels = [
    BotCommand(command='restart', description='Сбросить темы и выбрать новые'),
    BotCommand(command='help', description='Справочная информация'),
    BotCommand(command='my_categories', description='Список выбранных тем'),
    BotCommand(command='digest', description='Сформировать дайджест новостей')
]
