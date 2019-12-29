<p align="center"><img width="40%" src="docs/img/pyviz3d-logo.png" /></p>

----
PyViz3D is a Python package to visualize 3D point clouds.

### Installation
Using pip:
```pip install pyviz3d```

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

#### Distributing
The maintainers of the package keep the recent version of the ```pyviz3d``` package available on [PyPy](https://packaging.python.org/tutorials/packaging-projects/) and Anaconda.
The anaconda package is created from the pypi package.

##### PyPi

Loosely following the instructions from [[1](https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56)]

```
$ pip install twine
```

To test the release without messing around with the public PyPi release:
```
$ python setup.py sdist bdist_wheel
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```


When happy, prepare a new release on github:
```
https://github.com/francisengelmann/pyviz3d/releases
```

When done, we can upload the release to the public PyPi repository:
```
$ python setup.py sdist bdist_wheel
$ twine upload dist/*
```

##### Anaconda

We rely on Anaconda Cloud to host the pyviz3d package
[[2]]( https://docs.anaconda.com/anaconda-cloud/user-guide/tasks/work-with-packages/)
```
$ conda install anaconda-client conda-build conda-verify
$ conda config --set anaconda_upload no
$ conda skeleton pypi pyviz3d
$ conda build pyviz3d
```
