# _*_ coding:utf-8 _*_
"""
    @Author: liupu
    @filename: top500_music
    @date: 2018-8-13
    # Description:
        # usege: 爬取酷狗音乐Top500排行榜，并将其存放进excel文件中
        # 平台：Windows7 + Python3.6 + ipython/visual studio code
        # 基本库需求：requests,Beautifulsoup,xlwings
"""

# 导入相关的库
import requests
from bs4 import BeautifulSoup
import xlwings as xw 
import time

# 创建一个excel文件，便于后面存放歌曲信息
wb = xw.Book()
sht = wb.sheets[0]
sht.range('A1').value = [['排名','歌曲名称','歌手','播放时间']]     # 设置标题行

# 定义爬虫函数
def get_info(url):
    res = requests.get(url)
    bsobj = BeautifulSoup(res.text,'lxml')
    ranks = bsobj.select(
        '#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_num')
    titles = bsobj.select(
        '#rankWrap > div.pc_temp_songlist > ul > li > a')
    play_times = bsobj.select(
        '#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')
    for rank,title,play_time in zip(ranks,titles,play_times):
        rank = int(rank.get_text().strip())
        music = title.get_text().split('-')[1]
        singer = title.get_text().split('-')[0]
        play_time = play_time.get_text().strip()
        sht.range((rank+1,1)).value = rank
        sht.range((rank+1,2)).value = music
        sht.range((rank+1,3)).value = singer
        sht.range((rank+1,4)).value = play_time


if __name__ == '__main__':
    urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(str(ii)) for ii in range(1,25)]
    for url in urls:
        get_info(url)
        time.sleep(2)
    wb.save('top_500.xlsx')
    wb.close()


