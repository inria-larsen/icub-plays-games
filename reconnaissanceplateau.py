import prisephoto
import numpy as np
import cv2


def ima():
    filename=input("filename : ")
    frame=cv2.imread(filename)
    mir=255
    miv=255
    mib=255
    mar=0
    mav=0
    mab=0
    for x in range(len(frame)):
        for y in range(len(frame[x])):
            if mir>frame[x][y][2]:
                mir=frame[x][y][2]
            if miv>frame[x][y][1]:
                miv=frame[x][y][1]
            if mib>frame[x][y][0]:
                mib=frame[x][y][0]
            if mab<frame[x][y][0]:
                mab=frame[x][y][0]
            if mav<frame[x][y][1]:
                mav=frame[x][y][1]
            if mar<frame[x][y][2]:
                mar=frame[x][y][2]
    for x in range(len(frame)):
        for y in range(len(frame[x])):
            frame[x][y]=[(frame[x][y][0]-mib)*255/(mab-mib),(frame[x][y][1]-miv)*255/(mav-miv),(frame[x][y][2]-mir)*255/(mar-mir)]
    return(frame)




def image():
    frame=prisephoto.photo()
    mir=255
    miv=255
    mib=255
    mar=0
    mav=0
    mab=0
    for x in range(len(frame)):
        for y in range(len(frame[x])):
            if mir>frame[x][y][2]:
                mir=frame[x][y][2]
            if miv>frame[x][y][1]:
                miv=frame[x][y][1]
            if mib>frame[x][y][0]:
                mib=frame[x][y][0]
            if mab<frame[x][y][0]:
                mab=frame[x][y][0]
            if mav<frame[x][y][1]:
                mav=frame[x][y][1]
            if mar<frame[x][y][2]:
                mar=frame[x][y][2]
    for x in range(len(frame)):
        for y in range(len(frame[x])):
            frame[x][y]=[(frame[x][y][0]-mib)*255/(mab-mib),(frame[x][y][1]-miv)*255/(mav-miv),(frame[x][y][2]-mir)*255/(mar-mir)]
    return(frame)

    
    
    
def isrouge(pt,seuilrouge,seuilrb,seuilrv):
    if pt[2]>seuilrouge:
        if pt[2]>seuilrv*pt[1]:
            if pt[2]>seuilrb*pt[0]:
                return True
    return False

    
    
    
def ptsrouges(frame,seuilrouge,seuilrb,seuilrv):
    pts=[]
    for x in range(len(frame)):
        for y in range(len(frame[x])):
            pt=frame[x][y]
            if isrouge(pt,seuilrouge,seuilrb,seuilrv):
                pts.append([x,y])
    return pts

    
    


def centre(pts):
    n=len(pts)
    centrex=0
    centrey=0
    for i in range(len(pts)):
        centrex+=pts[i][0]
        centrey+=pts[i][1]
    centrex=int(centrex/n)
    centrey=int(centrey/n)
    return [centrex,centrey]




def direction(pt1,pt2):
    return [pt1[0]-pt2[0],pt1[1]-pt2[1]]



def distance(pt1,pt2):
    dire=direction(pt1,pt2)
    return (dire[0]**2+dire[1]**2)

    
    
def ppp(pts,pt):
    d=distance(pt,pts[0])
    idx=0
    for i in range(len(pts)):
        d2=distance(pt,pts[i])
        if d2<d:
            d=d2
            idx=i
    return idx

    
    
def ali(pts,pt,dir1):
    ptali=[]
    for i in range(len(pts)):
        dir2=direction(pt,pts[i])
        if abs(dir1[0]*dir2[1]-dir1[1]*dir2[0])<0.01*np.sqrt(distance(pt,[0,0])*distance(pts[i],[0,0])):
            ptali.append(pts[i])
    return ptali

    
    
def perp(pts,pt,dir1):
    ptperp=[]
    for i in range(len(pts)):
        dir2=direction(pt,pts[i])
        if abs(dir1[0]*dir2[0]+dir1[1]*dir2[1])<0.01*np.sqrt(distance(pt,[0,0])*distance(pts[i],[0,0])):
            ptperp.append(pts[i])
    return ptperp

    

def opp(pts,pt,dir1):
    ptopp=[]
    for i in range(len(pts)):
        dir2=direction(pt,pts[i])
        if dir1[0]*dir2[0]+dir1[1]*dir2[1]<0:
            ptopp.append(pts[i])
    return ptopp

    

def moyenne(pts):
    n=len(pts)
    p=[0,0,0]
    for i in range(n):
        p[0]+=pts[i][0]
        p[1]+=pts[i][1]
        p[2]+=pts[i][2]
    p[0]=p[0]/n
    p[1]=p[1]/n
    p[2]=p[2]/n
    return p
    
    
    
    
def plateau(frame,seuilrouge,seuilrb,seuilrv):
    prs=ptsrouges(frame,seuilrouge,seuilrb,seuilrv)
    pc=centre(prs)
    pu1=prs[ppp(prs,pc)]
    dir1=direction(pc,pu1)
    al=ali(prs,pc,dir1)
    op=opp(al,pc,dir1)
    pu2=op[ppp(op,pc)]
    pc2=centre([pu1,pu2])
    #dir1=direction(pc2,pu1)
    dir1=[int((pu2[0]-pu1[0])/2),int((pu2[1]-pu1[1])/2)]
    pe=perp(prs,pc2,dir1)
    pu3=pe[ppp(pe,pc2)]
    dir2=direction(pc2,pu3)
    op2=opp(pe,pc2,dir2)
    pu4=op2[ppp(op2,pc2)]
    pc3=centre([pu3,pu4])
    #dir2=direction(pc3,pu3)
    dir2=[int((pu4[0]-pu3[0])/2),int((pu4[1]-pu3[1])/2)]
    if (abs(dir1[0])>abs(dir2[0])):
        (dir1,dir2)=(dir2,dir1)
    if dir1[1]<0:
        dir1[0]=-dir1[0]
        dir1[1]=-dir1[1]
    if dir2[0]<0:
        dir2[0]=-dir2[0]
        dir2[1]=-dir2[1]
    pccs=[[],[],[],[],[],[],[],[]]
    for i in range(8):
        for j in range(8):
            pccs[i].append([int(pc3[0]-dir1[0]-dir2[0]+((i+0.5)*dir1[0]+dir2[0]*(j+0.5))*0.25),int(pc3[1]-dir1[1]-dir2[1]+((i+0.5)*dir1[1]+dir2[1]*(j+0.5))*0.25)])
    return [pccs,dir1,dir2]




def mcases(frame,pccs,dir1,dir2):
    mcs=[[],[],[],[],[],[],[],[]]
    #tc=int(np.sqrt(min(distance(dir1,[0,0]),distance(dir2,[0,0])))/8)
    tc=int(np.sqrt(distance(dir1,dir2)/2)/8)
    for i in range(8):
        for j in range(8):
            case=[]
            for x in range(tc*2):
                for y in range(tc*2):
                    case.append(frame[pccs[i][j][0]-tc+x][pccs[i][j][1]-tc+y])
            mcs[i].append(moyenne(case))
    return mcs
            
    

    
def colorier(frame,pt,couleur):
    for i in range(5):
        for j in range(5):
            frame[pt[0]-2+i][pt[1]-2+j]=couleur
    return 1

