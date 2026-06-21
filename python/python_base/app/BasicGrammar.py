#!/usr/bin/python3
import inspect

############## Number ##########################
"""
class Animal:
    pass

class Dog(Animal):
    pass

my_dog = Dog()

# 1. 使用 type() 检查
print(f"type 检查: {type(my_dog) == Dog}")    # True (它是狗)
print(f"type 检查: {type(my_dog) == Animal}") # False (它不是原始的 Animal)

# 2. 使用 isinstance() 检查
print(f"isinstance 检查: {isinstance(my_dog, Dog)}")    # True (它是狗)
print(f"isinstance 检查: {isinstance(my_dog, Animal)}") # True (它也是动物，因为它继承
"""
################# String #######################
"""
my_str = 'Runoob'       # 定义一个字符串变量（避免使用 str 作为变量名，会覆盖内置类型）

print(my_str)           # 打印整个字符串：Runoob
print(my_str[0:-1])     # 打印索引 0 到倒数第二个字符（不含最后一个）：Runoo
print(my_str[0])        # 打印第一个字符：R
print(my_str[2:5])      # 打印索引 2、3、4 的字符（不含索引 5）：noo
print(my_str[2:])       # 打印从索引 2 开始到末尾：noob
print(my_str * 2)       # 重复打印两次：RunoobRunoob
print(my_str + "TEST")  # 字符串拼接：RunoobTEST
"""
################## bool ######################
"""
# 布尔类型的值和类型
a = True
b = False
print(type(a))  # <class 'bool'>
print(type(b))  # <class 'bool'>

# 布尔类型的整数表现
print(int(True))   # 1
print(int(False))  # 0

# 使用 bool() 函数进行转换
print(bool(0))          # False
print(bool(42))         # True
print(bool(''))         # False
print(bool('Python'))   # True
print(bool([]))         # False
print(bool([1, 2, 3]))  # True

# 布尔逻辑运算
print(True and False)  # False
print(True or False)   # True
print(not True)        # False

# 布尔比较运算
print(5 > 3)   # True
print(2 == 2)  # True
print(7 < 4)   # False

# 布尔值在控制流中的应用
if True:
    print("This will always print")

if not False:
    print("This will also always print")

x = 10
if x:
    print("x 是非零值，在布尔上下文中为 True")
"""
################## list ######################
"""
my_list = ['abcd', 786, 2.23, 'runoob', 70.2]  # 避免使用 list 作为变量名，会覆盖内置类型
tinylist = [123, 'runoob']

print(my_list)             # 打印整个列表：['abcd', 786, 2.23, 'runoob', 70.2]
print(my_list[0])          # 打印第一个元素（索引 0）：abcd
print(my_list[1:3])        # 打印索引 1 和 2 的元素（不含索引 3）：[786, 2.23]
print(my_list[2:])         # 打印从索引 2 开始到末尾的所有元素：[2.23, 'runoob', 70.2]
print(tinylist * 2)        # 重复打印 tinylist 两次：[123, 'runoob', 123, 'runoob']
print(my_list + tinylist)  # 拼接两个列表
"""
################## tuple ######################
"""
my_tuple = ('abcd', 786, 2.23, 'runoob', 70.2)  # 避免使用 tuple 作为变量名
tinytuple = (123, 'runoob')

print(my_tuple)               # 输出完整元组
print(my_tuple[0])            # 输出第一个元素：abcd
print(my_tuple[1:3])          # 输出索引 1 和 2 的元素：(786, 2.23)
print(my_tuple[2:])           # 输出从索引 2 开始的所有元素
print(tinytuple * 2)          # 输出两次 tinytuple
print(my_tuple + tinytuple)   # 连接两个元组

tup1 = ()    # 空元组
tup2 = (20,) # 一个元素，需要在元素后添加逗号
not_a_tuple = (42)  # 这是整数 42，不是元组
"""
################## set ######################
"""
sites = {'Google', 'Taobao', 'Runoob', 'Facebook', 'Zhihu', 'Baidu'}

print(sites)   # 输出集合（无序，重复元素会被自动去掉）

# 成员测试
if 'Runoob' in sites:
    print('Runoob 在集合中')
else:
    print('Runoob 不在集合中')

# set 可以进行集合运算
a = set('abracadabra')
b = set('alacazam')

print(a)           # a 中的唯一字符

print(a - b)       # a 和 b 的差集（在 a 中但不在 b 中）
print(a | b)       # a 和 b 的并集（在 a 或 b 中）
print(a & b)       # a 和 b 的交集（同时在 a 和 b 中）
print(a ^ b)       # a 和 b 的对称差集（在 a 或 b 中，但不同时存在）
"""
################## dict ######################
"""
my_dict = {}
my_dict['one'] = "教程"
my_dict[2]     = "工具"

tinydict = {'name': 'runoob', 'code': 1, 'site': 'www.runoob.com'}

print(my_dict['one'])       # 输出键为 'one' 的值
print(my_dict[2])           # 输出键为 2 的值
print(tinydict)             # 输出完整的字典
print(tinydict.keys())      # 输出所有键
print(tinydict.values())    # 输出所有值
"""
################## Docstring  ######################

# def add(a, b):
#     """返回两数之和"""
#     return a + b

# # 通过 __doc__ 属性访问
# print(add.__doc__)  # 输出: 返回两数之和

# help(add)

# # 使用 inspect.getdoc() 获取文档
# print(inspect.getdoc(add))  # 输出: 返回两数之和


# def calculate(a, b, operation="add"):
#     """
#     执行数学运算

#     参数:
#         a: 第一个数字
#         b: 第二个数字
#         operation: 操作类型，可选 "add", "subtract", "multiply"

#     返回:
#         计算结果
#     """
#     if operation == "add":
#         return a + b
#     elif operation == "subtract":
#         return a - b
#     elif operation == "multiply":
#         return a * b
#     else:
#         raise ValueError("不支持的操作")

# # 查看完整文档
# help(calculate)


class Person:
    """人物类，用于表示一个人的基本信息"""

    def __init__(self, name, age):
        """
        初始化人物对象

        参数:
            name: 姓名
            age: 年龄
        """
        self.name = name
        self.age = age

    def introduce(self):
        """介绍这个人"""
        return f"我叫{self.name}，今年{self.age}岁"

# 访问类的文档
print(Person.__doc__)

# 访问方法的文档
print(Person.introduce.__doc__)











