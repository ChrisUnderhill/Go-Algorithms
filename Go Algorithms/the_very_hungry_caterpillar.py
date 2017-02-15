import random
from find_liberties import liberties, group, neighbouring_groups
from captures import is_suicidal, is_in_atari, is_ko

def play(player,board,game_state):
    #extend
    all_mine=True
    if game_state["last_pass"]==True:
        for i in board:
            if board[i]["player"] is not None:
                if board[i]["player"]!=player:
                    all_mine=False
    else: all_mine=False
    if game_state["moves_made"]==0:
        all_mine=False
    if all_mine==True: return "pass"
    allowed_moves = []
    idiotic_moves = []
    into_atari_moves=[]
    move=None
    people_who_need_saving = {} #dictionary of integers to list of lists
    people_who_need_saving_by_capture = []
    people_who_need_killing = {} #dictionary of integers to list of lists
    for i in board:
        if board[i]["player"] is None and is_suicidal(player,i,board)==False:
            if is_ko(player,i,board)==True and game_state["last_ko"]==True: break
            allowed_moves.append(i)
            idiotic_moves.append(i)
            idiot_perhaps = neighbouring_groups(i,board)
            for x in idiot_perhaps:
                if board[x[0]]["player"]!=player and board[x[0]]["player"] is not None and i in idiotic_moves:
                    idiotic_moves.remove(i)
            groupiee=group(i,board)
            n_groupies=neighbouring_groups(i,board)
            if len(groupiee)<=4:
                col=board[n_groupies[0][0]]["player"]
                for potato in n_groupies:
                    if board[potato[0]]["player"]!=col:
                        col=0
                if col in ["Black","White"]:
                    if i not in idiotic_moves:
                        idiotic_moves.append(i)
        #save yourself!
        elif board[i]["player"]==player:
            l=liberties(i,board)
            q=len(l)
            g=group(i,board)
            if q==1:
                saviour=l[0]
                board[saviour]["player"]=player
                saved_libs=liberties(saviour,board)
                board[saviour]["player"]=None
                if len(saved_libs)==1:
                    people_who_need_saving_by_capture.append(g)
                    break
            people_who_need_saving.setdefault(q, []).append(g)
        else:
            l=liberties(i,board)
            q=len(l)
            g=group(i,board)
            people_who_need_killing.setdefault(q, []).append(g)
    quacks={}
    for quark in people_who_need_saving:
        quacks[quark]=people_who_need_saving[quark]
    for quack in people_who_need_saving:
        if quack==0 or quack>=15:
            quacks.pop(quack)
    people_who_need_saving=quacks
    miaows={}
    for meow in people_who_need_killing:
        miaows[meow]=people_who_need_killing[meow]
    for miaow in people_who_need_killing:
        if miaow==0 or miaow>=15:
            miaows.pop(miaow)
    people_who_need_killing=miaows
    if len(people_who_need_saving)!=0:
        people_to_save = people_who_need_saving[ min(people_who_need_saving) ] #list of lists (groups in danger)
    else: people_to_save=[]
    if len(people_who_need_killing)!=0:
        people_to_kill = people_who_need_killing[ min(people_who_need_killing) ] #list of lists (groups in danger)
    else: people_to_kill=[]
    if len(people_to_kill)!=0:
        for k in people_to_kill:
            m=k[0]
            k_l = liberties(m,board)
            pond=[]
            for plant in k_l:
                pond.append(plant)
            for fish in k_l:
                if fish not in allowed_moves:
                    pond.remove(fish)
            if len(pond)>0:
                move=random.choice(pond)
            k_q = len(k_l)
    else: k_q=0
    if len(people_to_save)!=0:
        s=people_to_save[0]
        t=s[0]
        s_l = liberties(t,board)
        s_q = len(s_l)
        s_a = is_in_atari(s,board)
        if s_a is True:
            for j in people_to_save:
                n_g=neighbouring_groups(j[0],board)
                for n in n_g:
                    n_a = is_in_atari(n,board)
                    tree=[]
                    for coconut in s_l:
                        tree.append(coconut)
                    for conker in s_l:
                        if conker not in allowed_moves or conker in idiotic_moves:
                            tree.remove(conker)
                    if len(tree)>=1:
                        move=random.choice(tree)
                    if n_a is True:
                        l = liberties(n[0],board)
                        if l[0] in allowed_moves:
                            move=l[0]
        for jjj in people_who_need_saving_by_capture:
            n_g=neighbouring_groups(jjj[0],board)
            for n in n_g:
                n_a = is_in_atari(n,board)
                if n_a is True:
                    l = liberties(n[0],board)
                    if is_suicidal(player,l[0],board)==False:
                        move=l[0]
    else: s_q=0
    if move is None:
        good_opening_moves=["d3","c4","c6","d7","f7","f3","g4","g6"]
        djsfkh=[]
        for move in good_opening_moves:
            if move in allowed_moves:
                djsfkh.append(move)
        very_good_openings=[]
        for opening in djsfkh:
            alone=True
            for i in board[opening]["neighbours"]:
                if board[i]["player"] is not None:
                    alone=False
            if alone==True and opening in allowed_moves and opening not in idiotic_moves:
                very_good_openings.append(opening)
        if len(allowed_moves)<=80 and len(allowed_moves)>0:
            for z in idiotic_moves:
                if z in allowed_moves: allowed_moves.remove(z)
        if len(allowed_moves)>0:
            move=random.choice(allowed_moves)
        if len(allowed_moves)==0:
            move = "pass"
        if len(djsfkh)>0:
            move=random.choice(djsfkh)
        if len(very_good_openings)>0:
            move=random.choice(very_good_openings)
    return move
            
def intersections(list1,list2):
    copy1=[]
    for i in list1:
        if i in list2:
            copy1.append(i)
    return copy1
