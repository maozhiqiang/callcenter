# -*- encoding: utf-8 -*-

import io
import wave
import json
import time
import FlowHandler
import datetime
import Md5Utils
import VoiceApi as voice_api
import RedisHandler as redis
import WebAPI as xunfei_asr

from freeswitch import *
from PsqlUtils import DBHelper
from LogUtils import Logger
from pydub import AudioSegment
# from VoiceHandler import VoiceClient

# voiceasr = VoiceClient()
reload(voice_api)
reload(xunfei_asr)
reload(redis)

db = DBHelper()
logger = Logger()
#挂机操作
def hangup_hook(session, what):
    consoleLog("info", "hangup hook for %s!!\n\n" % what)
    channal_uuid = session.getVariable(b"origination_uuid")
    number = session.getVariable(b"caller_id_number")
    consoleLog("info", "hangup hook for %s!! \n\n" % number)
    FlowHandler.closeFlow(number, channal_uuid)  # 挂断电话后结束此次会话流程
    logger.info(".....关闭流程.......")
    return
#按键操作
def input_callback(session, what, obj):
    if (what == "dtmf"):
        consoleLog("info", what + " " + obj.digit + "\n")
    else:
        consoleLog("info", what + " " + obj.serialize() + "\n")
    return "pause"
#对话容器
class IVRBase(object):
    def __init__(self,session, args):
        self.session = session
        self.args = args
        self.in_count = 0
        self.out_count = 0
        self.loopTimes = 0
        self.__sessionId = None
        self.flow_id = None
        self.fs_call_id = None
        self.channal_uuid = session.getVariable(b"origination_uuid")
        self.caller_number = session.getVariable(b"caller_id_number")
        self.caller_in_wav = None
        self.caller_out_mp3 = None
        self.caller_out_fail = None
        self.call_full_wav = None
        self.text = None
        self.record_fpath = None
        self.create_at = None
        self.getFlowIdByUUID()

    def getFlowIdByUUID(self):
        try:
            logger.info('number is %s ... channal_uuid is %s ' % (self.caller_number, self.channal_uuid))
            list = db.getFlowIdAndAppId(self.caller_number, self.channal_uuid)
            self.flow_id = list[4]
            self.fs_call_id = list[0]
            self.__sessionId = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            #关闭流程
            FlowHandler.closeFlow(self.caller_number, self.channal_uuid)
        except Exception as e:
            logger.error('getFlowIdByUUID except error %s'% e.message)

    def get_voice_wav(self, text, filename):
        r = voice_api.bc.tts(text, filename)
        if r == 0:
            wavfilename = self.converTowav(filename)
            return wavfilename
        else:
            logger.error('error.......baidu tts error: %d'%r['err_no'])
            return None

    def converTowav(self, filename):
        arr = filename.split('.')
        wavfilename = arr[0] + '.wav'
        fp = open(filename, 'rb')
        data = fp.read()
        fp.close()
        aud = io.BytesIO(data)
        sound = AudioSegment.from_file(aud, format='mp3')
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

    def update_full_path(self, path, channal_uuid):
        db.updateFull_record_fpath(path, channal_uuid)

    def record_chat_run(self, who, text, record_fpath, create_at, call_id, jsonStr):
        db.record_chat_sql(who, text, record_fpath, create_at, call_id, jsonStr)

    def bot_flow(self, input):
        startTime = time.time()
        create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dict = FlowHandler.flowHandler(input, self.caller_number, self.flow_id)
        endTime = time.time()
        logger.error('Flow time .........: %s'%(endTime - startTime))
        jsonStr = json.dumps(dict)
        if dict['successful']:
            for item in dict['info']:
                text = ''.join(item['output'])
                logger.debug('flow return text %s' % text)
                if item['output_resource'] != '':
                    filename = "{0}".format(item['output_resource'])
                    filename = '/home/callcenter/recordvoice/bot_audio/'+filename
                    logger.info('-------------playback-------------%s' % (filename))
                    self.session.execute("playback", filename)
                    path = filename.split('/')[-1]
                    realy_file_path = "/bot_audio/{0}".format(path)
                    self.record_chat_run('bot', text, realy_file_path, create_at, self.fs_call_id, jsonStr)
                else:
                    ss_key = Md5Utils.get_md5_value(text)
                    if text == None:
                        self.bot_flow('')
                        logger.error(' flow return  output is None ')
                    elif redis.r.has_name(ss_key):
                        filename = redis.r.hget(ss_key)
                        logger.info('...... get-cache ........%s' % filename)
                        self.session.execute("playback", filename)
                        realy_file_path = filename.split('recordvoice')
                        self.record_chat_run('bot', text, realy_file_path[1], create_at, self.fs_call_id, jsonStr)
                    else:
                        self.playback_status_voice(text, jsonStr)
                if item['session_end'] or item['flow_end']:
                    logger.info('-------------flow end-------------')
                    self.session.hangup()
        else:
            logger.info('error.......Flow error: err_no   %s'%jsonStr)
            self.session.hangup()

    def playback_status_voice(self, text, jsonStr):
        create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file_out = self.caller_out_mp3.format(self.out_count, self.__sessionId)
        self.out_count += 1
        filename = self.get_voice_wav(text, file_out)  # 返回wav文件格式

        if filename:
            key = Md5Utils.get_md5_value(text)
            logger.info('......setCache....%s' % key)
            redis.r.hset(key, filename)
            self.session.execute("playback",filename)
            realy_file_path = filename.split('static')
            self.record_chat_run('bot', text, realy_file_path[1], create_at, self.fs_call_id, jsonStr)
        else:
            logger.info('error.......system error: err_no')
            self.session.hangup()

    def IVR_app(self):
        while self.session.ready():
            startTime = time.time()
            create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            filename = self.caller_in_wav.format(self.in_count, self.__sessionId)
            self.in_count += 1
            cmd = "{0} 4000".format(filename)
            logger.info('vad start time---%s '%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            self.session.execute("vad", cmd)
            logger.info('vad start end---%s ' %time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            endTime = time.time()
            logger.error("vad  time  : %s " % (endTime - startTime))
            flag = self.session.getVariable(b"vad_timeout")
# --------------------------------xun fei   asr --------------------------------------------
            if cmp(flag, 'true') != 0:
                startTime = time.time()
                info = xunfei_asr.vc.getText(filename)
                endTime = time.time()
                logger.error("xunfei asr time  : %s " % (endTime - startTime))
                if info['ret'] == 0:
                    input = ''.join(info['result'])
                    logger.error('xunfei asr result ---%s ' % input)
                    realy_file_path = filename.split('static')
                    self.record_chat_run('human', input, realy_file_path[1], create_at, self.fs_call_id,
                                         json.dumps(info))
                    self.bot_flow(input)
                else:
                    self.bot_flow('')
                    logger.info("......xunfei  asr ....error...........%s" % json.dumps(info))
            else:
                logger.info('vad......没有检测到声音')
                self.bot_flow('')

    def run(self):
        self.session.answer()
        self.session.setVariable("set_audio_level", "write +2")
        self.caller_in_wav = '/home/python_project/call/static/human_audio/%s_in_{0}_{1}.wav' % self.caller_number
        self.caller_out_mp3 = '/home/python_project/call/static/bot_audio/%s_out_{0}_{1}.mp3' % self.caller_number
        self.caller_out_fail = '/home/python_project/call/static/bot_audio/%s_out_fail.mp3' % self.caller_number
        self.call_full_wav = '/home/python_project/call/static/all_audio/%s_full_{0}_.wav' % self.caller_number
        full_path = self.call_full_wav.format(self.__sessionId)
        self.session.setVariable("RECORD_STEREO", "true")
        self.session.execute("record_session", full_path)
        realy_full_path = full_path.split('static')
        logger.info('realy_full_path.... %s'%realy_full_path[1])
        self.update_full_path(realy_full_path[1], self.channal_uuid)
        while self.session.ready():
            self.bot_flow('你好')
            self.IVR_app()

def handler(session, args):
    session.setHangupHook(hangup_hook)
    ivr = IVRBase(session,args)
    ivr.run()
