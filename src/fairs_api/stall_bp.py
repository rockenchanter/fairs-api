from flask import Blueprint, request, session

from .models import Stall, db
from . import utils as ut


bp = Blueprint("stall", __name__, url_prefix="/stalls")


def stall_params():
    return {
        "size": ut.get_float("size", 0),
        "electricity": ut.get_checkbox("electricity"),
        "network": ut.get_checkbox("network"),
        "support": ut.get_checkbox("support"),
        "image": ut.get_filename(request.files.get("image", None))[1],
        "max_amount": ut.get_int("max_amount", 0),
        "hall_id": ut.get_int("hall_id", 0)
    }


@bp.post("/create")
def create():
    ut.check_role("administrator")
    stall = Stall(**stall_params())
    stall.amount = stall.max_amount
    if stall.is_valid() and stall.hall_id != 0:
        ut.store_file(request.files["image"], "image")
        db.session.add(stall)
        db.session.commit()
        return {}, 201
    errors = stall.localize_errors(session["locale"])
    return {"errors": {"stall": errors}}, 422


@bp.patch("/<int:id>")
def update(id: int):
    ut.check_role("administrator")
    stall = db.session.get(Stall, id)
    sp = stall_params()
    # amount and max amount can not be modified
    sp.pop("max_amount")
    tmp = Stall(**sp)
    tmp.image = 'nothing'
    tmp.amount = stall.amount
    tmp.max_amount = stall.max_amount

    if tmp.is_valid() and stall:
        sp.pop("image")
        stmt = db.update(Stall).where(Stall.id == id).values(sp)
        db.session.execute(stmt)
        db.session.commit()
        return {}, 204
    errors = tmp.localize_errors(session["locale"])
    return {"errors": {"stall": errors}}, 422


@bp.delete("/<int:id>")
def destroy(id: int):
    ut.check_role("administrator")
    stall = db.session.get(Stall, id)
    if stall:
        ut.delete_file(stall.image)
        db.session.delete(stall)
        db.session.commit()
    return {}, 200
