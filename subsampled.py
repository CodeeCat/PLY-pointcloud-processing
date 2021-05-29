import time
import classes
import random

def subSampled(pointlist,gridlist):               #取一个栅格内所有点的坐标平均值、rgb平均值，创建新点代替栅格内所有点
    newpointlist=[]
    gridnum=0
    for grid in gridlist:
        Cx=0
        Cy=0
        Cz=0
        Cr=0
        Cg=0
        Cb=0
        for pid in grid.pointList:
            xyz=pointlist[pid].getXyz()
            Cx+=xyz[0]
            Cy+=xyz[1]
            Cz+=xyz[2]
            rgb=pointlist[pid].getRgb()
            Cr+=rgb[0]
            Cg+=rgb[1]
            Cb+=rgb[2]
        pointnum=len(grid.pointList)
        Cx=round(Cx/pointnum,4)
        Cy=round(Cy/pointnum,4)
        Cz=round(Cz/pointnum,4)
        Cr=int(Cr//pointnum)
        Cg=int(Cg//pointnum)
        Cb=int(Cb//pointnum)
        center=classes.Point(len(newpointlist),Cx,Cy,Cz,Cr,Cg,Cb)
        newpointlist.append(center)
        gridnum+=1
        if gridnum%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已下采样"+str(gridnum//(len(gridlist)//100))+"%")
    return newpointlist


def randomSampled(ratio,gridlist):                #对每一个栅格随其采样 0<ratio<1：采样比例
    newpointlist=[]
    gridnum=0
    for grid in gridlist:
        for i in range(int((1-ratio)*len(grid.pointList))):
            grid.pointList.pop(random.randrange(0,len(grid.pointList)))
        gridnum+=1
        if gridnum%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已下采样"+str(gridnum//(len(gridlist)//100))+"%")
