# author Haoyue Ao
# version 0.1
# update date 2020-3-16
# mod date record 2020-3-16 version 0.1 Linlin Liu

import numpy as np
import math


def PtSet_DownSamp(Pts, Ratio, nSmp='', ReturnIndOnly=''):
    r"""
    PURPOSE:
        Downsample point set, either 2D or 3D
        2D/3D点集降采样

    CATEGORY:
        basic mesh processing
        基础网格处理
    INPUTS:
        Pts: the input point set
             输入点集
        Ratio: the ratio of downsampling, e.g. 2 means two time down sampling
               降采样比例，例如：2表示向下取样两次
    KEYWORDS:
        nSmp: the number of desired sampled points, if set, Ratio will not work
              所需采样点的数量，如果设置，则比例数据Ratio将不进行处理
    OUTPUT:
        a structure containing:
        一个结构包含如下：
            Pts: the downsampled point set
                 降采样的点集
            inds: the indices of the down-sampled points in the original point set
                  原始点集中下采样点的索引
        ReturnIndOnly: if set, only return the indices
                       如果设置，则只返回索引

    Example::
        >>> a = np.array([[1, 1, 2, 3], [2, 3, 1, 2], [1, 3, 1, 1]])
        >>> r = 2
        >>> print('ratio = 2, nSmp未设置, ReturnIndOnly未设置')
        >>> print(PtSet_DownSamp(a, r))
        >>> print('ratio = 2, nSmp=2, ratio无用, ReturnIndOnly未设置')
        >>> print(PtSet_DownSamp(a, r, nSmp=2))
        >>> print('ratio = 2, nSmp未设置, ReturnIndOnly为1')
        >>> print(PtSet_DownSamp(a, r, ReturnIndOnly='ReturnIndOnly'))
        >>> print('ratio = 2, nSmp=2, ReturnIndOnly为1')
        >>> print(PtSet_DownSamp(a, r, nSmp=2, ReturnIndOnly='ReturnIndOnly'))
    """
    num = np.array(Pts)
    Sz = (num.shape)  # 获取Pts数组每一维的维度，得到一个元组

    nDim = Sz[0]
    nPts = Sz[1]

    if not nSmp:
        ind_Samp = np.arange((float(nPts) / Ratio - 1) * Ratio, dtype=int)
    else:
        ind_Samp = np.floor(np.arange(nSmp, dtype=float) * float(nPts - 1) / (nSmp - 1)).astype(np.int)

    if ReturnIndOnly:
        return ind_Samp

    Pts_Samp = Pts[:, ind_Samp]

    return Pts_Samp










    
