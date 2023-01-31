# author Gaoli Zhang
# version 0.1
# update date 2020-3-22
# mod date record 2020-3-22 version 0.1 Linlin Liu

import numpy as np
import ctypes


def Pts_XOR(Pts0, Pts1, d_th):
    r"""
    PURPOSE:
        point set XOR

    CATEGORY:
        asic mesh processing

    INPUTS:
        Pts0,Pts1, the point set to do XOR
        d_th, the distance threshold for XOR

    OUTPUT:
        Delist0: a bool vector whose length is equal to the number of points in Pts0, Delist0[i] eq 1 means delted
        Delist1: similar as above, but for Pts1

    Example::
        a = np.array([[1, 1, 2],
                      [2, 3, 1],
                      [1, 3, 1],
                      [3, 1, 1]])
        b = np.array([[1, 1, 2],
                      [2, 1, 1],
                      [1, 3, 1],
                      [3, 1, 1]])
    print(Pts_XOR(a, b, 1))
    """
    dll = ctypes.windll.LoadLibrary('E:/Pts_XOR.dll')
    #dll = ctypes.cdll.LoadLibrary('E:/Pts_XOR.dll')
    numPts0 = len(Pts0)
    numPts1 = len(Pts1)
    Delist0 = np.zeros(numPts0)
    Delist1 = np.zeros(numPts1)
    flow = dll.Pts_XOR(float(Pts0), float(Pts1), float(d_th^2), float(numPts0), float(numPts1), float(Delist0), float(Delist1))

    return Delist0, Delist1, flow



