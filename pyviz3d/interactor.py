import vtk

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent, pointcloud):
        self.parent = parent
        self.pointcloud = pointcloud
        self.AddObserver("KeyPressEvent", self.keyPressEvent)

    def keyPressEvent(self, obj, event):
        key = self.parent.GetKeySym()
        print('asd')
        if key == '+':
            point_size = self.pointcloud.vtkActor.GetProperty().GetPointSize()
            self.pointcloud.vtkActor.GetProperty().SetPointSize(point_size + 1)
            print(str(point_size) + " " + key)
        return
