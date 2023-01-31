# Author: Mingming Huo
# Created: 2019/01/08
# mod date record 2020-3-28 version 0.1 xingchuang wen


import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def Disp_MultiMesh(filename, filetxt):
    r"""
    Description: Display the multimesh structure, with each submesh a different color

    args:
    mesh_path: the path of the multimesh
    lable_path: the path of the lables

    Return:
    display

    Example::
        >>> Disp_MultiMesh("D:/pycharm_Image/79.off", "D:/pycharm_Image/79_labels.txt")

    """
    mesh = pv.read(filename)
    vertices = mesh.points  #顶点信息
    count_faces = 0
    #从off文件中读出面信息
    with open(filename) as file:
        faces = []
        while 1:
            line = file.readline()
            if not line:
                break
            strs = line.split(" ")
            if strs[0] == "3":
                faces.append(
                    (int(strs[0]), int(strs[1]), int(strs[2]), int(strs[3])))
                count_faces = count_faces + 1
            if strs[0] == "/n":
                break
    faces = np.array(faces)
    Num_faces = count_faces
    surf = pv.PolyData(vertices, faces)
    surf.plot()

    #从txt文件中选择不同子曲面的组成
    txt = open(filetxt, "r")  # 设置文件对象
    data = txt.readlines()  # 直接将文件中按行读到list里
    txt.close()  # 关闭文件
    Num_submesh = int(len(data) / 2)  #子曲面数
    k = np.zeros([1, 4], int)
    kl = np.zeros([1, 4], int)
    num_mesh = np.zeros([1, Num_submesh], int)
    i = 1
    j = 1
    mesh_faces = []
    mesh = []
    surf = {}
    #选择一个子曲面的组成面
    while 1:
        if i <= Num_submesh:
            mesh.append(data[j])
            mesh = data[j].split()
            num_mesh[0, i - 1] = len(mesh)
            mesh_faces.append(np.zeros([num_mesh[0, i - 1] - 1, 4], int))
            while 1:
                if kl[0, i - 1] <= num_mesh[0, i - 1]:
                    k[0, i - 1] = int(mesh[(kl[0, i - 1])])
                    (mesh_faces[i - 1])[kl[0, i - 1], :] = faces[k[0, i -
                                                                   1], :]
                    kl[0, i - 1] = kl[0, i - 1] + 1
                if kl[0, i - 1] == num_mesh[0, i - 1] - 1:
                    break
            surf[i - 1] = pv.PolyData(vertices, mesh_faces[i - 1])
            i = i + 1
            j = j + 2
        if i == Num_submesh + 1:
            break
    #将不同子曲面用不同颜色标识（此处为四个子曲面举例）
    plotter = pv.Plotter()
    plotter.add_mesh(surf[0], show_edges=False, color="red")
    plotter.add_mesh(surf[1], show_edges=False, color="green")
    plotter.add_mesh(surf[2], show_edges=False, color="blue")
    plotter.add_mesh(surf[3], show_edges=False, color="yellow")
    plotter.show()


# test
# Disp_MultiMesh("D:/pycharm_Image/79.off", "D:/pycharm_Image/79_labels.txt")
