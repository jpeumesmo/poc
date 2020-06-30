#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import time
import sys
import random
from matplotlib import pyplot as plt
from header import *

contorno = []

def draw_circle(event,x,y,flags,param):
    global contorno
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(frame_select,(x,y),5,(0,0,255),-1)
        contorno.append([x,y])
#        print contorno
    if len(contorno) == 4:
        points = np.array(contorno)
        cv2.fillConvexPoly(frame_select,points,color=(255,0,0))


##############ARG CALL SYSTEM CONFIGURATIONS###################
if '-h' in sys.argv:
    print ('HELP FOR ARGUMENTS')
    print('-o \t: file name for the output *.avi')
    print('-s \t: show frames while executing')
    print('-i \t: input file name, if not set a custom video is used')
    print('-v \t: to use the validate system')
    sys.exit()

if ('-s' not in sys.argv) and ('-o' not in sys.argv):
    print 'use -s or -o for system output'
    print 'use -h for help'
    sys.exit()

if '-i' in sys.argv:
    aux = sys.argv.index('-i')
    cap = cv2.VideoCapture(sys.argv[aux+1])
else:
    cap = cv2.VideoCapture('videos/4.mp4')

if ('-v' in sys.argv):
    cv2.namedWindow('validate')
    cv2.setMouseCallback('validate',draw_circle)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    aleatorios = random.sample(np.arange(length),1)
    f = open('saida/avaliado/saida.txt','a')

########################################################################

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print(frame_width,frame_height)
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
if '-o' in sys.argv:
    aux = sys.argv.index('-o')
    if '.avi' in sys.argv[aux+1]:
        
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        # out = cv2.VideoWriter(sys.argv[aux+1],fourcc, 20.0, (frame_width,frame_height),isColor= False)

        out = cv2.VideoWriter('teste.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (frame_width, frame_height))
    else:
        print 'please use .avi file extension'
        sys.exit()

flag = True
font = cv2.FONT_HERSHEY_SIMPLEX
cont = 0

while(cap.isOpened()):
    start = time.time()
    ret, frame = cap.read()
    if ret==True:
        ################ALGORITHM##################
        b, g, r = cv2.split(frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        ha = select_region(v)
        h_select = select_region(h)
        canny1 = np.absolute(cv2.Canny(ha,100,200))
        closing1 = cv2.morphologyEx(canny1, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))


        d = cv2.add(select_region(g),closing1)
        avg =  np.average(d)
        mask = cv2.inRange(d, avg-55, avg+55)
        res = cv2.bitwise_and(g,g, mask= mask)
        img3 = np.zeros_like(frame)
        img4 = np.zeros_like(frame)
        frame_select = select_region(frame)
        biggest_region(mask,img4)

        #
        b4, g4, r4 = cv2.split(img4)
        res1 = cv2.bitwise_and(r4,r)
        img3[:,:,0] = b
        img3[:,:,1] = res1
        img3[:,:,2] = r

        #CALCULATE FPS
        end = time.time()
        seconds = end - start
        fps = 1/seconds
        if '-v' in sys.argv and cont in aleatorios:
            while 1:
                cv2.imshow('validate',frame_select)
                if  cv2.waitKey(1) & 0xFF == ord('b'):
                    cv2.destroyAllWindows()
                    break
            points = np.array(contorno)
            b_select,g,r = cv2.split(frame_select)
            m_b_s = cv2.inRange(b_select, 255, 255)
            area_selecionada = getArea(m_b_s)
            avaliado = cv2.subtract(b_select,mask)
            m_avaliado = cv2.inRange(avaliado, 255, 255)
            dif_area = getArea(m_avaliado)
            cv2.imwrite('saida/avaliado/'+str(cont)+'.png',avaliado)
            p_dif_area = (dif_area/area_selecionada)*100
            f.write('frame:'+str(cont)+'\t'+'area selecionada:'+str(area_selecionada)+'\t'+'area encontrada:'+str(dif_area)+'\t'+'porcentagem'+str(p_dif_area)+'%'+'\n')
            f.close()
            contorno = []
        #SHOW AND/OR WRITE VIDEO
        if '-s' in sys.argv:
            cv2.putText(img3, 'FPS: '+str(round(fps,2)) ,(30,30), font, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(frame, 'FPS: '+str(round(fps,2)) ,(30,30), font, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.imshow('Saida',img3)


            cont = cont + 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if flag:
                flag = False
                print 'press \'q\' for exit'
        if '-o' in sys.argv:
            out.write(img3)
    else:
        break


# Release everything if job is finished
cap.release()
if '-o' in sys.argv:
    out.release()

cv2.destroyAllWindows()
