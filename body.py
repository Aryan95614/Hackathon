import pygame, os, sys
from pygame.sprite import Sprite
from b.constants import *
from pygame.mask import from_surface
from playsound import playsound
from os.path import join
from pygame.transform import scale

'''
Lambda Functions : [BASIC]
'''
load = lambda x: pygame.image.load(x).convert_alpha()
ranlen = lambda x: range(len(x))

'''
Temp assets and information
'''
laser_img = laserDesignated

'''
Normal Functions : [BASIC]
'''


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


'''
Classes : [BASIC] OOPS Implementation
'''


class general():
    def __init__(self, x, y, image, win):
        self.x = x
        self.y = y
        self.image = image
        self.win = win

    def render(self):
        self.win.blit(self.image, (self.x, self.y))


class Player(Sprite, general):
    COOLDOWN = 30

    def __init__(self, x, y, image, win):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (570, 244)
        self.current_frame = 0
        self.last_updated = 0
        self.vel = 0
        self.health = 100
        self.left_border, self.right_border = 250, 1150
        self.ground_y = 224
        self.box = pygame.Rect(self.rect.x, self.rect.y, self.rect.w * 2, self.rect.h)
        self.box.center = self.rect.center
        self.passed = False
        self.win = win
        self.rect.x = x
        self.rect.y = y
        self.ground_y = 336
        self.key_left, self.key_right, self.FACING_LEFT, self.attack = False, False, False, False
        general.__init__(self, self.rect.x, self.rect.y, self.image, self.win)
        self.box = pygame.Rect(self.rect.x, self.rect.y, self.rect.w * 2, self.rect.h)
        self.box.center = self.rect.center
        self.passed = False
        self.change = 1
        self.lasers = []
        self.laser_img = laser_img
        self.counter = 0
        self.mask = from_surface(self.image)

    def moves(self, obj, info):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.key_left = True
            self.key_right = False
            self.FACING_LEFT = True
            self.rect.x -= 2
            self.x -= 2
        if keys[pygame.K_d]:
            self.key_right = True
            self.key_left = False
            self.FACING_LEFT = True
            self.rect.x += 2
            self.x += 2
        if keys[pygame.K_SPACE]:
            self.key_right = False
            self.key_left = False
            self.FACING_LEFT = False
            playsound(join("Sounds", "Clash-Swords.wav"))
            if info:
                obj.health -= 30
                obj.x += 100

        self.move()

    def move(self):
        self.vel = 0
        if self.key_left:
            # self.rect.x -= 2
            self.vel = -2
        if self.key_right:
            # self.rect.x += 2
            self.vel = 2
        if self.vel == 0 and self.passed:
            self.passed = False
            self.box.center = self.rect.center
        if self.rect.x > 600 - self.rect.w:
            self.key_left = False
            self.rect.x = 599 - self.rect.w
        elif self.rect.x < 288:
            print("[LIMIT REACHED]")
            self.rect.x = 289
            self.key_right = False
        if self.rect.left > self.box.left and self.rect.right < self.box.right:
            pass
        else:
            self.passed = True
            if self.rect.left > self.box.left:
                self.box.left += self.vel
            elif self.rect.right < self.box.right:
                self.box.left += self.vel
        self.vel = 0

    def attack(self, obj):
        if self.collision(obj):
            obj.health -= 30

    def collision(self, obj):
        return collide(self, obj)


class Enemy(general, Sprite):
    change = 2

    def __init__(self, x, y, image, win):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.win = win
        self.health = 100
        self.obselete = False
        general.__init__(self, self.x, self.y, self.image, self.win)
        self.mask = from_surface(self.image)
        self.self = 0
        self.COUNTDOWN = 30
        self.rect = self.image.get_rect()
        enemies.append(self)
        sprites.add(enemies)

    def move(self, player, amount):
        x = player.rect.x / 5 - 50
        if x <= self.x:
            self.x -= 1

        elif player.x - self.x == 159:

            player.health -= 10
            print(f"Player Health: [{player.health}]")
        else:
            player.health -= 10
            self.x += 300
        self.y = player.rect.y - 200
        if self.x <= amount:
            player.health -= 10
            self.x += 100


class text():
    def __init__(self, win):
        self.font = pygame.font.SysFont('arial', 32)
        self.rect = [0, 0]
        self.win = win

    def display(self, Text):
        self.text = self.font.render(Text, True, blue, GREEN)
        self.win.blit(self.text, self.rect)

    def _display(self, Text, coordinates):
        self.text = self.font.render(Text, True, blue, GREEN)
        self.win.blit(self.text, coordinates)

    def _display_(self, Text, coordinates):
        self.text = self.font.render(Text, True, Gray)
        self.win.blit(self.text, coordinates)

    def __display__(self, Text, coordinates):
        self.fonts = pygame.font.SysFont('arial', 50)
        self.text = self.fonts.render(Text, True, Orange)
        self.win.blit(self.text, coordinates)


class Laser():
    def __init__(self, x, y, image, win):
        self.x = x
        self.y = y
        self.image = image
        self.win = win

    def render(self, lasers):
        self.coor = (self.x, self.y)
        self.win.blit(self.image, self.coor)
        self.y -= 1
        self.check(lasers)

    def check(self, lasers):
        if self.y < 800:
            lasers.remove(self)
            del self
