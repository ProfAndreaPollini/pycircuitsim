# pycircuitsim-
Python Hardware Simulator for circuits. It will also include some kind of assembly in the future


AND(a,b)

IN a
IN b

out OUT

f: a,b => a and b

AND ->  and(a,b) f(a,b)
IN(a)
AND(a,b) = AND(IN(a),IN(b))

DMUX(in,sel) => (a,b)

sel	|	a	b
============
0	|	in	0
1	|	0	in 

DMUX v,sel: (sel == 0 -> v:0,sel == 0 -> 0:v) 

SEL(IN(in),IN(sel)) = DMUX(in,sel) = OUT(a),OUT(b)