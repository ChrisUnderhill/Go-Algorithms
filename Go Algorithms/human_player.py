from visual import *

#According to the rules of my framework each ai must have a lay function that takes in player board state and gamestate, so this function does just that and returns whatever is returned by selectPlace
def play(player, board, game_state):
	place=selectPlace(board)
	#print("success")
	return place
	
#This function allows the user to actually select the position they want to play in. It takes in the board state to determine the size of the board and returns either pass or the position clicked on by the user
def selectPlace(board):
	alpha="abcdefghijklmnopqrstuvwxyz"
	numbers=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19")

	#get the selected scene and calculate the size of the board
	scene = display.get_selected()
	size=int((len(board))**0.5)
	
	#wait for a click event and assign it to ev. Default move is "pass"
	ev=scene.waitfor("click")
	place="pass"
	
	#loop through all rows and columns
	for i in range(0,size):
		for j in range(0,size):
			#if the position of the click lies within 35% of current row and column intersection...
			if ev.pos[0]> (1000/(size+3))*(i+1.65) and ev.pos[0] < (1000/(size+3))*(i+2.35):
				if ev.pos[1]> (1000/(size+3))*(j+1.65) and ev.pos[1] < (1000/(size+3))*(j+2.35):
					#...then make the string that corresponds to the place and return it 
					place=alpha[i]+numbers[j]
					#print(place)
	return place
	