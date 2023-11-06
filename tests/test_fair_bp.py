import pytest
import json
from os import path
from datetime import timedelta as dt
from datetime import date

from fairs_api.models import db, Fair, Hall

pytestmark = pytest.mark.usefixtures("clean_db")


@pytest.fixture
def make_fairs(app):
    base = date(2050, 1, 1)
    fairs = [
        Fair(name="First Fair", description="Some description", image="temp",
             start=base, end=base+dt(days=3), organizer_id=1),
        Fair(name="Second Fair", description="Some description", image="temp",
             start=base+dt(days=5), end=base+dt(days=8), organizer_id=1, published=False),
        Fair(name="Third Fair", description="Some description", image="temp",
             start=base+dt(days=10), end=base+dt(days=13), organizer_id=2, published=False),
        Fair(name="Fourth Fair", description="Some description", image="temp",
             start=base+dt(days=15), end=base+dt(days=18), organizer_id=1),
        Fair(name="Fifth Fair", description="Some description", image="temp",
             start=base+dt(days=20), end=base+dt(days=23), organizer_id=1),
    ]
    halls = [
        Hall(name="aaa", description="bbb", size="10", price=10, street="test", zipcode="12345", city="Rzeszów"),
        Hall(name="aaa", description="bbb", size="10", price=10, street="test", zipcode="12345", city="Przemyśl"),
        Hall(name="aaa", description="bbb", size="10", price=10, street="test", zipcode="12345", city="Rzeszów"),
        Hall(name="aaa", description="bbb", size="10", price=10, street="test", zipcode="12345", city="Jarosław"),
        Hall(name="aaa", description="bbb", size="10", price=10, street="test", zipcode="12345", city="Kraków")
    ]
    for i in range(len(fairs)):
        fairs[i].hall = halls[i]
    with app.app_context():
        db.session.add_all(fairs)
        db.session.commit()


def test_index_without_parameters(client, make_fairs):
    res = client.get("/fairs")
    data = json.loads(res.data)

    assert res.status_code == 200
    assert len(data) == 3


@pytest.mark.parametrize("params,expected", [
    ({"name": "First Fair"}, 1),
    ({"start": date(2050, 1, 10)}, 2),
    ({"start": date(2050, 1, 21)}, 1),
    ({"city": "Rzeszów"}, 1),
    ({"city": "Kraków"}, 1),
])
def test_index_with_parameters(client, params, expected, make_fairs):
    response = client.get("/fairs", query_string=params)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == expected


@pytest.mark.parametrize("id,status", [
    (1, 200),   # published fair
    (2, 200),   # unpublished fair, but accessed by organizer
    (3, 404),   # unpublished fair
    (13, 404),  # non existing fair
])
def test_show(client, make_fairs, id, status, create_user, auth):
    user = create_user({"role": "organizer"})
    auth.login(user["email"], user["password"])
    response = client.get(f"/fairs/{id}")

    assert response.status_code == status


def test_create(client, create_user, auth, fair_params, make_industries, make_halls):
    user = create_user({"role": "organizer"})
    auth.login(user["email"], user["password"])
    fp = fair_params.copy()
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/hall_img.jpg")
    fp["image"] = (open(image, "rb"), "image.jpg", "image/jpeg")
    fp["industry"] = "1,2,3"
    fp["start"] = date(2050, 1, 10)
    fp["end"] = date(2050, 1, 15)

    res = client.post("/fairs", data=fp)

    assert res.status_code == 201


def test_update(client, create_user, auth, fair_params, make_fairs, make_industries):
    user = create_user({"role": "organizer"})
    auth.login(user["email"], user["password"])
    par = fair_params.copy()
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/hall_img.jpg")
    par["image"] = (open(image, "rb"), "image.jpg", "image/jpeg")
    par["industry"] = "4,5,6"

    res = client.patch("/fairs/1", data=par)

    assert res.status_code == 200


def test_destroy(client, create_user, auth, make_fairs):
    user = create_user({"role": "organizer"})
    auth.login(user["email"], user["password"])

    response = client.delete("/fairs/1")

    assert response.status_code == 200
