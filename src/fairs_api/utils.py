from werkzeug.exceptions import Forbidden
from flask import current_app, request, session
import os
import datetime


def get_filename(key: str) -> str:
    file = request.files.get(key, None)
    if file:
        assets_dir = current_app.config["ASSETS_DIR"]
        files_in_assets = len(os.listdir(assets_dir))
        _, ext = os.path.splitext(file.filename)
        sfn = os.path.join(assets_dir, f"file_{files_in_assets}{ext}")

        while os.path.isfile(sfn):
            files_in_assets += 1
            sfn = os.path.join(assets_dir, f"file_{files_in_assets}{ext}")

        base = f"file_{files_in_assets}{ext}"
        return [
            base, f"/{os.path.basename(os.path.normpath(assets_dir))}/{base}"]
    return [None, None]


def store_file(key: str, mimetype_frag: str) -> None:
    file = request.files[key]
    assets_dir = current_app.config["ASSETS_DIR"]
    if mimetype_frag not in file.mimetype:
        raise ValueError
    fn = get_filename(key)[0]
    fn = os.path.join(assets_dir, fn)
    file.save(fn)


def delete_file(path: str) -> None:
    full_path = os.path.join(current_app.instance_path, path[1:])
    if os.path.exists(full_path):
        os.remove(full_path)


def get_checkbox(key: str) -> bool:
    return request.form.get(key, "").lower() == "true"


def get_date(key: str) -> datetime.datetime:
    trimmed = get_str(key)
    df = "%Y-%m-%d"
    if trimmed:
        try:
            dt = datetime.datetime.strptime(trimmed, df)
            return dt.date()
        except ValueError:
            pass

    return None


def get_int(key: str, default: int) -> int:
    d = request.form.get(key, None)
    return (int(d) if d else default)


def get_float(key: str, default: float) -> float:
    d = request.form.get(key, None)
    return (float(d) if d else default)


def get_str(key: str) -> str:
    return request.form.get(key, "").strip()


def check_role(role: str | list) -> None:
    urole = session.get("user_role", None)
    if isinstance(role, list) and urole not in role:
        raise Forbidden
    elif isinstance(role, str) and urole != role:
        raise Forbidden


def check_ownership(key: str) -> None:
    id = get_int(key, -1)
    if session.get("user_id", None) != id:
        raise Forbidden
