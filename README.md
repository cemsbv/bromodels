# BROmodels
The GEOTOP and REGIS data is downloaded from the DINOloket OPeNDAP server.

More information about the GEOTOP or REGIS:

- https://www.dinoloket.nl/en/search-and-request-geotop
- https://www.dinoloket.nl/en/regis-ii-hydrogeological-model
- http://dinodata.nl/opendap/

***Please note that an active internet connections is mandatory!***

# Installation

To install this package run:

```bash
pip install bromodels
```

# Contribution

## Environment

We recommend developing in Python3.9 with a clean virtual environment (using `virtualenv` or `conda`), installing the
requirements from the requirements.txt file:

Example using `virtualenv` and `pip` to install the dependencies in a new environment .env on Linux:

```bash
python -m venv .env
source activate .env/bin/activate
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
pip install -e .
```

## Documentation

Build the docs:

```bash
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
pip install .
sphinx-build -b html docs public
```

## Format

We format our code with black and isort.

```bash
black --config "pyproject.toml" src tests examples docs
isort --settings-path "pyproject.toml" src tests examples docs
```

## Lint

To maintain code quality we use the GitHub super-linter.

To run the linters locally, run the `run_super_linters.sh` bash script from the root directory.

## UnitTest

Test the software with the use of coverage:

```bash
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt
pip install .
coverage run -m pytest
```

## Requirements

Requirements are autogenerated by `pip-compile` with python 3.9

```bash
pip-compile --extra=test --extra=docs --extra=lint --extra=3d --output-file=requirements.txt pyproject.toml
```

To update the requirements within the defined ranges, run:

```bash
pip-compile --upgrade --extra=test --extra=docs --extra=lint --extra=3d --output-file=requirements.txt pyproject.toml
```