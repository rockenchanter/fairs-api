from flask import Flask, session, request
from flask_migrate import Migrate, upgrade
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix
import os

from .models import db, Administrator, Hall, Stall, FairProxy, FairProxyStatus
from .seed import seed
from .validations import get_from_locale
from . import config
from .api import hall, address, image, stall, fair, company

migrate = Migrate(db=db)


def register_api(app, item_api, group_api, name: str):
    api_group = group_api.as_view(f"{name}-group")
    api_item = item_api.as_view(f"{name}-item")
    app.add_url_rule(f"/{name}", view_func=api_group)
    app.add_url_rule(f"/{name}/<int:id>", view_func=api_item)


def handle_400(exc):
    return {"errors": {
        "generic": get_from_locale("bad_request", session["locale"])
    }}, 400


def handle_401(exc):
    return {"errors": {
        "generic": get_from_locale("invalid_credentials", session["locale"])
    }}, 401


def handle_404(exc):
    return {"errors": {
        "generic": get_from_locale("not_found", session["locale"])
    }}, 404


def create_root_user(app):
    stmt = db.select(Administrator)
    admins = db.session.scalars(stmt).all()
    if len(admins) == 0:
        adm = Administrator(
            name="Main",
            surname="Admin",
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
            image="/assets/admin.jpg"
            )
        adm.make_password_hash()
        db.session.add(adm)
        db.session.commit()


def create_app(mode="production"):
    app = Flask(__name__, instance_relative_config=True)


    if mode == "development":
        app.config.from_object(config.DevelopmentConfig(app))
        from flask import send_from_directory

        @app.route("/assets/<path:filename>")
        def serve_static(filename):
            return send_from_directory(
                app.config["ASSETS_DIR"], os.path.basename(filename)
            )
    elif mode == "test":
        app.config.from_object(config.TestConfig(app))
    else:
        # On production we're running behind proxy
        app.config.from_object(config.ProductionConfig())
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )
        Session(app)

    # create instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config["ASSETS_DIR"])
    except OSError:
        pass

    # configure session
    @app.before_request
    def set_session_defaults():
        if "locale" not in session:
            session["locale"] = "en"

    # initialize Flask-SQLAlchemy
    db.init_app(app)
    migrate.init_app(app)
    with app.app_context():
        upgrade()
        create_root_user(app)

    # register error handlers
    app.register_error_handler(400, handle_400)
    app.register_error_handler(401, handle_401)
    app.register_error_handler(404, handle_404)

    # register blueprints
    from .auth_bp import bp as auth
    from .proxy_bp import bp as proxy
    app.register_blueprint(auth)
    app.register_blueprint(proxy)

    # register apis
    register_api(app, hall.HallAPI, hall.HallListAPI, "halls")
    register_api(app, address.AddressAPI, address.AddressListAPI, "addresses")
    register_api(app, image.ImageAPI, image.ImageListAPI, "images")
    register_api(app, stall.StallAPI, stall.StallListAPI, "stalls")
    register_api(app, fair.FairAPI, fair.FairListAPI, "fairs")
    register_api(app, company.CompanyAPI, company.CompanyListAPI, "companies")

    app.cli.add_command(seed)

    # additional routes
    @app.get("/halls/cities")
    def get_cities():
        data = db.session.execute(
                db.select(Hall.city).group_by(Hall.city)).all()
        return {"cities": [r.city for r in data]}, 200

    @app.get("/halls/stalls")
    def get_stalls():
        stmt = db.select(Stall).outerjoin(Stall.proxies).outerjoin(FairProxy.fair).\
                filter(Stall.hall_id == request.args.get("hall_id", 0))
        data = db.session.scalars(stmt).unique().all()
        dset = []
        fid = int(request.args.get("fair_id", 0))
        for i in data:
            obj = i.serialize()
            available_slots = i.max_amount
            for pxy in i.proxies:
                if pxy.fair_id == fid:
                    available_slots -= 1
            obj["amount"] = available_slots
            dset.append(obj)

        return dset, 200
    return app
