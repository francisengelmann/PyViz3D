import vtk


class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent, pointcloud):
        vtk.vtkInteractorStyleTrackballCamera.__init__(self)
        self.parent = parent
        self.pointcloud = pointcloud
        self.AddObserver("KeyPressEvent", self.key_press_event)

    def key_press_event(self, obj, event):
        key = self.parent.GetKeySym()
        if key == '+':
            point_size = self.pointcloud.vtkActor.GetProperty().GetPointSize()
            self.pointcloud.vtkActor.GetProperty().SetPointSize(point_size + 1)
            print(str(point_size) + " " + key)
        return
