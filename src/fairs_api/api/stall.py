from fairs_api.models import db, Stall
from fairs_api import utils as ut

from .api import ListAPI, API


BASE_STMT = db.select(Stall)


def stall_params():
    return {
        "size": ut.get_float("size", 0),
        "electricity": ut.get_checkbox("electricity"),
        "network": ut.get_checkbox("network"),
        "support": ut.get_checkbox("support"),
        "image": ut.get_filename("image")[1],
        "max_amount": ut.get_int("max_amount", 0),
        "hall_id": ut.get_int("hall_id", 0)
    }


class StallAPI(API):

    def __init__(self):
        super().__init__(Stall, BASE_STMT, "administrator")

    def _create_params(self):
        return stall_params()

    def _update_params(self):
        ret = self._create_params()
        ret.pop("image")
        ret.pop("max_amount")
        return ret

    def get(self):
        return {}, 200


class StallListAPI(ListAPI):
    def __init__(self):
        super().__init__(Stall, BASE_STMT, "administrator")

    def _create_params(self):
        ret = stall_params()
        ret["amount"] = ret["max_amount"]
        return ret

    def _after_commit(self):
        self._store_file("image", "image")

    def _parse_index_params(self):
        select = self.base_stmt
        return select

    def get(self):
        return {}, 200
