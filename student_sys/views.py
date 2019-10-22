"""
问题：
前后端通信的实现方式：
1、后端向前端传递数据
2、前端向后端提交数据

数据验证：
1、用Form对数据进行验证
2、用中间件对数据进行验证
3、前端对数据进行验证
"""
# 模块级别的双下划线命名
__all__ = ['index', 'IndexView']
__version__ = '0.1'
__author__ = 'Bruce'

from django.views import View
from django.http import HttpResponseRedirect  # 重定向
from django.shortcuts import render, HttpResponse, redirect  # 必会三件套
# 根据urls.py中的 url(r'^$', index, name='index'), name 找到对应的url
# 不需要硬编码URL 到代码中，这意味着如果以后有修改U虹的需求，只要index 的名称不变，这个地方的代码就不用改。
from django.urls import reverse

from student_sys.forms import StudentForm  # 导入处理学生信息的Form类
from student_sys.models import Student

# 基于FBV的View实现
def index(request):
    """
    技术细节说明：
    里面有一个form . cleaned_data 对象， 它是Form 根据字段类型对用户提交的数据做完
    转换之后的结果。另外，还用了reverse 方法。我们在urls.py 中定义index 的时候，声明了
    name＝'index'，所以这里可以通过reverse 来拿到对应的URL 。这么做的好处是，不需要硬
    编码URL 到代码中，这意味着如果以后有修改U虹的需求，只要index 的名称不变，这个地
    方的代码就不用改。
    """
    # 调用类中的类方法、对数据库进行查询、取出所有的数据
    students = Student.get_all()
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            # 第一次实现
            # cleaned_data = form.cleaned_data
            # student = Student()
            # student.name = cleaned_data('name')
            # student.sex = cleaned_data('sex')
            # student.email = cleaned_data('email')
            # student.profession = cleaned_data('profession')
            # student.qq = cleaned_data('qq')
            # student.phone = cleaned_data('phone')
            # student.save()

            # 第二次实现
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = StudentForm()

    context = {
        'students': students,
        'form': form
    }  # 字典、用于向前端传输局

    return render(request, 'index.html', context=context)  # 后端向前端传递数据的方式

# 基于CBV的View实现
class IndexView(View):

    template_name = 'index.html'

    def get_context(self):
        students = Student.get_all()
        context = {
            'students': students,
        }
        return context

    def get(self, request, *args, **kwargs):

        context = self.get_context()
        form = StudentForm()
        context.update({
            'form': form
        })

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form =StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))

        context = self.get_context()
        context.update({
            'form': form
        })

        return render(request, self.template_name, context=context)


