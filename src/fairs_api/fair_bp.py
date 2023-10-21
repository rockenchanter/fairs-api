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
        "start": ut.get_str("start"),
        "end": ut.get_str("end"),
        "published": ut.get_checkbox("published"),
        "image": ut.get_filename(request.files["image"])[1]
    }


@bp.get("")
def index():
    select = _base_select

    if (name_arg := request.args.get("name", None)) is not None:
        select = select.filter(Fair.name.like(f"%{name_arg}"))
    if (city_arg := request.args.get("city", None)) is not None:
        select = select.filter(Hall.city == city_arg)

    s = request.args.get("start", None)

    if s:
        select = select.filter(Fair.start >= s)

    data = db.session.scalars(select).unique().all()
    return {"fairs": [obj.serialize() for obj in data]}, 200


# @bp.get("/<int:id>")
# def show(id: int):
#     select = db.select(Hall).outerjoin(Hall.images).outerjoin(
#             Hall.fairs).outerjoin(Hall.stalls).filter(
#                 Hall.id == id).options(
#                     contains_eager(Hall.images),
#                     contains_eager(Hall.fairs),
#                     contains_eager(Hall.stalls))

#     with db.session() as session:
#         hall = session.scalars(select).unique().first()
#         if hall is None:
#             raise NotFound
#         else:
#             return {"hall": hall.serialize()}, 200


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


# @bp.post("/create")
# def new():
#     check_role("administrator")
#     hp = hall_params()
#     hall = Hall(**hp)

#     if hall.is_valid():
#         db.session.add(hall)
#         db.session.flush()
#         dt = hall.serialize(False)
#         db.session.commit()
#         return {"hall": dt}, 201
#     errors = hall.localize_errors(session["locale"])
#     return {"hall": hall.serialize(False), "errors": errors}, 422


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
