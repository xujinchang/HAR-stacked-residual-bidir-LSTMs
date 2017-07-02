import numpy as np
import cv2
import cPickle
import sys
import time
import copy
from face_warp import *
from multiprocessing import Pool
from reco_DA import crop_image_with_pad

poch_size=40
def rectToSquare(rect):
    center_x = rect[0] + rect[2]/2
    center_y = rect[1] + rect[3]/2
    height=rect[2]
    width=rect[2]
    center_y += int(height*0.08)
    return [center_x - width / 2,center_y - height / 2, width, height]
def rectToSquare1(rect):
    height=rect[2]
    width=rect[3]
    flag=0 if height>width else 1
    if flag==0:
        diff=height-width
        return [rect[0],rect[1]-diff/2,height,height]
    else:
        diff=width-height
        return [rect[0]-diff/2,rect[1],width,width]


def write_rect(img_list):
    for idx,line in enumerate(img_list):
        filename = line.split()[0]
        rect =[int(float(la)) for la in line.split()[1:5]]
        img = cv2.imread(filename)
        rect2=rectToSquare1(rect)
        #newname='/home/xujinchang/share/AGG/Liveness/detection/dafeng_rect/'+filename.split('/')[-1]
        newname='./'+'15_'+filename.split('/')[-1]
        img_crop=crop_image_with_pad(img,rect2)
        cv2.imwrite(newname,img_crop)
        if idx%poch_size==0:
            print idx,"finished"

def write_landmark(img_list):
    for idx,line in enumerate(img_list):
        filename = line.split()[0]
        print filename
        landmark =[int(float(la)) for la in line.split()[1:5]]
        img = cv2.imread(filename)
        landmarks=line.split()[1:11]
        imgs,lands = face_warp_main(img,landmarks)
        img_crop = crop_image(imgs,lands,2,0)

        #newname='/localSSD/xjc/liveness/align/xiong_true/'+filename.split('/')[-1]
        #newname='./'+filename.split('/')[-1]
        #print newname
        cv2.imwrite(filename,img_crop)

if __name__=="__main__":
    image_lists=[line.strip() for line in open(sys.argv[1])]
    image_lists_length=len(image_lists)
    task_lists=[image_lists[i*poch_size:(i+1)*poch_size] for i in range(image_lists_length/poch_size)]
    if  not image_lists_length%poch_size==0:
        task_lists.append(image_lists[(image_lists_length/poch_size)*poch_size:])
    pool=Pool(20)
    pool.map(write_landmark,tuple(task_lists))
    pool.close()
    pool.join()

