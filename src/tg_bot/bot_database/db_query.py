from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from bot_database.models import Users, Categories, User_categories


# ############ Категории ############# #

async def orm_get_categories_from_name(session: AsyncSession,
                                       topic: str):
    query = select(Categories.id).where(Categories.name == topic)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_name_category_from_id(session: AsyncSession,
                                        id: int):
    query = select(Categories.name).where(Categories.id == id)
    result = await session.execute(query)
    return result.scalar()


# ############ Пользователи ############# #


async def orm_add_user(session: AsyncSession,
                       user_id: int,
                       nick: str):
    query = select(Users).where(Users.chat == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(Users(chat=user_id, nick_name=nick))
        await session.commit()


# ############ Пользователи и Категории ############# #


async def orm_add_users_category(session: AsyncSession,
                                 user: int,
                                 category: int):
    query = select(User_categories).where(User_categories.user_id == user,
                                          User_categories.category_id == category)
    result = await session.execute(query)
    if result.first() is None:
        session.add(User_categories(user_id=user, category_id=category))
        await session.commit()


async def orm_delete_users_category(session: AsyncSession,
                                    id: int):
    query = delete(User_categories).where(User_categories.user_id == id)
    await session.execute(query)
    await session.commit()


async def orm_get_users_categories(session: AsyncSession,
                                   id: int):
    query = select(User_categories.category_id).where(User_categories.user_id == id)
    result = await session.execute(query)
    return result.scalars().all()
