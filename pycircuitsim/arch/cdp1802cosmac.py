

from ..core.chip import ClockedChip
from ..hardware.memory import Register, RAM
from ..hardware.clock import Clock

class CDP1802(ClockedChip):
	""" CDP1802 implementation 

	source: http://bitsavers.trailing-edge.com/components/rca/cosmac/MPM-201A_User_Manual_for_the_CDP1802_COSMAC_Microprocessor_1976.pdf

	"""
	def __init__(self, input_pins, output_pins):
		super().__init__(input_pins, output_pins)
		self.add_part("N", Register(4))
		self.add_part("I", Register(4))
		self.add_part("P", Register(4))
		self.add_part("X", Register(4))

		self.add_part("A", Register(16))

		self.R = []
		for i in range(16):
			r = Register(16)
			self.add_part(f"R{i}", r)
			self.R.append(r)

		self.add_part("mem", RAM(100))
		self.mpc = 0


	def connect_to_clock(self, clock: Clock):
		clock.subscribe_to_tick(self)

	def setup_wiring(self):
		pass

	def on_tick(self, params=None):
		self.propagate_tick('N')
		self.propagate_tick('P')
		self.propagate_tick('X')
		self.propagate_tick('I')
		self.propagate_tick('A')
		for i in range(16):
			self.propagate_tick(f"R{i}")

	def boot(self):
		self.parts['N'].set_value(0)
		self.parts['I'].set_value(0)
		self.parts['P'].set_value(0)
		self.parts['X'].set_value(0)
		self.parts['A'].set_value(0)

	@property
	def N(self) -> int:
		return self.pin("N.out")

	@N.setter
	def N(self, v):
		self.parts['N'].set_value(v)

	@property
	def I(self) -> int:
		return self.pin("I.out")

	@I.setter
	def I(self, v):
		self.parts['I'].set_value(v)

	@property
	def P(self) -> int:
		return self.pin("P.out")

	@P.setter
	def P(self, v):
		self.parts['P'].set_value(v)

	@property
	def A(self) -> int:
		return self.pin("A.out")

	@A.setter
	def A(self, v):
		self.parts['A'].set_value(v)

	def getR(self, n):
		return self.R[n].get_value()

	def setR(self, n,v):
		return self.R[n].set_value(v)

	def fetch(self):
		yield 5
		self.A = self.getR(self.P)
		yield False
		self.propagate_tick('A')
		yield self.A
		mem = self.parts['mem']
		mem.set_pin('address', self.A)
		mem.set_pin('load', False)
		self.propagate_tick('mem')
		yield False
		code = mem.pin('out')
		self.propagate_tick('mem')
		yield code
		#return self.A
