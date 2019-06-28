from vpython import *
from visual.filedialog import get_file
import wx

import GUI
from game9 import *
import imp

#I had to use ListCtrl a lot in my code and it was a pain to handle so I created a class for myself to make it much easier
class listSelector():
	#this is the init function that just instantiates the object, panel is the window on which it is being drawn, 	
	def __init__(self,	panel, pos=(20,20), size=(100,100), style=wx.LC_REPORT | wx.LC_SINGLE_SEL  , label=""):
		#create a ListCtrl to be drawn on the panel at position pos. The panel, position, size and style are all taken from parameters, but all except panel have default values
		self.lc = wx.ListCtrl(panel, pos=pos, size=size, style= style )
		#insert a column as column 0, with label from parameter, which is the same width as the whole list
		self.lc.InsertColumn(0, label, width = size[0])
		
		#set the location(of selected program) and selected item to none, and the label to the same label as the parameter
		self.location=None
		self.selectedItem=None
		self.label=label
		
	#this function inserts all the programs from the programList into the listCtrl object
	def insertStrings(self):
		index=0
		#loop through the program list and insert the program's name as a string item into the listCtrl
		for i in programList:
			self.lc.InsertStringItem(index, i[0])
			#increment the index to insert the next item to the correct place
			index+=1

	#this function finds whichever item has been selected in the list by the user
	def getSelected(self, evt):
		#set the selected item to the name of the program that has been clicked on in the event
		self.selectedItem=evt.GetItem().GetText()
		print(self.selectedItem)
		
		#loop through the programList, if the name of any of the programs matches the selected item then find the corresponding location
		for i in programList:
			if i[0]==self.selectedItem:
				self.location=i[1]
				break

		#x is the combination of location and name of selected program
		x=(self.location, self.selectedItem)
		#if the list is selecting multiple AIs (only multi-lists had the label "AIs") then append x to the selected programs list if it's not already there
		if self.label == "AIs":
			if x not in selectedPrograms:
				selectedPrograms.append( x )
		
		#or if selecting from the single-choice list for Black then set the first item in selected programs to x, or if the 0th index doesn't exist already then append it instead
		elif self.label=="Black" or self.label=="Player1":
			try:
				selectedPrograms[0] = x
			except:
				selectedPrograms.append( x )
		#or if selecting from the single-choice list for White then try to set the second item in selected programs to x.
		elif self.label=="White" or self.label=="Player2":
			try:
				selectedPrograms[1] = x
			#if the 1st index doesn't exist already then check if the 0th index exists, and if so then append the item
			except:
				try:
					if selectedPrograms[0]:
						selectedPrograms.append( x )
				#otherwise append None followed by the item so that x is still at the 1st index
				except:
					selectedPrograms.append( None )
					selectedPrograms.append( x )
	
	
	#This function removes an item from the selected programs list if it has been deselected in the list
	def removeDeselected(self, evt):
		#get the name of the AI
		self.selectedItem=evt.GetItem().GetText()
		#loop through selected programs and if the names match then remove that AI from selected programs
		for i in selectedPrograms:
			if i[1]==self.selectedItem:
				selectedPrograms.remove(i)
		print(selectedPrograms)
		
#_____________________________________________________END OF CLASS DEFINITION



