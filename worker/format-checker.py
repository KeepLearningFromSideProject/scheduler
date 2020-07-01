#!/usr/bin/env python3

import re
class FormatChecker:
    def __init__(self):
        self.home_checker = re.compile(r'https://comicbus.com/html/\d+.html')
        self.episode_checker = re.compile(r'https://comicbus.live/online/a-\d+.html\?ch=\d+')
        self.img_checker = re.compile(r'https://img4.8comic.com/\d+/\d+/\d+/(\d+)_\w+.jpg')

    def is_home_url(self, data):
        result = self.home_checker.match(data)
        if result:
            return True
        else:
            return False

    def is_episode_url(self, data):
        for url in data:
            result = self.episode_checker.match(url)
            if result:
                return True
            else:
                return False

    def is_ordered_page_number(self, data):
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
                    return False
            else:
                return False
        if current_length != total_length:
            return False
        else:
            return True
        

if __name__ == "__main__":
    checker = FormatChecker()
    import json
    from subprocess import Popen, PIPE

    execute_command = ["../scripts/get_comic_home.py"]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    home_url = json.loads(out)
    ## static test data
    # home_urls = [
    #     "https://comicbus.com/html/9337.html",
    #     "https://comicbus.com/html/933",
    #     "https://comicbus.com/html/.html",
    #     "https://comicbus.com/html/9.hml"
    # ]
    if checker.is_home_url(home_url):
        print("correct home_url")
    else:
        print("incorrect home_url")

    
    execute_command = ["../scripts/get_episode_urls.py"]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    episode_urls = json.loads(out)
    ## static test data
    # episode_urls = [
    #     "https://comicbus.live/online/a-9337.html?ch=311",
    #     "https://comicbus.live/online/a-9337.html?ch=312",
    #     "https://comicbus.live/online/a-9337.html?ch=31"
    # ]
    print(episode_urls)
    if checker.is_episode_url(episode_urls):
        print("correct episode_url")
    else:
        print("incorrect episode_url")

    execute_command = ["../scripts/get_images.py"]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    img_urls = json.loads(out)
    ## static test data
    # img_urls = [
    #     "https://img4.8comic.com/4/17838/0/001_S98.jpg",
    #     "https://img4.8comic.com/4/17838/0/002_bUU.jpg",
    #     "https://img4.8comic.com/4/17838/0/003_4vM.jpg",
    #     "https://img4.8comic.com/4/17838/0/004_HHH.jpg",
    #     "https://img4.8comic.com/4/17838/0/005_d7c.jpg",
    #     "https://img4.8comic.com/4/17838/0/006_Gh8.jpg"
    # ]
    ## wrong page number
    # img_urls = [
    #     "https://img4.8comic.com/4/17838/0/001_S98.jpg",
    #     "https://img4.8comic.com/4/17838/0/002_bUU.jpg",
    #     "https://img4.8comic.com/4/17838/0/003_4vM.jpg",
    #     "https://img4.8comic.com/4/17838/0/004_HHH.jpg",
    #     "https://img4.8comic.com/4/17838/0/005_d7c.jpg",
    #     "https://img4.8comic.com/4/17838/0/007_Gh8.jpg"
    # ]
    if checker.is_ordered_page_number(img_urls):
        print("correct page number")
    else:
        print("incorrect page number")