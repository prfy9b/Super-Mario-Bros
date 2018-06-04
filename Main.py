import math
import random
import pygame
import sys
from pygame.locals import *
from copy import deepcopy

pygame.init()
pygame.mixer.init()
width, height = 256, 240
screen = pygame.display.set_mode((width, height))
playerkeys = [False, False, False, False]
playerpos = [16.0, 192.0]
playervel = [0.0 ,0.0]
clouds = [pygame.image.load("sprites/42.png"), pygame.image.load("sprites/43.png"), pygame.image.load("sprites/72.png")]
hills = [pygame.image.load("sprites/44.png"), pygame.image.load("sprites/45.png"), pygame.image.load("sprites/73.png"), pygame.image.load("sprites/74.png"), pygame.image.load("sprites/75.png")]
marsprites = [pygame.image.load("sprites/17.png"), pygame.image.load("sprites/16.png"), pygame.image.load("sprites/15.png"), pygame.image.load("sprites/18.png"), pygame.image.load("sprites/19.png"), pygame.image.load("sprites/5.png")]
goomsprites = [pygame.image.load("sprites/53.png"), pygame.image.load("sprites/54.png"), pygame.image.load("sprites/55.png")]
ground = pygame.image.load("sprites/71.png")
block = pygame.image.load("sprites/62.png")
sky = pygame.image.load("sprites/41.png")
playersprite = marsprites[0]
cloudlist = []
hillslist = []
spritechange = 0
changestate = 0
movementOffset = 0.0
flipmar = False
marUp = False
marDown = False
onBlock = False
marDead = False
marLayer = 0
startPos = playerpos[1]
jumpDist = 0
jumpHeight = 25
running = 1
exitcode = 0

for num in range(0, 50):
        if(random.randint(0, 1) == 0):
            cloudlist.append([random.randint(0, 2), num * 60, 30 + random.randint(0, 100)])
        if(random.randint(0, 1) == 0):
            hillslist.append([random.randint(0, 4), num * 60, 192])
            if(hillslist[-1][0] == 0):
                hillslist[-1][2] -= 16
            elif hillslist[-1][0] != 1:
                hillslist[-1][2] += 2

class Goomba:
    def __init__(self, xblocks, ylayer):
        self.xblocks = xblocks
        self.xPos = xblocks * 16
        self.layer = ylayer
        self.yPos = 192 - ylayer * 16
        self.currSprite = 0
        self.vel = -.3
        self.spriteChange = 0
        self.deathCount = -1
    def move(self, layer, offset = 0):
        if(self.deathCount >= 0):
            if(self.deathCount > 0):
                self.deathCount -= 1
            return
        self.xPos += self.vel
        for pos in layer.xList:
            if(abs(self.xPos - pos) < 16):
                self.vel *= -1
                break
        self.spriteChange += 1
        if(self.spriteChange == 20):
            self.spriteChange = 0
            self.currSprite = abs(self.currSprite - 1)
    def die(self):
        self.currSprite = 2
        self.deathCount = 100
        self.yPos += 8
    def display(self, offset = 0):
        if(self.deathCount != 0):
                screen.blit(goomsprites[self.currSprite], [self.xPos - offset, self.yPos])

goom1 = Goomba(15, 0)

class blockLayer:
    def __init__(self, xList, y):
        self.ylayer = y
        self.yPos = 192 - self.ylayer*16
        self.xList = []
        for x in xList:
            self.xList.append(x * 16)
    def display(self, offset):
        for x in self.xList:
            screen.blit(block, [x - offset, self.yPos])
layers = []
xBlocks = [[7, 8, 9, 10, 11], [8, 9, 10], [9]]
for num in range(0, 3):
    layers.append(blockLayer(xBlocks[num], num))

