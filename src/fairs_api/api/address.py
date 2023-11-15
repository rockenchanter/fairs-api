from flask import session
from werkzeug.exceptions import Forbidden

from fairs_api.models import db, Address
from fairs_api import utils as ut
from .api import API, ListAPI


BASE_STMT = db.select(Address).\
        join(Address.company).options(db.contains_eager(Address.company))


def address_params():
    return {
        "zipcode": ut.get_str("zipcode"),
        "city": ut.get_str("city"),
        "street": ut.get_str("street"),
        "company_id": ut.get_int("company_id", 0),
    }


class AddressAPI(API):
    def __init__(self):
        super().__init__(Address, BASE_STMT, "exhibitor")

    def _create_params(self):
        return address_params()

    def _update_params(self):
        ret = self._create_params()
        ret.pop("company_id")
        return ret

    def _before_patch(self, obj):
        super()._before_patch(obj)
        if obj.company.exhibitor_id != session.get("user_id", None):
            raise Forbidden

    def _before_delete(self, obj):
        super()._before_delete(obj)
        if obj.company.exhibitor_id != session.get("user_id", None):
            raise Forbidden


class AddressListAPI(ListAPI):
    def __init__(self):
        super().__init__(Address, BASE_STMT, "exhibitor")

    def _before_post(self):
        super()._before_post()

    def _create_params(self):
        return address_params()
