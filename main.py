from sys import*
import pygame
import random
import math
from pygame.locals import *

##########################################  Code From Here  ####################################################################################################
##########################################  Setting up the basics and display ####################################################################################################

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DISPLAY = pygame.display.set_mode((800,600))
DISPLAY.fill(BLACK)
pygame.display.set_caption("Shameless Space Invaders Copy")
gameIcon = pygame.image.load("Sprites/yellow.png")
pygame.display.set_icon(gameIcon)

score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

##########################################  Objects and defs ####################################################################################################
#as class
class Bullet():
    def __init__(self) :
        bulletImage = pygame.image.load('Sprites/bullet.png')
        bullet_X = 0
        bullet_Y = 500
        bullet_Xchange = 0
        bullet_Ychange = 5
        bullet_state = "rest"

#as regular variables
bulletImage = pygame.image.load('Sprites/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 5
bullet_state = "rest"

def draw(self,win):
    pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

playerImage = pygame.image.load('Sprites/player.png')
player_X = 370
player_Y = 523
player_Xchange = 0

enemyImage = []
enemy_X = []
enemy_Y = []
enemy_Xchange = []
enemy_Ychange = []
no_of_enemys = 8
for num in range(no_of_enemys):
    enemyImage.append(pygame.image.load('Sprites/yellow.png'))
    enemy_X.append(random.randint(64, 737))
    enemy_Y.append(random.randint(30, 180))
    enemy_Xchange.append(1.2)
    enemy_Ychange.append(50)
        

def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255,255,255))
    DISPLAY.blit(score, (x , y ))

def player(x, y):
    DISPLAY.blit(playerImage, (x - 16, y + 10))

def enemy(x, y, i):
    DISPLAY.blit(enemyImage[i], (x, y))
    
def bullet(x, y):
    global bullet_state
    DISPLAY.blit(bulletImage, (x, y))
    bullet_state = "fire"

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    DISPLAY.blit(game_over_text, (190, 250))
    
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
    if distance <= 50:
        return True
    else:
        return False

##########################################  Game loop ####################################################################################################

running = True
while running:
    DISPLAY.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -2
            if event.key == pygame.K_RIGHT:
                player_Xchange = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    #moving
    player_X += player_Xchange
    for i in range(no_of_enemys):
        enemy_X[i] += enemy_Xchange[i]

    # bullet moving
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state == "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    # enemy moving
    for i in range(no_of_enemys):
        
        if enemy_Y[i] >= 450:
            if abs(player_X-enemy_X[i]) < 80:
                for j in range(no_of_enemys):
                    enemy_Y[j] = 2000
                game_over()
                break

        if enemy_X[i] >= 735 or enemy_X[i] <= 0:
            enemy_Xchange[i] *= -1
            enemy_Y[i] += enemy_Ychange[i]
        # Collision
        collision = isCollision(bullet_X, enemy_X[i], bullet_Y, enemy_Y[i])
        if collision:
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            enemy_X[i] = random.randint(64, 736)
            enemy_Y[i] = random.randint(30, 200)
            enemy_Xchange[i] *= -1

        enemy(enemy_X[i], enemy_Y[i], i)



    # boundaries
    if player_X <= 16:
        player_X = 16
    elif player_X >= 800:
        player_X = 800

            

    player(player_X, player_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()
    FramePerSec.tick(FPS)