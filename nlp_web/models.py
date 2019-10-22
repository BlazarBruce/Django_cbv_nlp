from django.db import models
"""
模型文件：对数据库进行操作、有待改进
"""

# models 类的名称小写作为数据库表名的后缀、完整的表名为：app名_models类名小写（若重新定义表名这用定义的表名）
class Performance(models.Model):
    # 字段类型有问题
    start_time = models.CharField(u'开始时间', max_length=100,  default=0)  # start_time 是该字段的字段名
    stop_time = models.CharField(u'结束时间', max_length=100,   default=0)
    query_body = models.CharField(u'查询内容', max_length=100,  default='null')
    query_score = models.CharField(u'查询得分', max_length=10,  default='0.0')
    return_body = models.CharField(u'返回内容', max_length=100, default='null')
    check_tag = models.CharField(u'复检标志', max_length=10,    default='0')

    class Meta:
        # 重新定义表名.
        db_table = 'query_table'
