# author Ruxue Hu, Ye Han
# version 0.4
# update date 2021-06-12

import SimpleITK as sitk
from SimpleITK import ResampleImageFilter
from SimpleITK import Transform

def resample(image, o_size=None, o_spacing=[1,1,1], interpolator = 3):
    r"""
    resample the image by assigning the size and interpolator method.

    Args:
        image (simpleitk image): the input image.

        o_size (list): the image size you want to get. The order of the list is [axial, coronal, sagittal].
        
        o_spacing (list): the spacing you want to get. Default is [1,1,1]. Usually we want to resample the spacing of the image to [1,1,1] to train the network.

        interpolator (int): assign the method of interpolator. linear = 1, nearest = 2, bspline =3. Default is 3 for image. If you want to resample for the label, pls set it to 2.


    Return:
        image (simpleitk image): downsampled image.

    Example::
        >>> import pylib
        >>> import SimpleITK as sitk
        >>> path = r'.\id1_Seg.nii.gz'
        >>> img, array = pylib.Read_Image(input_path)
        >>> img = pylib.resample(img) 
        >>> output_path = r'.\downsampled.nii.gz'
        >>> sitk.Write_Image(img, output_path)
    """
    assert (o_size == None and o_spacing != None) or (o_size != None and o_spacing == None), 'o_size 和 o_spacing 只能指定一个。'
    print("Start to Resample.")
    t = time.time()

    file_spacing = image.GetSpacing()
    file_size = image.GetSize()
    trans = Transform()
    trans.__init__(3, 0)
    filter = ResampleImageFilter()

    filter.SetInterpolator(interpolator)
    filter.SetTransform(trans)
    filter.SetOutputOrigin(image.GetOrigin())

    if o_spacing is not None and o_size is None:
        o_size = [file_spacing[0] * file_size[0] / o_spacing[0], file_spacing[1] * file_size[1] / o_spacing[1], file_spacing[2] * file_size[2] / o_spacing[2]]
        o_size = [round(i) for i in o_size]

    elif o_size is not None and o_spacing is None:
        o_spacing = [file_spacing[0] * file_size[0] / o_size[0], file_spacing[1] * file_size[1] / o_size[1], file_spacing[2] * file_size[2] / o_size[2]]

    filter.SetOutputSpacing(o_spacing)  # output size * output spacing = original size * original spacing
    filter.SetSize(o_size)  # output size 
    filter.SetOutputDirection(image.GetDirection())

    filter.SetDefaultPixelValue(-1000)  # set the black ct value
    filter.SetOutputPixelType(8)  # flot32=8 int64=6
    # do downsample
    image = filter.Execute(image)

    print(f'Spacing:{[round(i,3) for i in file_spacing]}->{o_spacing}, Size:{[round(i,3) for i in file_size]}->{o_size}, Costime:{time.time()-t:.3f}s')

    return image
