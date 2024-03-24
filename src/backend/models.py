from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import DeclarativeBase


# родительский класс для наследования остальных
class Base(DeclarativeBase):
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now)


# класс для новостей, ключ из класса категории, чтобы завести отношение
class News(Base):
    __tablename__ = "News"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(150))
    url = Column(String(200), nullable=False)
    content = Column(Text())
    summary = Column(Text())
    category_id = Column(Integer(), nullable=False)
    score = Column(Integer())


# класс для категории (нужен для нормальной архитектуры бд)
class Categories(Base):
    __tablename__ = "Categories"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(100))


# класс для пользователей бота
class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(100))
    chat = Column(String(100))


# класс для хранения выбранных категорий пользователями бота
class UserCategories(Base):
    __tablename__ = "User_categories"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer())
    category_id = Column(String(100))
