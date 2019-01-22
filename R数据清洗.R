# 设置工作路径为ufo文件所在路径
setwd("C:/Users/Administrator/Desktop/")

# 加载相关的包
library(tidyverse)     # R语言中用于数据分析的综合包
library(lubridate)     # 用于处理日期数据以及进行日期数据转换
library(scales)        # 用于设置可视化过程中日期的显示格式

# 使用read.delim()读取ufo数据文件
ufo <- read.delim("ufo_awesome.tsv",               # 文件路径及名字，记得后缀
                  header = FALSE,                  # 数据文件没有标题行，所以这里使用FALSE
                  sep = "\t",                      # 指定分割符为制表符
                  stringsAsFactors = FALSE,        # 避免读取文件中将字符创转为因子
                  na.strings = "" )                # 将数据中的空值设置为R语言中的标准空值
    
# 将数据框转为另外一种更高效友好的数据形式tibble
ufo <- as.tibble(ufo)

# 命名各列
names(ufo) <- c("OccurDate","ReportDate","Location",
                "ShortDescription","Duration","LongDescription")   # R基础包中的命名方式
# tidyverse下的命名方式
## rename(ufo,"OccurDate"=V1,"ReportDate"=V2,"Location"=V3,
##         "ShortDescription"=V4,"Duration"=V5,"LongDescription"=V6)

# 剔除日期数据中不规则的行
good_rows <- ifelse(nchar(ufo$OccurDate) != 8 |
                      nchar(ufo$ReportDate) != 8,
                    FALSE,
                    TRUE)
ufo <- ufo[good_rows, ]

# 转换第一列和第二列为日期格式
ufo$OccurDate <- as.Date(ufo$OccurDate,format = "%Y%m%d")
ufo$ReportDate <- as.Date(ufo$ReportDate,format = "%Y%m%d")

# 获取城市和州分别存在City列和State列
split_city_state <- function(location)
{
  split_location <- tryCatch(strsplit(location, ",")[[1]],
                             error = function(e) return(c(NA, NA)))
  clean_location <- gsub("^ ","",split_location)
  if (length(clean_location) > 2)
  {
    return(c(NA,NA))
  }
  else
  {
    return(clean_location)
  }
}

city_state <- lapply(ufo$Location,split_city_state)
city_state_matrix <- do.call(rbind,city_state)
ufo$City <- city_state_matrix[,1]
ufo$State <- city_state_matrix[,2]

# 提取Duraton列中的时间数字
get_digit <- function(D)
{
  split_duration <- tryCatch(strsplit(D, ",")[[1]],
                             error = function(e) return(c(NA, NA)))
  clean_duration <- gsub("^ ","",split_duration)
  if (length(clean_duration) > 2)
  {
    return(c(NA,NA))
  }
  else
  {
    return(clean_duration)
  }
}

Time <- lapply(ufo$Duration,get_digit)
Time_matrix <- do.call(rbind,Time)
ufo$Dur <- Time_matrix[,1]

# 选择需要的列
ufo <- select(ufo,c("OccurDate","ReportDate","City","State","Dur","LongDescription"))

# 将Dur改名为Duration
ufo <- rename(ufo,"Duration"=Dur)

# 绘制ufo出现日期的直方图并保存
Hist <- ggplot(ufo,aes(x=OccurDate)) +
  geom_histogram() +
  scale_x_date(breaks = "50 years")

ggsave(plot = Hist,
       filename = "quick_hist.jpeg",
       height = 6,
       width = 8)
