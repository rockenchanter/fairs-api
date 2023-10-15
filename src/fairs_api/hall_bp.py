from flask import Blueprint, request, session
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import contains_eager
from sqlalchemy import and_, update

from .models import Hall, Fair, db
from .utils import get_checkbox, get_int, get_str, delete_file, check_role


bp = Blueprint("hall", __name__, url_prefix="/halls")


def hall_params():
    return {
            "name": get_str("name"),
            "price": get_int("price", 0),
            "street": get_str("street"),
            "zipcode": get_str("zipcode"),
            "city": get_str("city"),
            "description": get_str("description"),
            "parking": get_checkbox("parking"),
            "internet": get_checkbox("internet"),
            "dissability": get_checkbox("dissability"),
            "pets": get_checkbox("pets"),
            "public": get_checkbox("public"),
            "size": get_int("size", 0),
            }


@bp.get("/")
def index():
    select = db.select(Hall).outerjoin(Hall.images).outerjoin(
            Hall.fairs).options(
                contains_eager(Hall.images),
                contains_eager(Hall.fairs),
                )

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
    select = db.select(Hall).outerjoin(Hall.images).outerjoin(
            Hall.fairs).outerjoin(Hall.stalls).filter(
                Hall.id == id).options(
                    contains_eager(Hall.images),
                    contains_eager(Hall.fairs),
                    contains_eager(Hall.stalls))

    with db.session() as session:
        hall = session.scalars(select).unique().first()
        if hall is None:
            raise NotFound
        else:
            return {"hall": hall.serialize()}, 200


@bp.delete("/<int:id>")
def destroy(id: int):
    check_role("administrator")

    select = db.select(Hall).outerjoin(Hall.images).outerjoin(
            Hall.stalls).outerjoin(Hall.fairs).filter(Hall.id == id).options(
                contains_eager(Hall.images),
                contains_eager(Hall.fairs),
                contains_eager(Hall.stalls))
    hall = db.session.scalar(select)
    if hall:
        for obj in hall.images:
            delete_file(obj.path)
        for obj in hall.stalls:
            delete_file(obj.image)
        for obj in hall.stalls:
            delete_file(obj.image)
        db.session.execute(db.delete(Hall).filter(Hall.id == id))
        db.session.commit()
    return {}, 200


@bp.post("/create")
def new():
    check_role("administrator")
    hp = hall_params()
    hall = Hall(**hp)

    if hall.is_valid():
        db.session.add(hall)
        db.session.commit()
        return {}, 201
    errors = hall.localize_errors(session["locale"])
    return {"hall": hall.serialize(False), "errors": errors}, 422


@bp.patch("/<int:id>")
def _update(id: int):
    check_role("administrator")
    hp = hall_params()
    hp["id"] = id
    stmt = update(Hall).filter(Hall.id == hp["id"]).values(**hp)

    hall = Hall(**hp)
    if hall.is_valid():
        db.session.execute(stmt)
        db.session.commit()
        return {}, 204

    errors = hall.localize_errors(session["locale"])
    return {"hall": hall.serialize(False), "errors": errors}, 422
