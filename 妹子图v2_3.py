import requests, os, time
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def get_(way='page', num=1, tag=None):
	if not tag:
		url = 'https://www.mzitu.com/{}/{}'.format(way, str(num))
	else:
		url = tag + 'page/' + str(num)
	#	print(url)
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
		"Referer": "https://www.mzitu.com/"}
	r = req(url, headers=headers)
	soup = BeautifulSoup(r.text, features='html.parser')
	if soup.find('title').get_text().find('404') != -1:
		return
	try:
		num = soup.find(class_='nav-links').find_all('a')[-2].get_text()
	except AttributeError:
		num = 1
	try:
		li = soup.find(id='pins').find_all('li')
		name = [i.find('a').find('img').get('alt') for i in li]
		list = [i.find('a').get('href').split('/')[-1] for i in li]
	except AttributeError:
		li = soup.find(class_='tags').find_all('dd')
		#		web,name=li[0].find('a').get('href'),li[0].find('a').get_text()
		#		print(web,name)
		list = [(i.find('a').get('href'), i.find('a').get_text()) for i in li]
		li = soup.find(class_='tags')
		a = str(li).split('dt>')
		b = (a[1].replace('</', ''), a[2].count('</dd>'))
		c = (a[3].replace('</', ''), a[4].count('</dd>'))
		date = (b, c)
		# print(date)
		return (date, list)
	return (num, list, name)


def get_2(way='page', n_=1, tag=None):
	#	if not tag:
	#		date=get_(way,n_)
	#	else:
	#		date=get_(tag=tag)
	date = get_(way, n_) if not tag else get_(tag=tag)
	if date:
		num, list, name = date
		if int(num) <= 10:
			print('正在获取网址，请耐心等待')
			for i in range(2, 1 + int(num)):
				#				if not tag:
				#					num,li,na=get_(way,i)
				#				else:
				#					num,li,na=get_(num=i,tag=tag)
				num, li, na = get_(way, i) if not tag else get_(num=i, tag=tag)
				list += li
				name += na
				return (1, list, name)
		return (num, list, name)


def all_page(way='page', tag=None):
	def main_(n_=1):
		num, list, name = get_2(way, n_, tag)
		n = 0
		#		print(list)
		print('*' * 20)
		print('     共有{}个项目'.format(str(len(list))))
		print('*' * 20)
		for i in list:
			print('-' * 10 + '分割线' + '-' * 10)
			print('编号为:' + str(i))
			print('名字为:' + name[n])
			print('-开始下载-')
			get_pic(i)
			n += 1
		return True if int(num) != n_ else None

	n = 1
	while True:
		if main_(n):
			n += 1
		else:
			break


# 主页面的

def hot_page():
	all_page('hot')


#	date=get_2('hot')
# 最新的


def recommend_page():
	all_page('best')


#	date=get_2('best')
# 推荐的

def zhuanti_page():
	def print_fox(data=None, way=0):
		x = PrettyTable(['编号', '标题名称' if not way else '妹子名字'])
		n = 1
		for i in data:
			x.add_row([str(n), i[1]])
			n += 1
		print(x)
		return n

	date = get_('zhuanti')
	if date:
		num, list = date
		list = [(num[0][0], list[:int(num[0][-1])]), (num[1][0], list[int(num[0][-1]):])]
		#	print(list)
		print('查看标签/1   人物/2')
		n = chi(1, 2) - 1
		# print(list[n][-1])
		n_ = print_fox(list[n][-1], n)
		print('输入图集编号')
		cho = chi(next=n_)
		print('选择了:第{}个，名字为:{}'.format(str(cho), list[n][-1][cho - 1][1]))
		url = list[n][-1][cho - 1][0]
		# print(url)
		num, list, name = all_page(tag=url)


# zhuanti_page()


def chi(first=1, next=4):
	try:
		n = int(input('请输入:'))
		if first <= n <= next:
			return n
		print('输入应该在{}~{}中'.format(str(first), str(next)))
		return chi(first, next)
	except ValueError:
		print('请输入数字')
		return chi(first, next)


def get_pic(num=1, p=1):
	url = 'https://www.mzitu.com/'
	# num=1
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
		"Referer": "https://www.mzitu.com/"}
	r = req(url + str(num), headers=headers)
	r.encoding = 'utf_8'
	soup = BeautifulSoup(r.text, features='html.parser')
	# print(soup)
	if soup.find('title').get_text().find('404') != -1:
		return
	d = soup.find(class_='pagenavi').find_all('a')[-2]
	num = d.find('span').get_text()
	if p == 1:
		print('检测到:一共有{}页'.format(str(num)))
	#	web=''
	#	for i in d['href'].split('/')[:-1]:
	#		web+=i+'/'
	web = '/'.join(d['href'].split('/')[:-1]) + '/'
	#	print(web)

	list = [(web + str(n), n) for n in range(1, int(num) + 1)]
	# print(num,list)
	info = soup.find('p').find('a').find('img')
	name, url = info.get('alt'), info.get('src')

	'''
	web,num = list[0]
	print(web,num)
	d=requests.get(web,headers=headers)
	print(d.text)
	'''

	for web, num in list:
		if os.path.isdir(name) != True:
			os.makedirs(name)
		#	print(web)
		r = req(web, headers)
		soup = BeautifulSoup(r.text, features='html.parser')
		url = soup.find('p').find('a').find('img').get('src')
		p = req(url, headers=headers)
		na = '{}/{}.jpg'.format(name, str(num))
		with open(na, 'wb')as f_p:
			f_p.write(p.content)
		print(num)
		time.sleep(.5)


def req(url, headers):
	try:
		return requests.get(url, headers=headers)
	except requests.exceptions.ConnectionError as e:
		# print(e)
		time.sleep(1)
		return req(url, headers)


# get_pic(i)

'''
for i in zhuanti_page():
	print('---------'+str(i))
	get_pic(i)
'''

if __name__ == '__main__':
	print('说明:1/主菜单 2/最新的 3/推荐的 4/一个大分类')
	n = chi()
	try:
		if n == 1:
			all_page()
		elif n == 2:
			hot_page()
		elif n == 3:
			recommend_page()
		elif n == 4:
			zhuanti_page()
	except BaseException as e:
		print(e)
	print('二十秒钟过后自动关闭')
	time.sleep(20)
