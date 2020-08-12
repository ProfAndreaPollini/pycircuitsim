from itertools import product


from pycircuitsim.hardware.logic_gates import Not, And, Or, Nand, Xor, AndMultiWay, \
	MultiBitAnd, HalfAdder, DemuxNWay, MuxNWay


def test_not_gate():
	chip = Not()

	chip.set_pin('a', False)
	chip.process()
	assert chip.pin('out') == True

	chip.set_pin('a', True)
	chip.process()
	assert chip.pin('out') == False


def test_or_gate():
	chip = Or()

	for p in product([False, True], [False, True]):
		expected = p[0] or p[1]
		chip.set_pin('a', p[0])
		chip.set_pin('b', p[1])
		chip.process()
		assert chip.pin('out') == expected


def test_and_gate():
	chip = And()

	for p in product([False, True], [False, True]):
		expected = p[0] and p[1]
		chip.set_pin('a', p[0])
		chip.set_pin('b', p[1])
		chip.process()
		assert chip.pin('out') == expected

def test_nand_gate():
	chip = Nand()

	for p in product([False, True], [False, True]):
		expected = not(p[0] and p[1])
		chip.set_pin('a', p[0])
		chip.set_pin('b', p[1])
		chip.process()
		assert chip.pin('out') == expected


def test_xor_gate():
	chip = Xor()

	for p in product([False, True], [False, True]):
		expected = p[0] ^ p[1]
		chip.set_pin('a', p[0])
		chip.set_pin('b', p[1])
		chip.process()
		assert chip.pin('out') == expected


def test_multiand2_gate():
	chip = AndMultiWay(2)

	for p in product([False, True], [False, True]):
		expected = p[0] and p[1]
		chip.set_pin('0', p[0])
		chip.set_pin('1', p[1])
		chip.process()
		assert chip.pin('out') == expected

def test_multiand3_gate():
	chip = AndMultiWay(3)

	for p in product([False, True], [False, True], [False, True]):
		expected = p[0] and p[1] and p[2]
		chip.set_pin('0', p[0])
		chip.set_pin('1', p[1])
		chip.set_pin('2', p[2])
		chip.process()
		assert chip.pin('out') == expected

def test_multibit_and_gate():

	chip  = MultiBitAnd(16)
	chip.set_pin('a', 7)
	chip.set_pin('b', 3)
	chip.process()
	assert chip.pin('out') == 3

def test_half_adder():

	chip = HalfAdder()
	chip.set_pin('a', False)
	chip.set_pin('b', False)
	chip.process()
	assert chip.pin('sum') == False
	assert chip.pin('carry') == False

	chip = HalfAdder()
	chip.set_pin('a', True)
	chip.set_pin('b', False)
	chip.process()
	assert chip.pin('sum') == True
	assert chip.pin('carry') == False

	chip = HalfAdder()
	chip.set_pin('a', False)
	chip.set_pin('b', True)
	chip.process()
	assert chip.pin('sum') == True
	assert chip.pin('carry') == False

	chip = HalfAdder()
	chip.set_pin('a', True)
	chip.set_pin('b', True)
	chip.process()
	assert chip.pin('sum') == False
	assert chip.pin('carry') == True


def test_demuxer():
	chip = DemuxNWay(2)
	chip.set_pin('in', True)
	chip.set_pin('sel0', True)
	chip.set_pin('sel1', False)
	chip.process()
	assert chip.pin('out0') == False
	assert chip.pin('out1') == True
	assert chip.pin('out2') == False
	assert chip.pin('out3') == False

	chip.set_pin('in', True)
	chip.set_pin('sel0', True)
	chip.set_pin('sel1', True)
	chip.process()
	assert chip.pin('out0') == False
	assert chip.pin('out1') == False
	assert chip.pin('out2') == False
	assert chip.pin('out3') == True


def test_muxer():
	chip = MuxNWay(2)
	chip.set_pin('sel0', True)
	chip.set_pin('sel1', False)
	chip.set_pin('in0', False)
	chip.set_pin('in1', True)
	chip.set_pin('in2', True)
	chip.set_pin('in3', False)
	chip.process()
	assert chip.pin('out') == True