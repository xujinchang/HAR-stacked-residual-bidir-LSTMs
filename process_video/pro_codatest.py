import os
fp = open('test_condafinal','w+')
fp1 = open('sort_conda_test_final.txt','r')
list1 = os.listdir('/localSSD/xjc/codalab_test/')
list1.remove('1.py')
list1.remove('conda_test_final.txt')
list1.remove('train.txt')
#list1.remove('1469584007_CONTENTMENT')
list1 = sorted(list1)
print list1
index = 0
frame_list = []
print len(list1)
for line in fp1.readlines():
    line = line.strip().split(' ')
    key = line[0].split('/')[-2]
    if key == list1[index]:
        frame_list.append(line[0])
    else:
        frame_select=[]
        total = len(frame_list)
        if total < 128: print frame_list[0], len(frame_list)
        if total < 256: step = 1
        if total > 256 and total <384: step = 2
        if total > 384: step = 3
        count = 0
        for item in xrange(0,total,1):
            frame_select.append(frame_list[-item])
            count = count + 1
            if count == 128:break
        for item in frame_select:
            fp.write(item+'\n')
        index = index + 1
        frame_list = []

frame_select=[]
total = len(frame_list)
print "final",len(frame_list)
        #print total
count = 0
for item in xrange(0,total,3):
    frame_select.append(frame_list[-item])
    count = count + 1
    if count == 128:break
for item in frame_select:
    fp.write(item+'\n')
print (len(frame_select))
fp.close()
fp1.close()





