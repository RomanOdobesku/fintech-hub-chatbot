import requests
from datetime import datetime, timedelta
from newspaper import Article, ArticleException
import json
from typing import List, Dict
from logger import LOGGER

def parsing_www_rba_gov_au(check_years: int = 2, date_news: datetime = datetime.now(), check_news_numbers: int = 50) -> List[Dict[str, str]]:
    """
        Парсинг новостей с сайта www.rba.gov.au.

        :param check_years: Количество лет для проверки новостей (по умолчанию 2).
        :param date_news: Дата, с которой начинается проверка новостей (по умолчанию текущая дата).
        :param check_news_numbers: Количество новостей для проверки в каждом году (по умолчанию 50).
        :return: Список словарей с информацией о новостях.
    """
    list_news = []
    for y in range(check_years):
        year_news = str(date_news.year-y)
        for news_num in range(1, check_news_numbers+1):
            # Формирование URL новости
            if news_num < 10:
                article_url = f"https://www.rba.gov.au/media-releases/{year_news}/mr-{year_news[2:]}-0{news_num}.html"
            else:
                article_url = f"https://www.rba.gov.au/media-releases/{year_news}/mr-{year_news[2:]}-{news_num}.html"

            # Запрос и парсинг новости
            req = requests.get(article_url)
            article = Article(url=article_url)
            article.download()
            try:
                article.parse()
            except ArticleException as e:
                LOGGER.warning(f"status_code 404: {article_url}")
                LOGGER.error(str(e))
                break

            # Извлечение данных новости
            article_title = article.title
            article_text = article.text
            if article_text == "":
                LOGGER.warning(f"no text: {article_url}")
                continue
            LOGGER.info(f"status_code 200: {article_url}")
            article.nlp()
            article_summary = article.summary
            article_keywords = article.keywords

            # Добавление новости в список
            list_news.append({"article_url": article_url, "article_title": article_title,
                              "article_text": article_text, "article_summary": article_summary,
                              "article_keywords": article_keywords})

    return list_news

def parsing_www_oenb_at(check_days: int = 90, date_news: datetime = datetime.now()) -> List[Dict[str, str]]:
    """
        Парсинг новостей с сайта www.oenb.at.

        :param check_days: Количество дней для проверки новостей (по умолчанию 90).
        :param date_news: Дата, с которой начинается проверка новостей (по умолчанию текущая дата).
        :return: Список словарей с информацией о новостях.
    """
    list_news = []
    for d in range(check_days):
        date_news_str = str(date_news.date() - timedelta(days=d))
        year_news = date_news_str[0:4]
        month_news = date_news_str[5:7]
        day_news = date_news_str[8:10]

        # Формирование URL новости
        article_url = f"https://www.oenb.at/en/Media/Press-Archives/{year_news}/{year_news}{month_news}{day_news}.html"

        # Запрос и парсинг новости
        req = requests.get(article_url)
        article = Article(url=article_url)
        article.download()
        try:
            article.parse()
        except ArticleException as e:
            LOGGER.warning(f"status_code 404: {article_url}")
            LOGGER.error(str(e))
            continue

        # Извлечение данных новости
        article_title = article.title
        article_text = article.text
        if article_text == "":
            LOGGER.warning(f"no text: {article_url}")
            continue
        LOGGER.info(f"status_code 200: {article_url}")
        article.nlp()
        article_summary = article.summary
        article_keywords = article.keywords

        # Добавление новости в список
        list_news.append({"article_url": article_url, "article_title": article_title,
                          "article_text": article_text, "article_summary": article_summary,
                          "article_keywords": article_keywords})

    return list_news

