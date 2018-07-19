import pygame,os,sys,math,random
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2

pygame.init()
#==================游戏实体======================
class GameObject(object):
    def __init__(self):
        self.x=None
        self.y=None
        self.width=40
        self.height=40
        self.isAlive=True
        self.sprite=None

    def setImage(self,imgPath):
        self.sprite=pygame.image.load(imgPath)
        # self.width,self.height=self.sprite.get_size()

    def update(self):
        pass

    def display(self):
        surface.blit(self.sprite, (self.x, self.y))

    #用于检测在此方块上的碰撞
    def isCrash(self,other,re_flag):
        if self.x < other.x + other.width-10 \
                and self.x + self.width > other.x +10 \
                and self.y < other.y + other.height-10  \
                and self.y + self.height > other.y+10 :
            if re_flag:
                if self.direction==1:
                    self.y = other.y + other.height-10
                elif self.direction==2:
                    self.x = other.x + 10- self.width
                elif self.direction==3:
                    self.y  = other.y + 10-self.height
                elif self.direction==4:
                    self.x = other.x + other.width - 10
            return True
        return False

    def __str__(self):
        return "坐标(%d,%d),名称%s"%(self.x,self.y,self)

#========================地图类========================
class Block(GameObject):
    def __init__(self,x,y,type):
        super().__init__()
        self.x=x
        self.y=y
        self.sprite=wallSprite[type-1]
        self.type=type
        self.width,self.height=self.sprite.get_size()
        self.boom_index = 0
        self.boom_img = []
        self.boom_img.append(pygame.image.load("../resources/img/bomb_11.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_12.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_13.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_14.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_15.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_16.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_17.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_18.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_19.png"))
        self.boom_img.append(pygame.image.load("../resources/img/bomb_20.png"))
        if self.type == 7 or self.type==12:
            self.life=4
        elif self.type==2:
            self.life=1
        else:
            self.life=10000

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        pass

    def hurt(self,other):
        self.life-=other.damage
        if self.life<=0:
            self.isAlive=False

    def setImage(self,sprite):
        self.sprite=sprite
        self.width=sprite

    #在surface上绘制
    def display(self):
        if self.type == 0:
            return
        surface.blit(self.sprite,(self.x,self.y))

    def update(self):
        if self.isAlive:
            if self.type==7 or self.type==12:
                self.sprite = pygame.image.load("../resources/img/wall_7_%d.png" % (5-self.life)).convert_alpha()
        elif self.isAlive == False:
            if self.boom_index >= len(self.boom_img):
                if random.randint(0,1) == 0:
                    if random.randint(0,1) == 0:
                        hpPackages.append(HpPackage(self.x,self.y))
                    else:
                        superBulletPackages.append(SuperBulletPackage(self.x, self.y))
                mapList.remove(self)
                self.isAlive = False
                self.boom_index = len(self.boom_img) - 1
            self.sprite = self.boom_img[self.boom_index]
            #print(game_count)
            if gameCount % 6 == 0:
                self.boom_index += 1

    def __str__(self):
        return "坐标(%d,%d),地图%d"%(self.x,self.y,self.type)

# =====================玩家类=============================
class Player(GameObject):
    def __init__(self,x,y):
        super().__init__()
        super().setImage("../resources/img/tank_1.png")
        self.x=x
        self.y=y
        #self.direction=Vector2(0,-1)
        self.direction = 1      #坦克朝向 1上2右3下4左
        self.needMove=False
        self.speed=100
        self.life=5
        # self.superBulletNum=2
        self.lifeFrame = pygame.image.load("../resources/img/blood.png")    #血条

    def fire(self):
        if len(playerBullets) < 2:
            bullet = Bullet(self.x,self.y,self.width,self.height,self.direction)
            playerBullets.append(bullet)


    def fire1(self):
        global superBulletNum
        if superBulletNum>0:
            superBulletNum -= 1
            superBullet = SuperBullet(self.x, self.y, self.width, self.height, self.direction)
            playerSuperBullets.append(superBullet)

    def hurt(self,bullet):
        global isGameOver
        if winTheGame or gameCount < 120:
            self.life -= 0
        else:
            self.life -= bullet.damage
            if self.life <= 0:
                self.isAlive = False
                isGameOver = True

    def move(self):
        pass

    def isCrash(self,other):
        if super().isCrash(other,True) and other.isAlive:
            return self.direction
        return 0

    def update(self):
        if self.isAlive:
            moveDir=Vector2(0,0)    #移动方向
            if pressedKey[K_a]:
                moveDir.x = -1
                if self.direction == 1 :
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)

                self.direction = 4
                self.needMove=True
            elif pressedKey[K_d]:
                moveDir.x = 1
                if self.direction == 1 :
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 4:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)

                self.direction=2
                self.needMove = True
            elif pressedKey[K_w]:
                moveDir.y = -1
                if self.direction == 4 :
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)

                self.direction=1
                self.needMove = True
            elif pressedKey[K_s]:
                moveDir.y = 1
                if self.direction == 1 :
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 4:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)

                self.direction=3
                self.needMove = True
            # else:
            #     self.x=0
            #     self.y=0
            #     self.needMove=False
            moveDir.normalise()     #向量规格化
            self.x += moveDir.x * self.speed * timePassedSecond
            self.y += moveDir.y * self.speed * timePassedSecond
            borderLimit(self)

    def changWeapon(self):
        pass

    def display(self):
        if self.life > 0:
            if gameCount<=120 and gameCount%10>=5:
                pass
            else:
                surface.blit(self.lifeFrame, (self.x, self.y - 5))
                pygame.draw.rect(surface, (253, 240, 1),
                                 (self.x - self.width + 39.8, self.y - self.height + 35,
                                  1140 * self.life / 140, 5))
                surface.blit(self.sprite,(self.x,self.y))



