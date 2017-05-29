import reconnaissanceplateau as rp
import cv2
import numpy as np



seuilrouge=50
seuilrl=60
seuilbleu=80
seuilvert=50
seuilrb=1.8
seuilrv=1.8
seuilbr=1.5
seuilbv=1.2
seuilvr=1.5
seuilvb=1.2
seuilchange=70
seuilnoir=45
seuilblanc=100


    

def occupe(test):
    if test>seuilchange:
        return 1
    elif test<-seuilchange:
        return -1
    return 0


    
    
def rotate(plat,ang):
    plat2=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    if ang==0:
        for i in range(8):
            for j in range(8):
                plat2[i][j]=plat[7-i][7-j]
        return plat2
    if ang==3:
        for i in range(8):
            for j in range(8):
                plat2[i][j]=plat[7-j][i]
        return plat2
    if ang==1:
        for i in range(8):
            for j in range(8):
                plat2[i][j]=plat[j][7-i]
        return plat2
    if ang==2:
        for i in range(8):
            for j in range(8):
                plat2[i][j]=plat[i][j]
        return plat2
    return plat
    

    
    
def partieimmobile():
    frame=rp.image()
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    moyennevide=rp.mcases(frame,pccs,dir1,dir2)
    frame=rp.image()
    posdep=rp.mcases(frame,pccs,dir1,dir2)
    occupation=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    test=occupation
    for i in range(8):
        for j in range(8):
            test[i][j]=posdep[i][j][0]+posdep[i][j][1]+posdep[i][j][2]-moyennevide[i][j][0]-moyennevide[i][j][1]-moyennevide[i][j][2]
    mot=0
    nbm=0
    for i in range(8):
        for j in range(8):
            test[i][j]=int(test[i][j])
            if abs(test[i][j])<seuilchange:
                mot+=test[i][j]
                nbm+=1
    mot=int(mot/nbm)
    for i in range(8):
        for j in range(8):
            test[i][j]-=mot
    print(test)
    for i in range(8):
        for j in range(8):
            occupation[i][j]=occupe(test[i][j])
    print('\n')
    for i in range(8):
        print(occupation[i])
    print('\n')
    testang=[occupation[0][0],occupation[0][7],occupation[7][7],occupation[7][0]]
    ang=-1
    if testang==[1,1,-1,-1]:
        ang=0
    if testang==[1,-1,-1,1]:
        ang=1
    if testang==[-1,-1,1,1]:
        ang=2
    if testang==[-1,1,1,-1]:
        ang=3
    assert(ang!=-1)
    print(ang)
    platp=[[-1,-2,-3,-4,-5,-3,-2,-1],[-6,-6,-6,-6,-6,-6,-6,-6],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[6,6,6,6,6,6,6,6],[1,2,3,4,5,3,2,1]]
    occupationp=rotate(occupation,ang)
    for i in range(8):
        print(occupationp[i])
    test=True
    while test:
        plat=platp
        for i in range(8):
            print(plat[i])
        frame=rp.image()
        pos=rp.mcases(frame,pccs,dir1,dir2)
        testpos=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        for i in range(8):
            for j in range(8):
                testpos[i][j]=0
                for k in range(3):
                    testpos[i][j]+=pos[i][j][k]-moyennevide[i][j][k]
        mot=0
        nbm=0
        for i in range(8):
            for j in range(8):
                if abs(testpos[i][j])<seuilchange:
                    mot+=testpos[i][j]
                    nbm+=1
        mot=mot/nbm
        for i in range(8):
            for j in range(8):
                testpos[i][j]=int(testpos[i][j]-mot)
        for i in range(8):
            for j in range(8):
                occupation[i][j]=occupe(testpos[i][j])
        occupationa=rotate(occupation,ang)
        for i in range(8):
            print(occupationa[i])
        for i in range(8):
            print(occupationp[i])
        cali=[]
        cach=[]
        for i in range(8):
            for j in range(8):
                if occupationp[i][j]!=occupationa[i][j]:
                    if occupationa[i][j]==0:
                        print("li")
                        cali.append([i,j])
                    if occupationa[i][j]!=0:
                        print("chan")
                        cach.append([i,j])
        if len(cali)==1:
            if len(cach)==1:
                print("un mouvement")
                plat[cach[0][0]][cach[0][1]]=plat[cali[0][0]][cali[0][1]]
                plat[cali[0][0]][cali[0][1]]=0
        if len(cali)==2:
            if len(cach)==2:
                if cali[0]==[0,0]:
                    if cali[1]==[0,4]:
                        plat[0][3]=plat[0][0]
                        plat[0][0]=0
                        plat[0][2]=plat[0][4]
                        plat[0][4]=0
                if cali[1]==[0,0]:
                    if cali[0]==[0,4]:
                        plat[0][3]=plat[0][0]
                        plat[0][0]=0
                        plat[0][2]=plat[0][4]
                        plat[0][4]=0
                if cali[0]==[0,7]:
                    if cali[1]==[0,4]:
                        plat[0][5]=plat[0][7]
                        plat[0][7]=0
                        plat[0][6]=plat[0][4]
                        plat[0][4]=0
                if cali[1]==[0,7]:
                    if cali[0]==[0,4]:
                        plat[0][5]=plat[0][7]
                        plat[0][7]=0
                        plat[0][6]=plat[0][4]
                        plat[0][4]=0
                if cali[0]==[7,0]:
                    if cali[1]==[7,4]:
                        plat[7][3]=plat[7][0]
                        plat[7][0]=0
                        plat[7][2]=plat[7][4]
                        plat[7][4]=0
                if cali[1]==[7,0]:
                    if cali[0]==[7,4]:
                        plat[7][3]=plat[7][0]
                        plat[7][0]=0
                        plat[7][2]=plat[7][4]
                        plat[7][4]=0
                if cali[0]==[7,7]:
                    if cali[1]==[7,4]:
                        plat[7][5]=plat[7][7]
                        plat[7][7]=0
                        plat[7][6]=plat[7][4]
                        plat[7][4]=0
                if cali[1]==[7,7]:
                    if cali[0]==[7,4]:
                        plat[7][5]=plat[7][7]
                        plat[7][7]=0
                        plat[7][6]=plat[7][4]
                        plat[7][4]=0
        platp=plat
        occupationp=occupationa
    return 1

    
    
