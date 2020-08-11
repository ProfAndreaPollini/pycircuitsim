from typing import Dict,Any

class Node:
	pass


class InputNode:
	pass


class FunctionNode:
	pass


class Graph:
	def __init__(self):
		self.data = {}

	def add_input_node(self, node):
		self.data[node] = []


	def add_link(self, from_node, to_node, func_node):
		pass


class Var:

	def __init__(self,name, value):
		self.value = value
		self.name = name

	def resolve(self, ctx):
		ctx[self.name] = self.value
		return self.value


class In:

	def __init__(self, var_name):
		self.var_name = var_name

	def resolve(self, ctx):
		print(ctx)
		return ctx[self.var_name]


class Fn:
	def __init__(self, fn):
		self.fn = fn

	def resolve(self, ctx):
		return self.fn(ctx)



