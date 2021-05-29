import tools

class Point:
    __pid=0           #点序号
    __xyz=[0,0,0]     #点坐标
    __rgb=[0,0,0]     #0-255    
    __hsv=[0,0,0]     #0-360,0-1,0-1
    __idOfGrid=0      #所属栅格的序号

    def __init__(self,pid,x,y,z,r,g,b):
        self.__pid=pid
        self.__xyz=[x,y,z]
        self.__rgb=[r,g,b]
        self.__hsv=tools.rgb2hsv(self.__rgb)

    def getPid(self):
        return self.__pid

    def getXyz(self):                                   #深拷贝防止被篡改
        xyz=[]
        for i in self.__xyz:
            xyz.append(i)
        return xyz

    def getRgb(self):
        rgb=[]
        for i in self.__rgb:
            rgb.append(i)
        return rgb

    def getHsv(self):
        hsv=[]
        for i in self.__hsv:
            hsv.append(i)
        return hsv

    def setIdOfGrid(self,gid):
        self.__idOfGrid=gid
    
    def getIdOfGrid(self):
        return self.__idOfGrid

class Grid:
    __gid=0                   #栅格序号
    __Xyz=[0,0,0]             #栅格坐标
    pointList=[]              #存放该栅格内点序号的序列
    neighbourList=[]           #非空邻域栅格序号的序列
    iscanopy=0                 #栅格是否为树冠
    istrunk=0                   #是否为树干

    def __init__(self,gid,x,y,z):
        self.__gid=gid
        self.__Xyz=[x,y,z]
        self.pointList=[]
        self.neighbourList=[]
        self.iscanopy=0
        self.istrunk=0

    def getGid(self):
        return self.__gid

    def getXyz(self):
        xyz=[]
        for i in self.__Xyz:
            xyz.append(i)
        return xyz