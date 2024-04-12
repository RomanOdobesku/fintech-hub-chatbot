from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.models import Users, Categories, UserCategories, News


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
                                      cat_id: int) -> Optional[str]:
    """
    Получает название категории из базы данных по ее идентификатору.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - cat_id (int): Идентификатор категории, по которому будет выполнен поиск.

    Возвращает:
    - str: имя категории.
    """
    query = select(Categories.name).where(Categories.id == cat_id)
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
                       user_id: str,
                       nick: str) -> None:
    """
    Добавляет нового пользователя в базу данных, если записи о нем еще не существует.

    Аргументы:
    - session (Asyncsession): Сессия асинхронного соединения с базой данных.
    - user_id (str): Идентификатор telegram-чата с пользователем.
    - nict (str): Имя пользователя из telegram.

    Возвращает:
    - None
    """

    query = select(Users).where(Users.chat == user_id)
    result = await session.execute(query)
    if result.first() is None:
        user = Users(chat=user_id, username=nick)
        session.add(user)
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
                                 user: str,
                                 category: int) -> None:
    """
    Добавляет выбранную категорию и идентификатор пользователя в базу данных.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - user (str): Идентификатор чата с пользователем.
    - category (int): Идентификато выбранной пользователем категории из базы данных.

    Возвращает:
    - None
    """
    query = select(UserCategories).where(UserCategories.user_id == str(user),
                                         UserCategories.category_id == category)

    result = await session.execute(query)
    if result.first() is None:
        session.add(UserCategories(user_id=str(user), category_id=category))
        await session.commit()


async def orm_delete_users_category(session: AsyncSession,
                                    user: str) -> None:
    """
    Удаляет из базы данных категории, выбранные пользователем.

    Аргументы:
    - session (ASyncSession): Сессия асинхронного соединения с базой данных.
    - user (str): Идентификатор чата с пользователем.

    Возвращает:
    - None
    """
    query = delete(UserCategories).where(UserCategories.user_id == user)
    await session.execute(query)
    await session.commit()


async def orm_get_users_categories(session: AsyncSession,
                                   user: str) -> List[int]:
    """
    Возвращает идентификаторы выбранных пользователем категорий.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединения с базой данных.
    - user (int): Идентификатор чата с пользователем.

    Возвращает:
    - List[int]: Список идентификаторов из базы данных выбранных категорий.
    """

    print()
    print('ПОЛЬЗОВАТЕЛЬСКИЕ КАТЕГОРИИ ТУТ')
    print()

    query = select(UserCategories.category_id).where(UserCategories.user_id == user)
    result = await session.execute(query)
    result = result.scalars().all()
    return result


# ############ Новости ############# #


async def orm_get_latest_news_by_categories(session: AsyncSession) -> Dict[int, List[Any]]:
    """
    Получает из базы данных по 5 новых новостей для каждой категории.

    Аргументы:
    - session (AsyncSession): Сессия асинхронного соединениия с базой данных.

    Возвращает:
    - Dict[int, List[Any]]: Словарь новостей, где ключ - идентификатор категории, а ключ - список с
    соответствующими полями таблицы News базы данных.
    """

    news = dict()
    current_time = datetime.now()
    previous_day = current_time - timedelta(days=1)

    category_id = [i for i in range(1, 9)]
    for category in category_id:
        query = select(News).where(News.category_id == category,
                                   News.updated >= previous_day,
                                   News.score == 1,
                                   News.content is not None,
                                   News.summary is not None,
                                   News.summary != "Something went wrong, there's no text in DB").order_by(News.updated.desc())
        result = await session.execute(query)
        result = result.scalars().all()
        news[category] = result
    return news
