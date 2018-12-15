#base64 encodes zipped/encrypted module files and pushes them to github

import base64
import sys
import argparse
import json
from github3 import login

parser = argparse.ArgumentParser(description = "Push module/config files to GitHub")
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--config", action = "store_true", help = "Use config path"))
group.add_argument("-m", "--module", action = "store_true", help = "Use module path")
group.add_argument("-p", "--path", help = "Specify custom upload path")
parser.add_argument("files", nargs = "+", help = "Files to push to GitHub path"
args = parser.parse_args()

if not (args.module or args.config or args.path):
	print "Need to specify module or config path"
	sys.exit()

with open("conf.ig", "r") as c:
	cf = c.read()
	conf = json.loads(cf)
	usr = conf["usr"]
	repo = conf["repo"]
	tk = base64.b64decode(conf["token"])
	if args.module:
		path = conf["mod"]
	elif args.config:
		path = conf["config"]
	else:
		path = args.path

for fn in files:
	#get contents of file
	try:
		f = open(fn, "r")
		d = f.read()
		d = base64.b64encode(c)
	except:
		continue
	finally:
		f.close()

	#push to github
	try:
		gh = login(token = tk)
		rp = gh.repository(usr, repo)
	except:
		continue

	p = path + fn
	cm = "upload " + fn
	try:
		rp.create_file(p, cm, d) #file path, message, data
	except:
		#file already exists
		cm = "update " + fn
		rp.file_contents(fn).update(cm, d)
