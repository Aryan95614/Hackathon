from HACKATHON.camera import *
from pygame.locals import *
from HACKATHON.body import *
from HACKATHON.constants import *
from playsound import playsound

import b.Sounds as sounds
from pygame.transform import scale, rotate
from os.path import join
from pygame.display import update
import pygame, os, sys
from pygame.transform import scale, rotate
from os.path import join

pygame.init()
canvas = pygame.Surface(SIZE)
win = pygame.display.set_mode(SIZE)
icon = scale(load(join("assets", "laugh.png")), CHARACTERSIZE)
pygame.display.set_icon(icon)
pygame.display.set_caption("The Two Eccentricites")


def killing(score):
    run = True
    gameover = False
    blit_canvas = True
    #######################

    SIZE = (800, 800)
    clock = Clock()
    sprites = Group()

    GREEN = (218, 247, 166)
    startingLocation = (0, 0)
    CHARACTERSIZE = (70, 70)
    HOUSESIZE = (128, 128)
    fps = 60
    normal = (0, 0)
    White = (255, 255, 255)
    enemies = list()
    lasers = list()
    checking = list()
    green = (0, 255, 0)
    Black = (0, 0, 0)
    blue = (0, 0, 128)
    Middle = (100, 450)
    Middle1 = (200, 550)
    Middle2 = (200, 650)
    Gray = (127, 0, 255)
    Top = (350, 200)
    Click = (400, 250)
    Orange = (255, 165, 0)

    playerDesignated = join("images", "knight.png")
    homeDesignated = join("images", "home.png")
    enemyDesignated = join("images", "enemy.png")
    laserDesignated = join("images", "laser.png")
    enemy2Designated = join("images", "enemy2.png")
    BackgroundDesignated = join("images", "Background.jpg")
    ShipDesignated = join("images", "rocket.png")
    bulletDesignated = join("images", "yellow.png")
    #######################

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
            if not self.obselete:
                x = player.rect.x / 5 - 50
                if x <= self.x:
                    self.x -= 1

                elif player.x - self.x == 159:

                    player.health -= 10
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

        def ___display___(self, Text, coordinates):
            self.fonts = pygame.font.SysFont('arial', 50)
            self.text = self.fonts.render(Text, True, GREEN)
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

    #########################
    if run:

        player_image = scale(load(join("images", "knight.png")), CHARACTERSIZE)
        home_image = scale(load(homeDesignated), HOUSESIZE)
        enemy_image = scale(load(enemyDesignated), CHARACTERSIZE)
        enemy2_image = scale(load(enemyDesignated), CHARACTERSIZE)
        Background_Image = scale(load(BackgroundDesignated), SIZE)
        distance = 1
        enemieskilled = 0

        Text = text(win=win)
        Healthbar = text(win=win)
        Title = text(win=win)
        Play = text(win=win)
        Rules = text(win=win)
        Rules1 = text(win=win)
        Rules2 = text(win=win)
        Needed = text(win=win)

        Example = Player(336, 336, player_image, canvas)
        enemy = Enemy(800, 136, enemy_image, canvas)
        camera = Camera(Example)
        follow = Follow(camera, Example)
        border = Border(camera, Example)
        auto = Auto(camera, Example)
        menu_allows = False
        other_game = True
        camera.setmethod(follow)
        s = text(win=win)

        while not gameover:

            if menu_allows:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                        sys.exit()
                if enemieskilled == score or Example.health <= 0:
                    enemy.obselete = True
                    blit_canvas = False
                    other_game = True
                win.fill(White)
                canvas.fill(GREEN)

                checking.append([Example.x, enemy.x])

                if len(checking) > 1:
                    checking.remove(checking[0])


                Example.moves(enemy, bool(checking[0][-1] - checking[0][0] <= 14 and checking[0][-1] - checking[0][0] >= -300))
                print(checking[0][-1] - checking[0][0])
                canvas.blit(home_image, (0 - int(camera.offset.x) + 200, 0 - int(camera.offset.y) + 200))
                canvas.blit(home_image, (0 - int(camera.offset.x) + 200, 0 - int(camera.offset.y) + 400))
                canvas.blit(home_image, (0 - int(camera.offset.x) + 72, 0 - int(camera.offset.y) + 200))
                canvas.blit(home_image, (0 - int(camera.offset.x) + 72, 0 - int(camera.offset.y) + 400))
                if enemy.health > 0:
                    canvas.blit(enemy.image,
                                (enemy.x - int(camera.offset.x) + 200, enemy.y - int(camera.offset.y) + 200))

                    enemy.move(Example, int(0 - int(camera.offset.x) - 90))
                else:

                    enemieskilled += 1
                    if enemieskilled < 2:
                        del enemy
                        enemy = Enemy(800, 136, enemy_image, canvas)

                clock.tick(fps)

                distance += 1
                x, y = pygame.mouse.get_pos()

                camera.scroll()

                canvas.blit(Example.image,
                            (int(Example.rect.x - camera.offset.x), int(Example.rect.y - camera.offset.y)))
                if blit_canvas:
                    win.blit(canvas, startingLocation)

                Text.display(f'Enemies killed = {enemieskilled}')
                Needed._display(f'Enemies needed to kill {score}', (0, 64))
                if Example.health > 0:
                    Text._display(f'Player Health = {Example.health}', [500, 0])
                s.___display___("Game finished, Thank you", (168, 600))
                pygame.display.update()

            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        menu_allows = True

                win.fill(White)
                win.blit(Background_Image, normal)
                Title.__display__('Kill the bandits', Top)
                Rules._display_('Rules:  ', Middle)
                Rules1._display_('\n 1. Kill by pressing space', Middle1)
                Rules2._display_('\n 2. do not let the bandit enter the area', Middle2)
                Play._display_('Click to play', Click)
                pygame.display.update()



