
# -*- encoding: utf-8 -*-
import ESL
con = ESL.ESLconnection('localhost', '8021', 'Aicyber')  #通过ESL与freeswitch建立连接
if con.connected:
    con.events('plain', 'CHANNEL_CREATE CHANNEL_ANSWER CHANNEL_PROGRESS CHANNEL_PROGRESS_MEDIA CHANNEL_HANGUP')
    while 1:
        e = con.recvEvent()
        print 'event json  \n\n', e.serialize('json')
        event_name = e.getHeader("Event-Name")
        if event_name in ["CHANNEL_CREATE"]:
            unique_id = e.getHeader("unique-id")
            caller = e.getHeader("Caller-Caller-ID-Number") #主叫 按照事情进行获取消息字段中的值
            callee = e.getHeader("Caller-Destination-Number") #被叫
            con.execute("ring_ready", "", unique_id)
        elif (event_name in ['SERVER_DISCONNECTED']):
            break