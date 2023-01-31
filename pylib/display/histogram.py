# author Ye Han
# version 0.1
# update date 2019-12-16
# mod date record 2019-12-16 version 0.1

import numpy as np
from ..io import load
import matplotlib.pyplot as plt


def Histogram(array, range=[-1000, 2000], n=500):
    r"""
    This function is used to draw the histogram of the image.

    Args:
        array (numpy array): the file path you want to save

        range (list): the greyvalue of the image you want to draw on the figure. Default: range=[-1000,2000]

        n (int): the box nunmber of the figure. Default: n=500

    Return:
        A histogram image.


    Example:
        >>> import pylib
        >>> path = r'.\id1.nii.gz'
        >>> img, array = pylib.ReadImage(input_path)
        >>> range, n = [-1,1], 5
        >>> pylib.histogram(array, range, n)
    """
    def Stats_Num(array, left, right):
        # 统计 numpy 数组 a 在灰度区间(left, right)内的voxel数，返回voxel数
        return np.sum((array >= left) & (array < right))

    def Get_List(a, range, n):
        '''
        a: 待统计numpy数组
        range:灰度范围
        n:箱子数n
        '''
        stats_list = []
        bin_width = (range[1]-range[0])/n  # 箱子数->箱宽
        list_point = np.arange(range[0], range[1], bin_width)  # 灰度区间划分
        for i in list_point:
            stats_list.append(Stats_Num(a, i, i + bin_width))
        return(list_point, stats_list)

    rl, rs = Get_List(array, range, n)
    plt.plot(rl, rs)
    plt.show()


if __name__ == "__main__":

    path = '../../data/sample.nii.gz'
    img, array = load.Read_Image(path)
    range, n = [-1, 1], 5
    Histogram(array, range, n)