#==========================炮台============================
class Battery(GameObject):
    def __init__(self,x,y,level):
        super().__init__()
        self.level=level
        self.direction = 1
        self.isAlive=True
        self.life=18+3*self.level
        self.sprite=pygame.image.load("../resources/img/turret.png")   #装载炮台图片
        self.x=x
        self.y=y
        self.lifeFrame = pygame.image.load("../resources/img/blood.png")  # 血条
        self.boom_index = 0
        self.boom_img = []
        i=1
        while i<=64:
            self.boom_img.append(pygame.image.load("../resources/img/bossBomb__%d.png"%i))
            i+=1
        surface.blit(self.lifeFrame, (self.x, self.y - 5))
    def update(self):
        global winTheGame,gameMode
        if self.isAlive:
            pass
        else:
            if self.boom_index >= len(self.boom_img):

                self.isAlive = False
                bat.remove(self)
                gameMode = False
                winTheGame=True# 遊戲勝利
                self.boom_index = len(self.boom_img) - 1
            self.sprite = self.boom_img[self.boom_index]
            # print(game_count)
            if gameCount % 1 == 0:
                self.boom_index += 1
        #self.bat = pygame.image.load("../resources/img/tank_1.png")
    def display(self):
        if self.life > 0:
            pygame.draw.rect(surface, (255, 0, 0),
                             (self.x - self.width + 39.8, self.y - self.height + 35,
                              285 * self.life / 140, 5))
            surface.blit(self.sprite, (self.x, self.y))
        else:
            surface.blit(self.sprite, (440, 120))
    def fire(self):
        batteryDir=Vector2(player.x-self.x,player.y-self.y)

        missile = Missile(self.x, self.y, self.width, self.height, self.direction,batteryDir)
        batBullets.append(missile)
        # for missile in batBullets:
        #
        #     missile.update()
    def hurt(self,other):
        self.life-=other.damage
        if self.life<=0:
            self.isAlive=False

#=============================道具包基类==========================
class SupPackage(GameObject):
    def __init__(self,x,y):
        super().__init__()
        self.x=x
        self.y=y
    def isCrash(self):
        pass
    def update(self):
        pass
    def display(self):
        surface.blit(self.sprite, (self.x, self.y))
    def useIt(self,other):
        pass

#===============================血包==========================
class HpPackage(SupPackage):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.cureHP=2
        self.sprite=pygame.image.load("../resources/img/hpPackage.png")
    def update(self):
        pass
    def useIt(self,other):
        other.life+=self.cureHP
    def display(self):
        surface.blit(self.sprite, (self.x, self.y))

#===============================榴弹包==========================
class SuperBulletPackage(SupPackage):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.addSBNum=1
        self.sprite = pygame.image.load("../resources/img/superBulletNum.png")
    def update(self):
        pass

    def useIt(self):
        global superBulletNum
        superBulletNum += self.addSBNum
    def display(self):
        surface.blit(self.sprite, (self.x, self.y))


