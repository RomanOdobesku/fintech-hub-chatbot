import schedule
import json
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.backend.models import News, Base, Categories
import requests
from typing import List
import time
from tqdm import tqdm

from datetime import datetime
from datetime import timedelta

connection_string = URL.create(
  'postgresql',
  username='roman',
  password='gBsF2yztQ9pD',
  host='ep-bold-mouse-a2jqmrzs.eu-central-1.aws.neon.tech',
  database='postgresql',
  query={'sslmode':'require'}
)

engine = create_engine(connection_string, echo=True)
session = sessionmaker(bind=engine)()


def add_news(content, title='', url='', category_id='', score=1, ):
    news = News(
        title=title,
        url=url,
        category_id=category_id,
        score=score,
        content=content,
    )

    session.add(news)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print('Проблема с добавлением новости')


def update_info(minutes: int = 20):
    
    current_time = datetime.now()
    previous_time = current_time - timedelta(minutes=minutes)

    # title classification
    query = select(News).filter(News.score==None, News.title!=None, News.content!=None, News.created >= previous_time).order_by(News.created.desc())

    result = session.execute(query)
    result = result.scalars().all()

    print(len(result))

    for news in tqdm(result):

        answer = 0

        if len(news.title) > 0:

            data = json.dumps({"text": news.title})
            url = "http://10.6.156.21:8000/title/"
            response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

            answer = int(response.text)
            
        session.query(News).filter(
            News.id==news.id
        ).update({"score": answer}, synchronize_session='fetch')
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f'Проблема с добавлением Score. news.id: {news.id}')


    # summarization
    query = select(News).filter(News.summary==None, News.content!=None, News.score==1, News.created >= previous_time).order_by(News.created.desc())

    result = session.execute(query)
    result = result.scalars().all()

    print(len(result))

    for news in tqdm(result):

        text = news.title + '\n' + news.content

        summary = "Something went wrong, there's no text in DB"

        if len(news.content) > 0:

            data = json.dumps({"text": text})
            url = "http://10.6.156.21:8000/llm/"
            response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

            print(text)
            print(response.text)

            if response:
                if type(response.text)==str:
                    if len(response.text)!=0:
                        summary = response.text
            
        session.query(News).filter(
            News.id==news.id
        ).update({"summary": summary}, synchronize_session='fetch')
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f'Проблема с добавлением суммаризации. news.id: {news.id}')

    # category classification
    query = select(News).filter(News.category_id==None, News.title!=None, News.content!=None, News.created >= previous_time).order_by(News.created.desc())

    result = session.execute(query)
    result = result.scalars().all()

    for news in tqdm(result):

        text = news.title + '\n' + news.content

        answer = 4

        if len(news.content) > 0:

            data = json.dumps({"text": text})
            url = "http://10.6.156.21:8000/category/"
            response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

            answer = int(response.text)
            
        session.query(News).filter(
            News.id==news.id
        ).update({"category_id": answer}, synchronize_session='fetch')
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f'Проблема с добавлением category_id. news.id: {news.id}')


def get_news_by_ids(news_ids: List[int]):
    query = select(News).filter(News.id.in_(news_ids))
    result = session.execute(query)
    result = result.scalars()
    for news in result:
        print(f'Title: {news.title}')
        print(f'Summary: {news.summary}')


if __name__=='__main__':

    schedule.every(10).seconds.do(update_info) # запускаем раз в 10 секунд, но внутри функции берем данные за 20 минут.
    # насколько я понял, в следующий раз он запустится только после того как отработает первый

    while True:
        schedule.run_pending()
        time.sleep(1)
