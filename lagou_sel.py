from selenium import webdriver
import lxml
from lxml import etree
import time
import  re
import  json
import pymysql
drive_path=r'E:\chromedriver.exe'


# 连接MySQL数据库lagou
conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='lagou',charset='utf8')
cur=conn.cursor()



class LagouSprier(object):
	items=[]
	def __init__(self):
		self.positioneds=[]
		self.drive = webdriver.Chrome(executable_path=drive_path)
		
		#self.url='https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98?px=default&city=%E5%85%A8%E5%9B%BD#filterBox'
		#self.url='https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?px=default&city=%E5%8C%97%E4%BA%AC#filterBox'
		#self.url='https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput='

	def  run(self):
		for self.url in open('shujukaifa.txt'):
			time.sleep(3)
			self.url=str(self.url)
			print("输出url:",self.url)
			self.drive.get(self.url)
			while True:
				self.soursce=self.drive.page_source
				self.list_page(self.soursce)
				nex_bt=self.drive.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
				if 'pager_next pager_next_disabled' in nex_bt.get_attribute('class'):
					#json.dump(self.positioneds)
					break
				else:
					nex_bt.click()
					time.sleep(5)
					print("点击下一面")

	def list_page(self, source):                         #解析一面的url
		print("页面在解析")
		html = etree.HTML(source)
		links = html.xpath('//a[@class="position_link"]/@href')
		for link in links:
			print(link)
			#self.drive.get(link)
			self.drive.execute_script("window.open('%s')" %link)
			self.drive.switch_to_window(self.drive.window_handles[1])
			self.parse_positioned(self.drive.page_source)
			time.sleep(1)
			self.drive.close()
			self.drive.switch_to_window(self.drive.window_handles[0])
			time.sleep(6)
	def parse_positioned(self,text):              #解析详情界面
		item=[]
		html = etree.HTML(text)
		
		#公司名称
		company1=html.xpath('//*[@id="job_company"]/dt/a/div/h2/em/text()')[0]
		company=company1.strip()
		print(company)
		
		#岗位名称
		jobname=html.xpath('/html/body/div[2]/div/div[1]/div/span/text()')[0]
		print(jobname)
		
		
		name = html.xpath("//div[@class='job-name']/div/text()")[0]
		#print(name)
		item.append(name)
		span = html.xpath("//dd[@class='job_request']//span")
		#薪水
		salary = span[0].xpath('.//text()')[0]
		#print(salary)
		item.append(salary)
		
		#工作城市
		city = span[1].xpath('.//text()')[0].strip()
		city = re.sub(r"[\s/]", '', city)
		#print(city)
		item.append(city)
		
		#工作年限
		workyear = span[2].xpath('.//text()')[0].strip()
		workyear = re.sub(r"[\s/]", '', workyear)
		#print(workyear)
		item.append(workyear)
		
		#学历要求
		edu = span[3].xpath('.//text()')[0].strip()
		edu = re.sub(r"[\s/]", '', edu)
		#print(edu)
		item.append(edu)
		
		#职位诱惑
		position= html.xpath('//*[@id="job_detail"]/dd[1]/p/text()')[0]
		
		li = html.xpath("//ul[@class='c_feature']//li")
		#公司规模
		scale=li[0].xpath('.//text()')[1].strip()
		
		#scale=html.xpath('//*[@id="job_company"]/dd/ul/li[3]/text()')
		print(scale)
		
		#公司领域
		domain=html.xpath('//*[@id="job_company"]/dd/ul/li[2]/text()')[1].strip()
		domain=li[1].xpath('.//text()')[1].strip()
		print(domain)
		
		#公司发展阶段
		#stage=html.xpath('//*[@id="job_company"]/dd/ul/li[2]/text()')[1].strip()
		stage=li[2].xpath('.//text()')[1].strip()
		
		#岗位诱惑
		desc = ''.join(html.xpath("//dd[@class='job_bt']//text()")).strip()
		#print(desc)
		item.append(desc)
		self.items.append(item)
		pos={
			'name':name,
			'salary':salary,
			'city':city,
			'workyear':workyear,
			'edu':edu,
			'desc':desc
		}
		
		if desc:
			print("true")
		else:
			print("flase")
			
			


		sql = "INSERT INTO dashuju VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(jobname,company,salary,city,workyear,edu,desc,position,scale,domain,stage,time.time())
		###插入数据
		try:
		   # 执行sql语句
		   cur.execute(sql)
		   # 执行sql语句
		   conn.commit()
		   print('数据插入成功')
		except:
		   # 发生错误时回滚
		   conn.rollback()
		   print('数据插入错误')
		   

		 
		#self.positioneds.append(pos)
		


	

#conn.close()		
def main():
	spider=LagouSprier()
	spider.run()

if __name__ == '__main__':
	print("123")
	main()
	print("123")