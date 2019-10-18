"""
功能：天气业务支持

讯飞解析现状：
目前在数据库随机筛选300条话束
算上可接受的json、讯飞正确率可达到93.33%

天气业务解决思虑及关键点：
一：字符串地名提取——可以考虑调用实体提取
二; 字符串时间提取——比较复杂

需要解决的问题：
Q1：获取此时的日期
参考链接：https://www.cnblogs.com/general-seven/p/5893744.html

目前遇到的困难
困难一：话束中含有天气、丹玉天气查询无关或打开APP、例如“打开最美天气”、“今天天气真热”、“打开天气”、
“打开天气关闭天窗“

"""

import datetime

now_time = datetime.datetime.now()
print(now_time)
# 格式化日期
now_time = datetime.datetime.now().strftime('%Y-%m-%d')
print(now_time)



