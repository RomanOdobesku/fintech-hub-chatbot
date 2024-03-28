import time

from newspaper import Article
import requests
import grequests


class NoArchivePageError(Exception):
    def __init__(self, url: str) -> None:
        self.msg = f'No archive article found for {url}'
        super().__init__(self.msg)


class BadResponseException(Exception):
    def __init__(self, response) -> None:
        self.msg = f'Bad response {response.status_code} from {response.url}'
        super().__init__(self.msg)


def good_response(response: requests.Response):
    return response is not None and response.status_code == 200


def get_response_text(url: str) -> str:
    response = requests.get(url)
    if good_response(response):
        return response.text
    raise BadResponseException(response)


def retrieve_from_webarchive(url: str) -> str:
    response = requests.get('http://archive.org/wayback/available?url=' + url)
    if not good_response(response):
        raise BadResponseException(response)

    jsonobj = response.json()
    try:
        if jsonobj['archived_snapshots']['closest']['available']:
            return jsonobj['archived_snapshots']['closest']['url']
        raise NoArchivePageError(url)
    except KeyError:
        raise NoArchivePageError(url)


def parse_content(url: str) -> str:
    response_text = get_response_text(url)
    if len(response_text.strip()) == 0:
        return ''
    return get_article_content(url, response_text)


def get_article_content(url, response_text):
    article = Article(url)
    article.download(input_html=response_text)
    article.parse()
    return article.text


def parse_with_webarchive(url: str) -> str:
    sleep_time = 1
    time.sleep(sleep_time)

    try:
        url = retrieve_from_webarchive(url)
        return parse_content(url)
    except NoArchivePageError:
        try:
            return parse_content(url)
        except Exception as e:
            print(f'Could not retrieve a web page from {url}')
            print(e)


def many_slow(links, retrival_mode='source'):
    """
    Uses single thread and requests library, rarely faces 403
    :param retrival_mode: ['archive', 'source']
    :param links: list of Urls for requests
    :return: list of page's contents
    """
    if retrival_mode == 'source':
        return [parse_content(link) for link in links]
    return [parse_with_webarchive(link) for link in links]


def many_fast(links, nan_policy='ignore', verbose=True, **kwargs):
    """
    Uses multiple threads, often faces 403 forbidden
    :NOTE: You should import grequests before using this function, due monkey patching
    :param nan_policy: ['ignore', 'retry']
    :param links: list of Urls for requests
    :param verbose: True if you want to see output
    :return: list of page's contents
    """
    reqs = [grequests.get(link) for link in links]
    responses = grequests.map(reqs, **kwargs)
    if verbose:
        print(responses)

    if nan_policy == 'retry':
        for i in range(len(responses)):
            if responses[i] is None or responses[i].status_code == 403:
                try:
                    time.sleep(1)
                    responses[i] = requests.get(retrieve_from_webarchive(links[i]))
                except NoArchivePageError:
                    responses[i] = requests.get(links[i])
                except BadResponseException as e:
                    if verbose:
                        print(e.msg)

    return [get_article_content(link, response.text) if good_response(response) else '' for link, response in
            zip(links, responses)]
