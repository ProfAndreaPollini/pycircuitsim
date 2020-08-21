from itertools import product
import random

from pycircuitsim.core.chip import BooleanFunctionChip, MultiBitChip, Chip
from pycircuitsim.hardware.adder import FullAdder

def test_booleanfunctionchip():
	chip = BooleanFunctionChip(['a', 'b'], ['sum', 'carry'], {
		(False, False): (False, False),
		(True, False): (True, False),
		(False, True): (True, False),
		(True, True): (False, True)
	})
	for p in product([False, True], [False, True]):
		expected_sum = p[0] ^ p[1]
		expected_carry = p[0] and p[1]
		chip.set_pin('a', p[0])
		chip.set_pin('b', p[1])
		chip.process()
		assert chip.pin('sum') == expected_sum
		assert chip.pin('carry') == expected_carry


def test_two_bit_adder():
	

	def twobit_adder_wiring(chip : Chip, bit):
		a = chip.pin('in0') >> bit & 1
		b = chip.pin('in1') >> bit & 1
		out = 0

		chip.set_pin(f"adder{bit}.a", a)
		chip.set_pin(f"adder{bit}.b", b)
		if bit == 0 or bit == len(chip.parts)-1:
			chip.set_pin(f"adder{bit}.carry_in", False)
		else:
			chip.link_pins(f"adder{bit}.carry_out", f"adder{bit+1}.carry_in")
		chip.process_chip(f'adder{bit}')
		out = int(chip.pin('out0')) + chip.pin(f'adder{bit}.sum') * (2 ** bit)
		# out = chip.pin(f'adder{bit}.sum')
		chip.set_pin('out0', out)
		# print(chip.pin('out0'))



	chip = MultiBitChip(2,2, 1, twobit_adder_wiring)

	chip.add_part('adder0', BooleanFunctionChip(['a', 'b', 'carry_in'], ['sum', 'carry_out'], {
		(False, False, False): (False, False),
		(True, False, False): (True, False),
		(False, True, False): (True, False),
		(True, True, False): (False, True),
		(False, False, True): (True, False),
		(True, False, True): (False, True),
		(False, True, True): (False, True),
		(True, True, True): (True, True)
	}))
	chip.add_part('adder1', BooleanFunctionChip(['a', 'b', 'carry_in'], ['sum', 'carry_out'], {
		(False, False, False): (False, False),
		(True, False, False): (True, False),
		(False, True, False): (True, False),
		(True, True, False): (False, True),
		(False, False, True): (True, False),
		(True, False, True): (False, True),
		(False, True, True): (False, True),
		(True, True, True): (True, True)
	}))

	assert chip != None

	chip.set_pin('in0', 2)
	chip.set_pin('in1', 1)
	chip.process()

	assert chip.pin('out0') == 3


def test_16bit_adder():

	def twobit_adder_wiring(chip : Chip, bit):
		a = chip.pin('in0') >> bit & 1
		b = chip.pin('in1') >> bit & 1
		out = 0

		chip.set_pin(f"adder{bit}.a", a)
		chip.set_pin(f"adder{bit}.b", b)
		if bit == 0 or bit == len(chip.parts)-1:
			chip.set_pin(f"adder{bit}.carry_in", False)
	
		chip.process_chip(f'adder{bit}')
		if not bit == len(chip.parts)-1:
			chip.link_pins(f"adder{bit}.carry_out", f"adder{bit+1}.carry_in")

		out = int(chip.pin('out0')) + chip.pin(f'adder{bit}.sum') * (2 ** bit)
		# out = chip.pin(f'adder{bit}.sum')
		chip.set_pin('out0', out)
		# print(chip.pin('out0'))

	N_BITS = 16

	chip = MultiBitChip(16, 2, 1, twobit_adder_wiring)
	for b in range(N_BITS):
		chip.add_part(f'adder{b}', BooleanFunctionChip(['a', 'b', 'carry_in'], ['sum', 'carry_out'], {
			(False, False, False): (False, False),
			(True, False, False): (True, False),
			(False, True, False): (True, False),
			(True, True, False): (False, True),
			(False, False, True): (True, False),
			(True, False, True): (False, True),
			(False, True, True): (False, True),
			(True, True, True): (True, True)
		}))


	assert chip != None

	adder = FullAdder(16)

	for x, y in [(random.randint(0, 10), random.randint(0, 10)) for x in range(2000)]: 
		print(x, y)
		chip.reset()
		chip.set_pin('in0', x)
		chip.set_pin('in1', y)
		chip.process()

		adder.reset()
		adder.set_pin('in0',x)
		adder.set_pin('in1',y)
		adder.process()

		assert chip.pin('out0') == x + y
		assert chip.pin('out0') == adder.pin('out0')