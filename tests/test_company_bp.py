import pytest
import json
from os import path

from fairs_api import models as md

pytestmark = pytest.mark.usefixtures("clean_db")


@pytest.fixture
def make_companies(app, company_params, industry_params):
    companies = [
        md.Company(**company_params), md.Company(**company_params),
        md.Company(**company_params), md.Company(**company_params),
        md.Company(**company_params)
    ]
    companies[0].name = "Company 0"
    companies[1].name = "Company 1"
    companies[2].name = "Company 0"
    companies[3].name = "Company 3"
    companies[4].name = "Company 4"
    addresses = [
        md.Address(city="Rzeszów", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Przemyśl", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Rzeszów", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Przemyśl", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Jarosław", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Radymno", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Jarosław", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Żurawica", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Radymno", zipcode="35-015", street="Pigonia 1"),
        md.Address(city="Żurawica", zipcode="35-015", street="Pigonia 1"),
    ]

    with app.app_context():
        ai = 0
        for idx in range(len(companies)):
            c = companies[idx]
            c.industries.append(md.Industry(**industry_params))
            for a in addresses[ai:ai + 2]:
                c.addresses.append(a)
            ai += 2

        md.db.session.add_all(companies)
        md.db.session.commit()


def test_index_without_filters(client, make_companies):
    res = client.get("/companies")
    data = json.loads(res.data)

    assert res.status_code == 200
    assert len(data) == 5


@pytest.mark.parametrize("params,expected", [
    ({"city": "Rzeszów"}, 2),
    ({"name": "Company 0", "city": "Rzeszów"}, 1),
    ({"city": "Jarosław", "industry": 12}, 0),
    ({"name": "Company 0", "city": "Jarosław"}, 1),
])
def test_index_with_parameters(client, params, expected, make_companies):
    response = client.get("/companies", query_string=params)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == expected


def test_show_with_existing_company(client, make_companies):
    response = client.get("/companies/1")

    assert response.status_code == 200


def test_show_with_non_existing_company(client):
    response = client.get("/companies/10")

    assert response.status_code == 404


def test_create(client, auth, company_params, address_params, create_user, make_industries):
    usr = create_user({"role": "exhibitor"})
    auth.login(usr["email"], usr["password"])

    body = company_params.copy()
    ap = address_params.copy()
    body.update(ap)
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/face.jpg")
    body["image"] = (open(image, "rb"), "image.jpg", "image/jpeg")
    body["industry"] = "1,2,3"
    res = client.post("/companies", data=body)
    assert res.status_code == 201


def test_update(client, auth, company_params, create_user, make_industries, make_companies):
    usr = create_user({"role": "exhibitor"})
    auth.login(usr["email"], usr["password"])
    body = company_params.copy()
    body["exhibitor_id"] = usr["id"]

    res = client.patch("/companies/1", data=body)
    assert res.status_code == 200


def test_destroy(client, auth, create_user, make_industries, make_companies):
    usr = create_user({"role": "exhibitor"})
    auth.login(usr["email"], usr["password"])

    res = client.delete("/companies/1")

    assert res.status_code == 200
