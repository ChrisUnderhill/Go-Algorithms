# "be patterns, be examples in all countries, places, islands, nations... then you will come to walk cheerfully over the world"

import random
from find_liberties import liberties, group, neighbouring_groups, is_eye_candidate, is_alive
from captures import is_suicidal, is_in_atari
from ko import check_ko

#this is the play function that returns a move
def play(player,board,game_state):
	
	#find how far each tile is from the end of the board
	distances=greatest_distance(board)
	
	#patterns is the list of functiosn (declared below) that return true or false when given a move, according to certain criteria. These are in priority order.
	patterns=[capture,save_from_probable_death,ladder,invade_large_empty_space,seal_off_territory,seal_the_edges,sneak]
	
	#default move is pass, allowed moves stores all moves that aren't illegal and decisions is a dictionary mapping from pattern to movs that the patern wants to make
	move="pass"
	allowed_moves=[]
	decisions={}
	
	#friends is a list of tiles that are essential to the life of a group. f is the list of friend moves
	friends=find_friends(board)
	f=[]
	
	#loop through friends, if any of the moves are allowed then add them to f
	for i in friends:
		if is_allowed(i,board,player,game_state)==True:
			f.append(i)
	
	#if there are any moves in f, then pick a random f to return (because friends is the most important patern and is run across the entire board
	if len(f)>0:
		return random.choice(f)
		
	#loop through the board, if the move is allowed (not occupied and not suicidal) and is not ko then pretend to play there
	for tile in board:
		if board[tile]["player"]==None and is_suicidal(player,tile,board)==False:
				if check_ko(player,tile,board,game_state)==False:
					board[tile]["player"]=player
					
					#check whether the group is in atari after the move
					a=is_in_atari(group(tile,board),board)
					b=False
					#loop through the board and if the move makes any captures then set b = True
					for n in board[tile]["neighbours"]:
						if board[n]["player"] is not None and board[n]["player"] != player:
							l=liberties(n,board)
							if len(l)==0:
								b=True
					#if we are not putting ourselves in atari or we make captures despite this then add the tile to allowed moves
					if a==False or b==True:
						allowed_moves.append(tile)
					#undo the hypothetical move
					board[tile]["player"]=None
					
	#loop through patterns, adding a new empty list for each pattern (these will store the moves that this pattern wants to make)
	for p in patterns:
		decisions[p]=[]
		
	#loop through all allowed moves and all patterns. 
	for tile in allowed_moves:
		for pat in patterns:
			#call the pattern's function on the tile and if the pattern wants to play there, add it to it's corresponding decisions list
			verdict=pat(tile,player,board,distances,game_state)
			if verdict==True:
				decisions[pat].append(tile)
				
	#loop through patterns again and if there are any moves for that pattern then choose a random one of them to return
	for i in patterns:
		if len(decisions[i])>0:
			move=random.choice(decisions[i])
			return move
	#this will return pass if none of the patterns decide on any moves
	return move

#____________________End of play function. Patterns declared below__________


#this function finds empty tiles that could be played to make a group live
def find_friends(board):
	groups=[]
	friends=[]
	#loop through the board, if the tile is not empty then add it's group to the list of groups, if not already in there
	for tile in board:
		if board[tile]["player"] is not None:
			g=group(tile,board)
			if g not in groups:
				 groups.append(g)
				 
	#loop through groups and find the player who own's them and a list of tiles that could be played to make the group "alive" if it isn't already
	for g in groups:
		player=board[g[0]]["player"]
		s=saviours(g[0],board)            
		
		#if the group has only one saviour place then add that place to friends (if there are two or more then it is unnecessary to play in the spot because if attacked it can be saved by one of the other places)
		if len(s)==1:
			friends.append(s[0])
			
		#or if there are no saviour tiles then loop through the liberties of the group
		elif len(s)==0:
			for tile in liberties(g[0],board):
				#pretend to play in the position and look for saviours then undo the move
				board[tile]["player"]=player
				t=saviours(g[0],board)
				board[tile]["player"]=None
				#if there are now two or more saviours then add the original position to friends
				if len(t)>=2:
					friends.append(tile)
	return friends

