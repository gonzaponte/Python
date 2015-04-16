from RandomNumbers import MersenneTwister as MT
R = MT()

suits   = [ 'hearts', 'spades', 'diamonds', 'clubs' ]
#suits   = [ 'H', 'S', 'D', 'C' ]
numbers = {}
numbers[2]  = '2'
numbers[3]  = '3'
numbers[4]  = '4'
numbers[5]  = '5'
numbers[6]  = '6'
numbers[7]  = '7'
numbers[8]  = '8'
numbers[9]  = '9'
numbers[10] = '10'
numbers[11] = 'J'
numbers[12] = 'Q'
numbers[13] = 'K'
numbers[14] = 'A'
ranks = map( str, range(2,11) ) + [ 'J', 'Q', 'K', 'A' ]

class card:
    def __init__( self, number, suit ):
        self.rank = number
        self.suit = suit

    def __repr__( self ):
        return self.rank + ' of ' + self.suit

    def __eq__( self, other ):
        return True if self.rank == other.rank and self.suit == other.suit else False
    
    def SameRank( self, other ):
        return self.rank == other.rank

    def SameSuit( self, other ):
        return self.rank == other.rank

class Deck:
    cards = [ card(i,s) for s in suits for i in ranks ]
    out = []
    def __call__( self ):
        while True:
            c = R.Choose(self.cards)
            if not c in self.out:
                self.out.append(c)
                return c

def PocketPair( N = 1e6 ):
    deck = Deck()
    p = 0.
    for i in xrange(int(N)):
        deck.out = []
        card1 = deck()
        card2 = deck()
        if card1.SameRank(card2):
            p += 1.
    return p/N

def PocketSuited( N = 1e6 ):
    deck = Deck()
    p = 0.
    for i in xrange(int(N)):
        deck.out = []
        card1 = deck()
        card2 = deck()
        if card1.SameSuit(card2):
            p += 1.
    return p/N

print PocketPair()
print PocketSuited()

