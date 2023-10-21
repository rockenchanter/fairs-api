from flask import Blueprint, request, session
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import contains_eager
from sqlalchemy import and_, update

from .models import Organizer, Fair, Hall, db
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
    obj = Fair(**obj_par)
    obj.organizer_id = session["user_id"]

    if obj.is_valid():
        db.session.add(obj)
        db.session.flush()
        ut.store_file(request.files["image"], "image")
        dt = obj.serialize()
        db.session.commit()
        return {"fair": dt}, 201
    errors = obj.localize_errors(session["locale"])
    return {"obj": obj.serialize(False), "errors": errors}, 422

# @bp.delete("/<int:id>")
# def destroy(id: int):
#     check_role("administrator")

#     select = db.select(Hall).outerjoin(Hall.images).outerjoin(
#             Hall.stalls).outerjoin(Hall.fairs).filter(Hall.id == id).options(
#                 contains_eager(Hall.images),
#                 contains_eager(Hall.fairs),
#                 contains_eager(Hall.stalls))
#     hall = db.session.scalar(select)
#     if hall:
#         db.session.delete(hall)
#         db.session.commit()
#     return {}, 200




# @bp.patch("/<int:id>")
# def _update(id: int):
#     check_role("administrator")
#     hp = hall_params()
#     hp["id"] = id
#     stmt = update(Hall).filter(Hall.id == hp["id"]).values(**hp)

#     hall = Hall(**hp)
#     if hall.is_valid():
#         db.session.execute(stmt)
#         db.session.commit()
#         return {"hall": id}, 200

#     errors = hall.localize_errors(session["locale"])
#     return {"hall": hall.serialize(False), "errors": errors}, 422
