#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
author Tian Yang
Version 1.0
update date 2020-01-08
mod date record  2020-01-08 version 1.0
'''

import numpy as np
import SimpleITK as sitk


def Rigid_Transform_Pts(pts, center, shifts, angles):
    """
    Rigid transformation for the points, either 2D or 3D

    Parameters
        pts : ndarray
            the Pts array

    Returns
        deformed : ndarray
            the deformed vertices
        center : ndarray
            the origine for the transformation
        shifts : ndarray
            the shift vector
        angles : float or list
            the rotation angles, Unit(rad)

    Examples
    >>> point = [[10, 11], [11, 10]]
    >>> Rigid_Transform_Pts(point, (0, 0), (7.2, 8.4), np.pi)
    """

    pts = np.array(pts)
    dim = pts.ndim

    if dim == 2:
        transform2 = sitk.Euler2DTransform()
        transform2.SetAngle(angles)
        transform2.SetCenter(center)
        transform2.SetTranslation(shifts)
        deformed = transform2.TransformPoint(pts)
    elif dim == 3:
        transform3 = sitk.Euler3DTransform()
        angleX, angleY, angleZ = angles
        transform3.SetRotation(angleX, angleY, angleZ)
        transform3.SetTranslation(shifts)
        transform3.SetCenter(center)
        deformed = transform3.TransformPoint(pts)
    else:
        raise ValueError('The dimension of points is wrong')
    return deformed


if __name__ == '__main__':
    point = [[10, 11], [11, 10]]
    Rigid_Transform_Pts(point, (0, 0), (7.2, 8.4), np.pi)
