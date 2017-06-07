import prisephoto
import numpy as np
import cv2



def image():#prend une photo
    frame=prisephoto.photo()
    mir=255#minimum de rouge
    miv=255#minimum de vert
    mib=255#minimum de bleu
    mar=0#maximum de rouge
    mav=0#maximu de vert
    mab=0#maximum de bleu
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
#redimensionnement des couleurs pour utiliser une gamme plus large et augmenter les differences
    return(frame)

    
    
    
def isrouge(pt,seuilrouge,seuilrb,seuilrv):#determine si un pixel est rouge
    if pt[2]>seuilrouge:#suffisamment de rouge
        if pt[2]>seuilrv*pt[1]:#plus de rouge que de vert
            if pt[2]>seuilrb*pt[0]:#plus de rouge que de bleu
                return True
    return False

    
    
    
def ptsrouges(frame,seuilrouge,seuilrb,seuilrv):#liste des points rouges de la frame
    pts=[]
    for x in range(len(frame)):
        for y in range(len(frame[x])):
            pt=frame[x][y]
            if isrouge(pt,seuilrouge,seuilrb,seuilrv):
                pts.append([x,y])
    return pts

    
    


def centre(pts):#barycentre des points pts
    n=len(pts)#nombre de points
    centrex=0#coordonnee x du barycentre
    centrey=0#coordonnee y du barycentre
    for i in range(len(pts)):
        centrex+=pts[i][0]
        centrey+=pts[i][1]
    centrex=int(centrex/n)
    centrey=int(centrey/n)
    return [centrex,centrey]




def direction(pt1,pt2):#vecteur allant du point pt2 au point pt1
    return [pt1[0]-pt2[0],pt1[1]-pt2[1]]



def distance(pt1,pt2):#distance au carre entre deux points en pixels carres
    dire=direction(pt1,pt2)
    return (dire[0]**2+dire[1]**2)

    
    
def ppp(pts,pt):#determine parmi les points pts lequel est le plus proche du point pt
    d=distance(pt,pts[0])
    idx=0
    for i in range(len(pts)):
        d2=distance(pt,pts[i])
        if d2<d:
            d=d2
            idx=i
    return idx

    
    
def ali(pts,pt,dir1):#determine l'ensemble des points parmi pts qui sont dans la direction du vecteur dir1 a partir du point pt
    ptali=[]
    for i in range(len(pts)):
        dir2=direction(pt,pts[i])
        if abs(dir1[0]*dir2[1]-dir1[1]*dir2[0])<0.01*np.sqrt(distance(pt,[0,0])*distance(pts[i],[0,0])):
            ptali.append(pts[i])
    return ptali

    
    
def perp(pts,pt,dir1):#determine l'ensemble des points parmi pts qui sont dans la direction perpendiculaire a dir1 a partir du point pt
    ptperp=[]
    for i in range(len(pts)):
        dir2=direction(pt,pts[i])
        if abs(dir1[0]*dir2[0]+dir1[1]*dir2[1])<0.01*np.sqrt(distance(pt,[0,0])*distance(pts[i],[0,0])):
            ptperp.append(pts[i])
    return ptperp

    

def opp(pts,pt,dir1):#determine l'ensemble des points parmi pts qui sont dans la direction opposee a dir1 depuis le point pt
    ptopp=[]
    for i in range(len(pts)):
        dir2=direction(pt,pts[i])
        if dir1[0]*dir2[0]+dir1[1]*dir2[1]<0:
            ptopp.append(pts[i])
    return ptopp

    

def moyenne(pts):#calcule la couleur moyenne des points pts
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
    
    
    
    
def plateau(frame,seuilrouge,seuilrb,seuilrv):#detection de l'echiquier
    prs=ptsrouges(frame,seuilrouge,seuilrb,seuilrv)#ensemble des points rouges
    frame2=frame
    for i in range(len(prs)):
        frame2[prs[i][0]][prs[i][1]]=[255,0,255]
    pc=centre(prs)#premiere approximation du centre
    pu1=prs[ppp(prs,pc)]
    dir1=direction(pc,pu1)
    al=ali(prs,pc,dir1)
    op=opp(al,pc,dir1)
    pu2=op[ppp(op,pc)]
    pc2=centre([pu1,pu2])#deuxieme approximation du centre
    dir1=[int((pu2[0]-pu1[0])/2),int((pu2[1]-pu1[1])/2)]#premier vecteur
    pe=perp(prs,pc2,dir1)
    pu3=pe[ppp(pe,pc2)]
    dir2=direction(pc2,pu3)
    op2=opp(pe,pc2,dir2)
    pu4=op2[ppp(op2,pc2)]
    pc3=centre([pu3,pu4])#derniere approximation du centre
    dir2=[int((pu4[0]-pu3[0])/2),int((pu4[1]-pu3[1])/2)]#deuxieme vecteur
    if (abs(dir1[0])>abs(dir2[0])):
        (dir1,dir2)=(dir2,dir1)#premier vecteur vertical et deuxieme horizontal
    if dir1[1]<0:#si le vecteur est vers le bas
        dir1[0]=-dir1[0]
        dir1[1]=-dir1[1]
    if dir2[0]<0:#si le vecteur est vers la gauche
        dir2[0]=-dir2[0]
        dir2[1]=-dir2[1]
    pccs=[[],[],[],[],[],[],[],[]]# tableau repertoriant les positions des cases
    for i in range(8):
        for j in range(8):
            pccs[i].append([int(pc3[0]-dir1[0]-dir2[0]+((i+0.5)*dir1[0]+dir2[0]*(j+0.5))*0.25),int(pc3[1]-dir1[1]-dir2[1]+((i+0.5)*dir1[1]+dir2[1]*(j+0.5))*0.25)])
    for i in range(8):
        for j in range(8):
            colorier(frame2,pccs[i][j],[0,0,255])
    cv2.imshow("frame2",frame2)
    return [pccs,dir1,dir2]




def mcases(frame,pccs,dir1,dir2):#calcul des couleurs moyennes de chaque case
    mcs=[[],[],[],[],[],[],[],[]]#tableau a renvoyer
    tc=int(np.sqrt(distance(dir1,dir2)/2)/12)#taille du demi-carre autour du centre de la case
    for i in range(8):
        for j in range(8):
            case=[]
            for x in range(tc*2):
                for y in range(tc*2):
                    case.append(frame[pccs[i][j][0]-tc+x][pccs[i][j][1]-tc+y])
            mcs[i].append(moyenne(case))
    return mcs
            
    

 
    

    
    
def colorier(frame,pt,couleur):#colorie un petit carre autour du point pt
    for i in range(5):
        for j in range(5):
            frame[pt[0]-2+i][pt[1]-2+j]=couleur
    return 1

