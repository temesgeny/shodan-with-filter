from urllib import urlencode

from connect import *

def search(sess, text):
    sess.mount('https://www.shodan.io', HTTP20Adapter())
    url = "https://www.shodan.io/search?" + urlencode({"query" : text})
    headers = {}
    headers[":authority"] = "www.shodan.io"
    headers[":method"] = "GET"
    headers[":path"] = "/search?" + urlencode({"query" : text})
    headers[":scheme"] = "https"
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    headers["accept-encoding"] = "gzip, deflate, br"
    headers["accept-language"] = "en-US,en;q=0.9"
    # headers["cache-control"] = "max-age=0"
    # headers["content-type"] = "application/x-www-form-urlencoded"
    headers["origin"] = "https://www.shodan.io/"
    headers["referer"] = "https://www.shodan.io/"
    headers["upgrade-insecure-requests"] = "1"
    headers["user-agent"] = user_agent

    response = sess.get(url, headers = headers)
    hosts = text_parser.get_search_results(response.text)
    response = sess.get("https://www.shodan.io/search?" + urlencode({"query" : text, "page" : 1}), headers = headers)
    hosts_found = text_parser.get_search_results(response.text)
    hosts.extend(hosts_found)
    print hosts

def search_map(sess, text):
    # sess.mount('https://www.shodan.io', HTTP20Adapter())
    headers = {}
    response = sess.get("https://maps.shodan.io/_search?" + urlencode({"q" : text}), headers = headers)
    hosts_found = text_parser.parse_map(response.text)
    print hosts_found


if __name__ == '__main__':
    sess = connect()
    while True:
        text = raw_input(">> ")
        if text == "q" or text == "quit":
            print "Exiting..."
            sys.exit(1)
        search_map(sess, text)

