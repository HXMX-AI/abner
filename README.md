# log-conditioning

## Description

This repository provides tools for oil well log conditioning.... TODO

### Initialization

1. Ensure you are in the base directory.
2. Ensure you have a python version ^3.12 installed (development requirement). A virtual environment is recommended. I suggest installing [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) for virtual env management.
3. If not already, ensure [Poetry](https://python-poetry.org/) is installed.
   - It is recommended to update the poetry config with the following commnads
   ```bash
   poetry config virtualenvs.create true
   poetry config virtualenvs.in-project true
   poetry virtualenvs.prefer-active-python true
   ```
4. Run the following command to install the dependencies:
   ```bash
   poetry install
   ```

### Adding Packages

Since Poetry is used for package management, we can use it to install additional dependencies. To install packages run `poetry add {package_name}`. If the package will only be used for development purposes (not in production) use `poetry add {package_name} --group=dev`. To remove a package run `poetry remove {package_name}`. Additional Poetry documentation can be found on the main [site](https://python-poetry.org/).
