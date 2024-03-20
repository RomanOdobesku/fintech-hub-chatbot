# formats links like /en/user to base_url/en/user or returns '' if link is going outside base_url
def format(base_url: str, to_format: str) -> str:
    if to_format.__contains__('http') and not to_format.__contains__(base_url):
        return ''
    elif to_format.__contains__('http'):
        return to_format
    else:
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        if to_format[0] == '/':
            to_format = to_format[1:]
        return base_url + '/' + to_format


# links = get_all_data_recursive("https://www.boj.or.jp",'https://www.boj.or.jp/en/'), uses beautifulsoup4, requests
def get_all_data_recursive(base: str, url: str) -> set:
    import requests
    from bs4 import BeautifulSoup
    all_links = set()
    to_remove = set()
    queue = [url]
    all_links.add(url)
    while len(queue) != 0:
        fr = queue.pop(0)
        try:
            resp = requests.get(fr)
            parsed = BeautifulSoup(resp.content, 'html.parser')
            for link in parsed.find_all('a', href=True):
                if link.has_attr('href'):
                    formatted = format(base, link['href'])
                    if formatted == '':
                        continue
                    if not all_links.__contains__(formatted):
                        queue.append(formatted)
                        all_links.add(formatted)
        except:
            to_remove.add(fr)
    for i in to_remove:
        all_links.remove(i)
    return all_links


# uses requests
def scrape_link(url: str) -> str:
    import requests
    return requests.get(url).text


# newspaper3k
def get_data_from_html_newspaper(html: str) -> str:
    import newspaper
    parser = newspaper.Article("")
    parser.download(input_html=html)
    parser.parse()
    return parser.text


# beautifulsoup4
def get_data_from_html_bs4(html: str) -> str:
    from bs4 import BeautifulSoup
    prepared = BeautifulSoup(html, 'html.parser')
    return prepared.text
