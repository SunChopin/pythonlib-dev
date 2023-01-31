# author Ye Han
# version 0.1
# update date 2019-12-16
# mod date record 2019-12-16 version 0.1

import numpy as np
import SimpleITK as sitk
from ..io import load, save


def Rearrange_Labvlm(array):
    r"""
    There's a label which value corresponds the organ. For example,

    {value 0: background, value 2: liver, value 5: spleen, value 190: left kidney...}

    However, the values are not discontinuous. (0, 2, 5, 190...)

    This function is used to rearrange the value of the label.
    
    eg: (0, 2, 5, 190...)->(0, 1, 2, 3...)

    Args:
        array (numpy array)

    Return:
        array (numpy array)


    Example::
        >>> import pylib
        >>> from pylib.utilities import tools
        >>> path = r'.\id1_Seg.nii.gz'
        >>> img, array = pylib.Read_Image(input_path)
        >>> array = tools.Rearrange_Labvlm(array)
        >>> output_path = r'.\arrange_labvlm.nii.gz'
        >>> pylib.Write_Image(array, output_path)
    """
    c = 0
    for i in np.unique(array):
        array[array == i] = c
        c += 1
    return array


if __name__ == "__main__":
    path = '../../data/sample.nii.gz'
    img, array = Read_Image(path)
    array = Rearrange_Labvlm(array)
    output_path = '../../data/test_sample.nii.gz'
    Write_Image(array, output_path)
