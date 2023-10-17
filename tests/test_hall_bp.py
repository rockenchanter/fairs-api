from fairs_api.models import Hall, Fair, Image, db
import pytest
import json
from datetime import date

pytestmark = pytest.mark.usefixtures("clean_db")


@pytest.fixture()
def make_halls(app, hall_params, fair_params, image_params, create_user):
    halls = [
        Hall(**hall_params), Hall(**hall_params), Hall(**hall_params),
        Hall(**hall_params), Hall(**hall_params)
    ]
    fairs = [
        Fair(**fair_params), Fair(**fair_params), Fair(**fair_params),
        Fair(**fair_params), Fair(**fair_params)
    ]
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
        fairs[i].organizer_id = 1

    with app.app_context():
        db.session.add_all(halls)
        db.session.add_all(fairs)
        db.session.commit()


def test_index_without_parameters(client, make_halls):
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
def test_index_with_parameters(client, params, expected, make_halls):
    response = client.get("/halls/", query_string=params)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data["halls"]) == expected


@pytest.mark.parametrize("id", [1, 2, 3, 4, 5])
def test_show_with_existing_halls(client, id, make_halls):
    response = client.get(f"/halls/{id}")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "hall" in data


def test_show_with_non_existing_hall(client):
    response = client.get("/halls/6")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "errors" in data


def test_delete_with_existing_hall(auth, client, create_hall, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    response = client.delete("/halls/1")

    assert response.status_code == 200


def test_delete_with_existing_hall_without_permissions(
        auth, client, create_hall):
    response = client.delete("/halls/1")

    assert response.status_code == 403


def test_create_with_valid_data(auth, client, hall_params, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    response = client.post("/halls/create", data=hall_params)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert "errors" not in data


def test_create_with_valid_data_without_permissions(auth, client, hall_params):
    auth.login("jane@email.com", "Test1234")
    response = client.post("/halls/create", data=hall_params)

    assert response.status_code == 403


def test_create_with_invalid_data(auth, client, hall_params, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    cp = hall_params.copy()
    cp["size"] = -1
    response = client.post("/halls/create", data=cp)
    data = json.loads(response.data)

    assert response.status_code == 422
    assert len(data["errors"]["size"]) > 0


def test_update_with_valid_data(auth, client, hall_params, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    cp = hall_params.copy()
    cp["size"] = 9999
    cp["name"] = "A new name"
    response = client.patch("/halls/4", data=cp)

    assert response.status_code == 200


def test_update_with_valid_data_without_permission(auth, client, hall_params):
    auth.login("jane@email.com", "Test1234")
    cp = hall_params.copy()
    cp["size"] = 9999
    cp["name"] = "A new name"
    response = client.patch("/halls/4", data=cp)

    assert response.status_code == 403


def test_update_with_invalid_data(auth, client, hall_params, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    cp = hall_params.copy()
    cp["size"] = -9999
    response = client.patch("/halls/4", data=cp)
    data = json.loads(response.data)

    assert response.status_code == 422
    assert len(data["errors"]["size"]) > 0
