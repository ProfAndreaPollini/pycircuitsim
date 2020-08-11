from pycircuitsim.utils.graph import Fn, Var
from itertools import product




class AndGate:

	def __init__(self):
		self.inPins = {'a': 0, 'b': 0}
		self.outPins = {'out': 0}

	def setInput(self, pin_name, value):
		self.inPins[pin_name] = value

	def getOutput(self, pin_name):
		return self.outPins[pin_name]

	def process(self):
		self.outPins['out'] = 0
		if self.inPins['a'] and self.inPins['b']:
			self.outPins['out'] = 1


class Chip:

	def __init__(self):
		super().__init__()
		self.ctx = {}  #??? serve?

		self.inPins = {}
		self.outPins = {}
		self.parts = {}

		self.wiring = None


	def pin(self, pin_name):
		if pin_name in self.inPins.keys():
			return self.inPins[pin_name]
		elif pin_name in self.outPins.keys():
			return self.outPins[pin_name]
		elif '.' in pin_name:  # if is requested a pin from a chip component, get it!
			fields = pin_name.split('.')
			if fields[0] in self.parts.keys():
				return self.parts[fields[0]].pin(fields[1])
		else:
			raise "Incorrect pin name"

	def set_pin(self, name, value):
		if name in self.inPins.keys():
			self.inPins[name] = value
		elif name in self.outPins.keys():
			self.outPins[name] = value
		elif '.' in name:  # if is requested a pin from a chip component, get it!
			fields = name.split('.')
			if fields[0] in self.parts.keys():
				return self.parts[fields[0]].set_pin(fields[1],value)
		else:
			raise "Incorrect pin name"

	def process(self):
		self.ctx = {}
		self.wiring.resolve(self.ctx)


class Not(Chip):
	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0}
		self.outPins = {'out': 0}
		def f(ctx):
			out = 0
			if self.pin('a') == 0:
				out = 1
			
			self.set_pin('out',out)
			return ctx

		self.wiring = Fn(f)


class Or(Chip):
	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0,'b': 0}
		self.outPins = {'out': 0}
		def f(ctx):
			out = 0
			if self.pin('a') or self.pin('b'):
				out = 1
			
			self.set_pin('out', out)
			return ctx

		self.wiring = Fn(f)

class And(Chip):
	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0,'b': 0}
		self.outPins = {'out': 0}
		def f(ctx):
			out = 0
			if self.pin('a') and self.pin('b'):
				out = 1
			
			self.set_pin('out', out)
			return ctx

		self.wiring = Fn(f)

class And3(Chip):
	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0,'b': 0, 'c': 0}
		self.outPins = {'out': 0}
		self.parts = {'and1': And(), 'and2': And()}
		def f(ctx):	
			self.parts['and1'].set_pin('a', self.pin('a'))
			self.parts['and1'].set_pin('b', self.pin('b'))
			self.parts['and1'].process()

			self.parts['and2'].set_pin('a', self.pin('c'))
			self.parts['and2'].set_pin('b', self.parts['and1'].pin('out'))
			self.parts['and2'].process()	
			self.set_pin('out', self.parts['and2'].pin('out'))
			return ctx

		self.wiring = Fn(f)	

class Nand(Chip):

	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0, 'b': 0}
		self.outPins = {'out': 0}
		self.parts = {'and': And(),'not': Not()}

		def f(ctx):
			a = self.pin('a')
			b = self.pin('b')
			self.set_pin('and.a', a)
			self.set_pin('and.b', b)
			and_out = self.pin('and.out')
			self.set_pin('not.a', and_out)
			self.set_pin('out', self.pin('not.out'))


		self.wiring = Fn(f)


class Xor(Chip):
	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0, 'b': 0}
		self.outPins = {'out': 0}
		self.parts = {'not1': Not(), 'not2': Not(), 'and1': And(), 'and2': And(), 'or': Or()}

		def f(ctx):
			a = self.pin('a')
			b = self.pin('b')
			
			self.set_pin('not1.a', a)
			self.set_pin('not2.a', b)
			self.parts['not1'].process()
			self.parts['not2'].process()
			nota = self.pin('not1.out')
			notb = self.pin('not2.out')

			self.set_pin('and1.a', a)
			self.set_pin('and1.b', notb)
			self.set_pin('and2.a', nota)
			self.set_pin('and2.b', b)
			self.parts['and1'].process()
			self.parts['and2'].process()

			self.set_pin('or.a', self.pin('and1.out'))
			self.set_pin('or.b', self.pin('and2.out'))
			self.parts['or'].process()

			self.set_pin('out', self.pin('or.out'))



		self.wiring = Fn(f)

