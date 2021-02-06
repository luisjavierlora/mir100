# -*- coding: utf-8 -*-
import cv2
import numpy as np
import genetico
global points

points =list()

def marcarCasillas(img,cuadrados,h,w):

	espace =h//cuadrados
	for i in range(cuadrados+1):
	    cv2.line(img, (0, 0+espace*i), (w, 0+espace*i), (0,0,0))

	for i in range(cuadrados+1):
	    cv2.line(img, (0+espace*i, 0), (0+espace*i, h), (0,0,0))


def convertToFilaColumn(x,y,cuadrados,h):

	espace =h//cuadrados
	c = (x//espace) 
	f = (y//espace)

	return f,c

def casillaRed(img,x,y,cuadrados,h):
	
	espace =h//cuadrados
	f,c = convertToFilaColumn(x,y,cuadrados,h)
	
	img[f*espace:f*espace+espace,c*espace:c*espace+espace,:]=[0,0,255]

	return img




def drawPoints(img,pts,cuadrado,h):

    
    for i in pts:
	img=casillaRed(img,i[0],i[1],cuadrado,h)
    return img

def mouse_drawing(event, x, y, flags, params):
    global point, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        point= (x, y)
        print(point)
        points.append(point)

def convertNumber(pts,cuadrado,h):
    numbers=list()

    for i in pts:
	f,c=convertToFilaColumn(i[0],i[1],cuadrado,h)
	numbers.append(f*20+c)

    return numbers

def numToFilcol(num,cuadrado):
	c=num%cuadrado
	f=(num-c)/cuadrado
	return f,c

def drawPath(img,numbers,cuadrado,h):
	espace =h//cuadrado
	for i in numbers:
		f,c=numToFilcol(int(i),cuadrado)
		img[f*espace:f*espace+espace,c*espace:c*espace+espace,:]=[0,255,0]

	return img

def convertToXY(numbers,cuadrado,h,w):
	espace =h//cuadrado
	pos=list()
	for i in numbers:
		f,c=numToFilcol(int(i),cuadrado)
		x=c-w/40 + 0.5
		y=h/40 - f - 0.5
		pos.append([x,y])	
	
	return pos
		

def getRuta():
	mapp= cv2.imread("/home/luis/catkin_ws2/src/MIR100/mir_description/src/map2.tif")

	h,w,c= mapp.shape

	cuadrado=20

	imgCasi=mapp.copy()
	marcarCasillas(imgCasi,cuadrado,h,w)

	img2=imgCasi.copy()
	cv2.imshow("Gris",img2 )
	send=list()
	while True:
	    cv2.setMouseCallback("Gris", mouse_drawing)
	    key = cv2.waitKey(25)
	    mpp2=drawPoints(img2.copy(),points,cuadrado,h)
	    cv2.imshow("Gris",mpp2 )
	    if(len(points)==2):
		nums=convertNumber(points,cuadrado,h)
		print(nums)
		ruta=genetico.genetico(nums[0],nums[1])
		print(ruta)
		mpp2=drawPath(mpp2,ruta,cuadrado,h)
		send=ruta	
		break
	    if key== 13:    
		print('done')
	    elif key == 27:
		break

	pos=convertToXY(send,cuadrado,h,w)
	cv2.imshow("Gris",mpp2 )
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return pos
