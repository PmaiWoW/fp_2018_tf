import pygame
import math
import sys
import random
from pygame.locals import *


pygame.init()

#------Setting up variables------#
end = False

x, y = 0, 0

playerX, playerY = 0, 384
playerWidth, playerHeight = 64, 64
shieldActive = False

enemyX, enemyY = 1210, 384
enemyWidth, enemyHeight = 64, 64

coffeeWidth, coffeeHeight = 32, 32
beanX, beanY = 970, 250


speed = 10
walkAnimCounter = 0
enemyAnimCounter = 0
leftAnim = False
rightAnim = True

DISPLAYWIDTH = 1280
DISPLAYHEIGHT = 832
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


#------Setting up the game display and other elements of it------#
gameDisplay = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
pygame.display.set_caption('FOR THE LOVE OF COFFEE, DODGE!')
clock = pygame.time.Clock()



#------Loading images------#
bgImg = pygame.image.load('./Assets/Art/bg.png')

winScreen = pygame.image.load('./Assets/Art/winScreen.png')

deathScreen = pygame.image.load('./Assets/Art/deathScreen.png')

firstScreen = pygame.image.load('Assets/Art/firstScreen.png')

playerIdleImg = pygame.image.load('./Assets/Art/CovfefeCrusader.png')

enemyImg = pygame.image.load('./Assets/Art/enemyAnim/enemyAnim1.png')

coffeeImg = pygame.image.load('./Assets/Art/coffeeBean.png')

shield = pygame.image.load('./Assets/Art/aoeAttack.png')

enemyImgs = [pygame.image.load('./Assets/Art/enemyAnim/enemyAnim1.png'),
            pygame.image.load('./Assets/Art/enemyAnim/enemyAnim2.png'),
            pygame.image.load('./Assets/Art/enemyAnim/enemyAnim3.png'),
            pygame.image.load('./Assets/Art/enemyAnim/enemyAnim4.png')]
            
rightWalkImgs = [pygame.image.load('./Assets/Art/walk/rightWalk1.png'),
                 pygame.image.load('./Assets/Art/walk/rightWalk2.png'),
                 pygame.image.load('./Assets/Art/walk/rightWalk3.png'),
                 pygame.image.load('./Assets/Art/walk/rightWalk4.png'),
                 pygame.image.load('./Assets/Art/walk/rightWalk5.png'),
                 pygame.image.load('./Assets/Art/walk/rightWalk6.png')]

leftWalkImgs =  [pygame.image.load('./Assets/Art/walk/leftWalk1.png'),
                 pygame.image.load('./Assets/Art/walk/leftWalk2.png'),
                 pygame.image.load('./Assets/Art/walk/leftWalk3.png'),
                 pygame.image.load('./Assets/Art/walk/leftWalk4.png'),
                 pygame.image.load('./Assets/Art/walk/leftWalk5.png'),
                 pygame.image.load('./Assets/Art/walk/leftWalk6.png')]



#------Defining functions------#
def redrawGameDisplay():
    gameDisplay.blit(bgImg, (x,y))


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

def terminate():
    pygame.quit()
    sys.exit()


    
#------Setting up classes------#
class Player:
    
    def __init__(self):
        self.x = playerX
        self.y = playerY
        self.width = playerWidth
        self.height = playerHeight
        self.death = False
        if leftAnim == True:
            self.currentImgRect = leftWalkImgs[walkAnimCounter].get_rect()
        elif rightAnim == True:
            self.currentImgRect = rightWalkImgs[walkAnimCounter].get_rect()
        else:
            self.currentImgRect = playerIdleImg.get_rect()
        
    def draw(self, x, y):
        global walkAnimCounter
        
        if(walkAnimCounter + 1 >= 6):
            walkAnimCounter = 0
        if(leftAnim == True):
            gameDisplay.blit(leftWalkImgs[walkAnimCounter], (self.x, self.y))
            walkAnimCounter += 1
        elif(rightAnim == True):
            gameDisplay.blit(rightWalkImgs[walkAnimCounter], (self.x, self.y))
            walkAnimCounter += 1
        else:
            gameDisplay.blit(playerIdleImg, (self.x, self.y))


    def shieldDraw(self, x, y):
        gameDisplay.blit(shield, (self.x, self.y))
        
    def is_collided_with(self, enemy):
        return self.currentImgRect.colliderect(enemy)

    def is_collided_with(self, bean):
        return self.currentImgRect.colliderect(bean)

    def kill(self):
        self.death = True

        
