# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# import pymysql
import sqlite3
import time
import settings


class DoubanMoviePipeline(object):
    def __init__(self):
        #  self.connect = pymysql.connect(
        #          host=settings.MYSQL_HOST,
        #          db=settings.MYSQL_DBNAME,
        #          user=settings.MYSQL_USER,
        #          passwd=settings.MYSQL_PASSWD,
        #          charset='utf8',
        #          use_unicode=True
        #          )
        self.connect = sqlite3.connect('./movies.db')
        self.cursor = self.connect.cursor()
        self.file = open('movie_id.log', 'a+')
        self.file2 = open('movie_id_insert.log', 'a+')
        self.insert_count = 0
        self.crawl_count = 0

    def if_movie_at_db(self, movie_id):
        sql = 'select movie_id from douban_movie_info where movie_id = {}'.format(movie_id)
        self.cursor.execute(sql)
        ret = self.cursor.fetchone()
        if ret:
            print('{} : Crawled....{}'.format(time.ctime(), movie_id))
            return True
        else:
            return False

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
        try:
            #  sql = 'select movie_id from douban_movie_info where movie_id = {}'.format(movie_id)
            #  self.cursor.execute(sql)
            #  ret = self.cursor.fetchone()
            #  if ret:
            #      print('{} : Crawled....{}'.format(time.ctime(), movie_id))
            #  else:

            if self.file2:

                # self.file2.write('{} : ' +
                # '{}\n'.format(time.ctime(), book_id))
                self.file2.write('{}\n'.format(movie_id))

            datetime = self.get_current_datetime()
            self.cursor.execute(
                """insert into douban_movie_info (\
                id, movie_id, title, cover, director, scriptwriter,\
                starring, movie_type, region,language, release_date,\
                running_time, alternate_name, imdb, rating,\
                rating_people,created_time, updated_time)\
                values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                ?, ?, ?, ?, ?, ?, ?, ?)""",
                (movie_id, title, cover, director, scriptwriter,
                 starring, movie_type, region, language, release_date,
                 running_time, alternate_name, imdb, rating,
                 rating_people, datetime, datetime))
            self.connect.commit()
            print('{} : 数据{}成功入库'.format(time.ctime(), movie_id))
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
        except Exception as error:
            print(error)

        # print(cover,author,translator, publisher, subtitle,title,
        # original_title, publish_date, pages,
        # price, isbn, rating, rating_people, book_id)
        print('=' * 40)

        return item

    def get_current_datetime(self):
        now = int(time.time())
        timeArray = time.localtime(now)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
