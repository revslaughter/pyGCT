from mathgame import game

#zero game
g = game()

#star game
star = game('*')
star.Lput(g)
star.Rput(g)

#game one
o = game('1')
o.Lput(g)

#minus one
m = o.neg()

#up
up = game('up')
up.Lput(g)
up.Rput(star)

def makenum(n):
# makes a positive surreal integer n
	if n < 0:
		return makenum(n*-1).neg()
	i = 0
	number = game(str(n))
	builder = game()
	while i < n:
		builder = makenum(n-1)
		i+=1
	if i != 0:
		number.Lput(builder)
	return number
