import asyncio
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
# from pandas import Timestamp
import advtools_enhanced as adv
import database
import aiohttp


def parser(from_time, all_sitemaps, timeout=None):
    datas = []
    for i in range(0, len(all_sitemaps), 1):
        try:
            mdf = adv.sitemap_to_df(all_sitemaps[i], timeout=timeout)
            mdf = mdf[mdf['lastmod'].apply(lambda x: x.value) > from_time * (10 ** 9)]
            mdf = mdf.loc[:, ['lastmod', 'loc']]
            print(mdf)
            print(mdf.values.tolist())
            if len(mdf.values.tolist()) > 100:
                raise Exception(f'Too many new news on site ${all_sitemaps[i]}: probably wrong timing on news')
            datas.extend(mdf.values.tolist())
        except Exception as e:
            print("error")
            print(e)
        except:
            print('error, but not exception')
    return datas


def parsing_domens_sitemaps(sites_texts, minlen=1000):
    parsed_sites = []
    for i in range(len(sites_texts)):
        size_list = []
        try:
            data = BeautifulSoup(sites_texts[i], features="lxml")
            title = ''
            for j in data.find_all('title'):
                title += j.get_text()
            size_list.append(title)
            data = ' '.join(data.text.split())
            if len(data) < minlen:
                size_list.append(None)
            else:
                size_list.append(data)
        except:
            size_list.append(None)
        parsed_sites.append(size_list)
    return parsed_sites


async def _link_parser(link: str, counter, timeout=None):
    async with aiohttp.ClientSession(conn_timeout=timeout) as session:
        try:
            async with session.get(link) as response:
                text = await response.text()
                counter[0] += 1
                print(counter)
                # print(text)
                return text
        except Exception as e:
            counter[0] += 1
            print(counter)
            print(e, link)
        except:
            counter[0] += 1
            print(counter)
            print(f'uncatched exception at ${link}')
        return None


def parse_links(links: list[str], timeout=None, timeout_between_requests: float = 0.2):
    tasks = []
    counter = [0, len(links)]
    for i in links:
        tasks.append(asyncio.ensure_future(_link_parser(i, counter, timeout)))
        time.sleep(timeout_between_requests)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
    answers = []
    for i in tasks:
        answers.append(i.result())
    return answers


def parse(source_links, delta_time, csv_filename, timeout):
    parsed_links = parser(from_time=time.time() - delta_time, all_sitemaps=source_links, timeout=timeout)
    print(parsed_links)
    my_links = []
    for i in parsed_links:
        my_links.append(i[1])
    parsed_sites = parse_links(my_links, timeout=timeout)
    cropped_sites = parsing_domens_sitemaps(parsed_sites)
    for i in range(len(cropped_sites)):
        # cropped_sites[i].append(parsed_links[i])
        cropped_sites[i].extend(parsed_links[i])
    df = pd.DataFrame(cropped_sites)
    df = df.rename(columns={'0': 'title', '1': 'content', '2': 'time', '3': 'url'})
    database.fill_database_from_parser(df)
    df.to_csv(str(os.path.dirname(__file__)) + '/' + csv_filename)


import sourceslinks

# database.create_tables()
if __name__ == '__main__':
    while True:
        parse(sourceslinks.links, 6 * 60 * 60, 'parsed_sources.csv', 100)
        time.sleep(6 * 60 * 60)