class Bullet(GameObject):
    def __init__(self,x,y,width,height,direction):
        super().__init__()
        self.direction = direction
        # self.damage = random.randint(5,10)
        self.damage = 1
        self.setImage("../resources/img/bullet_2.png")
        if(direction == 1):
            self.sprite = pygame.transform.rotate(self.sprite, 90.)
            self.xSpeed = 0
            self.ySpeed = -5
            self.x = x + width/2 - self.width/2
            self.y = y - self.height + 25
        elif(direction == 2):
            # self.sprite = pygame.transform.rotate(self.sprite, 90.)
            self.xSpeed = 5
            self.ySpeed = 0
            self.x = x + width - 25
            self.y = y + height/2 - self.height/2
        elif(direction == 3):
            self.sprite = pygame.transform.rotate(self.sprite, -90.)
            self.xSpeed = 0
            self.ySpeed = 5
            self.x = x + width/2 - self.width/2
            self.y = y + height - 25
        elif(direction == 4):
            self.sprite = pygame.transform.rotate(self.sprite, 180.)
            self.xSpeed = -5
            self.ySpeed = 0
            self.x = x - self.width + 25
            self.y = y + height/2 -self.height/2

    def isCrash(self,other):
        if self.x < other.x + other.width-15 \
                and self.x + self.width > other.x +15 \
                and self.y < other.y + other.height-15  \
                and self.y + self.height > other.y+15 :
            return True
        return False

    def update(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.x > surface_WIDTH or self.x + self.width < 0 or \
            self.y > surface_HEIGHT or self.y + surface_HEIGHT < 0:
            self.isAlive = False
    def display(self):
        surface.blit(self.sprite,(self.x, self.y))

#=========================导弹类=====================
class Missile(Bullet):
    def __init__(self, x, y, width, height, direction,battaryDir):
        self.direction = direction
        self.isAlive = True
        self.damage = 1
        self.width=40
        self.height=40
        self.xSpeed = 3
        self.ySpeed = 3
        self.speed=40
        self.x = x + width / 2 - self.width / 2
        self.y = y - self.height + 25
        self.mis = pygame.image.load("../resources/img/blue.png")
        self.flyDir=battaryDir.normalise()
    def update(self):
        self.x += self.flyDir.x*self.xSpeed
        self.y += self.flyDir.y*self.ySpeed

        if self.x > surface_WIDTH or self.x + self.width < 0 or \
                self.y > surface_HEIGHT or self.y + surface_HEIGHT < 0:
            self.isAlive = False
    def display(self):
        surface.blit(self.mis, (self.x, self.y))

#========================敌人类=====================
class Enemy(GameObject):
    def __init__(self,x,y,level):
        super().__init__()
        super().setImage("../resources/img/tank_2.png")
        self.level=level
        self.x = x
        self.y = y
        # self.direction=Vector2(0,-1)
        self.direction = 1  # 坦克朝向 1上2右3下4左
        self.needMove = False
        self.speed = 40+10*self.level
        self.life = 4+self.level
        self.patrolPath=[]
        self.lifeFrame = pygame.image.load("../resources/img/blood.png")
        self.randomDir = 1
        self.moveAble = True
        self.boom_index = 0
        self.boom_img = []
        for i in range(11,21):
            self.boom_img.append(pygame.image.load("../resources/img/bomb_"+str(i)+".png"))

    def hurt(self,bullet):
        self.life -= bullet.damage
        if self.life <= 0:
            #to do socre
            global score
            score+=10
            self.isAlive = False

    def fire(self):
        bullet = Bullet(self.x,self.y,self.width,self.height,self.direction)
        enemyBullets.append(bullet)

    def move(self):
        pass

    def update(self):
        global enemies
        if self.isAlive:
            moveDir = Vector2(0, 0) #移动方向
            # randomDir = random.randint(1, 4)
            # randomDir = 1
            if gameCount % 30 == 0:
                self.fire()
            if gameCount % 30 == 0:
                self.randomDir = random.randint(1,4)
            if self.randomDir == 4:
                moveDir.x = -1
                if self.direction == 1:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)

                self.direction = 4
                self.needMove=True
            elif self.randomDir == 2:
                moveDir.x = 1
                if self.direction == 1 :
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 4:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)

                self.direction=2
                self.needMove = True
            elif self.randomDir == 1:
                moveDir.y = -1
                if self.direction == 4 :
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)
                elif self.direction == 3:
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)

                self.direction=1
                self.needMove = True
            elif self.randomDir == 3:
                moveDir.y = 1
                if self.direction == 1 :
                    self.sprite = pygame.transform.rotate(self.sprite, 180.)
                elif self.direction == 2:
                    self.sprite = pygame.transform.rotate(self.sprite, -90.)
                elif self.direction == 4:
                    self.sprite = pygame.transform.rotate(self.sprite, 90.)

                self.direction=3
                self.needMove = True
            # else:
            #     self.x=0
            #     self.y=0
            #     self.needMove=False
            moveDir.normalise()     #向量规格化
            # if self.moveAble:
            self.x += moveDir.x * self.speed * timePassedSecond
            self.y += moveDir.y * self.speed * timePassedSecond
            if self.moveAble==False:
                if gameCount%30 ==0:
                    self.moveAble=True
                    self.speed=50


            # else:
            #     moveDir.x = -moveDir.x
            #     moveDir.y = -moveDir.y
            #     self.x += moveDir.x * self.speed * timePassedSecond
            #     self.y += moveDir.y * self.speed * timePassedSecond
            #     # if gameCount%40==0:
            #     self.moveAble = True

            borderLimit(self)
        else:
            if self.boom_index >= len(self.boom_img):
                enemies.remove(self)
                self.isAlive = False
                self.boom_index = len(self.boom_img) - 1
            self.sprite = self.boom_img[self.boom_index]
            # print(game_count)
            if gameCount % 6 == 0:
                self.boom_index += 1

    def display(self):
        if self.life > 0:
            surface.blit(self.lifeFrame, (self.x, self.y - 5))
            pygame.draw.rect(surface, (255, 0, 0),
                             (self.x - self.width + 39.8, self.y - self.height + 35,
                              1140 * self.life / 140, 5))
        surface.blit(self.sprite,(self.x,self.y))

    def isCrash(self,other):
        if super().isCrash(other,True) and other.isAlive:
        # if super().isCrash(other, False) and other.isAlive:
            if other==player:
                self.speed=0
                self.moveAble = False
            # self.speed = -self.speed

            return self.direction
        return 0

