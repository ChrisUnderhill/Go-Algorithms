import random

from find_liberties import group, neighbouring_groups, territory, liberties, is_eye_candidate
from captures import is_ko, is_suicidal, is_in_atari

def play(player,board):
    #this is a territorial player
    my_groups=[]
    enemy_groups=[]
    my_territory=[]
    enemy_territory=[]
    loosely_mine=[]
    loosely_enemy=[]
    neutral_space=[]
    allowed_moves=[]
    stupid_moves=[]
    fight_points=[]
    distances=distances_from_edge(board)
    #work out what's what
    for tile in board:
        if board[tile]["player"]==player:
            g=group(tile,board)
            if g not in my_groups:
                my_groups.append(g)
        elif board[tile]["player"] is None:
            if is_ko(player, tile, board)==False or game_state["last_ko"]==False:
                if is_suicidal(player, tile, board)==False:
                    allowed_moves.append(tile)
            sort_of_owner=loosely_territory(tile,board)
            if sort_of_owner==player:
                loosely_mine.append(tile)
            elif sort_of_owner=="Neutral":
                neutral_space.append(tile)
            elif sort_of_owner=="Nobody":
                fight_points.append(tile)
            else:
                loosely_enemy.append(tile)
            actual_owner=territory(tile,board)
            if actual_owner==player:
                my_territory.append(tile)
            elif actual_owner=="Neutral":
                pi=3.14
            else:
                enemy_territory.append(tile)
        else:
            h=group(tile,board)
            if h not in enemy_groups:
                enemy_groups.append(h)
    #forget about stuff inside other people's eyes
    for enemy_group in enemy_groups:
        rep=enemy_group[0]
        libs=liberties(rep,board)
        is_deaded=False
        eyeness=is_eye_candidate(libs[0],board)
        if eyeness==None:
            break
        else:
            if eyeness["owner"]==player:
                enemy_groups.remove(enemy_group)
            for l in eyeness["group"]:
                if l in allowed_moves:
                    stupid_moves.append(l)
                if l in fight_points:
                    fight_points.remove(l)
    for my_group in my_groups:
        rep=my_group[0]
        libs=liberties(rep,board)
        is_deaded=False
        eyeness=is_eye_candidate(libs[0],board)
        if eyeness==None:
            break
        else:
            if eyeness["owner"]!=player:
                my_groups.remove(my_group)
            for l in eyeness["group"]:
                if l in allowed_moves:
                    stupid_moves.append(l)
                if l in fight_points:
                    fight_points.remove(l)
    #1: if possible, make a non-alive group of mine be an alive group
    #2: make a nearly_alive group of the enemy's be a deaded group
    #3: seal off some loosely territory into proper territory (multiple seal points??)
    #4: claim some new loosely territory close-ish to the edge (row 3 or 4)
    #We do these in reverse order so that more important things overwrite the move variable
    move="pass"
    #So without further ado: Number 4:
    break_new_ground=[]
    for i in allowed_moves:
        if i in distances[2] or (i in distances[3] and i not in distances[5]):
            if i in neutral_space:
                break_new_ground.append(i)
    #Cool.  Now let's try Number 3, securing loose territory:
    fight_moves=[]
    for i in fight_points:
        if i in allowed_moves:
            fight_moves.append(i)
    #Before we do that, let's kill dangerous people, 2.5:
    saviours=[]
    for my_group in my_groups:
        a=is_in_atari(my_group,board)
        if a==True:
            n_g=neighbouring_groups(my_group[0],board)
            for nnn in n_g:
                b=is_in_atari(nnn,board)
                if b==True and nnn[0] in allowed_moves:
                    saviours.append(liberties(nnn[0],board)[0])
    feedback="I'm not doing anything"
    if len(fight_moves)>0:
        move=random.choice(fight_moves)
        feedback="I'm fighting"
    if len(break_new_ground)>0:
        move=random.choice(break_new_ground)
        feedback="I'm breaking new ground"
    if len(saviours)>0:
        move=random.choice(saviours)
        feedback="I'm saving people"
    #print(feedback)
    return move

def loosely_territory(tile,board):
    if board[tile]["player"]!=None:
        return None
    else:
        places_to_check=[]
        diagonal_adjacents=[]
        for n in board[tile]["neighbours"]:
            places_to_check.append(n)
            for m in board[n]["neighbours"]:
                if m in diagonal_adjacents:
                    places_to_check.append(m)
                if m!=tile:
                    diagonal_adjacents.append(m)
        owner=""
        for place in places_to_check:
            if owner=="":
                if board[place]["player"]!=None:
                    owner=board[place]["player"]
            else:
                if board[place]["player"]!=None and board[place]["player"]!=owner:
                    owner="Nobody"
        if owner=="":
            owner="Neutral"
    return owner

def surroundings(tile,board):
    places=[]
    diagonal_adjacents=[]
    for n in board[tile]["neighbours"]:
        places.append(n)
        for m in board[n]["neighbours"]:
            if m in diagonal_adjacents:
                places.append(m)
            if m!=tile:
                diagonal_adjacents.append(m)
    return places

def distances_from_edge(board):
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
