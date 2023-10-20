from flask import Blueprint, session

from werkzeug.exceptions import NotFound
from sqlalchemy.orm import contains_eager
from .models import Address, Company, db, get_company_id
from . import utils as ut

_base_select = db.select(Address).\
        join(Address.company).options(contains_eager(Address.company))

bp = Blueprint("address", __name__, url_prefix="/addresses")


def address_params():
    return {
        "zipcode": ut.get_str("zipcode"),
        "city": ut.get_str("city"),
        "street": ut.get_str("street"),
        "company_id": get_company_id()
    }


@bp.post("/create")
def new():
    ut.check_role("exhibitor")
    ut.check_ownership("exhibitor_id")
    obj = Address(**address_params())
    if obj.is_valid():
        db.session.add(obj)
        db.session.flush()
        dt = obj.serialize(False)
        db.session.commit()
        return {"address": dt}, 201
    errors = obj.localize_errors(session["locale"])
    return {"errors": {"address": errors}}, 422


@bp.patch("/<int:id>")
def update(id: int):
    ut.check_role("exhibitor")
    ut.check_ownership("exhibitor_id")
    obj = db.session.scalar(_base_select.filter(Address.id == id))
    if obj:
        obj.update(address_params())
        if obj.is_valid():
            db.session.commit()
            return {"address": id}, 200
        errors = obj.localize_errors(session["locale"])
        return {"errors": {"address": errors}}, 422
    raise NotFound


@bp.delete("/<int:id>")
def destroy(id: int):
    ut.check_role("exhibitor")
    stmt = db.select(Address).\
        join(Address.company).\
        join(Company.exhibitor).\
        options(
            contains_eager(Address.company).
            contains_eager(Company.exhibitor)).\
        filter(Address.id == id)

    obj = db.session.scalar(stmt)
    if obj and obj.company.exhibitor.id == session.get("user_id", None):
        db.session.delete(obj)
        db.session.commit()
    return {}, 200
