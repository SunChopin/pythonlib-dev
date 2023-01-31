#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
author Tian Yang
Version 1.0
update date 2020-01-08
mod date record  2020-01-08 version 1.0
'''

import cv2
import matplotlib.pyplot as plt
import numpy as np


def TPS_Transform_Pts(sshape, tshape, matches):
    """
    Calculate 3D affine transformation between two point sets. The two input point sets are in correspondance already,
    i.e. the number of points in the two sets should be equal, and the order of points should be in correspondence

    Parameters
        sshape : ndarray
            the source point set
        tshape : ndarray
            the target point set
        matches : int
            Standard vector of Matches between points. Just need the length of Matches.

    Returns
        dfm : ndarray
            The affine transformation matrix

    Notes
        opencv-contrib-python must be installed for using cv2.createThinPlateSplineShapeTransformer.

    Examples
    >>> sshape = np.array([[[67, 90, 20], [26, 90, 20]], [[67, 90, 20], [26, 90, 20]]], np.float32)
    >>> tshape = np.array([[[60, 63, 20], [20, 22, 20]], [[67, 90, 20], [26, 90, 20]]], np.float32)
    >>> dfm = TPS_Transform_Pts(sshape, tshape, 10)
    """
    tps = cv2.createThinPlateSplineShapeTransformer()

    sshape = sshape.reshape(1, -1, 2)
    tshape = tshape.reshape(1, -1, 2)

    matches = [cv2.DMatch(i, i, 0) for i in range(matches)]

    tps.estimateTransformation(tshape, sshape, matches)
    ret, dfm = tps.applyTransformation(sshape)
    return dfm


if __name__ == '__main__':
    sshape = np.array(
        [[[67, 90, 20], [26, 90, 20]], [[67, 90, 20], [26, 90, 20]]],
        np.float32)
    tshape = np.array(
        [[[60, 63, 20], [20, 22, 20]], [[67, 90, 20], [26, 90, 20]]],
        np.float32)
    dfm = TPS_Transform_Pts(sshape, tshape, 10)
