# -*- encoding: utf-8 -*-

import os
import  time
from ctypes import *
from io import BytesIO
import glob
import os
import commands
from pydub import AudioSegment

BASEPATH = os.path.split(os.path.realpath(__file__))[0]

#define USC_ASR_SDK_APP_KEY "djf25awkwd3aiuddhfvmxg6bj6tjm4t5vdlopjyx"
#define USC_ASR_SDK_SECRET_KEY "bb30a3893daf45be34ab7706b314dbca"

#app-key
USC_ASR_SDK_APP_KEY = "kajl37havsxqsu5qh3jxgeh6lmqfneeshfbiwkif"
#secret-key
USC_ASR_SDK_SECRET_KEY = "da50bfb0eae8f3d0fb0110fe2e3d9fad"
#buffer
BUFFER_SIZE = 2048
#参数为APP_KEY
USC_OPT_ASR_APP_KEY = 9
#语音编码格式
audio_format = "pcm16k"
#识别领域
domain = "general"
#状态开关
USC_ENABLE = "true"
USC_DISABLED = "false"
# 语言
LANGUAGE_CHINESE = "chinese"
#识别正常
USC_ASR_OK = 0
#参数为用户secret
USC_OPT_USER_SECRET = 204
# 输入语音编码格式
USC_OPT_INPUT_AUDIO_FORMAT = 1001
#选择识别领域
USC_OPT_RECOGNITION_FIELD = 18
#有结果返回
USC_RECOGNIZER_PARTIAL_RESULT = 2
#检测到语音结束
USC_RECOGNIZER_SPEAK_END = 101

class VoiceClient(object):

    def __init__(self):

        self.__cur = cdll.LoadLibrary(BASEPATH + '/sdk/libusc.so')
        self.handler = c_int(0)
        self.USC_OPT_ASR_APP_KEY = 9 # c_int(9)
        self.USC_ASR_SDK_APP_KEY = "kajl37havsxqsu5qh3jxgeh6lmqfneeshfbiwkif"    # c_char_p("kajl37havsxqsu5qh3jxgeh6lmqfneeshfbiwkif")
        self.usc_create_service = self.__cur.usc_create_service
        self.usc_set_option = self.__cur.usc_set_option
        self.usc_login_service = self.__cur.usc_login_service
        self.usc_release_service = self.__cur.usc_release_service
        self.usc_start_recognizer = self.__cur.usc_start_recognizer
        self.usc_feed_buffer = self.__cur.usc_feed_buffer
        self.usc_get_result = self.__cur.usc_get_result
        self.usc_stop_recognizer = self.__cur.usc_stop_recognizer
        self.usc_get_result_begin_time = self.__cur.usc_get_result_begin_time
        self.usc_get_result_end_time = self.__cur.usc_get_result_end_time
        self.usc_cancel_recognizer = self.__cur.usc_cancel_recognizer
        print '.......init......0......'
        # 1 - 创建实例 usc_create_service
        self.usc_create_service.argtypes = [c_void_p]
        ret = self.usc_create_service(byref(self.handler))
        if ret != USC_ASR_OK:
            print 'usc_create_service_ext error.. : ', ret

        # 2 - 设置识别AppKey
        # self.usc_set_option.argtypes = [c_int, c_int, c_char_p]

        ret = self.usc_set_option(self.handler, USC_OPT_ASR_APP_KEY, c_char_p(USC_ASR_SDK_APP_KEY))
        print '.......init......2......'
        ret = self.usc_set_option(self.handler, USC_OPT_USER_SECRET, c_char_p(USC_ASR_SDK_SECRET_KEY))
        if ret != USC_ASR_OK:
            print "usc_set_option error  : ", ret
        print '.......init......3......'
        # 3 - login :usc_login_service
        ret = self.usc_login_service(self.handler)
        print '.......init......4......'
        if ret != USC_ASR_OK:
            print 'usc_login_service error', ret
        # 4 - 设置输入语音的格式
        ret = self.usc_set_option(self.handler, USC_OPT_INPUT_AUDIO_FORMAT, "pcm16k")
        ret = self.usc_set_option(self.handler, USC_OPT_RECOGNITION_FIELD, domain)
        ret = self.usc_set_option(self.handler, 20, LANGUAGE_CHINESE)
        if ret != USC_ASR_OK:
            print 'usc_set_option error ', ret

    def getWaveData(self,_tmpFile='./A2_1_16k.wav'):
        with open(_tmpFile, 'rb') as f:
            return f.read()
    def convDataToPointer(self,wav_data):
        tmpBytes = BytesIO()
        f_size = tmpBytes.write(wav_data)
        array = (c_byte * f_size)()
        tmpBytes.seek(0, 0)
        tmpBytes.readinto(array)
        return array

    def sox(self,file):

        dataset ='./8000'
        outputdir ='./16000'
        cmd = 'sox ' + os.path.join(dataset, file) + ' -r 16000 ' + os.path.join(outputdir, file)
        out = commands.getoutput(cmd)
        file_16000 = os.path.join(outputdir, file)
        return file_16000

    def converTowav(self, filename):
        arr = filename.split('.')
        wavfilename = arr[0] + '_.wav'
        seg = AudioSegment.from_wav(filename)
        seg = seg.set_frame_rate(16000)
        seg.export(wavfilename, format="wav")
        return wavfilename

    def asr(self,FileName):
        info = {}
        # 5 - 打开语音文件(16K/8K 16Bit pcmr
        # pcmFileName = self.sox(FileName)
        pcmFileName = self.converTowav(FileName)
        # print pcmFileName
        f_pcm = open(pcmFileName, "rb")
        if f_pcm == None:
            print 'Open File error '
            info['success'] = False
            info['error'] = 'Open File error '
            info['data'] = None
            return info

        waveData = self.getWaveData(pcmFileName)
        p_pcm = self.convDataToPointer(waveData)
        pcm_size = sizeof(p_pcm)
        pcm_data = f_pcm.read(pcm_size)
        # 6 - 开启语音识别
        ret = self.usc_start_recognizer(self.handler)
        result_text = ""
        i=0
        stepsize=640
        for i in range(0,pcm_size,stepsize):
            startIndex=i
            endIndex= min((i+stepsize),pcm_size)
            dataBffer = pcm_data[startIndex:endIndex]
            #print databBffer
            self.usc_feed_buffer.argtypes = [c_int,c_char_p,c_int]
            self.usc_feed_buffer.restype = c_int
            ret = self.usc_feed_buffer(self.handler, dataBffer, len(dataBffer))
            #获取中间部分识别结果
            self.usc_get_result.argtypes = [c_int]
            self.usc_get_result.restype = c_char_p
            if ret == 2:
                thisResult=self.usc_get_result(self.handler)
                result_text +=thisResult
        #停止语音输入
        ret = self.usc_stop_recognizer(self.handler)
        if ret == 0:
            result_text += self.usc_get_result(self.handler)
        print 'success - - result :',result_text
        # 6 - 释放： usc_release_service
        self.usc_release_service(self.handler)
        ret = self.usc_cancel_recognizer(self.handler)
        print  'asdasd----',ret
        info['success'] = True
        info['error'] = ''
        info['data'] = result_text
        return info
vc = VoiceClient()
if __name__ == '__main__':
    vc = VoiceClient()
    pcmFileName = '/mnt/asr/15880114563_in_4_20170721150453.wav'

    time1 = time.time()
    result = vc.asr(pcmFileName)
    print'-------time ----', (time.time() -time1)
    print '--------2...start-------'
    time1 = time.time()
    result = vc.asr(pcmFileName)
    print'-------time2 ----', (time.time() -time1)
    pass