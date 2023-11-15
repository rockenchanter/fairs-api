from flask import Blueprint, session, request

from werkzeug.exceptions import NotFound, Forbidden
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager
from .models import FairProxy, FairProxyStatus, Stall, Fair, Company, db
from . import utils as ut

_base_select = db.select(FairProxy).\
    join(FairProxy.company).\
    join(FairProxy.fair).\
    outerjoin(FairProxy.stall).\
    options(
        contains_eager(FairProxy.company),
        contains_eager(FairProxy.fair),
        contains_eager(FairProxy.stall))
bp = Blueprint("invitations", __name__, url_prefix="/invitations")


def proxy_params():
    return {
        "company_id": ut.get_int("company_id", 0),
        "fair_id": ut.get_int("fair_id", 0),
    }


@bp.get("")
def index():
    uid = int(session.get("user_id", 0))
    role = session.get("user_role", None)

    stmt = _base_select
    if not role:
        raise Forbidden
    elif role == "organizer":
        stmt = stmt.filter(
                FairProxy.status == FairProxyStatus.SENT,
                FairProxy.invitation == False,
                Fair.organizer_id == uid)
    else:
        stmt = stmt.filter(
                Company.exhibitor_id == uid,
                FairProxy.invitation)
    ret = []
    res = db.session.scalars(stmt).unique().all()
    print(uid)
    print(len(res))
    for x in res:
        val = x.serialize()
        val["fair"]["organizer"] = x.fair.organizer.serialize(False)
        val["company"]["exhibitor"] = x.company.exhibitor.serialize(False)
        ret.append(val)
    return ret, 200


@bp.post("/create")
def new():
    ut.check_role(["exhibitor", "organizer"])
    obj = FairProxy(**proxy_params())
    obj.status = FairProxyStatus.SENT
    obj.invitation = session["user_role"] == "organizer"
    if obj.is_valid():
        db.session.add(obj)
        try:
            db.session.flush()
            dt = obj.serialize(False)
            db.session.commit()
            return {"invitation": dt}, 201
        except IntegrityError:
            obj.add_error("invitation", "invitation_exists")
    errors = obj.localize_errors(session["locale"])
    return {"errors": errors}, 422


@bp.patch("")
def update():
    ut.check_role(["exhibitor", "organizer"])
    cid = ut.get_int("company_id", 0)
    fid = ut.get_int("fair_id", 0)
    uid = int(session["user_id"])
    urole = session.get("user_role")

    obj = db.session.scalar(_base_select.filter(
        FairProxy.company_id == cid), FairProxy.fair_id == fid)
    if obj and (obj.company.exhibitor_id == uid or
                obj.fair.organizer_id == uid) and obj.is_valid():
        obj.status = FairProxyStatus.ACCEPTED if ut.get_int(
            "decision", 0) else FairProxyStatus.REJECTED
        if obj.status == FairProxyStatus.ACCEPTED and urole == "exhibitor":
            stall = db.session.get(Stall, ut.get_int("stall_id", 0))
            obj.stall_id = stall.id
        db.session.commit()
        return {}, 200
    raise NotFound


@bp.delete("")
def destroy():
    ut.check_role(["exhibitor", "organizer"])
    cid = int(request.args.get("company_id", 0))
    fid = int(request.args.get("fair_id", 0))
    obj = db.session.\
        scalar(_base_select.
               filter(FairProxy.company_id == cid).
               filter(FairProxy.fair_id == fid))
    uid = session["user_id"]
    if obj and (obj.company.exhibitor_id == uid or
                obj.fair.organizer_id == uid):
        db.session.delete(obj)
        db.session.commit()
    return {}, 200
