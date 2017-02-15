import random
from find_liberties import *
 
#This is function is a fairly basic "AI" that selects a favourable position to play in and then returns that position
def play(player, board, game_state):
    #Allowedmoves stores ALL of the moves that are allowed by the rules of the game (excluding ko). 
    allowedMoves=[]
    myGroups=[]
    enemyGroups=[]
    goodAttackMoves=[]
    goodDefendMoves=[]
    #AttackLibs and DefendLibs are used to store the number of liberties that a "goodAttackMove" or "goodDefendMove" will add or remove from a group.
    attackLibs=[]
    defendLibs=[]
    #move is the move that will be returned
    move = None
    
    #loop through all the positions on the board, if the position is not already owned and is not suicidal for me then add the move to allowed moves (this ignores ko but this was deliberate, as this helped to shorten games significantly)
    for i in board:
        if board[i]["player"] is None and is_suicidal(player,i,board)==False:
            allowedMoves.append(i)
        #or if the position is occupied, then find it's containing group. If the player who owns it is me then add it to myGroups, otherwise add it to enemyGroup
        else:
            g=group(i, board)
            if board[g[0]]["player"] == player:
                if g not in myGroups:
                    myGroups.append(g)
                    ##print("mine")
            else:
                if g not in enemyGroups:
                    enemyGroups.append(g)
                    ##print("enemy")
            
    #loop through all of my groups and find the number of liberties they possess
    for g in myGroups:
        myLibs=liberties(g[0], board)
        if True:
            #loop through every piece in the group and then through all of its neighbours 
            for i in g:
                for n in board[i]["neighbours"]:
                    #if the neighbour has no owner and is in allowedMoves then play there and calculate it's liberties
                    if board[n]["player"]==None and n in allowedMoves:
                        board[n]["player"]=player
                        nLibs=liberties(i,board)
                        #if it has more liberties now that it did originally then set the original liberties to the new liberteis and set it as the chosen move
                        if len(nLibs)>len(myLibs):
                            myLibs=nLibs
                            move=n
                        #undo the move
                        board[n]["player"]=None
            #if the move is not already a goodDefendMove and it's not None then add it to goodDefendMoves, and append the new number of liberties to defendLibs
            if move not in goodDefendMoves and move!=None:
                goodDefendMoves.append(move)
                defendLibs.append(len(myLibs))
    
    #loop through all enemy groups and calculate their liberties
    for g in enemyGroups:
        myLibs=liberties(g[0], board)
        #loop through each group and then loop through all of its neighbours
        for i in g:
            for n in board[i]["neighbours"]:
                #if the neighbour is not owned by anyone and is in allowedmoves then play there and calculate it's new liberties
                if board[n]["player"]==None and n in allowedMoves:
                    board[n]["player"]=player
                    nLibs=liberties(i,board)
                    #if it now has less liberties than before then add make it the selected move and set the new libs as the baselin
                    if len(nLibs)<len(myLibs):
                        myLibs=nLibs
                        move=n
                    #undo the move
                    board[n]["player"]=None
        #if the move is not already an attackMove and isn't none then add it to good attack moves and append it's liberties as well
        if move not in goodAttackMoves and move!=None:
            goodAttackMoves.append(move)
            attackLibs.append(len(myLibs))
            #if there are no liberties after the move (ie the group is killed), then return the move
            if len(nLibs)==0:
                return move
    
    #try to select a random allowedMove, or if none exist then pass instead
    try:
        move=random.choice(allowedMoves)
    except:
        move="pass"
            
    #try sorting goodDefendMoves according to the number of liberties that the move has, then reverse it so that it's in descending order
    try:
        defendLibs, goodDefendMoves = (list(x) for x in zip(*sorted(zip(defendLibs, goodDefendMoves))))
        defendLibs.reverse()
        goodDefendMoves.reverse()
        #if the best move has more than 6 liberties then pick that move
        if defendLibs[0]>=6:
            move=goodDefendMoves[0]
    #if there are no goodDefendMoves then just print back to the screen
    except:
        pass
    
    #try sorting goodAttackMoves by the number of liberties.
    try:
        attackLibs, goodAttackMoves = (list(x) for x in zip(*sorted(zip(attackLibs, goodAttackMoves))))
        #if a move decreases an enemy group to below two liberties then return that as the move immediately
        if attackLibs[0]<=2:
            return goodAttackMoves[0]
    #or if tehre are no goodAttackMovs then just print back to the screen
    except:
        pass
    
    
    #if the board is empty then play at d4, a good starting move    
    if len(allowedMoves)==81:
        return "d4"
    else:
        return move


#This function takes a player, move and board state and returns whether the move would be suicidal
def is_suicidal(player,move,board):
    #by default the move is not suicidal. Pretend to play there and calculate the new liberties
    response=False
    board[move]["player"]=player
    l=liberties(move, board)
    
    #if there are no liberties left then the move is suicidal, undo the move and return the response
    if len(l)==0:
        response = True #although this technically isn't true, a move that capture despite being "suicidal" isn't counted as a suicide, if I let the AI make these kinds of moves then it would be very unlikely to ever pass and games would go on for far too long
    board[move]["player"]=None
    return response

#this function takes in a group and checks whether the group is in atari (only has 1 liberty)
def is_in_atari(group,board):
    #take the first tile from the group and calculate it's liberties
    p=group[0]
    l=liberties(p,board)
    #if the group only has 1 liberty then return true, otherwise return false
    if len(l)==1:
        return True
    else:
        return False
