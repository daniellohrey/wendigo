import zlib
import base64
import argparse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

parser = argparse.ArgumentParser(description = "Decrypts specified files"
parser.add_argument("-p", "--private", default = "pk.o", 
	help = "File with private key")
parser.add_argument("-o", "--out", 
	help = "File to append results to (default is stdout")
parser.add_argument("-s", "--size", type = int, default = 256, help = 
	"Cipher block size")
parser.add_argument("files", nargs = "+", help = "Files to decrypt")
args = parser.parse_args()

with open(args.private, "r") as k:
	priv = k.read()
key = RSA.importKey(priv)
key = PKCS1_OAEP.new(key)

size = args.size
offset = 0
decrypted = ""

for fn in files:
	with open(fn, "r") as f:
		data = f.read()
	data = base64.b64decode(data)

	while offset < len(data):
		decrypted += key.decrypt(data[offset:offset + size])
		offset += size

	plain = zlib.decompress(decrypted)

	if args.out:
		with open(args.out, "a") as f:
			f.write(plain)
			f.write("\n")
	else:
		print plain
		print
