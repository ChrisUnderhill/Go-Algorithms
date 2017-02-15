#import scoring functions and deathcheckers and graphics etc
from captures import check_captures
from ko import stringy, is_ko, unstring
from find_liberties import liberties
from scoring import score
from board9 import make_a_board
from GUI import setupDrawing, update,  delete

#This function will take in two player functions and a parameter to tell it whether to draw graphics or not, and then runs a game between the two players
def play_game(player1,player2, graphics=True):
  #make a board and set all the default values
  board=make_a_board()
  game_state={"in_progress":True,"last_pass":False,"last_ko":False,"capture points":{"Black":0,"White":0},"moves_made":0,"history":[]}

  x="pass"
  y="pass"
  
  #if drawing graphics then remove all the current screen drawings and redraw the screen in size 9x9
  if graphics==True:
    delete()
    setupDrawing(9)
    
  #while the game is still in progress...
  while game_state["in_progress"]==True:
    #take a move from player1, if it's pass then set last_pass to true and if the previous move was a pass as well then end the game
    x=player1("Black",board, game_state)
    if x=="pass":
      print("black passed")
      if game_state["last_pass"]==True:
        game_state["in_progress"]=False
        print("game over")
      game_state["last_pass"]=True
      
    #if x is not a move that exists on the board then pass instead
    elif x not in board:
      print("Black was really really stupid")
      game_state["last_pass"]=True
      
    #if x is already occupied then pass instead
    elif x in board and board[x]["player"]!=None:
      print("Black was Stupid")
      game_state["last_pass"]=True
      
    #otherwise so long as the move is not pass and the tile is unowned then play there
    else:
      if x!="pass":
        game_state["last_pass"]=False
        if board[x]["player"] is None:
          board[x]["player"] = "Black"
          
          #check if any captures have happened, and check if the new board state is ko or not
          board=check_captures(x,board,game_state["capture points"])
          k=is_ko(board,game_state["history"])
          #if the move is ko then return the board to it's previous state and set last_pass to true
          if k==True:
            board=unstring(board,game_state["history"][-1])
            game_state["last_pass"]=True
            print("Black attempted ko")
          #calculate the liberties of the group containing the piece that was just played in
          l=liberties(x,board)
          q=len(l)
          #if the piece has no liberties then undo the move and set last pass to true
          if q==0:
            #print ("Black was suicidal")
            board[x]["player"]=None
            game_state["last_pass"]=True
    #add one to moves made (even pass counts as a move in this case) and add the hash of board state to history
    game_state["moves_made"]=game_state["moves_made"]+1
    game_state["history"].append(stringy(board))
    
    #if graphics is true then draw the new board and then check if game is still in progress
    if graphics==True:
      update(board)
    if game_state["in_progress"]==True:
      #take a move from player1, if it's pass then set last_pass to true and if the previous move was a pass as well then end the game
      y=player2("White",board,game_state)
      if y=="pass":
        print("white passed")
        if game_state["last_pass"]==True:
          game_state["in_progress"]=False
          print("game over")
        game_state["last_pass"]=True
      
      #if y is not a move that exists on the board then pass instead
      elif y not in board:
        print("White was really really stupid")
        game_state["last_pass"]=True
      
      #if y is already occupied then pass instead
      elif y in board and board[y]["player"]!=None:
        print("White was Stupid")
        game_state["last_pass"]=True
        
      #otherwise so long as the move is not pass and the tile is unowned then play there
      else:
        if y!="pass":
          game_state["last_pass"]=False
          if board[y]["player"] is None:
            board[y]["player"] = "White"
            
            #check if any captures have happened, and check if the new board state is ko or not
            board=check_captures(y,board,game_state["capture points"])
            k=is_ko(board,game_state["history"])
            #if the move is ko then return the board to it's previous state and set last_pass to true
            if k==True:
              board=unstring(board,game_state["history"][-1])
              game_state["last_pass"]=True
              print("Black attempted ko")
            #calculate the liberties of the group containing the piece that was just played in
            l=liberties(y,board)
            q=len(l)
            #if the piece has no liberties then undo the move and set last pass to true
            if q==0:
              #print ("Black was suicidal")
              board[y]["player"]=None
              game_state["last_pass"]=True
      #add one to moves made (even pass counts as a move in this case)
      game_state["moves_made"]=game_state["moves_made"]+1
      game_state["history"].append(stringy(board))
      
      #if graphics is true then draw the new board and then check if game is still in progress
      if graphics==True:
        update(board)
  
  #at the end of the game score the board and then return this dictionary.
  points=score(board,game_state["capture points"],{"Black":0,"White":5.5})
  return points

#This competition function plays a certain number of games between two players without drawing the graphics
def competition(player1, player2, gameNum):
  
  #set games won to 0 for each.
  games_won={"Black":0,"White":0}
  
  #half of the games should be played as each colour. 
  for i in range(0,gameNum//2):
    #get the poitns from the game and if black has more points then add points to black and if not then add points to white (draws are impossible in go)
    points=play_game(player1,player2, False)
    if points["Black"]>points["White"]:
      games_won["Black"]=games_won["Black"] + 1
    else:
      games_won["White"]=games_won["White"] + 1
    print (i)
    
  #The other half of the games need to be played as the other colour, so player1 and player2 are reversed in teh play_game function call
  for i in range(0,gameNum//2):
    points=play_game(player2,player1, False)
    
    #white is now black and vice versa, so if white scored more points then give black a point to games_won 
    if points["White"]>points["Black"]:
      games_won["Black"]=games_won["Black"] + 1
    else:
      games_won["White"]=games_won["White"] + 1
    print (i)
    
  #return the number of games won by each player, where "Black" is really player1 and "White" is really player 2.
  return games_won
