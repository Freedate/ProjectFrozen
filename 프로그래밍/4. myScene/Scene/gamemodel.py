from __future__ import division, print_function, unicode_literals

# pyglet related
import pyglet

# This code is so you can run the samples without installing the package
import sys
import os
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

working_dir = os.path.dirname(os.path.realpath(__file__))
pyglet.resource.path = [os.path.join(working_dir,'data')]
pyglet.resource.reindex()

# stdlib
import copy
import random
import weakref


# cocos2d related
from cocos.euclid import Point2

# tetrico related
from constants import *
from status import status
from colors import *
import levels

__all__ = ['GameModel']

#
# Model (of the MVC pattern)
#

class GameModel( pyglet.event.EventDispatcher ):

    def __init__(self):
        super(GameModel,self).__init__()

        self.init_map()

        # current character
        self.character = Character()

        # grid
        self.map = {}

        # init
        status.reset()


        # phony level
        status.level = levels.levels[0]
        
    def set_controller( self, ctrl ):
        self.ctrl = weakref.ref( ctrl )

    def start( self ):
        self.set_next_level()
        
    def set_next_level( self ):
        self.ctrl().resume_controller()

        if status.level_idx is None:
            status.level_idx = 0
        else:
            status.level_idx += 1


        l = levels.levels[ status.level_idx ]

        self.init_map()
        status.level = l()
        
        self.dispatch_event("on_new_level")

    def init_map(self):
        self.map= {}
        for i in range( COLUMNS ):
            for j in range( ROWS ):
                self.map[ (i,j) ] = 0

    # character moves
    def char_right( self ):
        self.character.backup()
        self.character.sprite.x += 5
        if not self.is_valid_move():
            self.character.restore()
        else:
            self.dispatch_event("on_move_char")

    def char_left( self ):
        self.character.backup()
        self.character.sprite.x -= 5
        if not self.is_valid_move():
            self.character.restore()
        else:
            self.dispatch_event("on_move_char")

    def char_up( self, sound=True ):
        # jump
        self.character.backup()
        self.character.sprite.y += 5
        if not self.is_valid_move():
            self.character.restore()
        else:
            if sound:
                self.dispatch_event("on_move_char")

    def is_valid_move( self ):
        # collision with maps
        # for now, collision with tetris map. we should fix this
        
        return True
   
class Character( object ):

    def __init__(self):
        super( Character, self ).__init__()

        self.pos = Point2( COLUMNS//2-1, ROWS )
        self.status = 'STAY'

        s0 = pyglet.resource.image('fez.png')
        sprites = [s0]

        anim = pyglet.image.Animation.from_image_sequence(sprites, 0.5, True)
        self.sprite = pyglet.sprite.Sprite(anim)

    def draw( self ):
        '''draw character'''
        self.sprite.draw()
            
    def backup( self ):
        '''saves character'''
        self.save_pos = copy.copy( self.sprite.position )
        self.save_status = self.status

    def restore( self ):
        '''restore character'''
        self.sprite.position = self.save_pos
        self.status = self.save_status
        
GameModel.register_event_type('on_move_char')
GameModel.register_event_type('on_up_character')
GameModel.register_event_type('on_level_complete')
GameModel.register_event_type('on_new_level')
GameModel.register_event_type('on_game_over')
GameModel.register_event_type('on_win')