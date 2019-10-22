"""
在python中方法名如果是__xxxx__()的，那么就有特殊的功能，因此叫做“魔法”方法当使用
print输出对象的时候，只要自己定义了__str__(self)方法，那么就会打印从在这个方法中
return的数据__str__方法需要返回一个字符串，当做这个对象的描写
"""

class Animal:
    def __init__(self, new_name, new_age):
        self.name = new_name
        self.age = new_age

    def __str__(self):
        # 返回值
        return "名字是:%s , 年龄是:%d" % (self.name, self.age)

    def eat(self):
        print("%s在吃...." % self.name)

    def drink(self):
        print("%s在喝..." % self.name)

    def introduce(self):
        print("名字是:%s, 年龄是:%d" % (self.name, self.age))


# 创建了一个对象
king = Animal("牛魔王", 28)
print(king)
king.drink()