class SuperBullet(Bullet):
    def __init__(self,x,y,width,height,direction):
        super().__init__(x,y,width,height,direction)
        self.damage = 1
        self.setImage("../resources/img/superBullet.png")
        self.boom_index = 0
        self.boom_img = []
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_1.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_2.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_3.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_4.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_5.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_6.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_7.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_8.png"))
        self.boom_img.append(pygame.image.load("../resources/img/superBullet_9.png"))
        if (direction == 1):
            # self.setImage("../resources/img/super_bullet_1.png")
            # self.sprite = pygame.transform.rotate(self.sprite, 90.)
            self.xSpeed = -100
            self.ySpeed = -160
            self.g=200
            self.x = x + width / 2 - self.width / 2
            self.y = y - self.height + 25
        elif (direction == 2):
            # self.setImage("../resources/img/super_bullet_2.png")
            self.sprite = pygame.transform.rotate(self.sprite, -90.)
            self.xSpeed = 160
            self.ySpeed = -100
            self.g = 200
            self.x = x + width - 25
            self.y = y + height / 2 - self.height / 2
        elif (direction == 3):
            # self.setImage("../resources/img/super_bullet_3.png")
            self.sprite = pygame.transform.rotate(self.sprite, 180.)
            self.xSpeed = 100
            self.ySpeed = 160
            self.g=-200
            self.x = x + width / 2 - self.width / 2
            self.y = y + height - 25
        elif (direction == 4):
            # self.setImage("../resources/img/super_bullet_4.png")
            self.sprite = pygame.transform.rotate(self.sprite, 90.)
            self.xSpeed = -160
            self.ySpeed = -100
            self.g=200
            self.x = x - self.width + 25
            self.y = y + height / 2 - self.height / 2

    def update(self):
        if self.isAlive:
            if (self.direction == 1):
                self.xSpeed+=self.g*timePassedSecond
                self.x+=self.xSpeed*timePassedSecond
                self.y+=self.ySpeed*timePassedSecond
                if self.x > surface_WIDTH or self.x + self.width < 0 or \
                    self.y > surface_HEIGHT or self.y + surface_HEIGHT < 0 or \
                        self.xSpeed>=100:
                    self.isAlive = False
            if (self.direction == 2):
                self.ySpeed += self.g * timePassedSecond
                self.x += self.xSpeed * timePassedSecond
                self.y += self.ySpeed * timePassedSecond
                if self.x > surface_WIDTH or self.x + self.width < 0 or \
                        self.y > surface_HEIGHT or self.y + surface_HEIGHT < 0 or \
                        self.ySpeed >= 100:
                    self.isAlive = False
            if (self.direction == 3):
                self.xSpeed+=self.g*timePassedSecond
                self.x+=self.xSpeed*timePassedSecond
                self.y+=self.ySpeed*timePassedSecond
                if self.x > surface_WIDTH or self.x + self.width < 0 or \
                    self.y > surface_HEIGHT or self.y + surface_HEIGHT < 0 or \
                        self.xSpeed<=-100:
                    self.isAlive = False
            if (self.direction == 4):
                self.ySpeed += self.g * timePassedSecond
                self.x += self.xSpeed * timePassedSecond
                self.y += self.ySpeed * timePassedSecond
                if self.x > surface_WIDTH or self.x + self.width < 0 or \
                        self.y > surface_HEIGHT or self.y + surface_HEIGHT < 0 or \
                        self.ySpeed >= 100:
                    self.isAlive = False
        else:
            if self.boom_index >= len(self.boom_img):
                playerSuperBullets.remove(self)
                self.isAlive = False
                self.boom_index = len(self.boom_img) - 1
            self.sprite = self.boom_img[self.boom_index]
            # print(game_count)
            if gameCount % 6 == 0:
                self.boom_index += 1
    def display(self):
        if self.isAlive:
            surface.blit(self.sprite,(self.x, self.y))
        else:
            surface.blit(self.sprite, (self.x-20, self.y-20))
# =====================白云类=============================
class Cloud(GameObject):
    def __init__(self):
        super().__init__()
        if random.randint(0, 1) == 0:
            self.x_speed =random.randint(8,10)
        else:
            self.x_speed = -random.randint(5,8)
        self.y_speed =random.randint(8,10)
        self.x = random.randint(0, surface_WIDTH)
        self.y = -10

    def move(self):
        if gameCount % 200 == 0:
            if random.randint(0, 3) == 0:
                self.x_speed = -random.randint(5,8)
            else:
                self.x_speed = random.randint(8,10)
            if random.randint(0, 6) == 0:
                self.y_speed =-random.randint(5,8)
            else:
                self.y_speed =random.randint(8,10)
        self.x += self.x_speed*timePassedSecond
        self.y += self.y_speed*timePassedSecond
        if self.y > surface_HEIGHT:
            self.isAlive = False
        if self.x - self.width < 0 or self.x>surface_WIDTH:
            self.isAlive = False

    def move1(self,other):
        if other.x_speed > 0:
            self.x_speed = other.x_speed - 2
        else:
            self.x_speed = other.x_speed + 2
        if other.y_speed > 0:
            self.y_speed = other.y_speed - 2
        else:
            self.y_speed = other.y_speed + 2
        self.x += self.x_speed * timePassedSecond
        self.y += self.y_speed * timePassedSecond
        if not other.isAlive:
            self.isAlive = False


    def update(self):
        if self.isAlive:
            self.move()
    def update1(self,other):
        if self.isAlive:
            self.move1(other)

    def display(self):
        super().display()

