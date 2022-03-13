
from tkinter import Button, Canvas, messagebox
import numpy as np
import cv2
import tkinter
from PIL import Image
from PIL import ImageTk
import imutils
# Load an color image




def load(ruta:str):
    img = cv2.imread(ruta)
    #img=imutils.resize(img, height=180)
    img=cv2.resize(img, (1062,594))
    #img=imutils.resize(img, width=280)
    #Rearrang the color channel
    b,g,r = cv2.split(img)
    img = cv2.merge((r,g,b))
    return img



def poner(imgtk):
    #im = Image.fromarray(load('C:/Users/j_lal/Desktop/python/mineria_p1/imgprueba/aghioaehp{oaspbaswr.png'))
    #imgtk = ImageTk.PhotoImage(image=im)
    elcvas.create_image(0,0, image=imgtk, anchor="nw")

def paso1(ruta:str):
    im=Image.fromarray(load(ruta))
    return im

def paso2(cosa):
    imgtk=ImageTk.PhotoImage(image=cosa)
    return imgtk

def definitivo():
    global res
    res=paso2(paso1('C:/Users/j_lal/Desktop/python/mineria_p1/imgprueba/aghioaehp{oaspbaswr.png'))
    #elcvas.create_image(0,0, image=res, anchor="nw")
    elcvas.itemconfig(mand, image=res)

# A root window for displaying objects
root = tkinter.Tk()  
inicial=255*np.ones((1062,598), np.uint8)
root.geometry("900x650")
root.config(bg="gray")

# Convert the Image object into a TkPhoto object
#im = Image.fromarray(load('C:/Users/j_lal/Desktop/python/mineria_p1/imgprueba/aghioaehp{oaspbaswr.png'))
#imgtk = ImageTk.PhotoImage(image=im)


elcvas=tkinter.Canvas(root, width=280, height=180)

preim=Image.fromarray(inicial)
posimg=ImageTk.PhotoImage(image=preim)

#res=paso2(paso1('C:/Users/j_lal/Desktop/python/mineria_p1/imgprueba/aghioaehp{oaspbaswr.png'))
#poner(res)
mand=elcvas.create_image(0,0, image=posimg, anchor="nw")

elcvas.place(x=0, y=0)


prueba=Button(root, text="aa", command=definitivo)
prueba.place(x=300, y=300)


root.mainloop() # Start the GUI