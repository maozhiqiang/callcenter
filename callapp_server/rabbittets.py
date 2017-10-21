# -*- encoding: utf-8 -*-

import rabbitMQ_produce as rabbitmq
import json
sql = 'INSERT INTO fs_call_replay(who, text, record_fpath,  call_id,resp_param)VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'.format(
            45, 454, 454, 454, 4545, 4545)
# print '.....0......%s'%sql
#
# objdata = {}
# objdata['mark'] = 'update'
# objdata['record_fpath'] = '78978'
# objdata['channal_uuid'] = 'a6d24d2d-cebe-4113-9f89-9ce80012d6fc'
# jsonStr = json.dumps(objdata)
# print '------jsonStr-uu-----', jsonStr
# rabbitmq.rabbitmqClint(jsonStr)
import commands
file_mp3 = '/home/callcenter/recordvoice/5a1c9c5a87183c7e586b38cded8394f2/bot_audio/15900282168_out_0_20170907183230.mp3'
file_wav = '/home/callcenter/recordvoice/5a1c9c5a87183c7e586b38cded8394f2/bot_audio/15900282168_out_0_20170907183230.wav'


cmd = 'faad -w -f 2 '+file_mp3+' | sox -V -t raw -r 8000 -b 16 -c 1 -e signed - /home/callcenter/recordvoice/5a1c9c5a87183c7e586b38cded8394f2/bot_audio/whc_test_maptowav_.wav'
#cmd = 'sox ' + file_mp3 + ' -r 16000 ' + '/home/callcenter/recordvoice/5a1c9c5a87183c7e586b38cded8394f2/bot_audio/test_111.wav'
# cmd = 'sox   '+ file_wav + '  -r 8000 -c 1 -e signe /home/callcenter/recordvoice/5a1c9c5a87183c7e586b38cded8394f2/bot_audio/whc_text_wav.wav'
out = commands.getoutput(cmd)
print '-*-*-*-*-',out