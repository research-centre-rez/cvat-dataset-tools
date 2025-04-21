# CVAT dataset tools

## Description

CLI tool for uploading images into CVAT in batch mode, automatically organizing them into a project and splitting them into separate tasks.


## Structure

```bash
├── README.md
├── app.py
├── assets
│   └── default_images
│       ├── fuel_rod1.jpg
│       └── fuel_rod2.jpg
├── config
│   └── labels.json
├── pyproject.toml
└── src
    └── uploader
        ├── __init__.py
        └── uploader.py
```

**app.py** - script for running the code
**assets** - folder with data the application will be processing
**config** - folder with configuration files
**src.uploader** - folder with the source code
**pyproject.toml** - configuration file for the project


## Installation

This library can be installed as a module using pip

Create a virtual environment and activate it. Then install the application via pip.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

Consider using flag `-e` for editable mode e.g.

```bash
pip install -e .
```
Before working with the code, for security reasons do the following steps to protect your password:

For linux users:
```bash
read -s -p "Password: " SCR_PASS
```
For MacOS users (copy and paste both commands into the terminal at the same time):
```bash
echo -n "Password: "
read -s SCR_PASS
```

## Usage

This can be run either as a script with the following commands

```bash
$ python app.py --help

usage: app.py [-h] [--project-name PROJECT_NAME] [--image-dir IMAGE_DIR]
              [--images-per-task IMAGES_PER_TASK] --username USERNAME
              --password PASSWORD [--debug]

CVAT CLI tool to upload images in batches as tasks in a project.

options:
  -h, --help            show this help message and exit
  --project-name PROJECT_NAME
                        Name of the CVAT project to create or reuse (default: Auto
                        Project)
  --image-dir IMAGE_DIR
                        Directory with .jpg/.png images (default: assets/)
  --images-per-task IMAGES_PER_TASK
                        Number of images per one generated task (default: 10)
  --username USERNAME   CVAT username
  --password PASSWORD   CVAT password
  --debug               Enable debug logging
```

**Example**:

CLI:
```
python app.py \
  --image-dir assets/data_1 \
  --images-per-task 50 \
  --username your_username \
  --password your_password \
  --project-name "Your_project_name" \
  --debug #if necessary
```

## License

This project is proprietary and confidential. All rights reserved.
