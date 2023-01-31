# author Boyang Cao
# version 0.1
# update date 2020-3-16
# mod date record 2020-3-16 version 0.1 Linlin Liu

import math
import numpy as np
from rebin import rebin


def Scale_Pts_alongAxis(Pts, axis2, scale, outputMatrix=''):
    r"""
    PURPOSE:
        scale a 3D point set along an arbitray axis
        沿任意轴缩放三维点集
    CATEGORY:
        basic mesh processing

    INPUT:
        Pts: point set to be scaled, assuming the input points are already centered
             点集要缩放，假设输入点已经居中
        axis: the vector of the axis
              轴的向量
        scale: the scaling factor
               比例因子

    KEYWORDS:
        outputMatrix: if set, output the transform matrix instead of the resultant point set
        outputMatrix: 如果设置，则输出转换矩阵，而不是生成的点集
    OUTPUT:
        Pts1: point set after rotation
        Pts1: 旋转后的点集

    Example::
        >>> a = np.array([[1, 1, 2, 3], [2, 3, 1, 2], [1, 3, 1, 1]])
        >>> axis2 = np.array([[3], [4], [0]])
        >>> t = 3
        >>> Pts1 = Scale_Pts_alongAxis(a, axis2, t)
        >>> print(Pts1)
        >>> transform_matrix = Scale_Pts_alongAxis(a, axis2, t, outputMatrix='outputMatrix')
        >>> print(transform_matrix)
    """
    # normalize the axis vector
    axis1 = axis2;
    norm_axis = sum(axis2 ** 2)
    if abs(norm_axis - 1.0) > 1e-12:
        axis1 = axis2 / math.sqrt(norm_axis)

    # do scaling
    if not outputMatrix:
        # project the points onto the axis
        num_Pts = len(np.transpose(Pts))
        AX = rebin(axis1, (3, num_Pts))
        pp = (Pts * AX).sum(axis=0).reshape(num_Pts, 1)
        Pts1 = Pts + AX * np.transpose(rebin((scale - 1) * pp, (num_Pts, 3)))
        return np.transpose(Pts1)
    else:
        Tsfm = np.eye(4)
        Tsfm[0:3, 0:3] = np.eye(3) + (scale - 1) * np.dot(axis1, np.transpose(axis1))
        return Tsfm