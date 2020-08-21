

from pycircuitsim.hardware.clock import Clock
from pycircuitsim.hardware.memory import ClockedChip, DataFlipFlop, Register, RAM
from pycircuitsim.hardware.adder import FullAdder
 



def test_dff_chip():
	clock = Clock()
	chip = DataFlipFlop()
	clock.subscribe_to_tick(chip)

	assert chip.pin('out') is False
	chip.set_pin('in', True)

	assert chip.pin('out') is False

	clock.tick()

	assert chip.pin('out') is True


def test_register_chip():
	clock = Clock()
	chip = Register()
	clock.subscribe_to_tick(chip)

	chip.set_pin('in', True)
	chip.set_pin('load', False)
	assert chip.pin('out') is False
	clock.tick()
	assert chip.pin('out') is False
	chip.set_pin('load', True)
	assert chip.pin('out') is False
	clock.tick()
	assert chip.pin('out') is True


def test_register_chip_int():
	clock = Clock()
	chip = Register()
	clock.subscribe_to_tick(chip)
	chip.set_pin('in', 23)
	chip.set_pin('load', False)
	assert int(chip.pin('out')) == 0
	
	chip.set_pin('load', True)
	
	assert int(chip.pin('out')) == 0
	clock.tick()
	assert int(chip.pin('out')) == 23


def test_ram():
	clock = Clock()
	chip = RAM(3)
	clock.subscribe_to_tick(chip)
	chip.set_pin('in', 23)
	chip.set_pin('load', False)
	chip.set_pin('address', 0)
	assert int(chip.pin('out')) == 0
	clock.tick()
	assert int(chip.pin('out')) == 0
	chip.set_pin('load', True)
	clock.tick()
	assert int(chip.pin('out')) == 23


def test_cosmac():
	clock = Clock()
	N = Register(4)
	clock.subscribe_to_tick(N)
	P = Register(4)
	I = Register(4)
	X = Register(4)

	D = Register(8)
	A = Register(16)

	Adder = FullAdder(8)
	R: list[Register] = [Register(16) for i in range(16)]
	for r in R:
		clock.subscribe_to_tick(r)

	N.set_value(3)
	R[3].set_value(4)

	#N.on_tick(1)
	clock.tick()
	assert int(N.pin('out')) == 3
	assert N.get_value() == 3
	assert N.low(1) == 1
	assert N.high(3) == 1
	assert N.high(4) == 3
	assert N.low(3) == 3
	assert N.low(4) == 3

	clock.tick()
	assert int(N.pin('out')) == 3

	reg: Register = R[N.get_value()]
	v = int(reg.get_value())
	#i = Adder.set_pin('')
	reg.set_value(v+1)
	clock.tick()
	assert int(reg.get_value()) == v + 1
	assert int(R[N.get_value()].get_value()) == v+1