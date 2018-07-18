import pygame,os,sys,math,random
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2
import time

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
class Map(GameObject):
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
                mapList.remove(self)
                self.isAlive = False
                self.boom_index = len(self.boom_img) - 1
            self.sprite = self.boom_img[self.boom_index]
            #print(game_count)
            if gameCount % 3 == 0:
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
        self.life=100
        self.lifeFrame = pygame.image.load("../resources/img/blood.png")    #血条

    def fire(self):
        bullet = Bullet(self.x,self.y,self.width,self.height,self.direction)
        playerBullets.append(bullet)

    def hurt(self):
        if gameCount % 10 == 0:
            self.life -= 5

    def move(self):
        pass

    def isCrash(self,other):
        if super().isCrash(other,True) and other.isAlive:
            return self.direction
        return 0

    def update(self):
        #pressedKey = pygame.key.get_pressed()   #获取按键
        moveDir=Vector2(0,0)    #移动方向
        #self.hurt() #此处完成后需删除
        global isGameOver
        if self.life <= 0:
            isGameOver = True
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
        surface.blit(self.lifeFrame, (self.x, self.y - 5))
        if self.life > 0:
            pygame.draw.rect(surface, (255, 0, 0),
                             (self.x - self.width + 39.8, self.y - self.height + 35,
                              57 * self.life / 140, 5))
        surface.blit(self.sprite,(self.x,self.y))

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
            self.y = y - self.height
        elif(direction == 2):
            # self.sprite = pygame.transform.rotate(self.sprite, 90.)
            self.xSpeed = 5
            self.ySpeed = 0
            self.x = x + width
            self.y = y + height/2 - self.height/2
        elif(direction == 3):
            self.sprite = pygame.transform.rotate(self.sprite, -90.)
            self.xSpeed = 0
            self.ySpeed = 5
            self.x = x + width/2 - self.width/2
            self.y = y + height
        elif(direction == 4):
            self.sprite = pygame.transform.rotate(self.sprite, 180.)
            self.xSpeed = -5
            self.ySpeed = 0
            self.x = x - self.width
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

#========================敌人类=====================
class Enemy():
    def __init__(self,x,y):
        super().__init__()
        super().setImage("../resources/img/tank_2.png")
        self.x = x
        self.y = y
        # self.direction=Vector2(0,-1)
        self.direction = 1  # 坦克朝向 1上2右3下4左
        self.needMove = False
        self.speed = 100
        self.life = 100
        self.patrolPath=[]

    def hurt(self):
        pass

    def move(self):
        pass

    def update(self):
        moveDir = Vector2(0, 0) #移动方向

        if self.direction==1:
            moveDir=Vector2(0,-1)
        elif self.direction == 2:
            moveDir=Vector2(1,0)
        elif self.direction == 3:
            moveDir=Vector2(0,1)
        elif self.direction == 4:
            moveDir=Vector2(-1,0)

        moveDir.normalise()  # 向量规格化

        # self.x += moveDir.x * self.speed * timePassedSecond
        # self.y += moveDir.y * self.speed * timePassedSecond

    def patrol(self):
        pathPoint=self.patrolPath.pop()


    def setPatrolPath(self):
        pass


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

#============操控行为方法================
def arrive(source,destination):
    lenX=destination.x-source.x
    lenY=destination.y-source.y
    # dirTo=destination-source
    if lenY==0:
        if lenX > 10:
            source.x+=source.speed * timePassedSecond
        elif lenX <-10:
            source.x -= source.speed * timePassedSecond
        else :
            source.x+=source.speed*timePassedSecond*lenX/10.
    elif lenX==0:
        if lenY > 10:
            source.y+=source.speed * timePassedSecond
        elif lenY<-10:
            source.y -= source.speed * timePassedSecond
        else :
            source.y+=source.speed*timePassedSecond*lenY/10.

def seek(source,destination):
    lenX = destination.x - source.x
    lenY = destination.y - source.y
    # dirTo=destination-source
    if lenY == 0:
        source.x += source.speed * timePassedSecond
    elif lenX == 0:
        source.y += source.speed * timePassedSecond


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
    global pressedKey,gameMode,startPage,pause   #按键信息
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            left, wheel, right = pygame.mouse.get_pressed()
            if left == 1 and gameMode == True:
                player.fire()
            if left == 1 and gameMode == False and startPage.isFocus():
                gameMode = True
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.fire()
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
            mp=Map(j*mapBlockLenth,i*mapBlockLenth,Tarray[i][j])
            Tlist.append(mp)
            j+=1
        j=0
        i+=1

#=========================初始化方法==========================
def init():
    global surface,clock,player,background,tank1,tank2,tank3,startPage,pauseBackground,overImg
    surface = pygame.display.set_mode((surface_WIDTH, surface_HEIGHT), 0, 32)
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
    clock = pygame.time.Clock()
    player = Player(320, 240)
    startPage = StartPage()

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
    if not isGameOver:
        player.update()
    crash()
    bulletsUpdate()
    blocksUpdate()

#========================显示 绘制 方法========================
def display():
    surface.blit(background, (0, 0))
    for mps in mapList:
        mps.display()
    if not isGameOver:
        player.display()
        for bullet in playerBullets:
            bullet.display()

def bulletsUpdate():
    needRemove = []
    for bullet in playerBullets:
        if not bullet.isAlive:
            needRemove.append(bullet)
        bullet.update()
    for bullet in needRemove:
        playerBullets.remove(bullet)

def crash():
    if not isGameOver:
        playerCrashBlock()
        playerBulletCrashBlock()


def playerCrashBlock():
    for blk in mapList:
        if blk.type:
            player.isCrash(blk)

def playerBulletCrashBlock():
    for p_b in playerBullets:
        for blk in mapList:
            if blk.type:
                if p_b.isCrash(blk) and p_b.isAlive and blk.isAlive:
                    blk.hurt(p_b)
                    p_b.isAlive = False
# 开始游戏界面
# def showGame():
#     if(gameMode == False):
#         surface.blit(beforeStart, (0, 0))
# 真正的初始化
def startGame():
    global gameCount,mapList
    mapArrayIndex = randomMap()
    mapList = []  # 地图表，存储障碍物精灵图片
    init()  # 初始化
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
gameMode = False #标志位，判断是游戏开始界面还是游戏界面
surface = None
clock = None
background=None
tank1=None
tank2=None
tank3=None
beforeStart = None
afterStart = None
timePassed=0        #记录游戏时间，ms
timePassedSecond=0  #记录游戏时间，s
gameTime = 0        #游戏总时间
surface_WIDTH=600   #屏幕宽度
surface_HEIGHT=400  #屏幕高度
# bgColor = (55,45,85)

playerBullets = [] #玩家子弹

FPS=60          #最大帧数
mapBlockLenth=40 #地图块大小
wallSprite=[]   #障碍物精灵组
tankSprite=[]   #坦克精灵组
wallNum=12      #障碍物总种类
tankNum=2       #坦克总数
gameCount = 0
player=None     #玩家
startPage = None
isGameOver = False #玩家是否存活
mapList = None #地图表
gameOverCount = 0 #
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

startGame()

# showGame()
pause=False

while True:
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


    if(gameMode == False):
        startPage.display()
    else:
        update()
        display()
    if isGameOver:
        # for i in range(1,180):
        # surface.blit(overImg, (215, 125))
        surface.blit(overImg, (0, 0))
        gameOverCount += 1
        if gameOverCount > 70:
            gameMode = False
            isGameOver = False
            gameOverCount = 0
            startGame()
    pygame.display.update()