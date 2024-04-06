import os, sys

#todo
# sys.path.insert(1, "\\".join(os.path.realpath(__file__).split("\\")[0:-3]))

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.exc import NoResultFound, IntegrityError

from models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import News, Categories
from dotenv import load_dotenv

_engine = None
_session = None


# _engine_async = None
# _session_async = None


def create_tables():
    # создание таблиц
    global _engine
    if _engine is None:
        load_dotenv('.env')
        # print(os.getenv('DB_POSTGRESQL_ASYNC'))
        _engine = create_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    Base.metadata.create_all(_engine)


def fill_database_from_parser(news: pd.DataFrame) -> list[str]:
    # Example of filling the table with data from the parser
    new_articles_without_content = []
    global _engine
    if _engine is None:
        load_dotenv('.env')
        _engine = create_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    global _session
    if _session is None:
        _session = sessionmaker(_engine, expire_on_commit=False)()

    for (_, new) in news.iterrows():
        url = new['url']
        try:
            # Check if the URL already exists in the database
            _session.query(News).filter(News.url == url).one()
            # If it exists, do nothing
            # print('exists')
            continue
        except NoResultFound:
            # If it doesn't exist, add it to the database
            element = News(
                title=new['title'],
                url=url,
                content=new['content'],
                created=new['time'],
            )
            if new['content'] is None:
                new_articles_without_content.append(new)
            _session.add(element)
            # print('added')
        except Exception as e:
            print("An error occurred while querying the database:", e)
            _session.rollback()
            continue
    try:
        _session.commit()
    except IntegrityError:
        _session.rollback()
        print("IntegrityError occurred. Rolling back changes.")
    except Exception as e:
        _session.rollback()
        print("An error occurred while committing changes:", e)
    print('data pushed to database')
    _session.close()
    _session = None
    _engine.dispose()
    _engine = None
    return new_articles_without_content


def update_news(news: pd.DataFrame):
    global _engine
    if _engine is None:
        load_dotenv('.env')
        _engine = create_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    global _session
    if _session is None:
        _session = sessionmaker(_engine, expire_on_commit=False)()

    for (_, new) in news.iterrows():
        url = new['url']
        try:
            # Check if the URL already exists in the database
            article = _session.query(News).filter(News.url == url).one()
            try:
                workout = BeautifulSoup(new['content'], features='lxml').text
                new['content'] = workout
            except:
                pass
            article.content = new['content']

            try:
                _session.commit()
            except IntegrityError:
                _session.rollback()
                print("IntegrityError occurred. Rolling back changes.")
            except Exception as e:
                _session.rollback()
                print("An error occurred while committing changes:", e)
            continue
        except NoResultFound:
            print("error occured: no instances to update found")
        except Exception as e:
            print("An error occurred while querying the database:", e)
            _session.rollback()
            continue
    print('data updated in database')
    _session.close()
    _session = None
    _engine.dispose()
    _engine = None


# async def create_tables_async():
#     # создание таблиц
#     global _engine_async
#     if _engine_async is None:
#         load_dotenv('.env')
#         _engine_async = create_async_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
#     await Base.metadata.create_all(_engine)


# async def fill_database_from_parser_async(news: pd.DataFrame):
#     # пример заполненения таблицы данными из парсера
#     global _engine_async
#     if _engine_async is None:
#         load_dotenv('.env')
#         _engine_async = create_async_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
#     global _session_async
#     if _session_async is None:
#         _session_async = sessionmaker(_engine_async, expire_on_commit=False, class_=AsyncSession)()
#     for (_id, new) in news.iterrows():
#         element = News(
#             title=new['title'],
#             url=new['url'],
#             content=new['content'],
#             created=new['time'],
#         )
#         _session_async.add(element)
#     await _session_async.commit()
