# coding: utf8

from face_det import face_det
import subprocess as sp
import logging
import os

from Queue import Queue
import threading

__author__ = 'hezhiqun'

logger = logging.getLogger(__name__)

class video_test:
    command0      = 'ffprobe -i {} -show_format | grep duration'
    command1      = 'ffmpeg -ss {time_off_h}:{time_off_m}:{time_off_s} -i {input_file} -frames:v 1 {output_file}'
    command2      = 'ffmpeg -y -i {input_file} -ss {start_time} -t {duration} -acodec aac -strict experimental {output_file}'
    stopProcess   = False
    _do_extract_finished      = False #_do_extract是否执行完的标志
    detect_finished = False
    dur           = 0

    ############################提取图片################################
    '''
    功能:初始化函数
    参数:
    video_name: 视频名
    gframe_dir: 截取的视频的图像的保存位置
    '''
    def __init__(self,video_name,frame_dir,cut_dir):
        self.video_name = video_name
        self.frame_dir  = frame_dir
        self.cut_dir    = cut_dir
    '''
    功能:
    通过读取视频文件名返回视频的总时间
    '''
    def read_video_duration(self):
        the_command0 = self.command0
        duration = sp.check_output(the_command0.format(self.video_name), shell=True)
        try:
            duration = float(duration.split('=')[1])
            return duration
        except Exception as e:
            logger.error('get video duration exception', e)

    '''
    功能:
    从视频中每隔一定时间提取一帧并且保存成图片
    '''
    def _do_extract(self,offset):
        the_command1 = self.command1
        the_current_frame = 0
        dur = 0

        dur = self.read_video_duration()
        logger.debug('******************duration: {}'.format(dur))

        the_current_frame = offset

        while the_current_frame <= dur:
            logger.debug('******************current time {}'.format(the_current_frame))
            cmd = the_command1.format(
                time_off_h=int(the_current_frame / 3600),
                time_off_m=int((the_current_frame / 60) % 60),
                time_off_s=the_current_frame % 60,
                input_file=self.video_name,
                output_file=(self.frame_dir+'/{}.jpg').format(the_current_frame)
            )
            sp.call(cmd, shell=True)
            the_current_frame += 0.02
        self._do_extract_finished = True

    # #########################发送detect请求##########################
    '''
    功能:
    检测视频帧的图片是否有人脸并且用list保存结果
    '''
    def detect(self):
        self.detect_finished = False
        faces = []
        image = sorted(os.listdir(self.frame_dir), key=lambda x: (x.split('.')[0]))
        logging.debug("***************detection******************")
        print "***************detection******************"
        print "detect"
        for img in image :
            image_file=self.frame_dir+'/'+img #路径标准格式为：“C:/Desktop/jack.jpg“，否则会报错
            print image_file
            det_result=face_det(image_file)  # 检测一张图片里的脸。返回的结果是字典
            print det_result
            if(len(det_result) == 1):
                faces.append(img[0:img.index(".jpg")])
            logging.debug("***************"+img+":success"+"******************")
        self.detect_finished = True
        return faces

    '''
    功能:

    '''
    def video(self,faces):
        the_command2 = self.command2
        logging.debug("****************video*********************")
        print "****************video*********************"
        q = Queue(maxsize = 7)
        for face in faces:
            q.put(face)
            if(q.qsize() == 7):
                start = q.get()
                print float(face) - float(start)
                if( (float(face) - float(start) ) == 3.0):
                    logging.debug("******************* put video:"+(self.cut_dir+'/{}.mp4').format(start))
                    cmd = the_command2.format(
                        input_file= self.video_name,
                        start_time= get_hhmmss(start),
                        duration="00:00:03",
                        output_file=(self.cut_dir+'/{}.mp4').format(start)
                    )
                    sp.call(cmd, shell=True)
                    q.queue.clear()
                else:
                    q.queue.clear()

    '''
    功能:
    执行所有功能模块
    '''
    def execute(self,offset):
        logging.debug("****************extract start********************")
        print "****************extract start********************"
        self._do_extract(offset)
        logging.debug("****************extract end********************")
        # faces = []
        # if(self._do_extract_finished):
        #     faces = self.detect()
        # print faces
        # if(self.detect_finished):
        #     print "*********detect_finished=True"
        #     self.video(faces)
'''
功能:
返回hh:mm:ss的字符串
'''
def get_hhmmss(seconds):
    seconds = float(seconds)
    if seconds%1 != 0:
        seconds = seconds+0.5
    hh=int(seconds / 3600)
    if(hh<10):
        hh = "0"+str(hh)
    mm=int((seconds / 60) % 60)
    if(mm<10):
        mm = "0"+str(mm)
    ss=int(seconds % 60)
    if (ss<10):
        ss = "0"+str(ss)
    return str(hh)+":"+str(mm)+":"+str(ss)

'''
功能:
定义线程
'''
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self,i):
        threading.Thread.__init__(self)
        self.i = i
    def run(self):
        file_name =  "/home/tmp_data_dir/zhuzezhou/codalab/CTest"
        save_name = "/localSSD/xjc/codalab_test"
        #mp4_list =  os.listdir(file_name)
        mp4_list = ['2481608439_HAPPINESS.mp4']
        for x in mp4_list:
            # if not os.path.exists("{name}/{name1}".format(name=save_name,name1=str(self.i))):
            #     os.makedirs("{name}/{name1}".format(name=save_name,name1=str(self.i)))
            if not os.path.exists("{name}/{name2}".format(name=save_name,name2=x[:-4])):
                os.makedirs("{name}/{name2}".format(name=save_name,name2=x[:-4]))
            gvideo_name   = "{name}/{mp4_file}".format(name=file_name,mp4_file=x)
            print(gvideo_name)
            log_path      = './log/{name}.log'.format(name=str(self.i)+"_"+x[:-4])
            gframe_dir    = "{name}/{frames}".format(name=save_name,frames=x[:-4])
            print(gframe_dir)
            gcut_dir      = None
        #输出到日志
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename=log_path,
                                filemode='w')

            test = video_test(gvideo_name,gframe_dir,gcut_dir)
            test.execute(0)

threads = []
for i in range(1,2):
    thread = myThread(i)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
