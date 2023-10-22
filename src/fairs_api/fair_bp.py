from flask import Blueprint, request, session
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import contains_eager
import datetime

from .models import Fair, Hall, Industry, db
from . import utils as ut


bp = Blueprint("fairs", __name__, url_prefix="/fairs")
_base_select = db.select(Fair).\
    outerjoin(Fair.organizer).\
    outerjoin(Fair.hall).\
    outerjoin(Fair.industries).\
    outerjoin(Fair.fair_proxies).\
    options(
    contains_eager(Fair.organizer),
    contains_eager(Fair.hall),
    contains_eager(Fair.industries),
    contains_eager(Fair.fair_proxies),
)


def get_industries():
    fd = request.form.get("industry", None)
    if fd:
        fd = fd.split(",")
        industries_ids = [int(x.strip()) for x in fd]
        industries = db.session.scalars(
            db.select(Industry).
            filter(Industry.id.in_(industries_ids))).all()
        return industries
    return None


def hall_available(hall_id: int, start: datetime.date, end: datetime.date) -> bool:
    fairs = db.session.\
        scalars(db.select(Fair).filter(Fair.hall_id == hall_id)).all()
    if not fairs:
        return False
    valid = True
    for f in fairs:
        if not (end < f.start or start > f.end):
            valid = False
            break
    return valid


def fair_params():
    return {
        "name": ut.get_str("name"),
        "description": ut.get_str("description"),
        "hall_id": ut.get_int("hall_id", 0),
        "start": ut.get_date("start"),
        "end": ut.get_date("end"),
        "published": ut.get_checkbox("published"),
        "image": ut.get_filename(request.files["image"])[1]
    }


@bp.get("")
def index():
    select = _base_select.filter(Fair.published)

    if (name_arg := request.args.get("name", None)) is not None:
        select = select.filter(Fair.name.like(f"%{name_arg}"))
    if (city_arg := request.args.get("city", None)) is not None:
        select = select.filter(Hall.city == city_arg)

    s = request.args.get("start", None)

    if s:
        select = select.filter(Fair.start >= s)

    data = db.session.scalars(select).unique().all()
    return {"fairs": [obj.serialize() for obj in data]}, 200


@bp.get("/<int:id>")
def show(id: int):
    select = _base_select.filter(Fair.id == id)

    obj = db.session.scalar(select)
    if obj is None:
        raise NotFound
    elif obj.published is False and obj.organizer_id != session.get("user_id", None):
        raise NotFound
    else:
        return {"fair": obj.serialize()}, 200


@bp.post("/create")
def new():
    ut.check_role("organizer")
    obj_par = fair_params()
    hall_valid = hall_available(
            obj_par["hall_id"],
            obj_par["start"],
            obj_par["end"])
    obj = Fair(**obj_par)
    obj.organizer_id = session["user_id"]

    industries = get_industries()
    if industries:
        for i in industries:
            obj.industries.append(i)
    if obj.is_valid() and hall_valid:
        db.session.add(obj)
        db.session.flush()
        ut.store_file(request.files["image"], "image")
        dt = obj.serialize()
        db.session.commit()
        return {"fair": dt}, 201

    if not hall_valid:
        obj.add_error("hall_id", "hall_unavailable")

    errors = obj.localize_errors(session["locale"])
    return {"obj": obj.serialize(False), "errors": errors}, 422


@bp.patch("/<int:id>")
def update(id: int):
    ut.check_role("organizer")

    cp = fair_params()
    obj = db.session.scalar(_base_select.filter(Fair.id == id))
    industries = get_industries()
    if obj and obj.organizer_id == session["user_id"]:
        cp.pop("image")
        cp.pop("hall_id")
        obj.update(cp)
        if industries:
            obj.industries.clear()
            for ind in industries:
                obj.industries.append(ind)
        if obj.is_valid():
            db.session.commit()
            return {"fair": id}, 200
        err = obj.localize_errors(session["locale"])
        return {"errors": {"fair": err}}, 422
    raise NotFound


@bp.delete("/<int:id>")
def destroy(id: int):
    ut.check_role("organizer")
    obj = db.session.scalar(_base_select.filter(Fair.id == id))
    if obj:
        db.session.delete(obj)
        db.session.commit()
    return {}, 200
