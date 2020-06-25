#!/usr/bin/env python3

import re
class FormatChecker:
    def __init__(self):
        self.home_checker = re.compile(r'https://comicbus.com/html/\d+.html')
        self.episode_checker = re.compile(r'https://comicbus.live/online/a-\d+.html\?ch=\d+')
        self.img_checker = re.compile(r'https://img4.8comic.com/\d+/\d+/\d+/(\d+)_\w+.jpg')

    def is_home_url(self, data):
        print("is home url?")
        result = self.home_checker.match(data)
        if result:
            print("match")
        else:
            print("no")

    def is_episode_url(self, data):
        print("is episode url?")
        for url in data:
            result = self.episode_checker.match(url)
            if result:
                print("match")
            else:
                print("no")

    def is_ordered_page_number(self, data):
        print("is ordered page number?")
        
        current_length = 0
        total_length = len(data)
        start = None
        for url in data:
            result = self.img_checker.match(url)
            if result:
                if start == None:
                    current_length += 1
                    start = int(result.group(1))
                elif int(result.group(1)) == (start + 1):
                    start = int(result.group(1))
                    current_length += 1
                else:
                    print("no")
                    return
            else:
                print("no")
                return
        if current_length != total_length:
            print("no")
        else:
            print("match")
        

if __name__ == "__main__":
    checker = FormatChecker()
    home_urls = [
        "https://comicbus.com/html/9337.html",
        "https://comicbus.com/html/933",
        "https://comicbus.com/html/.html",
        "https://comicbus.com/html/9.hml"
    ]
    for url in home_urls:
        checker.is_home_url(url)

    episode_urls = [
        "https://comicbus.live/online/a-9337.html?ch=311",
        "https://comicbus.live/online/a-9337.html?ch=312",
        "https://comicbus.live/online/a-9337.html?ch=31"
    ]
    checker.is_episode_url(episode_urls)

    img_urls = [
        "https://img4.8comic.com/4/17838/0/001_S98.jpg",
        "https://img4.8comic.com/4/17838/0/002_bUU.jpg",
        "https://img4.8comic.com/4/17838/0/003_4vM.jpg",
        "https://img4.8comic.com/4/17838/0/004_HHH.jpg",
        "https://img4.8comic.com/4/17838/0/005_d7c.jpg",
        "https://img4.8comic.com/4/17838/0/006_Gh8.jpg"
    ]
    checker.is_ordered_page_number(img_urls)

    img_urls = [
        "https://img4.8comic.com/4/17838/0/001_S98.jpg",
        "https://img4.8comic.com/4/17838/0/002_bUU.jpg",
        "https://img4.8comic.com/4/17838/0/003_4vM.jpg",
        "https://img4.8comic.com/4/17838/0/004_HHH.jpg",
        "https://img4.8comic.com/4/17838/0/005_d7c.jpg",
        "https://img4.8comic.com/4/17838/0/007_Gh8.jpg"
    ]
    checker.is_ordered_page_number(img_urls)
