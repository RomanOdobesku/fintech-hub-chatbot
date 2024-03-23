from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.formatting import Bold, as_list, as_marked_section
from sqlalchemy.ext.asyncio import AsyncSession
import bot_database.db_query as db_query
from kb import reply

user_private_router = Router()


@user_private_router.message(Command("start"))
async def start_handler(msg: Message, session: AsyncSession) -> None:
    await msg.answer("""Привет 👻, я виртуальный помощник для отслеживания новостей по разными темам в финтех-сфере! Выбери нужные категории, и я буду присылать тебе самые свежие новости!""",
                     reply_markup=reply.start_kb)
    await db_query.orm_add_user(session, msg.from_user.id, msg.from_user.first_name)


@user_private_router.message(Command("restart"))
async def restart(msg: Message) -> None:
    await msg.answer("Вы уверены, что хотите сбросить текущие подписки?",
                     reply_markup=reply.restart_categories_kb)


@user_private_router.message(Command("my_categories"))
async def print_categories(msg: Message, session: AsyncSession) -> None:
    users_id = msg.from_user.id
    print("ТУТ", users_id)
    cats = await db_query.orm_get_users_categories(session, users_id)
    names = [await db_query.orm_get_name_category_from_id(session, element) for element in cats]
    answer_message = "Ваш список тем:\n"
    for element in names:
        answer_message += f"- {element}\n"
    await msg.answer(answer_message)


@user_private_router.message(Command("help"))
async def help_handler(msg: Message) -> None:
    await msg.answer("""Тут потом будет краткая инфа о боте, о категориях, о дайджесте и других функциях, если они появятся""")


@user_private_router.callback_query(F.data.startswith('print_help'))
async def print_help(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer("""Тут потом будет краткая инфа о боте, о категориях, о дайджесте и других функциях, если они появятся""")


@user_private_router.callback_query(F.data.startswith('choose_category'))
async def category_hadnler(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer("Выбери категории для отслеживания:", reply_markup=reply.categories_kb)


@user_private_router.callback_query(F.data.startswith('subscribe_finish'))
async def subscribe_finish(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await callback.message.answer(text='Подписки сохранены!')


@user_private_router.callback_query(F.data.startswith('subscribe_'))
async def subscribe_topic(callback: CallbackQuery, session: AsyncSession):
    topic = callback.data.split("_")[-1]

    if topic != 'finish':
        curr = await db_query.orm_get_categories_from_name(session, topic)
        await db_query.orm_add_users_category(session, callback.from_user.id, curr)
    else:
        callback.answer("Подписки сохранены!", reply_markup=ReplyKeyboardRemove)


@user_private_router.callback_query(F.data.startswith('restart_no'))
async def restart_no(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.delete()


@user_private_router.callback_query(F.data.startswith('restart_yes'))
async def restart_yes(callback: CallbackQuery, session: AsyncSession):
    await callback.message.edit_reply_markup()
    await db_query.orm_delete_users_category(session, callback.from_user.id)
    await callback.message.answer("Все подписки удалены!")
    await callback.message.answer("Выбери категории для отслеживания:", reply_markup=reply.categories_kb)

