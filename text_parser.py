import bs4, search


def get_csrf_token(text):
    soup = bs4.BeautifulSoup(text, "lxml")
    item = soup.findAll("input", {"type": "hidden", "name": "csrf_token"})
    if len(item) > 0:
        return item[0]['value']
    return None


def get_search_results(text):
    hosts = []
    soup = bs4.BeautifulSoup(text, "lxml")
    search_results = soup.findAll("div", {"class": "search-result"})
    for search_result in search_results:
        ip = search_result.findAll("a", {"class" : "details"})[0]['href'][6:]
        if ip not in hosts:
            hosts.append(search.Host(ip))

    return hosts