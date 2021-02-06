# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 21:57:59 2021

@author: ADMIN
"""

#import libraries

import cv2
import numpy as np
import utils
import math

def rotarImagen(img,angulo,center):
    """function for the image rotation 

	img: image RGB
	angulo: angle to rotate the imgggg
	center: center of image
    """
    ancho = img.shape[1] #columnas
    alto = img.shape[0] # filas
    # Rotación
    M = cv2.getRotationMatrix2D(center,angulo,1)
    imageOut = cv2.warpAffine(img,M,(ancho,alto))
    return imageOut
#1 read the map 

#here we gonna check if the image is in correct position and totally oriented

mapp= cv2.imread("/home/luis/catkin_ws2/src/MIR100/mir_navigation/config/my_map.pgm")
img_gris = cv2.cvtColor(mapp, cv2.COLOR_BGR2GRAY)
#img_gris=mapp
print(mapp.shape)
#binarization of mapp
ret,thresh1 = cv2.threshold(img_gris,127,255,cv2.THRESH_BINARY_INV)

#edged
edged=cv2.Canny(thresh1,30,200)

print(thresh1.shape)
#contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours( mapp, contours, -1, (0, 255, 0), 3 )
squares = utils.find_squares(thresh1)
cv2.drawContours(mapp, squares, -1, (0, 255, 0), 3)

"""
cv2.imshow('Gris', cv2.resize(mapp,None,fx=0.4,fy=0.4))
cv2.waitKey(0)
"""
squares=squares[0]

#left
x1=squares[0][0]
y1=squares[0][1]
x2=squares[1][0]
y2=squares[1][1]

#right
x3=squares[2][0]
y3=squares[2][1]

x4=squares[3][0]
y4=squares[3][1]

#cv2.circle(mapp, (x1,y1), 2, (255,0,0), thickness=2)
#cv2.circle(mapp, (x4,y4), 2, (255,0,0), thickness=2)

#cv2.circle(mapp, ((x1+x3)//2,(y1+y3)//2), 2, (255,0,0), thickness=2)

angle=math.atan2((y4-y1),(x4-x1)) * 180.0 / np.pi
#angle=math.atan2((x2-x3),(y2-y3)) 
mappRo=rotarImagen(mapp,angle, ((x1+x3)//2,(y1+y3)//2))
"""
cv2.imshow('Gris', cv2.resize(mappRo,None,fx=0.4,fy=0.4))
cv2.waitKey(0)
"""

#distancia
d= int(math.sqrt((x1-x4)*(x1-x4) +(y1-y4)*(y1-y4)))

cx = (x1+x3)//2 
cy = (y1+y3)//2
mapp2 = mappRo.copy()
mapp2=mapp2[cy-d//2:cy+d//2,cx-d//2:cx+d//2,:]
"""

cv2.imshow('Gris', mapp2)
cv2.waitKey(0)
"""
mapp2=cv2.rotate(mapp2, cv2.ROTATE_90_CLOCKWISE)
mapp2=cv2.rotate(mapp2, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite("map2.tif",mapp2)