#=============开始菜单=============
class StartPage(object):
    def __init__(self):
        self.beforeStart = []
        for i in range(1,11):
            self.beforeStart.append(pygame.image.load("../resources/img/beforeStart_"+str(i)+".jpg"))
        # self.beforeStart = pygame.image.load("../resources/img/beforeStart.jpg").convert_alpha()
        self.afterStart = pygame.image.load("../resources/img/afterStart.jpg").convert_alpha()

    def isFocus(self):
        point_x, point_y = pygame.mouse.get_pos()
        if (220 < point_x < 380) and (293 < point_y < 333):
            return True
        else:
            return False
    def display(self):
        if self.isFocus():
            surface.blit(self.afterStart, (0, 0))
        else:
            if gameCount % 9 == 0:
                num = gameCount % 10
                surface.blit(self.beforeStart[num], (0, 0))

#=============胜利界面=============
class WinPage(object):
    def __init__(self):
        # self.beforeStart = []
        # for i in range(1,11):
        #     self.beforeStart.append(pygame.image.load("../resources/img/beforeStart_"+str(i)+".jpg"))
        # self.beforeStart = pygame.image.load("../resources/img/beforeStart.jpg").convert_alpha()
        self.beforeContinue = pygame.image.load("../resources/img/test.jpg").convert_alpha()
        self.afterContinue = pygame.image.load("../resources/img/test.jpg").convert_alpha()

    def isFocus(self):
        point_x, point_y = pygame.mouse.get_pos()
        if (220 < point_x < 380) and (293 < point_y < 333):
            return True
        else:
            return False
    def display(self):
        if self.isFocus():
            surface.blit(self.afterContinue, (0, 0))
        else:
            surface.blit(self.beforeContinue, (0, 0))

#============操控行为方法================
# def arrive(source,destination):
#     lenX=destination.x-source.x
#     lenY=destination.y-source.y
#     # dirTo=destination-source
#     if lenY==0:
#         if lenX > 10:
#             source.x+=source.speed * timePassedSecond
#         elif lenX <-10:
#             source.x -= source.speed * timePassedSecond
#         else :
#             source.x+=source.speed*timePassedSecond*lenX/10.
#     elif lenX==0:
#         if lenY > 10:
#             source.y+=source.speed * timePassedSecond
#         elif lenY<-10:
#             source.y -= source.speed * timePassedSecond
#         else :
#             source.y+=source.speed*timePassedSecond*lenY/10.

# def seek(source,destination):
#     lenX = destination.x - source.x
#     lenY = destination.y - source.y
#     # dirTo=destination-source
#     if lenY == 0:
#         source.x += source.speed * timePassedSecond
#     elif lenX == 0:
#         source.y += source.speed * timePassedSecond


#==================边界限制方法====================
def borderLimit(eneity):
    if eneity.x > surface_WIDTH - eneity.width:
        eneity.x = surface_WIDTH - eneity.width
    if eneity.x < 0:
        eneity.x = 0
    if eneity.y > surface_HEIGHT- eneity.height:
        eneity.y = surface_HEIGHT- eneity.height
    if eneity.y < 0:
        eneity.y = 0

#=======================事件监听方法=====================
def eventListener():
    global pressedKey,gameMode,startPage,pause,winPage   #按键信息
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            left, wheel, right = pygame.mouse.get_pressed()
            if left == 1 and gameMode == True:
                player.fire()
            if left == 1 and gameMode == False and startPage.isFocus():
                gameMode = True
            if left == 1 and gameMode == False and winPage.isFocus():
                gameMode = True

        if event.type == KEYDOWN:
            if event.key == K_j:
                player.fire()
            if event.key == K_k:
                player.fire1()
            if event.key == K_p:
                pause=True
                gamePause()
            # if event.key == K_k:
            #     surface.blit(afterStart, (0, 0))
            #     gameMode = True
        # if event.type == MOUSEBUTTONDOWN:  # 按下鼠标触发
        #     left, wheel, right = pygame.mouse.get_pressed()
        #     if left == 1:
        #         player.move()
        # if event.type == MOUSEBUTTONUP:  # 抬起鼠标触发
        #     left, wheel, right = pygame.mouse.get_pressed()
        #     if left == 0:
        #         player.stop()
        # if event.type == KEYDOWN:  #键盘按下
        #     if event.key == locals.K_b:
        #         super_boom()
        # if event.type == VIDEORESIZE: #屏幕拉伸
        #     surface_SIZE = event.size
        #     surface = pygame.display.set_mode(surface_SIZE, RESIZABLE, 32)
        #     pygame.display.set_caption("Window resized to" + str(event.size))
    pressedKey = pygame.key.get_pressed()

#======================获取地图表方法===========================
def getList(Tlist,Tarray):
    blockLen=len(Tarray) #地图表长度
    i,j=0,0
    #获取地图表
    while i<blockLen:
        while j<len(Tarray[i]):
            mp=Block(j*mapBlockLenth,i*mapBlockLenth,Tarray[i][j])
            Tlist.append(mp)
            j+=1
        j=0
        i+=1