#this function runs a match between two AIs. It takes evt as a parameter so that it can be called by clicking on a button, and comp decides whether the match is a single match or a competition
def runMatch(evt, comp=False):
	#if exactly two programs have been selected
	if len(selectedPrograms)==2:
		print(selectedPrograms)
		
		#open a new file called RunMe.py in write mode
		f=open("RunMe.py", "w")
		#write the lines into the new python file such that is looks like the example screenshotted in the coursework (look for RunMe.py Match example immediately below this section for explanation of RunMe logic)
		f.write("import imp\n")
		f.write("black = imp.load_source( \"" + selectedPrograms[0][1] + "\", \"" + str(selectedPrograms[0][0]) + "\" )\n"  )
		f.write("white = imp.load_source( \"" + selectedPrograms[1][1] + "\", \"" + str(selectedPrograms[1][0]) + "\" )\n"  )
		f.write("from game9 import *\n")
		f.write("def run():\n")
		#if comp is false then get the program to simply run one match and return the results
		if comp==False:
			f.write("\treturn play_game(black.play, white.play)\n")
		#otherwise return the results of a competition involving comp number of matches
		else:
			f.write("\treturn competition(black.play, white.play, " + str(comp) + ")\n")
		#close the file
		f.close()
		
		#import the newly create file
		import RunMe
		#since Python doesn't let you reimport modules if they have already been imported, reload the module to make sure we have the most up to date one
		reload(RunMe)
		#find the results of the matchby running the RunMe function. Format the results nicely then set the to display in the text box on the main screen
		points=RunMe.run()
		prntPoints = "Results are\n" + str(selectedPrograms[0][1]) +" scored: " + str(points["Black"]) + "\n" + str(selectedPrograms[1][1]) + " scored: " + str(points["White"])
		results.SetLabel(prntPoints)
	
	#otherwise tell the user to select two programs.
	else:
		results.SetLabel("Please select two programs")
	

#this function sets up all prerequisites to run a match in a new window. It is called when the user clicks on the Run A Match button on the main screen
def setupMatch(evt, comp = False):
	#set selectedPrograms to a blank list
	global selectedPrograms
	selectedPrograms=[]
	
	#get the scene for compatability with Vpython
	scene= display.get_selected()
	
	#create a new window without windows, called "Pick AIs".
	win=window(id=2, menus=False, title="Pick AIs", x=400, y=100, width=500, height=500)
	
	#when the window is closed, do not close all other windows by default
	win._exit = False
	
	#find the panel so that button cans be drawn on it
	pan2= win.panel
	
	#make an OK button on pan2 
	ok= wx.Button(pan2, label="OK", pos=(400, 380), size = (50,50) )
	 
	#give the user instructions at the top of the page
	txt=wx.StaticText(pan2, pos=(20, 20), label="Please select two AIs from the following lists, then hit OK")
	
	#if it is an individual match then make two lists titled "Black" and "White"
	if comp==False:
		choice1=listSelector(pan2, pos=(20,60), size=(200, 300), label = "Black" )
		choice2=listSelector(pan2, pos=(240,60), size=(200, 300), label="White" )
	#otherwise make two identical lists called "Player1" and "Player2" 
	else:
		choice1=listSelector(pan2, pos=(20,60), size=(200, 300), label = "Player1" )
		choice2=listSelector(pan2, pos=(240,60), size=(200, 300), label="Player2" )

	#insert all of the programs into both lists
	choice1.insertStrings()
	choice2.insertStrings()

	#bind both lists' Item Selection events to their getSelected functions
	choice1.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, choice1.getSelected )
	choice2.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, choice2.getSelected )
	
	#if it is an individual match then bind the ok button to runMatch
	if comp == False: 
		ok.Bind(wx.EVT_BUTTON, runMatch )
	#otherwise define a new function called passComp 
	elif comp == True:
		#this function takes an evt so that it can be called by a button click and then runs a competition
		def passComp(evt):
			#find the number of games the user wants to run and then round up to the nearest multiple of 2 so that an even number of games can be run as black and white
			x=nGames.GetValue()
			x += x%2
			print("RUNNING COMP")
			#run a match with the new number of games
			runMatch(wx.EVT_BUTTON, comp=x)
			
		#bind the ok button to this new passComp function
		ok.Bind(wx.EVT_BUTTON, passComp)
		
		#make a slider taking values from 2 to 200 that lets the user select the number of games they want to run between the two AIs, with ticks spaced every ten values
		nGames=wx.Slider(pan2, value=10, minValue=2, maxValue=200, pos= (20, 390), size=(300, 30), style= wx.SL_HORIZONTAL | wx.SL_BOTTOM | wx.SL_LABELS | wx.SL_AUTOTICKS, name = "Please select the number of games")
		nGames.SetTickFreq( 10 )
		txt = wx.StaticText(pan2, pos=(20,370), size= (300, 20),  label = "Please select the number of games to play" , style=wx.ALIGN_CENTRE )
	
	#this infinte loop is required by VPython as a new window has been made
	while True:
		rate(1)
	return True
	
	
