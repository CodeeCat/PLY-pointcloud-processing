import time

def deleteNoise(noisethreshold,gridlist,gridspace):
    gridnum=0
    for grid in gridlist:
        xyz=grid.getXyz()
        x=xyz[0]
        y=xyz[1]
        z=xyz[2]
        if len(grid.pointList)<noisethreshold:                  #如果该栅格点数小于阈值
            if len(grid.neighbourList)==0:                       #且没有非空邻域
                gridspace[x][y][z]=-1
            else:
                for neighbourid in grid.neighbourList:           #如果有邻域则考察邻域的阈值
                    if len(gridlist[neighbourid].pointList)<noisethreshold:
                        gridspace[x][y][z]=-1
        gridnum+=1
        if gridnum%(len(gridlist)//100)==0:
            print(time.asctime( time.localtime(time.time()))+"  Log:  已将"+str(gridnum//(len(gridlist)//100))+"%的噪点栅格删除")