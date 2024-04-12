import json
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import News, Base, Categories

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


# строка движок и подключение к базе данных
# engine = create_engine(os.getenv('DB_POSTGRESQL'), echo=True)

connection_string = URL.create(
  'postgresql',
  username='olga',
  password='XGAs4trRJ0hW',
  host='ep-bold-mouse-a2jqmrzs.eu-central-1.aws.neon.tech',
  database='postgresql',
  query={'sslmode': 'require'}
)

engine = create_engine(connection_string, echo=True)


# создаем полученную базу данных и сохраняем ее (пока пустую)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


# подготовляем сессию для работы
session = sessionmaker(bind=engine)()

# заполнение таблицы categories известными категориями
category_list = {"cr": "Крипто",
                 "ai": "Искусственный интеллект",
                 "cbdc": "ЦВЦБ",
                 "oth": "Прочее",
                 "bid": "Биометрия и идентификация",
                 "tok": "Токенизация",
                 "defi": "Децентрализованные финансы",
                 "api": "Открытые API"}

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
        category = 'Прочее'

    # достаем id категории из бд
    id_category_from_db = select(Categories.id).where(Categories.name == category)

    # заполняем необходимые поля в нашей бд и закидываем в нее
    news = News(title=info_element['article_title'],
                url=info_element['article_url'],
                category_id=id_category_from_db,
                score=info_element['score']
                # content = info_element['text'],
                # summary = info_element['text']
                )

    session.add(news)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print('Новость с таким url уже внесена в базу данных. Пропускаем...')
