# Author: Mingming Huo
# Created: 2019/01/08
# mod date record 2020-3-28 version 0.1 xingchuang wen

import pyvista as pv
from pyvista import examples

def Disp_2_Meshes(filename1,filename2):
    r"""
    Description: Display two meshes at the same time

    args:
    filepaths of two meshfile

    Return:
    display two meshes

    Example::
        >>> Disp_2_Meshes("C:/Users/wenxc/Desktop/lab_face/M1.obj","C:/Users/wenxc/Desktop/lab_face/M2.obj")

    """
    plotter = pv.Plotter(shape=(1, 2))

    # Note that the (0, 0) location is active by default
    # load and plot an airplane on the left half of the screen
    plotter.subplot(0, 0)
    plotter.add_text("File1\n", font_size=30)
    mesh1=pv.read(filename1)
    plotter.add_mesh(mesh1, show_edges=False)

    # load and plot the uniform data example on the right-hand side
    plotter.subplot(0, 1)
    plotter.add_text("File2\n", font_size=30)
    mesh2=pv.read(filename2)
    plotter.add_mesh(mesh2, show_edges=True)

    # Display the window
    plotter.show()

