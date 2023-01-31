# author Gaoli Zhang
# version 0.1
# update date 2020-3-16
# mod date record 2020-3-16 version 0.1 Linlin Liu

import keyword
import numpy as np
from numpy import *
import math
from rebin import rebin
from Calc_PrincipalAxes import Calc_PrincipalAxes
from Rot_Pts_alongAxis import Rot_Pts_alongAxis


def BndBox_Pts(Pts, margin='', isOblique='', isDisp='', Conn_Pts='', FindMiniumBndBx=''):
    r"""
    PURPOSE:
        Calculate the bounding box of the point set

    CATEGORY:
        bounding box, morphological processing

    INPUTS:
        Pts: the 3D input point set

    KEYWORDS:
        margin: the margin length of the bounding box, 3-elements vector, in physical units (e.g., mm) rather than voxel unit
        isOblique: whether or not to compute oblique bounding boxes
        isDisp: if set, display the bounding box with the input point set;
        Conn_Pts: the mesh connection of the input points, if set, will be used to display the mesh of the input points
        FindMiniumBndBx: if set, the point set will be rotate along the three axes (x,y,and z) respectively to find the minimum bounding box

    Returned Value:
        {Bnd:[xmin,xmax,ymin,ymax,zmin,zmax],  l:[xmax-xmin,ymax-ymin,zmax-zmin],
         c: [xmax+xmin,ymax+ymin,zmax+zmin]/2, o:[xmin,ymin,zmin], BoxVerts, BoxConn};

    Example::
        >>> a = np.array([[1, 1, 2],
                  [2, 3, 1],
                  [1, 3, 1],
                  [4, 0, 1] ])
        >>> print(BndBox_Pts(a))
        >>> print(BndBox_Pts(a, isOblique='isOblique'))
        >>> print(BndBox_Pts(a, margin=[1, 1, 1] ))
        >>> print(BndBox_Pts(a, Conn_Pts='Conn_Pts'))
        >>> print(BndBox_Pts(a, FindMiniumBndBx='FindMiniumBndBx'))
    """
    if margin:
        margin = margin
    else:
        margin = np.zeros(3)

    if isOblique:
        isOblique = isOblique
    else:
        isOblique = 0

    if Conn_Pts:
        Conn_Pts = Conn_Pts
    else:
        Conn_Pts = -1

    if len(margin)==1:
         margin= np.zeros(3) + margin

    if isOblique:
        Axes = Calc_PrincipalAxes(Pts)
        o = Axes[0]
        T = Axes[1]
        T2 = np.multiply(T, T)
        T = T / rebin((np.sqrt(mat(T2).sum(axis=1))), (3, 3))
        nv = len(Pts) / 3
        Pts1 = np.dot((Pts - rebin(mat(o), (nv, 3))), np.transpose(T))
    else:
        Pts1 = Pts

    if FindMiniumBndBx:
        angle_step = 10
        n_angles = math.ceil(90/angle_step) + 1
        vlm_axis = np.zeros((n_angles, 3))

        for i_angle in range(0, n_angles, 1):
            angle = i_angle*angle_step
            Pts1 = Rot_Pts_alongAxis(Pts, np.array([1.0, 0.0, 0.0]), angle*(math.pi) / 180.)
            BndBx = BndBox_Pts(Pts1, margin='', Conn_Pts='')
            vlm_axis[i_angle, 0] = BndBx['v']

        for i_angle in range(0, n_angles, 1):
            angle = i_angle*angle_step
            Pts1 = Rot_Pts_alongAxis(Pts, np.array([0.0, 1.0, 0.0]), angle*(math.pi) / 180.)
            BndBx = BndBox_Pts(Pts1, margin='', Conn_Pts='')
            vlm_axis[i_angle, 1] = BndBx['v']

        for i_angle in range(0, n_angles, 1):
            angle = i_angle*angle_step
            Pts1 = Rot_Pts_alongAxis(Pts, np.array([0.0, 0.0, 1.0]), angle*(math.pi) / 180.)
            BndBx = BndBox_Pts(Pts1, margin='', Conn_Pts='')
            vlm_axis[i_angle, 2] = BndBx['v']

        vmin = np.amin(vlm_axis)
        L = vlm_axis.tolist()
        cood_min = [(L.index(i), i.index(min(i))) for i in L if min([min(i) for i in L]) in i][0]

        rot_axis = np.zeros(3)
        rot_axis[cood_min[1]] = 1.0
        angle = cood_min[0] * angle_step
        Pts1 = Rot_Pts_alongAxis(Pts, rot_axis, angle *math.pi / 180.)

    Pts11 = np.array(Pts1)
    xmin = min(Pts11[:, 0]) - margin[0]
    xmax = max(Pts11[:, 0]) + margin[0]
    ymin = min(Pts11[:, 1]) - margin[1]
    ymax = max(Pts11[:, 1]) + margin[1]
    zmin = min(Pts11[:, 2]) - margin[2]
    zmax = max(Pts11[:, 2]) + margin[2]
    l = [xmax - xmin, ymax - ymin, zmax - zmin]
    v = l[0] * l[1] * l[2]

    BoxVerts = [[xmin, ymin, zmin], [xmax, ymin, zmin], [xmax, ymax, zmin], [xmin, ymax, zmin],
                [xmin, ymin, zmax], [xmax, ymin, zmax], [xmax, ymax, zmax], [xmin, ymax, zmax]]
    BoxConn = [4, 0, 1, 2, 3, 4, 4, 5, 6, 7, 4, 0, 1, 5, 4, 4, 2, 3, 7, 6]

    if isOblique:
        BoxVerts = np.dot(BoxVerts, T) + rebin(mat(o), (8, 3))
        BndBox = {'Verts':BoxVerts, 'o':o, 'T':T, 'Conn':BoxConn, 'Pts1':Pts1}
    else:
        c = [(xmax+xmin) / 2, (ymax+ymin) / 2, (zmax+zmin) / 2]
        o = [xmin, ymin, zmin]
        BndBox = {'Bnd':[xmin, xmax, ymin, ymax, zmin, zmax], 'Pts1': Pts1, 'l': l, 'v': v,
                  'c':c, 'o': o, 'Verts': BoxVerts, 'Conn': BoxConn}

    #if isDisp:
    #    Disp_2_Meshes(Pts1, Conn_Pts, BoxVerts, BoxConn, style1 = 2, style2 = 1, thick2=2)

    return(BndBox)