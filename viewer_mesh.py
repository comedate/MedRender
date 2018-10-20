
import vtk
import viewer_data_loader

renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

reader = viewer_data_loader.reader

skinExtractor = vtk.vtkContourFilter()
skinExtractor.SetInputConnection(reader.GetOutputPort())
skinExtractor.SetValue(0, 500)

skinNormals = vtk.vtkPolyDataNormals()
skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
skinNormals.SetFeatureAngle(60.0)

skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinNormals.GetOutputPort())
skinMapper.ScalarVisibilityOff()

skin = vtk.vtkActor()
skin.SetMapper(skinMapper)

outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0, 0, 1)

aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

aCamera.Azimuth(30.0)
aCamera.Elevation(30.0)

renderer.AddActor(outline)
renderer.AddActor(skin)
renderer.SetActiveCamera(aCamera)
renderer.ResetCamera()
aCamera.Dolly(1.5)

renderer.SetBackground(0.2, 0.3, 0.4)
renWin.SetSize(320, 240)

renderer.ResetCameraClippingRange()
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()

