import Queue
import time
import re
import xxhash

class Config:
	def __init__(self):
		self.mod = ""
		self.config = ""
		self.data = ""
		self.usr = ""
		self.pwd = ""
		self.repo = ""
		self.branch = ""
		self.pk = ""
		self.fn_s = ""
		self.id_s = ""
		self.modules = []
		self.tasks = Queue.Queue()
		self.id = new_id()

	def new_id(self):
		i_time = int(time.time())
		t_id = str(i_time) + fixstr(self.id_s)
		self.id = xxhash.xxh64(t_id).hexdigest()

	def my_id(self):
		return xxhash.xxh64(self.id).hexdigest()

	def my_mod(self):
		return fixstr(self.mod)

	def new_mod(self, new):
		self.mod = new
		return

	def my_config(self):
		return fixstr(self.config) + my_id()

	def new_config(self, new):
		self.config = new
		return

	def my_data(self):
		return fixstr(self.data) + my_id() + "/" + new_fn()

	def new_data(self, new):
		self.data = new
		return

	def my_usr(self):
		return fixstr(self.usr)

	def new_usr(self, new):
		self.usr = new
		return

	def my_pwd(self):
		return xxhash.xxh64(fixstr(self.pwd)).hexdigest()

	def new_pwd(self, new):
		self.pwd = new
		return

	def my_repo(self):
		return fixstr(self.repo)

	def new_repo(self, new):
		self.repo = new
		return

	def my_branch(self):
		return fixstr(self.branch)

	def new_branch(self, new):
		self.branch = new
		return

	def my_pk(self):
		return base64.b64decode(self.pk)

	def new_pk(self, new):
		self.pk = new
		return

	def new_fn(self):
		i_time = int(time.time())
		fn = str(i_time) + fixstr(self.fn_s)
		return xxhash.xxh64(fn).hexdigest()

	def my_com(self):
		com = str(time.time())
		return xxhash.xxh64(com).hexdigest()

	def fixstr(self, t_str):
		for c in t_str:
			if re.match("[a-zA-Z_./]", c) != None:
				n_str += c
		return n_str
