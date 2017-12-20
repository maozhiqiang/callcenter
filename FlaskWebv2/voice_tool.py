#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-13 下午2:45
# @Author  : Arvin
# @Site    : 
# @File    : voice_tool.py
# @Software: PyCharm

from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer
from util import atc
from pypinyin import lazy_pinyin
import pypinyin
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent

PUNCTUATION = ['，', '、', '。','？','！','“','”','；','：','（',"）",":",";",",",".","?","!","\"","\'","(",")"]


def text2pinyin(syllables):
    temp = []
    for syllable in syllables:
        # if syllable.isdigit():
        try:
            syllable = atc.num2chinese(syllable)
            new_sounds = lazy_pinyin(syllable, style=pypinyin.TONE2)
            for e in new_sounds:
                temp.append(e)
        except:
            for p in PUNCTUATION:
                syllable = syllable.replace(p, "")
            temp.append(syllable)
    return temp

class TextToSpeech():
    def __init__(self):
        print(hparams_debug_string())
        self.synth = Synthesizer()
        self.synth.load('./logs-tacotron/model.ckpt-52000')

    def speech_connect(self,*speeches):
        print('---------0----------')
        result = AudioSegment.silent(duration=100)
        for speech in speeches:
            if type(speech) == str:
                print('synthesize: ',speech)
                syllables = lazy_pinyin(speech, style=pypinyin.TONE2)
                print('---------1 ' ,speech,'----------')
                syllables = text2pinyin(syllables)
                text = ' '.join(syllables)
                bytewav = self.synth.synthesize(text)
                result += AudioSegment.from_file(bytewav, format='wav')
            elif type(speech) == AudioSegment:
                print('--------- audio----------')
                result += self.cutspeech(speech)

        return result

    def cutspeech(self, song1):
        not_silence_ranges = detect_nonsilent(song1, min_silence_len=100, silence_thresh=-32)
        starti = not_silence_ranges[0][0]
        if len(not_silence_ranges) == 0:
            return song1

        endi = not_silence_ranges[-1][1]
        return song1[starti:endi]

# if __name__ == '__main__':
#     tts = TextToSpeech()
#     a = AudioSegment.from_wav('/mnt/audio_wav/A1.wav')
#     c = AudioSegment.from_wav('/mnt/audio_wav/A2.wav')
#     b = '檀玉飞'
#     bb = tts.speech_connect(b,a,c).set_frame_rate(16000)
#     bb.export('./audio/text_1111.wav', format='wav')
