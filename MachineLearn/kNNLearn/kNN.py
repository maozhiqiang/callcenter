#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
from numpy import *

'''
我觉得可以这样理解，每一种方括号都是一个维度（秩）
这里就是二维数组，最里面括着每一行的有一个方括号，后面又有一个，就是二维，四行
'''
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0],
                   [0, 0.1]])

    labels = ['A', 'A', 'B', 'B']
    return group, labels

'''
# inX是你要输入的要分类的“坐标”，
  dataSet是上面createDataSet的array，就是已经有的，分类过的坐标，
  label是相应分类的标签，
  k是KNN，k近邻里面的k
'''
def classify0(inX, dataSet, labels,k):

    '''dataSetSize是sataSet的行数，用上面的举例就是4行'''
    dataSetSize = dataSet.shape[0]
    # 前面用tile，把一行inX变成4行一模一样的（tile有重复的功能，
    # dataSetSize是重复4遍，后面的1保证重复完了是4行，而不是一行里有四个一样的）
    # ，然后再减去dataSet，是为了求两点的距离，先要坐标相减，这个就是坐标相减
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    # print 'inX\n' ,tile(inX, (dataSetSize,1))
    # print  'dataSet \n',dataSet
    # print '坐标相减、\n',diffMat

    # 上一行得到了坐标相减，然后这里要(x1-x2)^2，要求乘方
    sqDiffMat = diffMat ** 2
    # print '欧式距离公式----,先(x1-x2)^2 \n',sqDiffMat
    # axis=1是列相加，，这样得到了(x1-x2)^2+(y1-y2)^2
    sqDistances = sqDiffMat.sum(axis=1)
    # print '欧式距离公式----,求和 \n\n', sqDistances
    distances = sqDistances ** 0.5
    # print '欧式距离公式----,开根号 \n\n', distances
    # argsort是排序，将元素按照由小到大的顺序返回下标，比如([3,1,2]),它返回的就是([1,2,0])
    sortedDistIndicies = distances.argsort()
    # print '欧式距离公式----,排序 \n\n', distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        # get是取字典里的元素，如果之前这个voteIlabel是有的，那么就返回字典里这个voteIlabel里的值，
        # 如果没有就返回0（后面写的），
        # print '\n\n...voteIlabel..',voteIlabel
        # 这行代码的意思就是算离目标点距离最近的k个点的类别，这个点是哪个类别哪个类别就加1
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        # print '...classCount[voteIlabel]..', classCount[voteIlabel]
        # key=operator.itemgetter(1)的意思是按照字典里的第一个排序，
        # {A:1,B:2},要按照第1个（AB是第0个），即‘1’‘2’排序。reverse=True是降序排序
    soredClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1),reverse=True)
    return soredClassCount[0][0]  # 返回类别最多的类别


# 将文本记录到转换numPy的解析程序
def file2matrix(filename):
    #打开文件并得到文件行数
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    #创建返回的numPy矩阵
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index =0
    #解析文件数据到列表
    for line in arrayOLines:
        line = line.strip()
        listFormLine = line.split('\t')
        returnMat[index,:] = listFormLine[0:3]
        classLabelVector.append(int(listFormLine[-1]))
        index += 1
    return returnMat, classLabelVector

#归一化特征值
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet, ranges, minVals
