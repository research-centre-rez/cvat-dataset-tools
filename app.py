import argparse
import logging
import json
from pathlib import Path
import urllib3
import requests
from uploader import disable_ssl_verification, authenticate, create_project, upload_batches
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = ""

def create_parser():
    parser = argparse.ArgumentParser(
        description="CVAT CLI tool to upload images in batches as tasks in a project."
    )

    parser.add_argument(
        "--project-name",
        type=str,
        help="Name of the CVAT project to create or reuse",
    )

    parser.add_argument(
        "--image-dir",
        type=Path,
        help="Directory with .jpg/.png images",
    )

    parser.add_argument(
        "--images-per-task",
        type=int,
        default=10,
        help="Number of images per one generated task (default: 10)",
    )
    parser.add_argument(
        "--username",
        type=str,
        required=True,
        help="CVAT username",
    )
    parser.add_argument(
        "--password",
        type=str,
        required=True,
        help="CVAT password",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()

def setup_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def load_config(path="config/labels.json"):
    with open(path) as f:
        return json.load(f)

def main():
    args = create_parser()
    setup_logging(args.debug)
    logging.debug(f"Parsed arguments: {args}")

    disable_ssl_verification()
    logging.debug("SSL verification disabled")

    session = requests.Session()
    session.verify = False
    host = "https://stinger.ad.ujv.cz"
    logging.debug(f"Session initialized. Host: {host}")

    authenticate(session, host, args.username, args.password)
    logging.debug("Authenticated successfully")

    client, project = create_project(session, host, args.username, args.password, args.project_name)
    logging.debug(f"Project ready: {project.name} (ID: {project.id})")

    upload_batches(client, session, host, project, args.image_dir, args.images_per_task)

if __name__ == "__main__":
    main()
