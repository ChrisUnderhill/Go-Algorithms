from visual import *
from visual.graph import *

alpha="abcdefghijklmnopqrstuvwxyz"
numbers=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"]

#this function takes a size and draws a grid with labels of that size, up to and including size 19. 
def setupDrawing(size):
	#Get the selected scene so that the grid gets drawn in the right window. Set the centre to 500,500,0 because I've chosen to make make the board 1000x1000.
	scene= display.get_selected()
	scene.center=(500,500,0)
	
	#This seperation is the distance between two gridlines, and wood is the background.
	seperation=1000/(size+3)
	wood = box(pos =(500, 500, -1), size = (980, 980, 2), color=(0.7, 0.4, 0.1))
	
	#axes hold the lines that make up the grid, labs holds the letter labels that appear below each line
	axes=[]
	labs=[]
	
	#These axes are just a red outline around the whole board.
	axes.append(  curve(pos=[(0,0,0), (0,1000, 0)], color=color.red)  )
	axes.append(  curve(pos=[(1000,0,0), (1000,1000, 0)], color=color.red)  )
	axes.append(  curve(pos=[(0,1000,0), (1000,1000, 0)], color=color.red)  )
	axes.append(  curve(pos=[(0,0,0), (1000,0, 0)], color=color.red)  )
	
	#loop through the number of lines that are required
	for i in range(1,size+1):
		#append lines that go from top to bottom and bottom to top.
		axes.append( curve(pos=[((i+1)*seperation,seperation*2,0), ((i+1)*seperation,1000-seperation*2, 0)], color=color.white))
		axes.append( curve(pos=[(seperation*2,(i+1)*seperation,0), (1000-seperation*2,(i+1)*seperation, 0)], color=color.white))
		
		#four labels are required per row and column pair, above, below, left and right.
		labs.append( text(text=alpha[i-1], pos = ((i+1)*seperation,seperation/1.5,0), align="center", depth=1, height=seperation/2, color=(1,1,1) ) )
		labs.append( text(text=numbers[i-1], pos = (seperation/1.5, (i+1)*seperation-25, 0), align="center", depth=1, height=seperation/2, color=(1,1,1) )) 
		labs.append( text(text=alpha[i-1], pos = ((i+1)*seperation, 1000-seperation,0), align="center", depth=1, height=seperation/2, color=(1,1,1) ) )
		labs.append( text(text=numbers[i-1], pos = (1000-seperation/1.5, (i+1)*seperation-25, 0), align="center", depth=1, height=seperation/2, color=(1,1,1) )) 
	#rate(100) just makes sure that the board gets drawn
	rate(100)
	return True
	

#this function takes the current board state and updates the drawn board to match.
def update(board):
	#spheres holds all of the pieces on the board. Rate(40) means that at most 40 updates can happen per second.
	spheres=[]
	rate(40)
	
	#Try clearing the board of all spheres, but this crashes if there are no spheres on the board at the moment so reset spheres if this happens. 
	try:
		clear()
	except:
		spheres=[]

	#Find the appropriate size and associated seperation for the board
	size=sqrt(len(board))
	seperation=1000/(size+3)
	
	#Loop through the entire board and find their equivalent positions in the real board
	for i in board:
		c=alpha.index(i[0])+2
		r=int(i[1])+1
		#if the current piece is owned by black or white draw a black sphere at the appropriate position,
		if board[i]["player"]=="Black":
			spheres.append( sphere(pos= (c*seperation, r*seperation, 0), color = (0.2,0.02,0.2), radius = seperation/2.5)  )
		elif board[i]["player"]=="White":
			spheres.append( sphere(pos= (c*seperation, r*seperation, 0), color = color.white, radius = seperation/2.5)  )


#this function clears the board of any pieces on it but leaves the background and the labels
def clear():
	#get the selected scene and then loop through all of the objects in the scene
    scene = display.get_selected()
    for obj in scene.objects:
        #if the object is an instance of sphere then make it invisible (Vpython has no delete function) and move it to 0,0,500 
        if isinstance(obj, sphere):
            obj.visible=False
            obj.pos=(0,0,500)


#Similar to the clear function above, this will delete ALL objects on the screen instead of just spheres
def delete():
	#get the selected scene and loop through all objects in it
    scene = display.get_selected()
    for obj in scene.objects:
		#make the object invisible and move it to 0,0,500
        obj.visible=False
        obj.pos=(0,0,500)

