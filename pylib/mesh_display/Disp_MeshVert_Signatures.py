# Author: XIAOXIAN JIN
# Created: 2020/1/13
# mod date record 2020-3-28 version 0.1 xingchuang wen

import pyvista as pv
import matplotlib.pyplot as plt

def Disp_Meshvert_Signatures(path, signature):
    r"""
    Description: Disp scalar field of mesh vertices signatures

    args:
    INPUTS:
    path: the path of the mesh
    signature: vertex attribute,which can be set to 'x', 'y', 'z'

    Return:
    dispaly

    Example::
        >>> path = r"C:/Users/Lenovo/Desktop/ImageProcess/average_Asian_male.obj"  # get the path of the  mesh
        >>> Disp_Meshvert_Signatures(path, 'x')  
        >>> Disp_Meshvert_Signatures(path, 'y') 
        >>> Disp_Meshvert_Signatures(path, 'z')  
    """
    # get the mesh
    mesh = pv.read(path)
    # access the points by fetching the attribute on any mesh as a NumPy array
    the_pts = mesh.points
    if signature == 'x':
        # fetching the X coordinate of the point
        new_array = the_pts[0:mesh.n_points, 0]
    elif signature == 'y':
        # fetching the Y coordinate of the point
        new_array = the_pts[0:mesh.n_points, 1]
    elif signature == 'z':
        # fetching the Z coordinate of the point
        new_array = the_pts[0:mesh.n_points, 2]
    else:
        # If there is an unexpected input, inform the error
        print('Sorry, We do not support this signature.')
    # Assign a new array to the point data
    mesh.point_arrays['values'] = new_array
    # Add scalar array with range (0, 100)
    mesh['normal_values'] = pv.plotting.normalize(mesh['values']) * 100
    # make a simple colormap,which can be passed to PyVista
    # "Viridis" can be replaced with any Matplotlib colormap.
    # "10" can be modified or cancelled to make the color gradient.
    boring_cmap = plt.cm.get_cmap("viridis", 10)
    mesh.plot(scalars='normal_values', cmap=boring_cmap)


# Test
# path = r"C:/Users/Lenovo/Desktop/ImageProcess/average_Asian_male.obj"  # get the path of the  mesh
# disp_meshvert_signatures(path, 'x')  # Call function
# disp_meshvert_signatures(path, 'y')  # Call function
# disp_meshvert_signatures(path, 'z')  # Call function
