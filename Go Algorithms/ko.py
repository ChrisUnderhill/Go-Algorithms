from captures import check_captures

#this function takes the board state and essentially produces a hash from it
def stringy(board):
	# h is for hash
    h=""
	#loop through the board, adding the first letter of the player who owns that position (so either B or W) to the hash
    for i in board:
        h+=str(board[i]["player"])[0]
	#return the hash
    return h

#this function is used by the main program to check whether a given board state is ko or not
def is_ko (board,history):
	#hash the board
    s=stringy(board)
	#if the hash already exists in history then the move is ko, otherwise return false
    if s in history:
        return True
    else:
        return False

#this function takes a hash and reverses it t0 produce a board state (used to undo a check_captures call if it turns out to be ko)
def unstring(board,string):
    #a is the index counter
    a=0
    #loop through the board
    for i in board:
	#find the letter corresponding to who owns that position
        f=string[a]
	#if it's black then set the owner to black, or if it's "w" then set it to white otherwise set it to None
        if f=="B":
            g="Black"
        elif f=="W":
            g="White"
        else:
            g=None
	#set the board state to reflect the player found above and increment the index counter
        board[i]["player"]=g
        a+=1
    #return the updated board state
    return board

#this function is used by players to test hypothetical moves for being ko
def check_ko(player,tile,board,game_state):
    #if no previous moves have been amde then the move cannot be ko
    if len(game_state["history"])==0:
        return False
    #if the tile being checked is unowned then play there and check captures
    if board[tile]["player"]==None:
        board[tile]["player"]=player
        board=check_captures(tile,board,game_state["capture points"])
	#check whether the current board state is ko.
        k=is_ko(board,game_state["history"])
	#undo the move AND the captures by reversing the previous board state's hash
        board=unstring(board,game_state["history"][-1])
	#make the tile unowned again
        board[tile]["player"]=None
    #return whether the move was ko or not
    return k    
                           
    
