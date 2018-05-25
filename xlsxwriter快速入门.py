# _*_ coding:utf-8 _*_

"""
 @Author: liupu
 @File: xlsxwriter01.py
 @Date:2018-05-25 晚上10:30
"""

'''
xlsxwriter快速入门程序
'''

# ===============日常开支01Excel表格的创建======================== #

import xlsxwriter  # 导入xlsxwriter库

# 创建一个工作簿与工作表
workbook = xlsxwriter.Workbook('日常开支01.xlsx')
worksheet = workbook.add_worksheet('月度日常开支')

# 需要写入的费用数据
expenses = (
    ['房租',2300,'广州房价真坑'],
    ['水电费',200,'广州天气太热'],
    ['食品消费',2000,'蛮节省的嘛'],
    ['文娱消费',1000,'能不能少去几次影院'],
    ['阅读',200,'书籍是进步的阶梯'],
)

# 开始写入数据，首先写入标题行
worksheet.write(0,0,'开支项目')
worksheet.write(0,1,'费用')
worksheet.write(0,2,'备注')

# 循环写入具体内容
row = 1
col = 0
for item,cost,demo in (expenses):
    worksheet.write(row,col,item)
    worksheet.write(row,col + 1,cost)
    worksheet.write(row,col + 2,demo)
    row += 1

# 加入一行汇总行
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B2:B6)')
worksheet.write(row,2,'——')

workbook.close() # 关闭工作簿


# ===============日常开支02Excel表格的创建======================== #

import xlsxwriter  # 导入xlsxwriter库

# 创建一个工作簿与工作表
workbook = xlsxwriter.Workbook('日常开支02.xlsx')
worksheet = workbook.add_worksheet('月度日常开支')

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Add a number format for cells with money.
money = workbook.add_format({'num_format': '￥###0'})

# 需要写入的费用数据
expenses = (
    ['房租',2300,'广州房价真坑'],
    ['水电费',200,'广州天气太热'],
    ['食品消费',2000,'蛮节省的嘛'],
    ['文娱消费',1000,'能不能少去几次影院'],
    ['阅读',200,'书籍是进步的阶梯'],
)

# 开始写入数据，首先写入标题行
worksheet.write(0,0,'开支项目',bold)
worksheet.write(0,1,'费用',bold)
worksheet.write(0,2,'备注',bold)

# 循环写入具体内容
row = 1
col = 0
for item,cost,demo in (expenses):
    worksheet.write(row,col,item)
    worksheet.write(row,col + 1,cost,money)
    worksheet.write(row,col + 2,demo)
    row += 1

# 加入一行汇总行
worksheet.write(row, 0, 'Total',bold)
worksheet.write(row, 1, '=SUM(B2:B6)',money)
worksheet.write(row,2,'——',bold)

workbook.close() # 关闭工作簿


# ===============日常开支03Excel表格的创建======================== #

from datetime import datetime
import xlsxwriter

# 创建工作簿和工作表
workbook = xlsxwriter.Workbook('日常开支03.xlsx')
worksheet = workbook.add_worksheet('月度日常开支')

# 加粗格式设置
bold = workbook.add_format({'bold': 1})

# 增加￥符号设置
money = workbook.add_format({'num_format': '￥###0'})

# 增加日期设置格式
date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})

# 调整列宽
worksheet.set_column(2, 2, 20)
worksheet.set_column(3, 3, 10)

# 写入标题行
worksheet.write('A1', '开支项目', bold)
worksheet.write('B1', '费用', bold)
worksheet.write('C1', '备注', bold)
worksheet.write('D1', '日期', bold)

# 表格内容
expenses = (
    ['房租',2300,'广州房价真坑','2018-05-01'],
    ['水电费',200,'广州天气太热','2018-05-05'],
    ['食品消费',2000,'蛮节省的嘛','2018-04-16'],
    ['文娱消费',1000,'能不能少去几次影院','2018-04-09'],
    ['阅读',200,'书籍是进步的阶梯','2018-04-26'],
)

# 写入单元格内容
row = 1
col = 0
for item,cost,demo,date_str in (expenses):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    worksheet.write_string(row, col, item)
    worksheet.write_number(row, col + 1, cost, money)
    worksheet.write_string(row, col + 2, demo)
    worksheet.write_datetime(row, col + 3, date, date_format)
    row += 1

# 写入汇总行
worksheet.write(row, 0, '总计', bold)
worksheet.write(row, 1, '=SUM(B2:B6)', money)

workbook.close() # 关闭工作簿