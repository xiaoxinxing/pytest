from urllib import request
from bs4 import BeautifulSoup
import mysql.connector
import time
import datetime

url = 'http://www.1tu.com'

t = time.time()

def saveData(imgurl,descs):

	db = mysql.connector.connect(user='root', password='root', database='python' )
	t = time.time()
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()

	# # SQL 插入语句
	# sql = """INSERT INTO img_log(img_url, create_time, desc_text)
	#          VALUES (imgurl, t, descs)"""
	try:
	   # 执行sql语句
	   cursor.execute('insert into img_log(img_url, create_time, desc_text) '
                   'values(%s, %s, %s)',[imgurl,t,descs] )
	   # 提交到数据库执行
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()

	# 关闭数据库连接
	db.close()
	# print(div_photo)
 
req = request.Request('http://www.1tu.com/search/result-2a50cc872494d87209756a3ad061131c-1.html')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0')
with request.urlopen(req) as f:
    # print('Status:', f.status, f.reason)
    soup = BeautifulSoup(f.read().decode('utf-8'))

div_photo = soup.findAll("div", class_="photo")
# with open('E:/Python/test.html', 'w') as f:
#     f.write(str(div_photo))


# descurl = request.Request(url + '/photo-3078522246.html')
# descurl.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0')
# with request.urlopen(descurl) as f:
#     soup_desc = BeautifulSoup(f.read().decode('utf-8'))


# with open('E:/Python/desc.html', 'w') as f:
#     f.write(str(desc_all))
# print(soup_desc)    

for div_tip in div_photo:
	if(div_tip.find("div",class_="flag")):
		continue
	# print(div_tip.find("div",class_="flag"))
	
	img_photo = div_tip.find("img").get('src')
	a_src = div_tip.find("img").previous_element.previous_element
	# print(img_photo)
	# print(a_src.get('href'))
	descurl = request.Request(url + a_src.get('href'))
	descurl.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0')
	with request.urlopen(descurl) as b:
		soup_desc = BeautifulSoup(b.read().decode('utf-8'))

	desc_all = soup_desc.find('ul',id="zh-kw").findAll('li')
	descAll = ''
	for descs in desc_all:
		descAll += descs.get_text()+','
	saveData(img_photo,descAll)
	
