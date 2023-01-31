# author Ye Han
# version 0.2
# update date 2020-03-26
# mod date record 2019-12-16 version 0.1 Ye Han
# mod date record 2020-03-26 version 0.2 Ye Han


import SimpleITK as sitk


def Read_Image(path):
    r"""
    Read the ``image`` and returns a ndarray with the image and numpy array.

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
        path (string): the file path you want to save

    Return:
        img (image): class SimpleITK image
        
        array (array): numpy array


    Example:
        >>> import pylib
        >>> path = r'.\id1.nii.gz'    
        >>> img, array = pylib.ReadImage(input_path)
    """
    img = sitk.ReadImage(path)
    array = sitk.GetArrayFromImage(img)
    return img, array

def Read_LDM(path, spacing, turn_index = False):
    r"""
    Read the ``LDM`` file and returns a list with the positions of all the landmarks. 
    Suitable for the image that origin equals 0.


    Args:
        path (string): the *.ldm file path you want to read
        spacing (list): the spacing of the image.
        turn_index (bool): default value is False. If we want to turn the position to the numpy index, set it as True.

    Return:
        pos_list (list): A list including all the landmarks position or index.

    """

    def pos2index(pos, spacing):
        index = round((pos + spacing/2)/spacing)-1 #AS 的 position 和 index 的转换公式
        return index

    def ldm2index(path, spacing):
        point_list = []
        file = open(path, "r", encoding="utf8") # 读文件
        lines = file.readlines() # 文件按行写入list。若文件太大（十万行级别），readlines方式会占用大量内存。小文件不会。
        for i in range(len(lines)):  # 逐行读文件
            if '#POINT_POS' in lines[i]: # 若该行有关键词 #POINT_POS
                pos = lines[i + 1] # 则下一行就是点的 position
                a,b,c = pos.replace("\n","").split(' ')
                pos = [a,b,c]
                pos = [float(x) for x in pos]
                if turn_index == True:
                    index = map(pos2index, pos, spacing)
                    point_list.append(list(index))
                else:
                    point_list.append(list(pos))
        file.close()
        return point_list
    
    pos_list = ldm2index(path, spacing)
    return pos_list