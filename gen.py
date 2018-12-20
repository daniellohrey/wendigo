import argparse
import time
import re
import xxhash
import random

def gk_hash(key):
	global cur
	global vars
	global used
	alpha = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
	while True:
		rand = str(random.random()) + cur
		rand = xxhash.xxh32(rand).hexdigest()
		rand = alpha[random.randint(0, 51)] + rand
		curr = xxhash.xxh64(rand).hexdigest()
		if rand not in used:
			used.append(rand)
			vars[key] = rand
			return

parser = argparse.ArgumentParser(description = 
	"Generates obfuscated wendigo script")
parser.add_argument("-v", "--variables", help = 
	"File with prefilled variables that won't be randomly generated (in form $[0-9][0-9][0-9]:value)")
parser.add_argument("-b", "--blank", default = "blank.py", help = 
	"Blank file to be filled with keys (variable names as $[0-9][0-9][0-9])")
parser.add_argument("-o", "--out", default = "b_out.py", help = 
	"Out file once blank is filled with keys")
parser.add_argument("-s", "--seed", help = 
	"Specify a seed for random number generation (default is current time)")
parser.add_argument("-g", "--generation", default = gk_hash, help = 
	"Strategy for variable generation")
args = parser.parse_args()

gen = args.generation

def replace(match):
	global vars
	global gen
	key = match.group()
	if key not in vars:
		gen(key)
	return vars[key]

vars = {}
used = []
random.seed(args.seed)
cur = xxhash.xxh64(str(random.random())).hexdigest()

if args.variables:
	with open(args.variables, "r") as f:
		for line in f:
			line = line.strip()
			key, value = line.split(":", 1)
			vars[key] = value
			used.append(value)

with open(args.blank, "r") as f:
	with open(args.out, "w") as g:
		for line in f:
			line = re.sub("\$[0-9][0-9][0-9]", replace, line)
			g.write(line)
