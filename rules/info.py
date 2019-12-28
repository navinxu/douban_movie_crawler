# -*- coding: utf-8 -*-
import re
from lxml import etree
#import chardet


class Info(object):
    def __init__(self, html, request_url):
        self.html = html
        self.request_url = request_url
        self.id_info = self.get_id_info_text()
        """
        ##print('-=' * 20)
        ##print(self.id_info)
        self.get_id_info_text()
        return
        """

    def get_movie_info(self, items):

        if not self.id_info:
            return False

        items.movie_id = self.get_movie_id()
        items.title = self.get_title()
        items.cover = self.get_cover()
        items.director = self.get_director()
        items.scriptwriter = self.get_scriptwriter()
        items.starring = self.get_starring()
        items.movie_type = self.get_movie_type()
        items.region = self.get_region()
        items.language = self.get_language()
        items.release_date = self.get_release_date()
        items.running_time = self.get_running_time()
        items.alternate_name = self.get_alternate_name()
        items.imdb = self.get_imdb()
        items.rating = self.get_rating()
        items.rating_people = self.get_rating_people()

        #print('=' * 20)
        #print('movie_id:' + items.movie_id)
        #print('title: ' + items.title)
        #print('cover: ' + items.cover)
        #print('director: ' + items.director)
        #print('scriptwriter:' + items.scriptwriter)
        #print('starring: ' + items.starring)
        #print('movie_type: ' + items.movie_type)
        #print('region: ' + items.region)
        #print('language: ' + items.language)
        #print('release_date: ' + items.release_date)
        #print('running_time:' + items.running_time)
        #print('alternate_name: ' + items.alternate_name)
        #print('imdb: ' + items.imdb)
        #print('rating: ' + items.rating)
        #print('rating_people: ' + items.rating_people)
        return items

    def get_id_info_text(self):
        #id_info = self.html.xpath('//div[@id="info"]').text()
        try:
            id_info = etree.tostring(self.html.xpath('//div[@id="info"]')[0], encoding='utf-8', pretty_print=True)
            return id_info.decode('utf-8')
        except IndexError as e:
            #print('在解析 id_info 时遇到未知错误！')
            #print(e)
            return False
        #id_info = id_info.decode(chardet.detect(id_info)['encoding'])

    def get_imdb(self):
        """
        IMDb链接:</span> <a...>...</a></br>
        唯一值
        """
        try:
            imdb_html = re.findall(r'IMDb链接:</span>([\s\S]+?)<br', self.id_info)[0]
            imdb = str(etree.HTML(imdb_html).xpath('//a/text()')[0])
        except Exception as e:
            imdb = 'None'
        return self.format_item(imdb)

    def get_elem_type(self, elem):
        """
        获取元素
        类型:</span> <span...>...</span> / <span...>...</span>...<br/>
        region"""
        try:
            elem = re.findall(r'{}:</span>([\s\S]+?)<br/>'.format(elem), self.id_info)[0]
            html = etree.HTML(elem)
            return self.format_item(html.xpath('//span/text()'))
        except IndexError as e:
            return self.format_item(['None'])

    def get_alternate_name(self):
        """
        又名
        """
        alternate_name = self.get_elem_region('又名')
        return alternate_name

    def get_running_time(self):
        """
        片长
        结构同 类型
        """
        running_time = self.get_elem_type('片长')
        return running_time


    def get_release_date(self):
        """
        上映日期
        结构同 类型
        """
        release_date = self.get_elem_type('上映日期')
        return release_date


    def get_language(self):
        """
        语言
        结构同 类型
        """
        language = self.get_elem_region('语言')
        return language

    def get_elem_region(self, elem):
        try:
            elem = re.findall(r'{}:</span>([\s\S]+?)<br/>'.format(elem), self.id_info)[0]
        except IndexError as e:
            elem = ''
        return elem

    def get_region(self):
        """
        制片国家/地区
        """
        region  = self.get_elem_region('制片国家/地区')
        return self.format_item(region)


    def get_movie_type(self):
        """
        电影类型
        类型:</span> <span...>...</span> / <span...>...</span>...<br/>
        """
        movie_type = self.get_elem_type('类型')
        return movie_type

    def get_elem_director(self, elem):
        """
        提取与“导演”类型的结构相似的元素
        """
        try:
            ##print(self.get_id_info_text())
            elem = re.findall(r'{}</span>: <span class="attrs">([\s\S]+?)</span></span><br/>'.format(elem), self.id_info)[0]
            html = etree.HTML(elem)
            return self.format_item(html.xpath('//a/text()'))
        except IndexError as e:
            return self.format_item(['None'])

    def get_starring(self):
        """
        主演
        结构同 导演
        """
        starring = self.get_elem_director('主演')
        return starring


    def get_scriptwriter(self):
        """
        编剧
        结构同 导演
        """
        scriptwriter = self.get_elem_director('编剧')
        return scriptwriter

    def get_director(self):
        """
        导演</span>: <span class='attrs'><a...>...</a> / <a...>...</a> / ...</span></span><br/>
        """
        director = self.get_elem_director('导演')
        return director


    def get_cover(self):
        try:
            cover = self.html.xpath('//div[@id="mainpic"]/a/img/@src')
        except Exception as e:
            cover = 'None'
        return self.format_item(cover)

    def get_title(self):
        try:
            ##print(etree.tostring(self.html, encoding="utf-8").decode('utf-8'))
            title = self.html.xpath('//title/text()')[0]
            title = re.findall(r'([\s\S]+?)(?:\s*\(豆瓣\)\s*)', title.strip())[0]
        except IndexError as e:
            title = 'None'
        return self.format_item(title)

    def get_movie_id(self):
        ## 电影在豆瓣的ID
        ## https://movie.douban.com/subject/1292052/
        movie_id = self.request_url.rstrip('/').split('/').pop()
        return movie_id

    def get_rating_people(self):
        ## 评分人数
        try:
            interest_sectl = self.html.xpath('//div[@id="interest_sectl"]')[0]
            rating_people =  str(interest_sectl.xpath('//a[@class="rating_people"]/span[@property="v:votes"]/text()')[0])
        except IndexError as e:
                rating_people = '0'

        return self.format_item(rating_people)

    def get_rating(self):
        try:
            ## 评分 
            interest_sectl = self.html.xpath('//div[@id="interest_sectl"]')

            rating = interest_sectl[0].xpath('//strong[@class="ll rating_num"]/text()')[0]
        except IndexError as e:
            # 评分人数不足（< 10）
            rating = '0.0'

        return self.format_item(rating)

    def format_item(self, items):

        if isinstance(items, str):
            items = items.strip()
            if items == "":
                items = "None"
            return items
        elif isinstance(items, list):
            for item in items:
                items[items.index(item)] = item.strip()
            return '/'.join(items)
        elif items is None:
            return "None"
