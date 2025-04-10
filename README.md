# YOUR project name

## Description

This is where you put the description of your project. In this example, there is an application that either inverts or thresholds it based on user input. 

## Structure

```bash
├── README.md
├── app.py
├── assets
├── config
├── notebooks
│   └── example.md
├── src
│   └── image_stuff
└── pyproject.toml
```

**app.py** - script for running the code
**assets** - folder with data required for the application
**config** - folder with configuration files
**notebooks** - folder with notebooks. Note that the notebooks are stored in markdown format. Use `jupytext --to ipynb <notebook>` to convert them to ipynb.
**src.image_stuff** - folder with the source code
**pyproject.toml** - configuration file for the project


## Installation

This library can be installed as a module using pip

Create a virtual environment and activate it. Then install the application via pip.

```bash
pip install .
```

Consider using flag `-e` for editable mode

## Usage

This can be run either as a script with the following commands

```bash
$ python app.py --help

usage: app.py [-h] [--debug] {invert,threshold} ...

CLI tool to process images with inversion or thresholding.

positional arguments:
  {invert,threshold}  Available commands
    invert            Invert the input image.
    threshold         Apply thresholding to the input image.

options:
  -h, --help          show this help message and exit
  --debug             Enable debug mode
```

**Example**:

CLI:
```
python app.py threshold --input assets/plt.png --output output/t.png --threshold 100
python app.py invert --input assets/plt.png --output output/t.png

# activate debug logging with
python app.py --debug threshold --input assets/plt.png --output output/t.png
```

Notebook:
See example in `notebooks` folder. (Note that you need to convert `.md` to `.ipynb` using `jupytext --to ipynb <notebook>`)

## License

This project is proprietary and confidential. All rights reserved.
