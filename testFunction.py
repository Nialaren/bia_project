from PyQt4 import QtCore, QtGui
import numpy as np
import math


def firstDeJong(basicPlane):
    result = 0
    for dim in basicPlane:
        result += dim**2
    return result


def rosenbrocksSaddle(data):
    result = None
    for i in range(len(data)-1):
        if(result is None):
            result = ((100 * (data[i]**2 - data[i+1])**2) + (1 - data[i])**2)
        else:
            result += ((100 * (data[i]**2 - data[i+1])**2) + (1 - data[i])**2)
    return result


def thirdDeJong(data):
    result = None
    for dim in data:
        if(result is None):
            result = abs(dim)
        else:
            result += abs(dim)
    return result


def forthDeJong(data):
    result = None
    for i in range(len(data)):
        if(result is None):
            result = (i+1) * data[i]**4
        else:
            result += (i+1) * data[i]**4
    return result


def rastrigin(data):
    result = None
    count_dim = len(data)
    for x in data:
        if(result is None):
            result = x**2 - (10 * np.cos((2*np.pi*x)))
        else:
            result += x**2 - (10 * np.cos((2*np.pi*x)))
    return 2*count_dim*result


def schewefel(data):
    result = None
    for x in data:
        if(result is None):
            result = (-x) * np.sin(np.sqrt(abs(x)))
        else:
            result += (-x) * np.sin(np.sqrt(abs(x)))
    return result


def griewangkova(data):
    result_sum = None
    result_mult = None
    for i in range(len(data)):
        if(result_sum is None):
            result_sum = (data[i]**2)/4000
            result_mult = np.cos(data[i]/np.sqrt((i+1)))
        else:
            result_sum += (data[i]**2)/4000
            result_mult *= np.cos(data[i]/np.sqrt((i+1)))
    return 1 + result_sum - result_mult


def sineEnvelope(data):
    result_sum = None
    for i in range(len(data)-1):
        x1 = data[i]**2
        x2 = data[i+1]**2
        if(result_sum is None):
            result_sum = 0.5 + (np.sin(x1 + x2 - 0.5)**2  /  (1+0.001*(x1 + x2))**2)
        else:
            result_sum += (0.5 + (  (np.sin(x1 + x2 - 0.5)**2)  /  (1+0.001*(x1 + x2))**2 ))
    return -1 *result_sum


def sineWave(data):
    result = None
    for i in range(len(data)-1):
        x1 = data[i]**2
        x2 = data[i+1]**2
        if(result is None):
            result = ((np.sqrt(np.sqrt(x1 + x2))) * np.sin((50 * (x1 + x2)**0.1))**2 + 1)
        else:
            result += ((np.sqrt(np.sqrt(x1 + x2))) * np.sin((50 * (x1 + x2)**0.1))**2 + 1)

    return result


# def MultiPurposeFnc(X1, X2=None, f=20, gs=11, gss=12, z_corrector=1):
#     # print X1
#     X1 = X1[0]
#     Z = [None] * len(X1)
#     for i in range(len(X1)):
#         Z[i] = []
#         for j in range(len(X1[i])):
#             Z[i].append(__multi_purpose_function(X1[i][i], X1[i][j], f) * z_corrector)
#
#
# def __multi_purpose_function(x1, x2, f, gs=11, gss=12):
#     print x1
#     print x2
#     alpha = 0.25 + 3.75*(10 * x2 - gss)/(gs-gss)
#     tmp1 = x1 / 10 * x2
#     h = tmp1**alpha - tmp1 * math.sin(math.pi * f * x1 * 10 * x1)

    # return h

class MultiPurposeFnc(object):
    NAME = 'multi_purpose_function'
    MAX_X = 1
    MIN_X = 0
    DEFAULT_STEP = 0.1

    @staticmethod
    def f1(x1):
        return x1

    @staticmethod
    def g(x2):
        return 10 + x2

    @staticmethod
    def function(x1, x2, F=20, gs=11, gss=12):
        alfa = 0.25 + 3.75*((MultiPurposeFnc.g(x2)-gss)/(gs-gss))
        tmp1 = MultiPurposeFnc.f1(x1) / MultiPurposeFnc.g(x2)
        h = tmp1**alfa - tmp1 * math.sin(math.pi * F * MultiPurposeFnc.f1(x1) * MultiPurposeFnc.g(x1))

        return h

    @staticmethod
    def graph_z(X1, X2, F=1, z_corrector=1):
        Z = [None] * len(X1)
        for i in range(len(X1)):
            Z[i] = []
            for j in range(len(X2)):
                Z[i].append(MultiPurposeFnc.function(X1[i], X2[j], F) * z_corrector)
        return Z

    @staticmethod
    def generate_default():
        x = np.arange(MultiPurposeFnc.MIN_X, MultiPurposeFnc.MAX_X, MultiPurposeFnc.DEFAULT_STEP)
        return (x,x)

    @staticmethod
    def get_widget(parent=None):
        root = QtGui.QWidget(parent)
        layout = QtGui.QFormLayout()

        #Controlls
        frequencyInput = QtGui.QLineEdit()
        submitBtn = QtGui.QPushButton()
        submitBtn.setText('apply')
        label = QtGui.QLabel('frequency')

        # add all to layout
        layout.addRow(label, frequencyInput)
        layout.addWidget(submitBtn)
        root.setLayout(layout)

        root.onBtnClick = lambda fn: submitBtn.pressed.connect(fn)
        root.getFrequency = frequencyInput.text
        return root
