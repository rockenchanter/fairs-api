from flask import session
from flask.views import MethodView
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError

from fairs_api.models import db
from fairs_api import utils as ut


class API(MethodView):
    init_every_request = False

    def __init__(self, model, base_stmt, role=None):
        self.model = model
        self.base_stmt = base_stmt
        self.role = role

    def _before_patch(self, obj):
        """Primary used to check permissions"""
        ut.check_role(self.role)

    def _before_delete(self, obj):
        """Primary used to check permissions"""
        ut.check_role(self.role)

    def _create_params(self) -> dict:
        pass

    def _update_params(self) -> dict:
        return self._create_params()

    def get(self, id: int):
        stmt = self.base_stmt.filter(self.model.id == id)
        obj = db.session.scalar(stmt)
        if obj:
            return obj.serialize(), 200
        raise NotFound

    def patch(self, id: int):
        stmt = self.base_stmt.filter(self.model.id == id)
        obj = db.session.scalar(stmt)
        if not obj:
            raise NotFound
        self._before_patch(obj)
        obj.update(self._update_params())
        if obj.is_valid():
            db.session.add(obj)
            db.session.flush()
            ret = obj.serialize()
            return ret, 200
        errors = obj.localize_errors(session.get("locale", "en"))
        return {"errors": errors}, 422

    def delete(self, id: int):
        stmt = self.base_stmt.filter(self.model.id == id)
        obj = db.session.scalar(stmt)
        if obj:
            self._before_delete(obj)
            db.session.delete(obj)
            db.session.commit()
        return {}, 200


class ListAPI(MethodView):
    init_every_request = False

    def __init__(self, model: db.Model, base_stmt, role=None):
        self.model = model
        self.base_stmt = base_stmt
        self.role = role

    def _parse_index_params(self):
        pass

    def _before_post(self):
        """Primary used to check permissions"""
        ut.check_role(self.role)

    def _after_commit(self):
        pass

    def _store_file(self, key: str, mimetype: str):
        ut.store_file(key, mimetype)

    def post(self):
        self._before_post()
        obj = self.model(**self._create_params())
        if obj.is_valid():
            try:
                db.session.add(obj)
                db.session.flush()
                ret = obj.serialize()
                db.session.commit()
                self._after_commit()
                return ret, 201
            except IntegrityError:
                self._on_integrity_error()
        errors = obj.localize_errors(session.get("locale", "en"))
        return {"errors": errors}, 422

    def get(self):
        stmt = self._parse_index_params()
        objs = db.session.scalars(stmt).unique().all()
        return [obj.serialize() for obj in objs], 200
