# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 22:26:20 2021

@author: ADMIN
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def showOpenCVImagesGrid(images, x, y, titles=None, axis="on"):
    fig = plt.figure()
    i = 1
    for image in images:
        copy = image.copy()
        channel = len(copy.shape)
        cmap = None
        if channel == 2:
            cmap = "gray"
        elif channel == 3:
            copy = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
        elif channel == 4:
            copy = cv2.cvtColor(copy, cv2.COLOR_BGRA2RGBA)

        fig.add_subplot(x, y, i)
        if titles is not None:
            plt.title(titles[i-1])
        plt.axis(axis)
        plt.imshow(copy, cmap=cmap)
        i += 1
    plt.show()


def grayImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def drawLines(image, lines, thickness=5):
    for line in lines:
        # print("line="+str(line))
        cv2.line(image, (line[0], line[1]), (line[2], line[3]),
                (255, 0, 255), thickness)


def drawContours(image, contours, thickness=1):
    i = 0
    for contour in contours:
        cv2.drawContours(image, [contours[i]], i, (0, 255, 0), thickness)
        area = cv2.contourArea(contour)
        i += 1
        
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )    
    
def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            _,contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares
