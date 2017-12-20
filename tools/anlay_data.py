#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-20 下午3:09
# @Author  : Arvin
# @Site    : 
# @File    : anlay_data.py
# @Software: PyCharm

import json

def modify_data():
    info_json = '{"info": [{"is_flow_output": true, "node_text": "\u505a\u751f\u610f", ' \
                '"flow_id": "5e19d87e7ba42eaa08687abf28695f93",' \
                '"user_label":"意向客户"'\
                ' "output": "\u8425\u4e1a\u6267\u7167\u662f\u5426\u6ee1\u4e00\u5e74\u4e86\u5462?\u60a8\u662f\u6cd5\u4eba\u8fd8\u662f\u80a1\u4e1c\u5462\uff1f",' \
                ' "session_end": false, "state": "", "node_id": -8, "output_resource": "g17.wav", "flow_end": false, "input": "\u6211\u81ea\u5df1\u505a\u5546\u4eba\u3002", ' \
                '"flow_title": "\u5de5\u4f5c\u6761\u4ef6", "output_type": "path", "id": "5e19d87e7ba42eaa08687abf28695f93_-8"}], "successful": true, "message": "ok"}'

    jsonStr = json.dumps(info_json)
    print type(info_json)

if __name__ == '__main__':
    modify_data()