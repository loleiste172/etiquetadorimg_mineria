###############   ARCHIVO DE PRUEBA PERSONAL, IGNORAR
###############   ARCHIVO DE PRUEBA PERSONAL, IGNORAR
###############   ARCHIVO DE PRUEBA PERSONAL, IGNORAR
###############   ARCHIVO DE PRUEBA PERSONAL, IGNORAR
###############   ARCHIVO DE PRUEBA PERSONAL, IGNORAR
###############   ARCHIVO DE PRUEBA PERSONAL, IGNORAR

from math import floor
import numpy as np
import os
import cv2
import numpy as np
#img=cv2.imread("C:/Users/j_lal/Desktop/imgprueba/Proyecto.png")
def load(ruta:str):
    img = cv2.imread(ruta)
    #img=imutils.resize(img, height=180)
    img=cv2.resize(img, (1062,594))
    #img=imutils.resize(img, width=280)
    #Rearrang the color channel
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    return img

matriz3d=[
    [[0, 5, 6],
    [2, 3, 6],
    [9, 7, 2]],

    [[8, 6, 4],
    [2, 8, 7],
    [0, 0, 8]],

    [[3, 4, 2],
    [6, 3, 8],
    [7, 2, 2]]
    ]

def ubicaciones(num_act:int):
    ubics=[]
    matriz_eleccion=[
        [0,118,236,354,472,590],
        [0,212,424,636,848,1060]
    ]
    real=num_act+1
    res=floor(real/5)
    resid=real%5
    xmin=matriz_eleccion[0][res]
    xmax=matriz_eleccion[0][res+1]+1
    ymin=matriz_eleccion[1][resid-1]
    ymax=matriz_eleccion[1][resid]+1
    ubics.append(xmin)
    ubics.append(xmax)
    ubics.append(ymin)
    ubics.append(ymax)
    return ubics


def prom_matriz(matriz,dimension):
    suma=0
    filas=len(matriz)
    columnas=len(matriz[0])
    if(dimension>2):
        return 0
    for i in range(0, filas):
        for j in range(0, columnas):
            suma=suma+matriz[i][j][dimension]
    
    prom=suma/(filas*columnas)
    return prom
        

def clear(): 
    os.system('cls')


clear()
a = np.array(range(50)).reshape(5,10)
clear()

for i in a:
    print(i)



i=load("C:/Users/j_lal/Desktop/imgprueba/Proyecto.png")

e=i[50:520,180:520]

cv2.imshow('logo',e)
cv2.waitKey(0)
cv2.destroyAllWindows()
#print(a[1:3, 4:7])

#prueba=ubicaciones(8)

#print("["+str(prueba[0])+":"+str(prueba[1])+","+str(prueba[2])+":"+str(prueba[3])+"]")

#ase=prom_matriz(matriz3d,2)

#print(ase)


