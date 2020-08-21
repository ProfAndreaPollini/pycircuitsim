"""
This module contains chip definition. Chip is an abstract base class.
In order to create your chip you must override the setup_wiring
function in order to create your chip wiring.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Tuple, Type, Union, TypeVar, Generic

from .errors import IncorrectPinNameError, ChipWiringError

from ..hardware.clock import Clock


# class INoClockSynced(ABC):
# 	"""Interface that describes a chip which is not synced with a clock, 
# 	i.e. it changes its outputs as soon as an input change
# 	"""

# 	clock_synced = False

# 	def set_pin(self, name, value):
# 		super().set_pin(name, value) # update pin value

# 		if name in self.inPins.keys(): # if the pin is an input, re-evaluate this chip
# 			self.process()

# 	@abstractmethod
# 	def process(self):
# 		pass


# class IClockSynced(ABC):
# 	"""Interface that describes a chip which is synced with a clock, 
# 	i.e. it changes its outputs as soon as the clock it's synced to ticks.
# 	"""

# 	clock_synced = True

# 	@abstractmethod
# 	def propagate_clock(self):
# 		pass


class AbstractChip(ABC):
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

		self.wiring = self.Wiring(self.setup_wiring())

	def link_pins(self, pin_from: str, pin_to: str) -> None:
		self.set_pin(pin_to, self.pin(pin_from))

	@abstractmethod
	def setup_wiring(self) -> None:
		pass

	def pin(self, pin_name):
		""" get pin_name value. You can address input pin,
		output pin or a chip part pin using the "partname.pinname" name for the pin.
		Raise exception if it can't fine the requested pin"""
		if pin_name in self.inPins.keys():
			return self.inPins[pin_name]
		elif pin_name in self.outPins.keys():
			return self.outPins[pin_name]
		else:
			raise IncorrectPinNameError(pin_name)

	def set_pin(self, name, value):
		""" set pin_name to value. You can address input pin,
		output pin or a chip part pin using the "partname.pinname"
		name for the pin name.
		Raise exception if it can't fine the requested pin"""
		if name in self.inPins.keys():
			self.inPins[name] = value
		elif name in self.outPins.keys():
			self.outPins[name] = value
		else:
			raise IncorrectPinNameError(name)




# class BaseChi2p(AbstractChip, INoClockSynced):
# 	def __init__(self, input_pins: List[str], output_pins: List[str]):
# 	 	super().__init__(input_pins, output_pins)

# 	 	self.parts: Dict[str, Type[INoClockSynced]] = {}

# 	def add_part(self, name: str, chip: Any):
# 		self.parts[name] = chip

# 	def process_chip(self, name):
# 		self.parts[name].process(2)

# 	def set_pin(self, name, value):
# 		""" set pin_name to value. You can address input pin,
# 		output pin or a chip part pin using the "partname.pinname"
# 		name for the pin name.
# 		Raise exception if it can't fine the requested pin"""
# 		try:
# 			return super().set_pin(name, value)
# 		except IncorrectPinNameError as err:
# 			pass
# 		if '.' in name:  # if is requested a pin from a chip component, get it!
# 			fields = name.split('.')
# 			if fields[0] in self.parts.keys():
# 				return self.parts[fields[0]].set_pin(fields[1], value)
# 		else:
# 			raise IncorrectPinNameError(name)

# 	def pin(self, pin_name):
# 		""" get pin_name value. You can address input pin,
# 		output pin or a chip part pin using the "partname.pinname" name for the pin.
# 		Raise exception if it can't fine the requested pin"""
# 		try:
# 			return super().pin(pin_name)
# 		except IncorrectPinNameError as err:
# 			if '.' in pin_name:  # if is requested a pin from a chip component, get it!
# 				fields = pin_name.split('.')
# 				if fields[0] in self.parts.keys():
# 					return self.parts[fields[0]].pin(fields[1])
# 			else:
# 				raise IncorrectPinNameError(pin_name)

