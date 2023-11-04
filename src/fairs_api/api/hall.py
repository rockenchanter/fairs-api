from flask import request

from fairs_api.models import db, Hall, Fair
from fairs_api import utils as ut

from .api import ListAPI, API


BASE_STMT = db.select(Hall).outerjoin(Hall.images).\
    outerjoin(Hall.fairs).outerjoin(Hall.stalls).\
    options(
        db.contains_eager(Hall.images),
        db.contains_eager(Hall.fairs),
        db.contains_eager(Hall.stalls))


def hall_params():
    return {
        "name": ut.get_str("name"), "price": ut.get_int("price", 0),
        "street": ut.get_str("street"), "zipcode": ut.get_str("zipcode"),
        "city": ut.get_str("city"),
        "description": ut.get_str("description"),
        "parking": ut.get_checkbox("parking"),
        "internet": ut.get_checkbox("internet"),
        "dissability": ut.get_checkbox("dissability"),
        "pets": ut.get_checkbox("pets"),
        "public": ut.get_checkbox("public"),
        "size": ut.get_int("size", 0),
    }


class HallAPI(API):

    def __init__(self):
        super().__init__(Hall, BASE_STMT, "administrator")

    def _create_params(self):
        return hall_params()


class HallListAPI(ListAPI):
    def __init__(self):
        super().__init__(Hall, BASE_STMT, "administrator")

    def _create_params(self):
        return hall_params()

    def _parse_index_params(self):
        select = self.base_stmt
        if (name_arg := request.args.get("name", None)) is not None:
            select = select.filter(Hall.name.like(f"%{name_arg}%"))
        if request.args.get("parking", None):
            select = select.filter(Hall.parking)
        if request.args.get("internet", None):
            select = select.filter(Hall.internet)
        if request.args.get("dissability", None):
            select = select.filter(Hall.dissability)
        if request.args.get("pets", None):
            select = select.filter(Hall.pets)
        if (city_arg := request.args.get("city", None)) is not None:
            select = select.filter(Hall.city == city_arg)

        s = request.args.get("start", None)
        e = request.args.get("end", None)

        if s is not None and e is not None:
            select = select.filter(
                ~Hall.fairs.any(db.and_(s <= Fair.end, e >= Fair.start))
            )
        return select
