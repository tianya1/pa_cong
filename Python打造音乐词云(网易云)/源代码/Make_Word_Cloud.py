import requests
import json
import os
import base64
import codecs
import math
import jieba
from Crypto.Cipher import AES
from wordcloud import WordCloud
from scipy.misc import imread
import name_to_id


# 用于算post的两个参数的函数
# 具体原理详见知乎：
# https://www.zhihu.com/question/36081767
def aesEncrypt(text, secKey):
	pad = 16 - len(text) % 16
	if isinstance(text, bytes):
		text = text.decode('utf-8')
	text = text + str(pad * chr(pad))
	encryptor = AES.new(secKey, 2, '0102030405060708')
	ciphertext = encryptor.encrypt(text)
	ciphertext = base64.b64encode(ciphertext)
	return ciphertext


def rsaEncrypt(text, pubKey, modulus):
	text = text[::-1]
	rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
	return format(rs, 'x').zfill(256)


def createSecretKey(size):
	return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


# 获得所有评论
def get_all_comments(songid):
	url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(songid)
	# proxies ={
	# 		'http': '47.90.62.177',
	# 		'https': '119.129.99.189'
	# 	}
	headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36',
				'referer': 'http://music.163.com/'
			}
	modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
	nonce = '0CoJUm6Qyw8W8jud'
	pubKey = '010001'
	num = 0
	comments_list = []
	comments_num = 0
	while True:
		text = {
				'username': '',
				'password': '',
				'rememberLogin': 'true',
				'offset': num * 10
				}
		text = json.dumps(text)
		secKey = createSecretKey(16)
		encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
		encSecKey = rsaEncrypt(secKey, pubKey, modulus)
		post_data = {
					'params': encText,
					'encSecKey': encSecKey
					}
		# res = requests.post(url, headers=headers, data=post_data, proxies=proxies)
		res = requests.post(url, headers=headers, data=post_data)
		if num == 0:
			# 获得评论总数
			comments_num = res.json()['total']
			num_max = math.ceil(comments_num / 10)
		res_dic = json.loads(res.text)
		comments = res_dic['comments']
		for comment in comments:
			try:
				comments_list.append(comment['content'])
			except:
				continue
		if num_max > num:
			num += 1
		else:
			break
	return comments_list


# 获得热门评论
def get_hot_comments(songid):
	url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(songid)
	# proxies ={
	# 		'http': '47.90.62.177',
	# 		'https': '119.129.99.189'
	# 	}
	headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36',
				'referer': 'http://music.163.com/'
			}
	modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
	nonce = '0CoJUm6Qyw8W8jud'
	pubKey = '010001'
	comments_list = []
	text = {
			'username': '',
			'password': '',
			'rememberLogin': 'true',
			}
	text = json.dumps(text)
	secKey = createSecretKey(16)
	encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
	encSecKey = rsaEncrypt(secKey, pubKey, modulus)
	post_data = {
				'params': encText,
				'encSecKey': encSecKey
				}
	# res = requests.post(url, headers=headers, data=post_data, proxies=proxies)
	res = requests.post(url, headers=headers, data=post_data)
	res_dic = json.loads(res.text)
	comments = res_dic['hotComments']
	for comment in comments:
		try:
			comments_list.append(comment['content'])
		except:
			continue
	return comments_list


# 过滤函数：清洗数据，删除不必要的符号。
def filterword(filterdata):
	symbol = ' ，。“”~！@#￥%……&*（）——+=【】{}、|；：‘’《》？!#$^&()[]{};:",.<>/?\\-\n'
	for sym in symbol:
		filterdata = filterdata.replace(sym, '')
		filterdata = filterdata.strip(' ')
	return filterdata


# 处理所有评论
def deal_comments(comments):
	all_comments = ''
	for c in comments:
		all_comments = all_comments + c
	all_comments = filterword(all_comments)
	words = ' '.join(jieba.cut(all_comments))
	bg_pic = imread('heart-mask.jpg')
	# 这里设置字体路径和背景图片
	Words_Cloud = WordCloud(font_path="simkai.ttf", mask=bg_pic).generate(words)
	Words_Cloud.to_file('song_cloud.jpg')


if __name__ == '__main__':
	song_name = input('请输入歌曲名：')
	song_list = name_to_id.get_name_id().get_id(song_name)
	while True:
		song_id = input('请输入需要制作词云的歌曲id(引号内的数字串)：')
		try:
			int(song_id)
			break
		except:
			print('歌曲id必须为纯数字！！！')
	while True:
		choice = input('利用热门评论制作词云请输入：0\n利用所有评论制作词云请输入：1\n：')
		if choice == '0':
			comments_list = get_hot_comments(song_id)
			deal_comments(comments_list)
			break
		elif choice == '1':
			comments_list = get_all_comments(song_id)
			deal_comments(comments_list)
			break
		else:
			print('选择有误，请重新输入！')


