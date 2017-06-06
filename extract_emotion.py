#coding:utf-8
import numpy as np
import time
import os
import json
import sys
import socket
import copy
import math
import matplotlib.pyplot as plt
import cv2
sys.path.insert(0,'./python')
import caffe

caffe.set_mode_gpu()
caffe.set_device(2)

MODEL_DEF = '/home/xujinchang/caffe-blur-pose/models/vgg/deploy_vgg_fer.prototxt'
MODEL_PATH = 'vgg_19_finetue_fer2013_iter_30000.caffemodel'

mean = np.array((104, 117, 123), dtype=np.float32)
SIZE = 250

def predict(the_net,image):
  inputs = []
  if not os.path.exists(image):
    raise Exception("Image path not exist")
    return
  try:
    tmp_input = cv2.imread(image)
    tmp_input = cv2.resize(tmp_input,(SIZE,SIZE))
    tmp_input = tmp_input[13:13+224,13:13+224]
    tmp_input = np.subtract(tmp_input,mean)
    tmp_input = tmp_input.transpose((2, 0, 1))
    tmp_input = np.require(tmp_input, dtype=np.float32)
  except Exception as e:
    return None
  the_net.blobs['data'].reshape(1, *tmp_input.shape)
  the_net.reshape()
  the_net.blobs['data'].data[...] = tmp_input
  the_net.forward()
  scores = copy.deepcopy(the_net.blobs['fc7'].data)
  return scores

if __name__=="__main__":
  f = open("/home/xujinchang/share/AGG/Liveness/detection/coda_lab/label_frame/sort_testcoda_all","rb")
  fp = open("test_fc7_feature_new.fea","w")
  fp2 = open("test_y_label_new.fea","w")
  net = caffe.Net(MODEL_DEF, MODEL_PATH, caffe.TEST)
  score_map = dict()
  for line in f.readlines():
    line = line.strip().split(" ")
    score_map[line[0]] = int(line[1])
  acc = 0
  start_time = time.time()
  X_features=[]
  y_label=[]
  count = 0
  for img_name in score_map:
    fea = predict(net,img_name)
    fea = list(np.reshape(fea, (fea.shape[1], fea.shape[0])))
    feature = np.require(fea)# (4096,1)
    X_features.append(feature)
    count = count + 1
    if count % 128 == 0:
        y_label.append(score_map[img_name])

  print len(X_features)
  print len(y_label)
  for item in X_features:
      for idx in range(item.shape[0]):
          fp.write(str(item[idx][0])+' ')
      fp.write('\n')
  for item in y_label:
      fp2.write(str(item)+'\n')

  f.close()
  fp.close()
  fp2.close()
  end_time = time.time()
  forward_time = end_time - start_time
  print "forward_time: ",forward_time/len(score_map)