def par():
    frame=rp.image()
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    moyennevide=rp.mcases(frame,pccs,dir1,dir2)
    frame=rp.image()
    posdep=rp.mcases(frame,pccs,dir1,dir2)
    occupation=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    test=occupation
    for i in range(8):
        for j in range(8):
            test[i][j]=posdep[i][j][0]+posdep[i][j][1]+posdep[i][j][2]-moyennevide[i][j][0]-moyennevide[i][j][1]-moyennevide[i][j][2]
    mot=0
    nbm=0
    for i in range(8):
        for j in range(8):
            test[i][j]=int(test[i][j])
            if abs(test[i][j])<seuilchange:
                mot+=test[i][j]
                nbm+=1
    mot=int(mot/nbm)
    for i in range(8):
        for j in range(8):
            test[i][j]-=mot
    print(test)
    for i in range(8):
        for j in range(8):
            occupation[i][j]=occupe(test[i][j])
    print('\n')
    for i in range(8):
        print(occupation[i])
    print('\n')
    testang=[occupation[0][0],occupation[0][7],occupation[7][7],occupation[7][0]]
    ang=-1
    if testang==[1,1,-1,-1]:
        ang=0
    if testang==[1,-1,-1,1]:
        ang=1
    if testang==[-1,-1,1,1]:
        ang=2
    if testang==[-1,1,1,-1]:
        ang=3
    assert(ang!=-1)
    print(ang)
    plat=[["a8","b8","c8","d8","e8","f8","g8","h8"],["a7","b7","c7","d7","e7","f7","g7","h7"],
          ["a6","b6","c6","d6","e6","f6","g6","h6"],["a5","b5","c5","d5","e5","f5","g5","h5"],
          ["a4","b4","c4","d4","e4","f4","g4","h4"],["a3","b3","c3","d3","e3","f3","g3","h3"],
          ["a2","b2","c2","d2","e2","f2","g2","h2"],["a1","b1","c1","d1","e1","f1","g1","h1"]]
    occupationp=rotate(occupation,ang)
    for i in range(8):
        print(occupationp[i])
    for i in range(8):
        print(plat[i])
    test=True
    coups=""
    while test:
        frame=rp.image()
        pos=rp.mcases(frame,pccs,dir1,dir2)
        testpos=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        for i in range(8):
            for j in range(8):
                testpos[i][j]=0
                for k in range(3):
                    testpos[i][j]+=pos[i][j][k]-moyennevide[i][j][k]
        mot=0
        nbm=0
        for i in range(8):
            for j in range(8):
                if abs(testpos[i][j])<seuilchange:
                    mot+=testpos[i][j]
                    nbm+=1
        mot=mot/nbm
        for i in range(8):
            for j in range(8):
                testpos[i][j]=int(testpos[i][j]-mot)
        for i in range(8):
            for j in range(8):
                occupation[i][j]=occupe(testpos[i][j])
        occupationa=rotate(occupation,ang)
        for i in range(8):
            print(occupationa[i])
        for i in range(8):
            print(occupationp[i])
        cali=[]
        cach=[]
        for i in range(8):
            for j in range(8):
                if occupationp[i][j]!=occupationa[i][j]:
                    if occupationa[i][j]==0:
                        print("li")
                        cali.append([i,j])
                    if occupationa[i][j]!=0:
                        print("chan")
                        cach.append([i,j])
        if len(cali)==1:
            if len(cach)==1:
                print("un mouvement")
                coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
        if len(cali)==2:
            if len(cach)==2:
                if cali[0]==[0,0]:
                    if cali[1]==[0,4]:
                        coups+=" e8c8"
                if cali[1]==[0,0]:
                    if cali[0]==[0,4]:
                        coups+=" e8c8"
                if cali[0]==[0,7]:
                    if cali[1]==[0,4]:
                        coups+=" e8g8"
                if cali[1]==[0,7]:
                    if cali[0]==[0,4]:
                        coups+=" e8g8"
                if cali[0]==[7,0]:
                    if cali[1]==[7,4]:
                        coups+=" e1c1"
                if cali[1]==[7,0]:
                    if cali[0]==[7,4]:
                        coups+=" e1c1"
                if cali[0]==[7,7]:
                    if cali[1]==[7,4]:
                        coups+=" e1g1"
                if cali[1]==[7,7]:
                    if cali[0]==[7,4]:
                        coups+=" e1g1"
        occupationp=occupationa
        print("position startpos moves"+coups+'\n')
    return 1
    
    
    
