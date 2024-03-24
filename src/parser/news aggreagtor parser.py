# !pip -qq install selenium_driverless
from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
import requests
import re
# !pip -qq install newspaper3k
from newspaper import Article, ArticleException
import json

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

driver.get("https://www.newsnow.co.uk/h/Business+&+Finance?type=ln", timeout=120)

content_news = driver.find_elements(By.CLASS_NAME, "article-card__headline")
content_title = driver.find_elements(By.CLASS_NAME, "article-title latest-title list-layout")
content_time = driver.find_elements(By.CLASS_NAME, "article-publisher__timestamp")
content_publisher = driver.find_elements(By.CLASS_NAME, "article-publisher__name u-right-spacer-xs")

list_news = []
for i in range(min([len(content_news), len(content_title), len(content_time), len(content_publisher)])):
    print(content_news[i].get_attribute("href"))
    page_source_url = requests.get(content_news[i].get_attribute("href")).text
    news_url = re.findall(r"url: '(.*)',", page_source_url)[0]
    print("Title:", content_news[i].text.strip())
    print("Time:", content_time[i].text.strip())
    print("Publisher:", content_publisher[i].text.strip())
    print(news_url)
    list_news.append({"url": news_url, "title": content_title[i].text.strip(), "time": content_time[i].text.strip(), "publisher": content_publisher[i].text.strip()})

# driver.refresh()
driver.close()

list_json = []
for info_news in list_news:
    article = Article(url=info_news["url"])
    article.download()
    try:
        article.parse()
    except ArticleException:
        continue
    article_title = article.title
    article_text = article.text
    article.nlp()
    article_summary = article.summary
    article_keywords = article.keywords
    dict_news = {"article_url": info_news["url"], "article_title": info_news["title"], "article_title_generate": article_title, "article_publisher": info_news['publisher'], "article_text": article_text, "article_summary": article_summary, "article_keywords": article_keywords}
    list_json.append(dict_news)

with open('news aggregator parser.json', 'w', encoding='utf-8') as file:
    json.dump(list_json, file, indent=3)