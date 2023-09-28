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


def test_company_validations(company_params):
    revalidate(md.Company(**company_params), True)
    set_and_revalidate(md.Company(**company_params), False, "name", "")
    set_and_revalidate(md.Company(**company_params), False, "description", "")
    set_and_revalidate(md.Company(**company_params), False, "image", "")


def test_industry_validations(industry_params):
    revalidate(md.Industry(**industry_params), True)
    set_and_revalidate(md.Industry(**industry_params), False, "name", "")
    set_and_revalidate(md.Industry(**industry_params), False, "color", "")
    set_and_revalidate(md.Industry(**industry_params), False, "icon", "")


def test_address_validations(address_params):
    revalidate(md.Address(**address_params), True)
    set_and_revalidate(md.Address(**address_params), False, "city", "")
    set_and_revalidate(md.Address(**address_params), False, "street", "")
    set_and_revalidate(md.Address(**address_params), False, "zipcode", "")


def test_image_validations(image_params):
    revalidate(md.Image(**image_params), True)
    set_and_revalidate(md.Image(**image_params), False, "path", "")
    set_and_revalidate(md.Image(**image_params), False, "description", "")


def test_hall_validations(hall_params):
    revalidate(md.Hall(**hall_params), True)
    set_and_revalidate(md.Hall(**hall_params), False, "name", "")
    set_and_revalidate(md.Hall(**hall_params), False, "description", "")
    set_and_revalidate(md.Hall(**hall_params), False, "size", 0)
    set_and_revalidate(md.Hall(**hall_params), False, "price", -1)
    set_and_revalidate(md.Hall(**hall_params), False, "city", "")
    set_and_revalidate(md.Hall(**hall_params), False, "street", "")
    set_and_revalidate(md.Hall(**hall_params), False, "zipcode", "")


def test_stall_validations(stall_params):
    revalidate(md.Stall(**stall_params), True)
    set_and_revalidate(md.Stall(**stall_params), False, "size", 0)
    set_and_revalidate(md.Stall(**stall_params), False, "max_amount", 0)
    set_and_revalidate(md.Stall(**stall_params), False, "amount", -1)
