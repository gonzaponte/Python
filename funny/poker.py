from ROOT import TRandom3
R = TRandom3()
r = lambda: int( -0.5 + R.Uniform() * 53 )


suits   = [ 'hearts', 'spades', 'diamonds', 'clubs' ]
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

class card:
    def __init__( self, number, suit ):
        self.number = int( number )
        self.symbol = numbers[self.number]
        self.suit   = str( suit )

    def __repr__( self ):
        return self.symbol + ' of ' + self.suit

    def __eq__( self, other ):
        if self.number == other.number and self.suit == other.suit:
            return True
        return False

cards = [ card( number, suit ) for suit in suits for number in numbers ]


for i in xrange(10000):
    set = [ cards[ r() ] for i in range(5) ]

    for j in range(5):
        aux = len( filter( lambda x: x == set[j], set) ) - 1
        if aux:
            










