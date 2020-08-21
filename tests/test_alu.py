from itertools import product
import random

from pycircuitsim.core.chip import BooleanFunctionChip, MultiBitChip, Chip
from pycircuitsim.hardware.adder import FullAdder
from pycircuitsim.hardware.logic_gates import DemuxNWay, Or, And, Not, MultiBitAnd, MultiBitOr, MultiBitNot


class Alu(Chip):



	def __init__(self, n_bits):
		super().__init__(['a','b','ena','enb','inva','f0','f1', ], ['out'])
		self.parts = {
			'ina': And(),
			'inb': And(),
			'decoder': DemuxNWay(2),
			'adder': FullAdder(n_bits),
			'or': MultiBitOr(n_bits),
			'and': MultiBitAnd(n_bits),
			'not': MultiBitNot(n_bits)
		}

	def setup_wiring(self):
		def f():
			inputs = {}
			for pin in ['a', 'b', 'ena', 'enb', 'inva', 'f0', 'f1', ]:
				inputs[pin] = self.pin(pin)


			a = inputs['a'] if inputs['ena'] else 0
			b = inputs['b'] if inputs['enb'] else 0

			# get enabled op	
			self.set_pin('decoder.in', True)
			self.set_pin('decoder.sel0', inputs['f0'])
			self.set_pin('decoder.sel1', inputs['f1'])
			self.process_chip('decoder')

			OUTPUT_ENABLED = [self.pin(f"decoder.out{x}") for x in range(2**2)]

			print(OUTPUT_ENABLED)

			if self.pin(f"decoder.out0"):
				# A and B 
				self.set_pin('and.a', a)
				self.set_pin('and.b', b)
				self.process_chip('and')
				self.link_pins('and.out', 'out')
			elif self.pin(f"decoder.out1"):
				# A or B 
				self.set_pin('or.a', a)
				self.set_pin('or.b', b)
				self.process_chip('or')
				self.link_pins('or.out', 'out')
			elif self.pin(f"decoder.out2"):
				# not B 
				self.set_pin('not.a', b)
				self.process_chip('not')
				self.link_pins('not.out', 'out')
			elif self.pin(f"decoder.out3"):
				# A + B
				self.set_pin('adder.in0', a)
				self.set_pin('adder.in1', b)
				self.process_chip('adder')

				self.link_pins('adder.out0', 'out')
			


		return f
	
def test_alu_16():
	chip = Alu(16)

	chip.set_pin('ena', True)
	chip.set_pin('enb', True)
	chip.set_pin('a', 3)
	chip.set_pin('b', 7)
	chip.set_pin('f0', True)
	chip.set_pin('f1', True)
	chip.process()

	assert chip.pin("out") == 10

	chip.set_pin('f0', False)
	chip.set_pin('f1', False)
	chip.process()

	assert chip.pin("out") == 3

	chip.set_pin('f0', True)
	chip.set_pin('f1', False)
	chip.process()

	assert chip.pin("out") == 7

	chip.set_pin('f0', False)
	chip.set_pin('f1', True)
	chip.process()

	assert chip.pin("out") == 0b1111111111111000


# def test_alu_8():
# 	chip = Alu(8)

# 	chip.set_pin('ena', True)
# 	chip.set_pin('enb', True)
# 	chip.set_pin('a', 3)
# 	chip.set_pin('b', 7)
# 	chip.set_pin('f0', True)
# 	chip.set_pin('f1', True)
# 	chip.process()

# 	assert chip.pin("out") == 10

# 	chip.set_pin('f0', False)
# 	chip.set_pin('f1', False)
# 	chip.process()

# 	assert chip.pin("out") == 3

# 	chip.set_pin('f0', True)
# 	chip.set_pin('f1', False)
# 	chip.process()

# 	assert chip.pin("out") == 7

# 	chip.set_pin('f0', False)
# 	chip.set_pin('f1', True)
# 	chip.process()

# 	assert chip.pin("out") == 0b1111111111111000
