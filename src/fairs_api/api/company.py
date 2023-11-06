from flask import request, session
from werkzeug.exceptions import Forbidden

from fairs_api.models import db, Company, Industry, Address
from fairs_api import utils as ut
from .api import ListAPI, API


BASE_STMT = db.select(Company).outerjoin(Company.addresses).outerjoin(
    Company.industries).outerjoin(Company.exhibitor).options(
    db.contains_eager(Company.addresses),
    db.contains_eager(Company.industries),
    db.contains_eager(Company.exhibitor),
)


def company_params():
    return {
        "image": ut.get_filename("image")[1],
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
    fd = ut.get_str("industry")
    if fd:
        fd = fd.split(",")
        industries_ids = [int(x.strip()) for x in fd]
        industries = db.session.scalars(
            db.select(Industry).
            filter(Industry.id.in_(industries_ids))).all()
        return industries
    return []


def add_industries(obj: db.Model):
    industries = get_industries()
    if len(industries):
        obj.industries.clear()
    for i in industries:
        obj.industries.append(i)


class CompanyAPI(API):

    def __init__(self):
        super().__init__(Company, BASE_STMT, "exhibitor")

    def _create_params(self):
        return company_params()

    def _modify_obj(self, obj):
        add_industries(obj)

    def _check_ownership(self, obj):
        if obj.exhibitor_id != session.get("user_id", 0):
            raise Forbidden

    def _update_params(self):
        ret = self._create_params()
        ret.pop("image")
        return ret


class CompanyListAPI(ListAPI):
    def __init__(self):
        super().__init__(Company, BASE_STMT, "exhibitor")

    def _create_params(self):
        return company_params()

    def _after_commit(self):
        self._store_file("image", "image")

    def _validate(self, obj):
        return super()._validate(obj) and obj.addresses[0].is_valid()

    def _localize_errors(self, obj):
        cpmy_errors = super()._localize_errors(obj)
        addr_errors = obj.addresses[0].localize_errors(
            session.get("locale", "en")
        )
        return {"company": cpmy_errors, "address": addr_errors}

    def _parse_index_params(self):
        a = request.args
        stmt = self.base_stmt
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
        return stmt

    def _modify_obj(self, obj):
        addr = Address(**address_params())
        addr.company_id = 1
        obj.addresses.append(addr)
        obj.exhibitor_id = session.get("user_id", 0)
        add_industries(obj)
