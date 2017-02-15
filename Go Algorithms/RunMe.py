import imp
black = imp.load_source( "icarus", "C:/Users/cribcreaky/Documents/Homework/Y12/Computing/Go project/Programs/New/icarus.py" )
white = imp.load_source( "cunning_fox", "C:/Users/cribcreaky/Documents/Homework/Y12/Computing/Go project/Programs/New/cunning_fox.py" )
from game9 import *
def run():
	return play_game(black.play, white.play)
