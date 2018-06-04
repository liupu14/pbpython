# _*_ coding:utf-8 _*_ 

"""
@Author: liupu
@File: wechat_friends_heatmap.py
@Date: 2018-06-04
"""

"""
目的:绘制微信好友省分布的热地图
需要解决问题：
    1、怎么使用Python获取微信好友的相关信息
    2、怎么使用Python绘制热地图
    3、将微信好友的省分布信息融入到热地图中
问题解析：
    1、使用Python中的第三方库itchat可以获取微信好友的相关信息
    2、使用matplotlib中的basemap库可以绘制热地图
所需文件：
    中国各省省界的shape文件
"""

# =================导入相关的库================= #
import itchat
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib 
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
import re

# ===============获取微信好友信息============== #

itchat.login()  # 登录网页版微信，这条命令会弹出一个二维码，手机扫描后便会登录到网页版微信

friends = itchat.get_friends(update = True)  # 获取微信好友信息
df_friends = pd.DataFrame(friends)  # 将微信好友消息转为数据框形式
pro_friends = df_friends.loc[:,['NickName','Province']]  # 获取好友信息中的昵称与省份信息

summaryInfo = pro_friends.groupby(['Province'])['NickName'].agg({'人员数量': np.size}).reset_index()  # 按照省份对各省的好友人数进行汇总，并将其命名为人员数量
summaryInfo.sort_values(by = ['人员数量'],ascending = False,inplace=True)  # 按照人员数量对数据表进行排序

def province_split(item):
	result = []
	for ii in item:
		try:
			pattern = re.search("^[\u4e00-\u9fa5]{1,}",ii).group()
			result.append(pattern)
		except:
			continue
	return(result)

dome_friends = province_split(summaryInfo.Province.tolist())
dome_friends = summaryInfo.loc[summaryInfo.Province.isin(dome_friends),:]
foreign_friends = summaryInfo.loc[summaryInfo.Province.isin([ii for ii in summaryInfo.Province.tolist() if ii not in dome_friends.Province.tolist()]),:]

dome_friends['standardism'] =(dome_friends.人员数量 - dome_friends.人员数量.min()) /(dome_friends.人员数量.max() - dome_friends.人员数量.min())


def ProvinceName_correct(name_list):
    name = []
    for item in name_list:
        if item in ["内蒙古","西藏"]:
            item += "自治区"
        elif item == "宁夏":
            item += "回族自治区"
        elif item == "新疆":
            item += "维吾尔族自治区"
        elif item == "广西":
            item += "壮族自治区"
        elif item in ["香港","澳门","台湾"]:
            item += "特别行政区"
        elif item in ["北京","天津","重庆","上海"]:
            item += "市"
        else:
            item += "省"
        name.append(item)
    return(name)

dome_friends["Province"] = ProvinceName_correct(dome_friends["Province"])

province_data = pd.read_excel("Province.xlsx") 
dome_friends = dome_friends.merge(province_data.loc[:,["province","jingdu","weidu"]],how = "left",left_on = "Province",right_on = "province")


fig = plt.figure(figsize=(16,12))
ax  = fig.add_subplot(111)

basemap = Basemap(llcrnrlon= 75,llcrnrlat=10,urcrnrlon=150,urcrnrlat=55,projection='poly',lon_0 = 116.65,lat_0 = 40.02,ax = ax)
basemap.readshapefile(shapefile = "bou2_4p",name = "china")

heatmapData = pd.DataFrame(basemap.china_info)
heatmapData["NAME"] = heatmapData["NAME"].map(lambda x: x.decode("gbk") if len(x) != 0 else x)
#mapData["NAME"] = [i.decode("gbk") if len(i) !=0 else i for i in mapData["NAME"].tolist()]
heatmapData = heatmapData.merge(dome_friends,how = "left",left_on='NAME', right_on="Province")


###构建省份填充函数（按照各省好友人数比例）：
def plotProvince(row):
    mainColor = (250/256, 1/256, 1/256,row['standardism']);
    patches = []
    for info,shape in zip(heatmapData["NAME"].tolist(),basemap.china): 
        if info == row['Province']:
            patches.append(Polygon(xy = np.array(shape), closed=True))
    ax.add_collection(PatchCollection(patches,facecolor=mainColor,edgecolor=mainColor,linewidths=1.,zorder=2))

dome_friends.apply(lambda row: plotProvince(row), axis=1)


plt.axis("off")  #关闭坐标轴
plt.savefig("wechat_friends_heatmap.png") #保存图表到本地
plt.show()    #显示图表