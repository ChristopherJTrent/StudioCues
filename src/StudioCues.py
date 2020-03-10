from tkinter import *
from tkinter import filedialog
from pyupdater.client import Client
from client_config import ClientConfig
from preferenceswindow import PreferencesWindow
import screeninfo
import configparser
import collections
from os import path

class masterWindow:
	
	def doUpdateCheckAndApply(this):
		def print_status_info(info):
			total = info.get(u'total')
			downloaded = info.get(u'downloaded')
			status = info.get(u'status')
			print(downloaded, total, status)
		client = Client(ClientConfig(), refresh=True, progress_hooks=[print_status_info])
		app_update=client.update_check(ClientConfig.APP_NAME, ClientConfig.APP_VERSION)
		#print(app_update)
		if app_update is not None:
			#print('not none')
			app_update.download()
			if app_update.is_downloaded():
				#print('isdownloaded')
				app_update.extract_restart()
		else:
			#print('no updates')
			pass
	def __init__(this,master=None):
		if master is None:
			this.master = Tk()
		else:
			this.master = master
		this.doUpdateCheckAndApply()
		this.defaultConfigOptions = {'UI_UX':{
							'font_family':'Helvetica',
							'font_size':'110',
							'font_size_small':'80',
							'listbox_font_size':'12',
							'tablet_listbox_font_size':'40',
							'slave_window_background':'#300A24',
							'slave_window_foreground':'#FFFFFF',
							'slave_window_active_background':'#300A24',
							'slave_window_active_foreground':'#FFC83D',
							'master_window_background':'#300A24',
							'master_window_foreground':'#FFFFFF',
							'data_entry_background':'#55113F',
							'data_entry_foreground':'#FFFFFF',
							'currently_playing':'Now Playing:'
						},'startup':{
							'defaultqueue':'none',
							'PreferencesLocation':'cfg/StudioCuesDefault.configuration',
						},'keybindings':{
							'savequeue':'<Control-s>',
							'openqueue':'<Control-o>',
							'enqueue':'<Key-q>',
							'enqueuetop':'<Key-t>',
							'advancequeue':'<Key-n>'
						},'modules':{
							'tablet_mode_enabled':'false'}}
		
		if not path.exists(this.defaultConfigOptions['startup']['PreferencesLocation']):
			open(this.defaultConfigOptions['startup']['PreferencesLocation'], 'w+').close()
		this.configuration = configparser.ConfigParser()	
		this.__writeDefaultConfigValuesIfNotPresent()
		this.__doConfigRead()
		this.danceQueue = collections.deque()
		this.MasterDanceList = this.getDanceStylesFromFile()
		this.prep(this.master)

	def __doConfigRead(this):
		configFile = open(this.defaultConfigOptions['startup']['PreferencesLocation'], 'r')
		this.configuration = configparser.ConfigParser()
		this.configuration.read_file(configFile)
		if this.configuration.has_section('startup'):
			if this.configuration.has_option('startup','PreferencesLocation'):
				if this.configuration['startup']['PreferencesLocation'] != this.defaultConfigOptions['startup']['PreferencesLocation']:
					try:
						with open(this.configuration['startup']['PreferencesLocation']) as INIFile:
							this.configuration.clear()
							this.configuration.read_file(INIFile)
					except:
						pass
		configFile.close()
		#for sect in this.configuration.keys():
		#	print(sect,":")
		#	for opt in this.configuration[sect].keys():
		#		print('    '+opt+': '+this.configuration[sect][opt])

	def moveConfig(this, location):
		with open(this.defaultConfigOptions['startup']['PreferencesLocation']) as defCFG:
			tempConfig = configparser.ConfigParser()
			tempConfig.read_file(defCFG)
			tempConfig['startup']['PreferencesLocation'] = location
			tempConfig.write(defCFG)

	def __writeDefaultConfigValuesIfNotPresent(this): 
		for k1 in this.defaultConfigOptions:
			if not this.configuration.has_section(k1):	
				this.configuration.add_section(k1)
			for k2 in this.defaultConfigOptions[k1]:
				if not this.configuration.has_option(k1, k2):
					this.configuration.set(k1, k2, this.defaultConfigOptions[k1][k2])
		this.writeConfiguration()

	def __initSlaveWindow(this):
		this.SlaveWindow.geometry("500x500")
		this.CurrentDance = StringVar()
		this.CurrentDanceLabel = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_active_background'],
									fg=this.configuration['UI_UX']['slave_window_active_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
										this.configuration['UI_UX']['font_size']),
									textvariable=this.CurrentDance)
		this.nextDance1 = StringVar()
		this.nextDance2 = StringVar()
		this.nextDance3 = StringVar()
		this.nextDance4 = StringVar()
		this.NextDanceLabel1 = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_background'],
									fg=this.configuration['UI_UX']['slave_window_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
								 		this.configuration['UI_UX']['font_size_small']),
									textvariable=this.nextDance1)		
		this.NextDanceLabel2 = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_background'],
									fg=this.configuration['UI_UX']['slave_window_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
										this.configuration['UI_UX']['font_size_small']),
									textvariable=this.nextDance2)		
		this.NextDanceLabel3 = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_background'],
									fg=this.configuration['UI_UX']['slave_window_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
									this.configuration['UI_UX']['font_size_small']),
									textvariable=this.nextDance3)		
		this.NextDanceLabel4 = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_background'],
									fg=this.configuration['UI_UX']['slave_window_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
									this.configuration['UI_UX']['font_size_small']),
									textvariable=this.nextDance4)
		this.CurrentDanceLabel.pack(fill=BOTH,expand=1)
		this.NextDanceLabel1.pack(fill=BOTH, expand=1)
		this.NextDanceLabel2.pack(fill=BOTH, expand=1)
		this.NextDanceLabel3.pack(fill=BOTH, expand=1)
		this.NextDanceLabel4.pack(fill=BOTH, expand=1)
		for mon in screeninfo.screeninfo.get_monitors():
			if mon.x > 0:
				this.SlaveWindow.overrideredirect(1)
				this.SlaveWindow.geometry(f"{mon.width}x{mon.height}+{mon.x}+0")

	def writeConfiguration(self, location=None):
		if location is None:
			location = self.defaultConfigOptions['startup']['PreferencesLocation']
		with open(location, 'w+') as configFile:
			self.configuration.write(configFile)

	def getDanceStylesFromFile(self, file='DanceStyles.list') -> dict:
		if not path.exists('DanceStyles.list'):
			open('DanceStyles.list', 'w+').close()
			return dict()
		outDictionary = {}
		iterator = 0
		dances = open(file,'r')
		danceList = dances.read().split('\n')
		for dance in danceList:
			outDictionary[iterator] = dance
			iterator += 1
		dances.close()
		return outDictionary

	def addDanceToQueue(this, Dance:str):
		if Dance == '':
			return
		if this.CurrentDance.get() == "":
			this.CurrentDance.set(Dance)
		elif this.nextDance1.get() == "":
			this.nextDance1.set(Dance)
		elif this.nextDance2.get() == "":
			this.nextDance2.set(Dance)		
		elif this.nextDance3.get() == "":
			this.nextDance3.set(Dance)		
		elif this.nextDance4.get() == "":
			this.nextDance4.set(Dance)
		else:
			this.danceQueue.append(Dance)
		this.updateMasterWindowDanceQueueLabel()

	def addDanceToTop(this, Dance:str):
		if Dance == '':
			return
		this.danceQueue.appendleft(this.nextDance4.get())
		this.nextDance4.set(this.nextDance3.get())
		this.nextDance3.set(this.nextDance2.get())
		this.nextDance2.set(this.nextDance1.get())
		this.nextDance1.set(this.CurrentDance.get())
		this.CurrentDance.set(Dance)
		this.updateMasterWindowDanceQueueLabel()

	def advanceDanceQueue(this):
		this.CurrentDance.set(this.nextDance1.get())
		this.nextDance1.set(this.nextDance2.get())
		this.nextDance2.set(this.nextDance3.get())
		this.nextDance3.set(this.nextDance4.get())
		if len(this.danceQueue) == 0:
			this.nextDance4.set("")
		else:
			this.nextDance4.set(this.danceQueue.popleft())
		this.updateMasterWindowDanceQueueLabel()

	def removeLastAddedDance(this):
		if len(this.danceQueue) >= 1:
			this.danceQueue.pop()	
		elif len(this.nextDance4.get())>0:
			this.nextDance4.set("")	
		elif len(this.nextDance3.get())>0:
			this.nextDance3.set("")		
		elif len(this.nextDance2.get())>0:
			this.nextDance2.set("")		
		elif len(this.nextDance1.get())>0:
			this.nextDance1.set("")
		elif len(this.CurrentDance.get())>0:
			this.CurrentDance.set("")
		this.updateMasterWindowDanceQueueLabel()

	def __createQueueLabelText(this) -> str:
		while True:
			try:
				this.danceQueue.remove('')
			except ValueError:
				break
		outputString = ""
		outputString+= this.configuration['UI_UX']['currently_playing'] + '\n'
		outputString+= this.CurrentDance.get() + '\n'
		outputString+= this.nextDance1.get() + '\n'
		outputString+= this.nextDance2.get() + '\n'
		outputString+= this.nextDance3.get() + '\n'
		outputString+= this.nextDance4.get() + '\n'
		for dance in this.danceQueue:
			outputString+=dance + '\n'
		return outputString

	def updateMasterWindowDanceQueueLabel(this):
		this.danceQueueLabelText.set(this.__createQueueLabelText())

	def registerNewDance(this, Dance:str):
		this.registerNewDanceTemp(Dance)
		with (open('DanceStyles.list','a')) as listFile:
			listFile.write(Dance + '\n')

	def registerNewDanceTemp(this, Dance:str):
		if not this.MasterDanceList:
			index = 0
		else:
			index = max(this.MasterDanceList.keys()) + 1
		this.MasterDanceList[index] = Dance
		this.DanceListbox.insert(index, Dance)

	def __doFileOpenPopup(self, startDir:str = '/', title:str = 'Select a file...', fileTypes:tuple = (('StudioCues Queue files','*.sc'),('All Files','*.*'))) -> str:
		return filedialog.askopenfilename(initialdir=startDir, title=title,filetypes=fileTypes)	

	def __doFileSavePopup(self, startDir:str = '/', title:str = 'Select a file...', fileTypes:tuple = (('StudioCues Queue files','*.sc'),('All Files','*.*'))) -> str:
		return filedialog.asksaveasfilename(initialdir=startDir, title=title,filetypes=fileTypes)

	def saveCurrentQueue(this):
		location = this.__doFileSavePopup()
		this._saveCurrentQueue(location)
	def _saveCurrentQueue(this, location, mode='w+'):
		if not location.lower().endswith('.sc'):
			location+='.sc'
		with open(location, mode) as queueFile:
			queueFile.write(this.CurrentDance.get()+'\n')
			queueFile.write(this.nextDance1.get()+'\n')
			queueFile.write(this.nextDance2.get()+'\n')
			queueFile.write(this.nextDance3.get()+'\n')
			queueFile.write(this.nextDance4.get()+'\n')
			for v in this.danceQueue:
				queueFile.write(v+'\n')
	def readQueueFile(this):
		location = this.__doFileOpenPopup()
	def _readQueueFile(this, location, mode='r'):
		with open(location,mode) as IOFile:
			temp = IOFile.read().split('\n')
			this.clearDanceQueue()
			for dance in temp:
				this.addDanceToQueue(dance)
	def updateDanceList(this):
		location = this.__doFileOpenPopup(fileTypes=(('StudioCues Dance List files','*.scd'),('All Files','*.*')))
		this.MasterDanceList = this.getDanceStylesFromFile(location)
		this.DanceListbox.delete(0,END)
		for key in this.MasterDanceList.keys():
			this.DanceListbox.insert(key, this.MasterDanceList[key])



	def clearDanceQueue(this):
		this.CurrentDance.set('')
		this.nextDance1.set('')
		this.nextDance2.set('')
		this.nextDance3.set('')
		this.nextDance4.set('')
		this.danceQueue.clear()

	def __createMenuBar(this, root:Tk):
		this.menuBar = Menu(root)
		this.FileMenu = Menu(this.menuBar, tearoff=0)
		this.FileMenu.add_command(label='Save Queue',underline=2,command=this.saveCurrentQueue)
		this.FileMenu.add_command(label='Open Queue',underline=1, command=this.readQueueFile)
		this.menuBar.add_cascade(label="File",menu=this.FileMenu)
		this.menuBar.add_command(label = 'Preferences', command=this.openPreferencesCallback)
		root.config(menu=this.menuBar)

	def __createDanceRegistrationArea(this, root:Tk):
		this.RegisterDanceArea = Frame(root)
		this.RegisterDanceActionArea = Frame(this.RegisterDanceArea)
		this.RegisterDanceTextBox = Entry(this.RegisterDanceArea, 
									bg=this.configuration['UI_UX']['Data_Entry_Background'],
									fg = this.configuration['UI_UX']['Data_Entry_Foreground'])
		this.RegisterDancePermanentButton = Button(this.RegisterDanceActionArea,
												bg=this.configuration['UI_UX']['master_window_background'],
												fg=this.configuration['UI_UX']['master_window_foreground'],
												text="Add dance\n(Permanent)",
												command=lambda:this.registerNewDance(this.RegisterDanceTextBox.get()))
		this.RegisterDanceTemporaryButton = Button(this.RegisterDanceActionArea,
												bg=this.configuration['UI_UX']['master_window_background'],
												fg=this.configuration['UI_UX']['master_window_foreground'],
												text="Add dance \n(Temp)",
												command=lambda:this.registerNewDanceTemp(this.RegisterDanceTextBox.get()))
		this.RegisterDancePermanentButton.pack(side=TOP, fill=BOTH, expand=1)
		this.RegisterDanceTemporaryButton.pack(side=TOP, fill=BOTH, expand=1)
		this.RegisterDanceTextBox.pack(side=LEFT, fill=BOTH, expand=1)
		this.RegisterDanceActionArea.pack(side=LEFT, fill=BOTH, expand=1)
		this.RegisterDanceArea.pack(side=TOP, fill=X, expand=0)

	def __createDanceListArea(this, root:Tk):
		this.listArea = Frame(root)
		this.DanceListboxScroll = Scrollbar(this.listArea,								
									  bg=this.configuration['UI_UX']['master_window_background'])
		this.DanceListboxScroll.pack(side=LEFT,fill=Y)
		this.DanceListbox = Listbox(this.listArea,
								font=(this.configuration['UI_UX']['font_family'],this.configuration['UI_UX']['tablet_listbox_font_size' if this.configuration['modules']['tablet_mode_enabled']=='true' else 'listbox_font_size']),
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'],
								yscrollcommand=this.DanceListboxScroll.set)
		this.DanceListboxScroll.config(command=this.DanceListbox.yview)
		this.danceQueueLabelText = StringVar(root)
		this.danceQueueLabelText.set(this.__createQueueLabelText())
		this.danceQueueLabel = Label(this.listArea, textvariable=this.danceQueueLabelText,
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])
		for key in this.MasterDanceList.keys():
			if not this.MasterDanceList[key] == "":
				this.DanceListbox.insert(key, this.MasterDanceList[key])
		this.DanceListbox.pack(side=LEFT, fill=BOTH,expand=1)
		this.danceQueueLabel.pack(side=LEFT,fill=BOTH,expand=0)
		this.listArea.pack(side=TOP,fill=BOTH,expand=1)

	def __createDanceControlArea(this, root:Tk):
		this.controlArea:Frame = Frame(root)
		this.addDanceArea:Frame = Frame(this.controlArea)
		this.AddDanceButton:Button = Button(this.addDanceArea,
							   text="Add to Queue", 
							   relief=GROOVE, 
							   height=7,
							   command=lambda:this.__masterWindowAddDanceCallback(this.DanceListbox.get(ACTIVE)),
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])		
		this.AddDanceToTopButton:Button = Button(this.addDanceArea,
							   text="Add to top \nof Queue", 
							   relief=GROOVE, 
							   height=7,
							   command=lambda:this.addDanceToTop(this.DanceListbox.get(ACTIVE)),
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])
		this.AdvanceDanceButton = Button(this.controlArea,
								  text="Next Dance",
								 relief=GROOVE,
								height=7,
								command=this.__masterWindowNextDanceCallback,
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])
		this.RemoveLastDanceButton = Button(this.controlArea,
										text="Remove the \nLast Dance",
										relief=GROOVE,
										height=7,
										command=this.__masterWindowRemoveLastAddedDanceCallback,
										bg=this.configuration['UI_UX']['master_window_background'],
										fg=this.configuration['UI_UX']['master_window_foreground'])
		this.AddDanceToTopButton.pack(side=TOP,fill=BOTH, expand=0)
		this.AddDanceButton.pack(side=TOP,fill=BOTH, expand=1)
		this.addDanceArea.pack(side=LEFT, fill=X, expand=1)
		this.AdvanceDanceButton.pack(side=LEFT, fill=BOTH, expand=1)
		this.RemoveLastDanceButton.pack(side=LEFT, fill=BOTH, expand=1)
		this.controlArea.pack(side=TOP,fill=BOTH,expand=0)

	def prep(this, root:Tk):
		this.configWindow = None
		this.master.title(f"StudioCues V.{ClientConfig.APP_VERSION}")
		this.SlaveWindow = Toplevel(this.master)
		this.SlaveWindow.title("StudioCues Slave Window")
		this.__initSlaveWindow()
		this.__createMenuBar(root)
		this.__createDanceRegistrationArea(root)
		this.__createDanceListArea(root)
		this.__createDanceControlArea(root)
		this.__registerKeyCommands(root)

	def reload(self):
		self._saveCurrentQueue('temp.sc')
		root = self.master
		for widget in root.winfo_children():
			widget.destroy()
		self.prep(root)
		self._readQueueFile('temp.sc')
	def __registerKeyCommands(this, root:Tk):
		root.bind(this.configuration['keybindings']['openqueue'], lambda event: this.readQueueFile())
		root.bind(this.configuration['keybindings']['savequeue'], lambda event: this.saveCurrentQueue())	
		for k in this.configuration['keybindings'].keys():
			this.RegisterDanceTextBox.bind(this.configuration['keybindings'][k], this.__TextBoxOverrideCallback)
		root.bind(this.configuration['keybindings']['enqueuetop'], this.__masterWindowEnqueueTopCallback)
		root.bind(this.configuration['keybindings']['enqueue'], this.__masterWindowAddDanceCallback)
		root.bind(this.configuration['keybindings']['advanceQueue'], lambda event:this.advanceDanceQueue())

	def __masterWindowAddDanceCallback(this, event):
		if this.DanceListbox.curselection == "":
			return
		else:
			this.addDanceToQueue(this.DanceListbox.get(this.DanceListbox.curselection()))
	
	def __masterWindowEnqueueTopCallback(this, event):
		if this.DanceListbox.curselection == "":
			return
		else:
			this.addDanceToTop(this.DanceListbox.get(this.DanceListbox.curselection()))

	def __TextBoxOverrideCallback(this, event):
		#print(__name__)
		if type(event.widget) == type(Entry()):
			event.widget.insert(len(event.widget.get()), event.char)
		return 'break'
	def __masterWindowNextDanceCallback(this):
		this.advanceDanceQueue()

	def __masterWindowRemoveLastAddedDanceCallback(this):
		this.removeLastAddedDance()
	
	def changeDanceListCallback(this):
		pass

	def openPreferencesCallback(self, event=None):
		if self.configWindow is None:
			self.configWindow = PreferencesWindow(self.master, self.configuration, self)
		else:
			self.configWindow.show()

def main():
	master = masterWindow()
	master.master.mainloop()
	master.writeConfiguration()

main()