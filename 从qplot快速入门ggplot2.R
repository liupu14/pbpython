# =============================从qplot快速入门ggplot2================================= #

# Author: Liupu
# date: 2018-05-29
# File: qplot.R

# ----------安装相关包-----------#
install.packages('ggplot2'，dependencies = TRUE)
install.packages('gridExtra'，dependencies = TRUE)

# ----------通用程序段导入-----------#
library(ggplot2)
library(gridExtra)
set.seed(1314)   # 设置随机数种子
dsmall <- diamonds[sample(nrow(diamonnds),100),] # 生成小数据集

# ----------qplot作图初瞰-----------#
# 分别绘制四个散点图，两个原数据，两个对数后
p1 <- qplot(carat,price,data = diamonds)
p2 <- qplot(log(carat),log(price),data = diamonds)
p3 <- qplot(carat,price,data = dsmall)
p4 <- qplot(log(carat),log(price),data = dsmall)
grid.arrange(p1,p2,p3,p4,nrow=2,ncol=2)  # 将绘制图形布置成两行两列

# 带格式的散点图绘制
p1 <- qplot(carat,price,data = dsmall,colour = color)
p2 <- qplot(carat,price,data = dsmall,shape = cut)
p3 <- qplot(carat,price,data = dsmall,size = price)
p4 <- qplot(carat,price,data = diamonds,alpha=I(1/200))
grid.arrange(p1,p2,p3,p4,nrow=2,ncol=2)

# ----------散点图和平滑线绘制------------- #
p1 <- qplot(carat,price,data = dsmall,geom = c('point','smooth'))
p2 <- qplot(carat,price,data = diamonds,geom = c('point','smooth'))
p3 <- qplot(carat,price,data = dsmall,geom = c('point','smooth'),span=0.2)
p4 <- qplot(carat,price,data = dsmall,geom = c('point','smooth'),span=1)
grid.arrange(p1,p2,p3,p4,nrow=2,ncol=2)

# ----------箱线图和扰动点图绘制------------- #
p1 <- qplot(color,price/carat,data = diamonds,geom = 'jitter')
p2 <- qplot(color,price/carat,data = diamonds,geom = 'boxplot')
p3 <- qplot(color,price/carat,data = diamonds,geom = 'jitter',alpha = I(1/50))
p4 <- qplot(color,price/carat,data = diamonds,geom = 'jitter',alpha = I(1/200))
grid.arrange(p1,p2,p3,p4,nrow=2,ncol=2)

# ----------直方图和密度曲线图绘制------------- #
p1 <- qplot(carat,data = diamonds,geom = 'histogram',binwidth = 0.2,xlim = c(0,3))
p2 <- qplot(carat,data = diamonds,geom = 'histogram',binwidth = 0.05,xlim = c(0,3))
p3 <- qplot(carat,data = diamonds,geom = 'density',adjust = 0.2,xlim = c(0,3))
p4 <- qplot(carat,data = diamonds,geom = 'density',adjust = 0.05,xlim = c(0,3))
grid.arrange(p1,p2,p3,p4,nrow=2,ncol=2)

# ----------条形图绘制------------- #
qplot(color,data = diamonds,geom = 'bar')

# ----------折线图和路径图绘制------------- #
p1 <- qplot(date,unemploy/pop,data = economics,geom = 'line')
p2 <- qplot(date,uempmed,data = economics,geom = 'line')
year = function(x) as.POSIXlt(x)$year + 1990
p3 <- qplot(unemploy/pop,uempmed,data = economics,geom = c('point','path'))
p4 <- qplot(unemploy/pop,uempmed,data = economics,geom = c('point','path'),colour = year(date))
grid.arrange(p1,p2,p3,p4,nrow=2,ncol=2)

# ----------分面图绘制------------- #
p1 <- qplot(carat,data = diamonds,facets = color ~.,geom = 'histogram' ,binwidth=0.1,xlim = c(0,3))
p2 <- qplot(carat,..density..,data = diamonds,facets = color ~.,geom = 'histogram' ,binwidth=0.1,xlim = c(0,3))
grid.arrange(p1,p2,nrow=1,ncol=2)

# ----------加入图表格式的图形绘制------------- #
qplot(carat,price,data = diamonds,xlab = 'Price($)',ylab = 'Weight(carats)',xlim = c(0,2),main = '钻石重量与价格关系图')