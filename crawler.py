# -*- coding: utf-8 -*-

from rules.info import Info
from lxml import etree
from item import MovieItems
import time
from core.request import Request
# from pipelinestest import DoubanMoviePipeline
from pipelines import DoubanMoviePipeline
from rules.pages import Pages
import json
import re

print(time.ctime() + ': 爬虫已经开始工作')
begin_date = time.ctime()
print(time.ctime() + ': 开始时间是：{}'.format(begin_date))

"""
保存上次爬取到的位置
（start 的值）
"""
filename = 'last_start.txt'
try:
    f_r = open(filename, 'r')
except FileNotFoundError as ex:
    try:
        f_w = open(filename, 'w')
        f_w.close()
        f_r = open(filename, 'r')
    except IOError as e:
        quit(e.message)

start = 0
content = f_r.readline()
if not (content == ""):
    start = int(content)
f_r.close()

try_counts = 0
try_counts4 = 0
try_counts5 = 0

db_pipeline = DoubanMoviePipeline()
while True:
    '''
    电影分页循环
    '''

    """
    实时改变文件中的 start 值
    """
    try:
        f_w = open(filename, 'w')
    except IOError as e:
        quit(e.message)
    f_w.write(str(start))

    print('进入第 {} 页'.format(int(start / 20 + 1)))
    url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}'.format(start)
    if try_counts == 10 or try_counts4 == 10 or try_counts5 == 10:
        print("可能被Ban了！位置：Outer")
        f_w.close()
        break

    request = Request()
    r = request.get_html_text(url)
    if r:
        if re.match(r'\{"data":\[\{"directors":\[', r):
            html_json = json.loads(r)
        else:
            try_counts += 1
            continue

        if request.status_code == 200:

            try_counts4 = 0
            try_counts5 = 0

            pages = Pages(html_json)

            if pages.is_end():
                end_date = time.ctime()
                print(end_date + ': 数据已经爬取完成，共收录 '
                                 + '{} 条数据。'.format(db_pipeline.insert_count))
                with open('end_date.txt', 'a+') as f:
                    f.write('Start@{}\nEnd@{}\n共爬取{}个条目\n数据库共收录{}个条目'.
                            format(begin_date, end_date,
                                   db_pipeline.crawl_count,
                                   db_pipeline.insert_count))
                print(time.ctime() + ': 结束时间是：{}'.format(end_date))
                f_w.close()
                quit()
            movie_items = pages.get_movie_pages()
            movie_item = movie_items.pop()

            try_counts2 = 0
            try_counts3 = 0
            while True:
                """
                电影主页循环
                """

                if try_counts2 == 10 or try_counts3 == 10:
                    f_w.write(str(start))
                    f_w.close()
                    quit()

                movie_id = movie_item.rstrip('/').split('/').pop()

                if db_pipeline.if_movie_at_db(movie_id):
                    try:
                        movie_item = movie_items.pop()
                        continue
                    except IndexError as e:
                        try_counts = 0
                        break

                print('{} : 已经爬取 {} 个电影页面'.format(
                                                           time.ctime(),
                                                           db_pipeline.
                                                           crawl_count))
                print('{} : 本次共收录 {} 个电影页面'.format(
                                                           time.ctime(),
                                                           db_pipeline.
                                                           insert_count))
                print('{} : 正在爬取电影 {}'.format(
                                                    time.ctime(),
                                                    movie_item.
                                                    rstrip('/').
                                                    split('/').
                                                    pop()))

                request = Request()
                r = request.get_html_text(movie_item)
                if not r:
                    try:
                        movie_item = movie_items.pop()
                        continue
                    except IndexError as e:
                        break

                info = Info(etree.HTML(r), movie_item)
                if request.status_code == 200:
                    item = MovieItems()
                    info.get_movie_info(item)
                    db_pipeline.process_item(item)
                    time.sleep(0.5)
                    try_counts2 = 0
                    try_counts3 = 0

                elif request.status_code == 403:
                    print(time.ctime() + ' : 爬虫所在 IP 已经被网站列入黑名单，需要更换 IP。退出位置：Inner While')
                    #  movie_items.append(movie_item)
                    try_counts3 += 1
                    continue
                else:
                    print('{} : HTTP CODE : {}未知错误，可能是错误的URL，也可能IP被封禁了！退出位置：Inner While'.format(
                                                      time.ctime(),
                                                      request.status_code))
                    #  movie_items.append(movie_item)
                    try_counts2 += 1
                    continue

                try:
                    movie_item = movie_items.pop()
                except IndexError as e:
                    try_counts = 0
                    break

            start += 20

            # 关闭文件
            f_w.close()

        elif request.status_code == 403:
            print(time.ctime() + ' : 爬虫所在 IP 已经被网站列入黑名单，需要更换 IP。退出位置：Outer While')
            try_counts4 += 1
        else:
            print('{} : HTTP CODE : {}未知错误，可能是错误的URL，也可能IP被封禁了！退出位置：Outer While'.format(time.ctime(), request.status_code))
            try_counts5 += 1
    else:
        try_counts += 1
        continue
