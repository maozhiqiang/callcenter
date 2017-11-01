# -*- encoding: utf-8 -*-
import io
import os
import json
import time
import wave
import datetime
import Md5Utils
import voice_api
import  FlowHandler
import Config as conf
import WebAPI as xunfei_asr
import RedisHandler as redis
from pydub import AudioSegment
from LogUtils import Logger
from freeswitch import *
reload(voice_api)
reload(xunfei_asr)
logger = Logger()

def hangup_hook(session, what):
    consoleLog("info", "hangup hook for %s!!\n\n" % what)
    return

def input_callback(session, what, obj):
    if (what == "dtmf"):
        consoleLog("info", what + " " + obj.digit + "\n")
    else:
        consoleLog("info", what + " " + obj.serialize() + "\n")
    return "pause"


class IVRBase(object):

    STATUS_MAP = {
        'banks_call': u'您好，中国农业银行，请说出您要办理的业务，您可以说：查询信用卡额度、查询开户行。请问，您要办理什么业务？',
        'banks_answer_loop': u'您还有其他问题要咨询我吗？结束请挂机！',
        'banks_answer_fail': u'我没听清，请问您要办理什么业务'

    }

    def __init__(self, session, args, status='banks_call'):
        self.session = session
        self.args = args
        self.in_count = 0
        self.out_count = 0
        self.__sessionId = None
        self.channal_uuid = session.getVariable(b"origination_uuid")
        self.caller_number = self.session.getVariable("caller_id_number")
        self.caller_in_wav = None
        self.caller_out_mp3 = None
        self.call_full_wav = None
        self.text = None
        self.flow_id = conf.flow_id
        self.record_fpath = None
        self.create_at = None
        self.status = status
        self.init_voice = '/home/callcenter/recordvoice/callIn/{0}/'
        self.human_audio = '/home/callcenter/recordvoice/callIn/{0}/human_audio/'
        self.all_audio = '/home/callcenter/recordvoice/callIn/{0}/all_audio/'
        self.bot_audio = '/home/callcenter/recordvoice/callIn/{0}/bot_audio/'
        self.init_file_path()

    def init_file_path(self):

        self.__sessionId = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.init_voice =self.init_voice.format(self.status)
        self.human_audio = self.human_audio.format(self.flow_id)
        self.all_audio = self.all_audio.format(self.flow_id)
        self.bot_audio = self.bot_audio.format(self.flow_id)

        if not os.path.exists(self.init_voice):
            os.makedirs(self.init_voice)
        if not os.path.exists(self.human_audio):
            os.makedirs(self.human_audio)
        if not os.path.exists(self.bot_audio):
            os.makedirs(self.bot_audio)
        if not os.path.exists(self.all_audio):
            os.makedirs(self.all_audio)
        FlowHandler.closeFlow(self.caller_number, self.channal_uuid)

    def get_voice_wav(self, text, filename):
        r = voice_api.bc.tts(text, filename)
        if r == 0:
            wavfilename = self.converTowav(filename)
            return wavfilename
        else:
            self.session.hangup()
            logger.info('error.......baidu tts error: %d'%r['err_no'])
            return None

    def converTowav(self, filename):
        arr = filename.split('.')
        wavfilename = arr[0] + '.wav'
        fp = open(filename, 'rb')
        data = fp.read()
        fp.close()
        aud = io.BytesIO(data)
        #sound = AudioSegment.from_file(aud, format='mp3')
        sound = AudioSegment.from_mp3(aud)
        raw_data = sound._data
        l = len(raw_data)
        f = wave.open(wavfilename, 'wb')
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.setnframes(l)
        f.writeframes(raw_data)
        f.close()
        return wavfilename

    def playback_status_voice(self, text, jsonStr):
        file_out = self.caller_out_mp3.format(self.out_count, self.__sessionId)
        self.out_count += 1
        # file_out 返回wav文件格式 /home/callcenter/recordvoice/{flow_id}/bot_audio/number_out_{0}_{1}.mp3
        filename = self.get_voice_wav(text,file_out)
        if filename:
            ss_flag = self.flow_id + '_' + text
            key = Md5Utils.get_md5_value(ss_flag)
            logger.info('......setCache....%s' % key)
            redis.r.hset(key, filename)
            self.session.execute("playback", filename)
        else:
            logger.info('error.......system error: err_no')
            self.session.hangup()

    def playback_tts_voice(self, text):
        filename = self.caller_out_mp3.format(self.out_count, self.__sessionId)
        self.out_count += 1
        r = voice_api.bc.tts(text, filename)
        if r == 0:
            filename_wav = self.converTowav(filename)
            consoleLog("info", "playback.....filename .... " + filename_wav + "\n")
            self.session.execute("playback", filename_wav)
        else:
            consoleLog('error', 'baidu tts error: %d' % r['err_no'])
            self.session.hangup()

    def bot_flow(self,input):
        dict = FlowHandler.flowHandler(input,self.caller_number)
        jsonStr = json.dumps(dict)
        if dict['successful']:
            for item in dict['info']:
                text = ''.join(item['output'])
                logger.error('flow return text %s' % text)
                if item['output_resource'] != '':
                    filename = "{0}".format(item['output_resource'])
                    path = self.bot_audio + filename
                    logger.info('-------------playback  %s' % filename)
                    self.session.execute("playback", path)
                else:
                    ss_flag = self.flow_id + '_' + text
                    ss_key = Md5Utils.get_md5_value(ss_flag)
                    if text == None:
                        logger.error(' flow return  output is None ')
                        self.session.hangup()
                    elif redis.r.has_name(ss_key):
                        filename = redis.r.hget(ss_key)
                        logger.info('...... get-cache ........%s' % filename)
                        self.session.execute("playback", filename)
                    else:
                        logger.info('...... start  ........')
                        self.playback_status_voice(text, jsonStr)
                if item['session_end'] or item['flow_end']:
                    self.session.hangup()
        else:
            logger.info('error.......Flow error: err_no   %s' % jsonStr)
            self.session.hangup()

    def IVR_app(self):
        while self.session.ready():
            startTime = time.time()
            filename = self.caller_in_wav.format(self.in_count, self.__sessionId)
            self.in_count += 1
            cmd = "100 400 {0} 4000 10000 100".format(filename)
            try:
                self.session.execute("vad", cmd)
            except Exception as e:
                print 'vad error .... ',e.message
            endTime = time.time()
            logger.error("vad  time  : %s " % (endTime - startTime))
            flag = self.session.getVariable(b"vad_timeout")
            logger.error('record file .....%s' % filename)
            if cmp(flag, 'true') != 0:
                startTime = time.time()
                info = xunfei_asr.vc.getText(filename)
                endTime = time.time()
                logger.error("xunfei asr time  : %s " % (endTime - startTime))
                if info['ret'] == 0:
                    input = ''.join(info['result'])
                    logger.error('xunfei asr result ---%s ' % input)
                    self.bot_flow(input)  # 需要返回文本信息
                else:
                    self.bot_flow('')  # 需要返回文本信息
                    logger.info("......xunfei  asr ....error...........%s" % json.dumps(info))
            else:
                logger.info('vad......没有检测到声音')
                self.bot_flow('')  # 需要返回文本信息

    def run(self):
        self.session.answer()
        self.session.setVariable("set_audio_level", "write +2")
        self.caller_in_wav = self.human_audio + '%s_in_{0}_{1}.wav' % self.caller_number
        self.caller_out_mp3 = self.bot_audio + '%s_out_{0}_{1}.mp3' % self.caller_number
        self.call_full_wav = self.all_audio + '%s_full_{0}_.wav' % self.caller_number
        full_path = self.call_full_wav.format(self.__sessionId)
        self.session.setVariable("RECORD_STEREO", "true")
        self.session.execute("record_session", full_path)
        while self.session.ready():
            if self.status == 'banks_call':
                self.bot_flow('你好')
                self.IVR_app()
            elif self.status == 'exit':
                self.session.hangup()

def handler(session, args):
    session.setHangupHook(hangup_hook)
    ivr = IVRBase(session, args)
    ivr.run()

