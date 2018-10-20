# coding=utf-8
import numpy as np
from vtk import *
import md_common


class RendererMPR():
    def __init__(self):
        """
        This Class is mainly to render volume and mask with parameters such as camera, lut, light and so
        Condition: This class can only used in GPU
        """
        self._imageReslice = vtk.vtkImageReslice()
        self._lookupTable = vtk.vtkLookupTable()
        self._imageMapToColors = vtk.vtkImageMapToColors()
        self._imageMapToColors.SetLookupTable(self._lookupTable)

        self._imageActor = vtk.vtkImageActor()
        self._renderer = vtk.vtkRenderer()
        self._renderWindow = vtk.vtkRenderWindow()
        self._camera = vtk.vtkCamera()
        self._sliceAxis = vtk.vtkMatrix4x4()
        self._bg_color = [0, 0, 0]

        self._renderWindow.AddRenderer(self._renderer)
        self._windowToImageFilter = vtk.vtkWindowToImageFilter()
        self._windowToImageFilter.SetInput(self._renderWindow)  # 保存成图片格式
        self._pngWriter = vtk.vtkPNGWriter()

        self._pngWriter.SetInputConnection(self._windowToImageFilter.GetOutputPort())

        # self._interactorStyle = vtk.vtkInteractorStyleImage()
        # self._interactor = vtk.vtkRenderWindowInteractor()
        # self._interactor.SetInteractorStyle(self._interactorStyle)
        # self._renderWindow.SetInteractor(self._interactor)

    def set_volume(self, volume):
        """
        :param volume: Type: vtkImageData
        :return:
        """
        # Set Volume and Volume Property
        self._imageReslice.SetInputConnection(volume.GetOutputPort())
        self._imageReslice.SetOutputDimensionality(2)
        self._imageReslice.SetInterpolationModeToLinear()
        self._imageMapToColors.SetInputConnection(self._imageReslice.GetOutputPort())

        # Calculate Slice Axis  Which can calculate camera parameters
        (xMin, xMax, yMin, yMax, zMin, zMax) = volume.GetOutput().GetExtent()
        (xSpacing, ySpacing, zSpacing) = volume.GetOutput().GetSpacing()
        (x0, y0, z0) = volume.GetOutput().GetOrigin()
        center = [x0 + xSpacing * 0.5 * (xMin + xMax),
                  y0 + ySpacing * 0.5 * (yMin + yMax),
                  z0 + zSpacing * 0.5 * (zMin + zMax)]
        self._sliceAxis.DeepCopy((0, 0, -1, center[0],
                           1, 0, 0, center[1],
                           0, -1, 0, center[2],
                           0, 0, 0, 1))
        self._imageReslice.SetResliceAxes(self._sliceAxis)

    def set_mask(self, mask):
        """
        Set the Volume Mask which is often one of the segment results.
        Voxel Value CAN ONLY be 0, 1, 2. The Dim should be the same of Volume
        :param mask: Type Of vtk.vtkImageData
        :return:
        """
        pass

    def set_output_image_size(self, width=512, height=512):
        """
        Set the render result width and height. Default value is 512, 512
        :param width:
        :param height:
        :return:
        """
        self._renderWindow.SetSize(width, height)

    def get_output_image_size(self):
        """
        Set the render result width and height. Default value is 512, 512
        :return width, height:
        """
        size = {}
        self._renderWindow.GetSize(size)
        return size

    def set_output_type(self, itype):
        """

        :param itype: 0 RGBA,  1, RGB,  2 Raw
        :return:
        """

    def set_sample_rate(self, rate = 0.5):
        """
        :param rate: Sample Rate， usually use 0.5 if for GPU Render
        :return:
        """
        pass

    def set_camera(self, camera):
        """

        :param camera: type of vtk.vtkCamera
        :return:
        """
        md_common.logging.info("Set Camera:" + str(camera))

        # Calculate SliceAxis According Camera Parameters

        camera_pos = camera.GetPosition()
        camera_focal = camera.GetFocalPoint()
        z_dir = [camera_pos[0] - camera_focal[0], camera_pos[1] - camera_focal[1], camera_pos[2] - camera_focal[2]]
        z_dir_norm = np.linalg.norm(z_dir, ord=2)
        z_dir_normalized = z_dir / z_dir_norm
        # print("z_dir_normalized" + str(z_dir_normalized[0]) + str(z_dir_normalized[1]) + str(z_dir_normalized[2]))
        # md_common.logging("Z-dir: " + z_dir_normalized)
        camera_view_up = camera.GetViewUp()
        camera_view_up = camera_view_up / np.linalg.norm(camera_view_up)
        x_dir_normal = np.cross(camera_view_up, z_dir_normalized)

        md_common.logging.info("Self._sliceAxis Begin:" + str(self._sliceAxis))
        self._sliceAxis.DeepCopy((x_dir_normal[0], camera_view_up[0], z_dir_normalized[0], camera_focal[0],
                                  x_dir_normal[1], camera_view_up[1], z_dir_normalized[1], camera_focal[1],
                                  x_dir_normal[2], camera_view_up[2], z_dir_normalized[2], camera_focal[2],
                                  0, 0, 0, 1))
        self._imageReslice.SetResliceAxes(self._sliceAxis)
        md_common.logging.info("Self._sliceAxis After:" + str(self._sliceAxis))
        self._imageReslice.Update()

        self._renderer.SetActiveCamera(camera)

    def get_camera(self):
        """
        Get Camera To Implement Logic
        :return: vtk.camera
        """
        return self._renderer.GetActiveCamera()

    def set_blend_mode(self, mode):
        """
        COMPOSITE_BLEND 0,  MAXIMUM_INTENSITY_BLEND  1,  MINIMUM_INTENSITY_BLEND  2,  AVERAGE_INTENSITY_BLEND  3,  ADDITIVE_BLEND  4,  ISOSURFACE_BLEND  5
        :param mode: int
        :return:
        """
        pass

    def set_window_width_level(self, ww, wl, label = 0):
        """
        :param ww: float windowwidth
        :param wl: float windowlevel
        :param label: Default value is 0 means set WWWL to volume. Change WWWL according label (Mask Voxel Value)
        :return:
        """
        pass

    def set_lut_property(self, property, label=0):
        """
        property["color"]
        property["opacity"]
        property["opacityGrad"]
        property["phong"]  Parameters: diffuse_color, specular_color, ambient_color, ( Optional: position, direction )
        :param property:
        :return:
        """
        # Set Default LookupTable
        self._lookupTable.SetRange(0, 2000)
        self._lookupTable.SetRange(0, 2000)  # image intensity range
        self._lookupTable.SetValueRange(0.0, 1.0)  # from black to white
        self._lookupTable.SetSaturationRange(0.0, 0.0)  # no color saturation
        self._lookupTable.SetRampToLinear()
        self._lookupTable.Build()

        # Set ImageMapToColors
        self._imageMapToColors.SetLookupTable(self._lookupTable)
        self._imageMapToColors.SetInputConnection(self._imageReslice.GetOutputPort())

        # Set Image Actor
        self._imageActor.GetMapper().SetInputConnection(self._imageMapToColors.GetOutputPort())

        # Add Actor
        self._renderer.AddActor(self._imageActor)

        md_common.logging.info("SetLutProperty: " + str(self._lookupTable) )

    def get_lut_property(self, label=0):
        """
        get lut property by label
        :return:
        """

    def set_background_color(self, r, g, b):
        """
        set background color
        :param r:
        :param g:
        :param b:
        :return:
        """
        self._bg_color = [r, g, b]
        #self._renderer.

    def pre_render(self):
        """
        Before render, should to judge wther need to render
        :return bool :
        """

        return True

    def render(self):
        """
        :return:bool
        """
        md_common.logging.info("Render MPR Begin!")

        try:
            #self._renderer.render()
            self._renderWindow.Render()
            #self._interactor.start()
        except BaseException as e:
            md_common.logging.error("Exception:" + str(e))

        md_common.logging.info("Render MPR End!")


    def post_render(self):
        """
        After render, should do something
        :return:
        """

        return True

    def get_output_image_result(self):
        """
        Render Result： Type  vtkImageData
        :return:vtkImageData
        """
        self._windowToImageFilter.update()
        return self

    def get_output_png_image(self, filename):
        """
        Output Result is png image
        :param filename:
        :return:
        """
        md_common.logging.info("Get Output PNG Result Begin!")
        try:
            self._pngWriter.SetFileName(filename)
            self._pngWriter.Write()
            self._pngWriter.Update()
            md_common.logging.info("pngWriter" + str(self._pngWriter))
        except BaseException as e:
            md_common.logging.error("Exception:" + str(e))
        md_common.logging.info("Get Output PNG Result End!")

    def update(self):
        """
        Use this methods to set flag whether it need render again.
        :return:
        """
        pass
