from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from src.tg_bot.kb import reply
import src.tg_bot.bot_database.db_query as db_query

user_private_router = Router()


@user_private_router.message(Command("start"))
async def start_handler(msg: Message, session: AsyncSession) -> None:
    """
    Обработчик команды "/start". Отправляет приветственное сообщение пользователю
    и добавляет его в базу данных.

    Аргументы:
    - msg (Message): Объект сообщения от пользователя.
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - None
    """
    await msg.answer("""Привет 👻, я виртуальный помощник для отслеживания новостей по разными темам в финтех-сфере! Выбери нужные категории, и я буду присылать тебе самые свежие новости!""",
                     reply_markup=reply.start_kb)
    await db_query.orm_add_user(session, msg.from_user.id, msg.from_user.first_name)


@user_private_router.message(Command("restart"))
async def restart(msg: Message) -> None:
    """
    Обработчик команды "/restart". Выводит inline-клавиатуру "да/нет".

    Аргументы:
    - msg (Message): Объект сообщения от пользователя.

    Возвращает:
    - None
    """
    await msg.answer("Вы уверены, что хотите сбросить текущие подписки?",
                     reply_markup=reply.restart_categories_kb)


@user_private_router.message(Command("my_categories"))
async def print_categories(msg: Message, session: AsyncSession) -> None:
    """
    Обработчик команды "/my_categories". Выводит сообщение с перечисленными названиями категорий.

    Аргументы:
    - msg (Message): Объект сообщения от пользователя.
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - None
    """
    users_id = msg.from_user.id
    cats = await db_query.orm_get_users_categories(session, users_id)
    names = [await db_query.orm_get_name_category_by_id(session, element) for element in cats]
    answer_message = "Ваш список тем:\n"
    for element in names:
        answer_message += f"- {element}\n"
    await msg.answer(answer_message)


@user_private_router.message(Command("help"))
async def help_handler(msg: Message) -> None:
    """
    Обработчик команды "/help". Выводит справку о боте.

    Аргументы:
    - msg (Message): Объект сообщения от пользователя.

    Возвращает:
    - None
    """
    await msg.answer("""Тут потом будет краткая инфа о боте, о категориях, о дайджесте и других функциях, если они появятся""")


@user_private_router.message(Command("digest"))
async def send_news_to_subscribers(msg: Message, session: AsyncSession) -> None:
    """
    Обработчик команды "/digest". Выводит по 5 недавних новостей
    по категориям, выбранных пользователем.

    Аргументы:
    - msg (Message): Объект сообщения от пользователя.
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - None
    """
    users_chat_id = await db_query.orm_get_list_of_users(session)
    latest_news = await db_query.orm_get_latest_news_by_categories(session)
    category = await db_query.orm_get_list_of_category(session)

    for user in users_chat_id:
        message = ""
        subscriptions = await db_query.orm_get_users_categories(session, int(user))
        for subscription in subscriptions:
            message += "\n*Ваши новости по теме '{}'* \n".format(category[int(subscription)])
            for news in latest_news[int(subscription)]:
                message += f"\n{news.title}: {news.url}\n"

        await msg.answer(message, parse_mode=ParseMode.MARKDOWN)


@user_private_router.callback_query(F.data.startswith('print_help'))
async def print_help(callback: CallbackQuery):
    """
    Обработчик нажатия на кнопку "Помощь" стартовой клавиатуры. Выводит справку о боте.

    Аргументы:
    - callback (CallbackQuery): Объект сообщения от пользователя.

    Возвращает:
    - None
    """
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer("""Тут потом будет краткая инфа о боте, о категориях, о дайджесте и других функциях, если они появятся""")


@user_private_router.callback_query(F.data.startswith('choose_category'))
async def category_hadnler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку "Выбрать категорию". Выводит клавиатуру для выбора категорий.

    Аргументы:
    - callback (CallbackQuery): Объект сообщения от пользователя.
    Возвращает:
    - None
    """
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer("Выбери категории для отслеживания:",
                                  reply_markup=reply.categories_kb)


@user_private_router.callback_query(F.data.startswith('subscribe_finish'))
async def subscribe_finish(callback: CallbackQuery,
                           session: AsyncSession,
                           apscheduler: AsyncIOScheduler,
                           bot: Bot):
    """
    Обработчик нажатия на кнопку "finish". Убирает inline-клавиатуру с выбором категорий
    и выводит сообщение о сохранении подписок.

    Аргументы:
    - callback (CallbackQuery): Объект сообщения от пользователя.
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - apscheduler (AsyncIOScheduler): Scheduler для запуска автоматической рассылки дайджеста.
    - bot (Bot): Объект класса Bot для отправки сообщений.

    Возвращает:
    - None
    """
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer(text='Подписки сохранены!')
    apscheduler.add_job(send_message_time,
                        trigger='cron',
                        hour=16,
                        kwargs={'bot': bot, 'session': session})


@user_private_router.callback_query(F.data.startswith('subscribe_'))
async def subscribe_topic(callback: CallbackQuery, session: AsyncSession):
    """
    Обработчик нажатия на кнопку с категорией. Убирает inline-клавиатуру с выбором категорий
    и сохраняет выбранную категорию в базу данных.

    Аргументы:
    - callback (CallbackQuery): Объект сообщения от пользователя.
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - None
    """
    topic = callback.data.split("_")[-1]

    curr = await db_query.orm_get_id_category_by_name(session, topic)
    await db_query.orm_add_users_category(session, callback.from_user.id, curr)


@user_private_router.callback_query(F.data.startswith('restart_no'))
async def restart_no(callback: CallbackQuery):
    """
    Обработчик нажатия на кнопку 'Нет' при рестаре выбора категорий. Удаляет
    выведенную клавиатуру и подпись к ней.

    Аргументы:
    - callback (CallbackQuery): Объект сообщения от пользователя.

    Возвращает:
    - None
    """
    await callback.message.edit_reply_markup()
    await callback.message.delete()


@user_private_router.callback_query(F.data.startswith('restart_yes'))
async def restart_yes(callback: CallbackQuery, session: AsyncSession):
    """
    Обработчик нажатия на кнопку 'Да' при рестаре выбора категорий. Удаляет
    выведенную клавиатуру и подпись к ней, удаляет старые записи о категориях
    данного пользователя и вносит новые в базу данных.

    Аргументы:
    - callback (CallbackQuery): Объект сообщения от пользователя.
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - None
    """
    await callback.message.edit_reply_markup()
    await db_query.orm_delete_users_category(session, callback.from_user.id)
    await callback.message.answer("Все подписки удалены!")
    await callback.message.answer("Выбери категории для отслеживания:",
                                  reply_markup=reply.categories_kb)


async def send_message_time(bot: Bot, session: AsyncSession) -> None:
    """
    Генерирует и рассылает дайджесты последних новостей по категориям.

    Аргументы:
    - bot (Bot): Объект бота для рассылки сообщений пользователям.
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - None
    """
    users_chat_id = await db_query.orm_get_list_of_users(session)
    latest_news = await db_query.orm_get_latest_news_by_categories(session)
    category = await db_query.orm_get_list_of_category(session)

    for user in users_chat_id:
        message = ""
        subscriptions = await db_query.orm_get_users_categories(session, int(user))
        for subscription in subscriptions:
            message += "\n*Ваши новости по теме '{}'* \n".format(category[int(subscription)])
            for news in latest_news[int(subscription)]:
                message += f"{news.title}: {news.url}\n"

        await bot.send_message(chat_id=user, text=message, parse_mode=ParseMode.MARKDOWN)
