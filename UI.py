import wx
import shelve, os
from shutil import copyfile
import wallpaper

HEADER_TEXT = "Choose your daytime and nighttime wallpapers."
LEFT_SPACING = 20
ON = True
OFF = False

path = os.getenv('APPDATA').rsplit("\\", 1)[0] + "\\Local\\Wallpaper Changer"

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
		return 0

class myButton(wx.StaticBitmap):
	def __init__(self, panel, img_png, id):
		wx.StaticBitmap.__init__(self, panel, -1, img_png)
		self.Bind(wx.EVT_LEFT_UP, self.click)
		self.id = id
	def click(self, event):
		self.Hide()
		self.other.Show()
		self.GetParent().Layout()
		if(self.id == ON): #On toggled -> turning off
			store("on", False)
		if(self.id == OFF): #Off toggled -> turning on
			store("on", True)

class myFrame(wx.Frame):
	def close(self, event):
		self.Close()
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(600, 500))
		
		panel = wx.Panel(self) 
		box = wx.BoxSizer(wx.VERTICAL) 
		
		#Create header text
		lbl = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER) 
		font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD) 
		lbl.SetFont(font) 
		lbl.SetLabel(HEADER_TEXT) 
		lbl.Wrap(600)
		
		#Create message
		# lbl5 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER) 
		# font5 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_NORMAL) 
		# lbl5.SetFont(font5) 
		# lbl5.SetLabel("(Changes may take up to a minute to take effect)") 
		# lbl5.Wrap(600)
		
		#Create explanation label
		lbl4 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER) 
		font4 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_NORMAL) 
		lbl4.SetFont(font4) 
		lbl4.SetLabel("Turn wallpaper changer on or off") 
		lbl4.Wrap(600)
		
		#Load on/off button
		#on_button = wx.StaticBitmap(panel, -1, on_png)
		on_png = wx.Image('C:/Program Files/Wallpaper Changer/on.png').ConvertToBitmap()
		off_png = wx.Image('C:/Program Files/Wallpaper Changer/off.png').ConvertToBitmap()
		on_button = myButton(panel, on_png, ON)
		off_button = myButton(panel, off_png, OFF)
		on_button.other = off_button
		off_button.other = on_button
		on_status = retrieve("on");
		if(on_status == True):
			off_button.Hide()
		else:
			on_button.Hide()
		#off_button = wx.StaticBitmap(panel, -1, off_png)
		
		
		#Create daytime label
		lbl2 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER) 
		font2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_NORMAL) 
		lbl2.SetFont(font2) 
		lbl2.SetLabel("Daytime") 
		lbl.Wrap(600)
		
		#Create Nightime label
		lbl3 = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER) 
		font2 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_NORMAL) 
		lbl3.SetFont(font2) 
		lbl3.SetLabel("Nighttime") 
		lbl.Wrap(600)
		
		#Create two file picker buttons
		#set them to be equal to currently saved paths
		last_daytime = retrieve("daytime")
		last_nighttime = retrieve("nighttime")
		if(last_daytime == 0):
			last_daytime = "C:" #If last path not found just set it to open on C drive
		if(last_nighttime == 0):
			last_nighttime = "C:" 
		allowed = "Image files (*.jpg;*.jpeg;*.png;*.gif)|*.jpg;*.jpeg;*.png;*.gif"
		filepicker1 = wx.FilePickerCtrl(panel, -1, last_daytime, "Choose daytime wallpaper", allowed)
		filepicker2 = wx.FilePickerCtrl(panel, -1, last_nighttime, "Choose nighttime wallpaper", allowed)
		filepicker1.SetInitialDirectory(last_daytime)
		filepicker1.SetPath(last_daytime)
		filepicker2.SetInitialDirectory(last_nighttime)
		filepicker2.SetPath(last_nighttime)
	
		
		
		#Close button
		closeBtn = wx.Button(panel, -1, "OK")
		closeBtn.Bind(wx.EVT_BUTTON, self.close)
		closeBtn.SetDefault()
		
		#Lay everything out
		box.AddSpacer(15)
		box.Add(lbl, 0, wx.ALIGN_CENTER)
		box.AddSpacer(50)
		box.Add(lbl4, 0, wx.LEFT, LEFT_SPACING)
		box.AddSpacer(5)
		box.Add(on_button, 0, wx.LEFT, LEFT_SPACING)
		box.Add(off_button, 0, wx.LEFT, LEFT_SPACING)
		box.AddSpacer(30)
		box.Add(lbl2, 0, wx.LEFT, LEFT_SPACING)
		box.Add(filepicker1, 0, wx.LEFT, LEFT_SPACING)
		box.AddSpacer(50)
		box.Add(lbl3, 0, wx.LEFT, LEFT_SPACING)
		box.Add(filepicker2, 0, wx.LEFT, LEFT_SPACING)
		box.AddSpacer(30)
		# box.Add(lbl5, 0, wx.LEFT, LEFT_SPACING)
		box.AddSpacer(15)
		box.Add(closeBtn, 0, wx.ALIGN_CENTER)
		
		panel.SetSizer(box)
		self.SetBackgroundColour("white")
		
		#panel.Add(wx.FilePickerCtrl)
		
		filepicker1.Bind(wx.EVT_FILEPICKER_CHANGED, SetPath)
		filepicker2.Bind(wx.EVT_FILEPICKER_CHANGED, SetPath2)
		self.Show(True)
		
def SetPath(event):
	global path
	pathname = event.GetPath()
	if(pathname.endswith((".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".gif", ".GIF"))):
		print(pathname)
		store("daytime", pathname)
		copyfile(pathname, path + "/daytime.jpg")
		wallpaper.comb()
def SetPath2(event):
	global path
	pathname = event.GetPath()
	if(pathname.endswith((".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".gif", ".GIF"))):
		print(pathname)
		store("nighttime", pathname)
		copyfile(pathname, path + "/nighttime.jpg")
		wallpaper.comb()
	
app = wx.App(False)
frame = myFrame(None, "Sunrise/Sunset Wallpaper Changer")
app.MainLoop()