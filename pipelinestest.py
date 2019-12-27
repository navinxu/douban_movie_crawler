# -*- coding: utf-8 -*-

# Define your item pipelines here
#
import time


class DoubanMoviePipeline(object):
    def __init__(self):
        self.file = open('movie_id.log', 'a+')
        self.file2 = open('movie_id_insert.log', 'a+')
        self.insert_count = 0
        self.crawl_count = 0

    def process_item(self, item):
        """
        item 为 Item 的对象
        """
        movie_id = item.movie_id
        title = item.title
        cover = item.cover
        director = item.director
        scriptwriter = item.scriptwriter
        starring = item.starring
        movie_type = item.movie_type
        region = item.region
        language = item.language
        release_date = item.release_date
        running_time = item.running_time
        alternate_name = item.alternate_name
        imdb = item.imdb
        rating = item.rating
        rating_people = item.rating_people

        if self.file:
            # self.file.write('{} : {}\n'.format(time.ctime(), book_id))
            self.file.write('{}\n'.format(movie_id))

        self.crawl_count += 1
        print(time.ctime() + ': 已爬取 {} 条电影数据'.format(self.crawl_count))
        print(time.ctime() + ' : 目前一共收录 {} 条电影数据'.format(self.insert_count))
        print('{} : Crawled....{}'.format(time.ctime(), movie_id))
        self.insert_count += 1

        print('=+' * 20)
        print(movie_id)
        print(title)
        print(cover)
        print(director)
        print(scriptwriter)
        print(starring)
        print(movie_type)
        print(region)
        print(language)
        print(release_date)
        print(running_time)
        print(alternate_name)
        print(imdb)
        print(rating)
        print(rating_people)
        print("=" * 40)
        # print(cover,author,translator, publisher, subtitle,title,
        # original_title, publish_date, pages,
        # price, isbn, rating, rating_people, book_id)
        # print('=' * 40)

        return item

    def get_current_datetime(self):
        now = int(time.time())
        timeArray = time.localtime(now)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
