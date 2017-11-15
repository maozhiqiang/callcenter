#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
from numpy import *


def create_random():
    # 生成4x4数组
    array = random.rand(4,4)
    print '\n生成4*4数组'
    print array
    #生成4*4矩阵
    randMat = mat(random.rand(4,4))
    print '\n生成4*4 矩阵，.I是矩阵求逆操作'
    print randMat.I

    invRandMat = randMat.I
    print '\n执行矩阵的乘法运算'
    myEye =   invRandMat * randMat
    print myEye
    print '\n 有误差，得到误差'
    result = myEye - eye(4)
    print result


if __name__ == '__main__':
    create_random()