class AndGate3(Chip):
	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0, 'b': 0, 'c': 0}
		self.outPins = {'out': 0}
		self.parts = {'and1': AndGate(), 'and2': AndGate()}

		def f(ctx):
			ctx['out1'] = self.pin('a') and self.pin('b')
			out = self.pin('c') and ctx['out1']
			self.set_pin('out',out)
			return ctx

		self.wiring = Fn(f)


class HalfAdder(Chip):
	def __init__(self):
		super().__init__()
		self.inPins = {'a': 0, 'b': 0}
		self.outPins = {'sum': 0, 'carry': 0}
		self.parts = {'and': And(), 'xor': Xor()}

		def f(ctx):
			a = self.pin('a')
			b = self.pin('b')
			
			self.set_pin('and.a', a)
			self.set_pin('and.b', b)
			self.parts['and'].process()
			self.set_pin('xor.a', a)
			self.set_pin('xor.b', b)
			self.parts['xor'].process()
			bitcarry = self.pin('and.out')
			bitsum = self.pin('xor.out')

			self.set_pin('sum', bitsum)
			self.set_pin('carry', bitcarry)
			
		self.wiring = Fn(f)

class MultiBitAnd(Chip):
	def __init__(self, n_bits=2):
		super().__init__()
		for bit in range(n_bits):
			self.inPins[f"a{bit}"] = 0
		
		self.outPins = {'out': 0}

		for bit in range(n_bits):
			self.parts[f"and{bit}"] = And()

		def f(ctx):
			in_values = [self.pin(f"a{i}") for i in range(n_bits)]

			self.set_pin("and0.a", in_values[0])
			self.set_pin("and0.b", in_values[1])
			self.parts["and0"].process()
			out = self.pin("and0.out")

			for bit in range(2, n_bits):
				self.set_pin(f"and{bit}.a", out)
				self.set_pin(f"and{bit}.b", in_values[bit])
				self.parts[f"and{bit}"].process()
			
			self.set_pin('out', self.pin(f"and{n_bits-1}.out"))

		self.wiring = Fn(f)


# class Demultiplexer(Chip):
# 	def __init__(self, n_bits):
# 		super().__init__()


# 		for i in range(n_bits):  # input bits init
# 			pin_name = "in" + i
# 			self.inPins[pin_name] = 0
# 		for i in range(n_bits**2):  # input bits init
# 			pin_name = "out" + i
# 			self.outPins[pin_name] = 0

# 		#self.inPins = {'a': 0, 'b': 0}
# 		#self.outPins = {'sum': 0, 'carry': 0}

# 		for i in range(n_bits):  # input bits init
# 			part_name = "not" + i
# 			self.parts[part_name] = Not()

# 		for i in range(n_bits):
# 			for k in range(n_bits):
# 				part_name = f"""and{i}{k}"""
# 				self.parts[part_name] = And()

# 		#self.parts = {'and': And(), 'xor': Xor()}

# 		def f(ctx):

# 			negated_input_values = {}
# 			input_values = {}

# 			for i in range(n_bits):
# 				input_value = self.pin('in'+i)
# 				self.set_pin(f"not{i}.a", input_value)
# 				self.parts['not'+i].process()
# 				negated_input_values['not'+i] = self.pin(f"not{i}.out")
			
# 			for p in product(*[[0,1] for x in range(n_bits)]):
# 				and_part_name = f"and{sum(p)}.a"
# 				for bit, i in enumerate(p):

					
# 			# for i in range(n_bits):
# 			# 	for k in range(n_bits):
# 			# 		if i == 1:
# 			# 			self.set_pin(f"and{i}.a",negated_input['not'+i])
# 			# 		else:
# 			# 			self.set_pin(f"and{i}.a", self.pin(f"in{i}"))

# 			# 		if k == 0:
# 			# 			self.set_pin(f"and{k}.b", self.pin(f"in{k}"))
# 			# 		else
# 			# 			self.set_pin(f"and{k}.b",negated_input['not'+k])
# 		self.wiring = Fn(f)