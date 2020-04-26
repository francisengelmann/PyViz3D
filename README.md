<p align="center"><img width="40%" src="docs/img/pyviz3d-logo.png" /></p>

----
PyViz3D is a Python package to visualize 3D point clouds.

### Installation
Using [pip](https://pypi.org/project/pyviz3d/):
```pip install pyviz3d```

Using [conda](https://anaconda.org/francisengelmann/pyviz3d):
```conda install -c francisengelmann pyviz3d```

### Getting started
Minimal example:
```python
import numpy as np
import pyviz3d as viz

points = np.array([[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]])  # Define 3D points
colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])  # Define corresponding colors

viz.show_pointclouds([points], [colors])  # Display point cloud
```

<p align="center"><img width="20%" src="docs/img/minimal_example.png" /></p>

### Contributing
You are more then welcome to contribute your own changes via github pull requests. 

We recommend developing in a conda environment.
From your console, create a new conda environment (using python <=3.7, required for VTK) and activate it:
```bash
$ conda create --name <environment_name> python=3.7
$ conda activate <environment_name>
```