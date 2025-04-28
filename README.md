# CVAT dataset tools

## Description

CLI tool for uploading images into CVAT in batch mode, automatically organizing them into a project and splitting them into separate tasks.


## Structure

```bash
├── README.md
├── pyproject.toml
├── example
│   └── test_images
│       ├── fuel_rod1.jpg
│       └── fuel_rod2.jpg
└── src
    └── uploader
        ├── __init__.py
        ├── uploader.py
        └── config
            └── default_label_config.json
```

**pyproject.toml** - configuration file for the project
**assets** - folder with data required by application to run (contains test images for now)
**config** - folder with configuration files
**src.uploader** - folder with the source code
**app.py** - script for running the code


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

After installing, app can be run as follows:

```bash
$ python cvat-dataset-tools --help

usage: cvat-dataset-tools [-h] [--project-name PROJECT_NAME]
                          [--image-dir IMAGE_DIR]
                          [--images-per-task IMAGES_PER_TASK]
                          [--username USERNAME] [--password PASSWORD] [--debug]
                          [--reuse-project] [--dump-config]

CVAT CLI tool to upload images in batches as tasks in a project.

options:
  -h, --help            show this help message and exit
  --project-name PROJECT_NAME
                        Name of the CVAT project to create or reuse
  --image-dir IMAGE_DIR
                        Directory with .jpg/.png images
  --images-per-task IMAGES_PER_TASK
                        Number of images per one generated task (default: 10)
  --username USERNAME   CVAT username
  --password PASSWORD   CVAT password
  --debug               Enable debug logging
  --reuse-project       If set, reuse the existing project owned by the current
                        user. If a project with the same name exists but belongs
                        to another user, a new one will be created. CVAT allows
                        duplicate project names across users.
  --dump-config         Dump all JSON configuration files and exit.
```

**Example**:

CLI:
```
python app.py \
  --image-dir example/test_images \
  --images-per-task 50 \
  --username your_username \
  --password your_password \
  --project-name "Your_project_name" \
#  [--debug]
#  [--reuse-project]
```

If you want to change the label configuration you can see the currect config via:
```
python cvat-dataset-tools --dump-config
```
Example output:
```
default_label_config.json
[
    {
        "name": "POI",
        "color": "#66ff66",
        "type": "any",
        "attributes": []
    }
]
```

## License

This project is proprietary and confidential. All rights reserved.

