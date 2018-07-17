
import pygame,os,sys
from pygame.locals import *
from sys import exit

pygame.init()
#游戏实体
class GameObject(object):
    def __init__(self):
        self.x=None
        self.y=None
        self.width=None
        self.height=None
        self.isAlive=True
        self.sprite=None

    def setImage(self):
        pass

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
        self.x=x
        self.y=y
        self.sprite=wallSprite[type-1]
        self.type=type

    #用于检测在此方块上的碰撞
    def isCrash(self,other):
        pass

    def setImage(self,sprite):
        self.sprite=sprite

    #在surface上绘制
    def display(self,surface):
        if self.type == 0:
            return
        surface.blit(self.sprite,(self.x,self.y))

    def update(self):
        pass

    def __str__(self):
        return "坐标(%d,%d),地图%d"%(self.x,self.y,self.type)

# 坦克类
# class Tank(GameObject):
#     def __init__(self,x,y,type):
#         super().__init__(x,y,type)
#         self.sprite=tankSprite[type-1]
#
#     def __str__(self):
#         return "坐标(%d,%d),坦克类型%d"%(self.x,self.y,self.type)
#

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
    i = 1
    # 获取墙图片
    while i <= wallNum:
        sprite = pygame.image.load("../resources/img/wall_%d.png" % (i)).convert_alpha()
        wallSprite.append(sprite)
        i += 1
    i = 1

surface_WIDTH=600   #屏幕宽度
surface_HEIGHT=400  #屏幕高度
# bgColor = (55,45,85)

surface=pygame.display.set_mode((surface_WIDTH,surface_HEIGHT),0,32)
background=pygame.image.load("../resources/img/background.png").convert()
clock=pygame.time.Clock()

mapBlockLenth=40 #地图块大小
wallSprite=[]   #障碍物精灵组
tankSprite=[]   #坦克精灵组
wallNum=6      #障碍物总数
tankNum=2       #坦克总数
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
mapList=[]
init()
getList(mapList,mapArrayIndex)
#绘制背景地图
surface.blit(background,(0,0))
for mps in mapList:
    mps.display(surface)
    print(mps)

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()

        # if event.type == VIDEORESIZE:
        #     surface_SIZE = event.size
        #     surface = pygame.display.set_mode(surface_SIZE, RESIZABLE, 32)
        #     pygame.display.set_caption("Window resized to" + str(event.size))
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

    for mps in mapList:
        mps.display(surface)
    pygame.display.update()