def parlong():
    frame=rp.image()
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    moyennevide=rp.mcases(frame,pccs,dir1,dir2)
    frame=rp.image()
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    posdep=rp.mcases(frame,pccs,dir1,dir2)
    occupation=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    test=occupation
    for i in range(8):
        for j in range(8):
            test[i][j]=posdep[i][j][0]+posdep[i][j][1]+posdep[i][j][2]-moyennevide[i][j][0]-moyennevide[i][j][1]-moyennevide[i][j][2]
    mot=0
    nbm=0
    for i in range(8):
        for j in range(8):
            test[i][j]=int(test[i][j])
            if abs(test[i][j])<seuilchange:
                mot+=test[i][j]
                nbm+=1
    mot=int(mot/nbm)
    for i in range(8):
        for j in range(8):
            test[i][j]-=mot
    print(test)
    for i in range(8):
        for j in range(8):
            occupation[i][j]=occupe(test[i][j])
    print('\n')
    for i in range(8):
        print(occupation[i])
    print('\n')
    testang=[occupation[0][0],occupation[0][7],occupation[7][7],occupation[7][0]]
    ang=-1
    if testang==[1,1,-1,-1]:
        ang=0
    if testang==[1,-1,-1,1]:
        ang=1
    if testang==[-1,-1,1,1]:
        ang=2
    if testang==[-1,1,1,-1]:
        ang=3
    assert(ang!=-1)
    print(ang)
    plat=[["a8","b8","c8","d8","e8","f8","g8","h8"],["a7","b7","c7","d7","e7","f7","g7","h7"],
          ["a6","b6","c6","d6","e6","f6","g6","h6"],["a5","b5","c5","d5","e5","f5","g5","h5"],
          ["a4","b4","c4","d4","e4","f4","g4","h4"],["a3","b3","c3","d3","e3","f3","g3","h3"],
          ["a2","b2","c2","d2","e2","f2","g2","h2"],["a1","b1","c1","d1","e1","f1","g1","h1"]]
    occupationp=rotate(occupation,ang)
    for i in range(8):
        print(occupationp[i])
    for i in range(8):
        print(plat[i])
    test=True
    coups=""
    while test:
        frame=rp.image()
        [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
        pos=rp.mcases(frame,pccs,dir1,dir2)
        testpos=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        for i in range(8):
            for j in range(8):
                testpos[i][j]=0
                for k in range(3):
                    testpos[i][j]+=pos[i][j][k]-moyennevide[i][j][k]
        mot=0
        nbm=0
        for i in range(8):
            for j in range(8):
                if abs(testpos[i][j])<seuilchange:
                    mot+=testpos[i][j]
                    nbm+=1
        mot=mot/nbm
        for i in range(8):
            for j in range(8):
                testpos[i][j]=int(testpos[i][j]-mot)
        for i in range(8):
            for j in range(8):
                occupation[i][j]=occupe(testpos[i][j])
        occupationa=rotate(occupation,ang)
        for i in range(8):
            print(occupationa[i])
        for i in range(8):
            print(occupationp[i])
        cali=[]
        cach=[]
        for i in range(8):
            for j in range(8):
                if occupationp[i][j]!=occupationa[i][j]:
                    if occupationa[i][j]==0:
                        print("li")
                        cali.append([i,j])
                    if occupationa[i][j]!=0:
                        print("chan")
                        cach.append([i,j])
        if len(cali)==1:
            if len(cach)==1:
                print("un mouvement")
                coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
        if len(cali)==2:
            if len(cach)==2:
                if cali[0]==[0,0]:
                    if cali[1]==[0,4]:
                        coups+=" e8c8"
                if cali[1]==[0,0]:
                    if cali[0]==[0,4]:
                        coups+=" e8c8"
                if cali[0]==[0,7]:
                    if cali[1]==[0,4]:
                        coups+=" e8g8"
                if cali[1]==[0,7]:
                    if cali[0]==[0,4]:
                        coups+=" e8g8"
                if cali[0]==[7,0]:
                    if cali[1]==[7,4]:
                        coups+=" e1c1"
                if cali[1]==[7,0]:
                    if cali[0]==[7,4]:
                        coups+=" e1c1"
                if cali[0]==[7,7]:
                    if cali[1]==[7,4]:
                        coups+=" e1g1"
                if cali[1]==[7,7]:
                    if cali[0]==[7,4]:
                        coups+=" e1g1"
        occupationp=occupationa
        print("position startpos moves"+coups+'\n')
    return 1

    
    
    
    
    
    
    
    
    
    
    
    
    
    
def occuper(test):
    oc=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    for i in range(8):
        for j in range(8):
            if test[i][7-j]<seuilnoir:
                oc[i][j]=-1
            if test[i][7-j]>seuilblanc:
                oc[i][j]=1
    return oc
    
    
    

    
        
    
    
    
    
def part():
    frame=rp.image()
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    posdep=rp.mcases(frame,pccs,dir1,dir2)
    test=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    for i in range(8):
        for j in range(8):
            test[i][j]=posdep[i][j][0]*0.1+posdep[i][j][1]*0.6+posdep[i][j][2]*0.3
    occupation=occuper(test)
    print('\n')
    for i in range(8):
        print(occupation[i])
    print('\n')
    testang=[occupation[0][0],occupation[0][7],occupation[7][7],occupation[7][0]]
    ang=-1
    if testang==[1,1,-1,-1]:
        ang=0
    if testang==[1,-1,-1,1]:
        ang=1
    if testang==[-1,-1,1,1]:
        ang=2
    if testang==[-1,1,1,-1]:
        ang=3
    assert(ang!=-1)
    print(ang)
    plat=[["a8","b8","c8","d8","e8","f8","g8","h8"],["a7","b7","c7","d7","e7","f7","g7","h7"],
          ["a6","b6","c6","d6","e6","f6","g6","h6"],["a5","b5","c5","d5","e5","f5","g5","h5"],
          ["a4","b4","c4","d4","e4","f4","g4","h4"],["a3","b3","c3","d3","e3","f3","g3","h3"],
          ["a2","b2","c2","d2","e2","f2","g2","h2"],["a1","b1","c1","d1","e1","f1","g1","h1"]]
    occupationp=rotate(occupation,ang)
    for i in range(8):
        print(occupationp[i])
    for i in range(8):
        print(plat[i])
    test=True
    coups=""
    while test:
        frame=rp.image()
        pos=rp.mcases(frame,pccs,dir1,dir2)
        testpos=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        for i in range(8):
            for j in range(8):
                testpos[i][j]=pos[i][j][0]*0.1+pos[i][j][1]*0.6+pos[i][j][2]*0.3
        occupation=occuper(testpos)
        occupationa=rotate(occupation,ang)
        for i in range(8):
            print(occupationa[i])
        for i in range(8):
            print(occupationp[i])
        cali=[]
        cach=[]
        for i in range(8):
            for j in range(8):
                if occupationp[i][j]!=occupationa[i][j]:
                    if occupationa[i][j]==0:
                        print("li")
                        cali.append([i,j])
                    if occupationa[i][j]!=0:
                        print("chan")
                        cach.append([i,j])
        if len(cali)==1:
            if len(cach)==1:
                print("un mouvement")
                coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
        if len(cali)==2:
            if len(cach)==2:
                if cali[0]==[0,0]:
                    if cali[1]==[0,4]:
                        coups+=" e8c8"
                if cali[1]==[0,0]:
                    if cali[0]==[0,4]:
                        coups+=" e8c8"
                if cali[0]==[0,7]:
                    if cali[1]==[0,4]:
                        coups+=" e8g8"
                if cali[1]==[0,7]:
                    if cali[0]==[0,4]:
                        coups+=" e8g8"
                if cali[0]==[7,0]:
                    if cali[1]==[7,4]:
                        coups+=" e1c1"
                if cali[1]==[7,0]:
                    if cali[0]==[7,4]:
                        coups+=" e1c1"
                if cali[0]==[7,7]:
                    if cali[1]==[7,4]:
                        coups+=" e1g1"
                if cali[1]==[7,7]:
                    if cali[0]==[7,4]:
                        coups+=" e1g1"
        occupationp=occupationa
        print("position startpos moves"+coups+'\n')
    return 1
    
    
    
    
    
    
    
    
    
    
def occuper2(test, countn, countb):
    valeurs=[]
    for i in range(64):
        valeurs.append(test[i//8][i%8])
    valeurs.sort()
    a=0
    for i in range(max(1,countn-1)):
        a+=valeurs[i]
    a=a/countn
    b=0
    for i in range(max(1,countb-1)):
        b+=valeurs[63-i]
    b=b/countb
    c=0
    for i in range(64-countn-countb):
        c+=valeurs[countn+i]
    c=c/(64-countn-countb)
    oc=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    v1=(a+c)/2
    v2=(b+c)/2
    for i in range(8):
        for j in range(8):
            if test[i][7-j]<v1:
                oc[i][j]=-1
            if test[i][7-j]>v2:
                oc[i][j]=1
    return oc
    
   
    
    
    
    
    
def testcases(mcases):
    mat=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    for i in range(8):
        for j in range(8):
            mat[i][j]=mcases[i][j][0]*0.1+mcases[i][j][1]*0.6+mcases[i][j][2]*0.3
    return mat

    
    
def bleu(pt):
    if pt[0]>seuilbleu and pt[0]>pt[1]*seuilbv and pt[0]>seuilbr*pt[2]:
        return True
    return False

    
    
def vert(pt):
    if pt[1]>seuilvert and pt[1]>seuilvb*pt[0] and pt[1]>pt[2]*seuilvr:
        return True
    return False
    
    
    
    
    
def occuper3(mcases):
    mat=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    for i in range(8):
        for j in range(8):
            if (not bleu(mcases[i][j])) and (not vert(mcases[i][j])):
                if mcases[i][j][0]*0.1+mcases[i][j][1]*0.6+mcases[i][j][2]*0.3<seuilnoir:
                    mat[i][j]=-1
                else:
                    mat[i][j]=1
    return mat
    
def libre(pt):
    if pt[2]>seuilrl:
        if pt[2]*seuilbr<pt[0] or pt[2]*seuilvr<pt[1]:
            return True
    return False
    
def occuper4(mcases):
    mat=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    for i in range(8):
        for j in range(8):
            if not libre(mcases[i][j]):
                if mcases[i][j][0]*0.1+mcases[i][j][1]*0.6+mcases[i][j][2]*0.3<seuilnoir:
                    mat[i][7-j]=-1
                if mcases[i][j][0]*0.1+mcases[i][j][1]*0.6+mcases[i][j][2]*0.3>seuilblanc:
                    mat[i][7-j]=1
    return mat
    
    
    
def part2():
    frame=rp.image()
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    posdep=rp.mcases(frame,pccs,dir1,dir2)
    test=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    for i in range(8):
        for j in range(8):
            test[i][j]=posdep[i][j][0]*0.1+posdep[i][j][1]*0.6+posdep[i][j][2]*0.3
    countn=16
    countb=16
    occupation=occuper2(test,countn,countb)
    print('\n')
    for i in range(8):
        print(occupation[i])
    print('\n')
    testang=[occupation[0][0],occupation[0][7],occupation[7][7],occupation[7][0]]
    ang=-1
    if testang==[1,1,-1,-1]:
        ang=0
    if testang==[1,-1,-1,1]:
        ang=1
    if testang==[-1,-1,1,1]:
        ang=2
    if testang==[-1,1,1,-1]:
        ang=3
    assert(ang!=-1)
    print(ang)
    plat=[["a8","b8","c8","d8","e8","f8","g8","h8"],["a7","b7","c7","d7","e7","f7","g7","h7"],
          ["a6","b6","c6","d6","e6","f6","g6","h6"],["a5","b5","c5","d5","e5","f5","g5","h5"],
          ["a4","b4","c4","d4","e4","f4","g4","h4"],["a3","b3","c3","d3","e3","f3","g3","h3"],
          ["a2","b2","c2","d2","e2","f2","g2","h2"],["a1","b1","c1","d1","e1","f1","g1","h1"]]
    occupationp=rotate(occupation,ang)
    for i in range(8):
        print(occupationp[i])
    for i in range(8):
        print(plat[i])
    test=True
    coups=""
    while test:
        frame=rp.image()
        pos=rp.mcases(frame,pccs,dir1,dir2)
        testpos=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
        for i in range(8):
            for j in range(8):
                testpos[i][j]=pos[i][j][0]*0.1+pos[i][j][1]*0.6+pos[i][j][2]*0.3
        occupation=occuper2(testpos,countn,countb)
        occupationa=rotate(occupation,ang)
        for i in range(8):
            print(occupationa[i])
        for i in range(8):
            print(occupationp[i])
        cali=[]
        cach=[]
        for i in range(8):
            for j in range(8):
                if occupationp[i][j]!=occupationa[i][j]:
                    if occupationa[i][j]==0:
                        print("li")
                        cali.append([i,j])
                    if occupationa[i][j]!=0:
                        print("chan")
                        cach.append([i,j])
        if len(cali)==1:
            if len(cach)==1:
                print("un mouvement")
                coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
                if occupationp[cach[0][0]][cach[0][1]]==-1:
                    countn-=1
                if occupationp[cach[0][0]][cach[0][1]]==1:
                    countb-=1
        if len(cali)==2:
            if len(cach)==2:
                if cali[0]==[0,0]:
                    if cali[1]==[0,4]:
                        coups+=" e8c8"
                if cali[1]==[0,0]:
                    if cali[0]==[0,4]:
                        coups+=" e8c8"
                if cali[0]==[0,7]:
                    if cali[1]==[0,4]:
                        coups+=" e8g8"
                if cali[1]==[0,7]:
                    if cali[0]==[0,4]:
                        coups+=" e8g8"
                if cali[0]==[7,0]:
                    if cali[1]==[7,4]:
                        coups+=" e1c1"
                if cali[1]==[7,0]:
                    if cali[0]==[7,4]:
                        coups+=" e1c1"
                if cali[0]==[7,7]:
                    if cali[1]==[7,4]:
                        coups+=" e1g1"
                if cali[1]==[7,7]:
                    if cali[0]==[7,4]:
                        coups+=" e1g1"
        occupationp=occupationa
        print("position startpos moves"+coups+'\n')
        print(countn)
        print(countb)
    return 1

    
    
def part2long():
    frame=rp.image()
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    frame2=frame
    for i in range(8):
        for j in range(8):
            rp.colorier(frame2,pccs[i][j],[0,0,255])
    cv2.imshow("frame2",frame2)
    posdep=rp.mcases(frame,pccs,dir1,dir2)
#    test=testcases(posdep)
#    countn=16
#    countb=16
#    occupation=occuper2(test,countn,countb)
    occupation=occuper4(posdep)
    print('\n')
    for i in range(8):
        print(occupation[i])
    print('\n')
    testang=[occupation[0][0],occupation[0][7],occupation[7][7],occupation[7][0]]
    ang=-1
    if testang==[1,1,-1,-1]:
        ang=0
    if testang==[1,-1,-1,1]:
        ang=1
    if testang==[-1,-1,1,1]:
        ang=2
    if testang==[-1,1,1,-1]:
        ang=3
    assert(ang!=-1)
    print(ang)
    plat=[["a8","b8","c8","d8","e8","f8","g8","h8"],["a7","b7","c7","d7","e7","f7","g7","h7"],
          ["a6","b6","c6","d6","e6","f6","g6","h6"],["a5","b5","c5","d5","e5","f5","g5","h5"],
          ["a4","b4","c4","d4","e4","f4","g4","h4"],["a3","b3","c3","d3","e3","f3","g3","h3"],
          ["a2","b2","c2","d2","e2","f2","g2","h2"],["a1","b1","c1","d1","e1","f1","g1","h1"]]
    occupationp=rotate(occupation,ang)
    for i in range(8):
        print(occupationp[i])
    for i in range(8):
        print(plat[i])
    test=True
    coups=""
    while test:
        frame=rp.image()
        [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
        frame2=frame
        for i in range(8):
            for j in range(8):
                rp.colorier(frame2,pccs[i][j],[0,0,255])
        cv2.imshow("frame2",frame2)
        pos=rp.mcases(frame,pccs,dir1,dir2)
#        testpos=testcases(pos)
#        occupation=occuper2(testpos,countn,countb)
        occupation=occuper4(pos)
        occupationa=rotate(occupation,ang)
        for i in range(8):
            print(occupationa[i])
        for i in range(8):
            print(occupationp[i])
        cali=[]
        cach=[]
        for i in range(8):
            for j in range(8):
                if occupationp[i][j]!=occupationa[i][j]:
                    if occupationa[i][j]==0:
                        print("li")
                        cali.append([i,j])
                    if occupationa[i][j]!=0:
                        print("chan")
                        cach.append([i,j])
        if len(cali)==1:
            if len(cach)==1:
                print("un mouvement")
                coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
#                if occupationp[cach[0][0]][cach[0][1]]==-1:
#                    countn-=1
#                if occupationp[cach[0][0]][cach[0][1]]==1:
#                    countb-=1
        if len(cali)==2:
            if len(cach)==2:
                if cali[0]==[0,0]:
                    if cali[1]==[0,4]:
                        coups+=" e8c8"
                if cali[1]==[0,0]:
                    if cali[0]==[0,4]:
                        coups+=" e8c8"
                if cali[0]==[0,7]:
                    if cali[1]==[0,4]:
                        coups+=" e8g8"
                if cali[1]==[0,7]:
                    if cali[0]==[0,4]:
                        coups+=" e8g8"
                if cali[0]==[7,0]:
                    if cali[1]==[7,4]:
                        coups+=" e1c1"
                if cali[1]==[7,0]:
                    if cali[0]==[7,4]:
                        coups+=" e1c1"
                if cali[0]==[7,7]:
                    if cali[1]==[7,4]:
                        coups+=" e1g1"
                if cali[1]==[7,7]:
                    if cali[0]==[7,4]:
                        coups+=" e1g1"
        occupationp=occupationa
        print("position startpos moves"+coups+'\n')
#        print(countn)
#        print(countb)
    return 1