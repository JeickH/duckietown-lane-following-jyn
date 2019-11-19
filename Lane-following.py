#!/usr/bin/env python2
#librerias
import rospy,  roslib
import sys
import cv2
import math
import picamera
import picamera.array
import numpy as np
from matplotlib import pyplot as plt
from std_msgs.msg import String

from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
#matplotlib inline

from sensor_msgs.msg import Joy

from __builtin__ import True


    

def todo(host):
    pub = rospy.Publisher('/'+host+'/joy', Joy, queue_size=1)
    rospy.init_node('joy-cli', anonymous=True)	
	#recibir imagen, img_colour contiene un vector de numpy el cual se puede usar en opencv
    with picamera.PiCamera() as camera:
    	camera.resolution = (320, 240)
 	with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb')
            img_colour = output.array
		
    
    ##procesamiento de la imagen
    img_size=img_colour.shape
    y=img_size[0]*0.4545
    y=int(y)
    x=0
    h=img_size[0]-y
    w=img_size[1]

    crop_img = img_colour[y:y+h, x:x+w]
    #cv2.waitKey(0)
    # convert the input colour image to grayscale
    img_greyscale = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
    # Gaussian blur
    blur = cv2.GaussianBlur(img_greyscale,(13,13),1)
    sobelx = cv2.Sobel(blur,cv2.CV_64F,1,0,ksize=13)
    sobely = cv2.Sobel(blur,cv2.CV_64F,0,1,ksize=13)
    G = np.hypot(sobelx, sobely)
    G = G / G.max() * 255
    theta = np.arctan2(sobely, sobelx)
    edges = cv2.Canny(blur,150,150,apertureSize = 3)

    minLineLength = 150
    maxLineGap = 20
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    img5=crop_img
    #clasificar las lineas en derecha e izquierda deacuerdo a su pendiente
    rlines=np.zeros((1,10))
    llines=np.zeros((1,10))
    promr=0
    proml=0
    cont0r=0
    cont0l=0
    ir=0
    il=0
    for line in lines :
        for x1, y1, x2, y2 in line:

            m=(y2-y1)/(x2-x1)
        if x2==x1:
            m=0
        if m<-1:
            rlines[0][ir]=m
            ir+=1
      
        if m>1:
            llines[0][il]=m
            il+=1
    #promedio de las pendientes
    for pendiente in range(rlines.shape[1]):
        promr+=rlines[0][pendiente]
        if rlines[0][pendiente]==0:
            cont0r+=1

    promr=promr/(10-cont0r) 

    for pendiente in range(llines.shape[1]):
        proml+=llines[0][pendiente]
    #eliminar datos que sean 0
        if llines[0][pendiente]==0:
            cont0l+=1

    proml=proml/(10-cont0l) 
    #Construccion de lineas de carril
    lyi=img5.shape[0]
    lyf=0
    lxf=(lyf-img5.shape[0]/promr)+50
    #cv2.line(img5,(50,lyi),(int(lxf),lyf),(0,0,255),2)

    ryi=img5.shape[0]
    ryf=0 
    rxf=(ryf-img5.shape[0]/proml)+750
    #cv2.line(img5,(750,ryi),(int(rxf),ryf),(0,0,255),2)
    #construccion de linea a seguir
    sxi=img5.shape[1]/2
    syi=img5.shape[0]
    sxf=(rxf+lxf)/2
    syf=(ryf+lyf)/2
    #cv2.line(img5,(int(sxi),int(syi)),(int(sxf),int(syf)),(255,255,0),2)
    #Hallar el angulo de la linea a seguir respecto a la vertical

    if (sxf-sxi)>0:
        ang=math.atan(img5.shape[0]/(sxf-sxi))
        angd=math.degrees(ang)-90
    if (sxf-sxi)<0:
        ang=math.atan(img5.shape[0]/-(sxf-sxi))
        angd=90-math.degrees(ang)
    if (sxf-sxi)==0:
        angd=90
  #enviar mensaje al topico joy para mover el robot
    if angd >5:
        axes = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0] 
    elif angd<-5:
        axes = [0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0] 
    else:
        axes = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 

    msg = Joy(header=None, axes=axes, buttons=None)
    pub.publish(msg)
    rospy.sleep(0.5)

    axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    msg = Joy(header=None, axes=axes, buttons=None)
    pub.publish(msg)




if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("No hostname specified!")
    else:
        hostname = sys.argv[1]

    try:
        todo(host = hostname)
    except rospy.ROSInterruptException:
        pass

