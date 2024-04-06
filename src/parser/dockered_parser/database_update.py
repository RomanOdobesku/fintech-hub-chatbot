import os
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.exc import NoResultFound, IntegrityError

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from models import News, Categories
from dotenv import load_dotenv
import database


def clean_site(site: str) -> str:
    return BeautifulSoup(site, features='lxml').text


def check_and_update_all_news():
    links = []
    from database import _engine
    if _engine is None:
        load_dotenv('.env')
        _engine = create_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    from database import _session
    if _session is None:
        _session = sessionmaker(_engine, expire_on_commit=False)()
    for article in _session.query(News).filter(News.content == None).all():
        links.append(article.url)
        print(article)
    from parser import parse_links
    texts = parse_links(links, 100)
    for i in range(len(texts)):
        try:
            texts[i] = clean_site(texts[i])
        except:
            pass
    for i in range(len(links)):
        url = links[i]
        try:
            # Check if the URL already exists in the database
            article = _session.query(News).filter(News.url == url).one()
            article.content = texts[i]
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


def clean_existed():
    from database import _engine
    if _engine is None:
        load_dotenv('.env')
        _engine = create_engine(os.getenv('DB_POSTGRESQL_ASYNC'))
    from database import _session
    if _session is None:
        _session = sessionmaker(_engine, expire_on_commit=False)()
    for article in _session.query(News).all():
        try:
            try:
                cls = clean_site(article.content)
                print(type(cls), cls)
                article.content = cls
                _session.commit()
            except IntegrityError:
                _session.rollback()
                print("IntegrityError occurred. Rolling back changes.")
            except Exception as e:
                _session.rollback()
                print("An error occurred while committing changes:", e)
            except:
                print("unhandled ex")
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


clean_existed()
# check_and_update_all_news()
