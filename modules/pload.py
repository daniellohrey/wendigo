import sys
import imp
from github3 import login

#searches for module files, from path provided
def search_file(fullname, search, config):
	gh = login(token = config.g_tk())
        repo = gh.repository(config.g_usr(), config.g_repo())
        cont = repo.directory_contents(search)
        for fn, c in cont:
                if "dir" in c.type:
                        s = search_file(fullname, c.path)
                        if s is not None:
                                return s
                        else:
                                continue
		#double check for bugs
                if fullname in fn or (fullname in c.path and "__init__" in fn):
			#possibily base64/encrypt package files
                        return repo.file_contents(c.path).decoded
        return None

#returns handle to module (such as with "import module as name")
def my_load(fullname, config):
	try:
		return sys.modules[fullname]
	except:
		pass
        name = fullname.split(".")
        pathname = config.g_mod()
	pathname = pathname[:-1]
        modname = ""
	fn = config.g_fn()
        for mod in name:
                if modname:
                        modname = modname + "." + mod
                else:
                        modname = mod
                contents = search_file(mod, pathname, config)
                if contents:
                        with open(fn, "w") as f:
                                f.write(contents)
                else:
                        return None
                suffixes = (".py", "r", imp.PY_SOURCE)
                pathname = pathname + "/" + mod
                file = open(fn, "r")
                try:
			#check usage of StringIO with pathname set to ""
                        sys.modules[modname] = imp.load_module(modname, file,
                                                                pathname, suffixes)
                finally:
                        file.close()
        return sys.modules[fullname]

def run(config, **args):
	loaded = "loaded: "
	try:
		to_load = args["load"]
	except:
		return None, None
	for module in to_load:
		try:
			my_load(str(module), config)
			loaded = loaded + str(module) + ", "
		except:
			pass
	return None, loaded
