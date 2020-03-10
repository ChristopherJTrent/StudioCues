from tkinter import Toplevel, Frame, Entry, Label, Button, Y, LEFT, TOP, X, END, BOTTOM
from ManagedFrame import managedframe
from configparser import ConfigParser


class PreferencesWindow(object):
	def __init__(self, parent, prefs, owner):
		self.owner = owner
		self.parent = parent
		self.configuration = prefs
		self.window = Toplevel(parent)
		self.sectionContainer = Frame(self.window)
		self.manager = managedframe(self.window)
		self.frameKeys = []
		self.updateManager = []
		self.anySectionsUpdated = False
		self.ConfigLocationChanged = False
		self.appConfigButtonArea = Frame(self.window)
		self.okbutton = Button(self.appConfigButtonArea, text='OK', command=self.__OKConfigChanges)
		self.cancelbutton = Button(self.appConfigButtonArea, text='Cancel', command = self.__cancelConfigChanges)
		self.okbutton.pack(side=LEFT)
		self.cancelbutton.pack(side=LEFT)
		self.appConfigButtonArea.pack(side=BOTTOM)
		for pref in self.configuration.sections():
			tempButton = Button(self.sectionContainer, text=pref, command = lambda pref_=pref:self.manager.changeOption(pref_))
			self.frameKeys.append(pref)
			tempFrame = Frame(self.manager)
			for opt in self.configuration[pref]:
				tempOptionArea = Frame(tempFrame)
				tempEntry = Entry(tempOptionArea, text=self.configuration[pref][opt])
				tempEntry.delete(0,END)
				tempEntry.insert(0, self.configuration[pref][opt])
				tempLabel = Label(tempOptionArea, text=opt)
				self.updateManager.append(lambda tempEntry_ = tempEntry, pref_ = pref, opt_ = opt: self.__doConfigUpdateForEntry(tempEntry_, pref_, opt_))
				tempEntry.pack(side=LEFT)
				tempLabel.pack(side=LEFT)
				tempOptionArea.pack(side=TOP, fill=X)
			self.manager.addOption(tempFrame, pref)
			tempButton.pack()
		if self.frameKeys:
			self.manager.changeOption(self.frameKeys[0])
		self.sectionContainer.pack(fill=Y,side=LEFT,expand=1)
		self.manager.pack(fill=Y,side=LEFT, expand=1)
		self.window.protocol('WM_DELETE_WINDOW', self.hide)


	def hide(self):
		self.window.withdraw()

	def show(self):
		self.window.deiconify()

	def __OKConfigChanges(self):
		self.__applyConfigChanges()
	def __cancelConfigChanges(self):
		self.hide()
		self = None
	def __applyConfigChanges(self):
		self.__doConfigWrite()
	def __doConfigWrite(self):
		for entry in self.updateManager:
			entry()
		if self.ConfigLocationChanged:
			self.owner.moveConfig(self.configuration['startup']['PreferencesLocation'])
		if self.anySectionsUpdated:
			self.owner.writeConfiguration()
			self.owner.reload()

	def __doConfigUpdateForEntry(self, Entry_, section, option):
		if Entry_.get() != self.configuration[section][option]:
			self.configuration[section][option] = Entry_.get()
			self.anySectionsUpdated = True