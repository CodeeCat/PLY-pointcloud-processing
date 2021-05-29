def rgb2hsv(rgb):                   #RGB转HSV,参数是序列
    r=rgb[0]/255
    g=rgb[1]/255
    b=rgb[2]/255
    rgb_max=max(r,g,b)
    rgb_min=min(r,g,b)

    s=0                             #饱和度0-1
    if rgb_max==0:
        s=0
    else:
        s=(rgb_max-rgb_min)/rgb_max

    v=rgb_max                       #明度0-1

    h=1                             #色相0-360
    if rgb_max==rgb_min:
        h=0
    elif rgb_max==r and g>=b:
        h=60*((g-b)/(rgb_max-rgb_min))
    elif rgb_max==r and g<b:
        h=60*((g-b)/(rgb_max-rgb_min))+360
    elif rgb_max==g:
        h=60*((b-r)/(rgb_max-rgb_min))+120
    elif rgb_max==b:
        h=60*((r-g)/(rgb_max-rgb_min))+240
    return [h,s,v]

def isAInscope(A,scope):                     #scope=[a,c]
    if A>=min(scope) and A<=max(scope):
        return 1
    else: 
        return 0

def isHueInHscopes(Hue,Hscopes):            #Hscopes=[[a,b],[c,d]..]
    In=0
    for scope in Hscopes:
        if isAInscope(Hue,scope)!=0:
            In=1
    return In

def isHsvInScopes(hsv,scopes):               #hsv=[0,0,0],scopes={'h':[[75,165],[280,340]],'s':[0,1],'v':[0,1]}
    h=hsv[0]
    s=hsv[1]
    v=hsv[2]
    In=0
    if isHueInHscopes(h,scopes['h']) and isAInscope(s,scopes['s']) and isAInscope(v,scopes['v']):
        In=1
    return In
