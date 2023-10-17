from flask import Blueprint, request, session
from sqlalchemy.orm import contains_eager
from werkzeug.exceptions import NotFound

from . import utils as ut
from .models import Address, Company, Industry, db

bp = Blueprint("company", __name__, url_prefix="/companies")
_base_select = db.select(Company).outerjoin(Company.addresses).outerjoin(
        Company.industries).options(
        contains_eager(Company.addresses),
        contains_eager(Company.industries),
    )


def company_params():
    return {
        "image": ut.get_filename(request.files.get("image", None)),
        "name": ut.get_str("name"),
        "description": ut.get_str("description")
    }


def address_params():
    return {
        "city": ut.get_str("city"),
        "zipcode": ut.get_str("zipcode"),
        "street": ut.get_str("street")
    }


@bp.get("/")
def index():
    a = request.args
    stmt = _base_select

    if cname := a.get("name", None):
        stmt = stmt.filter(Company.name.like(f"%{cname}%"))
    if ccity := a.get("city", None):
        stmt = stmt.filter(Company.addresses.any(
            Address.city.like(f"%{ccity}%")))
    if cind := a.get("industry_id", None):
        stmt = stmt.filter(Company.industries.any(Industry.id == cind))

    data = db.session.scalars(stmt).unique().all()
    return {"companies": [c.serialize(True) for c in data]}, 200


@bp.get("/<int:id>")
def show(id: int):
    res = db.session.scalar(_base_select.filter(Company.id == id))
    if res:
        return {"company": res.serialize(True)}, 200
    raise NotFound