#this function is just a handler for the Run A Competition button which sets up a match but with comp=True
def runComp(evt):
	setupMatch(None, comp=True)
	return True
	
	
#this function runs a tournament between at least two AIs. Evt is taken as a parameter so that the function can be called by a button event
def runTourn(evt):
	#if at least two programs have been selected then open a new file called RunMe.py in write mode
	if len(selectedPrograms)>=2:
		print(selectedPrograms)
		f=open("RunMe.py", "w")
		
		#write lines to it so that it looks like the RunMe.py Tournament example below this section.
		#import the import library and set programs to a blank list
		f.write("import imp\n")
		f.write("programs=[]\n")
		
		#loop through all the selected programs and import them as player i, then append them to the programs list
		for i in range(1, len(selectedPrograms)+1 ):
			f.write("Player" + str(i) + " = imp.load_source( \"" + selectedPrograms[i-1][1] + "\", \"" + str(selectedPrograms[i-1][0]) + "\" )\n"  )
			f.write("programs.append( Player" + str(i) + " )\n" ) 
		
		#import the game9 functions and set points to a blank dictionary
		f.write("from game9 import *\n")
		f.write("points = {}\n")
		
		#loop through all selected programs and create a new dictionary entry for player i setting they're score to 0
		for i in range(1, len(selectedPrograms)+1 ):
			f.write("points[\"Player" + str(i) + "\"] = 0 \n" )
		
		#create a new function that loops through all selected programs twice and runs a competition between each pair of programs
		f.write("def run():\n\t")
		f.write("for i in range(0, " + str( len(selectedPrograms)  ) + "):\n\t\t"  )
		f.write("for j in range(i+1, " + str( len(selectedPrograms)  ) + "):\n\t\t\t"  )
		f.write("p = competition( programs[i].play, programs[j].play, 2 ) \n\t\t\t")
		
		#if black got more points than white in the competition then add one to their tournament points, otherwise add one to white's points
		f.write("if p[\"Black\"]  >  p[\"White\"]: \n\t\t\t\t")		
		f.write("points[ \"Player\" + str(i+1) ] += 1  \n\t\t\t" )
		f.write("else: \n\t\t\t\t")		
		f.write("points[ \"Player\" + str(j+1) ] += 1  \n\t" )
		f.write("return points")
		
		#close the file
		f.close()
		
		#import RunMe and reload it to make sure it's the most up to date version
		import RunMe
		reload(RunMe)
		#run the new program and get the number of points.
		points=RunMe.run()
		print(points)
		
		#format points nicely then set it to display in the results box on the main page
		prntPoints=""
		for i in range(1, len(selectedPrograms)+1 ):
			prntPoints = prntPoints +  str(selectedPrograms[i-1][1]) + " scored " + str(  points["Player" + str(i)]  ) + "\n"
		results.SetLabel(prntPoints)
		
	#otherwise tell the user to select at least two programs
	else:
		print("Please select at least two programs")
		
		

#this function sets up all the prerequisites required to run a tournamnet, getting user selection of programs in a new window
def setupTourn(evt):
	#set selectedPrograms to a blank list
	global selectedPrograms
	selectedPrograms=[]
	
	#get the selected scene for compatability with Vpython
	scene= display.get_selected()
	
	#createa new window titled "Pick AIs" 
	win=window(id=3, menus=False, title="Pick AIs", x=400, y=100, width=500, height=500) #, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
	#when the window is closed, make sure it doesn't automatically kill all the other windows
	win._exit = False
	
	#find the window's panel so that it can be drawn to, then create an ok button on it
	pan2= win.panel
	ok= wx.Button(pan2, label="OK", pos=(400, 380), size = (50,50) )
	
	#give the user isntructions at the top of the page and create a list that allows multiple selection of AIs 
	txt=wx.StaticText(pan2, pos=(20, 20), label="Please select at least two AIs from the following lists, using the control or shift key to\nselect multiple items")
	choice1=listSelector(pan2, pos=(20,60), size=(200, 300), label="AIs", style= wx.LC_REPORT )
	
	#insert all the AIs into the list and bind the lists selection and deselection events to the corresponding functions from my class
	choice1.insertStrings()
	choice1.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, choice1.getSelected )
	choice1.lc.Bind(wx.EVT_LIST_ITEM_DESELECTED, choice1.removeDeselected )
	
	#bind the ok button to runTourn
	ok.Bind(wx.EVT_BUTTON, runTourn)
		
	#this infinite loop is required by Vpython because a new window has been created
	while True:
		rate(1)
		
	return True
	

