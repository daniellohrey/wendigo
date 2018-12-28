import sys
from getpass import getpass
from github3 import login

gh = login("daniellohrey", getpass("GitHub password:"))

if len(sys.argv) > 1:
	for auth in gh.authorizations():
		if not auth.delete():
			print "failed to delete"
			sys.exit()
	print "deleted all"
else:
	with open("tk.o", "r") as f:
		id = f.read()

	auth = gh.authorization(int(id))
	if auth.delete():
		print "deleted token"
	else:
		print "failed to delete"
