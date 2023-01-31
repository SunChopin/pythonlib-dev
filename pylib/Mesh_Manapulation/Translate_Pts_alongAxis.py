# author Boyang Cao
# version 0.1
# update date 2020-3-16
# mod date record 2020-3-16 version 0.1 Linlin Liu

import math
import numpy as np
from rebin import rebin


def Translate_Pts_alongAxis(Pts, axis2, t, outputMatrix=''):
    r"""
    PURPOSE:
        translate the point set along a certain axis 沿某条轴平移点集

    CATEGORY:
        mesh transformation, mesh deformation  网格变换，网格变形

    INPUTS:
        Pts: point set to be scaled, assuming the input points are already centered
             点集要缩放，假设输入点已经居中
        axis: the vector of the axis  轴的向量
        t: the distance of translation 平移距离

    KEYWORDS:
        outputMatrix: if set, output the transform matrix instead of the resultant points
                      如果设置，输出变换矩阵而不是合成点

    OUTPUT:
        Pts1:  point set after translation 平移后点集

    Example::
        >>> a = np.array([[0, 1, 2, 2], [2, 3, 1, 2], [1, 3, 1, 2]])
        >>> axis2 = np.array([[1], [1], [0]])
        >>> t = math.sqrt(2)
        >>> Pts1 = Translate_Pts_alongAxis(a, axis2, t)
        >>> print(Pts1)
        >>> outputMatrix = Translate_Pts_alongAxis(a, axis2, t, outputMatrix='outputMatrix')
        >>> print(outputMatrix)

    """
    # normalize the axis vector
    axis1 = axis2
    norm_axis = sum(axis2 ** 2)

    if abs(norm_axis - 1.0) > 1e-12:
        axis1 = axis2 / math.sqrt(norm_axis)

    # do translation
    if not outputMatrix:
        num_Pts = len(np.transpose(Pts))
        print(num_Pts)
        Pts1 = Pts + rebin(t * axis1, (3, num_Pts))
        return np.transpose(Pts1)
    else:
        Tsfm = np.eye(4)
        Tsfm[3, 0:3] = t * np.transpose(axis2)
        return Tsfm