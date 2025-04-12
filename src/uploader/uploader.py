import os
import json
import zipfile
import requests
import urllib3
import logging
from pathlib import Path
from tqdm import tqdm
from cvat_sdk.core import make_client
from cvat_sdk.models import ProjectWriteRequest, PatchedLabelRequest, TaskWriteRequest
from urllib3.poolmanager import PoolManager
from cvat_sdk.api_client import rest

# Disables SSL verification warnings + patches CVAT SDK for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = ""

def disable_ssl_verification():
    def patched_pool_manager(*args, **kwargs):
        kwargs["cert_reqs"] = "CERT_NONE"
        return PoolManager(*args, **kwargs)
    rest.urllib3.PoolManager = patched_pool_manager

def authenticate(session: requests.Session, host: str, username: str, password: str):
    session.get(f"{host}/auth/login")
    csrf_token = session.cookies.get("csrftoken")
    session.post(
        f"{host}/api/auth/login",
        json={"username": username, "password": password},
        headers={"X-CSRFToken": csrf_token, "Referer": f"{host}/auth/login"},
        cookies={"csrftoken": csrf_token}
    )

def create_project(session: requests.Session, host: str, username: str, password: str, project_name: str):
    with make_client(host=host, credentials=(username, password)) as client:
        for p in client.projects.list():
            if p.name == project_name:
                return client, p

        project = client.projects.create(
            ProjectWriteRequest(
                name=project_name,
                labels=load_labels()
            )
        )
        return client, project

def load_labels(path="config/labels.json"):
    with open(path) as f:
        labels_config = json.load(f)
    return [
        PatchedLabelRequest(
            name=label["name"],
            color=label.get("color", "#ffffff"),
            attributes=label.get("attributes", [])
        )
        for label in labels_config
    ]

def upload_batches(client, session: requests.Session, host: str, project, image_dir: Path, images_per_task: int):
    all_images = sorted([p for p in image_dir.rglob("*") if p.suffix.lower() in [".jpg", ".png"]])
    if not all_images:
        logging.error("No images found in the provided directory.")
        return

    batches = [all_images[i:i + images_per_task] for i in range(0, len(all_images), images_per_task)]

    for i, batch in enumerate(tqdm(batches, desc="Uploading image batches", unit="task")):
        zip_path = Path(f"batch_{i+1}.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for img in batch:
                zf.write(img, arcname=img.name)

        task = client.tasks.create(TaskWriteRequest(name=f"Auto Task {i+1}", project_id=project.id))

        upload_zip(session, host, task.id, zip_path)

        try:
            zip_path.unlink()
            logging.debug(f"Deleted temporary zip archive: {zip_path}")
        except Exception as e:
            logging.warning(f"Could not delete temporary file {zip_path}: {e}")

def upload_zip(session: requests.Session, host: str, task_id: int, zip_path: Path):
    session.get(f"{host}/tasks/{task_id}/data")
    csrf_token = session.cookies.get("csrftoken")

    with open(zip_path, "rb") as archive_file:
        files = {"client_files[0]": (archive_file.name, archive_file, "application/zip")}
        session.post(
            f"{host}/api/tasks/{task_id}/data",
            files=files,
            data={
                "image_quality": 100,
                "use_zip_chunks": "false",
                "use_cache": "false",
                "image_archive": ""
            },
            headers={
                "X-CSRFToken": csrf_token,
                "Referer": f"{host}/tasks/{task_id}/data"
            },
            cookies={"csrftoken": csrf_token}
        )
