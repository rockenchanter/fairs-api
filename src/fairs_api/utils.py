from werkzeug.datastructures import FileStorage
from flask import current_app
import os


def get_filename(file: FileStorage) -> str:
    assets_dir = current_app.config["ASSETS_DIR"]
    files_in_assets = len(os.listdir(assets_dir))
    _, ext = os.path.splitext(file.filename)
    sfn = os.path.join(assets_dir, f"file_{files_in_assets + 1}{ext}")

    while os.path.isfile(sfn):
        sfn = get_filename(ext)[0]

    base = f"file_{files_in_assets + 1}{ext}"
    return [base, f"{os.path.basename(os.path.normpath(assets_dir))}/{base}"]


def store_file(file: FileStorage, mimetype_frag: str) -> None:
    assets_dir = current_app.config["ASSETS_DIR"]
    if mimetype_frag not in file.mimetype:
        raise ValueError
    fn = get_filename(file)[0]
    fn = os.path.join(assets_dir, fn)
    file.save(fn)
