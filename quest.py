#coding:utf-8

#--------------------
# 遇到的疑惑 - 解释
#--------------------
# ---------- 目录 -------------
"""
 继承Object和不继承的区别 
 外部访问私有变量
 __setattr__, __getattr__, __delattr__, __call__的作用
 
"""
# --------- end 目录 -----------








#  __setattr__, __getattr__, __delattr__, __call__的作用
# 参考 http://www.cnblogs.com/dkblog/archive/2011/03/10/1980557.html

"""
class storage(dict):
	#通过使用__setattr__, __getattr__, __delattr__
	#可以重写dict，使之通过“.”调用
	def __setattr__(self, key, value):
		self[key] = value
	def __getattr__ (self, key):
		try:
			return self[key]
		except KeyError, k:
			return None
	def __delattr__ (self, key):
		try:
			del self[key]
		except KeyError, k:
			return None

	# __call__方法用于实例自身的调用
	#达到()调用的效果
	def __call__ (self, key):
		try:
			return self[key]
		except KeyError, k:
			return None

s = storage()
s.name = "hello"#这是__setattr__起的作用
print s("name")#这是__call__起的作用
print s["name"]#dict默认行为
print s.name#这是__getattr__起的作用
del s.name#这是__delattr__起的作用
print s("name")
print s["name"]
print s.name 
"""




# 外部访问私有变量
# 参考 http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386820042500060e2921830a4adf94fb31bcea8d6f5c000

"""
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print '%s: %s' % (self.__name, self.__score)
		
>>> bart = Student('Bart Simpson', 98)
>>> bart.__name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute '__name'

>>> bart._Student__name  ##########  不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name
'Bart Simpson'
"""





# 继承Object和不继承的区别 
"""
从object派生的话就是new style class，不带object就是classic class。具体的区别建议你去python.org的文档中有专题介绍。new style class支持内置类型的派生，可以处理metaclass(元类)，还有property(属性)，总之是一些相对高级的特性，以后也许会全部使用new style class。

>>> class storage(dict):
...     def __call__(self,key):
...             try:
...                     return self[key]
...             except:
...                     return 'Not the key'
>>> s = storage()
>>> s.name='xx'   ##############
>>> s.name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'storage' object has no attribute 'name'

--------------------------------

--------------------------------
>>> class storage(object):
...     def __call__(self,key):
...             try:
...                     return self[key]
...             except:
...                     return 'No'
...
>>> s = storage()
>>> s.name='xx'  ###############
>>> s.name
'xx'

"""