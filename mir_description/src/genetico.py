# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:13:17 2021

@author: ADMIN
"""

import numpy as np
import random
import matplotlib.pyplot as plt 
import cv2

p_list = list(range(0, 400))
p=np.array(p_list).reshape((20,20))


def readMap():
    mapp= cv2.imread("map2.tif")
    img_gris = cv2.cvtColor(mapp, cv2.COLOR_BGR2GRAY)
    cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) 
    


#############################################################
#############################################################
#############################################################
def genrandom(init,fin,cromo,Po):
    
    genes= list()
    for i in range(Po):
        gen = list()
        gen.append(init)
        
        
        while(True):
            m=gen[-1]//10
            limHi = m*10
            if(m %2!=0):
                limHi = limHi-10
                limHs = limHi+19
            else:
                
                limHs = limHi+9
                
            m=gen[-1]%20
            limVi=m
            limVs=380+m
            pasos=20       
                
            if(np.random.randint(0,2)==1):
                c=np.random.randint(limHi,limHs+1)
            else:
                c=random.randrange(limVi, limVs,pasos)        
            
            
            if (c not in gen) and (c != fin):
                gen.append(c)
            
            if len(gen)==cromo-1:
                break
        
        gen.append(fin)
        
        genes.append(gen)
        
    return genes





def fitness(gen):
    
    a= gen[0]
    suma=0
    for  i in range(1,len(gen)):
        b=gen[i]
        if(b//20==a//20):
            dis=abs(b-a)
        else:
            dis=abs(b-a)//20
        suma= suma +dis
        a=b
    
    
    fx= 1- suma/(20*len(gen))
    return fx

def getfitness(genes):
    
    fit_score=list()
    for i in genes:
        fx=fitness(i)
        fit_score.append(fx)
    
    return fit_score


def restriccion(gen,walls):
    
    fin=gen[-1]
    b=gen[-2]
    alfa=1
    if(b//20==fin//20):
        #estan  en la misma fila pero hay una pared
        for i in walls:
            if (min(b,fin)<i and i<max(b,fin )):
                alfa=0.45*abs(b-fin)/20
                break
    
    elif(b%20 == fin%20):
        #estan en la misma columna pero hay una pared
        for i in walls:
            if(i%20==b%20):
                alfa=0.45*(abs(b-fin)/20)/20
        
    
    else:
        alfa = 0.7*abs(b%20-fin%20)/20
    
    return alfa

def restricciones(genes,walls):
    restri=list()
    for i in genes:
        alfa=restriccion(i,walls)
        restri.append(alfa)
    
    return restri
    
def fitnees2(fit,alfa):
    
    fitn=list()
    
    for i in range(0,len(fit)):
        fitvalue=fit[i]*alfa[i]
        fitn.append(fitvalue)

    
    return fitn


def seleccion(fit,po):
    
    fil,col=po.shape
    
    #fil = numero de cromosomas
    #po = poblacion
    Psele=fit*fil/sum(fit)
    
    poblacionIntermedia = np.zeros([fil,col])
    
    for i in range(0,fil):
        maximo=max(Psele)[0]
        posi=np.where(Psele==maximo)
        f=posi[0][0]

        
        #cromo = po[f,:]
        poblacionIntermedia[i,:]=po[f,:]
        
        
        if(maximo>1):
            maximo=maximo-1
            Psele[f,0]=maximo
        else:
            Psele[f,0]=0
        
    #print(poblacionIntermedia)
        
    return poblacionIntermedia


def cruzar(Pi):
    
    Pc=0.2
    
    h,w = Pi.shape
    
    num_cruces= int(Pc*h)
    cont=0
    while(cont<num_cruces):
        pg1= np.random.randint(0,h)
        pg2= np.random.randint(0,h)
        
        g1=Pi[pg1,:]
        g2=Pi[pg2,:]
        
        
        p_cruze=np.random.randint(1,len(g1)-1)
        
        g1_a=g1[0:p_cruze]
        g2_b=g2[p_cruze:w]
        
        Pi[pg1,0:p_cruze]=g1_a
        Pi[pg1,p_cruze:w]=g2_b
        
        g2_a=g2[0:p_cruze]
        g1_b=g1[p_cruze:w]    
        
        Pi[pg2,0:p_cruze]=g2_a
        Pi[pg2,p_cruze:w]=g1_b
        
        cont= cont+2
        
        
    return Pi
        
    

    
    
    
        
def genetico(posIni,posFin):    
        
    

	robot=posIni

	posfinal=posFin
	walls=[8,28,48,108,128,148,168,188,208,228,248,268,288,308,328,348,368,388]
	#genes
	cromosomas = 6
	num_genes =30
	fitnessReco= list()

	Po=genrandom(robot,posfinal,cromosomas,num_genes)
	max_generations=20

	for i in range(0,max_generations):
	    fit=getfitness(Po)
	    restri=restricciones(Po,walls)
	    fit2=fitnees2(fit,restri)
	    Pi=seleccion(np.array(fit2).reshape(len(fit2),1),np.array(Po))
	    Pi2=cruzar(Pi)
	    Po=Pi2
	    fitnessReco.append(max(fit2))
	    
	    if(max(fit2)>0.9):
		break


	plt.plot(fitnessReco)


	maximo=max(fit2)
	f=fitnessReco.index(maximo)
	ruta=Po[f,:]
	print("Best route: ",Po[f,:])

	#cromo = po[f,:]
	#poblacionIntermedia[i,:]=po[f,:]


	#new poblation
	return Po[f,:]



