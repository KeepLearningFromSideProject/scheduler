#!/usr/bin/env python3
# please add the target episode_url at the start of this code, example:

import requests
import urllib
import execjs
import sys
import json
import re
import sys

from bs4 import BeautifulSoup as Soup

def doRequest(url):
    return requests.get(url, cookies={'RI': '0'})

def getImageInfo(episode_url, p=1):
    resp = doRequest(episode_url)
    resp_content = resp.content.decode('big5')
    
    ch = re.search("ch=(\d*)", episode_url)[1]
    ti = re.search("(\d*).html", episode_url)[1]
    chs = re.search("var chs=(\d*)", resp_content)[1]
    cs = re.search("var cs='(\w*)'", resp_content)[1]
    main_loop = re.search("for.*}}", resp_content)[0]
    nessary_js_funcs = """
        function lc(l)
        {
          if(l.length!=2)
            return l;
          var az="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
          var a=l.substring(0,1);
          var b=l.substring(1,2);
          if(a=="Z")
            return 8000+az.indexOf(b);
          else
            return az.indexOf(a)*52+az.indexOf(b);
        }
        
        function su(a,b,c)
        {
          var e=(a+'').substring(b,b+c);return (e);
        }
        
        function nn(n)
        {
          return n<10 ? '00'+n : n<100? '0'+n : n;
        }
        
        function mm(p)
        {
          return (parseInt((p-1)/10)%10)+(((p-1)%10)*3)
        }
    """

    context = execjs.compile(
        "var y=46;" +
        "var ch={};".format(ch) +
        "var ti={};".format(ti) +
        "var chs='{}';".format(chs) +
        "var cs='{}';".format(cs) +
        "var p={};".format(p) + 
        "var result={};" +
        "function ge(e) {return result;};" +
        nessary_js_funcs +
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

if __name__== '__main__':
    if len(sys.argv) > 1:
        episode_url = sys.argv[1]
    else:
        episode_url = 'https://comicbus.live/online/a-9337.html?ch=315'
    page_num = getImageInfo(episode_url)[1]
    image_urls = getPictureUrls(episode_url, page_num)

    print(json.dumps({
        'page_num': page_num,
        'image_urls': image_urls
    }), end = '')
