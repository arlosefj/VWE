# -*- coding: utf-8 -*-  
# Author: arlose                                                                                                                                     
# Create：2018/5/18
import os
import cv2
import numpy as np
import click

def video2img(videofile, imagedir, skipnum, rszratio):
    capture=cv2.VideoCapture(videofile)
    videoname = os.path.basename(videofile).split('.')[-2]
    if not os.path.exists(imagedir):
        os.makedirs(imagedir)
    n=1
    ret, im = capture.read()
    idx = 1
    if ret:
        img = cv2.resize(im,None,fx=rszratio, fy=rszratio, interpolation = cv2.INTER_CUBIC)
        imgname = imagedir+'/'+str(idx)+'.jpg'
        cv2.imwrite(imgname, img)
        
        while True:
            for i in range(skipnum):
                ret, im = capture.read()
                if not ret:
                    break
                n = n+1
            if not ret:
                break
            ret, im = capture.read()
            if not ret:
                break
            n=n+1
            img = cv2.resize(im,None,fx=rszratio, fy=rszratio, interpolation = cv2.INTER_CUBIC)
            idx=idx+1
            imgname = imagedir+'/'+str(idx)+'.jpg'
            cv2.imwrite(imgname, img)
            # print n
        print str(idx)+'/'+str(n)
        print "done!"
    else:
        print "read video file error"
    return idx

def findWMRegion(imagedir, number):
    imgname1 = imagedir+'/1.jpg'
    lastdiff = cv2.imread(imgname1)
    for i in range(number/2):
        imgname1 = imagedir+'/'+str(i+1)+'.jpg'
        imgname2 = imagedir+'/'+str(number-i)+'.jpg'
        img1 = cv2.imread(imgname1)
        img2 = cv2.imread(imgname2)
        img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 100, 255, cv2.THRESH_BINARY)
        diff = cv2.bitwise_and(img1,img2,mask = mask)
        diff = cv2.bitwise_and(diff,lastdiff,mask = mask)
        lastdiff=diff
        '''
        cv2.imshow('dst',diff)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        '''
    ret, mask = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2,2),np.uint8)
    wm = cv2.dilate(mask,kernel,iterations = 1)
    cv2.imshow('dst',wm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return wm

@click.command()
#@click.argument("videofile")
@click.option("--videofile", "-f", help="the video file")
@click.option("--imagedir", "-d", help="the extract dir")
@click.option("--skipnum", "-s", default=1, help="skip images")
@click.option("--rszratio", "-r", default=1.0, help="resize ratio")
def main(videofile, imagedir, skipnum, rszratio):
    number = video2img(videofile, imagedir, skipnum, rszratio)
    findWMRegion(imagedir, number)

if __name__ == "__main__":
    main()