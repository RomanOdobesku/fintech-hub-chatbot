import json
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import News, Base, Categories

# строка движок и подключение к базе данных
engine = create_engine("sqlite:///my_base.db", echo=True)
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
with open('src/backend/dict_hub.json', encoding='utf-8') as dataframe:
    news = json.loads(dataframe.read())


# заполнение таблицы News новостями из датасета после парсинга
for element, info_element in news.items():
    cat = info_element['category']
    if cat == "none":
        cat = 'oth'
    cat1 = select(Categories.id).where(Categories.name == cat)
    cat = session.execute(cat1).first()

    news = News(title=info_element['article_title'],
                URL=info_element['article_url'],
                category_id=cat1,
                score=info_element['score']
                # content = info_element['text'],
                # summary = info_element['text']
                )

    session.add(news)
session.commit()
