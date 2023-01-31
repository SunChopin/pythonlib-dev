# Author: Yang Yuxin
# Created: 2019/12/28
# mod date record 2020-3-28 version 0.1 xingchuang wen

import os
import vtk

def Read_Meshfile(path):
    r"""
    Read mesh files like .stl .ply .obj .off

    Args:
    path

    Return:
    mesh

    Example::
        >>> reader = Read_MeshFile('C:/Users/zenod/Desktop/a.obj')

    """
    suffix = os.path.splitext(path)[1]
    if suffix.lower() == '.stl':
        stlReader = vtk.vtkSTLReader()
        stlReader.SetFileName(path)
        stlReader.Update()
        return stlReader
    elif suffix.lower() == '.ply':
        plyReader = vtk.vtkPLYReader()
        plyReader.SetFileName(path)
        plyReader.Update()
        return plyReader
    elif suffix.lower() == '.obj':
        objReader = vtk.vtkOBJReader()
        objReader.SetFileName(path)
        objReader.Update()
        return objReader
    elif suffix.lower() == '.off':
        off2obj(path, "./tmp.obj")
        objReader = vtk.vtkOBJReader()
        objReader.SetFileName("./tmp.obj")
        objReader.Update()
        os.remove("./tmp.obj")
        return objReader
    else:
        print("Error: Invalid input path.")

# function for converting .off file to .obj file
def off2obj(offpath, objpath):
    vset = []
    fset = []

    with open(offpath, 'r') as f:
        lines = f.readlines()
    
    counter = 0

    for line in lines:
        if counter < 2:
            counter += 1
            continue
        
        line = line.split("\n")[0]
        parameters = line.split(" ")
        parameters = [x.strip() for x in parameters if x.strip()!='']
        if len(parameters) == 3:
            point = []
            point.append(eval(parameters[0]))
            point.append(eval(parameters[1]))
            point.append(eval(parameters[2]))
            vset.append(point)

        elif len(parameters) == 4:
            face = []
            face.append(eval(parameters[1]) + 1)
            face.append(eval(parameters[2]) + 1)
            face.append(eval(parameters[3]) + 1)
            fset.append(face)
            
    with open(objpath, 'w') as out:
        for i in range(len(vset)):
            out.write("v " + str(vset[i][0]) + " " + str(vset[i][1]) + " " + str(vset[i][2]) + "\n")

        for i in range(len(fset)):
            out.write("f " + str(fset[i][0]) + " " + str(fset[i][1]) + " " + str(fset[i][2]) + "\n")
