# Author: XIAOXIAN JIN
# Created: 2020/1/13
# mod date record 2020-3-28 version 0.1 xingchuang wen

import pyvista as pv
import string

def Disp_EachSubMesh(mesh_path, lable_path, submesh_path):
    r"""
    Description: 
    Display each sub-mesh of a multimesh structure, in order to observe the contained submeshes in the multimesh
    本程序的思路为通过读取lables和multimesh，为每个submesh创建一个.obj模型文件。
    由于所用函数对文件类型的限制，本程序调试时使用的multimesh模型是由.off模型文件通过MeshLab导出得到的.obj模型文件。

    args:
    mesh_path: the path of the multimesh
    lable_path: the path of the lables
    submesh_path: 生成submesh的模型文件路径

    Return:
    display each submesh

    Example::
        >>> lable_path = r"C:/Users/Lenovo/Desktop/ImageProcess/Airplane/64_labels.txt"
        >>> mesh_path = r"C:/Users/Lenovo/Desktop/ImageProcess/Airplane/64.obj"
        >>> submesh_path = r"C:/Users/Lenovo/Desktop/ImageProcess/Airplane/64_new.obj"
        >>> Disp_EachSubMesh(mesh_path, lable_path, submesh_path)
    """
    mesh = pv.read(mesh_path)
    mesh.plot()

    f = open(lable_path)
    for line in f.readlines():

        # ------读lable文档得到每个submesh包含的faces序号------
        line = line.strip('\n')
        if line[0] in string.ascii_letters:  # 开头是字母,说明本行是lable
            lable = line
            continue
        curline = line.strip().split(" ")
        intline = list(map(
            int, curline))  # 使用map函数把数据转化成为int类型,数据为某一lable下包含faces的序号

        # ------为submesh创建.obj模型文件------
        with open(mesh_path, 'r') as r:
            lines = r.readlines()
        with open(submesh_path, 'w') as w:
            cnt = 0
            for line in lines:
                if line[0] != 'f':  # 开头不是“f”,说明本行不是face相关的信息
                    w.write(line)
                else:
                    cnt = cnt + 1
                    if cnt in intline:  # face序号包含在intline中,则写入submesh的.obj模型文件
                        w.write(line)

        # ------子网格显示------
        submesh = pv.read(submesh_path)
        p = pv.Plotter()
        p.add_mesh(mesh, color="mintcream", opacity=1)
        p.add_mesh(submesh, color="Crimson")
        p.show(title=lable)

