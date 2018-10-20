'''
This file is mainly to VolumeRendering to Get Image2D using vtkGPURaycastingMapper and vtkRender
'''
# coding=utf-8
from vtk import *

import md_render_common

class RendererVR( md_render_common.ISerialization ):
    '''
    This Class is mainly to render volume and mask with parameters such as camera, lut, light and so

    '''
    def set_volume(self, volume):
        '''

        :param volume: Type: vtkI
        :return:
        '''
        pass


    def set_mask(self, volumemask):
        '''
        Set the Volume Mask which is often one of the segment results.
        Voxel Value CAN ONLY be 0, 1, 2. The Dim should be the same of Volume
        :param volumemask: Type Of vtk.vtkImageData
        :return:
        '''
        pass


    def set_display_size(self, width = 512, height = 512):
        '''
        Set the render result width and height. Default value is 512, 512
        :param width:
        :param height:
        :return:
        '''

    def set_output_type(self, itype):
        '''

        :param itype: 0 RGBA,  1, RGB,  2 Raw
        :return:
        '''


    def set_camera(self, camera):
        '''

        :param camera: type of vtk.vtkCamera
        :return:
        '''
        pass

    def get_camera(self):
        '''
        Get Camera To Implement Logic
        :return: vtk.camera
        '''
        pass


    def set_render_mode(self, mode):
        '''

        :param mode: int
        :return:
        '''
        pass


    def set_windowlevel(self, ww, wl, layer = 0):
        '''
        :param ww: float windowwidth
        :param wl: float windowlevel
        :param 0:  int 0, change WWWL for different layer
        :return:
        '''
        pass


    def set_lut(self, color, opactiy, layer = 0):
        '''
        Set Color and Opacity for Volume and Mask. For volume , use defual layer = 0
        For Mask , use layer = 1, or layer = 2
        :param color: vtkColorTransferFunction
        :param opactiy: vtkPiecewiseFunction
        :param layer:  default is 0. Layer can be 1, 2 for mask use
        :return:
        '''
        pass


    def set_ligth(self, light):
        '''
        ligth parameters include diffuse_color, specular_color, ambient_color, position, direction
        :param light: vtk.vtklight
        :return:
        '''
        pass

    def set_background_color(self, r, g, b):
        '''
        set background color
        :param r:
        :param g:
        :param b:
        :return:
        '''
        pass



    def pre_render(self):
        '''
        Before render, should to judge wther need to render
        :return:
        '''
        pass


    def render(self):
        '''

        :return:bool
        '''
        pass


    def post_render(self):
        '''
        After render, should do something
        :return:
        '''
        pass


    def get_render_result(self):
        '''
        Render Result： Type  vtkImageData
        :return:vtkImageData
        '''
