# Author: Mingming Huo
# Created: 2019/12/14
# mod date record 2020-3-28 version 0.1 xingchuang wen


import numpy as np
import pyvista as pv
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def Disp_Mesh(filename, image_file):
    r"""
    Description: Display a single mesh, given the input of verts and conn

    args:
    obj文件和纹理信息文件的路径

    Return:
    display the mesh with texture

    Example::
        >>>Disp_Mesh("D:/pycharm_practice/average_Asian_male.obj",
            "D:/pycharm_Image/mesh_face.png")
        
    """
    #filename = "D:/pycharm_practice/average_Asian_male.obj"
    mesh = pv.read(filename)
    vertices = mesh.points  #顶点信息
    faces = mesh.faces  #面信息
    Num_faces = mesh.n_faces
    mesh.plot()
    surf = pv.PolyData(vertices, faces)
    surf.plot()

    # 纹理信息
    #image_file = "D:/pycharm_Image/mesh_face.png"
    tex = pv.read_texture(image_file)
    mesh_save = mesh.plot(texture=tex)

    # 显示
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh_save)
    plotter.show(screenshot="D:/pycharm_Image/myscreenshot.png")


