from flask import Blueprint, request, session
from werkzeug.exceptions import NotFound, Forbidden
from sqlalchemy.orm import contains_eager
from sqlalchemy import and_

from .models import Hall, Fair, db
from .utils import get_checkbox, get_int, get_str


bp = Blueprint("hall", __name__, url_prefix="/halls")


def hall_params():
    return {
            "name": get_str("name"),
            "price": get_int("price", 0),
            "street": get_str("name"),
            "zipcode": get_str("name"),
            "city": get_str("name"),
            "description": get_str("name"),
            "parking": get_checkbox("parking"),
            "internet": get_checkbox("internet"),
            "dissability": get_checkbox("dissability"),
            "pets": get_checkbox("pets"),
            "public": get_checkbox("public"),
            "size": get_int("size", 0),
            }


@bp.get("/")
def index():
    select = db.select(Hall).join(Hall.images).filter(Hall.public).options(
            contains_eager(Hall.images))

    if (name_arg := request.args.get("name", None)) is not None:
        select = select.filter(Hall.name.like(f"%{name_arg}"))
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
                ~Hall.fairs.any(and_(s <= Fair.end, e >= Fair.start))
                )

    with db.session() as session:
        halls = session.scalars(select).unique().all()
        return {"halls": [h.serialize() for h in halls]}, 200


@bp.get("/<int:id>")
def show(id: int):
    select = db.select(Hall).join(Hall.images).outerjoin(Hall.fairs).outerjoin(
            Hall.stalls).filter(Hall.id == id)

    with db.session() as session:
        hall = session.scalars(select).unique().first()
        if hall is None:
            raise NotFound
        else:
            return {"hall": hall.serialize()}, 200


@bp.delete("/<int:id>")
def destroy(id: int):
    if session.get("user_role", None) != "administrator":
        raise Forbidden
    db.session.execute(db.delete(Hall).filter(Hall.id == id))
    # TODO: remove associated files from disk
    return {}, 200


@bp.post("/create")
def new():
    if session.get("user_role", None) != "administrator":
        raise Forbidden
    hp = hall_params()
    hall = Hall(**hp)

    if hall.is_valid():
        db.session.add(hall)
        db.session.commit()
        return {}, 201
    else:
        return {"errors": {"hall": hall.errors}}, 422
