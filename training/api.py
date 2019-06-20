## -*- coding: utf-8 -*-

import requests
import json

bookname = "なっとくする量子力学"
api="https://www.googleapis.com/books/v1/volumes?q={bookname}"
r=requests.get(api)
dic=json.loads(r.text)
book=dic["items"][0]['volumeInfo']
title=book['title']
page=book['pageCount']
imgurl=book['imageLinks']['thumbnail']
print(title,page,imgurl)
