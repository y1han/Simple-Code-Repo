# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import xlwt
import urllib3
from signal import signal, SIGPIPE, SIG_DFL
import pandas as pd
urllib3.disable_warnings()
signal(SIGPIPE, SIG_DFL)

true = 'True'
false = 'False'
nan = 'NaN'

def get_html(keyword, shanghai_or_not, workyear, postdate, industry):
	k = 1 #参数k代表存储到excel的行数
	wb = xlwt.Workbook(encoding="utf-8")  # 创建工作簿
	f = wb.add_sheet('招聘信息', cell_overwrite_ok=True)  # 创建工作表
	'''
	下方的循环是将Excel表格中第一行固定
	'''
	raw = ['职位', '公司', '工作地点', '薪水', '发布日期', '含985_211要求', '含海外优先', '含全日制要求', '性质', '规模', '分类', '学历要求', '网址']
	for i in range(len(raw)):
		f.write(0, i, raw[i])
		'''
		write函数中第一个参数表示存储到多少行
		第二各参数存储到多少列表，第三个参数代表存储到对应行列的值
		'''
	url = 'http://search.51job.com/list/' + shanghai_or_not + ',000000,0000,' + industry + ',' + postdate + ',99,' + keyword + ',2,{}.html?' + 'workyear=' + workyear
	try:
		soup = soup_get(url.format(1))
		print(url.format(1))
		for page in range(int(soup.select(".dw_table .dw_tlc .rt")[1].get_text().split()[2])):#解析所有
			soup = soup_get(url.format(page + 1))
			t1 = soup.select('.t1 span a')
			t2 = soup.select('.t2 a')
			t3 = soup.select('.t3')
			t4 = soup.select('.t4')
			t5 = soup.select('.t5')
			for i in range(len(t2)):
				job = t1[i].get('title')#获取职位
				href = t1[i].get('href')#获取链接
				company = t2[i].get('title')#获取公司名
				location = t3[i+1].text#获取工作地点
				salary = t4[i+1].text#获取薪水
				date = t5[i+1].text#获取发布日期

				det_soup = soup_get(href)
				if det_soup.select(".com_tag p"):
					detail = det_soup.select(".com_tag p")
					properties = detail[0].get_text()
					scale = detail[1].get_text()
					classification = detail[2].get_text().split()
					requirement = det_soup.select(".ltype")[0].get_text().split()[4]
				else:
					properties = nan
					scale = nan
					classification = [nan]
					requirement = nan

				print(str(k) + " : " + job + " " + company + " " + location + " " + salary + " " + date + " " + href)
				f.write(k, 0 , job)
				f.write(k, 1 , company)
				f.write(k, 2 , location)
				f.write(k, 3 , salary)
				f.write(k, 4 , date)
				f.write(k, 5 , true_or_false(job, href, ['985', '211']))
				f.write(k, 6 , true_or_false(job, href, ['海外留学生', '海外经历']))
				f.write(k, 7 , true_or_false(job, href, ['全日制']))
				f.write(k, 8 , properties)
				f.write(k, 9 , scale)
				f.write(k, 10, " | ".join(classification))
				f.write(k, 11, requirement)
				f.write(k, 12, href)
				k += 1#每存储一行 k值加1
			file_name = keyword + '_' + shanghai_or_not + '_' + workyear
			wb.save(file_name + '.xls')#写完后掉用save方法进行保存
			xls = pd.read_excel(file_name + '.xls')
			xls.to_csv(file_name + '.csv', encoding='utf-8')

		print(k)
	except TimeoutError:
		print("请求失败")
		return  None

def true_or_false(job, sub_url, lookup_list):
	try:
		soup = soup_get(sub_url)
		if (soup.select(".job_msg")):
			msg = soup.select(".job_msg")[0].find_all('p', class_=lambda x: x != 'fp')
			for item in lookup_list:
				if item in job:
					return true
				for ls in msg:
					if item in ls.text:
						return true
			return false
		else :
			for item in lookup_list:
				if item in soup.text:
					return true
			return false
		return nan
		
	except TimeoutError:
		print("请求失败")
		return nan


def soup_get(url): 
	session = requests.Session()
	retry = Retry(connect=5, backoff_factor=0.5)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)

	res = session.get(url, stream=True)
	res.encoding = 'gbk'
	return BeautifulSoup(res.text, features="html.parser")


if __name__=='__main__':
	'''
		%2B 空白
		url_all = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=6&dibiaoid=0&address=&line=&specialarea=00&from='
		
		workyear 	=	99  所有
						01  无经验

		shanghai_or_not 	=	020000 上海
								000000 全国

		postdate 	=	9 所有
						0 24小时内
						1 近三天
						2 近一周
						3 近一个月

		industry 	=	03  金融/投资/证券
						01  计算机软件
						00	无限制

	'''
	keyword = '%2B'
	shanghai_or_not = '020000'
	workyear = '99'
	postdate = '3'
	industry = '01'

	get_html(keyword, shanghai_or_not, workyear, postdate, industry)