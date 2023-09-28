from fairs_api import models as md
import datetime


def revalidate(obj, expected):
    sut = obj.is_valid()
    assert sut == expected


def set_and_revalidate(obj, expected, field, new_value):
    setattr(obj, field, new_value)
    print(field)
    revalidate(obj, expected)


def test_user_validations(user_params):
    revalidate(md.Exhibitor(**user_params), True)
    set_and_revalidate(md.Exhibitor(**user_params), False, "email", "test.com")
    set_and_revalidate(md.Exhibitor(**user_params), False, "password", "no_digit")
    set_and_revalidate(md.Exhibitor(**user_params), False, "image", "")
    set_and_revalidate(md.Exhibitor(**user_params), False, "name", "")
    set_and_revalidate(md.Exhibitor(**user_params), False, "surname", "")


def test_fair_validations(fair_params):
    now = datetime.date.today()
    valid_sd = now + datetime.timedelta(days=30)
    sut = md.Fair(**fair_params)

    revalidate(md.Fair(**fair_params), True)
    set_and_revalidate(md.Fair(**fair_params), False, "name", "")
    set_and_revalidate(md.Fair(**fair_params), False, "description", "")
    set_and_revalidate(md.Fair(**fair_params), False, "start", now)
    set_and_revalidate(md.Fair(**fair_params), True, "end", valid_sd)
    sut.start = valid_sd
    sut.end = valid_sd - datetime.timedelta(days=1)
    revalidate(sut, False)
