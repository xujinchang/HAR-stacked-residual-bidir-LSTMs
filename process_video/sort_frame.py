fp = open('test_condafinal','r')
fp1 = open('sort_testcodafinal','w')
list1 = []
for line in fp.readlines():
    line = line.strip().split('\n')
    list1.append(line[0])
list1 = sorted(list1)
for item in list1:
    fp1.write(item+'\n')
fp.close()
fp1.close()
