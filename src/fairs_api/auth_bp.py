from flask import Blueprint, session, request
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from . import models as md
from .utils import store_file, get_filename
from .models import db

bp = Blueprint("auth", __name__)


def save_user_in_session(user: md.User):
    session["user_id"] = user.id
    session["user_role"] = user.role


def remove_user_from_session():
    session.pop("user_id", None)
    session.pop("user_role", None)


def login_params():
    return {
        "email": request.form.get("email", None),
        "password": request.form.get("password", None)
    }


def register_params():
    return {
        "name": request.form.get("name", None),
        "surname": request.form.get("surname", None),
        "email": request.form.get("email", None),
        "role": request.form.get("role", None),
        "password": request.form.get("password", None),
    }


@bp.post("/login")
def login():
    params = login_params()
    stmt = db.select(md.User).where(md.User.email == params["email"])
    user = db.one_or_404(stmt, description="invalid_credentials")
    if check_password_hash(user.password, params["password"]):
        save_user_in_session(user)
        return {"user": user.serialize(False)}
    else:
        raise NotFound("invalid_credentials")


@bp.get("/logout")
def logout():
    remove_user_from_session()
    return {}, 200


@bp.get("/authenticate")
def authenticate():
    session["locale"] = request.args.get("locale", "en")
    if "user_id" in session:
        user = db.get_or_404(md.User, session["user_id"], description="not_found")
        return {"user": user.serialize(False)}, 200
    else:
        return {}, 200


@bp.post("/register")
def register():
    params = register_params()

    if params["role"] == "exhibitor":
        user = md.Exhibitor(**params)
    else:
        user = md.Organizer(**params)

    if user.is_valid():
        user.make_password_hash()
        try:
            user.image = get_filename(request.files["image"])[1]
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            user.add_errors_or_skip("email", [["email_taken"]])
            db.session.rollback()
        except ValueError:
            pass
        else:
            store_file(request.files["image"], "image")
            save_user_in_session(user)
            return {"user": user.serialize(False)}, 201
    errors = user.localize_errors(session["locale"])
    return {"user": user.serialize(False), "errors": errors}, 422
