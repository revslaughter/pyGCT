"""
A Python combinatorial game class.

Learn about Combinatorial Game Theory:
    http://www.ics.uci.edu/~eppstein/cgt/
    http://en.wikipedia.org/wiki/Combinatorial_game_theory

Combinatorial games can behave like numbers, but their iterative
nature makes them extremely difficult to compute.

One could also construct a subclass defining the surreal numbers
using the ordering methods (<=) in order to perform a member check.
The hope is that this can be used as a superclass to make programs
such as a nimber calculator, etc. and could even be used to make
on-the-fly calculations of a game in play.

For the time being, I can only represent games with a finite birthday.
I don't like that, but what with the reality constraints, it would be
pretty difficult to hold infinitely large numbers in a computer's memory.

Due to the intensively iterative nature of combinitorial games, it is
necessary to keep track of how your games are defined, lest you wind up
with enormous but simple games. It seems like five sums-of-sums
either breaks python or gets incalculably large. This is either due to my poor
coding or just the reality of how complicated games can get. I recommend the
simp() method to simplify number, as it produces an alike game.

This is my way of learning some Python and OOP in general,
please forgive/fix any inefficiencies. Please send comments/criticism to
prairie.squidman@gmail.com or improve the code at its home on GitHub:

https://github.com/revslaughter/pyGCT

TODO:
    -make a function to determine the best move for each player.
    -elimiate the limitation on num()
    -optimize the up function so that we can have better than 3up
    -error check the initial values so that if you enter in a number or
     a heap[0-9] or a col n* position that the class understands and reacts
     so that you don't have to input @^*&($ functions every time you make
     a new game.
    -see if there's a way to make addition or multiplication, uh, work good.
"""
class game:
    """
    Usage: g = game("name", left position, right position)
 
    Sans arguments, initializes to the 0 = {|} game, add other positions using
    the Lput or Rput methods.

    Options or positions of a game are themselves games.
    """
    def __init__(self, nom = "0", leftinit = None, rightinit = None):
        """
        It is ideal to name your game cleverly so that you don't get lost.

        Initializes to the 0 = {|} game, optional arguments allow you to
        define the position of your game.
        """
        self.L = []
        self.R = []

        if type(leftinit) is game:
            self.Lput(leftinit)

        if type(rightinit) is game:
            self.Rput(rightinit)

        self.name = nom

    def Lput(self, value):
        """
        Lput and Rput methods simply append using the List method
        to the appropriate list.
        """
        if type(value) is game:
            self.L.append(value)
        else:
            raise Exception("Item is not a game!")

    def Rput(self, value):
        """
        Lput and Rput methods simply append using the List method
        to the appropriate list.
        """
        if type(value) is game:
            self.R.append(value)
        else:
            raise Exception("Item is not a game!")
    def put(self, a=None, b=None):
        """
        Puts the first argument in the left, the second argument in the right.
        """
        if a:
            self.Lput(a)
        if b:
            self.Rput(b)

    def __repr__(self):
        """
        Shows the game in {L|R} format, according to the option's names
        If you name your games smartly, you should be able to tell what's
        inside them. Otherwise, this method may get pretty confusing.
        """
        printed = "{"
        if self.L:
            for g in self.L[:-1]:
                printed += (g.name + ", ")
            printed += (self.L[-1].name)
        printed += "|"
        if self.R:
            for g in self.R[:-1]:
                printed += (g.name + ", ")
            printed += (self.R[-1].name)
        printed += "}"
        return printed

    def __le__(self, other):
        """
        The Less Than or Equal to Relation.
        All comparisons between games are based upon the <= relation.
        Rule: For x = { x.L | x.R } and
        y = { y.L | y.R }, x <= y if and only if:
        There is no g in x.L such that y <= g, and
        there is no h in y.R such that h <= x.
        """
        for g in self.L:
            if other <= g:
                return False
        for h in other.R:
            if h <= self:
                return False
        return True

    def __eq__(self, other):
        """
        The Equivalence Relation. In CGT that means 'alike'.
        x == y iff x <= y and y <= x. This will help to 'simplify' games
        as games' respective option sets need not be equal for two
        games to be alike. ex: 0 == {|} == {-1|1} == {-3, -2 | 4} == {*|*}
        In this sense, we are not defining strict equality
        here, only 'alikeness' in order to easily form equivalence classes.
        One could use List object methods to check true ==.
        """
        if ((self <= other) and (other <= self)):
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Implements 'Not Alike'
        """
        if self == other:
            return False
        else:
            return True

    def __lt__(self, other):
        """
        Strictly less than. (Not unalike or great than or equal to)
        """
        if self <= other and other != self:
            return True
        else:
            return False

    def __ge__(self, other):
        """
        Greater than or equal to is the opposite of less than or equal to.
        Hooray for code reuse!
        """
        if other <= self:
            return True
        else:
            return False

    def __gt__(self, other):
        """
        Strictly greater than
        """
        if other < self:
            return True
        else:
            return False

    def fuzzy(self, other):
        """
        Fuzzy relation. This is a relation that games have that
        numbers don't. Games that are fuzzy to 0 are 0's 'opposite', as the
        first player has a winning strategy. Nimbers of the form n* = {n|n},
        n being any (surreal) number, n* || ('fuzzy to') n. It may be shown
        that any game that is either greater than, less than, or fuzzy to 0.
        We use this property to more easily define the fuzzy method.

        To check if a || b, use a.fuzzy(b)
        """

        if (self <= other) or (self >= other):
            return False
        else:
            return True
    
    def isnumber(self):
        """
        This method checks to see if the given game is a surreal number.

        Example: * = {0|0}. *.isnumber() == False
                 1 = {0|}. 1.isnumber == True
        """
        for g in self.L:
            for h in self.R:
                if h <= g:
                    return False
        return True
    def neg(self):
        """
        Returns a game negative to the input. 0 is its own negative.
        The rule is for G = {L|R}, -G = {-R|-L}
        """
        
        if self.L != [] or self.R != []:
            n = game("-" + self.name)
            for g in self.L:
                n.Rput(g.neg())
            for g in self.R:
                n.Lput(g.neg())
            return n
        else:
            return self

    def __add__(self, other):
        """
        Natural '+' operator overloading for adding ease-of-use.
        Rule is G + H = {[G.L + H, G + H.L] | [G.R + H, G + H.R]}
        When we reach g + empty, do nothing.
        WARNING: Iterations of addition deeper than 4 are very system-taxing.
        """
        added = game("(" + self.name + " + " + other.name + ")")
        if self.L:
            for g in self.L:
                added.Lput(g + other)
        if other.L:
            for g in other.L:
                added.Lput(g + self)
        if self.R:
            for g in self.R:
                added.Rput(g + other)
        if other.R:
            for g in other.R:
                added.Rput(g + self)
        return added

    def __sub__(self, other):
        """
        Subtraction is easy when we have additive inverses!
        """
        return self + other.neg()

    def __mul__(self, other):
        """
        Multiplying games is extremely complicated by hand.

        The rule is
        X * Y = {((X.L * Y) + (X * Y.L) - (X.L * Y.L)),
                 ((X.R * Y) + (X * Y.R) - (X.R * Y.R))
                                |
                ((X.L * Y) + (X * Y.R) - (X.L * Y.R)),
                ((X * Y.L) + (X.R * Y) - (X.R * Y.L))}

        Division is a nightmare - anything that isn't a dyadic/binary rational
        is an infinite limit, and recall that this game class cannot hope to
        output games born on day omega as their lists have an infinite number
        of members. Not too worried about it - mul isn't well-defined for
        games, just numbers.
        """
        product = game("(" + self.name + " * " + other.name + ")")
        
        alg = lambda a, b, c, d: ((a * b) + (c * d) - (a * d))

        for g in self.L:
            for h in other.L:
                product.Lput(alg(g, other, self, h))
            for h in other.R:
                product.Rput(alg(g, other, self, h))

        for g in self.R:
            for h in other.R:
                product.Lput(alg(g, other, self, h))
            for h in other.L:
                product.Rput(alg(g, other, self, h))
        return product

    def simp(self):
        """
        Simplifies a game to an alike game with fewer options, useful when
        repeatedly adding or multiplying games. Rule is that any number
        g = {a, b, ... | d, ...} is equivalent to {a | d} if a is the
        greatest option in the left side and d is the least option in the
        right side.
        """
        if self.isnumber():
            self.L.sort()
            self.R.sort()
            del self.L[:-1]
            del self.R[1:]
            return self
        else:
        #I'm still working on this part - what if G isn't a number? Left
        #would still want the greatest value...but what if they're all
        #fuzzy, or Nimber-y? Until implemented, I'm returning self 
        #if self isn't a number.
            return self
    def winner(self):
        """
        Determines who has the advantage to a particular game. Useful if you
        have an interesting game constructed and can't tell by looking.

        This is sort of the point of the whole thing. Should probably just
        return numbers or some other signal beside strings: 0,1,2,3

        That way people can actually use them in their programs and stuff.

        The question of who has the winning strategy all depends on how the
        game relates to zero.
        """
        z = game()
        if self < z:
            return 0
        elif self == z:
            return 1
        elif self > z:
            return 2
        else:
            return 3

def num(n):
    """
    Makes a surreal integer n.
    
    Can't make numbers larger than +994, -993 due to maximum recursion depth
    (default 1000).
    See Guido's post at:
    http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html
    
    For values between the above, this function is nice and fast. (as opposed
    to before!!)

    TODO: Make this based on iteration rather than recursion. How?
    """
    if n < 0:
        return num(n*-1).neg()
    number = game(str(n))
    builder = game()
    if n != 0:
        number.Lput(num(n-1))
    return number

def col(n):
    """
    Makes a col position n* = {n|n} from number n.
    """
    numb = game(str(n) + "*")
    numb.Lput(num(n))
    numb.Rput(num(n))
    return numb

def nim(n):
    """
    Makes a nim-heap of blocks n. n needs to be an integer.
    """
    nimber = game("heap" + str(n))
    builder = game()
    for i in range(n):
        builder = nim(i)
        nimber.Lput(builder)
        nimber.Rput(builder)
    return nimber

def up(n):
    """
    Makes up and up-games. For instance, up(0) is 0,
    up(1) is up, up(2) is double-up, etc.
    Algorithm is super super clunky. Python quits on up(4).
    Addition is waaay better than multiplication though
    as addition has only 4 self-calls while multiplication has 12 along with 6
    addition calls, each of which having 4 self-calls. Awesome.

    What's cool about up is that it's a surreal number that has no analog
    in the real numbers -- up is the proverbial 'smallest number' that is
    'right next to' zero! Its equivalent is 1/infinity.
    """
    if n == 0:
        return num(0)
    if n < 0:
        return up(n * -1).neg()
    i = 1    
    upp = game("up")
    upp.put(num(0), num(1))
    while i < n:
        upp += upp
        upp.name = (str(i) + "up")
        i += 1
        upp.simp()
    upp.name = (str(n) + "up")
    return upp

def windecode(num):
    """
    Just a function wrapper for a dictionary to return strings
    that interpret the value of game.winner()
    """
    di = {
        0:"Right has a winning strategy",
        1:"Second Player has a winning strategy",
        2:"Left has a winning strategy",
        3:"First player has a winning strategy"
        } #winning codes revealed!
    return di[num]

star = game("*", num(0), num(0))
up1 = up(1)
zero = game()
one = num(1)
negone = num(-1)