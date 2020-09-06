#!/usr/bin/env python3
"""
@author: FATESAIKOU
@date: 2020/06/12
@email: tsungfu.chiang@gmail.com
@argv[1]: comic name(str)
"""

import requests
import urllib
import execjs
import sys
import json
import re

from bs4 import BeautifulSoup as Soup
from pprint import pprint


def doRequest(url):
    return requests.get(url, cookies={'RI': '0'})

def searchComic(pattern):
    resp = doRequest(
            'https://comicbus.com/member/search.aspx?' + \
            urllib.parse.urlencode({"k": pattern}, encoding='big5'))

    page = Soup(resp.content.decode('big5'), features="html.parser")
    rows = page.find_all('td', style="border-bottom:1px dotted #cccccc; line-height:18px; padding-left:5px ")

    results = []
    for row in rows:
        results.extend(row.find_all('a', href=True))

    ret = {}
    for r in results:
        title = r.find('font').getText()
        if title == pattern:
            return 'https://comicbus.com' + r['href']

    return None

def searchEpisode(comic_url):
    resp = doRequest(comic_url)

    page = Soup(resp.content.decode('big5'), features="html.parser")
    rows = page.find_all('a', {"href": "#", "class": re.compile(r"Ch|Vol")})

    episodes = {}
    for row in rows:
        t = row.find('font')
        if t:
            title = t.getText().strip()
        else:
            title = row.getText().strip()
        episode_infos = \
                re.search('\'([\w|\d|-]*.html)\',(\d*),(\d*)', row['onclick']).groups()
        episodes[title] = 'https://comicbus.live/online/a-' + \
                episode_infos[0].replace('.html', '').replace('-', '.html?ch=')

    return episodes

def getImageInfo(episode_url, p=1):
    resp = doRequest(episode_url)
    resp_content = resp.content.decode('big5')
    
    ch = re.search("ch=(\d*)", episode_url)[1]
    ti = re.search("(\d*).html", episode_url)[1]
    chs = re.search("var chs=(\d*)", resp_content)[1]
    cs = re.search("var cs='(\w*)'", resp_content)[1]
    main_loop = re.search("for.*}}", resp_content)[0]
    
    with open('get_imgurl.js', 'r') as src:
        context = execjs.compile(
                "var y=46;" +
                "var ch={};".format(ch) +
                "var ti={};".format(ti) +
                "var chs='{}';".format(chs) +
                "var cs='{}';".format(cs) +
                "var p={};".format(p) + 
                "var result={};" +
                "function ge(e) {return result;};" +
                src.read() +
                "function getImgInfo() {" +
                main_loop +
                "return [result.src, ps];}"
        )

    return context.call('getImgInfo')

def getPictureUrls(episode_url, page_num):
    page_urls = []
    for i in range(1, page_num + 1):
        page_url = "https:" + getImageInfo("{}-{}".format(episode_url, i), i)[0]
        page_urls.append(page_url)

    return page_urls

def main(comic_name):
    episode_urls = searchEpisode(searchComic(comic_name))

    result = {}
    for ep_name in episode_urls:
        page_num = getImageInfo(episode_urls[ep_name])[1]
        #print("Downloading [" + comic_name + ":" + ep_name + "-" + str(page_num) + " pages]:")

        result[ep_name] = getPictureUrls(
                episode_urls[ep_name], page_num)
        pprint(result[ep_name])

    return result

if __name__== '__main__':
    comic_name = "失色世界"

    results = main(comic_name)

    with open('total_result_of_' + comic_name + '.json', 'w') as dst:
        dst.write(json.dumps(results, indent=4))
