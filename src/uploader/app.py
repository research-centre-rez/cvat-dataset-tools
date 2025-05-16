import argparse
import importlib
import logging
import json
from pathlib import Path
import urllib3
import requests
import sys
import os

from uploader import disable_ssl_verification, authenticate, find_or_create_project, upload_batches
from cvat_sdk.core import make_client

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = ""

def create_parser():
    parser = argparse.ArgumentParser(prog="cvat-dataset-tools",
                                     description="CVAT CLI tool to upload images in batches as tasks in a project")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upload_parser = subparsers.add_parser("upload", help="Upload images in batches to CVAT")
    upload_parser.add_argument("--project-name", type=str, help="Name of the CVAT project to create or reuse")
    upload_parser.add_argument("--image-dir", type=Path, help="Directory with .jpg/.png images")
    upload_parser.add_argument("--images-per-task", type=int, default=10,
                               help="Number of images per one generated task (default: 10)")
    upload_parser.add_argument("--username", type=str, required=True, help="CVAT username")
    upload_parser.add_argument("--password", type=str, required=True, help="CVAT password")
    upload_parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    upload_parser.add_argument("--reuse-project", action="store_true",
                               help="If set, reuse the existing project owned by the current user. If a project with the same name exists but belongs to another user, a new one will be created. CVAT allows duplicate project names across users.")

    dump_parser = subparsers.add_parser("dump-label-config", help="Print default label config to stdout")
    return parser.parse_args()

def setup_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def load_config(path="config/default_label_config.json"):
    module_path = importlib.resources.files(__package__)
    config_path = module_path.joinpath(path)
    with open(config_path) as f:
        return json.load(f)

def main():
    args = create_parser()

    if args.command == "dump-label-config":
        json.dump(load_config(), sys.stdout, indent=4, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    setup_logging(args.debug)
    logging.debug(f"Parsed arguments: {args}")

    disable_ssl_verification()
    logging.debug("SSL verification disabled")

    session = requests.Session()
    session.verify = False
    host = "https://stinger.ad.ujv.cz"
    logging.debug(f"Session initialized. Host: {host}")

    try:
        authenticate(session, host, args.username, args.password)
        logging.info("Authenticated successfully")

        client = make_client(host=host, credentials=(args.username, args.password))
        labels = load_config()

        project = find_or_create_project(
            client=client,
            project_name=args.project_name,
            #labels=labels,
            reuse_if_exists=args.reuse_project
        )
        logging.info(f"Project ready: {project.name} (ID: {project.id})")

        upload_batches(client, session, host, project, args.image_dir, args.images_per_task)

    except RuntimeError as e:
        logging.error(str(e))
        return 1

if __name__ == "__main__":
    main()
