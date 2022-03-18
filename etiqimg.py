#imports
from math import floor
from tkinter import *
import os
from tkinter import messagebox
import tkinter
from tkinter.filedialog import askdirectory, askopenfilename
import cv2
from matplotlib import image
import numpy as np
from PIL import Image
from PIL import ImageTk
import imutils
from skimage.feature import graycomatrix, graycoprops
import sys
sys.path.insert(0, 'C:/Users/coco_/Desktop/semestre 6/Mineria de datos/PrimerParcial/etiquetadorimg_mineria')
from funciones import pxmy_calc, glcm_contrast, glcm_stat_calc, glcm_correlation, glcm_homogeneity, glcm_energy, glcm_entropy, glcm_entropy_calc, get_glcms, quant_img , glcm_diffentropy, glcm_asm,  glcm_variance
#Funcion para obtener la particion
def particion(imagen,canal):
    #creamos una matriz para saber la posicion del cuadro seleccionado EJEMPLO los cuadros van del 0 al 24, si se selecciona el 24 estas en la pocicion 5,5 
    lugares=[[1,1],[2,1],[3,1],[4,1],[5,1],[1,2],[2,2],[3,2],[4,2],[5,2],[1,3],[2,3],[3,3],[4,3],[5,3],[1,4],[2,4],[3,4],[4,4],[5,4],[1,5],[2,5],[3,5],[4,5],[5,5]]
    lugar = lugares[contadorceldas]
    lugx = lugar[0]
    lugy = lugar[1]
    #calculando desviacion estandar de R
    #Obtenemos las dimensiones de la imagen original
    tamOiginal = imgOriginal.size/3
    anchoOriginal = int(imgOriginal.shape[1])
    alturaOriginal = int(imgOriginal.shape[0])
    
    #calculamos cuanto vale cada particion
    x = int(anchoOriginal/5)
    y = int(alturaOriginal/5)

    #Creamos la matriz vacia y un auxiliar para llenarla
    #La matrizR se llenara de una lista de listas
    matrizR = []
    #La matrizlineal es el valor de todos los pixeles pero en una sola lista, ya que las funciones de desviacion estandar predefinida solo acepta las listas asi
    matrizRLineal = []
    aux = []
    #este ciclo nos ayuda a llenar dos matrices, una de manera lineal y otra de manera de matriz
    #sabemos que la pocicion de los pixeles esta dado por filas y columnas empezando del 0
    #EL primer ciclo recorre las filas (Y) EJEMPLO la altura de tu imagen es de 500 pixeles, entonces se dividio entre 5, cada particion contiene 100 pixeles
    #si estamos en la posicion (1,1) de nuestra particion entonces el rango de Y es del 0 al 99, si estamos en la posicion (1,2) entonces el rango de Y es del 100 al 199
    #NOTA: LA FUNCION RANGE EMPIEZA DESDE EL CERO AL NUMERO ANTERIOR ESPECIFICADO
    if canal == 3:
        imageGp = imagen[y*(lugy-1):y*lugy, x*(lugx-1):x*lugx]
        return imageGp
    else:
        for fila in range(0+(y*(lugy-1)),y*lugy):
        #El segundo cilo aplica la misma teoria solo que para el eje X (las columnas)
            for columna in range(0+(x*(lugx-1)),x*lugx):
                aux.append(int(imagen[fila][columna][canal]))
                matrizRLineal.append(int(imagen[fila][columna][canal]))
            matrizR.append(aux)
            aux = []
        return matrizR, matrizRLineal

