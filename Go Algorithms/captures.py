#import functions for grouping and liberties
from find_liberties import liberties, neighbouring_groups, group

#captures MUST be checked before suicides

#This functions takes a tile t, the board, and the current capture_points and returns a new board after adding points to capture_points.
def check_captures(t,board,capture_points):
	#find all neighbouring groups and the player who owns the input piece
	n_g=neighbouring_groups(t,board)
	player=board[t]["player"]
	
	#loop through all neighbouring groups and find their player.
	for h in n_g:
		j=h[0]
		p=board[j]["player"]
		
		#if the groups are owned by a player then they must be owned by the enemy player (as if they were owned by the same player then it would be part of the original group). Calculate liberties of enemy group
		if p is not None:
			l=liberties(j,board)
			q=len(l)
			
			#if the group has no liberties then loop through all of it's peices and remove them, adding capture points.
			if q==0:
				for i in h:
					board[i]["player"]=None
					capture_points[player]=capture_points[player] + 1
	return board


#This function checks for a given player, move and board state whether the input move would be suicidal or not
def is_suicidal(player,move,board):
	#default response is false. 
	response=False
	#play in the position and calculate its liberties
	board[move]["player"]=player
	l=liberties(move, board)
	
	#if it has no liberties then set the response to true
	if len(l)==0:
		response = True 
		
		#but loop through neighbouring groups
		n_g=neighbouring_groups(move,board)
		for g in n_g:
			g_l = liberties(g[0],board)
			#and if a group has 0 liberties then it would be captured so the move is legal and set response to true
			if len(g_l)==0:
				response=False
	#undo the move
	board[move]["player"]=None
	return response


#This functions takes an input group and checks for atari (whether the group only has one liberty or not)
def is_in_atari(group,board):
	#calculate the liberties of the group, if it's equal to 1 then return true, otherwise return false
	l=liberties(group[0],board)
	q=len(l)
	if q==1:
		return True
	else:
		return False


#This function takes an input player and move, and checks if the move violates the ko rule.
def is_ko(player,move,board):
	#default response is false, and if the move isn't a valid position then return false.
	response=False
	if move not in board:
		return response
	
	#play in the position and find the neighbouring groups for that position.
	if move in board:
		board[move]["player"]=player
		g=group(move,board)
		n_g=neighbouring_groups(move,board)
		
		#takens stores the number of pieces that have been captured by the input move
		takens=0
		
		#if the move is not part of a larger group (only solitary pieces can commit ko) then loop through neighbouring groups
		if len(g)==1:
			for n in n_g:
				#if the neighbouring group is owned by the enemy then calculate it's liberties 
				if board[n[0]]["player"] is not None:
					t=n[0]
					l=liberties(t,board)
					
					#if the piece has no liberties left then it will be captured so add 1 to takens if the group consists of only one piece, or 5 (an arbitrary number) if the group is larger than 1
					if len(l)==0:
						if len(n)==1:
							takens=takens+1
						elif len(n)>1:
							takens=takens+5
		
		#if only one piece has been taken (the second condition for ko) then set response to true. Undo the move and return response
		if takens==1:
			response=True
		board[move]["player"]=None
	return response

