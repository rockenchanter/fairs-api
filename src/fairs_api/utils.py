from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app
import os


def get_filename(file: FileStorage) -> str:
    static_dir = current_app.config["ASSETS_DIR"]
    files_in_static = len(os.listdir(static_dir))

    sfn = secure_filename(file.filename)
    if len(sfn) == 0:
        raise ValueError

    _, ext = os.path.splitext(sfn)
    sfn = os.path.join(static_dir, f"file_{files_in_static + 1}{ext}")

    while os.path.isfile(sfn):
        sfn = get_filename(ext)[0]

    base = f"file_{files_in_static + 1}{ext}"
    return [base, f"{os.path.basename(os.path.normpath(static_dir))}/{base}"]


def store_file(file: FileStorage, mimetype_frag: str) -> None:
    static_dir = current_app.config["ASSETS_DIR"]
    if mimetype_frag not in file.mimetype:
        raise ValueError
    fn = get_filename(file)[0]
    fn = os.path.join(static_dir, fn)
    file.save(fn)
