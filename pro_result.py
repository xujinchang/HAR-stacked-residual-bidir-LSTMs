import os
import pickle
import pprint
path = '/home/tmp_data_dir/zhuzezhou/codalab/CTest'
list1 = os.listdir(path)
list1 = sorted(list1)
output = open('test_prediction.pkl','wb')
fp = open('test_label_result','r')
dic = {}
count = 0
for line in fp.readlines():
	line = line.strip().split('\n')
	if int(line[0]) == 0:
		dic[list1[count]] = 'fake'
	else:
		dic[list1[count]] = 'true'
	count = count + 1
pickle.dump(dic, output)

output.close()
fp.close()


pkl_file = open('test_prediction.pkl', 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)

pkl_file.close()

