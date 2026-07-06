#!/usr/bin/python3

# class MyClass:
#     """一个简单的类实例"""
#     i = 12345
#     def f(self):
#         return 'hello world'
 
# # 实例化类
# x = MyClass()
 
# # 访问类的属性和方法
# print("MyClass 类的属性 i 为：", x.i)
# print("MyClass 类的方法 f 输出为：", x.f())


# class Complex:
#     def __init__(self, realpart, imagpart):
#         self.r = realpart
#         self.i = imagpart
# x = Complex(3.0, -4.5)
# print(x.r, x.i)   # 输出结果：3.0 -4.5


# class Test:
#     def prt(self):
#         print(self)
#         print(self.__class__)
 
# t = Test()
# t.prt()


# class MyClass:
#     def __init__(haha, value):
#         haha.value = value

#     def display_value(a):
#         print(a.value)

# # 创建一个类的实例
# obj = MyClass(42) 

# # 调用实例的方法
# obj.display_value() # 输出 42


# #类定义
# class people:
#     #定义基本属性
#     # name = ''
#     # age = 0
#     #定义私有属性,私有属性在类外部无法直接进行访问
#     # __weight = 0
#     #定义构造方法
#     def __init__(self,n,a,w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#     def speak(self):
#         print("%s 说: 我 %d 岁 %dkg。" %(self.name,self.age,self.__weight))
 
# # 实例化类
# p = people('runoob',10,30)
# p.speak()


# #类定义
# class people:
#     #定义基本属性
#     name = ''
#     age = 0
#     #定义私有属性,私有属性在类外部无法直接进行访问
#     __weight = 0
#     #定义构造方法
#     def __init__(self,n,a,w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#     def speak(self):
#         print("%s 说: 我 %d 岁。" %(self.name,self.age))
 
# #单继承示例
# class student(people):
#     grade = ''
#     def __init__(self,n,a,w,g):
#         #调用父类的构函
#         people.__init__(self,n,a,w)
#         self.grade = g
#     #覆写父类的方法
#     def speak(self):
#         print("%s 说: 我 %d 岁了，我在读 %d 年级"%(self.name,self.age,self.grade))
 
# s = student('ken',10,60,3)
# s.speak()


# #类定义
# class people:
#     #定义基本属性
#     name = ''
#     age = 0
#     #定义私有属性,私有属性在类外部无法直接进行访问
#     __weight = 0
#     #定义构造方法
#     def __init__(self,n,a,w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#     def speak(self):
#         print("%s 说: 我 %d 岁。" %(self.name,self.age))
 
# #单继承示例
# class student(people):
#     grade = ''
#     def __init__(self,n,a,w,g):
#         #调用父类的构函
#         people.__init__(self,n,a,w)
#         self.grade = g
#     #覆写父类的方法
#     def speak(self):
#         print("%s 说: 我 %d 岁了，我在读 %d 年级"%(self.name,self.age,self.grade))
 
# #另一个类，多继承之前的准备
# class speaker():
#     topic = ''
#     name = ''
#     def __init__(self,n,t):
#         self.name = n
#         self.topic = t
#     def speak(self):
#         print("我叫 %s，我是一个演说家，我演讲的主题是 %s"%(self.name,self.topic))
 
# #多继承
# class sample(speaker,student):
#     a =''
#     def __init__(self,n,a,w,g,t):
#         student.__init__(self,n,a,w,g)
#         speaker.__init__(self,n,t)
 
# test = sample("Tim",25,80,4,"Python")
# test.speak()   #方法名同，默认调用的是在括号中参数位置排前父类的方法


x = "全局变量"

def outer_function():
    x = "外层局部变量"
    
    def inner_function():
        nonlocal x
        x = "被修改的外层变量"
        print(f"内部函数访问: {x}")
        
    inner_function()
    print(f"外层函数访问: {x}")

def change_global():
    global x
    x = "全局变量已被函数修改"

# 执行观察效果
outer_function()
print(f"当前全局状态: {x}")
change_global()
print(f"调用 global 修改后: {x}")






















