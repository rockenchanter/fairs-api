from flask import Blueprint, request, session
from werkzeug.exceptions import NotFound, Forbidden
from sqlalchemy.orm import contains_eager
from sqlalchemy import and_

from .models import Hall, Fair, db


bp = Blueprint("hall", __name__, url_prefix="/halls")


@bp.get("/")
def index():
    select = db.select(Hall).join(Hall.images).options(
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
    return {}, 200
