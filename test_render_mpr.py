
import vtk
from vtk.util.misc import vtkGetDataRoot
import viewer_mpr

import md_render_mpr

# reader = vtk.vtkMetaImageReader()
# reader.SetFileName("C:\\Users\\fei.wang\\PycharmProjects\\Rendering\\data\\org.mha")
# reader.Update()

reader = viewer_mpr.reader

render_mpr = md_render_mpr.RendererMPR()
render_mpr.set_volume(reader)
render_mpr.set_output_image_size(1024, 1024)
render_mpr.set_lut_property("")
render_mpr.render()
render_mpr.get_output_png_image("1.png")

# test Camera
cur_camera = render_mpr.get_camera()
print("cur_camera:" + str(cur_camera))
render_mpr.set_camera(cur_camera)
render_mpr.render()

