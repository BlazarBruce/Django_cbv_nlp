"""
功能：后台管理文件
用户名：Bruce
邮件地址：2950472980@qq.com
密码：123
"""
from django.contrib import admin
from student_sys.models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'profession', 'email', 'qq', 'phone', 'status', 'created_time')
    list_filter = ('sex', 'status', 'created_time')
    search_fields = ('name','profession')
    fieldsets = (
        (None, {
            "fields":(
                'name',
                ('sex', 'profession'),
                ('email', 'qq', 'phone'),
                'status',
            )

        }),
    )

# 将 Student与StudentAdmin类注册到admin.site后台管理中
admin.site.register(Student, StudentAdmin)