#this function will return a list of tiles that try to invade into unclaimed territory
def invade_large_empty_space(tile,player,board,distances,game_state):
	#if the tile is 2 places away from the edge board...
	if tile in distances[2]:
		good=True
		#loop through all the tile's neighbours and if the neighbours are not empty then it's not a large empty space so don't invade it
		for n in board[tile]["neighbours"]:
			if board[n]["player"] is not None:
				good=False
			#if the neighbour is 1 spaces away from the edge of the board then loop through it's neighbours
			if n in distances[1]:
				for nn in board[n]["neighbours"]:
					#if the new neighbour is not empty then the empty space is still not large enough so don't invade
					if board[nn]["player"] is not None:
						good=False
		#return whether to invade or not
		return good

#This function looks for territory that is partly surrounded and tries to seal it off
def seal_off_territory(tile,player,board,distances,game_state):
	v=False
	#if the tile is unowned and if 2 away from the edge of the board then loop through it's neighbours
	if board[tile]["player"] is None:
		if tile in distances[2]:
			for n in board[tile]["neighbours"]:
				#if the neighbour is also 2 away from the edge and is owned by the player then it's a good move to seal off the territory (usually).
				if n in distances[2] and board[n]["player"]==player:
					v=True
				#loop through all of the neighbour's neighbours and if they are 2 away from the board and owned by player then it's a good move (usually; this is a one point jump)
				for nn in board[n]["neighbours"]:
					if nn in distances[2] and board[nn]["player"]==player:
						v=True
		
		#or if the tile is 1 space away from the edge then loop through it's neighbours and check whether it's two away 
		elif tile in distances[1]:
			for n in board[tile]["neighbours"]:
				if n in distances[2]:
					#if the neighbour is owned by the player then it's possibly a good move
					if board[n]["player"]==player:
						v=True
			#loop through neighbours again. If the neighbour is 1 away from the edge and is owned by the player then it is no longer a good move
			for n in board[tile]["neighbours"]:                        
				if n in distances[1]:
					if board[n]["player"]==player:
						v=False
	return v

#this function makes sure that territory space is maximised around the edges
def seal_the_edges(tile,player,board,distances,game_state):
	v=False
	#if the tile is on the edge and is unowned then loop through it's neighbours.
	if tile in distances[0]:
		if board[tile]["player"] is None:
			for n in board[tile]["neighbours"]:
				#if the neighbour is 1 away from the edge and is owned by the player then it is a good move (because it will connect a piece that's one away from the edge to the edge and stop enemy attack)
				if n in distances[1]:
					if board[n]["player"]==player:
						v=True
				
				#or if the neighbour is also on the edge and is not owned by me (can be either enemy or blank) then loop through its neighbours
				elif n in distances[0]:
					if board[n]["player"]!=player:
						for nn in board[n]["neighbours"]:
							#if the new neighbour is 1 away and is owned by the player then it is a good move most of the time (will either seal off the edge or do so while capturing an enemy piece) 
							if nn in distances[1]:
								if board[nn]["player"]==player:
									v=True
	
	#if the tile is an eye candidate then don't play there because filling in eyes is a bad strategy
	if is_eye_candidate(tile,board) is not None:
		v=False
	return v

