# -*- coding: UTF-8 -*-
import sqlalchemy

#过滤数据
def filterDictData(clazz, json_dict):
    data_dict = {}
    for key in json_dict.keys():
        if hasattr(clazz, key):
            data = json_dict[key]
            if type(json_dict[key]) == unicode:
                data = data.encode('utf-8')
            data_dict[key] = data
    return data_dict

#字典数据转换到对象属性
def dictToObj(data_dict, obj):
    for key in data_dict.keys():
        if hasattr(obj, key):
            setattr(obj, key, data_dict[key])

#数据对象转换到字典
def dataObjToDict(obj):
    if obj is not None:
        data_dict = {}
        clazz = obj.__class__
        for key in clazz.__dict__:
            if isinstance(clazz.__dict__[key], sqlalchemy.orm.attributes.InstrumentedAttribute):
                data_dict[key] = getattr(obj, key)
        print data_dict
        return data_dict
    else:
        return None