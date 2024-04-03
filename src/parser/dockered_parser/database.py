import json
import os

import pandas as pd

from models import Base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import News, Categories
from dotenv import load_dotenv

_engine = None
_session = None
_engine_async = None
_session_async = None


def create_tables():
    # создание таблиц
    global _engine
    if _engine is None:
        load_dotenv('.env')
        # print(os.getenv('DB_POSTGRESQL_ASYNC'))
        _engine = create_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    Base.metadata.create_all(_engine)


def fill_database_from_parser(news: pd.DataFrame):
    # пример заполненения таблицы данными из парсера
    global _engine
    if _engine is None:
        load_dotenv('.env')
        _engine = create_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    global _session
    if _session is None:
        _session = sessionmaker(_engine, expire_on_commit=False)()

    for (_id, new) in news.iterrows():
        element = News(
            title=new['title'],
            url=new['url'],
            content=new['content'],
            created=new['time'],
        )
        _session.add(element)
    _session.commit()


async def create_tables_async():
    # создание таблиц
    global _engine_async
    if _engine_async is None:
        load_dotenv('.env')
        _engine_async = create_async_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    await Base.metadata.create_all(_engine)


async def fill_database_from_parser_async(news: pd.DataFrame):
    # пример заполненения таблицы данными из парсера
    global _engine_async
    if _engine_async is None:
        load_dotenv('.env')
        _engine_async = create_async_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    global _session_async
    if _session_async is None:
        _session_async = sessionmaker(_engine_async, expire_on_commit=False, class_=AsyncSession)()

    for (_id, new) in news.iterrows():
        element = News(
            title=new['title'],
            url=new['url'],
            content=new['content'],
            created=new['time'],
        )
        _session_async.add(element)
    await _session_async.commit()
