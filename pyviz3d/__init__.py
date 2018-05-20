import vtk
import numpy as np
from .pointcloud import PointCloud

def test():
    print("Hello PyViz3D")

def show_pointclouds(points, colors, title="Default"):
    """ Show multiple point clouds specified as lists. First clouds at the bottom.
    points: list of pointclouds, item: numpy (N x 3) XYZ
    colors: list of corresponding colors, item: numpy (N x 3) RGB [0..255]
    title:  window title
    """

    assert isinstance(points, type([])),  "Pointclouds argument must be a list!"
    assert isinstance(colors, type([])),  "Colors argument must be a list!"
    assert len(points) == len(colors), \
        "Number of pointclouds (%d) is different then number of colors (%d)" % (len(points), len(colors))

    num_pointclouds = len(points)  # Number of pointclouds to be displayed in this window

    pointclouds = [PointCloud() for _ in range(num_pointclouds)]
    renderers = [vtk.vtkRenderer() for _ in range(num_pointclouds)]

    height = 1.0/num_pointclouds
    viewports = [(i*height, (i+1)*height) for i in range(num_pointclouds)]

    # Iterate over all given point clouds
    for i, pc in enumerate(points):
        pc = pc.squeeze()
        co = colors[i].squeeze()
        assert pc.shape[0] == co.shape[0], \
            "Expected same number of points (%d) then colors (%d), cloud index = %d" % (pc.shape[0], co.shape[0], i)
        assert pc.shape[1] == 3, "Expected points to be N x 3, got N x %d" % pc.shape[1]
        assert co.shape[1] == 3, "Expected colors to be N x 3, got N x %d" % co.shape[1]

        # For each point cloud iterate over all points
        for j in range(pc.shape[0]):
            point = pc[j, :]
            color = co[j, :]
            pointclouds[i].add_point(point, color)

        renderers[i].AddActor(pointclouds[i].vtkActor)
        renderers[i].AddActor(vtk.vtkAxesActor())
        renderers[i].SetBackground(1.0, 1.0, 1.0)
        renderers[i].SetViewport(0.0, viewports[i][0], 1.0, viewports[i][1])
        renderers[i].ResetCamera()

    # Render Window
    render_window = vtk.vtkRenderWindow()
    for renderer in renderers:
        render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    render_window_interactor.SetRenderWindow(render_window)

    [center_x, center_y, center_z] = np.mean(points[0].squeeze(), axis=0)
    camera = vtk.vtkCamera()
    d = 10
    camera.SetViewUp(0, 0, 1)
    camera.SetPosition(center_x + d, center_y + d, center_z + d / 2)
    camera.SetFocalPoint(center_x, center_y, center_z)
    camera.SetClippingRange(0.002, 1000)
    for renderer in renderers:
        renderer.SetActiveCamera(camera)

    # Begin Interaction
    render_window.Render()
    render_window.SetWindowName(title)
    render_window.SetSize(1200, 800)
    render_window_interactor.Start()
