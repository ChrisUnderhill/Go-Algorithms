from find_liberties import territory, group

#this function takes the board state and the current points and then counts territory and adds the poitns to the correct person
def count_territory(board,points):
	#loop through the board, if the place is unowned then find who owns the territory
    for i in board:
        if board[i]["player"] is None:
            colour=territory(i,board)
			#so long as the territory isn't neutral, then add points to the correct person's counter
            if colour != "Neutral":
                points[colour]=points[colour]+1
	#return new points
    return points

#this function takes the board, current capture points and whatever level of komi has been set and returns the new total points
def score(board,capture_points,komi):
    #count the number of points given to each player from captured territory
    territory_points=count_territory(board,{"Black":0,"White":0})
    total_points={"Black":0,"White":0}
	#for each of the two players, their total points are equal to points from capturing + komi if they had it + territory if they captured any
    for i in ["Black","White"]:
        total_points[i]=capture_points[i]+komi[i]+territory_points[i]
	#return the total points
    return total_points