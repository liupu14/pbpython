# _*_ coding:utf-8 _*_

"""
@Author: liupu
@File: workbook.py
@Date: 2018-06-01
"""

'''
xlsxwriter中workbook命令介绍
'''

import xlsxwriter
workbook = xlsxwriter.Workbook('Workbook操作示例.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet('数据')
worksheet3 = workbook.add_chartsheet('图表') 
expenses = (['房租',2300],
            ['水电费',200],
            ['食品消费',2000],
            ['文娱消费',1000],
            ['阅读',200],
)
bold = workbook.add_format({'bold':True})
money = workbook.add_format({'num_format':'￥###0'})
worksheet1.write(0,0,'开支项目',bold)
worksheet1.write(0,1,'费用',bold)
row = 1
col = 0
for item,cost in (expenses):
    worksheet1.write(row,col,item)
    worksheet1.write(row,col + 1,cost,money)
    row += 1
worksheet1.write(row,0,'汇总',bold)
worksheet1.write(row,1,'=SUM(B2:B6)',money)

# 向数据工作表中添加数据
headings = ['Number', '柱状图1', '柱状图2']
data = [
[2, 3, 4, 5, 6, 7],
[10, 40, 50, 20, 10, 50],
[30, 60, 70, 50, 40, 30],
]
worksheet2.write_row('A1', headings, bold)
worksheet2.write_column('A2', data[0])
worksheet2.write_column('B2', data[1])
worksheet2.write_column('C2', data[2])

chart = workbook.add_chart({'type': 'bar'})
chart.add_series({
'name': '=数据!$B$1',
'categories': '=数据!$A$2:$A$7',
'values': '=数据!$B$2:$B$7',
})

chart.add_series({
'name': ['数据', 0, 2],
'categories': ['数据', 1, 0, 6, 0],
'values': ['数据', 1, 2, 6, 2],
})

chart.set_title ({'name': '柱状图'})
chart.set_x_axis({'name': '编号'})
chart.set_y_axis({'name': '值'})

chart.set_style(11)

worksheet3.set_chart(chart)
workbook.close()