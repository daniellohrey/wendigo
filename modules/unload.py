#unloads previously loaded modules
#uload is a list of modules to unload
#may be unstable, may need to change the way wendigo imports
#use sys.getrefcount() when testing

import sys

def run(config, **args):
	unloaded = "unloaded "
	try:
		uload = args["uload"]
	except:
		return None, None
	for mod in uload:
		cmd = "del(sys.modules[\"%s\"])" % mod
		try:
			exec cmd
			unloaded += "mod "
		except:
			continue
		#need to check whether this actually works
		#probably need to delete reference held by main thread
		#would require rewriting wendigo so it doesnt use import and only
		#references the modules in sys.modules
	try:
		unloaded = unloaded[:-1] #remove trailing space
		return None, unloaded
	except:
		return None, None #didnt unload anything (since len(unloaded) would
					#have to be 0 to fail
