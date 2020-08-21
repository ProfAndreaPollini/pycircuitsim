""" N bit Adder implemtation
"""

from ..core.chip import Chip, MultiBitChip, BooleanFunctionChip



def _twobit_adder_wiring(chip : Chip, bit):
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


class FullAdder(MultiBitChip):

	def __init__(self, n_bits,):
		super().__init__(n_bits, 2, 1, _twobit_adder_wiring)
		
		for b in range(n_bits):
			self.add_part(f'adder{b}', BooleanFunctionChip(['a', 'b', 'carry_in'], ['sum', 'carry_out'], {
				(False, False, False): (False, False),
				(True, False, False): (True, False),
				(False, True, False): (True, False),
				(True, True, False): (False, True),
				(False, False, True): (True, False),
				(True, False, True): (False, True),
				(False, True, True): (False, True),
				(True, True, True): (True, True)
			}))


	
