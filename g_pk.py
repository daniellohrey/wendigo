import sys
import base64
import argparse
from Crypto.PublicKey import RSA

parser = argparse.ArgumentParser(description = "Generates RSA key pairs, "\
	"or takes private key and calculates public key")
parser.add_argument("-k", "--key", type = int, default = 2048, 
	help = "key size to generate (default is 2048)")
parser.add_argument("-c", "--calculate", action = "store_true", 
	help = "Calculate public key from private key instead of generating key pair")
parser.add_argument("-o", "--out", default = "pk.o", 
	help = "Private key file to write to / read from")
parser.add_argument("-p", "--public", 
	help = "Print (unencoded) public key to file instead of stdout (base64 encoded)")
args = parser.parse_args()

if args.calculate:
	if args.out == "pk.o":
		print "Need to specify private key file with -o"
		sys.exit()
	with open(args.out, "r") as f:
		priv = f.read()
		key = RSA.importKey(priv)
		pub = key.publickey().exportKey("PEM")
else:
	key = RSA.generate(args.key, e = 65537)
	priv = key.exportKey("PEM")
	pub = key.publickey().exportKey("PEM")
	with open(args.out, "w") as f:
		f.write(priv)

if args.public:
	with open(args.public, "w") as g:
		g.write(pub)
else:
	print base64.b64encode(pub)
