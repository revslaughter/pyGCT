from mathgame import *

# Lets you play a game g from the game class in mathgame.
# It's fun, but right now it's quite persnickity. One mis-type and you exit
# the game. It's best to copy/paste at this point.

def endgame(player):
		print "You have no options! Sorry, you lose."
		if player:
			return "Left lost!"
		else:
			return "Right lost!"

def turn(g, player):
	print g.name + " = "
	print g
	options = ""
	if player:
		for o in g.L:
			options += o.name + ", "
	else:
		for o in g.R:
			options += o.name + ", "

	if options:
		print "Ok, make your choice. Options are:"
		print options
		choice = raw_input("What'll it be? ")
		if player:
			for h in g.L:
				if choice == h.name:
					player = False
					print "\nRight's Turn:"
					turn(h, player)
		else:
			for h in g.R:
				if choice == h.name:
					player = True
					print "\nLeft's Turn:"
					turn(h, player)
	else:
		endgame(player)

def start(g):
	print "Left or Right goes First?"
	response = raw_input("L or R? ")
	if response == "L":
		player = True
		print "\nLeft's Turn:"
	if response == "R":
		player = False
		print "\nRight's Turn:"
	turn(g, player)
	
def play(g, end=True):
	start(g)
	return "Thanks for Playing!"
	
