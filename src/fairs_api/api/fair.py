from flask import request, session
from werkzeug.exceptions import Forbidden, NotFound
import datetime

from fairs_api.models import db, Fair, Hall, FairProxy, FairProxyStatus, Industry
from fairs_api import utils as ut
from .api import ListAPI, API


BASE_STMT = db.select(Fair).\
    outerjoin(Fair.organizer).\
    outerjoin(Fair.hall).\
    outerjoin(Hall.stalls).\
    outerjoin(Fair.industries).\
    outerjoin(Fair.fair_proxies).\
    order_by(Fair.start).\
    options(
        db.contains_eager(Fair.organizer),
        db.contains_eager(Fair.industries),
        db.contains_eager(Fair.fair_proxies),
        db.contains_eager(Fair.hall).contains_eager(Hall.stalls)
    )


def fair_params():
    return {
        "name": ut.get_str("name"),
        "description": ut.get_str("description"),
        "hall_id": ut.get_int("hall_id", 0),
        "start": ut.get_date("start"),
        "end": ut.get_date("end"),
        "published": ut.get_checkbox("published"),
        "image": ut.get_filename("image")[1]
    }


def get_industries():
    fd = request.form.get("industry", None)
    if fd:
        fd = fd.split(",")
        industries_ids = [int(x.strip()) for x in fd]
        industries = db.session.scalars(
            db.select(Industry).
            filter(Industry.id.in_(industries_ids))).all()
        return industries
    return []


def add_industries(obj):
    industries = get_industries()
    obj.industries.clear()
    for i in industries:
        obj.industries.append(i)


def hall_available(hall_id: int, start: datetime.date, end: datetime.date) -> bool:
    fairs = db.session.\
        scalars(db.select(Fair).filter(Fair.hall_id == hall_id)).all()
    if not fairs:
        return True
    valid = True
    for f in fairs:
        if not (end < f.start or start > f.end):
            valid = False
            break
    return valid


class FairAPI(API):

    def __init__(self):
        super().__init__(Fair, BASE_STMT, "organizer")

    def _create_params(self):
        return fair_params()

    def _update_params(self):
        ret = self._create_params()
        ret.pop("image")
        ret.pop("hall_id")
        return ret

    def _modify_obj(self, obj):
        add_industries(obj)

    def _before_patch(self, obj):
        self.not_modifiable = obj.published

    def _validate(self, obj):
        obj_valid = super()._validate(obj)
        if self.not_modifiable:
            obj.add_error("generic", "not_modifiable")
            return False
        return obj_valid

    def _before_delete(self, obj):
        super()._before_delete(obj)
        if obj.organizer_id != session.get("user_id", None):
            raise Forbidden


class FairListAPI(ListAPI):
    def __init__(self):
        super().__init__(Fair, BASE_STMT, "organizer")

    def _create_params(self):
        ret = fair_params()
        ret["organizer_id"] = session.get("user_id", 0)
        return ret

    def _after_commit(self):
        self._store_file("image", "image")

    def _before_validate(self, obj):
        par = self._create_params()
        self.hall_available = hall_available(
            par["hall_id"],
            par["start"],
            par["end"]
        )

    def _before_get(self, objs):
        dset = []
        for fair in objs:
            serialized_item = fair.serialize()
            serialized_item["hall"]["stalls"] = [
                    s.serialize() for s in fair.hall.stalls
            ]
            dset.append(serialized_item)
        return dset

    def _validate(self, obj):
        obj_valid = super()._validate(obj)
        if not self.hall_available:
            obj.add_error("hall_id", "hall_unavailable")
        return obj_valid and self.hall_available

    def _modify_obj(self, obj):
        add_industries(obj)

    def _parse_index_params(self):
        usr_role = session.get("user_role", None)
        if usr_role == "organizer":
            select = BASE_STMT
        else:
            select = BASE_STMT.filter(Fair.published)

        if name_arg := request.args.get("name", None):
            select = select.filter(Fair.name.like(f"%{name_arg}%"))
        if city_arg := request.args.get("city", None):
            select = select.filter(Hall.city == city_arg)

        if hid := request.args.get("hall_id", None):
            select = select.filter(Hall.id == int(hid))
        if uid := request.args.get("organizer_id", None):
            select = select.filter(Fair.organizer_id == int(uid))
        if cid := request.args.get("company_id", None):
            select = select.filter(db.and_(
                FairProxy.company_id == cid,
                FairProxy.status == FairProxyStatus.ACCEPTED
            ))
        if cind := request.args.get("industry", None):
            fd = cind.split(",")
            industries_ids = [int(x.strip()) for x in fd]
            select = select.filter(Industry.id.in_(industries_ids))
        s = request.args.get("start", None)
        if s:
            select = select.filter(Fair.start >= s)
        return select
