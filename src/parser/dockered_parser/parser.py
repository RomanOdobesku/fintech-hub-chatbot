import asyncio
import os
import time

# import requests
from bs4 import BeautifulSoup
# from pandas import Timestamp

# import advertools as adv
import pandas as pd
from pandas import Timestamp

import advtools_enhanced as adv
import database
# import func_timeout
import aiohttp


# data = requests.get('https://example.com').text
# data_parsed = BeautifulSoup(data, features='lxml').text.lower()
# re.sub('[ .,!/:]', ' ', data_parsed)
# data_parsed = data_parsed.split()
# print(data_parsed)
# print(str(os.path.dirname(__file__)))
#
# # model = Word2Vec.load(str(os.path.dirname(__file__))+'\\GoogleNews-vectors-negative300.bin')
# goog_wordvecs = KeyedVectors.load_word2vec_format(
#     str(os.path.dirname(__file__)) + '\\GoogleNews-vectors-negative300.bin', binary=True, limit=100000)
# model = Word2Vec()
# model.wv = goog_wordvecs


# vector_repr = 0
# cnt = 0
# for i in data_parsed:
#     try:
#         vector_repr += model.wv[i]
#         cnt += 1
#     except:
#         pass
# vector_repr /= cnt

#
# def vec_from_text(text):
#     vector_repr = 0
#     cnt = 0
#     for i in text:
#         try:
#             if len(i) >= 5:
#                 vector_repr += model.wv[i]
#                 cnt += 1
#         except:
#             pass
#     vector_repr /= cnt
#     # print(vector_repr)
#     return vector_repr


# def vec_similarity(vec1, vec2):
#     sum = 0
#     size1 = 0
#     size2 = 0
#     if (len(vec1) != len(vec2)):
#         return -1
#     for i in range(len(vec2)):
#         sum += vec1[i] * vec2[i]
#         size1 += vec1[i] * vec1[i]
#         size2 += vec2[i] * vec2[i]
#     return sum / size1 / size2


# print(all_sitemaps)
def parser(from_time, all_sitemaps, timeout=None):
    # all_sitemaps = distill_aggregators.links
    # for i in newslinks.links:
    #     if (i[4] != None):
    #         for j in i[4]:
    #             for k in j.split():
    #                 if (k.__contains__('http')):
    #                     all_sitemaps.append(k)
    datas = []
    for i in range(0, len(all_sitemaps), 1):
        try:
            # mdf = func_timeout.func_timeout(100, adv.sitemap_to_df,
            #                                 args=(all_sitemaps[i], 8, True, timeout))
            mdf = adv.sitemap_to_df(all_sitemaps[i], timeout=timeout)
            # mdf = adv.sitemap_to_df(all_sitemaps[i], timeout=timeout)

            # mdf = mdf.sort_values(by=['lastmod'], ascending=True).head()
            # print(type(mdf['lastmod'].head().tolist()[0]))
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


# parsed_links = [[Timestamp('2024-03-29 20:58:22+0000', tz='UTC'), 'https://www.rbc.ru/rbcfreenews/6607254f9a7947eaa0215ee9'], [Timestamp('2024-03-29 21:01:19+0000', tz='UTC'), 'https://www.rbc.ru/politics/29/03/2024/660712e99a79478182d36b11'], [Timestamp('2024-03-29 21:17:22+0000', tz='UTC'), 'https://www.rbc.ru/rbcfreenews/6606c6059a7947036e3727d0'], [Timestamp('2024-03-29 20:57:21+0000', tz='UTC'), 'https://www.rbc.ru/rbcfreenews/6607132a9a7947f8baae159e'], [Timestamp('2024-03-29 21:00:23+0000', tz='UTC'), 'https://www.rbc.ru/finances/30/03/2024/6606e9869a794767190382ad'], [Timestamp('2024-03-29 21:09:33+0000', tz='UTC'), 'https://www.rbc.ru/politics/30/03/2024/660728c29a7947ad35196428'], [Timestamp('2024-03-29 21:17:28+0000', tz='UTC'), 'https://www.rbc.ru/politics/30/03/2024/660728609a7947e0e0ef5fc0'], [Timestamp('2024-03-29 21:00:23+0000', tz='UTC'), 'https://www.rbc.ru/story/5422bb83cbb20f63f25fb481'], [Timestamp('2024-03-29 21:24:02+0000', tz='UTC'), 'https://www.rbc.ru/story/65fdc2679a794730284d89d6'], [Timestamp('2024-03-29 21:17:28+0000', tz='UTC'), 'https://www.rbc.ru/story/61ee7c0f9a7947051824f535'], [Timestamp('2024-03-29 21:20:11+0000', tz='UTC'), 'https://www.whitehouse.gov/briefing-room/'], [Timestamp('2024-03-29 21:20:11+0000', tz='UTC'), 'https://www.whitehouse.gov/briefing-room/speeches-remarks/2024/03/29/remarks-by-president-biden-at-a-campaign-event-new-york-ny/'], [Timestamp('2024-03-29 21:09:38+0000', tz='UTC'), 'https://www.whitehouse.gov/oncd/briefing-room/'], [Timestamp('2024-03-29 21:09:38+0000', tz='UTC'), 'https://www.whitehouse.gov/oncd/briefing-room/2024/03/28/readout-tampa-cyber-florida/'], [Timestamp('2024-03-29 21:20:11+0000', tz='UTC'), 'https://www.whitehouse.gov/briefing-room/speeches-remarks/'], [Timestamp('2024-03-29 21:09:38+0000', tz='UTC'), 'https://www.whitehouse.gov/oncd/briefing-room/press-release/']]
# parsed_links = parser(from_time=time.time() - 60 * 10)
# print(
#     parsed_links)  # format [, [Timestamp('2024-03-29 21:09:38+0000', tz='UTC'), 'https://www.whitehouse.gov/oncd/briefing-room/press-release/']]

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
    # loop.close()
    return answers


