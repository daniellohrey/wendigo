#generates blank options file

import sys

if len(sys.argv) != 2:
	print "usage: %prog OUTFILE"
	sys.exit()

if sys.argv[1] == "-h" or sys.argv[1] == "--help":
	print "usage: %prog OUTFILE"

with open(sys.argv[1], "w") as f:
	for i in range(0, 178):
		if i < 10:
			z = "00"
		elif i < 100:
			z = "0"
		else:
			z = ""
		s = "$" + z + str(i) + ":\n"
		f.write(s)
