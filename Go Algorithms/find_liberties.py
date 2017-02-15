#This function will take in a position called t and the board and return the list of liberties that surround the group that contains the tile
def liberties(t,board):
    #set default values and find which player owns the position
    liberties=[]
    player=board[t]["player"]
    #add the position to places to check
    places_checked=[t]
    places_to_check=[]
    #loop through all the tile's neighbours and add them to places_to_check
    for n in board[t]["neighbours"]:
        places_to_check.append(n)
    
    #while there are still places to check, take the first place in the list, if it's empty add it to the liberties
    while len(places_to_check)>0:
        c=places_to_check[0]
        if board[c]["player"] is None:
            liberties.append(c)
        #or if the place is owned by the same player as the original tile then add all of it's neighbours to places to check, unless they are already there
        elif board[c]["player"]==player:
            for i in board[c]["neighbours"]:
                if i not in places_checked and i not in places_to_check:
                    places_to_check.append(i)
        #add the position we just checked to places checked and remove from places_to_check
        places_checked.append(c)
        places_to_check.remove(c)
    #return liberties
    liberties.sort()
    return liberties

#This function takes a tile and returns the group that contains it
def group(t,board):
    #add the original tile to the group and places_checked and find its player.
    group=[t]
    player=board[t]["player"]
    places_checked=[t]
    places_to_check=[]
    #loop through all of it's neighbours and add them to places to check
    for n in board[t]["neighbours"]:
        places_to_check.append(n)
        
    #while there are still places to check , take the first  place and if it's owned by the same player then add it to the group
    while len(places_to_check)>0:
        c=places_to_check[0]
        if board[c]["player"]==player:
            group.append(c)
            #loop through it's neighbours and if they haven't already been checked and aren't already in places to check then add them to places to check
            for i in board[c]["neighbours"]:
                if i not in places_checked and i not in places_to_check:
                    places_to_check.append(i)
        #add the checked tile to places_checked and remove it from places to check
        places_checked.append(c)
        places_to_check.remove(c)
    #return the group after sorting to allow 
    group.sort()
    return group

#This function takes in a tile and returns a list of all the groups that are touching the group that contains the original tile
def neighbouring_groups(t,board):
    #find the player who owns the tile and group it.
    neighbouring_groups=[]
    player=board[t]["player"]
    g=group(t,board)
    places_to_check=[]
    #loop through all the positions in the group, and loop through all of their neighbours adding them to places to check if they are owned by the enemy (not owned by player and not none)
    for i in g:
        for n in board[i]["neighbours"]:
            if board[n]["player"] is not None and board[n]["player"]!=player:
                places_to_check.append(n)
     #while there are still places to check, pick from the top of the list and find the group that contains that place. If this group is not already in neighbouring groups then add it.
    while len(places_to_check)>0:
        p=places_to_check[0]
        p_g=group(p,board)
        p_g.sort()
        if p_g not in neighbouring_groups:
            neighbouring_groups.append(p_g)
        #remove the place from places to check and then return the neighbouring groups
        places_to_check.remove(p)
    return neighbouring_groups

#This function takes a tile and if the piece is unowned it returns who's territory it is part of, or neutral if not.
def territory(t,board):
    #group the piece and initialise the neighbouring colours and places to check
    g=group(t,board)
    neighbouring_colours=[]
    places_to_check = []
    #loop through each piece in the group, and then through all of that pieces neighbours. If the neighbour is not part of the original group and is not already in places to check then add it to places to check
    for i in g:
        for n in board[i]["neighbours"]:
            if n not in g and n not in places_to_check:
                places_to_check.append(n)
                
    #loop through places to check and find the player who owns the piece. If that player's colour is not already in neighbouring_colours then add the colour to the list
    for p in places_to_check:
        q=board[p]["player"]
        if q not in neighbouring_colours:
            neighbouring_colours.append(q)
    #if the list only contains one element then return that colour, otherwise return neutral. 
    if len(neighbouring_colours)==1:
        return neighbouring_colours[0]
    else:
        return "Neutral"

#This function takes in a tile and returns whether the tile is a valid candidate for being an eye
def is_eye_candidate(t,board):
    if board[t]["player"]!=None:
        return None
    #it could belong to Black or White
    for p in ["Black","White"]:
        #bascially the group thing, but count opponents pieces as blank
        #candidate space stores the list of tile that will be inside the eye if it is an eye
        candidate_space=[t]
        places_checked=[t]
        places_to_check=[]
        #loops through the tile's neighbours and adds them to places to check
        for n in board[t]["neighbours"]:
            places_to_check.append(n)
        
        #while there are places to check, take the first place, if the colour of it is not the original player's colour then add it to candidate space
        while len(places_to_check)>0:
            c=places_to_check[0]
            if board[c]["player"]!=p:
                candidate_space.append(c)
                #loop through it's neighbours and add them to places to check unless already checked or already about to be checked
                for i in board[c]["neighbours"]:
                    if i not in places_checked and i not in places_to_check:
                        places_to_check.append(i)
            #add position to checked places and remove it from places to check
            places_checked.append(c)
            places_to_check.remove(c)
            
        #sort the candidates so that we can compare two eye spaces, and make the eye a "good" eye by default
        candidate_space.sort()
        good=True
        #loop through the eye space, and make each one not necessary for capture by default
        for i in candidate_space:
            necessary=False
            #loop through each of the tiles neighbours and if the neighbour is owned by the owner of the eye then make it necessary for capture
            for j in board[i]["neighbours"]:
                if board[j]["player"]==p:
                    necessary=True
            #if the tile is not necessary for capture then the eye is not good
            if necessary==False:
                good=False
        #if the tile is good then return results, where results is a dictionary referencing the group that contains the eye space and the player who own's that eye
        if good==True:
            results={"group":candidate_space,"owner":p}
            return results

#This function takes in a tile and returns whether the group that contains the piece is alive or dead.
def is_alive(t,board):
    eyes=[]
    #loop through all the liberties of the tile, and check whether the liberty is an eye candidate.
    for liberty in liberties(t,board):
        cand=is_eye_candidate(liberty,board)
        #if candidate exists and is owned by the same player as the original piece the add the candidate to eyes so long as it isn't in there already
        if cand is not None:
            if cand["owner"]==board[t]["player"]:
                if cand["group"] not in eyes:
                    eyes.append(cand["group"])
    #If there are at least two eyes then the group is alive, otherwise return false.
    if len(eyes)>=2:
        return True
    else:
        return False
                
#FALSE EYES
