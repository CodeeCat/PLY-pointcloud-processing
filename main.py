import keep_color as kc
import build_space as bs
import time
import cloud_tools as ct
import delete_noise as dn
import subsampled as sub
import coordinate_correction as cc

'''
程序入口--------------------------------------------------------------------------------------------
'''
if __name__=="__main__":
    print("--------------------"+time.asctime(time.localtime(time.time()))+"--------------------")
    L=1           #栅格边长
    struct=bs.getPointStruct(L)     #{"pointlist":pointlist,"gridlist":gridlist,"gridspace":gridspace}
    pointlist=struct["pointlist"]
    gridlist=struct["gridlist"]
    gridspace=struct["gridspace"]

    
##################### keep color 和L取值有关
    '''
    colorthreshold=10            #色点阈值
    scopes={'h':[[70,150]],'s':[0,1],'v':[0,1]}
    kc.keepColor(colorthreshold,scopes,pointlist,gridlist,gridspace)
    newname='k-h'+str(scopes['h'])+'s'+str(scopes['s'])+'v'+str(scopes['v'])+'L'+str(L)
    '''

##################### delete color 和L取值无关
    
    
    scopes={'h':[[0,360]],'s':[0,0.3],'v':[0.6,1]}
    kc.deleteColor(scopes, pointlist, gridlist, gridspace)
    newname='d-h'+str(scopes['h'])+'s'+str(scopes['s'])+'v'+str(scopes['v'])+'L'+str(L)
    
    
##################### delete noise 和L取值有关
    '''
    noisethreshold=500            #噪点阈值，小于该值就删除
    dn.deleteNoise(noisethreshold, gridlist, gridspace)
    newname='S'+str(noisethreshold)+'L'+str(L)
    '''
    
##################### subSampled 和L取值有关，形成新的point
    '''
    newpointlist=sub.subSampled(pointlist,gridlist)
    newname='sub'+'L'+str(L)
    '''

##################### randomSampled 和L取值无关
    '''
    ratio=0.2
    sub.randomSampled(ratio, gridlist)
    newname='sub'+'R'+str(ratio)
    '''

##################### coordiante correction
    '''
    face=[[-14.4798,17.5725,-2.0584],[-5.1785,5.7330,-1.15560],[-5.6869,12.0677,-1.6969]]
    newpointlist=cc.correct(face,pointlist)
    newname="旋转"
    '''
##################### generateNewCloud

    newpointlist=ct.generateRestPoint(gridspace,gridlist,pointlist)
    ct.generateNewCloud(newpointlist, newname)
    