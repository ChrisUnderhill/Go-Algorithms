# "be patterns, be examples in all countries, places, islands, nations... then you will come to walk cheerfully over the world"

import random
from find_liberties import liberties, group, neighbouring_groups, is_eye_candidate, is_alive
from captures import is_suicidal, is_in_atari, is_ko


def old_fox(player,board,game_state):
    distances=greatest_distance(board)
    patterns=[seal_the_edges,seal_off_territory,connect_lonely_people,invade_large_empty_space,save_from_certain_death]
    move="pass"
    for i in patterns:
        responses=i(player,board,distances,game_state)
        if len(responses)>0:
            move=random.choice(responses)
    return move

def invade_large_empty_space(player,board,distances,game_state):
    moves=[]
    for tile in board:
        if tile in distances[2]:
            good=False
            if board[tile]["player"]==None and is_suicidal(player,tile,board)==False:
                if is_ko==False or game_state["last_ko"]==False:
                    good=True
            for n in board[tile]["neighbours"]:
                if board[n]["player"] is not None:
                    good=False
                if n in distances[1]:
                    for nn in board[n]["neighbours"]:
                        if nn != tile and board[nn]["player"] is not None:
                            good=False
            if good==True:
                moves.append(tile)
    return moves

def seal_off_territory(player,board,distances,game_state):
    aims=[]
    moves=[]
    for tile in distances[2]:
        if board[tile]["player"]==player:
            for n in board[tile]["neighbours"]:
                if n in distances[2]:
                    if board[n]["player"] is None:
                        aims.append(n)
                        for nn in board[n]["neighbours"]:
                            if nn in distances[2] and nn!=tile:
                                if board[nn]["player"] is None:
                                    aims.append(nn)
                if n in distances[1]:
                    good=True
                    for nn in board[n]["neighbours"]:
                        if board[nn]["player"]==player and nn in distances[1]:
                            good=False
                    if good==True:
                        aims.append(n)
    for i in aims:
        if board[i]["player"]==None and is_suicidal(player,i,board)==False:
                if is_ko==False or game_state["last_ko"]==False:
                    moves.append(i)
    return moves

def seal_the_edges(player,board,distances,game_state):
    aims=[]
    moves=[]
    for tile in distances[1]:
        if board[tile]["player"]==player:
            for n in board[tile]["neighbours"]:
                if n in distances[0]:
                    if board[n]["player"] is None:
                        aims.append(n)
                    elif board[n]["player"]!=player:
                        for nn in board[n]["neighbours"]:
                            if nn in distances[0]:
                                for nnn in board[nn]["neighbours"]:
                                    if board[nnn]["player"] is not None and board[nnn]["player"] != player and nnn is not n:
                                        aims.append(nn)
    for i in aims:
        if board[i]["player"]==None and is_suicidal(player,i,board)==False:
                if is_ko==False or game_state["last_ko"]==False:
                    moves.append(i)                            
    return moves

def connect_lonely_people(player,board,distances,game_state):
    aims=[]
    moves=[]
    my_groups=[]
    for tile in board:
        if board[tile]["player"]==player:
            g=group(tile,board)
            if g not in my_groups:
                my_groups.append(g)
    for my_group in my_groups:
        libs=liberties(my_group[0],board)
        for l in libs:
            for n in board[l]["neighbours"]:
                for mg in my_groups:
                    if n in mg:
                        if mg != my_group:
                            aims.append(l)
                    if n in liberties(mg[0],board):
                        if mg != my_group:
                            aims.append(l)
    for i in aims:
        if board[i]["player"]==None and is_suicidal(player,i,board)==False:
                if is_ko==False or game_state["last_ko"]==False:
                    good=False
                    for n in board[i]["neighbours"]:
                        a=is_alive(n,board)
                        if a==False:
                            good=True
                    if good==True:
                        moves.append(i)                  
    return moves

def save_from_certain_death(player,board,distances,game_state):
    moves=[]
    my_groups=[]
    for tile in board:
        if board[tile]["player"]==player:
            g=group(tile,board)
            if g not in my_groups:
                my_groups.append(g)
    for my_group in my_groups:
        if is_alive(my_group[0],board)==False:
            libs=liberties(my_group[0],board)
            for l in libs:
                board[l]["player"]=player
                if is_alive(my_group[0],board)==True:
                    moves.append(l)
                board[l]["player"]=None
                for n in board[l]["neighbours"]:
                    if board[n]["player"]==None:
                        board[n]["player"]=player
                        if is_alive(my_group[0],board)==True:
                            moves.append(n)
                        board[n]["player"]=None
    return moves

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

#Each tile in one or two lists
def distances_from_edge(board):
    size=(len(board))**0.5
    distances=[[]]
    i=int(size/2 + 2)
    alpha="abcdefghijklmnopqrstuvwxyz"
    for j in range(0,i):
        k=[]
        for tile in board:
            a=alpha.index(tile[0])
            if a>(size)/2:
                a=size-a-1
            n=int(tile[1:])-1
            if n>(size)/2:
                n=size-n-1
            if a==j or n==j:
                k.append(tile)

        #print k
        distances.append(k)    
    return distances
