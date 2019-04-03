import requests
from lxml import etree

def parse():
    response = requests.get("http://www.scuec.edu.cn")
    response.encoding = "utf-8"
    html=response.text
    print(html)
    with open('index.html','w',encoding='utf-8') as f:
        f.write(html)
    ###
    html = etree.parse('index.html', etree.HTMLParser())

    result = html.xpath("//div[@id='menu99']")

    print(result)

parse()




import requests

res=requests.get('https://www.scuec.edu.cn/picture/article/1/3c/c5/d38099cf49649843aae7831e6304/486ac155-1963-454e-b389-6a4807e3f893.jpg')

with open('1.jpg','wb') as f:
    f.write(res.content)