#this function checks whether a tile will follow a ladder or not 
def ladder(tile,player,board,distances,game_state):
	v=False
	#if the tile is unowned...
	if board[tile]["player"] is None:
		enemies=[]
		frees=0
		#loop through the tile's neighbours, if the neighbour is unowned then add 1 to frees
		for n in board[tile]["neighbours"]:
			if board[n]["player"] is None:
				frees+=1
			#or if the neighbour is owned by the enemy then add the neighbour's position to the enemies lists
			elif board[n]["player"]!=player:
				enemies.append(n)
		#if there is only 1 enemy then find the groups that neighbour on the enemy group
		if len(enemies)==1:
			ng=neighbouring_groups(enemies[0],board)
			safe=True
			#loop through all the neighbouring groups, if the group is owned by the player and the group is in atari then the ladder is no longer safe
			for g in ng:
				if board[g[0]]["player"]==player:
					if is_in_atari(g,board)==True:
						safe=False
			#if the ladder is safe then calculate the liberties of the enemy group. If it only has 2 liberties and we have one less free than the number of neighbours that surround the original tile then return True
			if safe==True:
				libs=liberties(enemies[0],board)
				if len(libs)==2:
					if frees+1==len(board[tile]["neighbours"]):
						v=True
	return v

#this function ????????????????????????
def capture(tile,player,board,distances,game_state):
	v=False
	if board[tile]["player"]==None:
		x = is_eye_candidate(tile,board)
		if x is not None:
			if x["owner"]==player:
				return False
		for n in board[tile]["neighbours"]:
			if board[n]["player"] is not None and board[n]["player"] != player:
				l=liberties(n,board)
				if len(l)==1:
					v=True
	return v

#this function checks whether a certain move will save a group that is in danger of being killed
def save_from_probable_death(tile,player,board,distances,game_state):
	v=False
	#if the tile is unoccupied then loop through all of it's neighbours
	if board[tile]["player"]==None:
		for n in board[tile]["neighbours"]:
			#if the neighbour is owned by me then calculate its liberties
			if board[n]["player"]==player:
				libs=liberties(n,board)
				#if there is only one liberty then pretend to play in the tile and calculate liberties again.
				if len(libs)==1:
					board[tile]["player"]=player
					newlibs=liberties(n,board)
					#undo the move and if there are now more than 2 liberties then it is a good move
					board[tile]["player"]=None
					if len(newlibs)>2:
						v=True
	return v
	
#this function tries to sneak into enemy territory, reducing the territory by a small number of points.
def sneak(tile,player,board,distances,game_state):
	v=False
	#if the tile is unowned, check whether it's an eye
	if board[tile]["player"]==None:
		eye=is_eye_candidate(tile,board)
		#if it is not an eye, then loop through its neighbours.
		if eye is None:
			for n in board[tile]["neighbours"]:
				#if the neighbour is owned by me then check whether the neighbour's group is alive, and if so then it is a good move
				if board[n]["player"]==player:
					a=is_alive(n,board)
					if a==True:
						v=True
	return v
				
#this function looks for 
def saviours(tile,board):
	player=board[tile]["player"]
	saviours=[]
	if player==None:
		return []
	else:
		first=is_alive(tile,board)
		if first==True:
			return []
		if first==False:
			libs=liberties(tile,board)
			for l in libs:
				board[l]["player"]=player
				second=is_alive(tile,board)
				board[l]["player"]=None
				if second==True:
					saviours.append(l)
	return saviours

#Each tile in only one list
def greatest_distance(board):
	distances=[[],[],[],[],[],[],[]]
	places_to_check=[]
	for tile in board:
		if len(board[tile]["neighbours"])<4:
			distances[0].append(tile)
		else:
			places_to_check.append(tile)
	for d in range(1,6):
		for t in board:
			if t in places_to_check:
				for n in board[t]["neighbours"]:
					if n  not in places_to_check:
						for p in distances:
							if n in p:
								i=distances.index(p)
						distances[i+1].append(t)
		for t in board:
			if t in distances[d]:
				places_to_check.remove(t)
	return distances

def is_allowed(tile,board,player,game_state):
	answer=False
	if board[tile]["player"]==None:
		if board[tile]["player"]==None and is_suicidal(player,tile,board)==False:
			if check_ko(player,tile,board,game_state)==False:
				answer=True
	return answer
