# Author: Yang Yuxin
# Created: 2019/12/28
# mod date record 2020-3-28 version 0.1 xingchuang wen


import vtk
import os

def Write_Meshfile(mesh, path):
    r"""
    Description: Write mesh file

    args:
    mesh(vtkCommonDataModelPython.vtkPolyData)
    

    Return:
    file: .ply .stl

    Example::
        >>> a = Read_MeshFile('C:/Users/zenod/Desktop/a.obj')
        >>> b = Write_MeshFile(a, 'C:/Users/zenod/Desktop/b.stl')

    """
    suffix = os.path.splitext(path)[1]
    if suffix.lower() == 'stl':
        stlWriter = vtk.vtkSTLWriter()
        stlWriter.SetFileName(path)
        stlWriter.SetInputConnection(mesh)
        stlWriter.Write()

    elif suffix.lower() == 'ply':
        plyWriter = vtk.vtkPLYWriter()
        plyWriter.SetFileName(path)
        plyWriter.SetInputConnection(mesh)
        plyWriter.Write()

    elif suffix.lower() == 'obj':
        pass
    elif suffix.lower() == 'off':
        pass
    else:
        print("Error: Invalid inputs.")