#=========================初始化方法==========================
def init():
    global surface,clock,player,background,tank1,tank2,tank3,startPage,winPage,pauseBackground,overImg,enemies,myfont ,winImg  #,textSurface,fenshu
    surface = pygame.display.set_mode((surface_WIDTH, surface_HEIGHT), 0, 32)
    myfont=pygame.font.SysFont("../resources/font/consola.ttf",28)#字体设置
    # textSurface=myfont.render("分数：%d"%fenshu,True,(255,255,255))
    # fenshu=0
    pygame.display.set_caption("坦克大战")
    background = pygame.image.load("../resources/img/background.png").convert()
    tank1 = pygame.image.load("../resources/img/tank_1.png").convert_alpha()
    tank2 = pygame.image.load("../resources/img/tank_2.png").convert_alpha()
    tank3 = pygame.image.load("../resources/img/tank_3.png").convert_alpha()
    pauseBackground = pygame.image.load("../resources/img/pause.png").convert_alpha()
    # beforeStart = pygame.image.load("../resources/img/beforeStart.jpg").convert_alpha()
    # afterStart = pygame.image.load("../resources/img/afterStart.jpg").convert_alpha()
    # beforeStart = pygame.image.load("../resources/img/beforeStart.jpg").convert_alpha()
    # afterStart = pygame.image.load("../resources/img/afterStart.jpg").convert_alpha()
    overImg = pygame.image.load("../resources/img/fail.png").convert_alpha()
    winImg = pygame.image.load("../resources/img/victory.png").convert_alpha()
    clock = pygame.time.Clock()
    player = Player(80, 240)
    bat.append(Battery(480, 180,level))
    # enemy = Enemy(400,300)
    startPage = StartPage()
    winPage = WinPage()
    i = 1
    # 获取墙图片
    while i <= wallNum:
        sprite = pygame.image.load("../resources/img/wall_%d.png" % (i)).convert_alpha()
        wallSprite.append(sprite)
        i += 1


#=========================游戏暂停======================
def gamePause():
    global pause
    surface.blit(pauseBackground, (0, 0))
    while pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause=False
            if event.type == MOUSEBUTTONDOWN:  # 按下鼠标触发
                left, wheel, right = pygame.mouse.get_pressed()
                if left == 1:
                    pause=False
        clock.tick(FPS)
        pygame.display.update()


#=========================随机地图======================
def randomMap():
    i=1
    generatedMap=[]
    while i<=10:
        mapRow =[]
        j = 1
        while j<=15:
            if random.random()<=0.6:
                mapRow.append(0)
            elif random.random()<=0.3:
                mapRow.append(7)
            else:
                mapRow.append(random.randint(1,12))
            j+=1
        generatedMap.append(mapRow)
        i+=1
    return generatedMap
#=========================总更新方法======================
def update():
    cloud_update()
    for b in bat:
        b.update()
    if not isGameOver:
        player.update()
    for enemy in enemies:
        enemy.update()
    crash()
    bulletsUpdate()
    superBulletsUpdate()
    blocksUpdate()
    missileUpdate()
    for b in bat:
        missileLaunch(player, b)
    # textSurface = myfont.render("score:%d" % fenshu, True, (255, 255, 255))

#========================显示 绘制 方法========================
def display():
    surface.blit(background, (0, 0))
    for mps in mapList:
        mps.display()
    for b in bat:
        b.display()
    if not isGameOver:
        player.display()
        for bullet in playerBullets:
            bullet.display()
    for bullet in playerSuperBullets:
        bullet.display()
    for missile in batBullets:
        missile.display()
    for bullet in enemyBullets:
        bullet.display()
    for enemy in enemies:
        enemy.display()
    packageDisplay()
    for cld1 in clouds1:
        cld1.display()
    for cld in clouds:
         cld.display()

    surface.blit(myfont.render("score:%d" % score, True, (255, 255, 255)),(0,0))
    surface.blit(myfont.render("level:%d" % level, True, (255, 255, 255)), (0, 30))
    surface.blit(myfont.render(u"superBullet:%d"%superBulletNum,True,(255,255,255)),(0,60))

def bulletsUpdate():
    needRemove = []
    removeNeed = []
    for bullet in playerBullets:
        if not bullet.isAlive:
            needRemove.append(bullet)
        bullet.update()
    for bullet in enemyBullets:
        if not bullet.isAlive:
            removeNeed.append(bullet)
        bullet.update()
    for bullet in needRemove:
        playerBullets.remove(bullet)
    for bullet in removeNeed:
        enemyBullets.remove(bullet)
def missileUpdate():
    need_remove=[]
    for missile in batBullets:
        if not missile.isAlive:
            need_remove.append(missile)
        missile.update()
    for missile in need_remove:
        batBullets.remove(missile)

def packageDisplay():
    for p in hpPackages:
        p.display()
    for s in superBulletPackages:
        s.display()

def superBulletsUpdate():
    global score
    needRemove = []
    for bullet in playerSuperBullets:
        if not bullet.isAlive:
            needRemove.append(bullet)
        bullet.update()
    for bullet in needRemove:
        for blk in mapList:
            if blk.x<=bullet.x+60 and blk.x>=bullet.x-60 \
                and blk.y<=bullet.y+60 and blk.y>=bullet.y-60:
                blk.isAlive=False
        for enemy in enemies:
            if enemy.x<=bullet.x+60 and enemy.x>=bullet.x-60 \
                and enemy.y<=bullet.y+60 and enemy.y>=bullet.y-60:
                score +=10
                enemy.isAlive=False
        # playerSuperBullets.remove(bullet)

def crash():
    if not isGameOver:
        playerCrashBlock()
        packageCrash()
        enemyCrashBlock()
        playerBulletCrash()
        enemyBulletCrash()
        playerCrashEnemy()
        EnemyCrashEnemy()
        MisCrashPlayer()


