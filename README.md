# 豆瓣电影爬虫
Created On： 2019-12-27

## 编程语言
Python

## 依赖
1. Python3
2. pip库依赖都列在项目的 `requirements.pip` 文件中

## 使用的数据库
SQLite3

## 运行
只要 clone 到本地就可以使用了（只要豆瓣的 API 不变，这个爬虫是本人两年前写的，现在修改优化一下还能用，但不知以后的会怎样，不管怎样变化，万变不离其宗）。
运行：
```bash
python3 crawler.py
```
运行的前提条件是要有一个名字为 `movies.db` 的 SQLite3 数据库，且有个叫 `douban_movie_info` 的数据表，表的定义请看项目的 `sqlite3_table_create.sql` 文件。