class CompositeChip(AbstractChip):

	def __init__(self, input_pins, output_pins):
		super().__init__(input_pins, output_pins)

	def add_part(self, name: str, chip: Any):
		self.parts[name] = chip

	def process_chip(self, name):
		self.parts[name].process()

	def set_pin(self, name, value):
		""" set pin_name to value. You can address input pin,
		output pin or a chip part pin using the "partname.pinname"
		name for the pin name.
		Raise exception if it can't fine the requested pin"""
		try:
			return super().set_pin(name, value)
		except IncorrectPinNameError as err:
			pass
		if '.' in name:  # if is requested a pin from a chip component, get it!
			fields = name.split('.')
			if fields[0] in self.parts.keys():
				return self.parts[fields[0]].set_pin(fields[1], value)
		else:
			raise IncorrectPinNameError(name)

	def pin(self, pin_name):
		""" get pin_name value. You can address input pin,
		output pin or a chip part pin using the "partname.pinname" name for the pin.
		Raise exception if it can't fine the requested pin"""
		try:
			return super().pin(pin_name)
		except IncorrectPinNameError as err:
			if '.' in pin_name:  # if is requested a pin from a chip component, get it!
				fields = pin_name.split('.')
				if fields[0] in self.parts.keys():
					return self.parts[fields[0]].pin(fields[1])
			else:
				raise IncorrectPinNameError(pin_name)


# class LogicGate(BaseChip, INoClockSynced):

# 	def __init__(self, input_pins, output_pins):
# 		super().__init__(input_pins, output_pins)


class NotClockedChip(CompositeChip):
	def __init__(self, input_pins: List[str], output_pins: List[str]):
		super().__init__(input_pins, output_pins)
		self.parts: Dict[str, Type[NotClockedChip]] = {}

	def process(self):
		self.wiring.resolve()

	def set_pin(self, name, value):
		super().set_pin(name, value)
		if name in self.inPins.keys(): # if the pin is an input, re-evaluate this chip
			self.process()


class Chip(NotClockedChip):
	pass


class ClockedChip(CompositeChip):
	def __init__(self, input_pins: List[str], output_pins: List[str]):
		super().__init__(input_pins, output_pins)

		self.parts: Dict[str, Type[ClockedChip]] = {}
		self.wiring = self.Wiring(self.setup_wiring())

		#self.inPins['clock'] = False
		#self.clock = clock

	def on_tick(self, params=None):
		pass

	def on_tok(self, params=None):
		pass

	def propagate_tick(self, name, params=None):
		self.parts[name].on_tick(params)
	

class MultiBitChip(NotClockedChip):

	def __init__(self, n_bits: int, n_inputs: int, n_outputs: int,  fn: Callable[[NotClockedChip, int], None]):
		super().__init__([f"in{i}" for i in range(n_inputs)],
						[f"out{i}" for i in range(n_outputs)])

		self.fn = fn
		self.n_bits = n_bits
		self.n_inputs = n_inputs
		self.n_outputs = n_outputs

	def reset(self):
		for i in range(self.n_inputs):
			self.set_pin(f"in{i}",0)
		for i in range(self.n_outputs):
			self.set_pin(f"out{i}",0)

	def setup_wiring(self):
		def f():
			for bit in range(self.n_bits):
				self.fn(self, bit)
		return f


class BooleanFunctionChip(Chip):

	def __init__(self, input_pins: List[str], output_pins: List[str], fdata: Dict[ Tuple[Any,...], Tuple[Any,...]]):
		super().__init__(input_pins, output_pins)
		self.f_map = fdata

	def setup_wiring(self):
		def f():
			inputs = tuple([self.pin(x) for x in self.inPins.keys()])
			if inputs in self.f_map.keys():
				for pos, out_pin in enumerate(self.outPins.keys()):
					self.set_pin(out_pin, self.f_map[inputs][pos])
			else:
				raise ChipWiringError("Mapping not found")
		return f
