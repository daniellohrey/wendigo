#base64 encodes zipped/encrypted module files and pushes them to github

import base64
import sys
from github3 import login

if len(sys.argv) < 2:
	print "usage: %prog <file1 to push> [file2 to push] [...]"
	sys.exit(0)

mod = "modules/"
usr = "daniellohrey"
repo = "wendigo_test"
tk = "INSERT TOKEN"
tk = base64.b64decode(tk)
i = 1
while i < len(sys.argv):
	#get contents of file
	f = open(sys.argv[i], "r")
	c = f.read()
	c = base64.b64encode(c)
	f.close()

	#push to github
	try:
		gh = login(token = token)
		rp = gh.repository(usr, repo)
	except:
		print "couldnt connect to github"

	fn = mod + sys.argv[i]
	cm = "upload" + sys.argv[i]
	try:
		rp.create_file(fn, cm, c) #file path, message, data
	except:
		#file already exists
		cm = "update" + sys.argv[i]
		rp.file_contents(fn).update(cm, c)
