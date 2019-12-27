class Tags(object):

    def __init__(self, html):
        self.html = html
        

    def get_tags(self):
        result = self.html.xpath('//div[@class="article"]//table//a/@href')
        ## print(result)
        ## quit()

        hrefs = []
        for href in result:
            hrefs.append('https://book.douban.com' + href)
            print('https://book.douban.com' + href)
        print('共有 {} 条数据'.format(len(hrefs)))
        return hrefs 
