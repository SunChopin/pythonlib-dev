# author Ye Han
# version 0.2
# update date 2020-03-26
# mod date record 2019-12-16 version 0.1
# mod date record 2020-03-26 version 0.2

import SimpleITK as sitk


def Write_Image(array, path, origin=(0, 0, 0), spacing=[1, 1, 1], useCompress=False):
    r"""Save the image ``arr`` as file. The target image format is determined by the ``filename`` suffix.

    This function relies on SimpleITK, which enables the power of ITK for image loading and saving.
    The supported image file formats should include at least the following.


    Medical formats:


    - ITK MetaImage (.mha/.raw, .mhd)

    - Neuroimaging Informatics Technology Initiative (NIfTI) (.nia, .nii, .nii.gz, .hdr, .img, .img.gz)

    - Analyze (plain, SPM99, SPM2) (.hdr/.img, .img.gz)

    - Digital Imaging and Communications in Medicine (DICOM) (.dcm, .dicom)

    - Digital Imaging and Communications in Medicine (DICOM) series (<directory>/)

    - Nearly Raw Raster Data (Nrrd) (.nrrd, .nhdr)

    - Medical Imaging NetCDF (MINC) (.mnc, .MNC)

    - Guys Image Processing Lab (GIPL) (.gipl, .gipl.gz)


    Microscopy formats:


    - Medical Research Council (MRC) (.mrc, .rec)

    - Bio-Rad (.pic, .PIC)

    - LSM (Zeiss) microscopy images (.tif, .TIF, .tiff, .TIFF, .lsm, .LSM)

    - Stimulate / Signal Data (SDT) (.sdt)


    Visualization formats:


    - VTK images (.vtk)


    Other formats:


    - Portable Network Graphics (PNG) (.png, .PNG)

    - Joint Photographic Experts Group (JPEG) (.jpg, .JPG, .jpeg, .JPEG)

    - Tagged Image File Format (TIFF) (.tif, .TIF, .tiff, .TIFF)

    - Windows bitmap (.bmp, .BMP)

    - Hierarchical Data Format (HDF5) (.h5 , .hdf5 , .he5)

    - MSX-DOS Screen-x (.ge4, .ge5)

    Further information see https://simpleitk.readthedocs.io .

    Args:
    
        array (numpy array): the Numpy Array we get from image

        path (string): the file path you want to save

        origin (tuple): the origin of the image

        spacing (list): the spacing of the image

        useCompress (bool): compress the *.mhd file if the value is True. Default is False.



    Example:
        >>> import pylib
        >>> input_path = r'.\id1.nii.gz'
        >>> out_path = r'.compress_id1.mhd'
        >>> image, array = pylib.Read_Image(input_path)
        >>> # Some operation of the array
        >>> pylib.Write_Image(array, out_path, useCompress=True)

    """
    if path[-3:] != 'mhd' and useCompress == True:  # Check whether the file can be compressed.
        raise Exception("Only *.mhd file can be compressed. Please set useCompress = False "
                        "or change the file type which will be saved.")
    image = sitk.GetImageFromArray(array)
    image.SetOrigin(origin)
    image.SetSpacing(spacing)
    sitk.WriteImage(image, path, useCompress)


if __name__ == "__main__":
    # Test
    input_path = r'C:\Users\hanye\Desktop\pythonlib\id1.nii.gz'
    out_path = r'C:\Users\hanye\Desktop\pythonlib\test_compress_id1.nii'
    image = sitk.ReadImage(input_path)
    array = sitk.GetArrayFromImage(image)
    Write_Image(array, out_path, useCompress=True)

