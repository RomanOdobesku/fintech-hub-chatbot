import requests
from requests import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ProxyError
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from newspaper import Article, ArticleException
import json
from typing import List, Dict
from logger import LOGGER
import time

def proxy_requests_aggregator_url(url: str, proxies: Dict[str, str]) -> List[Dict[str, str]]:
    # Отправляем GET-запрос на URL-адрес новостного агрегатора с таймаутом 120 секунд
    response = requests.get(url, proxies=proxies, timeout=120)

    # Создаем объект BeautifulSoup для парсинга HTML-содержимого страницы
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим все элементы div с классом 'hl__inner', содержащие новости
    html_news = soup.find_all("div", class_='hl__inner')

    # Создаем список для хранения основной информации о новостях на сайте агрегатора для одного раздела
    content_news_for_one_url = []

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
            content_news_for_one_url.append({"href": news_href, "title": news_title, "publisher": news_publisher, "time": news_time,
                                 "time_str": news_time_str})
        except:
            continue
    return content_news_for_one_url

def news_aggregator_parser(check_minutes: int = 60, start_proxy_index_list_url: int = 0, start_proxy_index_list_redirect: int = 0) -> List[Dict[str, str]]:
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

    # Загрузка переменных окружения из файла .env
    load_dotenv(os.path.join('proxy authentication.env'))

    PROXY_USER = os.getenv("PROXY_USER")
    PROXY_PASS = os.getenv("PROXY_PASS")

    proxy_list_url = [{"proxy_host": "38.154.227.167", "proxy_port": "5868"},
                      {"proxy_host": "185.199.229.156", "proxy_port": "7492"}]

    proxy_list_redirect = [{"proxy_host": "185.199.228.220", "proxy_port": "7300"},
                           {"proxy_host": "185.199.231.45", "proxy_port": "8382"},
                           {"proxy_host": "188.74.210.207", "proxy_port": "6286"},
                           {"proxy_host": "188.74.183.10", "proxy_port": "8279"},
                           {"proxy_host": "188.74.210.21", "proxy_port": "6100"},
                           {"proxy_host": "45.155.68.129", "proxy_port": "8133"},
                           {"proxy_host": "154.95.36.199", "proxy_port": "6893"},
                           {"proxy_host": "45.94.47.66", "proxy_port": "8110"}]

    # URL-адреса новостного агрегатора
    url_list = ["https://www.newsnow.co.uk/h/Business+&+Finance?type=ln",
                "https://www.newsnow.co.uk/h/Business+&+Finance/Cryptocurrencies?type=ln",
                "https://www.newsnow.co.uk/h/Business+&+Finance/Fintech?type=ln",
                "https://www.newsnow.co.uk/h/Industry+Sectors/IT/Computer+Technology/Cloud+Computing?type=ln",
                "https://www.newsnow.co.uk/h/Science/AI?type=ln",
                "https://www.newsnow.co.uk/h/Technology/Cutting+Edge/Biometrics?type=ln"]

    # Создаем список для хранения основной информации о новостях на сайте агрегатора для одного раздела
    content_news = []

    proxy_index = start_proxy_index_list_url
    for i in range(len(url_list)):
        while proxy_index < len(proxy_list_url):
            proxy_dict = proxy_list_url[proxy_index]
            PROXY_HOST = proxy_dict["proxy_host"]
            PROXY_PORT = proxy_dict["proxy_port"]

            # Настройки прокси
            proxies = {
                "http": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}",
                "https": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
            }
            try:
                content_news.extend(proxy_requests_aggregator_url(url=url_list[i], proxies=proxies))
            except ConnectTimeout as e:
                LOGGER.error(str(e))
                proxy_index += 1
                continue
            except ProxyError as e:
                LOGGER.error(str(e))
                proxy_index += 1
                continue
            time.sleep(0.5)
            break

        LOGGER.info(f"Обработано ссылок на разделы newsnow: {i+1}/{len(url_list)}")

    if proxy_index >= len(proxy_list_url):
        LOGGER.error("Все прокси использованы")
        raise Exception('Proxies are dead')

    LOGGER.info(f"len(content_news): {len(content_news)}")

    # with open('news aggregator parser content news.json', 'w', encoding='utf-8') as file:
    #     json.dump(content_news, file, indent=3)

    filtered_content_news = []
    for news in content_news:
        if datetime.now() - datetime.strptime(news["time_str"],
                                              "%Y-%m-%d %H:%M:%S") <= timedelta(minutes=check_minutes+180):
            filtered_content_news.append(news)

    LOGGER.info(f"len(filtered_content_news): {len(filtered_content_news)}")

    # with open('news aggregator parser filtered content news .json', 'w', encoding='utf-8') as file:
    #     json.dump(content_news, file, indent=3)

    # Создаем список для хранения основной информации о новостях
    list_news = []

    proxy_index = start_proxy_index_list_redirect
    number_proxy_error_consistently = 0
    # Извлекаем основной информации о каждой новости с сайта первоисточника
    for i in range(len(filtered_content_news)):
        while number_proxy_error_consistently == 0 \
                or number_proxy_error_consistently % len(proxy_list_redirect) != 0:

            if proxy_index >= len(proxy_list_redirect):
                proxy_index = 0

            proxy_dict = proxy_list_redirect[proxy_index]
            PROXY_HOST = proxy_dict["proxy_host"]
            PROXY_PORT = proxy_dict["proxy_port"]

            # Настройки прокси
            proxies = {
                "http": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}",
                "https": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
            }

            try:
                # Получаем исходный код страницы новости с сайта первоисточника
                page_source_url = requests.get(filtered_content_news[i]["href"], proxies=proxies, timeout=2).text
                # page_source_url = requests.get(news["href"], timeout=2).text
                time.sleep(0.5)

            except ReadTimeout as e:
                LOGGER.error(str(e))
                LOGGER.info(f"proxy index = {proxy_index}")
                proxy_index += 1
                number_proxy_error_consistently += 1
                LOGGER.info(f"number of proxy errors consistently = {number_proxy_error_consistently}")
                continue
            except ConnectTimeout as e:
                LOGGER.error(str(e))
                LOGGER.info(f"proxy index = {proxy_index}")
                proxy_index += 1
                number_proxy_error_consistently += 1
                LOGGER.info(f"number of proxy errors consistently = {number_proxy_error_consistently}")
                continue
            except ProxyError as e:
                LOGGER.error(str(e))
                LOGGER.info(f"proxy index = {proxy_index}")
                proxy_index += 1
                number_proxy_error_consistently += 1
                LOGGER.info(f"number of proxy errors consistently = {number_proxy_error_consistently}")
                continue

            # Извлекаем URL новости с помощью регулярного выражения
            news_url = re.findall(r"url: '(.*)',", page_source_url)[0]

            # Добавляем информацию о новости в список list_news
            list_news.append(
                {"url": news_url, "title": filtered_content_news[i]["title"], "publisher": filtered_content_news[i]["publisher"],
                 "time": filtered_content_news[i]["time"], "time_str": filtered_content_news[i]["time_str"]})

            number_proxy_error_consistently = 0
            break

        if number_proxy_error_consistently >= len(proxy_list_redirect)*10:
            LOGGER.error("Все прокси использованы")
            raise Exception('Proxies are dead')

        LOGGER.info(f"Обработано редиректных ссылок: {i+1}/{len(filtered_content_news)}")

    LOGGER.info(f"len(list_news): {len(list_news)}")

    # with open('news aggregator parser list news.json', 'w', encoding='utf-8') as file:
    #     json.dump(list_news, file, indent=3)

    # Создаем список для хранения основной и дополнительной информации о новостях
    list_json = []

    # Парсим каждую новость с помощью библиотеки newspaper3k
    for i in range(len(list_news)):
        # Создаем объект Article из библиотеки newspaper для извлечения данных из статьи
        article = Article(url=list_news[i]["url"])

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

        # # Применяем обработку естественного языка (NLP) к статье
        # article.nlp()
        #
        # # Извлекаем краткое содержание статьи
        # article_summary = article.summary
        #
        # # Извлекаем ключевые слова статьи
        # article_keywords = article.keywords

        # # Создаем словарь с информацией о статье
        # dict_news = {"article_url": news["url"], "article_title": news["title"],
        #              "article_title_generate": article_title, "article_publisher": news['publisher'],
        #              "article_time": news["time"], "article_time_str": news["time_str"], "article_text": article_text,
        #              "article_summary": article_summary, "article_keywords": article_keywords}

        # Создаем словарь с информацией о статье
        dict_news = {"article_url": list_news[i]["url"], "article_title": list_news[i]["title"],
                     "article_title_generate": article_title, "article_publisher": list_news[i]['publisher'],
                     "article_time": list_news[i]["time"], "article_time_str": list_news[i]["time_str"],
                     "article_text": article_text}

        # Добавляем информацию о новости в список list_json
        list_json.append(dict_news)

        LOGGER.info(f"Обработано прямых ссылок: {i+1}/{len(list_news)}")

    # Сохраняем результаты в JSON файл
    with open('news aggregator parser result.json', 'w', encoding='utf-8') as file:
        json.dump(list_json, file, indent=3)

    # Вовзращаем список словарей с информацией о новостях.
    return list_json

if __name__ == '__main__':
    list_json = news_aggregator_parser(check_minutes=30, start_proxy_index_list_url=0, start_proxy_index_list_redirect=0)
    print(list_json)
    print(len(list_json))