#this function allows the user to add new AIs to the repository of programs using the file explorer menu
def addNewAI():
	#get the selected scene for compatability with Vpython 
	scene= display.get_selected()
	
	#create a new window titled "Add New AI"
	win2=window(id=6, menus=False, title="Add New AI", x=600, y=100, width=350, height=200) 
	#make sure that closing the window doesn't automatically kill all other open windows by default
	win2._exit = False
	
	#find the window's panel so it can be drawn to, then draw a text box on the screen
	pan3 = win2.panel
	location = wx.TextCtrl(pan3, pos=(20, 20), value='Program Location', size=(250,40), style = wx.HSCROLL | wx.TE_RICH2 )
	
	#create a button with a bitmap image on it, and another text box beneath it
	locButton = wx.BitmapButton(pan3, pos=(270, 20), bitmap=wx.Bitmap("folder-icon.bmp"), size = (20,20) )
	progName = wx.TextCtrl(pan3, pos=(20, 80), value='Program Name', size=(250,40), style = wx.HSCROLL | wx.TE_RICH2 )

	#create an ok button
	ok = wx.Button(pan3, label="OK", pos=(275, 80), size = (50,40) )
	
	#this function allows the location button to call it and allows the user to select a file from the file explorer
	def pickFile(evt):
		#use VPython's file explorer function to find all python files and set f to the file selected by the user
		f=get_file(".py")
		#find the address of the file and replace all occurences of \ with a / for compatability
		path=f.name.replace("\\", "/")
		#fill this path in to the text box
		location.SetValue(path)
		
		#the name of the file is string following the final / in the address.
		name = path.split("/")
		name = name[len(name)-1]
		#remove the .py from the end
		name = name[:-3]
		#fill this name into the text box
		progName.SetValue(name)
		
	#set the locations button to call the above function
	locButton.Bind(wx.EVT_BUTTON, pickFile)
	
	#this function allows the ok button to call it and adds the program to the list
	def addProg(evt):
		#open the repostiory in read and append mode
		repo=open("repo.txt", "r+")
		#get the name and location from the text boxes in the window
		name = progName.GetLineText(0)
		loc = location.GetLineText(0)
		#if the name and location have a length then try importing the program (if it fails tell the user to make the file end in .py)
		if len(name)>0 and len(loc)>0:
			try:
				prog = imp.load_source("prog", loc)
				#try referencing the modules play function (if it fails tell the user to call their function play)
				try:
					prog.play
					#try giving the play function 3 blank parameters (on a TypeError tell the user to make sure it takes 3 parameters as TypeError is the exception thrown when incorrect number of parameters is included)
					try:
						prog.play("", {}, {})
						#if the program somehow manages to accept blanks as the board and player and game state without making any errors at all during the entire execution then add it to the list
						#check whether the program's name already exists
						add=True
						for i in programList:
							if i[0] == name:
								add=False
						
						if add==True:
							programList.append( [name, loc] )
							#seek to the end of the program (required otherwise the file doesn't like being written to and throws errors)
							repo.seek(0,2)
							#format the information and write it to the file, then close it 
							repo.write( name + " | " + loc + "\n")
						repo.close()
					except TypeError:
						results.SetLabel("Please make sure the AI's play function takes 3 parameters (player, board, gamestate)")
					#most AI programs will raise some form of error when passed blanks as the parameters so on any non-TypeError add the program to the list
					except:
						programList.append( [name, loc] )
						#seek to the end of the program (required otherwise the file doesn't like being written to and throws errors)
						repo.seek(0,2)
						#format the information and write it to the file, then close it 
						repo.write( name + " | " + loc + "\n")
						repo.close()
				except:
					results.SetLabel("Please make sure the AI has a function called play")
			except:
				results.SetLabel("Please make sure the location points to a valid python file")
		else:
			results.SetLabel("Please enter a name")
		#delete the window and open a new ManageAIs window
		win2.delete()
		manageAIs(None) # required to get the lists to reload
	
	#bind the ok button to the above function
	ok.Bind(wx.EVT_BUTTON, addProg)
	
	#infinite loop required by VPython
	while True:
		rate(1)
				

