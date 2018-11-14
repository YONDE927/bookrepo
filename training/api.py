## -*- coding: utf-8 -*-

import requests
import json


api="https://www.googleapis.com/books/v1/volumes?q={なっとくする量子力学}"
r=requests.get(api)
dic=json.loads(r.text)
book=dic["items"][0]['volumeInfo']
title=book['title']
page=book['pageCount']
imgurl=book['imageLinks']['thumbnail']
print(title,page,imgurl)
