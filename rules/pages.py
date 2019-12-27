# -*- coding: utf-8 -*-
"""
电影翻页
"""

class Pages(object):
    def __init__(self, html_json):
        self.json = html_json

    def is_end(self):
        if not self.json:
            return True
        return False


    def get_movie_pages(self):
        movie_items = self.json['data']

        urls = []
        for item in movie_items:
            urls.append(item['url'])

        #print(urls)
        return urls