#Funcion para obtener una imagen en gris en cada particion
def MCG():
    #0-Entropia0, 1-Entropia45, 2-Entropia90, 3-Entropia135, 4-correlacion0, 5-correlacion45, 6-correlacion90, 7-correlacion135, 8-Energia0, 9-Energia45, 10-Energia90, 11-Energia135
    # 12-homogeneidad0, 13-homogeneidad45, 14-homogeneidad90, 15-homogeneidad135, 16-asm0, 17-asm45, 18-asm90, 19-asm135, 20-contraste, 21-contraste, 22-contraste, 23-contraste, 24-27 disimilitud
    datos = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    imgGray = cv2.cvtColor(imgO,cv2.COLOR_BGR2GRAY)
    imageGp = particion(imgGray, 3)
    glcm_dict = get_glcms(imageGp, levels=256, dist = 2)
    #glcm_dictM = get_glcms(imageGp, levels=32, dist = 2)
    glcm0 = graycomatrix(imageGp, distances=[2], angles=[0], levels=256, symmetric=True, normed=True) 
    glcm45 = graycomatrix(imageGp, distances=[2], angles=[45], levels=256, symmetric=True, normed=True) 
    glcm90 = graycomatrix(imageGp, distances=[2], angles=[90], levels=256, symmetric=True, normed=True) 
    glcm135 = graycomatrix(imageGp, distances=[2], angles=[135], levels=256, symmetric=True, normed=True) 
    datos[0],  datos[1],  datos[2],  datos[3]= glcm_entropy(glcm_dict, 256)
    datos[4] = graycoprops(glcm0, 'correlation')[0][0]
    datos[5] = graycoprops(glcm45, 'correlation')[0][0]
    datos[6] = graycoprops(glcm90, 'correlation')[0][0]
    datos[7] = graycoprops(glcm135, 'correlation')[0][0]
    datos[8] = graycoprops(glcm0, 'energy')[0][0]
    datos[9] = graycoprops(glcm45, 'energy')[0][0]
    datos[10] = graycoprops(glcm90, 'energy')[0][0]
    datos[11] = graycoprops(glcm135, 'energy')[0][0]
    #datos[8],  datos[9],  datos[10],  datos[11] = glcm_energy(glcm_dict, 256)
    datos[12] = graycoprops(glcm0, 'homogeneity')[0][0]
    datos[13] = graycoprops(glcm45, 'homogeneity')[0][0]
    datos[14] = graycoprops(glcm90, 'homogeneity')[0][0]
    datos[15] = graycoprops(glcm135, 'homogeneity')[0][0]
    #datos[12],  datos[13],  datos[14],  datos[15] = glcm_homogeneity(glcm_dict, 256)
    datos[16] = graycoprops(glcm0, 'ASM')[0][0]
    datos[17] = graycoprops(glcm45, 'ASM')[0][0]
    datos[18] = graycoprops(glcm90, 'ASM')[0][0]
    datos[19] = graycoprops(glcm135, 'ASM')[0][0]
    #datos[16],  datos[17],  datos[18],  datos[19] = glcm_asm(glcm_dict, 256)
    datos[20] = graycoprops(glcm0, 'contrast')[0][0]
    datos[21] = graycoprops(glcm45, 'contrast')[0][0]
    datos[22] = graycoprops(glcm90, 'contrast')[0][0]
    datos[23] = graycoprops(glcm135, 'contrast')[0][0]
    #datos[20],  datos[21],  datos[22],  datos[23] = glcm_contrast(glcm_dictM, 32)
    datos[24] = graycoprops(glcm0, 'dissimilarity')[0][0]
    datos[25] = graycoprops(glcm45, 'dissimilarity')[0][0]
    datos[26] = graycoprops(glcm90, 'dissimilarity')[0][0]
    datos[27] = graycoprops(glcm135, 'dissimilarity')[0][0]

    #contrasteH = glcm_contrast(glcm_dict, 256)
    #diffentropyH = glcm_diffentropy(glcm_dict, 256)
    
    return datos
    #print("Correlacion de Haralick: " + str(correlacionH))
    #print("Entropia de Haralick: " + str(entropiaH))

## Funcion para obtener la desviacion estandar de un conjunto de datos
def tendenciaCentral(canal):
    #Mandamos a llamar el metodo para llenar nuestras dos variables
    matrizR, matrizRLineal = particion(imgOriginal, canal)

    #calculamos la media de manera manual
    elementos = 0
    sumatoria = 0
    for fila in matrizR:
        for elemento in fila:
            sumatoria += elemento
            elementos += 1

    #mediaR = sumatoria / elementos

    #calculamos la media y desviacion estandar con las funciones predefinidas
    #global desEstandar
    #global mediaR
    desEstandar = np.std(matrizRLineal)
    mediaR = np.mean(matrizRLineal)
    return desEstandar, mediaR



