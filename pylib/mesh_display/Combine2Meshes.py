'''
Script Name: Combine_2_MultiMeshes
Author: Yang Yuxin
Created: 2019/12/28
Last modified: 
Version: 0.1
Description: Combine two meshes file
            input: mesh1: (vtkCommonDataModelPython.vtkPolyData)  mesh2: (vtkCommonDataModelPython.vtkPolyData)
            output: (vtkCommonDataModelPython.vtkPolyData)

'''

import vtk

def Combine_2_MultiMeshes(mesh1, mesh2):
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

'''
# function for testing
def test():
    colors = vtk.vtkNamedColors()

    # Set the background color.
    colors.SetColor("BkgColor", [0.3, 0.2, 0.1, 1.0])

    input1 = vtk.vtkPolyData()
    input2 = vtk.vtkPolyData()

    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(5, 0, 0)
    sphereSource.Update()

    input1.ShallowCopy(sphereSource.GetOutput())

    coneSource = vtk.vtkConeSource()
    coneSource.Update()

    input2.ShallowCopy(coneSource.GetOutput())

    result = Combine_2_MultiMeshes(input1, input2)

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(result.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actors to the scene
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d("BkgColor"))

    # Render and interact
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderer.GetActiveCamera().Zoom(0.9)
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == "__main__":
    test()
'''