# _*_ coding:utf-8 _*_

'''
@Author: Liupu
@File: rentDataClearing.py
@date: 2018-05-31
'''

# ==================租金数据清洗================== #
'''
# 清洗规则
  == 1，剔除重复记录
  == 2，剔除不在本市范围内的数据
  == 3，将数据中的租金以及平米两列重新命名为套租金和面积
  == 4，删除多余列，保留id、来源、newcode、套租金、面积、户型
  == 5，删除户型中户型为0以及户型大于10的数据记录
  == 6，删除面积字段中面积小于20或者面积大于230的记录
  == 7，删除套租金字段中数值大约20000或者小于500的记录
  == 8，删除户型为1户且面积大于70的数据记录
  == 9，删除户型为2户且面积小于40或大于100的数据记录
  == 10，删除户型为3且面积小于50或大于150的数据记录
  == 11，删除户型为4且面积小于60或大于200的数据记录
  == 12，删除户型为5且面积小于70的数据记录
  == 13，删除户型为6且面积小于80的数据记录
  == 14，删除户型为7且面积小于80的数据记录
  == 15，删除户型为8且面积小于90的数据记录
  == 16，删除户型为9且面积小于90的数据记录
  == 17，删除其中单位面积租金过高和过低的数据记录(即去头去尾2%)
  == 18，删除单位面积租金超过均值两个标准差的记录
'''

# 导入numpy和pandas两个分析库
import numpy as np
import pandas as pd 

# 决定需要读取的excel文档
city = input("请输入你需要清洗的租金数据所属城市，佛山or广州：")

Rent = pd.read_excel(city + '.xlsx')

# 

Rent = Rent.drop_duplicates(subset=['来源','城市','newcode','楼盘名称','区县','商圈','物业类型','租金','平米','户型'])
GZ_district = ['天河','越秀','荔湾','海珠','白云','黄埔','萝岗','番禺','花都','南沙','增城','从化']
FS_district = ['禅城','南海','顺德','三水','高明']
if city == '广州':
	Rent = Rent[Rent['区县'].isin(GZ_district)]
else:
	Rent = Rent[Rent['区县'].isin(FS_district)]
Rent = Rent.rename(columns = {'租金':'套租金','平米':'面积'})
del Rent['时间'],Rent['城市'],Rent['区县'],Rent['物业类型'],Rent['商圈']
Rent.drop(Rent[np.logical_or(Rent.户型 == 0,Rent.户型 >= 10)].index,inplace = True)
Rent.drop(Rent[np.logical_or(Rent.面积 < 20,Rent.面积 > 230)].index,inplace = True)
Rent.drop(Rent[np.logical_or(Rent.套租金 < 500,Rent.套租金 > 20000)].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 1,Rent.面积 > 70)].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 2,np.logical_or(Rent.面积 < 40,Rent.面积 > 100))].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 3,np.logical_or(Rent.面积 < 50,Rent.面积 > 150))].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 4,np.logical_or(Rent.面积 < 60,Rent.面积 > 200))].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 5,Rent.面积 < 70)].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 6,Rent.面积 < 80)].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 7,Rent.面积 < 80)].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 8,Rent.面积 < 90)].index,inplace = True)
Rent.drop(Rent[np.logical_and(Rent.户型 == 9,Rent.面积 < 90)].index,inplace = True)

Rent['unitRent'] = Rent['套租金'] / Rent['面积']
qt02 = np.percentile(Rent.unitRent,2)
qt98 = np.percentile(Rent.unitRent,98)
Rent.drop(Rent[np.logical_or(Rent.unitRent <= qt02,Rent.unitRent >= qt98)].index,inplace = True)

Mean = np.mean(Rent.unitRent)
Std = np.std(Rent.unitRent) 
Lower = Mean - 2 * Std
Upper = Mean + 2 * Std 
Rent.drop(Rent[np.logical_or(Rent.unitRent <= Lower,Rent.unitRent >= Upper)].index,inplace = True)

del Rent['unitRent'],Rent['楼盘名称']

Rent.to_excel('清洗后' + city + '.xlsx',index = False)
