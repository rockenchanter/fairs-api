from flask import Blueprint, session, request

from werkzeug.exceptions import NotFound, Forbidden
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import contains_eager
from .models import FairProxy, FairProxyStatus, Stall, Fair, Company, Hall, db
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
    elif fid := request.args.get("fair_id", None):
        stmt = stmt.filter(FairProxy.fair_id == fid)
    elif cid := request.args.get("company_id", None):
        stmt = stmt.filter(FairProxy.company_id == cid)
    elif role == "organizer":
        stmt = stmt.filter(
                FairProxy.status == FairProxyStatus.SENT,
                FairProxy.invitation == False,
                Fair.organizer_id == uid)
    else:
        stmt = stmt.filter(
                FairProxy.status == FairProxyStatus.SENT,
                Company.exhibitor_id == uid,
                FairProxy.invitation)
    ret = []
    res = db.session.scalars(stmt).unique().all()
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
    stmt = db.select(Hall).join(Hall.fairs).join(Hall.stalls).filter(
            Fair.id == obj.fair_id, Hall.id == Fair.hall_id).options(
                db.contains_eager(Hall.stalls),
                db.contains_eager(Hall.fairs)
            )
    hall = db.session.scalar(stmt)
    invites = db.session.scalars(db.select(FairProxy).filter(
        FairProxy.fair_id == obj.fair_id)).all()
    obj.status = FairProxyStatus.SENT
    obj.invitation = session["user_role"] == "organizer"

    has_slots = hall.slots - len(invites) > 0
    if obj.is_valid() and has_slots:
        db.session.add(obj)
        try:
            db.session.flush()
            dt = obj.serialize(False)
            db.session.commit()
            return dt, 201
        except IntegrityError:
            obj.add_error("invitation", "invitation_exists")

    if not has_slots:
        obj.add_error("invitation", "max_invitations")
    errors = obj.localize_errors(session["locale"])
    return {"errors": errors}, 422


@bp.patch("")
def update():
    ut.check_role(["exhibitor", "organizer"])
    cid = ut.get_int("company_id", 0)
    fid = ut.get_int("fair_id", 0)
    uid = int(session["user_id"])
    sid = ut.get_int("stall_id", 0)
    urole = session.get("user_role")


    obj = db.session.scalar(_base_select.filter(
        FairProxy.company_id == cid), FairProxy.fair_id == fid)
    if obj and (obj.company.exhibitor_id == uid or
                obj.fair.organizer_id == uid) and obj.is_valid():
        obj.status = FairProxyStatus.ACCEPTED if ut.get_int(
            "decision", 0) else FairProxyStatus.REJECTED
        if obj.status == FairProxyStatus.ACCEPTED and urole == "exhibitor":
            stmt = db.select(Stall).outerjoin(FairProxy).filter(
                    Stall.id == sid).options(db.contains_eager(Stall.proxies))
            stall = db.session.scalar(stmt)
            invites = 0
            for fp in stall.proxies:
                if fp.fair_id == fid:
                    invites += 1
            if stall.max_amount - invites <= 0:
                obj.add_error("invitation", "stall_unavailable")
                errors = obj.localize_errors(session.get("locale", "en"))
                return {"errors": errors}, 422
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