#funciones basicas
#funcion para transformar imagen de la ruta en array y transformarla en algo entendible para PIL, no habia camino intermedio me temo
#no sirve si lo pongo en otro metodo por separado por alguna razon (USA LOAD)
def paso1(ruta:str):
    im=Image.fromarray(load(ruta))
    return im
#funcion para transformar image de PIL a imagen entendible para tkinter
def paso2(cosa):
    imgtk=ImageTk.PhotoImage(image=cosa)
    return imgtk


#funcion para actualizar la funcion del cuadrado
def updcuadrado():
    if(contadorceldas==0):
        global cuadradoselec
        cuadradoselec=cvs_img.create_rectangle(0,0, 212, 118, outline="green", width=5)
    else:
        if(contadorceldas==5 or contadorceldas==10 or contadorceldas==15 or contadorceldas==20):
            cvs_img.move(cuadradoselec, -848, 118)
        else:
            cvs_img.move(cuadradoselec, 212, 0)
    
#importante: convertir la imagen de una ruta a un string
def load(ruta:str):
    if(len(ruta)>0):
        img = cv2.imread(ruta)
        #creando una variable global de la imagen original
        global imgOriginal
        imgOriginal = cv2.imread(ruta)
        global imgO 
        imgO = cv2.imread(ruta)
        imgOriginal = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
        #img=imutils.resize(img, height=180)
        img=cv2.resize(img, (1060,590))
        #img=imutils.resize(img, width=280)
        #Rearrang the color channel
        b,g,r = cv2.split(img)
        img = cv2.merge((r,g,b))
        return img
#promedio matriz
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
#funcion para saber los rangos para obtener la matriz dependiendo de la celda revisada
#devuelve una matriz: [0]: x minimo, [1]: x maximo, [2] y minimo, [3] y maximo
def ubicaciones(num_act:int):
    ubics=[]
    m_alto=int(imgOriginal.shape[0])/5
    m_ancho=int(imgOriginal.shape[1])/5
    listax=[0]
    listay=[0]

    for al in range(6):
        aux=0
        aux=m_alto*al
        listay.append(aux)

    for an in range(6):
        aux2=0
        aux2=m_ancho*an
        listax.append(aux2)

    matriz_eleccion=[]

    matriz_eleccion.append(listay)
    matriz_eleccion.append(listax)

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
    
#funcion para no ver compilaciones anteriores que nos puedan confundir
def clear(): 
    os.system('cls')

#funcion para actualizar la imagen actual dentro del canvas
def actualizar(ruta:str):
    global res
    res=paso2(paso1(ruta))
    cvs_img.itemconfig(contenedor_img, image=res)

#funcion para actualizar la ruta actual de la foto
def updruta():
    lista_fotos=os.listdir(ruta_carpeta)
    ruta_act=ruta_carpeta+"/"+lista_fotos[int(pant_cont.get())]
    return ruta_act


#funcion para obtener la carpeta deseada
def abrircarpeta():
    global ruta_carpeta
    ruta_carpeta=askdirectory(title="Seleccionar carpeta con imagenes")
    lista_fotos=os.listdir(ruta_carpeta)
    ruta_foto_act=ruta_carpeta+"/"+lista_fotos[int(pant_cont.get())]
    return ruta_foto_act

#funcion al dar click en abrir carpeta
def abrir_click():
    ruta_foto_act=abrircarpeta()
    actualizar(ruta_foto_act)
    dibujargrid()
    updcuadrado()


#funcion para dibujar grid
def dibujargrid():
    for i in range(0,1061,212):
        cvs_img.create_line(i,0,i,590)
    
    for j in range(0,591,118):
        cvs_img.create_line(0,j,1060,j)



#vars
ruta_carpeta="" #global para ruta carpeta
ruta_foto_act="" #global para ruta de la foto actual
lista_fotos=[] #global para los contenidos de la carpeta seleccionada



