from ..core.chip import Chip


class Not(Chip):
	def __init__(self):
		super().__init__(input_pins=['a'], output_pins=['out'])

	def setup_wiring(self):
		def f():
			self.set_pin('out', not self.pin('a'))
		return f


class Or(Chip):
	def __init__(self):
		super().__init__(input_pins=['a', 'b'], output_pins=['out'])

	def setup_wiring(self):
		def f():
			self.set_pin('out', self.pin('a') or self.pin('b'))
		return f


class And(Chip):
	def __init__(self):
		super().__init__(input_pins=['a', 'b'], output_pins=['out'])

	def setup_wiring(self):
		def f():
			self.set_pin('out', self.pin('a') and self.pin('b'))
		return f


class Nand(Chip):

	def __init__(self):
		super().__init__(input_pins=['a', 'b'], output_pins=['out'])
		self.add_part('and', And())
		self.add_part('not', Not())

	def setup_wiring(self):
		def f():
			self.link_pins('a', 'and.a')
			self.link_pins('b', 'and.b')

			self.process_chip('and')

			self.link_pins('and.out', 'not.a')

			self.process_chip('not')

			self.link_pins('not.out', 'out')

		return f


class Xor(Chip):
	def __init__(self):
		super().__init__(input_pins=['a', 'b'], output_pins=['out'])
		self.add_part('not1', Not())
		self.add_part('not2', Not())
		self.add_part('and1', And())
		self.add_part('and2', And())
		self.add_part('or', Or())

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

	def setup_wiring(self):
		def f():
			self.link_pins('a', 'not1.a')
			self.link_pins('b', 'not2.a')
			self.process_chip('not1')
			self.process_chip('not2')
			self.link_pins('a', 'and1.a')
			self.link_pins('not2.out', 'and1.b')

			self.link_pins('not1.out', 'and2.a')
			self.link_pins('b', 'and2.b')

			self.process_chip('and1')
			self.process_chip('and2')

			self.link_pins('and1.out', 'or.a')
			self.link_pins('and2.out', 'or.b')

			self.process_chip('or')
			self.link_pins('or.out', 'out')
		return f


class AndMultiWay(Chip):

	def __init__(self, n_bits=2):
		super().__init__([f"{i}" for i in range(n_bits)], ['out'])
		for part in range(n_bits-1):
			self.add_part(f"and{part}", And())

		self.n_bits = n_bits

	def setup_wiring(self):
		def f():
			for part in range(len(self.parts)):
				if part == 0:
					self.link_pins('0', 'and0.a')
					self.link_pins('1', 'and0.b')
					self.process_chip('and0')
				else:
					self.link_pins(f'and{part-1}.out', f'and{part}.a')
					self.link_pins(f'{part+1}', f'and{part}.b')
					self.process_chip(f'and{part}')
				if part == len(self.parts)-1:
					self.link_pins(f"and{part}.out", "out")
		return f


class MultiBitAnd(Chip):
	def __init__(self, bits):
		super().__init__(input_pins=['a', 'b'], output_pins=['out'])
		self.bits = bits

	def setup_wiring(self):
		def f():
			a = int(self.pin('a'))
			b = int(self.pin('b'))
			out = 0
			for bit in range(self.bits):
				v = (a >> bit & 1) and (b >> bit & 1)
				out |= v << bit
			self.set_pin('out', out)
		return f


class HalfAdder(Chip):
	def __init__(self):
		super().__init__(input_pins=['a', 'b'], output_pins=['sum', 'carry'])

	def setup_wiring(self):
		def f():
			a = int(self.pin('a'))
			b = int(self.pin('b'))

			self.set_pin('sum', a ^ b)
			self.set_pin('carry', a and b)
		return f


class DemuxNWay(Chip):
	def __init__(self, n):
		inputs = ['in']
		inputs.extend([f"sel{i}" for i in range(n)])
		super().__init__(input_pins=inputs, output_pins=[f"out{i}" for i in range(n**2)])
		self.n = n

	def reset_out_pins(self):
		for i in range(self.n**2):
			self.set_pin(f"out{i}", False)

	def setup_wiring(self):
		def f():
			sel_value = 0
			for bit in range(self.n):
				v = int(self.pin(f'sel{bit}'))
				sel_value |= v << bit

			self.reset_out_pins()
			self.set_pin(f'out{sel_value}', self.pin("in"))
		return f


class MuxNWay(Chip):
	def __init__(self, n):
		inputs = [f"sel{i}" for i in range(n)]
		inputs.extend([f"in{i}" for i in range(n**2)])
		super().__init__(input_pins=inputs, output_pins=['out'])
		self.n = n

	def reset_out_pins(self):
		for i in range(self.n**2):
			self.set_pin(f"out", False)

	def setup_wiring(self):
		def f():
			sel_value = 0
			for bit in range(self.n):
				v = int(self.pin(f'sel{bit}'))
				sel_value |= v << bit
			self.reset_out_pins()
			self.set_pin('out', self.pin(f"in{sel_value}"))
		return f
