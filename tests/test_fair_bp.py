import pytest
import json
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
             start=base+dt(days=5), end=base+dt(days=8), organizer_id=1),
        Fair(name="Third Fair", description="Some description", image="temp",
             start=base+dt(days=10), end=base+dt(days=13), organizer_id=1),
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
    assert len(data["fairs"]) == 5


@pytest.mark.parametrize("params,expected", [
    ({"name": "First Fair"}, 1),
    ({"start": date(2050, 1, 10)}, 3),
    ({"start": date(2050, 1, 21)}, 1),
    ({"city": "Rzeszów"}, 2),
    ({"city": "Kraków"}, 1),
])
def test_index_with_parameters(client, params, expected, make_fairs):
    response = client.get("/fairs", query_string=params)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data["fairs"]) == expected