def parsing_www_bcb_gov_br(check_nums: int = 90, check_numbers: int = 2500) -> List[Dict[str, str]]:
    """
        Парсинг новостей с сайта www.bcb.gov.br.

        :param check_nums: Количество номеров новостей для проверки (по умолчанию 90).
        :param check_numbers: Начальный номер новости для проверки (по умолчанию 2500).
        :return: Список словарей с информацией о новостях.
    """
    list_news = []
    for n in range(check_nums):
        num_news = check_numbers + n

        # Формирование URL новости
        article_url = f"https://www.bcb.gov.br/en/pressdetail/{num_news}/nota"

        # Запрос и парсинг новости
        req = requests.get(article_url)
        article = Article(url=article_url)
        article.download()
        try:
            article.parse()
        except ArticleException as e:
            LOGGER.warning(f"status_code 404: {article_url}")
            LOGGER.error(str(e))
            break

        # Извлечение данных новости
        article_title = article.title
        article_text = article.text
        if article_text == "":
            LOGGER.warning(f"no text: {article_url}")
            continue
        LOGGER.info(f"status_code 200: {article_url}")
        article.nlp()
        article_summary = article.summary
        article_keywords = article.keywords

        # Добавление новости в список
        list_news.append({"article_url": article_url, "article_title": article_title,
                          "article_text": article_text, "article_summary": article_summary,
                          "article_keywords": article_keywords})

    return list_news

def parsing_www_hkma_gov_hk(check_days: int = 7, date_news: datetime = datetime.now()) -> List[Dict[str, str]]:
    """
        Парсинг новостей с сайта www.hkma.gov.hk.

        :param check_days: Количество дней для проверки новостей (по умолчанию 7).
        :param date_news: Дата, с которой начинается проверка новостей (по умолчанию текущая дата).
        :return: Список словарей с информацией о новостях.
    """
    list_news = []
    for d in range(check_days):
        date_news_str = str(date_news.date() - timedelta(days=d))
        year_news = date_news_str[0:4]
        month_news = date_news_str[5:7]
        day_news = date_news_str[8:10]
        for num_news in range(1, 21):
            # Формирование URL новости
            article_url = f"https://www.hkma.gov.hk/eng/news-and-media/press-releases/{year_news}/{month_news}/{year_news}{month_news}{day_news}-{num_news}/"

            # Запрос и парсинг новости
            req = requests.get(article_url)
            article = Article(url=article_url)
            article.download()
            try:
                article.parse()
            except ArticleException as e:
                LOGGER.warning(f"status_code 404: {article_url}")
                LOGGER.error(str(e))
                continue

            # Извлечение данных новости
            article_title = article.title
            article_text = article.text
            if article_text == "":
                LOGGER.warning(f"no text: {article_url}")
                continue
            LOGGER.info(f"status_code 200: {article_url}")
            article.nlp()
            article_summary = article.summary
            article_keywords = article.keywords

            # Добавление новости в список
            list_news.append({"article_url": article_url, "article_title": article_title,
                              "article_text": article_text, "article_summary": article_summary,
                              "article_keywords": article_keywords})

    return list_news

def various_sources_parsing(check_years_www_rba_gov_au: int = 2, check_days_www_oenb_at: int = 90, check_nums_www_bcb_gov_br: int = 90, check_days_www_hkma_gov_hk: int = 7) -> List[Dict[str, str]]:
    """
        Парсинг новостей из различных источников.

        :param check_years_www_rba_gov_au: Количество лет для проверки на сайте www.rba.gov.au (по умолчанию 2).
        :param check_days_www_oenb_at: Количество дней для проверки на сайте www.oenb.at (по умолчанию 90).
        :param check_nums_www_bcb_gov_br: Количество номеров для проверки на сайте www.bcb.gov.br (по умолчанию 90).
        :param check_days_www_hkma_gov_hk: Количество дней для проверки на сайте www.hkma.gov.hk (по умолчанию 7).
        :return: Список словарей с информацией о новостях из различных источников.
    """
    list_news = []

    # Парсинг новостей с сайта www.rba.gov.au
    list_news.extend(parsing_www_rba_gov_au(check_years=check_years_www_rba_gov_au))

    # Парсинг новостей с сайта www.oenb.at
    list_news.extend(parsing_www_oenb_at(check_days=check_days_www_oenb_at))

    # Парсинг новостей с сайта www.bcb.gov.br
    list_news.extend(parsing_www_bcb_gov_br(check_nums=check_nums_www_bcb_gov_br))

    # Парсинг новостей с сайта www.hkma.gov.hk
    list_news.extend(parsing_www_hkma_gov_hk(check_days=check_days_www_hkma_gov_hk))

    with open('various sources parser result.json', 'w', encoding='utf-8') as file:
        json.dump(list_news, file, indent=3)

    return list_news

if __name__ == '__main__':
    list_json = various_sources_parsing()
    print(list_json)
    print(len(list_json))