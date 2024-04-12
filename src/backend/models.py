from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base


# родительский класс для наследования остальных
Base = declarative_base()


# класс для новостей, ключ из класса категории, чтобы завести отношение
class News(Base):
    __tablename__ = "News"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300))
    url = Column(String(300), nullable=False, unique=True)
    content = Column(Text())
    summary = Column(Text())
    category_id = Column(Integer())
    score = Column(Integer())
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now)


# класс для категории (нужен для нормальной архитектуры бд)
class Categories(Base):
    __tablename__ = "Categories"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(100))
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now)


# класс для пользователей бота
class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    chat = Column(String(100), unique=True)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now)


# класс для хранения выбранных категорий пользователями бота
class UserCategories(Base):
    __tablename__ = "User_categories"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(String(100))
    category_id = Column(Integer)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now)
