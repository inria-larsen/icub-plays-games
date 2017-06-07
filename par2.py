import reconnaissanceplateau as rp


#seuils pour la detection des pixels rouges:
seuilrouge=75
seuilrb=1.5
seuilrv=1.5




    
#fonction renvoyant la matrice d'occupation:
def occupe(pa,cn,cb):#pa est un tableau tridimensionnel representant la couleur moyenne de chaque case.
#                     cn est le nombre de piece noires presentes sur l'echiquier a la fin du coup precedent
#                     cb est le nombre de pieces blanches presentes sur l'echiquier a la fin du coup precedent
    oc=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
#oc est la matrice d'occupation a remplir puis a renvoyer
    sb=[]#tableau dont les valeurs triees permettront d'etablir un seuil pour detecter les pieces blanches
    sn=[]#tableau dont les valeurs triees permettront d'etablir un seuil pour detecter les pieces noires
    for i in range(8):
        for j in range(8):
            sb.append(pa[i][j][2])#ajout de la composante rouge de la case
            sn.append(pa[i][j][2])#ajout de la composante rouge de la case
    sb.sort(reverse=True)
    sn.sort()
    sbl=(sb[cb]+sb[max(cb-2,0)])/2#seuil de detection des pieces blanches
    sno=(sn[cn]+sn[max(cn-2,0)])/2#seuil de detection des pieces noires
    for i in range(8):
        for j in range(8):
            if pa[i][j][2]>sbl:#si la case est occupee par une piece blanche
                oc[i][7-j]=1
            if pa[i][j][2]<sno:#si la case est occupee par une piece noire
                oc[i][7-j]=-1
    return oc


    
#fonction de rotation pour bien orienter la matrice d'occupation
def rotate(plat,ang):#plat est la matrice a orienter
#                     ang correspond a la rotation a effectuer
    plat2=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
#plat2 est la matrice d'occupation orientee renvoyee par cette fonction
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




frame=rp.image()#prise de la photo
[pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)#reconnaissance de l'echiquier
posdep=rp.mcases(frame,pccs,dir1,dir2)#definition des couleurs moyennes des cases
cn=16#initialisation du nombre de pieces noires presentes sur l'echiquier
cb=16#initialisation du nombre de pieces blanches presentes sur l'echiquier
occupation=occupe(posdep,cn,cb)#matrice d'occupation
#
#definition de l'angle pour faire correspondre les cases avec leurs noms:
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
plat=[["a8","b8","c8","d8","e8","f8","g8","h8"],["a7","b7","c7","d7","e7","f7","g7","h7"],
      ["a6","b6","c6","d6","e6","f6","g6","h6"],["a5","b5","c5","d5","e5","f5","g5","h5"],
      ["a4","b4","c4","d4","e4","f4","g4","h4"],["a3","b3","c3","d3","e3","f3","g3","h3"],
      ["a2","b2","c2","d2","e2","f2","g2","h2"],["a1","b1","c1","d1","e1","f1","g1","h1"]]
#plat est la matrice contenant le nom des cases
occupationp=rotate(occupation,ang)#occupationp sert de reference pour trouver le coup joue
test=True#variable qui pourrait servir pour arreter la boucle while
coups=""
while test:
    frame=rp.image()#prise d'une nouvelle photo
    [pccs,dir1,dir2]=rp.plateau(frame,seuilrouge,seuilrb,seuilrv)
    pos=rp.mcases(frame,pccs,dir1,dir2)
    occupation=occupe(pos,cn,cb)
    occupationa=rotate(occupation,ang)#occupationa est comparee a occupationp pour trouver le coup joue
    cali=[]#liste des cases passant d'un etat occupe a un etat vide
    cach=[]#liste des autres cases changeant d'etat
    for i in range(8):
        for j in range(8):
            if occupationp[i][j]!=occupationa[i][j]:#si l'etat d'occupation change
                if occupationa[i][j]==0:#si la case est vide
                    cali.append([i,j])
                if occupationa[i][j]!=0:#si la case est occupee
                    cach.append([i,j])
    if len(cali)==1:
        if len(cach)==1:
            coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
#ajout du coup joue a la liste des coups de la partie
            if occupationp[cach[0][0]][cach[0][1]]==-1:#si une piece noire est prise
                cn-=1
            if occupationp[cach[0][0]][cach[0][1]]==1:#si une piece blanche est prise
                cb-=1
    if len(cali)==2:
        if len(cach)==2:#on va tester si les cases sont compatibles avec un roque
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
        if len(cach)==1:#on va tester si les cases sont compatibles avec la prise en passant
            if cali[0][0]==cali[1][0] and abs(cali[0][1]-cali[1][1])==1:
                ctest=False#booleen indiquant si une prise en passant est realisee
                if cach[0][0]==cali[0][0]+1:
                    if cach[0][1]==cali[0][1]:
                        coups+=' '+plat[cali[1][0]][cali[1][1]]+plat[cach[0][0]][cach[0][1]]
                        ctest=True
                    if cach[0][1]==cali[1][1]:
                        coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
                        ctest=True
                if cach[0][0]==cali[0][0]-1:
                    if cach[0][1]==cali[0][1]:
                        coups+=' '+plat[cali[1][0]][cali[1][1]]+plat[cach[0][0]][cach[0][1]]
                        ctest=True
                    if cach[0][1]==cali[1][1]:
                        coups+=' '+plat[cali[0][0]][cali[0][1]]+plat[cach[0][0]][cach[0][1]]
                        ctest=True
                if ctest:
                    if occupationa[cach[0][0]][cach[0][1]]==1:#si une piece noir est prise
                        cn-=1
                    if occupationa[cach[0][0]][cach[0][1]]==-1:#si une piece blanche est prise
                        cb-=1
    occupationp=occupationa#la matrice d'occupation devient la reference pour le coup suivant
    print("position startpos moves"+coups+'\n')