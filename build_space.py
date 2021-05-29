import numpy as np
import time
import tools
import classes
import sys

def openFile():                                                        #读取配置文件和点云并返回文件头和点云数据                                           #点云文件名称
    cloudname=str(sys.argv[1])
    pointformat=str(sys.argv[2])
    pointcloud=open(file=cloudname,mode='r',encoding='utf-8')
    pointlines=pointcloud.readlines()
    headline=1
    for line in pointlines:
        if line=="end_header\n":
            break
        headline+=1
    head=pointlines[:headline]                                         #文件头
    points=pointlines[headline:]                                       #点云数据
    print(time.asctime(time.localtime(time.time()))+"  Log:  点云读取结果:一共"+str(len(points))+"个点--------")
    pointcloud.close()
    return [head,points,pointformat]

def point2List(filedata):                                              #通过读取文件数据返回pointlist和最小长方体包围盒
    points=filedata[1]
    pointformat=filedata[2]
    pointlist=[]
    xindex=pointformat.find('x')
    yindex=pointformat.find('y')
    zindex=pointformat.find('z')
    rindex=pointformat.find('r')
    gindex=pointformat.find('g')
    bindex=pointformat.find('b')
    xmax=float(points[0].split()[xindex])
    ymax=float(points[0].split()[yindex])
    zmax=float(points[0].split()[zindex])
    xmin=float(points[0].split()[xindex])
    ymin=float(points[0].split()[yindex])
    zmin=float(points[0].split()[zindex])
    pointnum=0
    for point in points:
        x=float(point.split()[xindex])
        y=float(point.split()[yindex])
        z=float(point.split()[zindex])
        r=int(point.split()[rindex])
        g=int(point.split()[gindex])
        b=int(point.split()[bindex])
        p=classes.Point(len(pointlist),x,y,z,r,g,b)
        pointlist.append(p)
        if x>xmax:
            xmax=x
        if x<xmin:
            xmin=x
        if y>ymax:
            ymax=y
        if y<ymin:
            ymin=y
        if z>zmax:
            zmax=z
        if z<zmin:
            zmin=z
        pointnum+=1
        if pointnum%(len(points)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已将"+str(pointnum//(len(points)//100))+"%的点数据写入列表")
    print(time.asctime(time.localtime(time.time()))+"  Log:  所有点数据已写入列表--------")
    return [pointlist,xmax,xmin,ymax,ymin,zmax,zmin]

def buildGrid(filedatas,L):                                         #建立空间关系，返回栅格list和栅格空间位置
    pointlist=filedatas[0]
    xmax=filedatas[1]
    xmin=filedatas[2]
    ymax=filedatas[3]
    ymin=filedatas[4]
    zmax=filedatas[5]
    zmin=filedatas[6]
    gridx=int((xmax-xmin)//L)+3                                     #+1保证所有点都能录入栅格，+2保证所有非空栅格都有26个邻域
    gridy=int((ymax-ymin)//L)+3
    gridz=int((zmax-zmin)//L)+3
    gridspace=np.empty([gridx,gridy,gridz],dtype=int)               #栅格空间，存放对应位置的栅格id
    for x in range(gridx):
        for y in range(gridy):
            for z in range(gridz):
                gridspace[x][y][z]=-1                               #用-1填充space，避免和gid(>=0)冲突
        print(time.asctime(time.localtime(time.time()))+"  Log:  已创建空栅格"+str(x)+'/'+str(gridx))
    gridlist=[]                                                     #栅格list，存放非空栅格对象

    pointnum=0
    for point in pointlist:                                         #将点放到对应栅格，将栅格对应到栅格空间
        xyz=point.getXyz()
        x=int((xyz[0]-xmin)//L)+1                                   #点所属的栅格坐标，0栅格不放点
        y=int((xyz[1]-ymin)//L)+1
        z=int((xyz[2]-zmin)//L)+1
        gid=gridspace[x][y][z]
        if gid==-1:                                                 #如果栅格没有数据
            g=classes.Grid(len(gridlist),x,y,z)                     #创建新的栅格
            point.setIdOfGrid(g.getGid())                           #将栅格序号添加到点
            g.pointList.append(point.getPid())                      #将点序号添加到对应栅格
            gridlist.append(g)                                      #将栅格添加到list
            gridspace[x][y][z]=g.getGid()                           #将栅格添加到space
        else:
            gridlist[gid].pointList.append(point.getPid())          #将点序号添加到对应栅格
            point.setIdOfGrid(gridlist[gid].getGid())               #将栅格序号添加到点
        pointnum+=1
        if pointnum%(len(pointlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已将"+str(pointnum//(len(pointlist)//100))+"%的点录入栅格")
        
    gridnum=0
    for grid in gridlist:                                       #标记出每个栅格的非空邻域栅格
        xyz=grid.getXyz()
        x=xyz[0]
        y=xyz[1]
        z=xyz[2]
        for i in range(-1,1,1):                                 #遍历26个邻域
            for j in range(-1,1,1):
                for k in range(-1,1,1):
                    if i==0 and j==0 and k==0:                  #跳过自己
                        continue
                    if gridspace[x+i][y+j][z+k]!=-1:
                        grid.neighbourList.append(gridspace[x+i][y+j][z+k])
        gridnum+=1
        if gridnum%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已找到"+str(gridnum//(len(gridlist)//100))+"%栅格的非空邻域")


    return {"gridlist":gridlist,"gridspace":gridspace}

def getPointStruct(L):
    filedata=openFile()                         #[head,points,pointformat]
    filedatas=point2List(filedata)              #[pointlist,xmax,xmin,ymax,ymin,zmax,zmin]
    pointlist=filedatas[0]

    '''
    i=input("是否计算点云密度？（y/n）")
    if i=='y':
        print("点云密度："+str(len(pointlist)//len(buildGrid(filedatas,1)["gridlist"]))+"个点每单位栅格")
    conti=input("继续操作？（y/n）")
    if conti=='y':
        build=buildGrid(filedatas,L)      #[gridlist,gridspace]
        gridlist=build["gridlist"]
        gridspace=build["gridspace"]

        print(time.asctime(time.localtime(time.time()))+"  Log:  点云空间已建立---------------")
        return {"pointlist":pointlist,"gridlist":gridlist,"gridspace":gridspace}
    else:
        sys.exit(0)
    '''
    build=buildGrid(filedatas,L)      #[gridlist,gridspace]
    gridlist=build["gridlist"]
    gridspace=build["gridspace"]

    print(time.asctime(time.localtime(time.time()))+"  Log:  点云空间已建立---------------")
    return {"pointlist":pointlist,"gridlist":gridlist,"gridspace":gridspace}