#this function allowst he user to renmae and AI that has been selected from the previous window's selection box
def renameAI():
	#get the displayed scene for compatability with VPython
	scene= display.get_selected()
	
	#open a new window and set it to not kill all windows when it is closed
	win2=window(id=7, menus=False, title="Rename AI", x=600, y=100, width=350, height=200) 
	win2._exit = False
	
	#find the panel to draw to
	pan3 = win2.panel
	
	#so long as a program has been selected carry on executing code
	try:
		selectedPrograms[0]!=None
	#otherwise tell the user to select an AI to rename in the main results box
	except:
		results.SetLabel("Please select an AI to rename")
		#kill the window and reopen the manageAIs window
		win2.delete()
		manageAIs(None)
		#return false to make sure none of the rest of the code gets executed
		return False
	
	#create a new textbox to hold the program's name, and fill in the current name as it's value
	progName = wx.TextCtrl(pan3, pos=(20, 20), value=selectedPrograms[0][1], size=(250,40), style = wx.HSCROLL | wx.TE_RICH2 )

	#find the index of the program in programList
	programIndex = programList.index( [ selectedPrograms[0][1], selectedPrograms[0][0] ]  )
	
	#create an ok button
	ok = wx.Button(pan3, label="OK", pos=(275, 80), size = (50,40) )
	
	#create a new function that can be called from the ok button and saves the changes that have been made to the program name
	#this function needs to be local to the parent function so that it can kill the parent window (the window didn't close when it was passed as a parameter)
	def saveChange(evt):
		#set the name of the program in program list to the string that has been input into the text box
		if len(progName.GetLineText(0))>0:
			programList[programIndex][0] = progName.GetLineText(0)
		#open the repository in overwrite mode and loop through program list
		repo=open("repo.txt", "w")
		for i in programList:
			#so long as the program is not none then format it's data and add it to the repo
			if i != None:
				repo.write( i[0] + " | " + i[1] + "\n" )
		#close the repo and the window, then reopen the manageAIs window
		repo.close()
		win2.delete()
		manageAIs(None)
	
	#bind the ok button to this new function 
	ok.Bind(wx.EVT_BUTTON, saveChange)
	
	#infinite loop required for compatability with VPython
	while True:
		rate(1)
		
		
#this function allows the user to remove an AI from the list
def removeAI():
	#so long as a program has been selected carry on executing code
	try:
		selectedPrograms[0]!=None
	#otherwise tell the user to select an AI to remove in the main results box and reopen manageAIs window
	except:
		results.SetLabel("Please select an AI to remove")
		manageAIs(None)
		#return false to make sure none of the rest of the code gets executed
		return False
		
	#loop through the program list, if the name of the program matches the selected program's name remove the program.
	for i in programList:
		if i[1] == selectedPrograms[0][0]:
			programList.remove(i)
		
	#open the repository in overwrite mode and loop through the program list
	repo=open("repo.txt", "w")
	for i in programList:
		#if the program isn't none then format it's data and add it to the repo
		if i != None:
			repo.write( i[0] + " | " + i[1] + "\n" )
	
	#close the repo and reopen the manageAIs window
	repo.close()
	manageAIs(None)
	return True

