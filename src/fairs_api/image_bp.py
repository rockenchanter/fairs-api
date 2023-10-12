from flask import Blueprint, request

from .models import Image, db
from . import utils as ut


bp = Blueprint("image", __name__, url_prefix="/images")


def image_params():
    return {
        "path": ut.get_filename(request.files["path"])[1],
        "description": ut.get_str("description"),
        "hall_id": ut.get_int("hall_id", 0)
    }


@bp.post("/create")
def create():
    ut.check_role("administrator")
    im = Image(**image_params())
    if im.is_valid() and im.hall_id != 0:
        ut.store_file(request.files["path"], "image")
        db.session.add(im)
        db.session.commit()
        return {}, 201
    return {"errors": {"image": im.errors}}, 422


@bp.patch("/<int:id>")
def update(id: int):
    ut.check_role("administrator")
    im = db.session.get(Image, id)
    tmp = Image(**image_params())
    if im and tmp.is_valid():
        ut.delete_file(im.path)
        ut.store_file(request.files["path"], "image")
        stmt = db.update(Image).where(Image.id == id).values(**image_params())
        db.session.execute(stmt)
        return {}, 204
    return {"errors": {"image": tmp.errors}}, 422


@bp.delete("/<int:id>")
def destroy(id: int):
    ut.check_role("administrator")
    im = db.session.get(Image, id)
    if im:
        ut.delete_file(im.path)
        db.session.delete(im)
    return {}, 200
