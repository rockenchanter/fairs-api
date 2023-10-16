from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Forbidden
from flask import current_app, request, session
import os


def get_filename(file: FileStorage) -> str:
    if file:
        assets_dir = current_app.config["ASSETS_DIR"]
        files_in_assets = len(os.listdir(assets_dir))
        _, ext = os.path.splitext(file.filename)
        sfn = os.path.join(assets_dir, f"file_{files_in_assets}{ext}")

        while os.path.isfile(sfn):
            files_in_assets += 1
            sfn = os.path.join(assets_dir, f"file_{files_in_assets}{ext}")

        base = f"file_{files_in_assets}{ext}"
        return [base, f"/{os.path.basename(os.path.normpath(assets_dir))}/{base}"]
    return [None, None]


def store_file(file: FileStorage, mimetype_frag: str) -> None:
    assets_dir = current_app.config["ASSETS_DIR"]
    if mimetype_frag not in file.mimetype:
        raise ValueError
    fn = get_filename(file)[0]
    fn = os.path.join(assets_dir, fn)
    file.save(fn)


def delete_file(path: str) -> None:
    full_path = os.path.join(current_app.instance_path, path)
    if os.path.exists(full_path):
        os.remove(full_path)


def get_checkbox(key: str) -> bool:
    return request.form.get(key, "").lower() == "true"


def get_int(key: str, default: int) -> int:
    d = request.form.get(key, None)
    return (int(d) if d else default)


def get_float(key: str, default: float) -> float:
    d = request.form.get(key, None)
    return (float(d) if d else default)


def get_str(key: str) -> str:
    return request.form.get(key, "").strip()


def check_role(role: str) -> None:
    if session.get("user_role", None) != role:
        raise Forbidden
