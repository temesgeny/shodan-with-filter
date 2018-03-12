import requests
import fake_useragent
import sys
from hyper.contrib import HTTP20Adapter
import argparse

import text_parser

import httplib

username = ""
password = ""
proxies = None
user_agent = ""

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--username", help="shodan username")
arg_parser.add_argument("--password", help="shodan password")
arg_parser.add_argument("--proxy", help="proxy server to connect to")
arg_parser.add_argument("--useragent", help="user agent to request as")

args = arg_parser.parse_args()
if args.username:
    username = args.username
if args.password:
    password = args.password
if args.proxy:
    proxies = {
        'http': args.proxy,
        'https': args.proxy,
    }
if args.useragent:
    user_agent = args.useragent
else:
    ua = fake_useragent.UserAgent()
    user_agent = ua.random

def patch_send():
    old_send= httplib.HTTPConnection.send
    def new_send( self, data ):
        data = data.replace("python-requests/2.10.0", user_agent)
        # print data
        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
    httplib.HTTPConnection.send= new_send

patch_send()

def connect():
    sess = requests.session()
    sess.proxies = proxies
    response = sess.get('https://account.shodan.io/login')
    csrf_token = text_parser.get_csrf_token(response.text)
    if not csrf_token:
        print "CSRF token could not be obtained"
        sys.exit(1)
    else:
        print csrf_token
    print user_agent
    sess.mount('https://account.shodan.io', HTTP20Adapter())
    headers = {}
    headers[":authority"] = "account.shodan.io"
    headers[":method"] = "POST"
    headers[":path"] = "/login"
    headers[":scheme"] = "https"
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    headers["accept-encoding"] = "gzip, deflate, br"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["cache-control"] = "max-age=0"
    headers["content-type"] = "application/x-www-form-urlencoded"
    headers["origin"] = "https://account.shodan.io"
    headers["referer"] = "https://account.shodan.io/login"
    headers["upgrade-insecure-requests"] = "1"
    headers["User-Agent"] = user_agent

    data = {}
    data["username"] = username
    data["password"] = password
    data["grant_type"] = "password"
    data["continue"] = "https://account.shodan.io/"
    data["csrf_token"] = csrf_token
    data["login_submit"] = "Log in"

    response = sess.post('https://account.shodan.io/login', headers=headers, data=data, allow_redirects=False)

    if response.status_code == 302:
        polito_header = response.headers['set-cookie']
        polito_header = polito_header.split(";")[0]
        print sess.cookies
        sess.cookies[polito_header.split("=")[0]] = polito_header.split("=")[1].replace('"', '')
        print "Shodan session created successfully"
    else:
        print "Shodan session could not be established"
        sys.exit(1)

    return sess