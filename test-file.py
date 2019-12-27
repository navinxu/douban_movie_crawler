#!/usr/bin/env python
# coding:utf-8
# **********************************************************
# * Author        : Navin Xu
# * Email         : admin@navinxu.com
# * Create time   : 2019-12-27 20:13
# * Filename      : test-file.py
# * Description   :
# **********************************************************

#  try:
#      f_r = open('last_start.txt', 'r')
#  except FileNotFoundError as e:
#      try:
#          f_w = open('last_start.txt', 'w')
#          f_w.write("")
#          #  f_w.write(str(1024))
#          f_w.close()
#      except IOError as ex:
#          quit(ex.message)
#      f_r = open('last_start.txt', 'r')
#  #  print(f_r.readline())
#
#  content = f_r.readline()
#  #  if (content == ""):
#  #      print("ok")
#
#  if not (content == ""):
#      print("ok")
#  f_r.close()

f = open('test.txt', 'w')
f.write("111")

open('test.txt', 'w').close()
f.write("222")

f.close()
with open('test.txt', 'r') as f:
    for line in f.readlines():
        print(line)
    f.close()
