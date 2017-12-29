# -*- encoding: utf-8 -*-
import io
import os
import wave
import json
import time
import Md5Utils
import FlowHandler
import datetime
import Config as conf
import rabbitMQ_produce as rabbitmq
import VoiceApi as voice_api
import RedisHandler as redis
from freeswitch import *
from LogUtils import Logger
import WebAPI as xunfei_asr
from pydub import AudioSegment
import SinoVoice as sino_asr
reload(voice_api)
reload(xunfei_asr)
reload(sino_asr)
reload(redis)
logger = Logger()

def hangup_hook(session, what):
    number = session.getVariable(b"caller_id_number")
    consoleLog("info", "hangup hook for %s!! \n\n" % number)
    return

def input_callback(session, what, obj):
    if (what == "dtmf"):
        consoleLog("info", what + " " + obj.digit + "\n")
    else:
        consoleLog("info", what + " " + obj.serialize() + "\n")
    return "pause"

class IVRBase(object):
    def __init__(self,session, args):
        self.session = session
        self.args = args
        self.in_count = 0
        self.out_count = 0
        self.__sessionId = None
        self.flow_id = session.getVariable(b"flow_id")
        self.fs_call_id = session.getVariable(b"call_id")
        self.channal_uuid = session.getVariable(b"origination_uuid")
        self.caller_number = session.getVariable(b"caller_id_number")
        self.caller_in_wav = None
        self.caller_out_mp3 = None
        self.call_full_wav = None
        self.text = None
        self.record_fpath = None
        self.create_at = None
        self.human_audio = '/home/callcenter/recordvoice/{0}/human_audio/'
        self.all_audio = '/home/callcenter/recordvoice/{0}/all_audio/'
        self.bot_audio = '/home/callcenter/recordvoice/{0}/bot_audio/'
        self.closedFlow()
        self.init_file_path()

    def init_file_path(self):
        self.__sessionId = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.human_audio = self.human_audio.format(self.flow_id)
        self.all_audio = self.all_audio.format(self.flow_id)
        self.bot_audio = self.bot_audio.format(self.flow_id)
        logger.debug('root_file ......%s' %self.bot_audio)
        if not os.path.exists(self.human_audio):
            os.makedirs(self.human_audio)
        if not os.path.exists(self.bot_audio):
            os.makedirs(self.bot_audio)
        if not os.path.exists(self.all_audio):
            logger.info('mkdirs ......%s'%self.all_audio)
            os.makedirs(self.all_audio)

    def closedFlow(self):
        try:
            print '---caller_number---*%s*flow_id*%s***channal_uuid**%s-----'%(self.caller_number,self.flow_id, self.channal_uuid)
            FlowHandler.closeFlow(self.caller_number,self.flow_id, self.channal_uuid)
            consoleLog("info", "*****FlowHandler.closeFlow!!*****\n\n")
        except Exception as e:
            logger.error('FlowHandler.closeFlow!! except error %s' % e.message)
            self.session.hangup()
            return

    def get_voice_wav(self, text, filename):
        r = voice_api.bc.tts(text, filename)
        if r == 0:
            wavfilename = self.converTowav(filename)
            return wavfilename
        else:
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

    def update_full_path(self, record_fpath, channal_uuid):
        print 'record_fpath:(update).....%s....' % record_fpath
        objdata = {}
        objdata['mark'] = 'update'
        objdata['record_fpath'] = conf.server+ record_fpath
        objdata['channal_uuid'] = channal_uuid
        jsonStr = json.dumps(objdata)
        # logger.info('------jsonstr-----%s'%jsonStr)
        rabbitmq.rabbitmqClint(jsonStr)

    def record_chat_run(self, who, text, record_fpath, create_at, call_id, jsonStr):
        print  'record_fpath(record):.....%s....'%record_fpath
        objdata = {}
        objdata['mark'] = 'insert'
        objdata['who'] =who
        objdata['text'] =text
        objdata['record_fpath'] =conf.server+ record_fpath
        objdata['create_at'] =create_at
        objdata['call_id'] =call_id
        objdata['jsonStr'] =jsonStr
        jsonStr = json.dumps(objdata)
        # logger.info('------jsonstr-----%s' % jsonStr)
        rabbitmq.rabbitmqClint(jsonStr)

    def user_analysis(self,user_label):
        print '-----user_analysis -------user_label  %s'%user_label
        objdata = {}
        objdata['mark'] = 'user_label'
        objdata['user_label'] = user_label
        objdata['channal_uuid'] = self.channal_uuid
        jsonStr = json.dumps(objdata)
        # logger.info('------jsonstr-----%s'%jsonStr)
        rabbitmq.rabbitmqClint(jsonStr)


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
                logger.error('flow return text %s' % text)
                #新增 用户意向标签 需要存储数据库
                if item.has_key('user_label'):
                    user_label = item['user_label']
                    print  ' start.... user_label .... %s'%user_label
                    self.user_analysis(user_label)
                    print  ' end.... user_label .... %s' % user_label

                if item['output_resource'] != '':
                    filename = "{0}".format(item['output_resource'])
                    path = self.bot_audio+filename
                    logger.info('-------------playback  %s' % filename)
                    self.session.execute("playback", path)
                    realy_file_path = path.split('recordvoice')
                    self.record_chat_run('bot', text, realy_file_path[1], create_at, self.fs_call_id, jsonStr)
                else:
                    ss_flag = self.flow_id+'_'+text
                    ss_key = Md5Utils.get_md5_value(ss_flag)
                    if text == None:
                        logger.info(' *********flow return  output is None *********')
                        self.record_chat_run('bot', ' ', '', create_at, self.fs_call_id, jsonStr)
                        self.bot_flow('')
                    elif redis.r.has_name(ss_key):
                        filename = redis.r.hget(ss_key)
                        logger.info('...... get-cache ........%s' % filename)
                        self.session.execute("playback", filename)
                        realy_file_path = filename.split('recordvoice')
                        self.record_chat_run('bot', text, realy_file_path[1], create_at, self.fs_call_id, jsonStr)
                    else:
                        self.playback_status_voice(text, jsonStr)
                if item['session_end'] or item['flow_end']:
                    self.session.hangup()
        else:
            logger.info('error.......Flow error: err_no   %s'%jsonStr)
            self.session.hangup()

    def playback_status_voice(self, text, jsonStr):
        create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file_out = self.caller_out_mp3.format(self.out_count, self.__sessionId)
        self.out_count += 1
        filename = self.get_voice_wav(text, file_out)
        if filename:
            ss_flag = self.flow_id + '_' + text
            key =Md5Utils.get_md5_value(ss_flag)
            logger.info('......setCache....%s'%key)
            redis.r.hset(key,filename)
            self.session.execute("playback", filename)
            realy_file_path = filename.split('recordvoice')
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
            cmd = "200 400 {0} 5000 10000 0".format(filename)
            self.session.execute("vad", cmd)
            endTime = time.time()
            logger.error("vad  time  : %s " % (endTime - startTime))
            flag = self.session.getVariable(b"vad_timeout")
            logger.error('record file .....%s'%filename)
