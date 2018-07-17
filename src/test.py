
import pygame,os,sys
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2

# pygame.init()
#游戏实体
class GameObject(object):
    def __init__(self):
        self.x=None
        self.y=None
        self.width=None
        self.height=None
        self.isAlive=True
        self.img=None

    def setImage(self,imgPath):
        self.img=pygame.image.load(imgPath)
        self.width,self.height=self.img.get_size()

    def update(self):
        pass

    def display(self):
        pass

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        pass

    def __str__(self):
        return "坐标(%d,%d),名称%s"%(self.x,self.y,self)

#地图类
class Map(GameObject):
    def __init__(self,x,y,type):
        super().__init__()
        self.x=x
        self.y=y
        self.img=wallimg[type-1]
        self.type=type
        self.width,self.height=self.img.get_size()

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        pass

    def setImage(self,img):
        self.img=img
        self.width=img

    #在surface上绘制
    def display(self):
        if self.type == 0:
            return
        surface.blit(self.img,(self.x,self.y))

    def update(self):
        pass

    def __str__(self):
        return "坐标(%d,%d),地图%d"%(self.x,self.y,self.type)

# 玩家类
class Player(GameObject):
    def __init__(self,x,y):
        super().__init__()
        super().setImage("../resources/img/tank_1.png")
        self.x=x
        self.y=y
        self.diraction=Vector2(0,0)    #坦克朝向
        self.needMove=False
        self.speed=30
        self.life=100
        #self.lifeFrame=        #血条

    def fire(self):
        pass

    def hurt(self):
        pass

    def move(self):
        pass

    def update(self):
        pressedKey = pygame.key.get_pressed()
        if pressedKey:
            if pressedKey[K_a]:
                self.diraction.x = -1
                self.needMove=True
            if pressedKey[K_d]:
                self.diraction.x = 1
                self.needMove = True
            if pressedKey[K_w]:
                self.diraction.y = -1
                self.needMove = True
            if pressedKey[K_s]:
                self.diraction.y = 1
                self.needMove = True
        else:
            self.x=0
            self.y=0
            self.needMove=False
        self.diraction.normalise()
        self.x += self.diraction.x * self.speed * timePassedSecond
        self.y += self.diraction.y * self.speed * timePassedSecond
        borderLimit(self)

    def changWeapon(self):
        pass

    def display(self):

        surface.blit(self.img,(self.x,self.y))

#边界限制
def borderLimit(eneity):
    if eneity.x > surface_WIDTH - eneity.width:
        eneity.x = surface_WIDTH - eneity.width
    if eneity.x < 0:
        eneity.x = 0
    if eneity.y > surface_HEIGHT- eneity.height:
        eneity.y = surface_HEIGHT- eneity.height
    if eneity.y < 0:
        eneity.y = 0

#事件监听方法
def eventListener():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
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

#获取地图表
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

#初始化
def init():
    global surface,clock,player,background,tank1,tank2,tank3
    surface = pygame.display.set_mode((surface_WIDTH, surface_HEIGHT), 0, 32)
    background = pygame.image.load("../resources/img/background.png").convert()
    tank1 = pygame.image.load("../resources/img/tank_1.png").convert_alpha()
    tank2 = pygame.image.load("../resources/img/tank_2.png").convert_alpha()
    tank3 = pygame.image.load("../resources/img/tank_3.png").convert_alpha()
    clock = pygame.time.Clock()
    player = Player(320, 240)

    i = 1
    # 获取墙图片
    while i <= wallNum:
        img = pygame.image.load("../resources/img/wall_%d.png" % (i)).convert_alpha()
        wallimg.append(img)
        i += 1


#总更新方法
def update():
    player.update()

def display():
    surface.blit(background, (0, 0))
    for mps in mapList:
        mps.display()
    player.display()


surface = None
clock = None
background=None
tank1=None
tank2=None
tank3=None
timePassed=0        #记录游戏时间，ms
timePassedSecond=0  #记录游戏时间，s
surface_WIDTH=600   #屏幕宽度
surface_HEIGHT=400  #屏幕高度
# bgColor = (55,45,85)


FPS=60          #最大帧数
mapBlockLenth=40 #地图块大小
wallimg=[]   #障碍物精灵组
tankimg=[]   #坦克精灵组
wallNum=6      #障碍物总数
tankNum=2       #坦克总数

player=None     #玩家

#障碍物位置信息
mapArrayIndex=[
    [0,1,0,0,0,4,0,2,0,0,0,3,2,0,0,0,2,0,0,0],
    [0,0,0,0,2,0,4,0,0,0,0,0,0,1,2,0,0,0,3,0],
    [0,0,0,1,5,0,0,0,3,0,0,0,3,1,0,0,2,6,0,1],
    [2,0,0,1,0,6,1,0,0,0,0,0,0,5,0,1],
    [0,0,3,1,0,0,0,3,0,1],
    [0,2,6,0,0,5,0,0,0,0,0,2,0,0,0,1,2],
    [0,3,0,1,0,1,0,6,0,0],
    [0,0,0,1,0,1,0,3,1,0],
    [0,0,3,0,0,0,0,0,0,0],
    [0,0,2,1,6,0,0,5,0,4],
    [0,0,0,1,2,0,0,0,3,0,0,0,3,1,0,0,0,1,0,1],
    ]
mapList=[]      #地图表，存储障碍物精灵图片
init()          #初始化
getList(mapList,mapArrayIndex)  #根据障碍物位置信息填写地图表
#绘制背景地图
surface.blit(background,(0,0))
#绘制障碍物
# for mps in mapList:
#     mps.display(surface)
#     print(mps)

while True:
    eventListener() #事件监听
    timePassed = clock.tick(FPS)  # 获取时间ms
    timePassedSecond = timePassed / 1000.0  # 时间转换为s
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
    # surface.blit(ikongimg,(0,0))
    # 绘制地图
    # for mps in mapList:
    #     mps.drawWall(surface)
    #     print(mp)
    update()
    display()

    pygame.display.update()