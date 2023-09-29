from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask import current_app
import os


def get_filename(file: FileStorage) -> str:
    static_dir = current_app.static_folder
    files_in_static = len(os.listdir(static_dir))

    sfn = secure_filename(file.filename)
    if len(sfn) == 0:
        raise ValueError

    _, ext = os.path.splitext(sfn)
    sfn = os.path.join(static_dir, f"file_{files_in_static + 1}{ext}")

    while os.path.isfile(sfn):
        sfn = get_filename(ext)

    return os.path.join(static_dir, f"file_{files_in_static + 1}{ext}")


def store_file(file: FileStorage, mimetype_frag: str) -> None:
    if mimetype_frag not in file.mimetype:
        raise ValueError
    file.save(get_filename(file))
