import bs4, search, json

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

def parse_map(text):
    hosts = []
    try:
        data = json.loads(text)
        matches = data['matches']
        total = data['total']
        print "%d results found!" % total

        for match in matches:
            host = search.Host(match['ip_str'])
            host.add_port(match['port'])
            hosts.append(host)
    except:
        pass

    return hosts