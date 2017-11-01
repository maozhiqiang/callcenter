# -*- encoding: utf-8 -*-
import io
import os
import json
import time
import wave
import voice_api
import datetime
import AI_chat
import WebAPI as xunfei_asr
from pydub import AudioSegment
from LogUtils import Logger
from freeswitch import *
import subprocess
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
        # self.caller_number = None
        self.caller_number = self.session.getVariable("caller_id_number")
        self.caller_in_wav = None
        self.caller_out_mp3 = None
        self.call_full_wav = None
        self.text = None
        self.record_fpath = None
        self.create_at = None
        self.status = status
        self.init_voice = '/home/callcenter/recordvoice/callIn/{0}/'
        self.human_audio = '/home/callcenter/recordvoice/callIn/human_audio/'
        self.all_audio = '/home/callcenter/recordvoice/callIn/all_audio/'
        self.bot_audio = '/home/callcenter/recordvoice/callIn/bot_audio/'
        self.init_file_path()

    def init_file_path(self):

        self.__sessionId = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.init_voice =self.init_voice.format(self.status)
        self.human_audio = self.human_audio.format(self.__sessionId)
        self.all_audio = self.all_audio.format(self.__sessionId)
        self.bot_audio = self.bot_audio.format(self.__sessionId)

        if not os.path.exists(self.init_voice):
            os.makedirs(self.init_voice)
        if not os.path.exists(self.human_audio):
            os.makedirs(self.human_audio)
        if not os.path.exists(self.bot_audio):
            os.makedirs(self.bot_audio)
        if not os.path.exists(self.all_audio):
            os.makedirs(self.all_audio)

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

    def get_voice(self, status=None):
        if not status:
            status = self.status
        filename = self.init_voice+'callIn.mp3'
        r = voice_api.bc.tts(self.STATUS_MAP[status], filename)
        if r == 0:
            filename_wav = self.converTowav(filename)
            return filename_wav
        else:
            consoleLog('error', 'baidu tts error: %d' % r['err_no'])
            return None

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

    def IVR_app(self):
        while self.session.ready():
            startTime = time.time()
            create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            filename = self.caller_in_wav.format(self.in_count, self.__sessionId)
            self.in_count += 1
            cmd = "100 400 {0} 4000 10000 100".format(filename)
            try:
                self.session.execute("vad", cmd)
            except Exception as e:
                print e.message
            endTime = time.time()
            logger.error("vad  time  : %s " % (endTime - startTime))
            flag = self.session.getVariable(b"vad_timeout")
            logger.error('record file .....%s' % filename)
            # --------------------------------xunfei   asr --------------------------------------------
            if cmp(flag, 'true') != 0:
                startTime = time.time()
                info = xunfei_asr.vc.getText(filename)
                endTime = time.time()
                logger.error("xunfei asr time  : %s " % (endTime - startTime))
                if info['ret'] == 0:
                    input = ''.join(info['result'])
                    logger.error('xunfei asr result ---%s ' % input)
                    info = AI_chat.passive_chat(input)
                    self.playback_tts_voice(info)
                else:
                    info = AI_chat.passive_chat('')
                    self.playback_tts_voice(info)
                    logger.info("......xunfei  asr ....error...........%s" % json.dumps(info))
            else:
                logger.info('vad......没有检测到声音')
                info = AI_chat.passive_chat('')
                self.playback_tts_voice(info)

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
                filename = self.get_voice()
                self.session.execute("playback", filename)
                self.status = 'trans_bot'
                self.IVR_app()
            elif self.status == 'exit':
                self.session.hangup()

def handler(session, args):
    session.setHangupHook(hangup_hook)
    ivr = IVRBase(session, args)
    ivr.run()

