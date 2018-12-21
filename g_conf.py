import json
import xxhash
import random
import argparse
import base64
import os
import getpass
from github3 import authorize

parser = argparse.ArgumentParser(description = "Generates wendigo config files")
parser.add_argument("-s", "--seed", help = "Seed for random number generation")
parser.add_argument("-o", "--out", default = "conf.ig", help = "Out file")
parser.add_argument("-c", "--config", help = "Prefilled config options")
parser.add_argument("-k", "--key", default = "pk.o", help = 
	"Out file for private key")
parser.add_argument("-g", "--gen", default = "g_pk.py", help = 
	"Name of key generation script (uses default options except for out file)")
parser.add_argument("-p", "--pk", action = "store_true", help = 
	"Generate a public key")
parser.add_argument("-t", "--token", action = "store_true", help = 
	"Generate a GitHub token (requires username in config file)")
args = parser.parse_args()

def gk_hash():
	global cur
	global used
	while True:
		rand = str(random.random()) + cur
		rand = xxhash.xxh64(rand).hexdigest()
		curr = xxhash.xxh64(rand).hexdigest()
		if rand not in used:
			used.append(rand)
			return rand

random.seed(args.seed)
options = {}
used = []
keys = ["mod", "config", "data", "repo", "usr", "pwd", "fn_s", "id_s"]
cur = xxhash.xxh64(str(random.random())).hexdigest()

if args.config:
	with open(args.config, "r") as f:
		conf = f.read()
		options = json.loads(conf)
		for key in options:
			used.append(options[key])

for key in keys:
	if key not in options:
		options[key] = gk_hash()
		if key == "mod" or key == "config" or key == data:
			options[key] += "/"

if "token" not in options:
	if args.token:
		try:
			p = getpass.getpass("GitHub password: ")
			auth = authorize(options["usr"], p, scopes = ["public_repo"])
			options["token"] = base64.b64encode(auth.token)
		except:
			options["token"] = "INSERT TOKEN (base64 encoded)"
	else:
		options["token"] = "INSERT TOKEN (base64 encoded)"

if "p_k" not in options:
	if args.pk:
		try:
			s = "python " + args.gen + " -o " + args.key
			k = os.popen(s).read()
			options["p_k"] = base64.b64encode(k)
		except:
			options["p_k"] = "INSERT PUBLIC KEY (base64 encoded)"
	else:
		options["p_k"] = "INSERT PUBLIC KEY (base64 encoded)"


if "sleep" not in options:
	slp = random.randint(600, 1200)
	options["sleep"] = str(slp)

if "imp" not in options:
	options["imp"] = "import %s"

if "size" not in options:
	sz = random.randint(180, 230)
	options["size"] = str(sz)

j = json.dumps(options, indent = 2, separators = (',', ':'))
with open(args.out, "w") as f:
	f.write(j)
