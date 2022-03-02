#!/usr/bin/python3
import time
from math import sin, cos
FUNCTIONS = {"logistic_map" : 1, "sincosine_map" : 1, "bogdanov_map" : 1}
BLOCK = 10
class Function():
	def __init__(self, params, variables):
		self.params = params
		self.variables = variables
	def compute(self):
		pass
	def update(self):
		pass
	def gen_sequence(self, n):
		lis = []
		for i in range(n):
			y = self.compute()
			s = str(y)
			lis.append(int(s[-1] + s[-2]))
			self.update()
		return lis
	def set_seed(self, l, r):
		t = time.time()
		frac = t - int(t)
		i = int(t) % r
		if i < l:
			i = l
		seed = i + frac
		return seed
	def gen_keys(self, q):
		keys = []
		for i in range(q):
			for p in self.params:
				if p:
					p[0] = self.set_seed(p[1], p[2])
			for v in self.variables:
				if v:
					v[0] = self.set_seed(v[1], v[2])
			
			keystream = self.gen_sequence(BLOCK)
			keys.append(keystream)
		return keys
		
class LogisticMap(Function):
	def __init__(self, params, variables):
    		super().__init__(params, variables) 
	def compute(self):
		beta = self.params[0][0]
		x = self.variables[0][0]
		return (beta + 1) * ((1 + 1/beta)**beta) * (x) * ((1 - x) ** beta) 
	def update(self):
		self.variables[0][0] = self.compute()

class SinCosineMap(Function):
	def __init__(self, params, variables):
		super().__init__(params, variables)
	def compute(self):
		x = self.variables[0][0]
		return (2*sin(3/x))+(3*cos(5/x))+(4*sin(6/x))+(1*cos(3/x))
	def update(self):
		x = self.variables[0]
		self.variables[0][0] = self.set_seed(x[1], x[2])

class BogdanovMap(Function):
	def __init__(self, params, variables):
		super().__init__(params, variables)
	def compute(self):
		y = self.variables[1]
		x = self.variables[0]
		e = self.params[0]
		k = self.params[1]
		m = self.params[2]
		r = y[0] + (e[0] * y[0]) + (k[0] * x[0] * (x[0] - 1)) + (m[0] * x[0] * y[0]) + x[0]
		return r
	def update(self):
		r = self.compute()
		self.variables[1][0] = r - self.variables[0][0]
		self.variables[0][0] = r
		
def create_logistic_map():
	params = [[1 , 1, 4]]
	variables = [[0, 0, 1]]
	logistic_map = LogisticMap(params, variables)
	return logistic_map

def create_sincosine_map():
	variables = [[0, -0.05, 0.05]]
	params = [[]]
	sincosine_map = SinCosineMap(params, variables)
	return sincosine_map

def create_bogdanov_map():
	params = [[1, 0, 1], [1,0, 1], [1,0, 1 ]]
	variables = [[0, -0.00001, 0.00001], [0, -0.00001, 0.00001]]
	bogdanov_map = BogdanovMap(params, variables)
	return bogdanov_map

def create_function(function_name):
	if function_name == "logistic_map":
		return create_logistic_map()
	elif function_name == "sincosine_map":
		return create_sincosine_map()
	elif function_name == "bogdanov_map":
		return create_bogdanov_map()
