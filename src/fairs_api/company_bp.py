from flask import Blueprint, request, session
from sqlalchemy.orm import contains_eager
from werkzeug.exceptions import NotFound

from . import utils as ut
from .models import Address, Company, Industry, db

bp = Blueprint("company", __name__, url_prefix="/companies")
_base_select = db.select(Company).outerjoin(Company.addresses).outerjoin(
        Company.industries).outerjoin(Company.exhibitor).options(
        contains_eager(Company.addresses),
        contains_eager(Company.industries),
        contains_eager(Company.exhibitor),
    )


def company_params():
    return {
        "image": ut.get_filename(request.files.get("image", None))[1],
        "name": ut.get_str("name"),
        "description": ut.get_str("description")
    }


def address_params():
    return {
        "city": ut.get_str("city"),
        "zipcode": ut.get_str("zipcode"),
        "street": ut.get_str("street"),
    }


def get_industries():
    fd = request.form.get("industry", None)
    if fd:
        fd = fd.split(",")
        industries_ids = [int(x.strip()) for x in fd]
        industries = db.session.scalars(
                db.select(Industry).
                filter(Industry.id.in_(industries_ids))).all()
        return industries
    return None


@bp.get("")
def index():
    a = request.args
    stmt = _base_select

    if cname := a.get("name", None):
        stmt = stmt.filter(Company.name.like(f"%{cname}%"))
    if ccity := a.get("city", None):
        stmt = stmt.filter(Company.addresses.any(
            Address.city.like(f"%{ccity}%")))
    if cind := a.get("industry", None):
        fd = cind.split(",")
        industries_ids = [int(x.strip()) for x in fd]
        stmt = stmt.filter(Industry.id.in_(industries_ids))
    if cid := a.get("id", None):
        fd = cid.split(",")
        ids = [int(x.strip()) for x in fd]
        stmt = stmt.filter(Company.id.in_(ids))
    if uid := a.get("exhibitor_id", None):
        uid = int(uid)
        stmt = stmt.filter(Company.exhibitor_id == uid)
    data = db.session.scalars(stmt).unique().all()
    return {"companies": [c.serialize(True) for c in data]}, 200


@bp.get("/<int:id>")
def show(id: int):
    res = db.session.scalar(_base_select.filter(Company.id == id))
    if res:
        return {"company": res.serialize(True)}, 200
    raise NotFound


@bp.post("/create")
def new():
    ut.check_role("exhibitor")
    cmpny = Company(**company_params())
    addr = Address(**address_params())
    addr.company_id = 1

    industries = get_industries()
    if industries:
        for i in industries:
            cmpny.industries.append(i)

    cmpny.exhibitor_id = session.get("user_id", None)
    cmpny.addresses.append(addr)

    cvalid = cmpny.is_valid()
    avalid = addr.is_valid()

    if cvalid and avalid:
        db.session.add(cmpny)
        ut.store_file(request.files["image"], "image")
        db.session.flush()
        dat = cmpny.serialize(True)
        db.session.commit()
        return {"company": dat}, 201
    ce = cmpny.localize_errors(session["locale"])
    ae = addr.localize_errors(session["locale"])
    return {"errors": {"company": ce, "address": ae}}, 422


@bp.patch("/<int:id>")
def update(id: int):
    ut.check_role("exhibitor")
    ut.check_ownership("exhibitor_id")

    cp = company_params()
    company = db.session.scalar(_base_select.filter(Company.id == id))
    industries = get_industries()
    if company:
        cp.pop("image")
        company.update(cp)
        if industries:
            company.industries.clear()
            for ind in industries:
                company.industries.append(ind)
        if company.is_valid():
            db.session.commit()
            return {"company": id}, 200
        err = company.localize_errors(session["locale"])
        return {"errors": {"company": err}}, 422
    raise NotFound


@bp.delete("/<int:id>")
def destroy(id: int):
    ut.check_role("exhibitor")
    company = db.session.scalar(_base_select.filter(Company.id == id))
    if company and company.exhibitor.id == session["user_id"]:
        db.session.delete(company)
        db.session.commit()
    return {}, 200