#resto funciones

#funcion para ejecutarse al dar click a fuego
def fuego_click():
    global contadorceldas #numero del la ubicacion del cuadro verde
    txt_pasado.config(text="fuego")
    #descriptores (obtencion)

    #recort=ubicaciones(contadorceldas)
    #PARTICION DE IMAGEN,A PARTIR DE AHORA MATR_IMG TIENE LA PARTICION DE LA IMAGEN ORIGINAL SIN REDIMENSIONAR
    #matr_img=imgOriginal[int(recort[0]):int(recort[1]),int(recort[2]):int(recort[3])]

    #OBTENCION DE PROMEDIO
    #promr=prom_matriz(matr_img,0)
    #promg=prom_matriz(matr_img,1)
    #promb=prom_matriz(matr_img,2)



    #(escribir datos obtenidos)
    #f=open(txt_dest.get(), "a")
    #f.write(str(promr)+","+str(promg)+","+str(promb)+",fuego")
    #f.close()
    #fin descriptores
    desEstandarR, mediaR = tendenciaCentral(0)
    desEstandarG, mediaG = tendenciaCentral(1)
    desEstandarB, mediaB = tendenciaCentral(2)
    descriptores = MCG()
    #matrizCon = GLCM()
    
    #(escribir datos obtenidos) es "a" ya que con eso me permite agregar informacion sin eliminar lo que ya tenia
    f=open(txt_dest.get(), "a")
    try:
        # Procesamiento para escribir en el fichero
        f.write(str(mediaR) + ',' + str(desEstandarR) + ',' + str(mediaG) + ',' + str(desEstandarG) + ',' + str(mediaB) + ',' + str(desEstandarB) + ',' + str(descriptores[0]) + ',' + str(descriptores[1]) + ',' + str(descriptores[2]) + ',' + str(descriptores[3]) + ',' + str(descriptores[4]) + ',' + str(descriptores[5]) + ',' + str(descriptores[6]) + ',' + str(descriptores[7]) + ',' + str(descriptores[8]) + ',' + str(descriptores[9]) + ',' + str(descriptores[10]) + ',' + str(descriptores[11]) + ',' + str(descriptores[12]) + ',' + str(descriptores[13]) + ',' + str(descriptores[14]) + ',' + str(descriptores[15]) + ',' + str(descriptores[16]) + ',' + str(descriptores[17]) + ',' + str(descriptores[18]) + ',' + str(descriptores[19])+ ',' + str(descriptores[20]) + ',' + str(descriptores[21]) + ',' + str(descriptores[22]) + ',' + str(descriptores[23]) + ',' + str(descriptores[24]) + ',' + str(descriptores[25]) + ',' + str(descriptores[26]) + ',' + str(descriptores[27])  + ', 1' + '\n')
    finally:
        f.close()

    contadorceldas=contadorceldas+1
    if(contadorceldas>=25):
        contadorceldas=0
        num_actual=int(pant_cont.get())
        num_actual=num_actual+1
        pant_cont.delete(0, 'end')
        pant_cont.insert(0, num_actual)
        nruta=updruta()
        actualizar(nruta)
        cvs_img.move(cuadradoselec, -848, -472)
    else:
        updcuadrado()


