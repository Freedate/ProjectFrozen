from __future__ import division, print_function, unicode_literals

__all__ = [ 'status' ]

class Status( object ):
    def __init__( self ):

        # current score
        self.score = 0

        # current lifes
        self.lifes = 5

        # current level
        self.level = None

        # current level idx
        self.level_idx = None

    def reset( self ):
        self.score = 0
        self.lifes = 5
        self.level = None
        self.level_idx = None

status = Status()
