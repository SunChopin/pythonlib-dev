# author Ye Han
# version 0.1
# update date 2019-12-16
# mod date record 2019-12-16 version 0.1

import numpy as np
import SimpleITK as sitk
from ..io import load, save


def Rot(array, axis, angle):
    r"""
    rotate 90 and 180 degree the volume along a certain axis.

    Args:
        array (numpy array): the input image array

        axis (str): the axis to rotate around. Limit input: 'x', 'y' and 'z'.
        
        angle (int): the angle to rotate. Limit input: 90, 180.

    Return:
        array (numpy array): rotated array


    Example::
        >>> import pylib
        >>> path = r'.\id1_Seg.nii.gz'
        >>> img, array = pylib.Read_Image(input_path)
        >>> array = pylib.Rot(array, axis='x', angle=180)
        >>> output_path = r'.\roted.nii.gz'
        >>> pylib.Write_Image(array, output_path)
    """
    # Limit the parameter input format
    if axis not in ['x', 'y', 'z']:
        raise Exception("The axis can only be 'x', 'y' and 'z'.")
    if angle not in [90, 180]:
        raise Exception("This function can only rotate 90 and 180.")
    # End
    if angle == 90:
        if axis == 'x':
            array = np.transpose(array, (0, 2, 1))
            array = np.flip(array, 1)
        elif axis == 'y':
            array = np.transpose(array, (2, 1, 0))
            array = np.flip(array, 2)
        elif axis == 'z':
            array = np.transpose(array, (1, 0, 2))
            array = np.flip(array, 0)
    elif angle == 180:
        array = rot(array, axis, 90)
        array = rot(array, axis, 90)
    return array
