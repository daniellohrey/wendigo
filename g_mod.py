#takes module files and zip/encrypts them
#module files are <filename>.py, output files are <filename>
#needs to be in same directory as conf.ig

import sys
import os
import json

if len(sys.argv) < 2:
	print "usage: %prog <file1 to encrypt> [file2 to encrypt] [...]"
	sys.exit(0)

with open("conf.ig", "r") as c:
	cf = c.read()
	conf = json.loads(cf)
	temp = conf["fn_s"]
	pwd = conf["pwd"]

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
		print "dont use filenames with more than 1 \'.\'"
	ofn = fn[0]

	string = "zip -P " + pwd + " " + ofn + " " + temp
	os.system(string)
	string = "mv " + ofn + ".zip " + ofn
	os.system(string)

	i += 1
