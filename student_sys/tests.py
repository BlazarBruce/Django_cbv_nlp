"""
功能：
单元测试文件

用到的方法：
def setup (self)：用来初始化环境，包括创建初始化的数据，或者做一些其他准备工作。

def test_xxxx(self)：方法后面的xxxx 可以是任意东西。以test 开头的方法，会被认为是需要测试的方法，
跑测试时会被执行。每个需要被测试的方法是相互独立的。

def tearDown (self） ：跟setUp 相对，用来清理测试环境和测试数据。在Django 中，我们可以不关心这个。

测试位置：
1、models层测试
    这一层的测试主要保证数据的写入和查询是可用的，同时’也需要保证我们在Mode l 层所提供的方法是符合预期的。
2、views层测试
    这一层更多的是功能上的测试，也是我们重点关注的。功能可用是相当重要的事。很多时候，我们可能没有那么多时
    间来完成所有代码的单元测试，但无论如何， 要抽出时间来保证线上功能可用。虽然这事可以通过手动浏览器访问来
    测试（针对网页系统来说），但是如果你有几百个页面呢，打算如何下手？
    因此，我们需要自动化的逻辑，能够自动帮助我们运行系统，测试功能点。

问题：
测试文件怎么用？
"""
from django.test import TestCase, Client
from student_sys.models import Student

class StudentTestCase(TestCase):
    def setUp(self):
        """我们创建了一条数据用于测试"""
        Student.objects.create(
            name='BlazarBruce',
            sex=1,
            email='2950472980@qq.com',
            profession='程序员',
            qq='333344445555',
            phone='110',
        )

    def test_create_and_sex_show(self):
        """test_create_and_s ex_ show 用来测试数据创建以及sex 字段的正确展示"""
        Student.objects.create(
            name='chaoqiang',
            sex=1,
            email='spuerhero@dd.com',
            profession='程序员',
            qq='333344445555',
            phone='110',
        )
        self.assertEqual(Student.sex_show, '男', '性别字段内容和表示不一致')

    def test_filter(self):
        """test_filter 测试查询是否可用"""
        Student.objects.create(
            name='chaoqiang',
            sex=1,
            email='spuerhero@dd.com',
            profession='程序员',
            qq='333344445555',
            phone='110',
        )

        name= 'BlazarBruce'
        students = Student.objects.filter(name=name)
        self.assertEqual(students.count(), 1, '应该只存在一个名称为{}的记录'.format(name))

    def test_get_index(self):
        """测试首页的可用性"""
        client = Client()
        response = client.get('/student/')
        self.assertEqual(response.status_code, 200, 'status code must be 200 !')

    def test_post_student(self):
        """测试首页的可用性"""
        client = Client()
        data = dict(
            name='test_for_post',
            sex=1,
            email='spuerhero@dd.com',
            profession='程序员',
            qq='333344445555',
            phone='110',

        )
        response = client.post('/student/', data)
        self.assertEqual(response.status_code, 302, 'status code must be 302 !')

        response = client.get('/student/')
        self.assertEqual(b'test_for_post'in response.content, 'response.content must contain test_for_post !')