class Enemy:
    
    def __init__(self):
        self.x = enemyX
        self.y = enemyY
        self.width = enemyWidth
        self.height = enemyHeight
        self.death = False
        self.currentImgRect = enemyImgs[enemyAnimCounter].get_rect()

    def draw(self, enemyX, enemyY):
        global enemyAnimCounter
        
        if(enemyAnimCounter >= 4):
            enemyAnimCounter = 0
            
        gameDisplay.blit(enemyImgs[enemyAnimCounter], (self.x, self.y))
        enemyAnimCounter += 1
        
    def kill(self):
        self.death = True


class CoffeeBean:
    
    def __init__(self):
        self.x = beanX
        self.y = beanY
        self.width = coffeeWidth
        self.height = coffeeHeight
        self.rect = coffeeImg.get_rect()
        self.pickup = False

    def draw(self, beanX, beanY):
        gameDisplay.blit(coffeeImg, (self.x,self.y))



#------Begin game------#

player = Player()
enemy = Enemy()
bean = CoffeeBean()


gameDisplay.blit(firstScreen, (0, 0))
pygame.display.update()
waitForPlayerToPressKey()


while not end:
            
    
    if player.is_collided_with(enemy.currentImgRect):
        
        if enemy.x - 50 < player.x < enemy.x + 50 and enemy.y - 50 < player.y < enemy.y + 50:
            if(shieldActive == False):
                player.kill()
                gameDisplay.blit(deathScreen, (0, 0))
                pygame.display.update()
                waitForPlayerToPressKey()
                terminate()
            elif(shieldActive == True):
                enemy.kill()
                enemy.x = -100
                enemy.y = -100
 
    if player.is_collided_with(bean.rect):
        if bean.x - 32 < player.x < bean.x + 32 and bean.y - 32 < player.y < bean.y + 32:
            bean.pickup = True
            gameDisplay.blit(winScreen, (0, 0))
            pygame.display.update()
            waitForPlayerToPressKey()
            terminate()


    shieldActive = False
    redrawGameDisplay()
    
    
    if player.death == False:
        player.draw(player.x, player.y)
        
    if enemy.death == False:
        enemy.draw(enemy.x, enemy.y)
        
    if bean.pickup == False and enemy.death == True:
        bean.draw(bean.x, bean.y)

    for event in pygame.event.get():
            
        if event.type == pygame.QUIT:
            terminate()
    
    
    #------movement------
    controls = pygame.key.get_pressed()
    
    if player.death == False:
        if controls[pygame.K_w] and player.y > speed:
            player.y -= speed
            
        elif controls[pygame.K_a] and player.x > speed:
            player.x -= speed
            leftAnim = True
            rightAnim = False
            
        elif controls[pygame.K_s] and player.y < DISPLAYHEIGHT - player.height:
            player.y += speed
            
        elif controls[pygame.K_d] and player.x < DISPLAYWIDTH - player.width:
            player.x += speed
            leftAnim = False
            rightAnim = True
            
        else:
            rightAnim = False
            leftAnim = False
            walkAnimCounter = 0

        if(controls[pygame.K_q] and controls[pygame.K_w]):
            player.shieldDraw(player.x, player.y - 10)
            shieldActive = True
           
        elif(controls[pygame.K_q] and controls[pygame.K_a]):
            player.shieldDraw(player.x - 10, player.y)
            shieldActive = True
           
        elif(controls[pygame.K_q] and controls[pygame.K_s]):
            player.shieldDraw(player.x, player.y + 10)
            shieldActive = True

        elif(controls[pygame.K_q] and controls[pygame.K_d]):
            player.shieldDraw(player.x + 10, player.y)
            shieldActive = True
            

            
    
    pygame.display.update()
    clock.tick(60)


pygame.quit()
