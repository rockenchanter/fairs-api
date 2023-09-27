from flask_sqlalchemy import SQLAlchemy
from typing_extensions import Annotated
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy import func, Column, ForeignKey
import datetime
import enum

db = SQLAlchemy()

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


# fields like "logo", "image" are just paths
class NotificationKind(enum.IntEnum):
    NEW_INVITATION = 0
    NEW_REQUEST = 1
    ACCEPTED_INVITATION = 2
    REJECTED_INVITATION = 3
    ACCEPTED_REQUEST = 4
    REJECTED_REQUEST = 5


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
    role: Mapped[str]
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]
    image: Mapped[str]

    # mappings
    notifications: Mapped["Notification"] = relationship(
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )

    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_abstract": True
    }


class Administrator(User):
    __mapper_args__ = {
        "polymorphic_identity": "administrator",
    }


class Exhibitor(User):
    company: Mapped["Company"] = relationship(
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
    start: Mapped[datetime.datetime] = mapped_column(default=func.now())
    end: Mapped[datetime.datetime]
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


class Hall(DescribableMixin, db.Model):
    size: Mapped[float]
    parking: Mapped[bool] = mapped_column(default=False)
    internet: Mapped[bool] = mapped_column(default=False)
    dissability: Mapped[bool] = mapped_column(default=False)
    pets: Mapped[bool] = mapped_column(default=False)
    price: Mapped[float]
    city: Mapped[str]
    street: Mapped[str]
    zipcode: Mapped[str]

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


class Company(DescribableMixin, db.Model):
    image: Mapped[str]

    # mappings
    exhibitor_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    exhibitor: Mapped["Exhibitor"] = relationship(back_populates="company")
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


class Image(db.Model):
    id: Mapped[intpk]
    path: Mapped[str]
    description: Mapped[str]

    # mappings
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("hall.id", ondelete="CASCADE")
    )
    hall: Mapped["Hall"] = relationship(back_populates="images")


class Stall(db.Model):
    id: Mapped[intpk]
    size: Mapped[float]
    electricity: Mapped[bool] = mapped_column(default=False)
    network: Mapped[bool] = mapped_column(default=False)
    support: Mapped[bool] = mapped_column(default=False)
    image: Mapped[str]
    amount: Mapped[int]
    max_amount: Mapped[int]

    # mappings
    hall_id: Mapped[int] = mapped_column(
        ForeignKey("hall.id", ondelete="CASCADE")
    )
    hall: Mapped["Hall"] = relationship(back_populates="stalls")
    proxies: Mapped[List["FairProxy"]] = relationship(
        back_populates="stall",
        cascade="all, delete",
        passive_deletes=True
    )


class Notification(db.Model):
    id: Mapped[intpk]
    read: Mapped[bool] = mapped_column(default=False)
    kind: Mapped["NotificationKind"]

    # mappings
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(back_populates="notifications")


class FairProxy(db.Model):
    id: Mapped[intpk]
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
        ForeignKey("fair.id", ondelete="CASCADE")
    )
    company: Mapped["Company"] = relationship(back_populates="fair_proxies")
    fair: Mapped["Fair"] = relationship(back_populates="fair_proxies")
    stall: Mapped[Optional["Stall"]] = relationship(back_populates="proxies")
