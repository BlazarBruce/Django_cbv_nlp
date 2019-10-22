from django.db import models

class Student(models.Model):
    SEX_ITEMS = [
        (1, '男'),
        (2, '女'),
        (0, '未知'),
    ]
    STATUS_ITEMS = [
        (0, '申请'),
        (1, '通过'),
        (2, '拒绝'),
    ]

    name = models.CharField(max_length=128, verbose_name="姓名")
    sex = models.IntegerField(choices=SEX_ITEMS, verbose_name="性别")
    profession = models.CharField(max_length=128, verbose_name="职业")
    email = models.EmailField(verbose_name="Email")
    qq = models.CharField(max_length=128, verbose_name="QQ")
    phone = models.CharField(max_length=128, verbose_name="电话")
    status = models.IntegerField(choices=STATUS_ITEMS, default=0,  verbose_name="审核状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        # 重新定义表名.
        db_table = 'student_info'

    def __str__(self):
        """将类对象转化为方便阅读的字符串"""
        return '<Student: {}>'.format(self.name)

    @property
    def sex_show(self):
        """此处用于单元测试练习"""
        return dict(self.SEX_ITEMS)[self.sex]

    # 获取所有书聚德类方法
    @classmethod
    def get_all(cls):
        """
        说明：获取所有书聚德类方法
        作用：这样后期再修改需求时，只需要修改get_all这个函数即可，改动的影响范围就小了很多
        功能：返回数据库中的所有数据
        优势：可以把数据获取逻辑封装到Model 层中，对上暴露更语义化的接口。
        """
        return cls.objects.all()



