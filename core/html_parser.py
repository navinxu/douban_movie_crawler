# -*- coding: utf-8 -*-
'''
此文件生成xpath对象
'''

from lxml import etree

class HTMLParser(object):
    def __init__(self, html_text):
        self.html_text = html_text

    def get_xpath_html_obj(self):
        return etree.HTML(self.html_text)
