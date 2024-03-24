import json
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import News, Base, Categories

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

# строка движок и подключение к базе данных
engine = create_engine(os.getenv('DB_LITE'), echo=True)
conn = engine.connect()


# создаем полученную базу данных и сохраняем ее (пока пустую)
Base.metadata.create_all(engine)


# подготовляем сессию для работы
session = sessionmaker(bind=engine)()

# заполнение таблицы categories известными категориями
category_list = ["cr",
                 "ai",
                 "cbdc",
                 "oth",
                 "bid",
                 "tok",
                 "defi",
                 "api"]

for ctg in category_list:
    element = Categories(name=ctg)
    session.add(element)
session.commit()


# открытие файла json после парсинга новостей
with open('data/dict_hub.json', encoding='utf-8') as dataframe:
    news = json.loads(dataframe.read())


# заполнение таблицы News новостями из самого первого датасета
for element, info_element in news.items():
    category = info_element['category']

    # новости без категории закинем в категорию other
    if category == "none":
        category = 'oth'

    # достаем id категории из бд
    id_category_from_db = select(Categories.id).where(Categories.name == category)

    # заполняем необходимые поля в нашей бд и закидываем в нее
    news = News(title=info_element['article_title'],
                url=info_element['article_url'],
                category_id=id_category_from_db,
                score=info_element['score']
                # content = info_element['text'], # 
                # summary = info_element['text']
                )

    session.add(news)
session.commit()