#funcion del boton humo############
def humo_click():
    txt_pasado.config(text="humo")
    #descriptores
    #llamando a la funcion de desviacion estandar
    desEstandarR, mediaR = tendenciaCentral(0)
    desEstandarG, mediaG = tendenciaCentral(1)
    desEstandarB, mediaB = tendenciaCentral(2)
    descriptores = MCG()
    #matrizCon = GLCM()
    
    #(escribir datos obtenidos) es "a" ya que con eso me permite agregar informacion sin eliminar lo que ya tenia
    f=open(txt_dest.get(), "a")
    try:
        # Procesamiento para escribir en el fichero
        f.write(str(mediaR) + ',' + str(desEstandarR) + ',' + str(mediaG) + ',' + str(desEstandarG) + ',' + str(mediaB) + ',' + str(desEstandarB) + ',' + str(descriptores[0]) + ',' + str(descriptores[1]) + ',' + str(descriptores[2]) + ',' + str(descriptores[3]) + ',' + str(descriptores[4]) + ',' + str(descriptores[5]) + ',' + str(descriptores[6]) + ',' + str(descriptores[7]) + ',' + str(descriptores[8]) + ',' + str(descriptores[9]) + ',' + str(descriptores[10]) + ',' + str(descriptores[11]) + ',' + str(descriptores[12]) + ',' + str(descriptores[13]) + ',' + str(descriptores[14]) + ',' + str(descriptores[15]) + ',' + str(descriptores[16]) + ',' + str(descriptores[17]) + ',' + str(descriptores[18]) + ',' + str(descriptores[19])+ ',' + str(descriptores[20]) + ',' + str(descriptores[21]) + ',' + str(descriptores[22]) + ',' + str(descriptores[23])+ ',' + str(descriptores[24]) + ',' + str(descriptores[25]) + ',' + str(descriptores[26]) + ',' + str(descriptores[27])  + ', 0' + '\n')
    finally:
        f.close()

    #fin descriptores
    global contadorceldas
    contadorceldas=contadorceldas+1
    if(contadorceldas>=25):
        contadorceldas=0
        num_actual=int(pant_cont.get())
        num_actual=num_actual+1
        pant_cont.delete(0, 'end')
        pant_cont.insert(0, num_actual)
        nruta=updruta()
        actualizar(nruta)
        cvs_img.move(cuadradoselec, -848, -472)
    else:
        updcuadrado()


#funcion al dar click al boton nada
def nada_click():
    txt_pasado.config(text="no inc. / vacio")
    #descriptores

    desEstandarR, mediaR = tendenciaCentral(0)
    desEstandarG, mediaG = tendenciaCentral(1)
    desEstandarB, mediaB = tendenciaCentral(2)
    descriptores = MCG()
    #matrizCon = GLCM()
    
    #(escribir datos obtenidos) es "a" ya que con eso me permite agregar informacion sin eliminar lo que ya tenia
    f=open(txt_dest.get(), "a")
    try:
        # Procesamiento para escribir en el fichero
        f.write(str(mediaR) + ',' + str(desEstandarR) + ',' + str(mediaG) + ',' + str(desEstandarG) + ',' + str(mediaB) + ',' + str(desEstandarB) + ',' + str(descriptores[0]) + ',' + str(descriptores[1]) + ',' + str(descriptores[2]) + ',' + str(descriptores[3]) + ',' + str(descriptores[4]) + ',' + str(descriptores[5]) + ',' + str(descriptores[6]) + ',' + str(descriptores[7]) + ',' + str(descriptores[8]) + ',' + str(descriptores[9]) + ',' + str(descriptores[10]) + ',' + str(descriptores[11]) + ',' + str(descriptores[12]) + ',' + str(descriptores[13]) + ',' + str(descriptores[14]) + ',' + str(descriptores[15]) + ',' + str(descriptores[16]) + ',' + str(descriptores[17]) + ',' + str(descriptores[18]) + ',' + str(descriptores[19])+ ',' + str(descriptores[20]) + ',' + str(descriptores[21]) + ',' + str(descriptores[22]) + ',' + str(descriptores[23])+ ',' + str(descriptores[24]) + ',' + str(descriptores[25]) + ',' + str(descriptores[26]) + ',' + str(descriptores[27])  + ', 2' + '\n')
    finally:
        f.close()

    #(escribir datos obtenidos)
#    f=open(txt_dest.get(), "w")
#    f.close()
    #fin descriptores
    global contadorceldas
    contadorceldas=contadorceldas+1
    if(contadorceldas>=25):
        contadorceldas=0
        num_actual=int(pant_cont.get())
        num_actual=num_actual+1
        pant_cont.delete(0, 'end')
        pant_cont.insert(0, num_actual)
        nruta=updruta()
        actualizar(nruta)
        cvs_img.move(cuadradoselec, -848, -472)
    else:
        updcuadrado()

