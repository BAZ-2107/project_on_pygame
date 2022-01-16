# -*- coding: utf-8 -*-
import pygame
from functions import *

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        self.frames = [load_image('r1.png', 'aboutMario'), load_image('r2.png', 'aboutMario'),
                       load_image('l1.png', 'aboutMario'), load_image('l2.png', 'aboutMario')]
        self.cur_frame = 0
        self.r, self.l = self.frames[:2], self.frames[2:]
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((x, y))
                
    def setPos(self, pos):
        self.rect.x, self.rect.y = pos

    def update(self, pos=None):
        self.cur_frame = (self.cur_frame + 1) % 2
        if pos == 'right':
            self.image = self.r[self.cur_frame]
        if pos == 'left':
            self.image = self.l[self.cur_frame]

#Класс текстур    
class Tecstures(pygame.sprite.Sprite):
    def __init__(self, elem, group):
        super().__init__(group)
        if len(elem) == 3:
            self.image = load_image(elem[1], 'images')
            self.rect = self.image.get_rect()
            self.rect = self.rect.move((int(elem[2].split()[0]), int(elem[2].split()[1])))
        elif len(elem) == 6:
            x, y = int(elem[3].split()[0]), int(elem[3].split()[1])
            sizex, sizey = int(elem[4].split()[0]), int(elem[4].split()[1])
            width = elem[-1]
            color = (int(elem[2].split()[0]), int(elem[2].split()[1]), int(elem[2].split()[2]))
            self.image = pygame.Surface([sizex, sizey])
            self.image.fill(color)
            self.rect = pygame.Rect(x, y, sizex, sizey)
        self.mask = pygame.mask.from_surface(self.image)
        

#Класс фона   
class Fon(pygame.sprite.Sprite):
    def __init__(self, elem, group):
        super().__init__(group)
        if len(elem) == 3:
            self.image = load_image(elem[1], 'images')
            self.rect = self.image.get_rect()
            self.rect = self.rect.move((int(elem[2].split()[0]), int(elem[2].split()[1])))
        elif len(elem) == 6:
            x, y = int(elem[3].split()[0]), int(elem[3].split()[1])
            sizex, sizey = int(elem[4].split()[0]), int(elem[4].split()[1])
            width = elem[-1]
            color = (int(elem[2].split()[0]), int(elem[2].split()[1]), int(elem[2].split()[2]))
            self.image = pygame.Surface([sizex, sizey])
            self.image.fill(color)           
            self.rect = pygame.Rect(x, y, sizex, sizey)
        self.mask = pygame.mask.from_surface(self.image)

#Класс для отображения картинок(уровни, кнопки и т.д.)
class Sprites(pygame.sprite.Sprite):
    def __init__(self, image, coords, catalog, position='1', *group):
        super().__init__(*group)
        self.name = image
        self.catalog = catalog
        if position == '1':
            self.image = load_image(self.name, catalog)
        else:
            self.image = load_image('block.jpg', catalog)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        
    def set_pos(self, position):
        if position == '1':
            self.image = load_image(self.name, self.catalog)
        else:
            self.image = load_image('block.jpg', self.catalog)