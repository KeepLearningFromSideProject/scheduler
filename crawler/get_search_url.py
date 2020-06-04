#!/usr/bin/env python3

import requests
import urllib
import sys
import json

from bs4 import BeautifulSoup as Soup
from pprint import pprint

def doRequest(url):
    return requests.get(url, cookies={'RI': '0'})

def search(search_key):
    resp = doRequest(
            'https://comicbus.com/member/search.aspx?' + \
            urllib.parse.urlencode({"k": search_key}, encoding='big5'))

    page = Soup(resp.content.decode('big5'), features="html.parser")
    rows = page.find_all('td', style="border-bottom:1px dotted #cccccc; line-height:18px; padding-left:5px ")

    results = []
    for row in rows:
        results.extend(row.find_all('a', href=True))

    ret = {}
    for r in results:
        title = r.find('font').getText()
        ret[title] = r['href']

    pprint(ret)

    with open('search_of_' + search_key + '_urls.json', 'w') as dst:
        dst.write(json.dumps(ret, indent=4))

if __name__ == '__main__':
    search(sys.argv[1])
