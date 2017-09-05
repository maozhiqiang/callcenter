# -*- encoding: utf-8 -*-
'''

    云知声

'''
import os
from ctypes import *
from io import BytesIO
import glob
import os
import commands
from pydub import AudioSegment

BASEPATH = os.path.split(os.path.realpath(__file__))[0]

# define USC_ASR_SDK_APP_KEY "djf25awkwd3aiuddhfvmxg6bj6tjm4t5vdlopjyx"
# define USC_ASR_SDK_SECRET_KEY "bb30a3893daf45be34ab7706b314dbca"

# app-key
USC_ASR_SDK_APP_KEY = "kajl37havsxqsu5qh3jxgeh6lmqfneeshfbiwkif"
# secret-key
USC_ASR_SDK_SECRET_KEY = "da50bfb0eae8f3d0fb0110fe2e3d9fad"
# buffer
BUFFER_SIZE = 2048
# 参数为APP_KEY
USC_OPT_ASR_APP_KEY = 9
# 语音编码格式
audio_format = "pcm16k"
# 识别领域
domain = "general"
# 状态开关
USC_ENABLE = "true"
USC_DISABLED = "false"
# 语言
LANGUAGE_CHINESE = "chinese"
# 识别正常
USC_ASR_OK = 0
USC_OK = 0
# 参数为用户secret
USC_OPT_USER_SECRET = 204
# 输入语音编码格式
USC_OPT_INPUT_AUDIO_FORMAT = 1001
# 选择识别领域
USC_OPT_RECOGNITION_FIELD = 18
# 有结果返回
USC_RECOGNIZER_PARTIAL_RESULT = 2
# 检测到语音结束
USC_RECOGNIZER_SPEAK_END = 101


class VoiceClient(object):
    def __init__(self):
        self.__cur = cdll.LoadLibrary(BASEPATH + '/sdk/libusc.so')
        self.handler = c_longlong(0)
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

    def asrInit(self):
        # 1 - 创建实例 usc_create_service
        self.usc_create_service.argtypes = [c_void_p]
        ret = self.usc_create_service(byref(self.handler))
        if ret != USC_ASR_OK:
            print 'usc_create_service_ext error.. : ', ret

        # 2 - 设置识别AppKey
        ret = self.usc_set_option(self.handler, USC_OPT_ASR_APP_KEY, USC_ASR_SDK_APP_KEY)
        if ret != USC_OK:
            print 'usc_set_option error.. : ', ret

        ret = self.usc_set_option(self.handler, USC_OPT_USER_SECRET, USC_ASR_SDK_SECRET_KEY)
        if ret != USC_OK:
            print 'usc_set_option error,USC_OPT_USER_SECRET.. : ', ret

        # 3 - login :usc_login_service
        ret = self.usc_login_service(self.handler)
        if ret != USC_ASR_OK:
            print 'usc_login_service error', ret

        # 4 - 设置输入语音的格式
        ret = self.usc_set_option(self.handler, USC_OPT_INPUT_AUDIO_FORMAT, "pcm16k")
        if ret != USC_OK:
            print 'usc_set_option error,USC_OPT_INPUT_AUDIO_FORMAT.. : ', ret

        ret = self.usc_set_option(self.handler, USC_OPT_RECOGNITION_FIELD, domain)
        if ret != USC_OK:
            print 'usc_set_option error,UUSC_OPT_RECOGNITION_FIELD. : ', ret

        ret = self.usc_set_option(self.handler, 20, LANGUAGE_CHINESE)
        if ret != USC_OK:
            print 'usc_set_option error,LANGUAGE_CHINESE.. : ', ret

    def getWaveData(self, _tmpFile):
        with open(_tmpFile, 'rb') as f:
            return f.read()

    def convDataToPointer(self, wav_data):
        tmpBytes = BytesIO()
        f_size = tmpBytes.write(wav_data)
        array = (c_byte * f_size)()
        tmpBytes.seek(0, 0)
        tmpBytes.readinto(array)
        return array

    def sox(self, file):

        dataset = './8000'
        outputdir = './16000'
        cmd = 'sox ' + os.path.join(dataset, file) + ' -r 16000 ' + os.path.join(outputdir, file)
        out = commands.getoutput(cmd)
        file_16000 = os.path.join(outputdir, file)
        return file_16000

    def converTowav(self, filename):
        arr = filename.split('.')
        wavfilename = arr[0] + '.wav'
        seg = AudioSegment.from_wav(filename)
        seg = seg.set_frame_rate(16000)
        seg.export(wavfilename, format="wav")
        return wavfilename

    def release(self):
        self.usc_release_service.argtypes = [c_longlong]
        ret = self.usc_release_service(self.handler)
    def asr(self, FileName):
        self.asrInit()
        info = {}

        # 5 - 打开语音文件(16K/8K 16Bit pcmr
        # pcmFileName = self.sox(FileName)
        pcmFileName = self.converTowav(FileName)
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
        # print '......pcm_size....', pcm_size
        pcm_data = f_pcm.read(pcm_size)
        # print '......000000....'
        # 6 - 开启语音识别
        ret = self.usc_start_recognizer(self.handler)
        # print '......usc_start_recognizer..ret..', ret
        result_text = ""
        pcm_count = 0
        i = 0
        stepsize = 640
        j = 0
        for i in range(0, pcm_size, stepsize):
            j += 1
            startIndex = i
            endIndex = min((i + stepsize), pcm_size)
            databBffer = pcm_data[startIndex:endIndex]
            self.usc_feed_buffer.argtypes = [c_longlong, c_char_p, c_int]
            self.usc_feed_buffer.restype = c_int
            ret = self.usc_feed_buffer(self.handler, databBffer, len(databBffer))
            if ret != 0:
                print '--++++++++++-------ret----------', ret, j
                self.usc_get_result.argtypes = [c_longlong]
                self.usc_get_result.restype = c_char_p
                thisResult = self.usc_get_result(self.handler)
                result_text += thisResult

        # 停止语音输入
        self.usc_stop_recognizer.argtypes = [c_longlong]
        ret = self.usc_stop_recognizer(self.handler)
        # print 'stop....',ret
        if ret == 0:
            self.usc_get_result.argtypes = [c_longlong]
            self.usc_get_result.restype = c_char_p
            result_text += self.usc_get_result(self.handler)
        print 'success - - result :', result_text
        self.release()
        f_pcm.close()
        info['success'] = True
        info['error'] = None
        info['data'] = result_text
        return info

vc = VoiceClient()
# FileName = '13132229287_in_3_20170728182437.wav'
FileName = '/home/python_project/call/static/human_audio/15900282168_in_1_20170810103357.wav'
filename = "/mnt/asr/aliyun/A2_58.wav"
if __name__ == '__main__':
    vc.asr(filename)

    print '--++++++++++-------close----------'
    print vc.asr(filename)