def parse(source_links, delta_time, csv_filename, timeout):
    parsed_links = parser(from_time=time.time() - delta_time, all_sitemaps=source_links, timeout=timeout)
    # parsed_links = [[Timestamp('2024-03-29 20:58:22+0000', tz='UTC'), 'https://www.rbc.ru/rbcfreenews/6607254f9a7947eaa0215ee9'], [Timestamp('2024-03-29 21:01:19+0000', tz='UTC'), 'https://www.rbc.ru/politics/29/03/2024/660712e99a79478182d36b11'], [Timestamp('2024-03-29 21:17:22+0000', tz='UTC'), 'https://www.rbc.ru/rbcfreenews/6606c6059a7947036e3727d0'], [Timestamp('2024-03-29 20:57:21+0000', tz='UTC'), 'https://www.rbc.ru/rbcfreenews/6607132a9a7947f8baae159e'], [Timestamp('2024-03-29 21:00:23+0000', tz='UTC'), 'https://www.rbc.ru/finances/30/03/2024/6606e9869a794767190382ad'], [Timestamp('2024-03-29 21:09:33+0000', tz='UTC'), 'https://www.rbc.ru/politics/30/03/2024/660728c29a7947ad35196428'], [Timestamp('2024-03-29 21:17:28+0000', tz='UTC'), 'https://www.rbc.ru/politics/30/03/2024/660728609a7947e0e0ef5fc0'], [Timestamp('2024-03-29 21:00:23+0000', tz='UTC'), 'https://www.rbc.ru/story/5422bb83cbb20f63f25fb481'], [Timestamp('2024-03-29 21:24:02+0000', tz='UTC'), 'https://www.rbc.ru/story/65fdc2679a794730284d89d6'], [Timestamp('2024-03-29 21:17:28+0000', tz='UTC'), 'https://www.rbc.ru/story/61ee7c0f9a7947051824f535'], [Timestamp('2024-03-29 21:20:11+0000', tz='UTC'), 'https://www.whitehouse.gov/briefing-room/'], [Timestamp('2024-03-29 21:20:11+0000', tz='UTC'), 'https://www.whitehouse.gov/briefing-room/speeches-remarks/2024/03/29/remarks-by-president-biden-at-a-campaign-event-new-york-ny/'], [Timestamp('2024-03-29 21:09:38+0000', tz='UTC'), 'https://www.whitehouse.gov/oncd/briefing-room/'], [Timestamp('2024-03-29 21:09:38+0000', tz='UTC'), 'https://www.whitehouse.gov/oncd/briefing-room/2024/03/28/readout-tampa-cyber-florida/'], [Timestamp('2024-03-29 21:20:11+0000', tz='UTC'), 'https://www.whitehouse.gov/briefing-room/speeches-remarks/'], [Timestamp('2024-03-29 21:09:38+0000', tz='UTC'), 'https://www.whitehouse.gov/oncd/briefing-room/press-release/']]
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

# print(type(fsave['lastmod'].head().tolist()[0]))
# print(type(pd.to_datetime(np.datetime64(int(time.time()), 's'), utc=True)))
