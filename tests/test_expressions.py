from pycircuitsim.utils.graph import In,Var, Fn 
from pycircuitsim.chip import Chip

def test_var_expression_node():
	ctx = {}
	v = Var('test', 3)
	assert v.resolve(ctx) == 3
	assert ctx == {'test':3}


def test_in_expression_node():
	ctx = {
		'a':1
	}

	in_node = In('a')
	assert in_node.resolve(ctx) == 1


def test_fn_expression_node():
	ctx = {
		'a':1
	}

	def add(add_ctx):
		a = In('a').resolve(add_ctx)
		out = Var('out_a', a+1)
		return out.resolve(ctx) 

	f_out = Fn(add)
	f_out.resolve(ctx)

	assert ctx['out_a'] == ctx['a'] + 1


def test_fn_expression_node_composition():
	ctx = {
		'a':1
	}

	def add(add_ctx):
		a = In('a').resolve(add_ctx)
		Var('a', a+1).resolve(add_ctx)
		return add_ctx

	def compose(f, g):
		return lambda x: f(g(x))

	f_out = Fn(compose(add, add))
	f_out.resolve(ctx)
	print(ctx)
	assert ctx['a'] == 3

def test_fn_expression_node_and_gate():
	ctx = {
		'a':1,
		'b':1
	}

	def f(f_ctx):
		a = In('a').resolve(f_ctx)
		b = In('b').resolve(f_ctx)
		out = 0
		if a and b:
			out = 1
		Var('out', out).resolve(f_ctx)

	f_add = Fn(f)

	f_add.resolve(ctx)

	assert ctx['out'] == 1


