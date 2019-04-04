import os,sys
import requests
from bs4 import BeautifulSoup


def get():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36',
		'Cookie': 'gr_user_id=2acad582-e3d9-4d7d-be07-1e666593044b;\
		 _vwo_uuid_v2=38ABDBB03F0E5D6276C46F1F08FED63F|9025347f700dca4733492e78287c5197;\
		 douban-fav-remind=1; bid=7NEM3PwlB5U; ll="118254";\
		  viewed="30253245_6427971_26827295_21642008_26709315_3988517_6052205_26337727_1968704_1801062"; \
		  dbcl2="194409884:Yx+rtw2JMuw"; push_noty_num=0; push_doumail_num=0; \
		  douban-profile-remind=1; __yadk_uid=6wLr3OInjYbLT4P5jxDzffSQZPo5bcHS; \
		  gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f6b04841-6218-4162-bf32-dc8e24bc4f78; \
		  gr_cs1_f6b04841-6218-4162-bf32-dc8e24bc4f78=user_id%3A1;\
		   gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f6b04841-6218-4162-bf32-dc8e24bc4f78=true;\
		    ck=tIDX; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1554342115%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D2pu3D_S8H_6n4yFqDk37XZfk79Op7mvhk3WTahlt2ZBWJHM0Gu8HcGFcq5GxFGJe%26wd%3D%26eqid%3Db9802d2100108b34000000035ca4a510%22%5D;\
		     _pk_ses.100001.3ac3=*; __utmc=30149280; __utmc=81379588; ap_v=0,6.0; \
		     _pk_id.100001.3ac3=cd1263907d0d510d.1512391724.19.1554343221.1554301582.;\
		      __utma=30149280.1937024719.1523114193.1554342115.1554343221.28;\
		       __utmz=30149280.1554343221.28.26.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt_douban=1;\
		        __utmb=30149280.1.10.1554343221; __utma=81379588.1289709393.1512391724.1554342115.1554343221.16;\
		         __utmz=81379588.1554343221.16.13.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1;\
		          __utmb=81379588.1.10.1554343221'
		}
	url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-hot'
	res = requests.get(url, headers=headers)
	soup = BeautifulSoup(res.text,'lxml')
	category_list = []
	soup_list = soup.find('div', attrs={'class': 'article'})
	first_class = soup_list.findAll('a', attrs={'class': 'tag-title-wrapper'})
	second_class = soup_list.findAll('table', attrs={'class': 'tagCol'})
	first_class_list = []
	for fc in first_class:
		first_class_list.append(fc.attrs['name'])
	num = 0
	for sc in second_class:
		second_class_list = []
		sc = sc.findAll('a')
		for sc_i in sc:
			second_class_list.append(sc_i.string.strip())
		category_list.append([first_class_list[num], second_class_list])
		num += 1
	return category_list


print(get())	