#--------------------------------xunfei   asr --------------------------------------------sino_asr
            # if cmp(flag, 'true') != 0:
            #     startTime = time.time()
            #     info = xunfei_asr.vc.getText(filename)
            #     endTime = time.time()
            #     logger.error("xunfei asr time  : %s " % (endTime - startTime))
            #     if info['ret'] == 0:
            #         input = ''.join(info['result'])
            #         logger.error('xunfei asr result ---%s ' % input)
            #         realy_file_path = filename.split('recordvoice')
            #         self.record_chat_run('human', input, realy_file_path[1], create_at, self.fs_call_id, json.dumps(info))
            #         self.bot_flow(input)#需要返回文本信息
            #     else:
            #         realy_file_path = filename.split('recordvoice')
            #         self.record_chat_run('human', '', realy_file_path[1], create_at, self.fs_call_id,json.dumps(info))
            #         self.bot_flow('')  # 需要返回文本信息
            #         logger.error("......xunfei  asr ....is ERROR...........%s"%json.dumps(info))
            # else:
            #     logger.error('vad......没有检测到声音')
            #     self.record_chat_run('human', '', '', create_at, self.fs_call_id, 'vad 没有检测到声音')
            #     self.bot_flow('')  # 需要返回文本信息
# --------------------------------sino_asr   asr --------------------------------------------
            if cmp(flag, 'true') != 0:
                startTime = time.time()
                info = sino_asr.trans.asr_text(filename)
                endTime = time.time()
                logger.error("sino_asr asr time  : %s " % (endTime - startTime))
                if info['ret'] == 0:
                    input = ''.join(info['result'])
                    logger.error('sino_asr asr result ---%s ' % input)
                    realy_file_path = filename.split('recordvoice')
                    self.record_chat_run('human', input, realy_file_path[1], create_at, self.fs_call_id,
                                         json.dumps(info))
                    self.bot_flow(input)  # 需要返回文本信息
                else:
                    realy_file_path = filename.split('recordvoice')
                    self.record_chat_run('human', '', realy_file_path[1], create_at, self.fs_call_id,
                                         json.dumps(info))
                    self.bot_flow('')  # 需要返回文本信息
                    logger.error("......sino_asr  asr ....is ERROR...........%s" % json.dumps(info))
            else:
                logger.error('vad......没有检测到声音')
                self.record_chat_run('human', '', '', create_at, self.fs_call_id, 'vad 没有检测到声音')
                self.bot_flow('')  # 需要返回文本信息

    def run(self):
        self.session.answer()
        self.session.setVariable("set_audio_level", "write +2")
        self.caller_in_wav = self.human_audio+'%s_in_{0}_{1}.wav' % self.caller_number
        self.caller_out_mp3 = self.bot_audio+'%s_out_{0}_{1}.mp3' % self.caller_number
        self.call_full_wav = self.all_audio+'%s_full_{0}_.wav' % self.caller_number
        full_path = self.call_full_wav.format(self.__sessionId)
        self.session.setVariable("RECORD_STEREO", "true")
        self.session.execute("record_session", full_path)
        #'/home/callcenter/recordvoice/{0}/all_audio/'
        realy_full_path = full_path.split('recordvoice')
        self.update_full_path(realy_full_path[1], self.channal_uuid)
        while self.session.ready():
            self.bot_flow('你好')
            self.IVR_app()

def handler(session, args):
    session.setHangupHook(hangup_hook)
    ivr = IVRBase(session,args)
    ivr.run()
