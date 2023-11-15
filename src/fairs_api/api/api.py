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
        self._check_ownership(obj)

    def _before_delete(self, obj):
        """Primary used to check permissions"""
        ut.check_role(self.role)
        self._check_ownership(obj)

    def _create_params(self) -> dict:
        pass

    def _update_params(self) -> dict:
        return self._create_params()

    def _validate(self, obj: db.Model) -> bool:
        return obj.is_valid()

    def _modify_obj(self, obj):
        pass

    def _before_get(self, obj):
        return obj.serialize()

    def get(self, id: int):
        stmt = self.base_stmt.filter(self.model.id == id)
        obj = db.session.scalar(stmt)
        if obj:
            return self._before_get(obj), 200
        raise NotFound

    def patch(self, id: int):
        stmt = self.base_stmt.filter(self.model.id == id)
        obj = db.session.scalar(stmt)
        if not obj:
            raise NotFound
        self._before_patch(obj)
        obj.update(self._update_params())
        self._modify_obj(obj)
        if self._validate(obj):
            db.session.add(obj)
            db.session.flush()
            ret = obj.serialize()
            db.session.commit()
            return ret, 200
        errors = obj.localize_errors(session.get("locale", "en"))
        return {"errors": errors}, 422

    def _check_ownership(self, obj) -> None:
        pass

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

    def _validate(self, obj: db.Model) -> bool:
        return obj.is_valid()

    def _before_validate(self, obj: db.Model):
        pass

    def _before_get(self, objs: list):
        return [obj.serialize() for obj in objs]

    def _modify_obj(self, obj):
        pass

    def _localize_errors(self, obj):
        return obj.localize_errors(session.get("locale", "en"))

    def post(self):
        self._before_post()
        obj = self.model(**self._create_params())
        self._before_validate(obj)
        self._modify_obj(obj)
        if self._validate(obj):
            try:
                db.session.add(obj)
                db.session.flush()
                db.session.commit()
                self._after_commit()
                stmt = self.base_stmt.filter(self.model.id == obj.id)
                obj = db.session.scalar(stmt)
                if obj:
                    return obj.serialize(), 201
                raise NotFound
            except IntegrityError as e:
                print(e)
                self._on_integrity_error()
        errors = self._localize_errors(obj)
        return {"errors": errors}, 422

    def get(self):
        stmt = self._parse_index_params()
        objs = db.session.scalars(stmt).unique().all()
        return self._before_get(objs), 200
