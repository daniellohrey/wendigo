import sys

if len(sys.argv) != 2:
	print "Need out file"
	sys.exit()

with open(sys.argv[1], "w") as f:
	for i in range(0, 178):
		s = "$" + str(i) + ":\n"
		f.write(s)
