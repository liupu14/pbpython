# _*_ coding:utf-8 _*_
"""
    @Author: liupu
    @Filename: lianjia_zufang.py
    @Date: 2018-8-20
    @Description:
        # usage: 爬取链家网租房信息
        # platform: win7+python3+visual studio code
"""

# 导入关联库
import requests 
from bs4 import BeautifulSoup
import xlwings as xw 
import time

# 创建excel文件并设置标题行
wb = xw.Book()
sht = wb.sheets[0]
sht.range('A1').value = '房源名称'
sht.range('B1').value = '所在小区'
sht.range('C1').value = '所在商圈'
sht.range('D1').value = '区域'
sht.range('E1').value = '价格'
sht.range('F1').value = '面积'
sht.range('G1').value = '户型'
sht.range('H1').value = '地铁'
sht.range('I1').value = '经纪人'
sht.range('J1').value = '联系电话'

# 构造爬虫主函数
def get_html(url,pages):
    res = requests.get(url)
    bsobj = BeautifulSoup(res.text,'lxml')
    urls = bsobj.select('#house-lst > li > div.info-panel > h2 > a')
    location = 2
    for url in urls:
        url = url.get('href')
        get_info(url,location,page = pages)
        location += 1


# 构造爬取具体网页信息函数
def get_info(url,location,page = 0):
    res = requests.get(url)
    bsobj = BeautifulSoup(res.text,'lxml')
    title = bsobj.find('h1',{'class':'main'}).get_text()
    price = bsobj.find('span',{'class':'total'}).get_text()
    area = bsobj.find_all('p',{'class':'lf'})[0].get_text()[3:]
    house_type = bsobj.find_all('p',{'class','lf'})[1].get_text()[5:]
    metor = bsobj.find_all('p')[4].get_text()[3:]
    park = bsobj.find_all('p')[5].get_text().split('\n')[0][3:]
    distrinct = bsobj.find_all('p')[6].get_text().split(' ')[0][3:]
    bankuai = bsobj.find_all('p')[6].get_text().split(' ')[1]
    broker = bsobj.find('div', {'class': 'brokerName'}).get_text().split('\n')[1] if bsobj.find('div', {'class': 'brokerName'}) is not None else 0
    phone = bsobj.find('div', {'class': 'phone'}).get_text().strip().replace('\n', '').replace(' ', '') if bsobj.find('div', {'class': 'phone'}) is not None else 0
    sht.range(page * 30 + location, 1).value = title
    sht.range(page * 30 + location, 2).value = park
    sht.range(page * 30 + location, 3).value = bankuai
    sht.range(page * 30 + location, 4).value = distrinct
    sht.range(page * 30 + location, 5).value = price
    sht.range(page * 30 + location, 6).value = area
    sht.range(page * 30 + location, 7).value = house_type
    sht.range(page * 30 +location, 8).value = metor
    sht.range(page * 30 +location, 9).value = broker
    sht.range(page * 30 +location, 10).value = phone


# 运行程序
if __name__ == '__main__':
    urls = ['https://gz.lianjia.com/zufang/pg{}'.format(ii) for ii in range(1,101)]
    for ii,url in enumerate(urls):
        get_html(url,ii)
        time.sleep(1) 
    wb.save('lianjia_zufang.xlsx')
    wb.close()
