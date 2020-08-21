
from pycircuitsim.arch.cdp1802cosmac import CDP1802
from pycircuitsim.hardware.clock import Clock


def test_N_register():
	cosmac = CDP1802([],[])
	clock = Clock()
	cosmac.connect_to_clock(clock)
	cosmac.boot()
	clock.tick()

	assert cosmac.N == 0

	cosmac.P = 2 
	clock.tick()
	assert cosmac.P == 2
	#assert cosmac.fetch() == 2

	cosmac.setR(2,10)
	clock.tick()
	assert cosmac.getR(2) == 10
	#assert cosmac.fetch() == 10

def test_fetch():
	cosmac = CDP1802([],[])
	clock = Clock()
	cosmac.connect_to_clock(clock)
	cosmac.boot()
	clock.tick()

	assert cosmac.N == 0

	cosmac.P = 2
	clock.tick()
	assert cosmac.P == 2
	#assert cosmac.fetch() == 2

	cosmac.setR(2,10)
	clock.tick()
	
	g = cosmac.fetch()
	steps = next(g)
	assert steps == 5

	assert next(g) == False
	assert next(g) == 10
	assert next(g) == False
	assert next(g) == 0

