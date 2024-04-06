import time
from datetime import datetime
from datetime import timezone
import feedparser
# import aiohttp
# import requests
# from requests import get

# from dockered_parser import database
import database
from parser import parse_links
import rss_list
import pandas as pd


# rss_url = "https://rss.art19.com/apology-line"
# response = get(rss_url)
#
# rss = RSSParser.parse(response.text)
# parsed_rss = parse_links(rss_list.links, 100)
# # print(parsed_rss)
# for i in range(len(parsed_rss)):
#     try:
#         rss = feedparser.parse(parsed_rss[i])
#         # print('ok', rss_list.links[i])
#     except Exception as e:
#         print('error', (' '.join(str(e).split()))[:100], rss_list.links[i])
#         pass
#     except:
#         print('very bad error', rss_list.links[i])
# for item in rss:
#     if item.pubDate
# import feedparser
#
# d = feedparser.parse("https://betanews.com/feed/")
# for item in d['entries']:
#     # print(item)
#     print(datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S %z"), item.title, item.description, item.link)


def _parse_rss(texts: list[str], target_time: datetime, max_news_per_source: int = 20):
    result = list()
    for text in texts:
        cnt = 0
        try:
            rss = feedparser.parse(text)
            for item in rss['entries']:
                time = None
                try:
                    time = datetime.strptime(item.published, "%a, %d %b %Y %H:%M:%S %z")
                except:
                    pass
                if (time is None and cnt < max_news_per_source) or time > target_time:
                    article = [time, item.title, item.description, item.link]
                    result.append(article)
                    cnt += 1
        except Exception as e:
            print('error')
            print((' '.join(str(e).split()))[:100])
        except:
            print('unhandled error')
    return result


# print(parse_rss([requests.get("https://betanews.com/feed/").text],
#                 datetime.fromtimestamp(time.time() - 60 * 60 * 24, tz=timezone.utc)))
# Print out rss meta data
# print("Language", rss.channel.language)
# print("RSS", rss.version)

# # Iteratively print feed items
# for item in rss.channel.items:
#     # print(item.title)
#     # print(item.description)
#     print(item)

def parser(target_time: float, max_news_per_source: int = 20, timeout: int = 100):
    links = parse_links(rss_list.links, timeout)
    news = _parse_rss(links, datetime.fromtimestamp(target_time, tz=timezone.utc), max_news_per_source)
    df = pd.DataFrame(news, columns=['time', 'title', 'content', 'url'])
    print(df)
    to_update = database.fill_database_from_parser(df)
    to_update = pd.DataFrame(to_update)
    database.update_news(to_update)

# database.create_tables()
while True:
    parser(time.time() - 30 * 60)
    time.sleep(30 * 60)
