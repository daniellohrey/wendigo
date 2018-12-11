#takes module files and zip/encrypts them
#module files are <filename>.py, output files are <filename>

import zipfile
import sys
import os

if len(sys.argv) < 2:
	print "usage: %prog <file1 to encrypt> [file2 to encrypt] [...]"
	sys.exit(0)

temp = "TEMP FILE NAME"
pwd = "PASSWORD"
i = 1
while i < len(sys.argv):
	#copy file to temp file with name we expect to extract from
	f = open(temp, "w")
	g = open(sys.argv[i], "r")
	f.write(g.read())
	g.close()
	f.close()

	#build string to use in system zip command
	fn = sys.argv[i].split(".")
	if len(fn) > 2:
		print "dont use filenames with more than 1 ."
	ofn = fn[0]

	os.system("zip -P %s %s %s" % pwd, ofn, temp)
