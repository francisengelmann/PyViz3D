<p align="center"><img width="40%" src="docs/img/pyviz3d-logo.png" /></p>

----
PyViz3D is a Python package to visualize 3D point clouds.

### Installation
Run this command:
```pip install pyviz3d```

### Getting started
Minimal example:
```python
import numpy as np
import pyviz3d as viz

points = np.array([[2,0,0],[0,2,0],[0,0,2]])  # Define 3D points
colors = np.array([[255,0,0],[0,255,0],[0,0,255]])  # Define corresponding colors

viz.show_pointclouds([points], [colors])  # Display point cloud
```

<p align="center"><img width="20%" src="docs/img/minimal_example.png" /></p>

### Development
We recommend developing in a conda environment:
- conda create --name <environment_name> python=3.7
- conda activate <environment_name>

#### Distribution with PyPI
https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
- pip install twine
- python setup.py sdist
- twine upload dist/*

#### Distribution with Anaconda Cloud

We rely on Anaconda Cloud to host the pyviz3d package, as described in https://docs.anaconda.com/anaconda-cloud/user-guide/tasks/work-with-packages/
- conda install anaconda-client conda-build conda-verify
- conda config --set anaconda_upload no

Two files are required: build.sh and meta.yaml

- conda build .

It's great to add a new release on github: https://github.com/francisengelmann/pyviz3d/releases
