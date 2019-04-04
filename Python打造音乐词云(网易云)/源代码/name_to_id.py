# 将输入的歌名转化为网页ID
import selenium
import time
import re
from selenium.webdriver.support.ui import WebDriverWait


# 搜索歌名
class get_name_id():
	def __init__(self):
		pass
	def get_id(self, song_name):
		self.browser = selenium.webdriver.Chrome()
		self.browser.set_window_size(0, 0)
		self.url = 'http://music.163.com/#/search/m/'
		self.browser.get(self.url)
		# 有多个frame时需要先切换到对应的frame下才能够找到对应的元素
		# 切换
		self.frame1 = self.browser.find_element_by_css_selector(".g-iframe")
		self.browser.switch_to.frame(self.frame1)
		# 定位
		self.browser.find_element_by_id("m-search-input").send_keys(song_name)
		self.browser.find_element_by_css_selector(".btn").click()
		WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_class_name("srchsongst"))
		self.text = self.browser.page_source
		self.browser.close()
		self.pattern = re.compile(r'<div cla.*?song_(.*?)" cla.*?b title="(.*?)">.*?artist.*?\d+">([^<][^s].*?)</.*?album.*?le="(.*?)">.*?</div>')
		# re.S用于跨行匹配
		self.song_list = self.pattern.findall(self.text, re.S)
		print('共找到相关歌曲{0}首'.format(len(self.song_list)))
		self.flag = True
		with open('song_list.txt', 'w', encoding='utf-8') as f:
			for self.song in self.song_list:
				f.write(str(self.song) + '\n')
		for self.song in self.song_list:
			try:
				print(self.song)
			except:
				self.flag = False
				continue
		if not self.flag:
			print('*' * 80)
			print('部分歌曲无法正常显示,若显示的歌曲均不满足要求,可在代码所在文件中的song_list.txt文件中查看所有歌曲')
			print('*' * 80)



if __name__ == '__main__':
	get_name_id().get_id('晴天')