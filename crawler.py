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

start = 0
try_counts = 0

db_pipeline = DoubanMoviePipeline()
while True:
    '''
    电影分页循环
    '''
    print('进入第 {} 页'.format(int(start / 20 + 1)))
    url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}'.format(start)
    if try_counts == 5:
        print("可能被Ban了！")
        break
    request = Request()
    r = request.get_html_text(url)
    if r:
        if re.match(r'\{"data":\[\{"directors":\[', r):
            html_json = json.loads(r)
        else:
            continue

        if request.status_code == 200:

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
                quit()
            movie_items = pages.get_movie_pages()
            movie_item = movie_items.pop()

            while True:
                """
                电影主页循环
                """

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

                elif request.status_code == 403:
                    print(time.ctime() + ' : 爬虫所在 IP 已经被网站列入黑名单，需要更换 IP')
                    movie_items.append(movie_item)
                else:
                    print('{} : HTTP CODE : {}未知错误，可能是错误的URL，' +
                          '也可能IP被封禁了！'.format(
                                                      time.ctime(),
                                                      request.status_code))
                    movie_items.append(movie_item)

                try:
                    movie_item = movie_items.pop()
                except IndexError as e:
                    try_counts = 0
                    break

            start += 20

        elif request.status_code == 403:
            print(time.ctime() + ' : 爬虫所在 IP 已经被网站列入黑名单，需要更换 IP')
            quit()
        else:
            quit('{} : HTTP CODE : {}未知错误，可能是错误的URL，' +
                 '也可能IP被封禁了！'.format(time.ctime(), request.status_code))
    else:
        try_counts += 1
        continue
