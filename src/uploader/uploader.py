import json
import zipfile
import requests
import logging
from pathlib import Path
from tqdm import tqdm
from cvat_sdk.core import make_client
from cvat_sdk.models import ProjectWriteRequest, PatchedLabelRequest, TaskWriteRequest
from urllib3.poolmanager import PoolManager
from cvat_sdk.api_client import rest

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

def create_project(session: requests.Session, host: str, username: str, password: str, project_name: str, reuse_if_exists: bool = False):
    with make_client(host=host, credentials=(username, password)) as client:
        current_user = client.users.retrieve_current_user()

        for existing_project in client.projects.list():
            if existing_project.name == project_name:
                if not reuse_if_exists:
                    raise RuntimeError(
                        f"A project named '{project_name}' already exists (owned by user {existing_project.owner.username}). "
                        f"Use --reuse-project to reuse it, or choose a different project name."
                    )
                if existing_project.owner.id != current_user.id:
                    raise RuntimeError(
                        f"Cannot reuse project '{project_name}' owned by another user (ID: {existing_project.owner.username})."
                    )
                return client, existing_project

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

    existing_tasks = [t for t in client.tasks.list() if t.project_id == project.id]
    task_offset = len(existing_tasks)

    for i, batch in enumerate(tqdm(batches, desc="Uploading image batches", unit="task")):
        zip_path = Path(f"batch_{i+1}.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for img in batch:
                zf.write(img, arcname=img.name)

        task_number = task_offset + i + 1
        task_name = f"Auto Task {task_number}"

        task = client.tasks.create(TaskWriteRequest(name=task_name, project_id=project.id))

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
