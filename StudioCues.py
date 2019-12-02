from tkinter import *
import configparser
from queue import Queue

class masterWindow:
	configuration = ""
	def __init__(this,master=None):
		this.SlaveWindow = Toplevel(master)
		this.danceQueue = []
		this.doConfigRead()
		this.writeDefaultConfigValuesIfNotPresent()
		this.MasterDanceList = this.getDanceStylesFromFile()
		this.initSlaveWindow()
		this.prep(master)
	def doConfigRead(this):
		configFile = open('StudioCues.configuration', 'r')
		this.configuration = configparser.ConfigParser()
		this.configuration.read_file(configFile)
		configFile.close()
	def writeDefaultConfigValuesIfNotPresent(this): 
		configFile = open('StudioCues.configuration','w')
		if not this.configuration.has_section('UI_UX'):
			this.configuration.add_section('UI_UX')
		if not this.configuration.has_option('UI_UX','font_family'):
			this.configuration.set('UI_UX','font_family','Helvetica')
		if not this.configuration.has_option('UI_UX','font_size'):
			this.configuration.set('UI_UX','font_size','100')
		if not this.configuration.has_option('UI_UX','currently_playing'):
			this.configuration.set('UI_UX','currently_playing','Currently Playing:')
		if not this.configuration.has_option('UI_UX','next_up'):
			this.configuration.set('UI_UX','next_up','Coming up next:')
		if not this.configuration.has_option('UI_UX','slave_window_background'):
			this.configuration.set('UI_UX','slave_window_background','#300A24')
		if not this.configuration.has_option('UI_UX','slave_window_foreground'):
			this.configuration.set('UI_UX','slave_window_foreground',"#FFFFFF")
		if not this.configuration.has_option('UI_UX','master_window_background'):
			this.configuration.set('UI_UX','master_window_background',"#300A24")
		if not this.configuration.has_option('UI_UX','master_window_foreground'):
			this.configuration.set('UI_UX','master_window_foreground',"#FFFFFF")
		this.configuration.write(configFile)
		configFile.close()
	def initSlaveWindow(this):
		this.CurrentDanceInfoLabel = Label(this.SlaveWindow,
										 bg=this.configuration['UI_UX']['slave_window_background'],
										 fg=this.configuration['UI_UX']['slave_window_foreground'],
										 font=(this.configuration['UI_UX']['font_family'],
												this.configuration['UI_UX']['font_size']),
										 text=this.configuration['UI_UX']['currently_playing'])
		this.CurrentDance = StringVar()
		this.CurrentDanceLabel = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_background'],
									fg=this.configuration['UI_UX']['slave_window_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
										this.configuration['UI_UX']['font_size']),
									textvariable=this.CurrentDance)
		this.NextDanceInfoLabel = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_background'],
									fg=this.configuration['UI_UX']['slave_window_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
										this.configuration['UI_UX']['font_size']),
									text=this.configuration['UI_UX']['next_up'])
		this.NextDance = StringVar()
		this.NextDanceLabel = Label(this.SlaveWindow,
									bg=this.configuration['UI_UX']['slave_window_background'],
									fg=this.configuration['UI_UX']['slave_window_foreground'],
									font=(this.configuration['UI_UX']['font_family'],
										this.configuration['UI_UX']['font_size']),
									textvariable=this.NextDance)
		this.CurrentDanceInfoLabel.pack(fill=BOTH, expand=1)
		this.CurrentDanceLabel.pack(fill=BOTH,expand=1)
		this.NextDanceInfoLabel.pack(fill=BOTH,expand=1)
		this.NextDanceLabel.pack(fill=BOTH, expand=1)
		pass
	def getDanceStylesFromFile(self) -> dict:
		outDictionary = {}
		iterator = 0
		dances = open('DanceStyles.list','r')
		danceList = dances.read().split('\n')
		print(danceList)
		for dance in danceList:
			print(dance)
			outDictionary[iterator] = dance
			iterator += 1
		dances.close()
		return outDictionary
	def addDanceToQueue(this, Dance:str):
		if this.CurrentDance.get() == "":
			this.CurrentDance.set(Dance)
		elif this.NextDance.get()=="":
			this.NextDance.set(Dance)
		else:
			this.danceQueue.append(Dance)
		this.updateMasterWindowDanceQueueLabel()
	def advanceDanceQueue(this):
		this.CurrentDance.set(this.NextDance.get())
		if len(this.danceQueue)==0:
			this.NextDance.set("")
		else:
			this.NextDance.set(this.danceQueue[0])
			del this.danceQueue[0]
		this.updateMasterWindowDanceQueueLabel()
	def removeLastAddedDance(this):
		if len(this.danceQueue)>=1:
			del this.danceQueue[-1]
		elif len(this.NextDance.get())!=0:
			this.NextDance.set("")
		elif len(this.CurrentDance.get())!=0:
			this.CurrentDance.set("")
		this.updateMasterWindowDanceQueueLabel()
	def createQueueLabelText(this) -> str:
		outputString = ""
		outputString+= this.configuration['UI_UX']['currently_playing'] + '\n'
		outputString+= this.CurrentDance.get() + '\n'
		outputString+= this.configuration['UI_UX']['next_up'] + '\n'
		outputString+= this.NextDance.get() + '\n'
		for dance in this.danceQueue:
			outputString+=dance+'\n'
		return outputString
	def updateMasterWindowDanceQueueLabel(this):
		this.danceQueueLabelText.set(this.createQueueLabelText())
	def prep(this, root:Tk):
		print(this.MasterDanceList)
		this.listArea = Frame(root)
		this.DanceListbox = Listbox(this.listArea,
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])
		this.danceQueueLabelText = StringVar(root)
		this.danceQueueLabelText.set(this.createQueueLabelText())
		this.danceQueueLabel = Label(this.listArea, textvariable=this.danceQueueLabelText,
								bg=this.configuration['UI_UX']['master_window_background'],
								fg=this.configuration['UI_UX']['master_window_foreground'])
		this.controlArea = Frame(root)
		for key in this.MasterDanceList.keys():
			this.DanceListbox.insert(key, this.MasterDanceList[key])
		this.AddDanceButton = Button(this.controlArea, 
							   text="Add to Queue", 
							   relief=GROOVE, 
							   height=7,
							   command=lambda:this.masterWindowAddDanceCallback(this.DanceListbox.get(ACTIVE)),
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
		this.DanceListbox.pack(side=LEFT, fill=BOTH,expand=1)
		this.danceQueueLabel.pack(side=LEFT,fill=BOTH,expand=0)
		this.AddDanceButton.pack(side=LEFT,fill=X, expand=1)
		this.AdvanceDanceButton.pack(side=LEFT, fill=X, expand=1)
		this.RemoveLastDanceButton.pack(side=LEFT, fill=X, expand=1)
		this.listArea.pack(side=TOP,fill=BOTH,expand=1)
		this.controlArea.pack(side=TOP,fill=BOTH,expand=0)
	def masterWindowAddDanceCallback(this, index:int):
		this.addDanceToQueue(index)
	def masterWindowNextDanceCallback(this):
		this.advanceDanceQueue()
	def masterWindowRemoveLastAddedDanceCallback(this):
		this.removeLastAddedDance()

root = Tk()
sl = masterWindow(root)
root.mainloop()