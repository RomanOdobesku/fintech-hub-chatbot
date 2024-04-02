# Финтех Хаб Банка России. Бизнес-кейс "Новостной чат-бот"

## Авторы:
Одобеску Роман, Team Lead  
Антропова Ольга, Backend разработчик  
Герасимов Александр, Data Scientist  
Комаров Дмитрий, Backend разработчик  
Хусаинов Даниэль, Backend разработчик    

## Описание:

Наш новостной чат-бот представляет собой комплексное решение для сбора, анализа и доставки наиболее актуальных и важных новостей в сфере финтеха персонально каждому пользователю. 

Архитектура нашего сервиса обеспечивает полный цикл от сбора "сырых" новостей до доставки пользователям наиболее ценной для них информации в удобном формате через интерфейс чат-бота. Система максимально автоматизирована и способна обрабатывать большие потоки данных, выдавая на выходе сжатую и персонализированную информацию.

<img src="image.png" width="650" height="800">


## Функциональность:

* Парсинг новостей с ведущих новостных агрегаторов.
* Фильтрация важных и актуальных новостей.
* Классификация по темам и составление саммари с помощью моделей машинного обучения.
* Составление персонализированных дайджестов и их рассылка пользователям.

## Технологии:

* Python (3.9 и выше)
* База данных (sqlalchemy, PostgreSQL)
* Telegram Api (aiogram)
* Парсер (newspaper, BeautifulSoup)

## Используемые модели

* Модель для классификации новостей по нескольким тематикам: **distilbert-base-uncased**
* Модель для составления саммари по новостям: **Mistral-7B-Instruct-v0.2**
* Модель для фильтрации важных/неважных новостей: in development...


## Использование:

1. Начните чат с нашим Telegram-ботом, [перейдя по ссылке](https://t.me/fintech_news_chatbot).
2. Используйте команды для взаимодействия с ботом и получения новостей:
    * `/help` - вывод справочной информации
    * `/my_categories` - вывод списка выбранных тем для отслеживания
    * `/restart` - сброс списка выбранных тем и выбор новых
    * `/digest` - составление дайджеста актуальных на данный момент новостей по выбранным темам. 


