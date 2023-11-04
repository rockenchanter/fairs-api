
from flask import request

from fairs_api.models import db, Image
from fairs_api import utils as ut

from .api import ListAPI, API


BASE_STMT = db.select(Image)


def image_params():
    return {
        "path": ut.get_filename(request.files.get("path", None))[1],
        "description": ut.get_str("description"),
        "hall_id": ut.get_int("hall_id", 0)
    }


class ImageAPI(API):

    def __init__(self):
        super().__init__(Image, BASE_STMT, "administrator")

    def _create_params(self):
        return image_params()

    def _update_params(self):
        ret = self._create_params()
        ret.pop("path")
        return ret

    def get(self):
        return {}, 200


class ImageListAPI(ListAPI):
    def __init__(self):
        super().__init__(Image, BASE_STMT, "administrator")

    def _create_params(self):
        return image_params()

    def _after_commit(self):
        self._store_file("path", "image")

    def _parse_index_params(self):
        select = self.base_stmt
        return select

    def get(self):
        return {}, 200
