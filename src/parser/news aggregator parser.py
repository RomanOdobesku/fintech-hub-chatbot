import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from newspaper import Article, ArticleException
import json
from typing import List, Dict

def news_aggregator_parser() -> List[Dict[str, str]]:
    """
        Функция для парсинга новостного агрегатора и сохранения результатов в JSON файл.

        Этапы работы:
        1. Получение HTML-страницы с новостями.
        2. Извлечение основной информации о новостях (ссылка, заголовок, издатель, время...).
        3. Получение URL-адреса каждой новости.
        4. Парсинг каждой новости с помощью библиотеки newspaper3k.
        5. Формирование словаря с подробной информацией о каждой новости.
        6. Сохранение результатов в JSON файл.

        :return: Список словарей с информацией о новостях.
    """

    # URL-адрес новостного агрегатора
    url = "https://www.newsnow.co.uk/h/Business+&+Finance?type=ln"

    # Отправляем GET-запрос на URL-адрес новостного агрегатора с таймаутом 120 секунд
    response = requests.get(url, timeout=120)

    # Создаем объект BeautifulSoup для парсинга HTML-содержимого страницы
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим все элементы div с классом 'hl__inner', содержащие новости
    html_news = soup.find_all("div", class_='hl__inner')

    # Создаем список для хранения основной информации о новостях на сайте агрегатора
    content_news = []

    # Извлекаем основную информацию о каждой новости с сайта агрегатора
    for news in html_news:
        try:
            # Извлекаем ссылку на новость с сайта первоисточника
            news_href = news.find("a")["href"]

            # Извлекаем заголовок новости
            news_title = news.find("a").text.strip()

            # Извлекаем издателя новости
            news_publisher = news.find("span", class_='src src-part').text.strip()

            # Извлекаем время публикации новости в формате timestamp
            news_time = news.find("span", class_='time')["data-time"]

            # Преобразуем timestamp в строковый формат даты и времени
            news_time_str = datetime.utcfromtimestamp(int(news_time)).strftime('%Y-%m-%d %H:%M:%S')

            # Добавляем информацию о новости в список content_news
            content_news.append({"href": news_href, "title": news_title, "publisher": news_publisher, "time": news_time,
                                 "time_str": news_time_str})
        except:
            continue

    # Создаем список для хранения основной информации о новостях
    list_news = []

    # Извлекаем основной информации о каждой новости с сайта первоисточника
    for news in content_news:
        # Получаем исходный код страницы новости с сайта первоисточника
        page_source_url = requests.get(news["href"]).text

        # Извлекаем URL новости с помощью регулярного выражения
        news_url = re.findall(r"url: '(.*)',", page_source_url)[0]

        # Добавляем информацию о новости в список list_news
        list_news.append(
            {"url": news_url, "title": news["title"], "publisher": news["publisher"], "time": news["time"],
             "time_str": news["time_str"]})

    # Создаем список для хранения основной и дополнительной информации о новостях
    list_json = []

    # Парсим каждую новость с помощью библиотеки newspaper3k
    for news in list_news:
        # Создаем объект Article из библиотеки newspaper для извлечения данных из статьи
        article = Article(url=news["url"])

        # Загружаем содержимое статьи
        article.download()

        try:
            # Парсим содержимое статьи
            article.parse()
        except ArticleException:
            continue

        # Извлекаем заголовок статьи
        article_title = article.title

        # Извлекаем текст статьи
        article_text = article.text

        # Применяем обработку естественного языка (NLP) к статье
        article.nlp()

        # Извлекаем краткое содержание статьи
        article_summary = article.summary

        # Извлекаем ключевые слова статьи
        article_keywords = article.keywords

        # Создаем словарь с информацией о статье
        dict_news = {"article_url": news["url"], "article_title": news["title"],
                     "article_title_generate": article_title, "article_publisher": news['publisher'],
                     "article_time": news["time"], "article_time_str": news["time_str"], "article_text": article_text,
                     "article_summary": article_summary, "article_keywords": article_keywords}

        # Добавляем информацию о новости в список list_json
        list_json.append(dict_news)

    # Сохраняем результаты в JSON файл
    with open('news aggregator parser.json', 'w', encoding='utf-8') as file:
        json.dump(list_json, file, indent=3)

    # Вовзращаем список словарей с информацией о новостях.
    return list_json

if __name__ == '__main__':
    print(news_aggregator_parser())