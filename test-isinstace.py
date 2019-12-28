#!/usr/bin/env python
# coding:utf-8
# **********************************************************
# * Author        : Navin Xu
# * Email         : admin@navinxu.com
# * Create time   : 2019-12-28 20:09
# * Filename      : test-isinstace.py
# * Description   :
# **********************************************************

aStr = ""
if isinstance(aStr, str):
    print("str")

aList = [1, 2, 3]
if isinstance(aList, list):
    print("list")

if isinstance(aStr, list):
    print("list")

aNone = None
if aNone is None:
    print("None")
