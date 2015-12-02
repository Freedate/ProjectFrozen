from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# stdlib


#pyglet
from pyglet.gl import *

# cocos2d related
from cocos.layer import Layer, ColorLayer
from cocos.scene import Scene
from cocos.director import director
from cocos.actions import *

# tetrico related
from gamectrl import *
from gamemodel import *
import levels
import gameover
from constants import *
import soundex
from HUD import *
from colors import *


__all__ = ['get_newgame']

class GameView( Layer ):

    def __init__(self, model, hud ):
        super(GameView,self).__init__()

        width, height = director.get_window_size()

        aspect = width / float(height)
        self.grid_size = ( int(20 *aspect),20)
        self.duration = 8

        self.position = ( width//2 - COLUMNS * SQUARE_SIZE // 2, 0 )
        self.transform_anchor = ( COLUMNS*SQUARE_SIZE //2, ROWS * SQUARE_SIZE//2)

        # background layer to delimit the pieces visually
        cl = ColorLayer( 112,66,20,50, width = COLUMNS * SQUARE_SIZE, height=ROWS * SQUARE_SIZE )
        self.add( cl, z=-1)

        self.model = model
        self.hud = hud

        self.model.push_handlers(   
                                    self.on_up_character, \
                                    self.on_level_complete, \
                                    self.on_new_level, \
                                    self.on_game_over, \
                                    self.on_win, \
                                    )

        self.hud.show_message( 'GET READY', self.model.start )

    def on_enter(self):
        super(GameView,self).on_enter()

        soundex.set_music('title.ogg')
        soundex.play_music()

    def on_exit(self):
        super(GameView,self).on_exit()
        soundex.stop_music()

    def on_up_character(self ):
        soundex.play('line.mp3')
        return True

    def on_level_complete( self ):
        soundex.play('level_complete.mp3')
        self.hud.show_message('Level complete', self.model.set_next_level)
        return True

    def on_new_level( self ):
        soundex.play('go.mp3')
        self.stop()
        self.do( StopGrid() )
        self.rotation = 0
        self.scale = 1
        return True

    def on_game_over( self ):
        self.parent.add( gameover.GameOver(win=False), z=10 )
        return True

    def on_win( self ):
        self.parent.add( gameover.GameOver(win=True), z=10 )
        return True

    def draw( self ):
        '''draw the map and the character'''

        glPushMatrix()
        self.transform()

        for i in range( COLUMNS ):
            for j in range( ROWS ):
                color = self.model.map.get( (i,j) )
                if color:
                    Colors.images[color].blit( i * SQUARE_SIZE, j* SQUARE_SIZE)

        if self.model.character:
            self.model.character.draw()

        glPopMatrix()

def get_newgame():
    '''returns the game scene'''
    scene = Scene()

    # model
    model = GameModel()

    # controller
    ctrl = GameCtrl( model )

    # view
    hud = HUD()
    view = GameView( model, hud )

    # set controller in model
    model.set_controller( ctrl )

    # add controller
    scene.add( ctrl, z=1, name="controller" )

    # add view
    scene.add( hud, z=3, name="hud" )
    scene.add( BackgroundLayer(), z=0, name="background" )
    scene.add( view, z=2, name="view" )

    return scene
