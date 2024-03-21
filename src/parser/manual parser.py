# !pip -qq install newspaper3k

import requests
from datetime import datetime, timedelta
from newspaper import Article, ArticleException

def parsing_www_rba_gov_au(check_years: int, date_news: datetime = datetime.now()) -> list:
    list_news = []
    for y in range(check_years):
        year_news = str(date_news.year-y)
        for num_news in range(1, 51):
            if num_news < 10:
                article_url = f"https://www.rba.gov.au/media-releases/{year_news}/mr-{year_news[2:]}-0{num_news}.html"
            else:
                article_url = f"https://www.rba.gov.au/media-releases/{year_news}/mr-{year_news[2:]}-{num_news}.html"
            req = requests.get(article_url)
            article = Article(url=article_url)
            article.download()
            try:
                article.parse()
            except ArticleException:
                print(f"status_code 404: {article_url}")
                break
            article_title = article.title
            article_text = article.text
            if article_text == "":
                print(f"no text: {article_url}")
                continue
            print()
            print(f"status_code 200: {article_url}")
            print()
            article.nlp()
            article_summary = article.summary
            list_news.append({"article_title": article_url, "article_title": article_title, "article_text": article_text, "article_summary": article_summary})
    return list_news

def parsing_www_oenb_at(check_days: int, date_news: datetime = datetime.now()) -> list:
    list_news = []
    for d in range(check_days):
        date_news_str = str(date_news.date() - timedelta(days=d))
        year_news = date_news_str[0:4]
        month_news = date_news_str[5:7]
        day_news = date_news_str[8:10]
        article_url = f"https://www.oenb.at/en/Media/Press-Archives/{year_news}/{year_news}{month_news}{day_news}.html"
        req = requests.get(article_url)
        article = Article(url=article_url)
        article.download()
        try:
            article.parse()
        except ArticleException:
            print(f"status_code 404: {article_url}")
            continue
        article_title = article.title
        article_text = article.text
        if article_text == "":
            print(f"no text: {article_url}")
            continue
        print()
        print(f"status_code 200: {article_url}")
        print()
        article.nlp()
        article_summary = article.summary
        list_news.append({"article_title": article_url, "article_title": article_title, "article_text": article_text, "article_summary": article_summary})
    return list_news

def parsing_www_bcb_gov_br(check_nums: int) -> list:
    list_news = []
    for n in range(check_nums):
        num_news = 2550 - n
        article_url = f"https://www.bcb.gov.br/en/pressdetail/{num_news}/nota"
        req = requests.get(article_url)
        article = Article(url=article_url)
        article.download()
        try:
            article.parse()
        except ArticleException:
            print(f"status_code 404: {article_url}")
            continue
        article_title = article.title
        article_text = article.text
        if article_text == "":
            print(f"no text: {article_url}")
            continue
        print()
        print(f"status_code 200: {article_url}")
        print()
        article.nlp()
        article_summary = article.summary
        list_news.append({"article_title": article_url, "article_title": article_title, "article_text": article_text, "article_summary": article_summary})
    return list_news

def parsing_www_hkma_gov_hk(check_days: int, date_news: datetime = datetime.now()) -> list:
    list_news = []
    for d in range(check_days):
        date_news_str = str(date_news.date() - timedelta(days=d))
        year_news = date_news_str[0:4]
        month_news = date_news_str[5:7]
        day_news = date_news_str[8:10]
        for num_news in range(1, 21):
            article_url = f"https://www.hkma.gov.hk/eng/news-and-media/press-releases/{year_news}/{month_news}/{year_news}{month_news}{day_news}-{num_news}/"
            req = requests.get(article_url)
            article = Article(url=article_url)
            article.download()
            try:
                article.parse()
            except ArticleException:
                print(f"status_code 404: {article_url}")
                continue
            article_title = article.title
            article_text = article.text
            if article_text == "":
                print(f"no text: {article_url}")
                continue
            print()
            print(f"status_code 200: {article_url}")
            print()
            article.nlp()
            article_summary = article.summary
            list_news.append({"article_title": article_url, "article_title": article_title, "article_text": article_text, "article_summary": article_summary})
    return list_news

def manual_parsing() -> list:
    list_news = []
    list_news.extend(parsing_www_rba_gov_au(check_years=2))
    list_news.extend(parsing_www_oenb_at(check_days=200))
    list_news.extend(parsing_www_bcb_gov_br(check_nums=100))
    list_news.extend(parsing_www_hkma_gov_hk(check_days=100))
    return list_news

# list_news = manual_parsing()