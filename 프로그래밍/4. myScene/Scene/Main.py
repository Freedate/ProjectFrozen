#from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from cocos.director import director
from cocos.layer import *
from cocos.scene import Scene
from cocos.scenes.transitions import *
from cocos.actions import *
from cocos.sprite import *
from cocos.menu import *
from cocos.text import *

import pyglet
from pyglet import gl, font
from pyglet.window import key

from HUD import BackgroundLayer
import soundex
import hiscore

class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('쌓아라 뛰어라')

        #self_select_sound = soundex.load('move.mp3')

        self.font_title['font_name'] = 'HUCreA'
        self.font_title['font_size'] = 72
        self.font_title['color'] = (255,255,0, 255)

        self.font_item['font_name'] = 'HUCreA',
        self.font_item['color'] = (255,255,0, 255)
        self.font_item['font_size'] = 36
        self.font_item_selected['font_name'] = 'HUCreA'
        self.font_item_selected['color'] = (255,0,0, 255)
        self.font_item_selected['font_size'] = 48


        self.menu_anchor_y = CENTER
        self.menu_anchor_x = CENTER
        
        items = []

        items.append( MenuItem('게임 시작', self.on_new_game) )
        items.append( MenuItem('환경 설정', self.on_options) )
        items.append( MenuItem('랭킹', self.on_scores) )
        items.append( MenuItem('끝내기', self.on_quit) )

        self.create_menu( items, shake(), shake_back() )

    def on_new_game(self):
        import gameview
        director.push(FlipX3DTransition(gameview.get_newgame(), 1.5))

    def on_options( self ):
        self.parent.switch_to(1)

    def on_scores( self ):
        self.parent.switch_to(2)

    def on_quit(self):
        pyglet.app.exit()

if __name__ == "__main__":

    pyglet.resource.path.append('res')
    pyglet.resource.reindex()
    font.add_directory('res')

    director.init( resizable=True, width=960, height=540 , autoscale=True, fullscreen = False)
    scene = Scene()
    scene.add( MultiplexLayer(
                   MainMenu())
    #                OptionsMenu(),
    #                ScoresLayer(),
    #                ),
               ,z=1) 
    scene.add( BackgroundLayer(), z=0 )
    director.run( scene )