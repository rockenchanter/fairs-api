from fairs_api.models import Hall, Fair, Organizer, Image
import pytest
import json
from datetime import date


@pytest.fixture(scope="module")
def make_couple_halls(hall_params, user_params, fair_params,
                      image_params, session):
    halls = [
        Hall(**hall_params), Hall(**hall_params), Hall(**hall_params),
        Hall(**hall_params), Hall(**hall_params)
    ]
    fairs = [
        Fair(**fair_params), Fair(**fair_params), Fair(**fair_params),
        Fair(**fair_params), Fair(**fair_params)
    ]
    org = Organizer(**user_params)
    org.role = "organizer"
    org.image = "blabla"
    halls[0].parking = True
    halls[0].internet = True
    halls[1].internet = True
    halls[2].dissablitity = True
    halls[3].pets = True

    day = 1
    for i in range(len(fairs)):
        fairs[i].start = date(2023, 1, day)
        day += 4
        fairs[i].end = date(2023, 1, day)
        day += 1
        halls[i].fairs.append(fairs[i])
        halls[i].images.append(Image(**image_params))
        fairs[i].organizer = org

    session.add_all(halls)
    session.commit()


def test_index_without_parameters(client, make_couple_halls):
    response = client.get("/halls/")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data["halls"]) == 5


@pytest.mark.parametrize("params,expected", [
    ({"internet": 1}, 2),
    ({"internet": 1, "parking": 1}, 1),
    ({"internet": 1, "pets": 1}, 0),
    ({"start": date(2023, 1, 3), "end": date(2023, 1, 5)}, 4),
    ({"start": date(2023, 1, 3), "end": date(2023, 1, 7)}, 3),
    ({"start": date(2023, 1, 3), "end": date(2023, 1, 20)}, 1),
])
def test_index_with_parameters(client, make_couple_halls, params, expected):
    response = client.get("/halls/", query_string=params)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data["halls"]) == expected


@pytest.mark.parametrize("id", [1, 2, 3, 4, 5])
def test_show_with_existing_halls(client, make_couple_halls, id):
    response = client.get(f"/halls/{id}")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "hall" in data


def test_show_with_non_existing_hall(client, make_couple_halls):
    response = client.get("/halls/6")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "errors" in data
