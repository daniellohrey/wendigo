import sys

if len(sys.argv) != 2:
	print "Need out file"
	sys.exit()

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
