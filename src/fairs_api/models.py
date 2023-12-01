from flask_sqlalchemy import SQLAlchemy
from typing_extensions import Annotated
from typing import List, Optional
from sqlalchemy import event, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy import func, Column, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import datetime
import enum

from . import validations as va
from .utils import delete_file


class Base(DeclarativeBase):
    """Base class for all models

    Provides:
        * method serializing objects to json
        * validation system
        * method for updating attributes
    """

    @property
    def errors(self):
        return self._errors

    def localize_errors(self, locale: str = "en") -> dict:
        """Replaces error dictionary with localized messages"""
        errors = {}

        for key, error_list in self._errors.items():
            data = error_list[0]
            errors[key] = va.get_from_locale(data[0], locale).format(*data[1:])
        return errors

    def add_errors_or_skip(self, field: str, error_msgs: list):
        """Adds error to dictionary when validation fails"""
        for error in error_msgs:
            if error is not None:
                if field not in self._errors.keys():
                    self._errors[field] = []
                # no need for duplicates
                if error not in self._errors[field]:
                    self._errors[field].append(error)

    def add_error(self, field, error_key):
        """Manually add error to dictionary without running any validation"""
        if field not in self._errors.keys():
            self._errors[field] = []
        self._errors[field].append([error_key])

    def update(self, params: dict) -> None:
        """Update object attributes

        It skips any attribute that does not belong to specified class
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """Runs all validations"""
        self._errors = {}
        self._validate()
        return len(self._errors.keys()) == 0

    def _validate(self):
        """Use this method to add validations"""
        pass

    def __delete__(self):
        """Run on 'after_delete' sqlalchemy hook"""
        pass

    def serialize(self, include_relationships: bool = True) -> dict:
        """Returns dictionary with class attributes

        If class has any relationship it will include their shallow
        representation ie. without their related objects.

        """
        props = self.__dict__.copy()
        props.pop('_sa_instance_state')  # Unserializable
        props.pop('_errors', None)  # Errors need to be localized anyway
        keys_to_delete = []


        # Although password is stored as hash, there's no need to send it
        if isinstance(self, User):
            props.pop("password", None)

        for key, value in props.items():
            if not include_relationships:
                if isinstance(value, list | db.Model):
                    keys_to_delete.append(key)
            else:
                if isinstance(value, list):
                    props[key] = [rel.serialize(False) for rel in value]
                elif isinstance(value, db.Model):
                    props[key] = value.serialize(False)
                elif isinstance(value, datetime.date):
                    props[key] = value.strftime("%Y-%m-%d")
        for key in keys_to_delete:
            props.pop(key)

        return props


db = SQLAlchemy(model_class=Base)


intpk = Annotated[int, mapped_column(primary_key=True)]

company_industry = db.Table(
    "company_industry",
    Column("company_id", ForeignKey("company.id"), primary_key=True),
    Column("industry_id", ForeignKey("industry.id"), primary_key=True),
)
fair_industry = db.Table(
    "fair_industry",
    Column("fair_id", ForeignKey("fair.id"), primary_key=True),
    Column("industry_id", ForeignKey("industry.id"), primary_key=True),
)


class FairProxyStatus(enum.IntEnum):
    SENT = 0
    ACCEPTED = 1
    REJECTED = 2


class DescribableMixin:
    id: Mapped[intpk]
    name: Mapped[str]
    description: Mapped[str]


class User(db.Model):
    id: Mapped[intpk]
    name: Mapped[str]
    surname: Mapped[str]
    role: Mapped[str]
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]
    image: Mapped[str]

    # mappings
    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_abstract": True
    }

    def make_password_hash(self):
        self.password = generate_password_hash(self.password)

    def can_change_password(self, oldPass, newPass, passConf) -> bool:
        old_password = self.password
        self.password = newPass
        validation_res = self.is_valid()
        if newPass != passConf:
            self.add_error("password_confirmation", "password_not_match")
        if not check_password_hash(old_password, oldPass):
            self.add_error("old_password", "invalid_password")
        elif validation_res:
            self.make_password_hash()
            return True
        return False

    def _validate(self) -> bool:
        self.add_errors_or_skip("name", [va.min_length(self.name, 1)])
        self.add_errors_or_skip("image", [va.min_length(self.image, 1)])
        self.add_errors_or_skip("surname", [va.min_length(self.surname, 1)])
        self.add_errors_or_skip("email", [va.email(self.email)])
        self.add_errors_or_skip("password", [
            va.min_length(self.password, 8),
            va.contains(self.password, va.upc_letter, "contains_uppercase"),
            va.contains(self.password, va.digit_regex, "contains_digit"),
        ])

    def __delete__(self):
        delete_file(self.image)


class Administrator(User):
    __mapper_args__ = {
        "polymorphic_identity": "administrator",
    }


class Exhibitor(User):
    companies: Mapped[List["Company"]] = relationship(
        back_populates="exhibitor",
        cascade="all, delete",
        passive_deletes=True
    )

    __mapper_args__ = {
        "polymorphic_identity": "exhibitor",
    }


class Organizer(User):
    fairs: Mapped[List["Fair"]] = relationship(
        back_populates="organizer",
        cascade="all, delete",
        passive_deletes=True
    )

    __mapper_args__ = {
        "polymorphic_identity": "organizer",
    }


class Fair(DescribableMixin, db.Model):
    start: Mapped[datetime.date] = mapped_column(default=func.now())
    end: Mapped[datetime.date]
    image: Mapped[str]
    published: Mapped[bool] = mapped_column(default=True)

    # mappings
    organizer_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("hall.id", ondelete="CASCADE")
    )

    organizer: Mapped["Organizer"] = relationship(back_populates="fairs")
    hall: Mapped["Hall"] = relationship(back_populates="fairs")
    industries: Mapped[List["Industry"]] = relationship(
        secondary=fair_industry,
        back_populates="fairs"
    )
    fair_proxies: Mapped[List["FairProxy"]] = relationship(
        back_populates="fair",
        cascade="all, delete-orphan"
    )
    companies: AssociationProxy[List["Company"]] = association_proxy(
        "fair_proxies",
        "company",
        creator=lambda company_obj: FairProxy(company=company_obj)
    )

    def _validate(self):
        self.add_errors_or_skip("name", [va.min_length(self.name, 1)])
        self.add_errors_or_skip("image", [va.min_length(self.image, 1)])
        self.add_errors_or_skip(
            "description", [va.min_length(self.description, 1)])
        self.add_errors_or_skip("start", [va.days_from_now(self.start, 30)])
        self.add_errors_or_skip("end", [
            va.days_from_now(self.end, 30),
            va.min(self.end, self.start),
            ])
        self.add_errors_or_skip("hall_id", [va.min(self.hall_id, 1)])
        self.add_errors_or_skip("organizer_id", [va.min(self.organizer_id, 1)])
        self.add_errors_or_skip("industries", [va.min_children(self.industries, 1)])

    def __delete__(self):
        delete_file(self.image)


class Hall(DescribableMixin, db.Model):
    size: Mapped[float]
    parking: Mapped[bool] = mapped_column(default=False)
    internet: Mapped[bool] = mapped_column(default=False)
    dissability: Mapped[bool] = mapped_column(default=False)
    pets: Mapped[bool] = mapped_column(default=False)
    public: Mapped[bool] = mapped_column(default=False)
    price: Mapped[float]
    city: Mapped[str]
    street: Mapped[str]
    zipcode: Mapped[str]

    @property
    def slots(self):
        amt = 0
        for stall in self.stalls:
            amt += stall.max_amount
        return amt

    # mappings
    fairs: Mapped[List["Fair"]] = relationship(
        back_populates="hall",
        cascade="all, delete",
        passive_deletes=True
    )
    images: Mapped[List["Image"]] = relationship(
        back_populates="hall",
        cascade="all, delete",
        passive_deletes=True
    )
    stalls: Mapped[List["Stall"]] = relationship(
        back_populates="hall",
        cascade="all, delete",
        passive_deletes=True
    )

    def _validate(self):
        self.add_errors_or_skip("name", [va.min_length(self.name, 1)])
        self.add_errors_or_skip(
            "description", [va.min_length(self.description, 1)])
        self.add_errors_or_skip("size", [va.min(self.size, 1)])
        self.add_errors_or_skip("price", [va.min(self.price, 0)])
        self.add_errors_or_skip("city", [va.min_length(self.city, 1)])
        self.add_errors_or_skip("street", [va.min_length(self.street, 1)])
        self.add_errors_or_skip("zipcode", [va.min_length(self.zipcode, 5)])


class Company(DescribableMixin, db.Model):
    image: Mapped[str]

    # mappings
    exhibitor_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    exhibitor: Mapped["Exhibitor"] = relationship(back_populates="companies")
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="company",
        cascade="all, delete",
        passive_deletes=True
    )
    industries: Mapped[List["Industry"]] = relationship(
        secondary=company_industry,
        back_populates="companies"
    )
    fair_proxies: Mapped[List["FairProxy"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    fairs: AssociationProxy[List["Fair"]] = association_proxy(
        "fair_proxies",
        "fair",
        creator=lambda fair_obj: FairProxy(fair=fair_obj)
    )

    def _validate(self):
        self.add_errors_or_skip("name", [va.min_length(self.name, 1)])
        self.add_errors_or_skip("exhibitor_id", [va.min(self.exhibitor_id, 1)])
        self.add_errors_or_skip(
            "description", [va.min_length(self.description, 1)])
        self.add_errors_or_skip("image", [va.min_length(self.image, 1)])
        self.add_errors_or_skip("industries",
                                [
                                    va.min_children(self.industries, 1),
                                    va.max_children(self.industries, 3),
                                ])


class Address(db.Model):
    id: Mapped[intpk]
    city: Mapped[str]
    street: Mapped[str]
    zipcode: Mapped[str]

    # mappings
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE")
    )
    company: Mapped["Company"] = relationship(back_populates="addresses")

    def _validate(self):
        self.add_errors_or_skip("city", [va.min_length(self.city, 1)])
        self.add_errors_or_skip("street", [va.min_length(self.street, 1)])
        self.add_errors_or_skip("zipcode", [va.min_length(self.zipcode, 5)])
        self.add_errors_or_skip("company_id", [va.min(self.company_id, 1)])


class Industry(db.Model):
    id: Mapped[intpk]
    name: Mapped[str]
    icon: Mapped[str]
    color: Mapped[str]

    # mappings
    companies: Mapped[List["Company"]] = relationship(
        secondary=company_industry,
        back_populates="industries"
    )
    fairs: Mapped[List["Fair"]] = relationship(
        secondary=fair_industry,
        back_populates="industries"
    )

    def _validate(self):
        self.add_errors_or_skip("name", [va.min_length(self.name, 2)])
        self.add_errors_or_skip("icon", [va.min_length(self.icon, 2)])
        self.add_errors_or_skip("color", [va.min_length(self.color, 2)])


class Image(db.Model):
    id: Mapped[intpk]
    path: Mapped[str]
    description: Mapped[str]

    # mappings
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("hall.id", ondelete="CASCADE")
    )
    hall: Mapped["Hall"] = relationship(back_populates="images")

    def _validate(self):
        self.add_errors_or_skip("path", [va.min_length(self.path, 1)])
        self.add_errors_or_skip("hall_id", [va.min(self.hall_id, 1)])
        self.add_errors_or_skip(
            "description", [va.min_length(self.description, 1)])

    def __delete__(self):
        delete_file(self.path)


class Stall(db.Model):
    id: Mapped[intpk]
    size: Mapped[float]
    electricity: Mapped[bool] = mapped_column(default=False)
    network: Mapped[bool] = mapped_column(default=False)
    support: Mapped[bool] = mapped_column(default=False)
    image: Mapped[str]
    max_amount: Mapped[int]

    # mappings
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("hall.id", ondelete="CASCADE")
    )
    hall: Mapped["Hall"] = relationship(back_populates="stalls")
    # TODO:  SWITCH TO SET NULL
    proxies: Mapped[List["FairProxy"]] = relationship(
        back_populates="stall",
        cascade="all, delete",
        passive_deletes=True
    )

    def _validate(self):
        self.add_errors_or_skip("size", [va.min(self.size, 1)])
        self.add_errors_or_skip("hall_id", [va.min(self.hall_id, 1)])
        self.add_errors_or_skip("max_amount", [va.min(self.max_amount, 1)])
        self.add_errors_or_skip("image", [va.min_length(self.image, 1)])

    def __delete__(self):
        delete_file(self.image)


class FairProxy(db.Model):
    status: Mapped["FairProxyStatus"]
    invitation: Mapped[bool] = mapped_column(default=True)
    # mappings
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id"), primary_key=True
    )
    fair_id: Mapped[int] = mapped_column(
        ForeignKey("fair.id"), primary_key=True
    )
    stall_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stall.id", ondelete="CASCADE")
    )
    company: Mapped["Company"] = relationship(back_populates="fair_proxies")
    fair: Mapped["Fair"] = relationship(back_populates="fair_proxies")
    stall: Mapped[Optional["Stall"]] = relationship(back_populates="proxies")

    def _validate(self):
        self.add_errors_or_skip("company_id", [va.min(self.company_id, 1)])
        self.add_errors_or_skip("fair_id", [va.min(self.fair_id, 1)])


def before_delete(mapper, connection, target):
    target.__delete__()


def get_company_id():
    stmt = db.select(Company).\
           filter(Company.exhibitor_id == session["user_id"])

    if com := db.session.scalar(stmt):
        return com.id
    return None


event.listen(Image, 'after_delete', before_delete)
event.listen(Stall, 'after_delete', before_delete)
event.listen(Fair,  'after_delete', before_delete)
event.listen(User,  'after_delete', before_delete)
