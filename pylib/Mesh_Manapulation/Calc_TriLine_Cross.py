# author Boyang Cao
# version 0.1
# update date 2020-3-18
# mod date record 2020-3-18 version 0.1 Linlin Liu

import numpy as np
import math
from numpy import *
from rebin import rebin


def Calc_TriLine_Cross(Verts, TRI, Src, Vect, lmax=''):
    r"""
    PURPOSE:
         Calcuate the intersection of triangle patches and line set 计算三角形面片和线集的交点

    CATEGORY:
         line and triangle

    INPUT:
         Verts: the [3,m] vertices of the triangular mesh
                三角形网格的顶点[3,m]
         TRI: the [3,m] index array of the triangluar patches
              三角片的[3,m]索引数组
         Src: the [3,n] point set of source points of the line set
              行集合的源点集合[3,n]
         Vect: the [3,n] vector set of the line vectors, vects should be normalized already.
               直线向量的向量集[3,n]应该已经被标准化了。
               Src and Vect together describe n lines, starting from Src and pointing into the direction of Vect
               Src和Vect共同描述n条线，从Src开始，指向Vect的方向
         lmax: the maximum searching distance of t for each ray
               t对每条射线的最大搜索距离

    RETURNED VALUES:
        tMat: an [m,n] array of the t value for the intersection, if the line j intersects with triangle i, then
              tMat[i,j] is the t value of intersection, otherwise tMat[i,j] is -1e10;
              一个[m,n]数组的t值的交集.如果直线j与三角形i相交，则tMat[i,j]为交集的t值，否则tMat[i,j]为-1e10;
    Example::
        >>> a = np.array([[1.5, 1, 2],
                          [2, 3, 3],
                          [0, 3, 1],
                          [2.5, 1, 2]])
        >>> b = np.array([[0, 1, 2],
                          [1, 0, 3],
                          [3, 2, 0],
                          [1, 2, 3]])
        >>> src = np.array([[0, 1, 2],
                          [1, 3, 3],
                          [0, 2, 3]])
        >>> v = np.array([[0, 1, 0],
                          [1, 0, 0],
                          [0, 0, 1]])
        >>> lmax = 3
        >>> tMat = Calc_TriLine_Cross(a, b, src, v, lmax)
    """
    print("ff..")
    if lmax:
        lmax = lmax
    else:
        lmax = 1e30

    num_Verts = len(Verts)  # 三角形顶点个数
    num_TRI = len(TRI)  # 三角形个数（索引地址）
    num_Src = len(Src)  # 直线向量的源点个数

    # each triangular patch will be constructed into a 3D coordinate system,
    # with the first vertex as the origin, the first edge as the x axis, the normal as the z axis
    # 每个三角形的patch被构造成一个3D坐标系，以第一个顶点为原点，第一个边为x轴，法线为z轴
    o = Verts[TRI[:, 0], :]  # 每个三角形的第一个顶点作为该3D坐标系的原点
    v1 = Verts[TRI[:, 1], :] - Verts[TRI[:, 0], :]  # the first edge, 第一、二个顶点的边
    v2 = Verts[TRI[:, 2], :] - Verts[TRI[:, 0], :]  # the second edge, 第一、三个顶点的边
    n = mat(zeros((num_TRI, 3)))  # the normal vector, i.e. the z axis 法向量，也就是z轴

    for iT in range(0, num_TRI):
        n[iT, :] = np.cross(v1[iT, :], v2[iT, :])  # 求向量积

    n2 = np.multiply(n, n)
    n = n / rebin((np.sqrt(n2.sum(axis=1))), (num_TRI, 3))
    v12 = np.multiply(v1, v1)
    v22 = np.multiply(v2, v2)
    a = np.sqrt(v12.sum(axis=1))
    b = np.sqrt(v22.sum(axis=1))
    ab = a * b
    fenmu = v1[:, 0] * v2[:, 1] - v1[:, 1] * v2[:, 0]

    # for each vert, calcuate the intersection points 对于每个点，计算交点
    t_Mat = mat(zeros((num_TRI, num_TRI))) - 1e10
    for iT in range(0, num_TRI):
        oi = np.transpose(rebin(o[iT, :].reshape(3, 1), (3, num_Src)))
        ni = np.transpose(rebin(n[iT, :].reshape(3, 1), (3, num_Src)))
        v_1 = np.transpose(rebin(v1[iT, :].reshape(3, 1), (3, num_Src)))
        v_2 = np.transpose(rebin(v2[iT, :].reshape(3, 1), (3, num_Src)))

        t1 = (np.multiply((oi - Src), ni).sum(axis=1))
        t2 = (np.multiply(Vect, ni).sum(axis=1))
        t = t1 / t2
        ind_valids = np.where(abs(t) < lmax)
        ind_valid = ind_valids[0]

        if ind_valid[0] != -1:
            num_valid = len(ind_valid)  # 获取数组元素个数
            c = Src[ind_valid, :] + rebin(np.transpose(t[ind_valid]), (num_valid, 3)) * Vect[ind_valid, :]
            P = c - oi[ind_valid, :]
            p0 = P[:, 0]
            v21 = v_2[ind_valid, 1].reshape(num_valid, 1)
            p1 = P[:, 1]
            v20 = v_2[ind_valid, 0].reshape(num_valid, 1)
            p1 = P[:, 1]
            v10 = v_1[ind_valid, 0].reshape(num_valid, 1)
            p0 = P[:, 0]
            v11 = v_1[ind_valid, 1].reshape(num_valid, 1)
            u = a[iT] * (np.multiply(p0, v21) - np.multiply(p1, v20)) / fenmu[iT]
            v = b[iT] * (np.multiply(p1, v10) - np.multiply(p0, v11)) / fenmu[iT]
            ind_cross = np.where((a[iT] * v + b[iT] * u <= ab[iT]) & (u >= 0) & (v >= 0))[0]
            ind_cross = ind_valid[ind_cross]
            t = t.reshape(1, num_Src)
            t_Mat[iT, ind_cross] = t[0, ind_cross]
    return t_Mat


