# author Haoyue Ao, Gaoli Zhang
# version 0.1
# update date 2020-3-17
# mod date record 2020-3-17 version 0.1 Linlin Liu

import numpy as np
from numpy import *
import math
from Quaternion_2_Rotation import Quaternion_2_Rotation


def Rot_Pts_alongAxis(Pts0, axis_rot, angle, outputMatrix='', RotCenter='', RotAlongCentroid=''):
    """
    PURPOSE:
        Rotate a 3D point set by an arbitrary angle along an arbitray axis
        沿任意轴旋转任意角度设置的3D点

    CATEGORY:
        mesh transformation, basic mesh processing
        网格转换，基本的网格处理

    INPUTS:
        Pts: point set to be rotated
             被旋转的点集
        axis_rot: the vector of the axis of rotation
                  旋转轴的矢量
        angle: the angle of rotation, in rad
               旋转角度，以rad为单位

    KEYWORDS:
        outputMatrix: if set to 1, only output the M_Rot, for generalized coordinate (x,y,z,1)
                      如果设置为1，则对于广义坐标(x,y,z,1)只输出M_Rot
        RotCenter: the center for rotation, if not set, use [0,0,0]
                   旋转中心，如果没有设置，则使用[0,0,0]
        RotAlongCentroid: if set, rotate along the centroid of the point set
                          如果设置，则沿点集的质心旋转

    OUTPUT:
         if outputMatrix is not set, return the point set after rotation
         如果未设置outputMatrix，则在旋转之后返回点集
         if outputMatrix is set, return the 4x4 transform matrix, although only the upper 3x3 elements has values
         如果设置了outputMatrix，则返回4x4转换矩阵，尽管只有上面的3x3元素有值

    Example::
        >>> a = np.array([[1.5, 1, 2],
                  [2, 3, 3],
                  [0, 3, 1],
                  [2.5, 1, 2]])
        >>> axis = np.array([1, 0, 0])
        >>> b = (math.pi) / 2
        >>> print(Rot_Pts_alongAxis(a, axis, b, outputMatrix='outputMatrix', RotAlongCentroid='RotAlongCentroid'))
        >>> print(Rot_Pts_alongAxis(a, axis, b, RotCenter=[1, 0, 0]))
    """
    if not outputMatrix:
        Pts = Pts0
        if RotAlongCentroid:
            oo = np.mean(Pts, 0)
            for idim in range(0, 3, 1):
                Pts[:, idim] = Pts0[:, idim] - oo[idim]
        if RotCenter:
            for idim in range(0, 3, 1):
                Pts[:, idim] = Pts0[:, idim] - RotCenter[idim]

    # normalize the axis vector
    axis_rot1 = axis_rot
    norm_axis = sum(axis_rot ** 2)
    if abs(norm_axis - 1.0) > 1e-12:
        axis_rot1 = axis_rot / math.sqrt(norm_axis)

    # construct the quotanion
    half_angle = angle / 2
    q1 = axis_rot1 * math.sin(half_angle)
    q2 = [math.cos(half_angle)]
    q = np.hstack((q1, q2))

    # convert to rotation matrix
    M_Rot = np.transpose(Quaternion_2_Rotation(q))

    if outputMatrix:
        Matrix = np.identity(4, dtype=None)
        Matrix[:3, :3] = M_Rot
        return Matrix

    # rotate the point set
    Pts1 = np.dot(Pts, M_Rot)

    if RotAlongCentroid:
        for idim in range(0, 3, 1):
            Pts1[:, idim] = Pts1[:, idim] + oo[idim]
    if RotCenter:
        for idim in range(0, 3, 1):
            Pts1[:, idim] = Pts1[:, idim] + RotCenter[idim]

    return Pts1