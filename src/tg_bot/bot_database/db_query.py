import sys
import os
from typing import Optional, List, Dict, Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

# для правильного имортирования файла из другой папки (иначе почему-то не работает)

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT, PACKAGE_PARENT)))

from backend.models import Users, Categories, UserCategories, News


# ############ Категории ############# #

async def orm_get_id_category_by_name(session: AsyncSession,
                                      topic: str) -> Optional[int]:
    """
    Получает идентификатор категории из базы данных по ее имени.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - topic (str): Имя категории, по которой будет выполнен поиск.

    Возвращает:
    - int: индектификатор категории.
    """
    query = select(Categories.id).where(Categories.name == topic)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_name_category_by_id(session: AsyncSession,
                                        id: int) -> Optional[str]:
    """
    Получает название категории из базы данных по ее идентификатору.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - id (int): Идентификатор категории, по которому будет выполнен поиск.

    Возвращает:
    - str: имя категории.
    """
    query = select(Categories.name).where(Categories.id == id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_list_of_category(session: AsyncSession) -> Dict[int, str]:
    """
    Получает список категории из базы данных и возвращает словарь с ключами -
    идентификаторами категорий и значениями - названиями категорий.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - Dict[int, str]: Словарь с категориями, где ключ - идентификатор категории,
    значение - название категории
    """
    query = select(Categories)
    result = await session.execute(query)
    result = result.scalars()
    dct = dict()
    for cat in result:
        dct[cat.id] = cat.name
    return dct


# ############ Пользователи ############# #


async def orm_add_user(session: AsyncSession,
                       user_id: int,
                       nick: str) -> None:
    """
    Добавляет нового пользователя в базу данных, если записи о нем еще не существует.

    Аргументы:
    - session (Asyncsession): Сессия асинхронного соединения с базой данных.
    - user_id (int): Идентификатор telegram-чата с пользователем.
    - nict (str): Имя пользователя из telegram.

    Возвращает:
    - None
    """
    query = select(Users).where(Users.chat == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(Users(chat=user_id, username=nick))
        await session.commit()


async def orm_get_list_of_users(session: AsyncSession) -> List[str]:
    """
    Получает список идентификаторов активных чатов с пользователями из базы данных.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.

    Возвращает:
    - List[str]: Список идентификаторов чатов всех активных пользователей.
    """
    query = select(Users.chat)
    result = await session.execute(query)
    return result.scalars().all()


# ############ Пользователи и Категории ############# #


async def orm_add_users_category(session: AsyncSession,
                                 user: int,
                                 category: int) -> None:
    """
    Добавляет выбранную категорию и идентификатор пользователя в базу данных.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - user (int): Идентификатор чата с пользователем.
    - category (int): Идентификато выбранной пользователем категории из базы данных.

    Возвращает:
    - None
    """
    query = select(UserCategories).where(UserCategories.user_id == user,
                                         UserCategories.category_id == category)
    result = await session.execute(query)
    if result.first() is None:
        session.add(UserCategories(user_id=user, category_id=category))
        await session.commit()


async def orm_delete_users_category(session: AsyncSession,
                                    user: int) -> None:
    """
    Удаляет из базы данных категории, выбранные пользователем.

    Аргументы:
    - session (ASyncSession): Сессия асинхронного соединения с базой данных.
    - user (int): Идентификатор чата с пользователем.

    Возвращает:
    - None
    """
    query = delete(UserCategories).where(UserCategories.user_id == user)
    await session.execute(query)
    await session.commit()


async def orm_get_users_categories(session: AsyncSession,
                                   user: int) -> List[int]:
    """
    Возвращает идентификаторы выбранных пользователем категорий.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - user (int): Идентификатор чата с пользователем.

    Возвращает:
    - List[int]: Список идентификаторов из базы данных выбранных категорий.
    """
    query = select(UserCategories.category_id).where(UserCategories.user_id == user)
    result = await session.execute(query)
    return result.scalars().all()


# ############ Новости ############# #


async def orm_get_latest_news_by_categories(session: AsyncSession) -> Dict[int, List[Any]]:
    """
    Получает из базы данных по 5 новых новостей для каждой категории.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединениия с базой данных.

    Возвращает:
    - Dict[int, List[Any]]: Словарь новостей, где ключ - идентификатор категории, а ключ - список с
    соответствующими полями таблицы News базы данных."""
    news = dict()
    category_id = [i for i in range(1, 9)]
    for category in category_id:
        query = select(News).where(News.category_id == category).order_by(News.created.desc()).limit(5)
        result = await session.execute(query)
        result = result.scalars().all()
        news[category] = result
    return news
