import time
import tools

def keepColor(colorthreshold,scopes,pointlist,gridlist,gridspace):                 #参数[色点个数阈值，hsv区间，点的字符串序列，点的列表，栅格列表，栅格空间]
    canopynum=0
    for grid in gridlist:                                                   #标记出树冠
        keeppoint=0                                                         #指定颜色点的个数
        for point in grid.pointList:
            if tools.isHsvInScopes(pointlist[point].getHsv(),scopes):  #如果点的色相属于给定的范围
                keeppoint+=1
        if keeppoint>colorthreshold:                                                 #如果指定颜色的点大于规定数量
            grid.iscanopy=1
        canopynum+=1
        if canopynum%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已统计"+str(canopynum//(len(gridlist)//100))+"%的树冠")

    trunknum=0
    for grid in gridlist:                                                   #标记出树干
        if grid.iscanopy==0:
            for gidup in gridspace[grid.getXyz()[0]][grid.getXyz()[1]][grid.getXyz()[2]:]:      #如果栅格上面的栅格是树冠
                if gridlist[gidup].iscanopy==1:
                    grid.istrunk=1
        trunknum+=1
        if trunknum%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已统计"+str(trunknum//(len(gridlist)//100))+"%的树干")

    gridtodelet=0
    for grid in gridlist:
        xyz=grid.getXyz()
        if grid.iscanopy==0 and grid.istrunk==0:                              #栅格如果不是树冠也不是树干就将栅格id从空间移除(=-1)
            gridspace[xyz[0]][xyz[1]][xyz[2]]=-1
        gridtodelet+=1
        if gridtodelet%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已将"+str(gridtodelet//(len(gridlist)//100))+"%的非植被栅格删除")


def deleteColor(scopes,pointlist,gridlist,gridspace):
    gridnum=0
    for grid in gridlist:
        xyz=grid.getXyz()
        pointstodelete=[]
        for pid in grid.pointList:                                      #倒叙遍历栅格的点列表，找到指定的颜色点并从list中移除
            if tools.isHsvInScopes(pointlist[pid].getHsv(),scopes):
                pointstodelete.append(pid)
        for pid in pointstodelete:
            grid.pointList.remove(pid)
        if len(grid.pointList)==0:                                                              #删除结束验证栅格是否为空
            gridspace[xyz[0]][xyz[1]][xyz[2]]=-1
        gridnum+=1
        if gridnum%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已将"+str(gridnum//(len(gridlist)//100))+"%的异色点删除")