def MisCrashPlayer():
    for b in batBullets:
        if b.isCrash(player):
            player.hurt(b)
            b.isAlive=False

def playerCrashBlock():
    for blk in mapList:
        if blk.type and blk.isAlive:
            player.isCrash(blk)

def missileLaunch(player,bat): #导弹发射策略
    global level
    dis_x=bat.x-player.x
    dis_y=bat.y-player.y
    dis_s=math.sqrt(dis_x**2+dis_y**2)
    if dis_s<700:
         if gameCount%(310-10*level)==0:
            bat.fire()
            # print("炮台开火")

def playerCrashEnemy():
    for enemy in enemies:
        # player.isCrash(enemy)
        enemy.isCrash(player)

def EnemyCrashEnemy():
    for enemy1 in enemies:
        for enemy2 in enemies:
            if enemy1 != enemy2:
                enemy1.isCrash(enemy2)

def enemyCrashBlock():
    for blk in mapList:
        for enemy in enemies:
            if blk.type:
                enemy.isCrash(blk)

def playerBulletCrash():
    for p_b in playerBullets:
        for blk in mapList:
            if blk.type:
                if p_b.isCrash(blk) and p_b.isAlive and blk.isAlive:
                    blk.hurt(p_b)
                    p_b.isAlive = False
        for enemy in enemies:
            if p_b.isCrash(enemy) and p_b.isAlive and enemy.isAlive:
                enemy.hurt(p_b)
                p_b.isAlive = False
        for p_b in playerBullets:
            for b in bat:
                if p_b.x < b.x + b.width \
                        and p_b.x + p_b.width > b.x \
                        and p_b.y < b.y + b.height \
                        and p_b.y + p_b.height > b.y and p_b.isAlive and b.isAlive:
                    b.hurt(p_b)
                    p_b.isAlive = False


def enemyBulletCrash():
    for p_b in enemyBullets:
        for blk in mapList:
            if blk.type:
                if p_b.isCrash(blk) and p_b.isAlive and blk.isAlive:
                    blk.hurt(p_b)
                    p_b.isAlive = False
        if p_b.isCrash(player) and p_b.isAlive and player.isAlive:
            player.hurt(p_b)
            p_b.isAlive = False

def packageCrash():
    needRemove1=[]
    needRemove2=[]
    for p in hpPackages:
        if player.x < p.x + p.width \
                and (player.x + player.width) > p.x \
                and player.y < p.y + p.height \
                and (player.y + player.height) > p.y :
            p.useIt(player)
            needRemove1.append(p)
    for s in superBulletPackages:
        if player.x < s.x + s.width \
                and (player.x + player.width) > s.x \
                and player.y < s.y + s.height \
                and (player.y + player.height) > s.y :
            s.useIt()
            needRemove2.append(s)

    for p in needRemove1:
        hpPackages.remove(p)
    for s in needRemove2:
        superBulletPackages.remove(s)

# 开始游戏界面
# def showGame():
#     if(gameMode == False):
#         surface.blit(beforeStart, (0, 0))
# 真正的初始化
def startGame():
    global gameCount,mapList,randomDir,mapArrayIndex,score
    if firstLevel:
        score = 0
    init()

    randomDir = random.randint(1, 4)
    mapArrayIndex = randomMap()
    mapArrayIndex[6][2] = 0
    mapArrayIndex[4][12] = 0
    mapArrayIndex[5][12] = 0
    mapList = []  # 地图表，存储障碍物精灵图片
    # init()  # 初始化
    getList(mapList, mapArrayIndex)  # 根据障碍物位置信息填写地图表
    gameCount = 0


def blocksUpdate():
    for blk in mapList:
        if blk.type:
            #print(blk.isAlive)
            #if not blk.isAlive:
                #mapList.remove(blk)
            #need_remove.append(blk)
            blk.update()
    # for blk in need_remove:
    #     mapList.remove(blk)

def cloud_update():
    global cloud_time
    need_remove = []
    need_remove1 = []
    for cld in clouds:
        if not cld.isAlive:
            need_remove.append(cld)
        cld.update()
    for cld1 in clouds1:
        if not cld1.isAlive:
            need_remove1.append(cld1)
        if clouds1.index(cld1)<len(clouds1):
            cld1.update1(clouds[clouds1.index(cld1)])
        else:
            cld1.update1(clouds[clouds1.index(cld1)-1])
    for cld in need_remove:
        clouds.remove(cld)
    for cld1 in need_remove1:
        clouds1.remove(cld1)
    if gameCount % cloud_time == 0:
        cloud_time = random.randint(1, 4) * 50
        if len(clouds)<=3:
            c = Cloud()
            c1= Cloud()
            c1.x=c.x+30
            c1.y=c.y+30
            # if c.x_speed>0:
            #     c1.x_speed=c.x_speed-1
            # else:
            #     c1.x_speed = c.x_speed + 1
            # if c.y_speed>0:
            #     c1.y_speed=c.y_speed-1
            # else:
            #     c1.y_speed = c.y_speed + 1
            i=random.randint(1, 3)
            c.sprite=pygame.image.load("../resources/img/cloud_%d.png" % (i)).convert_alpha()
            c1.sprite=pygame.image.load("../resources/img/cloud_%d.png" % (i+3)).convert_alpha()
            clouds1.append(c1)
            clouds.append(c)

