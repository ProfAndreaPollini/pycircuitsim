from abc import abstractmethod
from typing import List, Dict
from math import log2
from ..core.chip import   ClockedChip, NotClockedChip
from ..hardware.logic_gates import MuxNWay

from .clock import Clock

class DataFlipFlop(ClockedChip):

	def __init__(self):
		super().__init__(['in'], ['out'])

		self.data = False
		self.wait_for_tick = False

	def on_tick(self, value):
		self.wait_for_tick = False
		self.data = self.pin('in')
		self.wiring.resolve()

	def setup_wiring(self):
		def f():
			self.set_pin('out', self.data)
		return f


class Register(ClockedChip):

	def __init__(self, nbits = 16):
		super().__init__(['in', 'load'], ['out'])
		self.parts = {
			'mux': MuxNWay(1),
			'dff': DataFlipFlop()
		}

		self.nbits = nbits

		self.last_out = False

	def _check_overflow(self, value):
		return (value >> 16) > 0

	def bits(self, offset, bits):
		return (self.get_value() >> offset) & int('1' * bits, 2)

	def low(self, bits):
		return self.bits(0,bits)

	def high(self, bits):
		return self.bits(self.nbits - bits, bits)

	def set_value(self, value: int):
		if self._check_overflow(value):
			raise OverflowError(f"value {value} don't fit into a {self.nbits} register")

		self.set_pin('in', value)
		self.set_pin('load', True)

	def get_value(self):
		return self.pin('out')

	def setup_wiring(self):
		def f():
			self.set_pin('mux.in0', self.last_out)
			self.set_pin('mux.in1', self.pin('in'))
			self.set_pin('mux.sel0', self.pin('load'))
			self.process_chip('mux')
			self.link_pins('mux.out', 'dff.in')
			#self.process_chip('dff')
			self.propagate_tick('dff')
			self.last_out = self.pin('dff.out')
			self.link_pins('dff.out', 'out')
		return f

	def on_tick(self, value):
		self.wiring.resolve()
		self.last_out = self.get_value()


class RAM(ClockedChip):

	def __init__(self,  size: int):
		super().__init__(['in', 'load', 'address'], ['out'])

		self.data = [0 for i in range(size)]

	def setup_wiring(self):
		def f():
			pos = self.pin('address')
			if self.pin('load') is True:
				self.data[pos] = self.pin('in')
				self.set_pin('out', self.data[pos])
			else:
				self.set_pin('out', self.data[pos])
		return f

	def on_tick(self, value):
		self.wiring.resolve()


class RAMMultiBank(ClockedChip):

	def __init__(self, clock: Clock, n_banks: int, bank_size: int):
		super().__init__(['in', 'load', 'address'], ['out'], clock)
		self.n_bank_bits = int(log2(n_banks))
		self.n_banksize_bits = int(log2(bank_size))
		self.mask = bin(int(''.join(['1' for x in range(int(log2(bank_size)))]),2) << int(log2(n_banks)))[2:]
		self.invmask = bin(int(self.mask, 2) ^ int(''.join(['1' for x in range(int(log2(bank_size)))], 2)))[2:]
		self.address_bits = self.n_bank_bits + self.n_banksize_bits
		self.parts = {
			f"bank{i}": RAM(clock, bank_size) for i in range(n_banks)
		}

	def setup_wiring(self):
		def f():
			address = self.pin('address')
			bank = int(bin(address)[2:][-self.address_bits] & int(self.mask,2),2)
			address_bit = int(bin(address)[2:][:],2)
			if self.pin('load') is True:
				pos = self.pin('address')
				self.data[pos] = self.pin('in')
				self.set_pin('out', self.data[pos])
			else:
				self.set_pin('out', self.pin('address'))
			
		return f

	def on_tick(self, value):
		super().process()