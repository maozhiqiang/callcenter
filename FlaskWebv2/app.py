#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import time
import json
import datetime
from pydub import AudioSegment
print('***************load 0*************')
# import voice_tool
print('***************load 1*************')
from flask import Flask,jsonify
from flask import render_template, redirect,url_for
from flask import request
from flask import make_response , send_file
print('=====load model====')
# tts = voice_tool.TextToSpeech()
print('===load model done =======')

app = Flask(__name__,template_folder='templates',static_folder='', static_url_path='')

STATIC_AUDIO_WAV = '/mnt/audio_wav/'
UPLOAD_PATH = '/mnt/audio_wav/compose_wav/'
@app.route('/',methods=['GET'])
def Index():
    return render_template('voice.html')

@app.route('/aicyber/resource/voice/compose/',methods=['GET','POST'])
def voice_compose():
    print('------',request.json)
    session_Id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if request.method == 'POST':
        templ = request.json['templ_']
        text = request.json['text_']
        select_ = request.json['select_']
        voice_ = request.json['voice_']
        if voice_:
            audio_arr = voice_.split(',')
        '''template  您好___先生，这里是___'''
        # if select_ != None and  select_ != '':
        #     audio = tts.speech_connect(AudioSegment.from_wav(STATIC_AUDIO_WAV + audio_arr[0]), text,
        #                                AudioSegment.from_wav(STATIC_AUDIO_WAV + audio_arr[1])).set_frame_rate(16000)
        # else:
        #     audio = tts.speech_connect(AudioSegment.from_wav(STATIC_AUDIO_WAV + audio_arr[0]), text).set_frame_rate(16000)
        # path = audio.export('/mnt/audio_wav/compose_wav/'+session_Id+'.wav', format='wav')
        # print('********path*******',path)
        return jsonify({'success': True, 'message': u'成功响应', 'data': session_Id+'.wav'})
    else:
        return jsonify({'success': False, 'message': u'请使用POST请求', 'data': None})

@app.route('/aicyber/resource/download/<filename>', methods=['GET'])
def download(filename):
    file =UPLOAD_PATH +filename
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename="+file+";"
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("8089"),debug=True)
    # app.run(host="0.0.0.0", port=int("8089"))
