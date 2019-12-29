import ctypes, schedule, time, ephem, geocoder
from datetime import datetime
import shelve, os

#Get the Appdata path where files are stored
path = os.getenv('APPDATA').rsplit("\\", 1)[0] + "\\Local\\Wallpaper Changer"
DAY = path + "/daytime.jpg" #the wallpaper will change to this after sunrise
NIGHT = path + "/nighttime.jpg" #the wallpaper will change to this after sunset

me = ephem.Observer()
def store(key, entry):
	global path
	shelfFile = shelve.open(path + "/data")
	shelfFile[key] = entry
	shelfFile.close()
def retrieve(key):
	shelfFile = shelve.open(path + "/data")
	try:
		return shelfFile[key]
	except:
		print("Invalid Key")
		return -1

def updateLocation():
	global me
	try:
		g = geocoder.ip("me") 
		currentLocation = g.latlng
		me.lat = repr(currentLocation[0])
		me.lon = repr(currentLocation[1]) #set current location based on geocoder api
	except: 
		"""
		If theres no Internet, me.lat and me.lon will very likely still hold the last past value. 
		If they don't, check cache
		If that fails too (super unlikely), give up
		"""
		
		print("Dude, where's my Internet")
		if(me.lat == 0.0 or me.lon == 0):
			me.lat = retrieve("lat")
			me.lon = retrieve("lon")
			if(me.lat == -1 or me.lon == -1):
				print("Now we're really screwed")
				me.lat = "1.0"
				me.lon = "-1.0"
	print("Updating location!")
	#hardcode these (Fremont) in case Internet is down

	
#calculate when rising and setting is
def calcTimes():
	global me
	rising = me.next_rising(ephem.Sun())
	r = ephem.localtime(rising)
	
	timerise = r - datetime.now()
	sunrise = r.strftime("%H:%M")
	
	setting = me.next_setting(ephem.Sun())
	s = ephem.localtime(setting)
	sunset = s.strftime("%H:%M")
	timeset = s - datetime.now()
	
	if(timeset.seconds < timerise.seconds):
		changeToDay()
	else:
		changeToNight()
	print(sunrise, sunset)
	
def changeToDay():
	ctypes.windll.user32.SystemParametersInfoW(20, 0, DAY, 0)
	# return schedule.CancelJob
	
def changeToNight():
	ctypes.windll.user32.SystemParametersInfoW(20, 0, NIGHT, 0)
	# return schedule.CancelJob
	
#store the location of user in case the Internet goes down
def cacheLoc():
	print("Storing")
	try:
		g = geocoder.ip("me") 
		currentLocation = g.latlng
		store("lat", repr(currentLocation[0]))
		store("lon", repr(currentLocation[1])) #set current location based on geocoder api
	except: 
		"""
		If theres no Internet, me.lat and me.lon will very likely still hold the last past value. 
		If they don't, set to Fremont location
		"""
		print("Dude, where's my Internet")
def comb():

	state = retrieve("on")
	paths_set1 = retrieve("daytime")
	paths_set2 = retrieve("nighttime")
	if(state == -1):
		store("on", False)
	print(paths_set1)
	if(state == True and paths_set1 != -1 and paths_set2 != -1):
		updateLocation()
		calcTimes()
	else:
		print("off or error")

#every 1 minute check 
if __name__ == "__main__":
	schedule.every(1).minutes.do(comb)
	schedule.every(1).minutes.do(cacheLoc)

	updateLocation()
	calcTimes()

	while(True):
		schedule.run_pending()
		time.sleep(1)