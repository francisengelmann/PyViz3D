

## Setting up local developement environment
- Pull the latest stable release from the master branch.
- Ideally create a new python environment.
- Do not install and uninstall existing packages of pyviz3d in your local environment. This guarantees that you are running your code and not the one from the installed package.
- Run your code (i.e. examples) from the root of the code base so guarantee all pathes are correct.

## Documentation
The documentation pages are mainted using [mkdocs](https://www.mkdocs.org/).

* To update the documentation modify the markdown files in `docs/*.md`.
* When adding new pages, modify the file `mkdocs.yml` accordingly.
* The locally test the documentation, go to `'./'` and run `mkdocs serve`. 
* To deploy the documentation: `mkdocs gh-deploy`.