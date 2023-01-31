# author Ye Han
# version 0.1
# update date 2019-12-18
# mod date record 2019-12-18 version 0.1

import numpy as np

def Crop(array, axial, sagittal, coronal):
    r"""
    Crop the image by assignning the axial, sagittal and coronal. The order of the parameter (axial, sagital, coronal) 
    is the same as MITK in order to use easily.

    Args:
        array (numpy array): the input image array

        axial (list): the axial we want to save from the origin image.

        sagittal (list): the sagittal we want to save from the origin image.

        coronal (list): the coronal we want to save from the origin image.



    Return:
        array (numpy array): cropped array


    Example::
        >>> import pylib
        >>> path = r'.\id1_Seg.nii.gz'
        >>> img, array = pylib.Read_Image(input_path)
        >>> #If we want to get the {axial:[5-10], sagittal:[6-11], coronal:[7-12]} from the origin image.
        >>> array = pylib.Crop(array, [5, 10], [6, 11], [7, 12]) 
        >>> output_path = r'.\arrange_labvlm.nii.gz'
        >>> pylib.Write_Image(array, output_path)
    """
    #TODO:加一个形状判断
    crop_array = array[axial[0]:axial[1], coronal[0]:coronal[1], sagittal[0]:sagittal[1]]
    #In numpy and simpleitk, the order of the array is [axial, coronal, sagittal].
    return crop_array
