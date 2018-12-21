import argparse
import re
import xxhash
import random
import json

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
parser.add_argument("-c", "--config", help = "Config file strings are filled from")
args = parser.parse_args()

gen = args.generation

def replace(match):
	global vars
	global gen
	key = match.group()
	if key not in vars:
		gen(key)
	return vars[key]

def str_replace(match):
	global strings
	key = match.group().lower()
	return obfstr(strings[key])

def obfstr(f_str):
	global cur
	rand = str(random.random()) + cur
	rand = str(xxhash.xxh64(rand).hexdigest())
	cur = str(xxhash.xxh64(rand).hexdigest())
	i = 0
	o_str = ""
	for c in f_str:
		o_str += rand[i % len(rand)]
		o_str += c
		i += 1
	o_str += rand[i % len(rand)]
	return o_str

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

if args.config:
	with open(args.config, "r") as f:
		conf = f.read()
		strings = json.loads(conf)
		for key in strings:
			used.append(strings[key])

with open(args.blank, "r") as f:
	with open(args.out, "w") as g:
		for line in f:
			if args.config:
				for key in strings:
					line = re.sub(key.upper(), str_replace, line)
			line = re.sub("\$[0-9][0-9][0-9]", replace, line)
			g.write(line)
