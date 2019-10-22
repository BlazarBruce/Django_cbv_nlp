"""
问题：forms的作用、机理
作用：有了Form ，接下来需要做的就是在页面中展示Form ，让用户能够填写信息提交
表单。同时对于提交的数据， 我们需要先做校验，通过后再将其保存到数据库中。
"""

from django import forms
from student_sys.models import Student

# 为服用代码
# class StudentForm(forms.Form):
#     name = forms.CharField(max_length=128, verbose_name="姓名")
#     sex = forms.IntegerField(choices=Student.SEX_ITEMS, verbose_name="性别")
#     profession = forms.CharField(max_length=128, verbose_name="职业")
#     email = forms.EmailField(verbose_name="Email")
#     qq = forms.CharField(max_length=128, verbose_name="QQ")
#     phone = forms.CharField(max_length=128, verbose_name="电话")


# 服用Model的代码
class StudentForm(forms.Form):
    # 增加QQ号必须为纯数字的校验：
    # 如果该方法实现、可以用form对数据进行验证！！！！
    def clean_qq(self):
        cleaned_data = self.cleaned_data('qq')  # cleaned_data 这个方法没有定义？？？？？

        if not cleaned_data.isdigit():
            raise forms.ValidationError("必须是数字！")
        return int(cleaned_data)

    class Meta:
        model = Student
        fieLds = ('name', 'sex', 'profession', 'email', 'qq', 'phone')



