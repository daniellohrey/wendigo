#takes module files and zip/encrypts them

import os
import json
import argparse

parser = argparse.ArgumentParser(description = 
	"Encrypts and zips module/config files")
parser.add_argument("-c", "--config", default = "conf.ig", 
	help = "Name of config file")
parser.add_argument("files", nargs = "+", help = "Files to encrypt/zip")
args = parser.parse_args()

with open(args.config, "r") as c:
	cf = c.read()
	conf = json.loads(cf)
	temp = conf["fn_s"]
	pwd = conf["pwd"]

for fn in files:
	try:
		#copy file to temp file with name we expect to extract from
		f = open(temp, "w")
		g = open(fn, "r")
		f.write(g.read())
	except:
		continue
	finally:
		g.close()
		f.close()

	#build string to use in system zip command
	nfn = fn.split(".")
	if len(fn) > 2:
		print "dont use filenames with more than 1 \'.\'"
		continue
	ofn = nfn[0]

	s = "zip -P " + pwd + " " + ofn + " " + temp
	os.system(s)
	s = "mv " + ofn + ".zip " + ofn
	os.system(s)
