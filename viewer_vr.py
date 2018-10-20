#!/usr/bin/env python

# This is a simple volume rendering example that uses a
# vtkGPUVolumeRayCastMapper

import vtk
import logging
import viewer_data_loader

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ViewerVR:
    '''
    VR Render API
    '''
    def __init__(self, reader):
        logging.info("begin Init ViewerVR")
        self._reader = reader
        #init VolumeRayCastMapper
        self._volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
        self._volumeMapper.SetSampleDistance(self._volumeMapper.GetSampleDistance()/2)
        self._volumeMapper.SetBlendModeToComposite()
        self._volumeMapper.SetInputConnection(reader.GetOutputPort())

        self._volumeColor = vtk.vtkColorTransferFunction()
        self._volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        self._volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        self._volumeProperty = vtk.vtkVolumeProperty()

        self._volume = vtk.vtkVolume()
        self._render = vtk.vtkRenderer()
        logging.info("End Init ViewerVR")

    def set_lut(self):
        self._volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
        self._volumeColor.AddRGBPoint(500, 1.0, 0.5, 0.3)
        self._volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
        self._volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

        self._volumeScalarOpacity.AddPoint(0, 0.00)
        self._volumeScalarOpacity.AddPoint(500, 0.15)
        self._volumeScalarOpacity.AddPoint(1000, 0.15)
        self._volumeScalarOpacity.AddPoint(1150, 0.85)

        self._volumeGradientOpacity.AddPoint(0, 0.0)
        self._volumeGradientOpacity.AddPoint(90, 0.5)
        self._volumeGradientOpacity.AddPoint(100, 1.0)

        self._volumeProperty.SetColor(self._volumeColor)
        self._volumeProperty.SetScalarOpacity(self._volumeScalarOpacity)
        self._volumeProperty.SetGradientOpacity(self._volumeGradientOpacity)
        self._volumeProperty.SetInterpolationTypeToLinear()
        self._volumeProperty.ShadeOn()
        self._volumeProperty.SetAmbient(0.4)
        self._volumeProperty.SetDiffuse(0.6)
        self._volumeProperty.SetSpecular(0.2)

    def set_mapper_and_property(self):
        self._volume.SetMapper(self._volumeMapper)
        self._volume.SetProperty(self._volumeProperty)

    def set_volume(self):
        self._render.AddVolume(self._volume)
        self._render.SetBackground(0, 0, 0)

    def get_render(self):
        return self._render

    def get_volume(self):
        return self._volume

# Init viewer_vr
viewer_vr = ViewerVR(viewer_data_loader.reader)
viewer_vr.set_lut()
viewer_vr.set_mapper_and_property()
viewer_vr.set_volume()
viewer_vr.get_render()

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer( viewer_vr.get_render() )
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renWin.SetSize(600, 600)
renWin.Render()

def CheckAbort(obj, event):
    if obj.GetEventPending() != 0:
        obj.SetAbortRender(1)

renWin.AddObserver("AbortCheckEvent", CheckAbort)

iren.Initialize()
renWin.Render()
iren.Start()
