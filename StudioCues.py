from tkinter import *
from tkinter import filedialog
import screeninfo
import configparser
import collections

class masterWindow:
	configuration = ""
	version = "2.0.0"	
	
	def __init__(this,master=None):
		this.SlaveWindowDanceLists = {
							    'current':{'content': StringVar(),'locked':False},
								'next1':{'content':StringVar(),'locked':False},
								'next2':{'content':StringVar(),'locked':False},
								'next3':{'content':StringVar(),'locked':False},
								'next4':{'content': StringVar(),'locked':False}}

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
							'defaultqueue':'none'
						},'keybindings':{
							'savequeue':'<Control-s>',
							'openqueue':'<Control-o>',
							'enqueue':'<Key q>',
							'enqueuetop':'<Key-t>',
							'advancequeue':'<Key-n>'
						},'modules':{
							'tablet_mode_enabled':'true'}}
		master.title("StudioCues")
		this.writeDefaultConfigValuesIfNotPresent()
		this.doConfigRead()
		this.SlaveWindow = Toplevel(master)
		this.SlaveWindow.title("StudioCues Slave Window")
		this.danceQueue = collections.deque()
		this.MasterDanceList = this.getDanceStylesFromFile()
		this.initSlaveWindow()
		this.prep(master)

	def doConfigRead(this):
		configFile = open('StudioCues.configuration', 'r')
		this.configuration = configparser.ConfigParser()
		this.configuration.read_file(configFile)
		#for sect in this.configuration.keys():
		#	print(sect,":")
		#	for opt in this.configuration[sect].keys():
		#		print('    '+opt+': '+this.configuration[sect][opt])
		configFile.close()

	def writeDefaultConfigValuesIfNotPresent(this): 
		this.configuration = configparser.ConfigParser()
		for k1 in this.defaultConfigOptions:
			if not this.configuration.has_section(k1):	
				this.configuration.add_section(k1)
			for k2 in this.defaultConfigOptions[k1]:
				if not this.configuration.has_option(k1, k2):
					this.configuration.set(k1, k2, this.defaultConfigOptions[k1][k2])
		for sect in this.configuration:
			print(sect,":")
		for opt in this.configuration[sect]:
			print('    '+opt+': '+this.configuration[sect][opt])
		this.writeConfiguration()

	def initSlaveWindow(this):
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

	def writeConfiguration(self, location='StudioCues.configuration'):
		with open(location, 'w+') as configFile:
			self.configuration.write(configFile)

	def getDanceStylesFromFile(self, file='DanceStyles.list') -> dict:
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

	def createQueueLabelText(this) -> str:
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
		this.danceQueueLabelText.set(this.createQueueLabelText())

	def registerNewDance(this, Dance:str):
		this.registerNewDanceTemp(Dance)
		with (open('DanceStyles.list','a')) as listFile:
			listFile.write('\n' + Dance)

	def registerNewDanceTemp(this, Dance:str):
		index = max(this.MasterDanceList.keys()) + 1
		this.MasterDanceList[index] = Dance
		this.DanceListbox.insert(index, Dance)

	def doFileOpenPopup(self, startDir:str = '/', title:str = 'Select a file...', fileTypes:tuple = (('StudioCues Queue files','*.sc'),('All Files','*.*'))) -> str:
		return filedialog.askopenfilename(initialdir=startDir, title=title,filetypes=fileTypes)	

	def doFileSavePopup(self, startDir:str = '/', title:str = 'Select a file...', fileTypes:tuple = (('StudioCues Queue files','*.sc'),('All Files','*.*'))) -> str:
		return filedialog.asksaveasfilename(initialdir=startDir, title=title,filetypes=fileTypes)

	def saveCurrentQueue(this):
		location = this.doFileSavePopup()
		if not location.endswith(suffix=('.sc','.SC','.Sc','.sC')):
			location+='.sc'
		with open(location, 'w') as queueFile:
			queueFile.write(this.CurrentDance.get()+'\n')
			queueFile.write(this.nextDance1.get()+'\n')
			queueFile.write(this.nextDance2.get()+'\n')
			queueFile.write(this.nextDance3.get()+'\n')
			queueFile.write(this.nextDance4.get()+'\n')
			for v in this.danceQueue:
				queueFile.write(v+'\n')
	
	def readQueueFile(this):
		location = this.doFileOpenPopup()
		with open(location,'r') as IOFile:
			temp = IOFile.read().split('\n')
			this.clearDanceQueue()
			for dance in temp:
				this.addDanceToQueue(dance)

	def updateDanceList(this):
		location = this.doFileOpenPopup()
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

	def createMenuBar(this, root:Tk):
		this.menuBar = Menu(root)
		this.FileMenu = Menu(this.menuBar, tearoff=0)
		this.FileMenu.add_command(label='Save Queue',underline=1,command=this.saveCurrentQueue)
		this.FileMenu.add_command(label='Open Queue',underline=1, command=this.readQueueFile)
		this.menuBar.add_cascade(label="File",menu=this.FileMenu)
		root.config(menu=this.menuBar)

	def createDanceRegistrationArea(this, root:Tk):
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

	def createDanceListArea(this, root:Tk):
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
		this.danceQueueLabelText.set(this.createQueueLabelText())
		this.danceQueueLabel = Label(this.listArea, textvariable=this.danceQueueLabelText,
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])
		for key in this.MasterDanceList.keys():
			this.DanceListbox.insert(key, this.MasterDanceList[key])
		this.DanceListbox.pack(side=LEFT, fill=BOTH,expand=1)
		this.danceQueueLabel.pack(side=LEFT,fill=BOTH,expand=0)
		this.listArea.pack(side=TOP,fill=BOTH,expand=1)

	def createDanceControlArea(this, root:Tk):
		this.controlArea:Frame = Frame(root)
		this.addDanceArea:Frame = Frame(this.controlArea)
		this.AddDanceButton:Button = Button(this.addDanceArea,
							   text="Add to Queue", 
							   relief=GROOVE, 
							   height=7,
							   command=lambda:this.masterWindowAddDanceCallback(this.DanceListbox.get(ACTIVE)),
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
								command=this.masterWindowNextDanceCallback,
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])
		this.RemoveLastDanceButton = Button(this.controlArea,
										text="Remove the \nLast Dance",
										relief=GROOVE,
										height=7,
										command=this.masterWindowRemoveLastAddedDanceCallback,
										bg=this.configuration['UI_UX']['master_window_background'],
										fg=this.configuration['UI_UX']['master_window_foreground'])
		this.AddDanceToTopButton.pack(side=TOP,fill=BOTH, expand=0)
		this.AddDanceButton.pack(side=TOP,fill=BOTH, expand=1)
		this.addDanceArea.pack(side=LEFT, fill=X, expand=1)
		this.AdvanceDanceButton.pack(side=LEFT, fill=BOTH, expand=1)
		this.RemoveLastDanceButton.pack(side=LEFT, fill=BOTH, expand=1)
		this.controlArea.pack(side=TOP,fill=BOTH,expand=0)

	def prep(this, root:Tk):
		this.createMenuBar(root)
		this.createDanceRegistrationArea(root)
		this.createDanceListArea(root)
		this.createDanceControlArea(root)
		this.registerKeyCommands(root)

	def registerKeyCommands(this, root:Tk):
		root.bind(this.configuration['keybindings']['openqueue'], lambda event: this.readQueueFile())
		root.bind(this.configuration['keybindings']['savequeue'], lambda event: this.saveCurrentQueue())
		root.bind(this.configuration['keybindings']['enqueue'], lambda event:this.addDanceToQueue(this.DanceListbox.get(this.DanceListbox.curselection())))		
		root.bind(this.configuration['keybindings']['enqueuetop'], lambda event:this.addDanceToTop(this.DanceListbox.get(this.DanceListbox.curselection())))
		root.bind(this.configuration['keybindings']['advanceQueue'], lambda event:this.advanceDanceQueue())

	def masterWindowAddDanceCallback(this, index:int):
		this.addDanceToQueue(index)

	def masterWindowNextDanceCallback(this):
		this.advanceDanceQueue()

	def masterWindowRemoveLastAddedDanceCallback(this):
		this.removeLastAddedDance()
	
	def changeDanceListCallback(this):
		pass

def main():
	root = Tk()
	master = masterWindow(root)
	root.mainloop()
	master.writeConfiguration()

main()