# -*- coding: UTF-8 -*-

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


if __name__ == '__main__':

    # dct = {u'status': 0, u'result': None}
    # print dct['status']
    list_params = []
    list_params.append(1)
    list_params.append(2)
    list_params.append('a1.wav')
    print(list_params)