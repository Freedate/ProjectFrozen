import sys, os
import pygame


SCREEN_SIZE = [1000,400]
WHITE=(255,255,255)
x = 100
y = 100

class Blocks(pygame.sprite.Sprite):
    def __init__(self, type, xy):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if type==0:
            self.image = pygame.image.load(os.path.join('block.png'))
        elif type==1:
            self.image = pygame.image.load(os.path.join('ground.png'))
        self.image.convert()
        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = xy

    def transform(self,type):
        self.type = type
        if type==0:
            self.image = pygame.image.load(os.path.join('block.png'))
        elif type==1:
            self.image = pygame.image.load(os.path.join('ground.png'))
        self.image.convert()

class Character(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('fez.png'))
        self.image.convert()
        self.rect = self.image.get_rect()

        self.rect.left, self.rect.top = x,y


class Game(object):
    #char = pygame.image.load('fez.png')
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('쌓아라 뛰어라')
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(SCREEN_SIZE)
        self.background.fill(WHITE)
        pygame.display.flip()
        
        self.initChar(100,100)

    def initChar(self,x,y):
        char = Character(x,y)
#        self.window.blit(char, (x,y))
        all_sprites_list = pygame.sprite.Group()
        all_sprites_list.add(char)
        all_sprites_list.draw(self.window)


    def run(self):
        crashed = False

        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -5
                    elif event.key == pygame.K_RIGHT:
                        x_change = 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0

            
           

            #print(event)

            pygame.display.update()
            self.clock.tick(60)
        

if __name__ == '__main__':
    game = Game()
    game.run()
