# -*- coding: utf-8 -*-

import requests
from fake_useragent import UserAgent
  
  # 蘑菇代理的隧道代理，以及隧道订单
appKey = "xxxx"
ip = 'transfer.mogumiao.com'
port = '9001'

# 蘑菇隧道代理服务器地址
proxy = {'http': 'http://{}:{}'.format(ip, port)}

# 准备去爬的 URL 链接
url = 'https://ip.cn'

#  用 Python 的 Requests 模块。先订立 Session()，再更新 headers 和 proxies 
s = requests.Session()
s.headers.update({'Proxy-Authorization': 'Basic '+ appKey})
s.proxies.update(proxy)
pg = s.get(url, timeout=(300, 270),headers = {'User-Agent': UserAgent().random}, verify=False,allow_redirects=False)  # tuple: 300 代表 connect timeout, 270 代表 read timeout
pg.encoding = 'UTF-8'
print(pg.text)
