# -*- coding: utf-8 -*-
# @Author: Marte
# @Date:   2019-04-02 18:30:40
# @Last Modified by:   Marte
# @Last Modified time: 2019-04-02 19:11:11


from bs4 import BeautifulSoup
import requests,sys

server = 'http://www.biqukan.com/'
target = 'http://www.biqukan.com/1_1094/'
path='file.txt'


def geturl(target,server,path):
    req = requests.get(url = target)
    html = req.text
    div_bf = BeautifulSoup(html)
    div = div_bf.find_all('div', class_ = 'listmain')
    a_bf = BeautifulSoup(str(div[0]))
    a = a_bf.find_all('a')
    for item in a[15:]:
        print('name:{%s}' %item.string)
        url=server+item.get('href')
        txt=getcontent(url)
        writetxt(path,item.string,txt)


def getcontent(url):
    req = requests.get(url = url)
    html = req.text
    bf = BeautifulSoup(html)
    texts = bf.find_all('div', class_ = 'showtxt')
    texts = texts[0].text.replace('\xa0'*8,'\n\n')
    return texts



def writetxt(path,name,text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(name + '\n')
        f.writelines(text)
        f.write('\n')

geturl(target = 'http://www.biqukan.com/1_1094/',server = 'http://www.biqukan.com/',path='file.txt')


