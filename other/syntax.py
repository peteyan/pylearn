#coding:utf-8

"""
filter(function, sequence)
对sequence中的item依次执行function(item)，将执行结果为True的item组成一个List/String/Tuple（取决于sequence的类型）返回
"""
def f(x):
	return x > 10  #返回条件  True / False

filter(f,range(2,25))  #@[11, 12, ... 23, 24]

	
"""
map(function, sequence) ：对sequence中的item依次执行function(item)，见执行结果组成一个List返回：
另外map也支持多个sequence，这就要求function也支持相应数量的参数输入：
"""
def cube(x):
	return x*x*x 
	
map(cube, range(1, 11)) 

def add(x, y): 
	return x+y 
map(add, range(8), range(8)) 

"""
reduce(function, sequence, starting_value)：对sequence中的item顺序迭代调用function，如果有starting_value，还可以作为初始值调用，例如可以用来对List求和：
"""

def add(x,y):
	return x + y 
reduce(add, range(1, 11)) #55 （注：1+2+3+4+5+6+7+8+9+10）
reduce(add, range(1, 11), 20) #75 （注：20+1+2+3+4+5+6+7+8+9+10）



"""
lambda  注意def是语句而lambda是表达式

(lambda x: x * 2)(3) 
g = lambda x: x * 2 
g(3) 

下面这种情况下就只能用lambda而不能用def
[(lambda x:x*x)(x) for x in range(1,11)]
map，reduce，filter中的function都可以用lambda表达式来生成！
map(lambda x:x*x,range(1,5))
filter(lambda x:x%2!=0,range(1,11))
reduce(lambda x,y:x+y,range(1,11))
"""