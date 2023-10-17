from flask import Blueprint, request, session

from .models import Image, db
from . import utils as ut


bp = Blueprint("image", __name__, url_prefix="/images")


def image_params():
    return {
        "path": ut.get_filename(request.files.get("path", None))[1],
        "description": ut.get_str("description"),
        "hall_id": ut.get_int("hall_id", 0)
    }


@bp.post("/create")
def new():
    ut.check_role("administrator")
    im = Image(**image_params())
    if im.is_valid() and im.hall_id != 0:
        ut.store_file(request.files["path"], "image")
        db.session.add(im)
        db.session.flush()
        dt = im.serialize(False)
        db.session.commit()
        return {"image": dt}, 201
    errors = im.localize_errors(session["locale"])
    return {"errors": {"image": errors}}, 422


@bp.patch("/<int:id>")
def update(id: int):
    ut.check_role("administrator")
    im = db.session.get(Image, id)
    par = image_params()
    par.pop("path")
    tmp = Image(**par)
    tmp.path = 'nothing'
    if tmp.is_valid() and im:
        stmt = db.update(Image).where(Image.id == id).values(**par)
        db.session.execute(stmt)
        db.session.commit()
        return {"image": id}, 200
    errors = im.localize_errors(session["locale"])
    return {"errors": {"image": errors}}, 422


@bp.delete("/<int:id>")
def destroy(id: int):
    ut.check_role("administrator")
    im = db.session.get(Image, id)
    if im:
        db.session.delete(im)
        db.session.commit()
    return {}, 200
