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
player = Rect((16.0, 192.0), (16, 16))
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
startPos = player.top
jumpDist = 0
jumpHeight = 25
running = 1
exitcode = 0

for num in range(0, 50):
        if(random.randint(0, 1) == 0):
            cloudlist.append([random.randint(0, 2), num * 60, 30 + random.randint(0, 100)])
        if(random.randint(0, 1) == 0):
            hillslist.append([random.randint(0, 4), num * 60, 224])
            if(hillslist[-1][0] == 0):
                hillslist[-1][2] -= 16
            elif hillslist[-1][0] != 1:
                hillslist[-1][2] += 2

class Goomba:
    def __init__(self, xlayer, ylayer):
        self.xlayer = xlayer
        self.layer = ylayer
        self.rect = Rect((xlayer * 16.0, 224 - ylayer*16.0), (16.0, 16.0))
        self.currSprite = 0
        self.vel = -.3
        self.spriteChange = 0
        self.deathCount = -1
    def move(self, layer, offset = 0):
        if(self.deathCount >= 0):
            if(self.deathCount > 0):
                self.deathCount -= 1
            return
        self.rect.left += self.vel
        for pos in layer.rectList:
            if(self.rect.colliderect(pos)):
                self.vel *= -1
                break
        self.spriteChange += 1
        if(self.spriteChange == 20):
            self.spriteChange = 0
            self.currSprite = abs(self.currSprite - 1)
    def die(self):
        self.currSprite = 2
        self.deathCount = 100
        self.rect.top += 8
    def display(self, offset = 0):
        if(self.deathCount != 0):
                screen.blit(goomsprites[self.currSprite], [self.rect.left - offset, self.rect.top])

goom1 = Goomba(15, 2)

class blockLayer:
    def __init__(self, xList, y, flip = False):
        self.ylayer = y
        self.yPos = 224 - self.ylayer*16
        self.rectList = []
        self.sprite = block
        if(self.ylayer < 2):
            self.sprite = ground
        if(not flip):
            for x in xList:
                self.rectList.append(Rect((x * 16, self.yPos), (16, 16)))
        else:
            for x in range(0, 40):
                self.rectList.append(Rect((x * 16, self.yPos), (16, 16)))
            for x in range(0, len(xList) - 1):
                del self.rectList[x]
    def display(self, offset):
        for x in self.rectList:
            screen.blit(self.sprite, [x.left - offset, self.yPos])
layers = []
xBlocks = [[-1], [-1], [7, 8, 9, 10, 11], [8, 9, 10], [9], [], [], [], []]
for num in range(0, 9):
    if(len(xBlocks[num]) == 0 or xBlocks[num][0] != -1):
        layers.append(blockLayer(xBlocks[num], num))
    else:
        layers.append(blockLayer(xBlocks[num][1:], num, True))

while running:
    screen.fill(0)
    for num in range(0, 9):
        for row in range(0, 8):
            screen.blit(sky, [num * 30, row * 30])
    for cloud in cloudlist:
        screen.blit(clouds[cloud[0]], [cloud[1] - movementOffset / 1.5, cloud[2]])
    for hill in hillslist:
        screen.blit(hills[hill[0]], [hill[1] - movementOffset, hill[2]])

    if(not marDead and marDown and goom1.deathCount < 0 and player.colliderect(goom1)):
        goom1.die()
        marDown = False
        marUp = True
        jumpDist = jumpHeight / 2
        playervel[1] = 1.5
    if(not marDead and goom1.deathCount < 0 and abs(goom1.rect.left - player.left) < 16 and goom1.rect.top - player.top < 16):
        marDead = True
        playervel[0] = 0
        playervel[1] = 0
    if(marDead):
        playersprite = marsprites[5]
        if(playervel[1] == 0):
             pygame.time.delay(500)
    marLayer = int((224 - player.top) / 16)
    screen.blit(playersprite, (player.left, player.top))
    
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
                playersprite = pygame.transform.flip(marsprites[1], True, False)
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

    for pos in layers[marLayer].rectList:
        if(abs(player.colliderect(pos))):
            if(player.left <= pos.left and playervel[0] > 0):
                playervel[0] = 0
                player.left = pos.left - 16
            elif(player.left > pos.left and playervel[0] < 0):
                playervel[0] = 0
                player.left = pos.left  + 16
    if(player.left >= 224 and playervel[0] > 0):
        movementOffset += playervel[0]
    elif(player.left < 0):
        player.left = 0
    else:
        player.left += playervel[0]
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

    if(not marDead and playerkeys[0]):
        if(not marUp and not marDown):
            marUp = True
            jumpDist = 0
            playervel[1] = 1.5
        if(marUp and abs(playervel[1]) <= .03):
            marUp = False
            marDown = True
    elif(marUp):
        marUp = False
        marDown = True
    if(marDead):
        if(not marUp and not marDown):
            marUp = True
            playervel[1] = 1.5
        if(marUp and jumpDist > jumpHeight):
            marUp = False
            marDown = True
    elif(playervel[1] > -2):
        playervel[1] -= .05
            

    player.top -= playervel[1]
    jumpDist += playervel[1]
    
    if (layers[marLayer - 1].yPos - player.top - 16 <= 1):
        for pos in layers[marLayer - 1].rectList:
            if(player.colliderect(pos)):
                onBlock = True
                player.top = 224 - marLayer * 16
                marDown = False
                playervel[1] = 0
                break
            else:
                onBlock = False
                marDown = True
    if(not onBlock):
        if(flipmar):
            playersprite = pygame.transform.flip(marsprites[4], True, False)
        else:
            playersprite = marsprites[4]
    pygame.time.delay(8)












    
        

