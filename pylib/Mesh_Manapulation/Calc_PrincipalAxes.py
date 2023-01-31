# author Haoyue Ao
# version 0.1
# update date 2020-3-17
# mod date record 2020-3-17 version 0.1 Linlin Liu

import numpy as np
import math
from rebin import rebin


def Calc_PrincipalAxes(Pts, isDisp='', last_axes='', regularize_direction=''):
    r"""
    PURPOSE:
        Compute the principal axies of a 3D point set
        计算3D点集的主轴

    CATEGORY:
        mesh and mesh, spatial transform
        网格与网格之间的空间变换

    INPUTS:
        Pts: the 3xn input point set
             3 x n的输入点集

    KEYWORDS:
        isDisp: bool constant, if display the result or not
                布尔型常量，是否显示result
        regularize_direction: a bool constant, if set, then the code will make sure the axes point to the same directions as the x,y,z axes
                             一个布尔型常量，如果设置，则代码将确保坐标轴指向与x、y、z轴相同的方向
        last_axes: the axis of last step, as a referece of the direction of this step
                   最后一步的坐标轴作为这一步的参考方向

    RETURNED VALUES:
        A structure containing:
       一个结构包含如下
            o:the centroid of Pts
              点集Pts的中心
            Eigenvect and Eigenval: the eigen decomposition result of the input points
                                    输入点集的特征分析结果

    Example::
        >>> a = np.array([[1.5, 1, 2],
                  [2, 3, 3],
                  [0, 3, 1],
                  [2.5, 1, 2]])
        >>> o, Eigenvect, Eigenval = Calc_PrincipalAxes(a)
        >>> print('o:the centroid of Pts')
        >>> print(o)
        >>> print('Eigenvect')
        >>> print(Eigenvect)
        >>> print('Eigenval')
        >>> print(Eigenval)
    """
    num_Pts = len(Pts)
    o = np.sum(Pts, axis=0) / float(num_Pts)
    oo = rebin(o.reshape(3, 1), (3, num_Pts))
    Pts1 = Pts - np.transpose(oo)
    Eigenval, Eigenvect = np.linalg.eig(np.dot(np.transpose(Pts1), Pts1) / num_Pts)
    Eigenvect[2,] = Eigenvect[2,] * np.sign(sum(Eigenvect[2,]) * np.dot(Eigenvect[0,], Eigenval[1,]))

    if isDisp:
        result = Disp_VectorField(np.zeros(3, 3), np.dot(np.diag(math.sqrt(Eigenval)), Eigenvect), Scale=5,
                                  MeshVerts=Pts1, MeshConn=-1, MeshType=0, MeshThick=2)

    # make sure the axes point to the same directions as the x,y,z axes
    if regularize_direction:
        for id in range(0, 3, 1):
            v = Eigenvect[id,]
            maxv = max(abs(v), idmax)
            Eigenvect[id,] = Eigenvect[id,] * np.sign(v[idmax])

    if last_axes:
        for id in range(0, 3, 1):
            v = Eigenvect[id,]
            Eigenvect[id,] = Eigenvect[id,] * np.sign(sum(v * last_axes[id,]))

    return o, Eigenvect, Eigenval




