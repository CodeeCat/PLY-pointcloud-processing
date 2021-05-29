import math
import numpy as np
import classes
import time
def Rodrigues(face):        #([[1,1,1],[2,2,2],[3,3,3]])
    #平面上三点
    x1=face[0][0]
    y1=face[0][1]
    z1=face[0][2]
    x2=face[1][0]
    y2=face[1][1]
    z2=face[1][2]
    x3=face[2][0]
    y3=face[2][1]
    z3=face[2][2]

    #平面法向量
    nx=(y2-y1)*(z3-z1)-(y3-y1)*(z2-z1)
    ny=(z2-z1)*(x3-x1)-(z3-z1)*(x2-x1)
    nz=(x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)

    #旋转角
    θ=math.acos(nz/math.sqrt(nx*nx+ny*ny+nz*nz))

    #旋转轴向量
    wx=ny
    wy=-nx
    wz=0
    l=math.sqrt(wx*wx+wy*wy+wz*wz)
    if l==0:
        wx=0
        wy=0
        wz=0
    else:
        wx=wx/l
        wy=wy/l
        wz=wz/l

    #罗德里格旋转矩阵
    cosθ=math.cos(θ)
    sinθ=math.sin(θ)
    matrix=[[cosθ+wx*wx*(1-cosθ),wx*wy*(1-cosθ)-wz*sinθ,wy*sinθ+wx*wz*(1-cosθ)],
            [wz*sinθ+wx*wy*(1-cosθ),cosθ+wy*wy*(1-cosθ),-wx*sinθ+wy*wz*(1-cosθ)],
            [-wy*sinθ+wx*wz*(1-cosθ),wx*sinθ+wy*wz*(1-cosθ),cosθ+wz*wz*(1-cosθ)]]
    rodrigues=np.mat(matrix)

    return rodrigues

def correct(face,pointlist):
    rodrigues=Rodrigues(face)
    newpointlist=[]
    pointnum=0
    for point in pointlist:
        pid=point.getPid()
        xyz=point.getXyz()
        rgb=point.getRgb()
        px=xyz[0]
        py=xyz[1]
        pz=xyz[2]
        newpvector=rodrigues*np.mat([[px],[py],[pz]])       #旋转变换作用于所有点上
        newpx=round(float(newpvector[0]),4)
        newpy=round(float(newpvector[1]),4)
        newpz=round(float(newpvector[2]),4)
        newpoint=classes.Point(pid,newpx,newpy,newpz,rgb[0],rgb[1],rgb[2])
        newpointlist.append(newpoint)
        pointnum+=1
        if pointnum%(len(pointlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已转换"+str(pointnum//(len(pointlist)//100))+"%点的坐标")
    return newpointlist

if __name__=="__main__":
    face=[[1,0,0],[0,123,123],[0,1,1]]
    correct(face,face)
    