gameMode = False #标志位，判断是游戏开始界面还是游戏界面
surface = None
clock = None
background=None
myfont=None
textSurface=None
# fenshu=0
clouds=[]
clouds1=[]
bat=[]
batBullets=[]  #炮塔子弹
cloud_time = random.randint(1, 6) * 35
tank1=None
tank2=None
tank3=None
beforeStart = None
afterStart = None

hpPackages=[]
superBulletPackages=[]

superBulletNum=2
timePassed=0        #记录游戏时间，ms
timePassedSecond=0  #记录游戏时间，s
gameTime = 0        #游戏总时间
surface_WIDTH=600   #屏幕宽度
surface_HEIGHT=400  #屏幕高度
# bgColor = (55,45,85)
enemies = [] #敌人数组
playerBullets = [] #玩家子弹
enemyBullets = [] #敌人子弹
playerSuperBullets=[]
randomDir = None
FPS=60          #最大帧数
mapBlockLenth=40 #地图块大小
wallSprite=[]   #障碍物精灵组
tankSprite=[]   #坦克精灵组
wallNum=12      #障碍物总种类
tankNum=2       #坦克总数
gameCount = 0
player=None     #玩家
startPage = None
winPage=None
isGameOver = False #玩家是否存活
winTheGame=False
mapList = None #地图表
gameOverCount = 0 #
winGameCount = 0
mapArrayIndex = None
firstLevel=True
#障碍物位置信息  15*10
# mapArrayIndex=[
#     [0,1,0,0,0,4,0,2,0,0,0,3,2,0,0,0],
#     [0,0,0,0,2,0,4,0,0,0,0,0,0,1,2,0],
#     [0,0,0,1,5,0,0,0,3,0,0,0,3,1,0,0],
#     [2,0,0,1,0,6,1,0,0,0,0,0,0,5,0,1],
#     [0,0,3,1,0,0,0,3,0,1,2,0,0,0,2,1],
#     [0,2,6,0,0,5,0,0,0,0,0,2,0,0,0,1],
#     [0,3,0,1,0,1,0,6,0,0,0,0,3,0,3,6],
#     [0,0,0,1,0,1,0,3,1,0,0,1,0,1,5,2],
#     [0,0,3,0,0,0,0,0,0,0,2,6,0,1,4,6],
#     [0,0,2,1,6,0,0,5,0,4,0,6,1,0,2,1],
#     #[0,0,0,1,2,0,0,0,3,0,0,0,3,1,0,0],
#     ]
# mapArrayIndex=randomMap()
# mapList=[]      #地图表，存储障碍物精灵图片
# init()          #初始化
# getList(mapList,mapArrayIndex)  #根据障碍物位置信息填写地图表
#绘制背景地图
#绘制障碍物
# for mps in mapList:
#     mps.display(surface)
#     print(mps)
# gameCount = 0
# showGame()
level=1
startGame()
# showGame()
pause=False

while True:
    if gameCount%120==0:
        while (len(enemies) < 3):
            enemy = Enemy(random.randint(10,14)*40,random.randint(4,6)*40,level)
            mapArrayIndex[enemy.y//40][enemy.x//40] = 0
            enemies.append(enemy)

    gameCount += 1
    if gameCount == 1000000:
        gameCount = 0
    eventListener() #事件监听
    timePassed = clock.tick(FPS)  # 获取时间ms
    timePassedSecond = timePassed / 1000.0  # 时间转换为s
    gameTime += timePassed
    # for event in pygame.event.get():
    #     if event.type == QUIT:
    #         exit()
    # surfaceWidth, surfaceHeight = surface_SIZE
    #
    # # 重新填满窗口
    # for y in range(0, surfaceHeight, background.get_height()):
    #     for x in range(0, surfaceWidth, background.get_width()):
    #         surface.blit(background, (x, y))
    # clock.tick(60)
    #surface.blit(background,(0,0))
    # surface.blit(ikongSprite,(0,0))
    # 绘制地图
    # for mps in mapList:
    #     mps.drawWall(surface)
    #     print(mp)

    if(gameMode == False and firstLevel==True):
        # if winTheGame:
        #     winPage.display()
        # else:
        startPage.display()
    else:
        update()
        display()
    # if winTheGame:
    #     surface.blit(winImg, (0, 0))
    # if winTheGame:
    #     if winPage.isf

    if winTheGame:
        bat.clear()
        #hpPackages.clear()
        #superBulletPackages.clear()
        gameMode = True
        surface.blit(winImg, (0, 0))
        winGameCount += 1
        if winGameCount > 70:
            level+=1
            firstLevel=False
            winTheGame = False
            gameMode = False
            winGameCount = 0
            startGame()

    elif isGameOver:
        bat.clear()
        hpPackages.clear()
        superBulletPackages.clear()
        # for i in range(1,180):
        # surface.blit(overImg, (215, 125))
        gameMode = True
        surface.blit(overImg, (0, 0))
        gameOverCount += 1
        level=1
        if gameOverCount > 70:
            gameMode = False
            firstLevel=True
            isGameOver = False
            gameOverCount = 0
            startGame()
    pygame.display.update()