def descartar_click():
    global contadorceldas
    contadorceldas=contadorceldas+1
    if(contadorceldas>=25):
        contadorceldas=0
        num_actual=int(pant_cont.get())
        num_actual=num_actual+1
        pant_cont.delete(0, 'end')
        pant_cont.insert(0, num_actual)
        nruta=updruta()
        actualizar(nruta)
        cvs_img.move(cuadradoselec, -848, -472)
    else:
        updcuadrado()

#funcion para deshacer
def deshacer():
    global contadorceldas
    if(contadorceldas!=0):
        
        if(contadorceldas==5 or contadorceldas==10 or contadorceldas==15 or contadorceldas==20):
            
            cvs_img.move(cuadradoselec, 848, -118)
            
        else:
            cvs_img.move(cuadradoselec, -212, 0)
        
        contadorceldas=contadorceldas-1
        #TODO AÑADIR BORRAR UNA ULTIMA LINEA
        
    else:
        messagebox.showerror(title="operacion invalida", message="la imagen anterior ya fue completada, por cuestiones de tiempo esta operacion no se puede realizar")


#funcion para el boton salir
def salir():
    messagebox.showinfo(title="Guarda este dato", message="te quedaste en la imagen: "+pant_cont.get()+", guarda este dato")
    raiz.destroy()

#boton para elegir el archivo de destino
def cambiar_click():
    ruta=askopenfilename(title="selecciona un archivo a mandar los resultados")
    txt_dest.insert(0,ruta)
    abrcrp.config(state="normal")

#tki
raiz=Tk()
clear()
contadorceldas=0
inicial=255*np.ones((590,1060), np.uint8)#imagen blanca para enseñar por defecto
preim=Image.fromarray(inicial)
posimg=ImageTk.PhotoImage(image=preim)

raiz.title("Etiquetador de imagenes V0.3")
raiz.state("zoomed")

frm_img=Frame(raiz)#frame para el contenedor de la imagen
frm_img.config(width=1072, height=610, bg="gray")
frm_img.place(x=25, y=10)

cvs_img=tkinter.Canvas(frm_img, width=1060, height=590) #canvas de la imagen
contenedor_img=cvs_img.create_image(0,0, image=posimg, anchor="nw")
cvs_img.place(x=3, y=5)

######### IMAGENES A RECIBIR: 1060x590###########


####TODO AÑADIR STATE="DISABLED AL TERMINAR LAS PRUEBAS"
abrcrp=Button(text="Abrir carpeta", width=10, command=abrir_click)
abrcrp.place(x=1150, y=10)

detener=Button(text="Detener", width=10, bg="red", fg="white", command=salir)
detener.place(x=1150, y=60)

lbl_inf=Label(raiz, text="Archivo de destino")
lbl_inf.place(x=1140, y=100)
txt_dest=Entry(width=13, justify=RIGHT)
txt_dest.place(x=1150, y=120)

btn_dest=Button(text="Cambiar...", width=10, command=cambiar_click).place(x=1150, y=140)

lbl_num_im=Label(raiz, text="# de imagen:").place(x=1150, y=200)
pant_cont=Entry(width=5)
pant_cont.insert(0, "0")
pant_cont.place(x=1155, y=220)

lbl_pasado=Label(raiz,text="Ultimo ingresado:").place(x=1150, y=250)
txt_pasado=Label(width=13, text="")
txt_pasado.place(x=1155, y=270)

btn_fuego=Button(text="Fuego", width=10, bg="orange", fg="white", command=fuego_click).place(x=1150, y=350)
btn_humo=Button(text="Humo", width=10, bg="gray", fg="white", command=humo_click).place(x=1150, y=390)
btn_nada=Button(text="No fuego", bg="green", width=10, command=nada_click).place(x=1150, y=430)
btn_nada=Button(text="Descartar", width=10, command=descartar_click).place(x=1150, y=470)
btn_deshacer=Button(text="Deshacer", width=10, bg="#FF5733", command=deshacer).place(x=1150, y=510)

raiz.mainloop()