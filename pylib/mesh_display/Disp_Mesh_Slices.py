# Author: XIAOXIAN JIN
# Created: 2020/1/13
# mod date record 2020-3-28 version 0.1 xingchuang wen

import pyvista as pv
import matplotlib.pyplot as plt

def Disp_Mesh_Slices(path, idx, idy, idz):
    r"""
    Description: D   Display mesh with slices

    args:
    path: the path of the mesh
    idx,idy,idz: the cut position of the x y z plane, idx=0 means does not display this slice.
                If all three parameters are 0, the default slice position is used.
    
    Return:
    display

    Example::
        >>> path = r"C:/Users/Lenovo/Desktop/ImageProcess/average_Asian_male.obj"   # get the path of the  mesh
        >>> Disp_Mesh_Slices(path, 0, 0, 0)   # Call function
        >>> Disp_Mesh_Slices(path, 120, -120, 130)   # Call function
    """

    # get the mesh
    mesh = pv.read(path)
    # define a categorical colormap
    # "Viridis" can be replaced with any Matplotlib colormap.
    # "4" can be modified or cancelled.
    cmap = plt.cm.get_cmap("viridis", 4)
    # set the cut position of the x y z plane
    if (idx == 0) and (idy == 0) and (idz == 0):
        slices = mesh.slice_orthogonal()
        slices.plot(cmap=cmap)
    else:
        slices = mesh.slice_orthogonal(idx, idy, idz)
        slices.plot(cmap=cmap)


# Test 
# path = r"C:/Users/Lenovo/Desktop/ImageProcess/average_Asian_male.obj"   # get the path of the  mesh
# disp_mesh_slices(path, 0, 0, 0)   # Call function
# disp_mesh_slices(path, 120, -120, 130)   # Call function
