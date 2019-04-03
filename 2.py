# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2019-04-02 20:44:17
# @Last Modified by:   Marte
# @Last Modified time: 2019-04-03 12:42:43


import requests
from requests import codes
from urllib.parse import urlencode
from multiprocessing.pool import Pool
import os,sys


def get_page(offset):
    params = {
       'page':offset,
       'per_page':12
    }
    base_url = 'https://unsplash.com/napi/photos?'
    url = base_url + urlencode(params)
    try:
        resp = requests.get(url)
        if 200  == resp.status_code:
            return resp.json()
    except requests.ConnectionError:
        return None


def parse(json):
    for item in json:
        id=item['id']
        downlaod(id)

def downlaod(id):
    para={
        'force':'true'
    }
    base_url1 = 'https://unsplash.com/photos/xxx/download?'
    path=base_url1.replace('xxx',id) + urlencode(para)
    file_path='img'+os.path.sep+id+'.jpg'
    img_path='img'
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    #print(file_path)
    try:
        resp = requests.get(path)
        if codes.ok == resp.status_code:
            with open(file_path, 'wb') as f:
                  f.write(resp.content)
            print('filename:%s download' %(id+'.jpg'))
    except requests.ConnectionError:
        print('download error')


def main(offset):
    res=get_page(offset)
    parse(res)

NUM= 6

if __name__ == '__main__':
    pool = Pool()
    groups = ([i for i in range(3,NUM)])
    pool.map(main, groups)
    pool.close()
    pool.join()
