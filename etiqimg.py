#imports
from math import floor
from tkinter import *
import os
from tkinter import messagebox
import tkinter
from tkinter.filedialog import askdirectory, askopenfilename
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
import imutils




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
    img_tratar=load(ruta_foto_act)
    #recort=ubicaciones(contadorceldas)

    #matr_img=img_tratar[recort[0]:recort[1],recort[2]:recort[3]]

    #promr=prom_matriz(matr_img,0)
    #promg=prom_matriz(matr_img,1)
    #promb=prom_matriz(matr_img,2)
    #(escribir datos obtenidos)
    #f=open(txt_dest.get(), "w")
    #f.write(str(promr)+","+str(promg)+","+str(promb))
    #f.close()
    #fin descriptores
    
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


#funcion del boton humo
def humo_click():
    txt_pasado.config(text="humo")
    #descriptores

    
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


#funcion al dar click al boton nada
def nada_click():
    txt_pasado.config(text="no inc. / vacio")
    #descriptores


    
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
btn_nada=Button(text="Vacio/NS", width=10, command=nada_click).place(x=1150, y=430)
btn_deshacer=Button(text="Deshacer", width=10, bg="#FF5733", command=deshacer).place(x=1150, y=490)

raiz.mainloop()