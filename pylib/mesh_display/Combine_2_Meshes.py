# Author: Yang Yuxin
# Created: 2019/12/28
# mod date record 2020-3-28 version 0.1 xingchuang wen

import vtk

def Combine_2_Meshes(mesh1, mesh2):
    r"""
    Combine two meshes file

    args:
    mesh1: (vtkCommonDataModelPython.vtkPolyData)  
    mesh2: (vtkCommonDataModelPython.vtkPolyData)

    return:
    mesh: (vtkCommonDataModelPython.vtkPolyData)

    Example::
        >>> mesh1 = Read_MeshFile('C:/Users/zenod/Desktop/a.obj')
        >>> mesh2 = Read_MeshFile('C:/Users/zenod/Desktop/b.obj')
        >>> mesh = Combine_2_Mesh(mesh1, mesh2)

    """


    # Append the two meshes
    appendFilter = vtk.vtkAppendPolyData()
    appendFilter.AddInputData(mesh1)
    appendFilter.AddInputData(mesh2)
    appendFilter.Update()

    # Remove any duplicate points.
    cleanFilter = vtk.vtkCleanPolyData()
    cleanFilter.SetInputConnection(appendFilter.GetOutputPort())
    cleanFilter.Update()

    return cleanFilter