while running:
    screen.fill(0)
    for num in range(0, 9):
        for row in range(0, 8):
            screen.blit(sky, [num * 30, row * 30])
    for cloud in cloudlist:
        screen.blit(clouds[cloud[0]], [cloud[1] - movementOffset / 1.5, cloud[2]])
    for hill in hillslist:
        screen.blit(hills[hill[0]], [hill[1] - movementOffset, hill[2]])
    for num in range(0, 200):
        screen.blit(ground, [num * 16 - movementOffset, 208])
        screen.blit(ground, [num * 16 - movementOffset, 224])

    if(not marDead and marDown and goom1.deathCount < 0 and goom1 and abs(goom1.xPos - movementOffset - playerpos[0]) < 16 and goom1.yPos - playerpos[1] < 16):
        goom1.die()
        marDown = False
        marUp = True
        jumpDist = jumpHeight / 2
        playervel[1] = 1.5
    if(not marDead and goom1.deathCount < 0 and abs(goom1.xPos - playerpos[0]) < 16 and goom1.yPos - playerpos[1] < 16):
        marDead = True
        playervel[0] = 0
        playervel[1] = 0
    if(marDead):
        playersprite = marsprites[5]
        if(playervel[1] == 0):
             pygame.time.delay(500)

    marLayer = int((playerpos[1] - 192) / 16)
    screen.blit(playersprite, playerpos)
    
    goom1.move(layers[goom1.layer], movementOffset)
    goom1.display(movementOffset)
    for layer in layers:
        layer.display(movementOffset)
    
    pygame.display.flip()

    for ev in pygame.event.get():
        if ev.type == KEYDOWN:
            if ev.key == K_w:
                playerkeys[0] = True
            elif ev.key == K_a:
                playerkeys[1] = True
            elif ev.key == K_s:
                playerkeys[2] = True
            elif ev.key == K_d:
                playerkeys[3] = True
                playersprite = marsprites[1]
                
        if ev.type == KEYUP:
            if ev.key == K_w:
                playerkeys[0] = False
            elif ev.key == K_a:
                playerkeys[1] = False
            elif ev.key == K_s:
                playerkeys[2] = False
            elif ev.key == K_d:
                playerkeys[3] = False
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    #Mario movement
    if(playerkeys[3] and not marDead):
        if(playervel[0] < 1):
            playervel[0] += .06
        flipmar = False
    elif(playerkeys[1] and not marDead):
        if(playervel[0] > -1):
            playervel[0] -= .06
        flipmar = True
    else:
        if(abs(playervel[0]) <= .02):
            playervel[0] = 0
        if(playervel[0] > 0):
            playervel[0] *= .95
        elif(playervel[0] < 0):
            playervel[0] *= .95
        else:
            if(flipmar):
                playersprite = pygame.transform.flip(marsprites[0], True, False)
            else:
                playersprite = marsprites[0]

    for pos in layers[marLayer].xList:
        if(abs(playerpos[0] - pos + movementOffset) < 16):
            if(playerpos[0] + 24 >= pos - movementOffset and playervel[0] > 0):
                playervel[0] = 0
                playerpos[0] = pos - movementOffset - 16
            if(playerpos[0] <= pos + 16 - movementOffset and playervel[0] < 0):
                playervel[0] = 0
                playerpos[0] = pos- movementOffset + 16
    if(playerpos[0] >= 192 and playervel[0] > 0):
        movementOffset += playervel[0]
    elif(playerpos[0] < 0):
        playerpos[0] = 0
    else:
        playerpos[0] += playervel[0]
    if(spritechange < 1):
        spritechange += abs(playervel[0]) / 5
    else:
        spritechange = 0
        if(changestate == 0):
            if(flipmar):
                playersprite = pygame.transform.flip(marsprites[2], True, False)
            else:
                playersprite = marsprites[2]
            changestate += 1
        elif(changestate == 1):
            if(flipmar):
                playersprite = pygame.transform.flip(marsprites[3], True, False)
            else:
                playersprite = marsprites[3]
            changestate += 1
        elif(changestate == 2):
            if(flipmar):
                playersprite = pygame.transform.flip(marsprites[2], True, False)
            else:
                playersprite = marsprites[2]
            changestate += 1
        elif(changestate == 3):
            if(flipmar):
                playersprite = pygame.transform.flip(marsprites[1], True, False)
            else:
                playersprite = marsprites[1]
            changestate = 0

    if(playerkeys[0] or marDead):
        if(not marUp and not marDown):
            marUp = True;
            playervel[1] = 1.5
        if(marUp and jumpDist > jumpHeight):
            marUp = False
            marDown = True
    else:
        if(marUp):
            marUp = False
            marDown = True
    if(not marDead and marDown and jumpDist > 0 and playervel[1] > -4):
        playervel[1] -= .07
    if(marDead):
        playervel[1] -= .03
    if(layers[max(marLayer - 1, 0)].yPos - playerpos[1] <= 2):
        for pos in layers[max(marLayer - 1, 0)].xList:
            if(abs(playerpos[0] - pos + movementOffset) <= 16):
                playerpos[1] = 192 - marLayer * 16
                marDown = False
                jumpDist = 0
                playervel[1] = 0
    if(not marDead and marDown and jumpDist <= 0):
        playerpos[1] = startPos
        marDown = False
        jumpDist = 0
        playervel[1] = 0
            

    playerpos[1] -= playervel[1]
    jumpDist += playervel[1]

    if(marUp or marDown):
        if(flipmar):
            playersprite = pygame.transform.flip(marsprites[4], True, False)
        else:
            playersprite = marsprites[4]
    pygame.time.delay(5)












    
        

