from flask import Blueprint, session

from sqlalchemy.orm import contains_eager
from .models import Address, Company, Exhibitor, db
from . import utils as ut


bp = Blueprint("address", __name__, url_prefix="/addresses")


def address_params():
    return {
        "zipcode": ut.get_str("zipcode"),
        "city": ut.get_str("city"),
        "street": ut.get_str("street"),
        "company_id": ut.get_int("company_id", 0)
    }


@bp.post("/create")
def new():
    ut.check_role("exhibitor")
    ut.check_ownership("exhibitor_id")
    obj = Address(**address_params())
    if obj.is_valid() and obj.company_id != 0:
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
    obj = db.session.get(Address, id)
    par = address_params()
    tmp = Address(**par)
    if tmp.is_valid() and obj:
        stmt = db.update(Address).where(Address.id == id).values(**par)
        db.session.execute(stmt)
        db.session.commit()
        return {"address": id}, 200
    errors = obj.localize_errors(session["locale"])
    return {"errors": {"address": errors}}, 422


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
