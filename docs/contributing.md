

## Setting up local developement environment
- Pull the latest stable release from the master branch.
- Ideally create a new python environment.
- Do not install and uninstall existing packages of pyviz3d in your local environment. This guarantees that you are running your code and not the one from the installed package.
- The examples in `examples` are a good starting point for developing new features.
- When running code (e.g. `examples/example_instance.py`) set your working directory to the root directory of the code base such that the path to the pyviz module is correct.

## Documentation
The documentation pages are mainted using [mkdocs](https://www.mkdocs.org/).

* To update the documentation modify the markdown files in `docs/*.md`.
* When adding new pages, modify the file `mkdocs.yml` accordingly.
* The locally test the documentation, go to `./` and run `mkdocs serve`. 
* To deploy the documentation: `mkdocs gh-deploy`.

Automatically generating the documentation from docstrings:

* Install the mkdocstrings plugin for mkdocs: `pip install mkdocstrings`
* Add the plugin to the `mkdocs.yaml':
'''# mkdocs.yml
plugins:
  - mkdocstrings'''
