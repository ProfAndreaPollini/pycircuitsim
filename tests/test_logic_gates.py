from pycircuitsim.chip import AndGate, AndGate3, And3,  \
			Not, Nand, Xor, HalfAdder, MultiBitAnd


def test_and_gate():
	gate = AndGate()
	gate.setInput('a', 1)
	gate.setInput('b', 1)
	gate.process()
	assert gate.getOutput('out') == 1

def test_and3_gate():
	gate = AndGate3()
	gate.set_pin('a', 1)
	gate.set_pin('b', 1)
	gate.set_pin('c', 1)
	gate.process()
	assert gate.pin('out') == 1

def test_and3_gatev2():
	gate = And3()
	gate.set_pin('a', 1)
	gate.set_pin('b', 1)
	gate.set_pin('c', 1)
	gate.process()
	assert gate.pin('out') == 1

def test_and3_gatev3():
	gate = MultiBitAnd(3)
	gate.set_pin('a0', 1)
	gate.set_pin('a1', 1)
	gate.set_pin('a2', 1)
	gate.process()
	assert gate.pin('out') == 1

def test_and4_gatev3():
	gate = MultiBitAnd(4)
	gate.set_pin('a0', 1)
	gate.set_pin('a1', 1)
	gate.set_pin('a2', 1)
	gate.set_pin('a3', 0)
	gate.process()
	assert gate.pin('out') == 0


def test_nand():
	chip = Nand()
	
	chip.set_pin('a',1)
	chip.set_pin('b',1)
	assert chip.pin('out') == 0

def test_xor():
	chip = Xor()
	
	chip.set_pin('a',0)
	chip.set_pin('b',0)
	chip.process()
	assert chip.pin('out') == 0

	chip.set_pin('a',1)
	chip.set_pin('b',0)
	chip.process()
	assert chip.pin('out') == 1

	chip.set_pin('a',0)
	chip.set_pin('b',1)
	chip.process()
	assert chip.pin('out') == 1

	chip.set_pin('a',1)
	chip.set_pin('b',1)
	chip.process()
	assert chip.pin('out') == 0


def test_half_adder():
	chip = HalfAdder()
	
	chip.set_pin('a', 0)
	chip.set_pin('b', 0)
	chip.process()
	assert chip.pin('sum') == 0
	assert chip.pin('carry') == 0

	chip.set_pin('a', 1)
	chip.set_pin('b', 0)
	chip.process()
	assert chip.pin('sum') == 1
	assert chip.pin('carry') == 0

	chip.set_pin('a', 0)
	chip.set_pin('b', 1)
	chip.process()
	assert chip.pin('sum') == 1
	assert chip.pin('carry') == 0

	chip.set_pin('a', 1)
	chip.set_pin('b', 1)
	chip.process()
	assert chip.pin('sum') == 0
	assert chip.pin('carry') == 1