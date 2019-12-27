# -*- coding: utf-8 -*-
import requests
import hashlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from fake_useragent import UserAgent
import random
import time
import settings
# from lxml import etree
# from info import Info
# from item import MovieItems
# from pipelines import DoubanMoviePipeline


class Request(object):
    def __init__(self):
        # self.status_code = 0
        pass

    def get_random_ua(self):
        return UserAgent().random

    def send_request(self, url):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        try_count = 0
        while True:
            try:
                delay = 0
                if bool(settings.DOWNLOAD_RANDOM):
                    # 保证不小于1,且小于3
                    delay = random.randint(1, 6) * int(settings.DOWNLOAD_DELAY) * 0.25
                    time.sleep(delay)
                else:
                    delay = int(settings.DOWNLOAD_DELAY)
                    time.sleep(delay)
                print("间隔 {} s！".format(delay))

                #  authHeader, mayi_proxy = self.generate_sign()
                #  headers = {
                #      "Mayi-Authorization": authHeader,
                #      "User-Agent": UserAgent().random
                #  }
                #
                #  proxies = {
                #      "http": mayi_proxy,
                #      "https": mayi_proxy,
                #  }
                # print('=' * 20)
                # print(url)
                print('{} : 正在爬取 {}'.format(time.ctime(), url))
                headers = {
                   "User-Agent": UserAgent().random
                }
                # self.r = requests.get(url=url, proxies=proxies, headers=headers, allow_redirects=False, verify=False)
                self.r = requests.get(url=url, headers=headers, allow_redirects=False, verify=False)
                # print(self.r.status_code)
                # print(response.headers)
                # print(response.text)

                self.r.encoding = 'utf-8'
                self.status_code = self.r.status_code
                # print(self.status_code)
                return self.r
            except Exception:
                # print(e)
                if try_count == 10:
                    print('{}: 超时！'.format(time.ctime()))
                    return False
                    break
                try_count += 1
                print('{} : 页面 {} 进行第 {} 次尝试'.format(time.ctime(), url, try_count))

    def get_html_text(self, url):
        r = self.send_request(url)

        if r:
            return r.text
        else:
            print('{}: 未知错误！'.format(time.ctime()))
            return False

    def generate_sign(self):
        appkey = "166675335"
        secret = "d85906226907a4bf6b3648d69bfd4706"
        mayi_url = "s5.proxy.mayidaili.com"
        mayi_port = "8123"
        mayi_proxy = 'http://{}:{}'.format(mayi_url, mayi_port)

        paramMap = {
            "app_key": appkey,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        keys = sorted(paramMap)
        codes = "%s%s%s" % (secret, str().join('%s%s' % (key, paramMap[key]) for key in keys), secret)
        sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()
        paramMap["sign"] = sign
        keys = paramMap.keys()
        authHeader = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, paramMap[key]) for key in keys)
        return authHeader, mayi_proxy


# request = Request()
# htmlText = request.get_html_text('https://movie.douban.com/subject/1468155/')
# # print(htmlText)
# info = Info(etree.HTML(htmlText), 'https://movie.douban.com/subject/1468155/')
# item = MovieItems()
# info.get_movie_info(item)
# db_movie_pipeline = DoubanMoviePipeline()
# db_movie_pipeline.process_item(item)
# info.get_id_info_text()
# print(len(json.loads(request.get_html_text('https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=0'))['data']))
# print(request.get_html_text('https://book.douban.com'))
