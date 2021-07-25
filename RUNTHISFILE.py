import sys, math
from os.path import join
import pygame
from pygame.transform import scale, rotate
from random import randint
from pygame.time import Clock
from HACKATHON.main import killing


pygame.init()
SIZE = (800, 800)
CHARACTERSIZE = (64, 64)
White = (255, 255, 255)

win = pygame.display.set_mode(SIZE)

load = lambda x: pygame.image.load(x).convert_alpha()
background = scale(load(join("assets", "Background.jpg")), SIZE)

ranlen = lambda x: range(len(x))
icon = scale(load(join("assets", "laugh.png")), CHARACTERSIZE)
pygame.display.set_icon(icon)
pygame.display.set_caption("The Two Eccentricites")

class spaceship():
    bullet_State = "ready"

    def __init__(self, x, y, image, win):
        self.x = x
        self.y = y
        self.image = image
        self.bulletimg = scale(load(join("assets", "yellow.png")), CHARACTERSIZE)
        self.win = win
        self.lasers = []

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x != 10:
            self.x -= 3
        if keys[pygame.K_d] and self.x != 736:
            self.x += 3
        if keys[pygame.K_SPACE] and self.bullet_State == "ready":
            self.bullet_State = "Fire"

    def draw(self):
        self.coor = (self.x, self.y)
        self.win.blit(self.image, self.coor)
        self.move()


playerImg = scale(load(join("assets", "rocket.png")), CHARACTERSIZE)

Spaceship = spaceship(368, 700, playerImg, win)

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyNumbers = 6

for i in range(enemyNumbers):
    enemyImg.append(rotate(scale(load(join("assets", "enemy3.png")), CHARACTERSIZE), 180))
    enemyX.append(randint(0, 736))
    enemyY.append(randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletImg = scale(load(join("assets", "yellow.png")), (60, 120))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0

textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

Background = scale(load(join("assets", "bbackground.jpg")), SIZE)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    s_text = over_font.render(f"You killed: {score_value}", True, (255, 255, 255))
    win.blit(over_text, (200, 250))
    win.blit(s_text, (200, 400))


def player(x, y):
    win.blit(playerImg, (x, y))


def enemy(x, y, i):
    win.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bulletImg, (x + 16, y + 10))


def collides(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


gameover = False
clock = Clock()
run = False
Orange = (255, 165, 0)
Gray = (127, 0, 255)
GREEN = (0, 255, 0)
Black = (0, 0, 0)
blue = (0, 0, 128)


class text():
    def __init__(self, win):
        self.font = pygame.font.SysFont('arial', 32)
        self.rect = [0, 0]
        self.win = win

    def display(self, Text):
        self.text = self.font.render(Text, True, blue, GREEN)
        self.win.blit(self.text, self.rect)

    def _display(self, Text, coordinates):
        self.font = pygame.font.SysFont('arial', 32)
        self.text = self.font.render(Text, True, White)
        self.win.blit(self.text, coordinates)

    def _display_(self, Text, coordinates):
        self.text = self.font.render(Text, True, Gray)
        self.win.blit(self.text, coordinates)

    def __display__(self, Text, coordinates):
        self.fonts = pygame.font.SysFont('arial', 50)
        self.text = self.fonts.render(Text, True, Orange)
        self.win.blit(self.text, coordinates)

menuallows = False
Text = text(win=win)
Healthbar = text(win=win)
Title = text(win=win)
Play = text(win=win)
Rules = text(win=win)
Rules1 = text(win=win)
Rules2 = text(win=win)

while not gameover:
    if menuallows:
        win.fill(White)
        win.blit(background, (0, 0))
        Spaceship.draw()
        clock.tick(60)
        pygame.draw.rect(win, White, (0, 350, 800, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = Spaceship.x
                        fire_bullet(bulletX, bulletY)

        for i in range(enemyNumbers):

            if enemyY[i] > 350:
                for j in range(enemyNumbers):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = collides(enemyX[i], enemyY[i], bulletX, bulletY)
            enemy(enemyX[i], enemyY[i], i)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = randint(0, 736)
                enemyY[i] = randint(50, 150)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(Spaceship.x, Spaceship.y)

        pygame.display.update()

    else:
        win.fill(White)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.MOUSEBUTTONUP:
                menuallows = True
        win.blit(Background, (0, 0))

        Text.__display__("Kill all Aliens!", (0, 0))
        Play._display("Click to play", (0, 100))
        Rules._display("Rules", (500, 500))
        Rules1._display("Kill the Aliens", (500, 600))
        Rules2._display("or they will nuke", (500, 700))
        pygame.display.update()

killing(score_value)