#this function opens up a new window allowing the user to manage the AI list, including changing their names, adding new AIs or removing unwanted ones.
def manageAIs(evt):
	#set the global variable selectedPrograms to a blank list
	global selectedPrograms
	selectedPrograms=[]
	
	#get hte currently selected scene for compatability with VPython
	scene= display.get_selected()
	
	#open a new window title Manage AIs and make sure it doesn't kill all windows when it's closed
	win=window(id=5, menus=False, title="Manage AIs", x=600, y=100, width=400, height=500) 
	win._exit = False
	#find the window's panel
	pan2= win.panel
	
	#make ok, addNew, rename and remove Buttons
	ok= wx.Button(pan2, label="OK", pos=(275, 380), size = (50,50) )
	addNew = wx.Button(pan2, label="Add New AI", pos=(250, 60), size = (100,50) )
	rename = wx.Button(pan2, label="Rename", pos=(250, 120), size = (100,50) )
	remove = wx.Button(pan2, label="Remove", pos=(250, 180), size = (100,50) )
	
	#give the user instructions at the top of the screen
	txt=wx.StaticText(pan2, pos=(20, 20), label="Please select an AI from the following list")
	
	#create a list on screen and populate it with all the AIs
	choice1=listSelector(pan2, pos=(20,60), size=(200, 300), label="AIs" )
	choice1.insertStrings()
	
	#bind the selection and deselection events to the correct functions in the list selector class
	choice1.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, choice1.getSelected )
	choice1.lc.Bind(wx.EVT_LIST_ITEM_DESELECTED, choice1.removeDeselected )
	
	#this function kills the window and can be called from the OK button
	def kill(evt):
		win.delete()
	ok.Bind(wx.EVT_BUTTON, kill)
	
	#this function calls the addNewAI function and deletes the window, but is callable by button click
	def add(evt):
		win.delete()
		addNewAI()
	#bind the button to the function
	addNew.Bind(wx.EVT_BUTTON, add)
	
	#this function calls the renameAI function and deletes the window, but is callable by button click
	def ren(evt):
		win.delete()
		renameAI()
	#bind the button to the function
	rename.Bind(wx.EVT_BUTTON, ren)
	
	#this function calls the removeAI function and deletes the window, but is callable by button click
	def rev(evt):
		win.delete()
		removeAI()
	#bind the button to the function
	remove.Bind(wx.EVT_BUTTON, rev)
	
	#infinite loop required by VPython
	while True:
		rate(1)
	return True
	
	
#open the repository in read and write mode
repo=open("repo.txt", "r+")
programList=[]

#read from the file and split it by lines
temp=repo.read().splitlines()
#loop through the lines and append the name and location to programList.
for i in temp:
	programList.append(i.split(" | ") )
#sort the programList and close the file
programList.sort()
repo.close()

#set the selectedPrograms to a blank list
selectedPrograms=[]

#open a window and add a square display of size bSize to it with center (500,500,0) 
w = window(id = 1, menus=False, title="Go Platform", x=20, y=20, width=1000, height=1000, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
d = 20
bSize=600  #size of board
dis=display(window=w, x=d, y=d, center = (500,500,0), width=bSize, height=bSize)
#setup the board in this display
GUI.setupDrawing(9)

#find te window's panel and set the button font to size 18
pan = w.panel
buttonFont= wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)

#create match, competition, tournament and manage buttons
match = wx.Button(pan, label = "Run a Match", pos = (bSize+100,50), size = (220, 100) )
comp = wx.Button(pan, label = "Run a Competition", pos = (bSize+100,200), size = (220, 100) )
tourn = wx.Button(pan, label = "Run a Tournament", pos = (bSize+100,350), size = (220, 100) )
manage = wx.Button(pan, label = "Manage AIs", pos = (bSize+100,700), size = (220, 100) )

#set the fonts and foreground colours of all the buttons.
match.SetFont(buttonFont)
match.SetForegroundColour(wx.Colour( 78,197,237 ) )
match.Bind(wx.EVT_BUTTON, setupMatch)

comp.SetFont(buttonFont)
comp.SetForegroundColour(wx.Colour( 203,78,237 ) )
comp.Bind(wx.EVT_BUTTON, runComp)

tourn.SetFont(buttonFont)
tourn.SetForegroundColour(wx.Colour( 237,78,107 ) )
tourn.Bind(wx.EVT_BUTTON, setupTourn)

manage.SetFont(buttonFont)
manage.SetForegroundColour(wx.Colour( 78,237,118 ) )
manage.Bind(wx.EVT_BUTTON, manageAIs)

#make the results font size 12
resultsFont= wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)

#create a text box that can't be edited at the bottom and set the font to the one above
results = wx.TextCtrl(pan, pos=(d,bSize+50), value='Results will be printed here', size=(bSize,200), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.TE_BESTWRAP)
results.SetFont(resultsFont)

while True:
	rate(1)