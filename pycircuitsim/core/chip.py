"""
This module contains chip definition. Chip is an abstract base class.
In order to create your chip you must override the setup_wiring
function in order to create your chip wiring.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable


class Chip(ABC):
	"""This abstract class represnts a chip. You must inhert and override
	setup_wiring to create your own chip.
	It support composition, every chip has multiple
	parts that are chip on their own"""
	class Wiring:
		def __init__(self, fn):
			self.fn = fn

		def resolve(self):
			return self.fn()

	def __init__(self, input_pins: List[str], output_pins: List[str]):
		super().__init__()

		self.inPins: Dict[str, bool] = {}
		for pin in input_pins:
			self.inPins[pin] = False
		self.outPins: Dict[str, bool] = {}
		for pin in output_pins:
			self.outPins[pin] = False
		self.parts: Dict[str, Chip] = {}
		self.wiring = self.Wiring(self.setup_wiring())

	def add_part(self, name: str, chip: Any):
		self.parts[name] = chip

	def process_chip(self, name):
		self.parts[name].process()

	def link_pins(self, pin_from: str, pin_to: str) -> None:
		self.set_pin(pin_to, self.pin(pin_from))

	@abstractmethod
	def setup_wiring(self) -> None:
		pass

	def process(self):
		self.wiring.resolve()

	def pin(self, pin_name):
		""" get pin_name value. You can address input pin,
		output pin or a chip part pin using the "partname.pinname" name for the pin.
		Raise exception if it can't fine the requested pin"""
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
		""" set pin_name to value. You can address input pin,
		output pin or a chip part pin using the "partname.pinname"
		name for the pin name.
		Raise exception if it can't fine the requested pin"""
		if name in self.inPins.keys():
			self.inPins[name] = value
		elif name in self.outPins.keys():
			self.outPins[name] = value
		elif '.' in name:  # if is requested a pin from a chip component, get it!
			fields = name.split('.')
			if fields[0] in self.parts.keys():
				return self.parts[fields[0]].set_pin(fields[1], value)
		else:
			raise "Incorrect pin name"


class MultiBitChip(Chip):

	def __init__(self, n_bits: int, n_inputs: int, fn: Callable[[int], None]):
		super().__init__([f"in{i}" for i in range(n_bits)],
						[f"out{i}" for i in range(n_bits)])

		self.fn = fn
		self.n_bits = n_bits

	def setup_wiring(self):
		def f():
			for bit in self.n_bits:
				self.fn(bit)
		return f
