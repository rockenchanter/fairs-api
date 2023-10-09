from fairs_api.models import Hall, Fair, Organizer, Image
import pytest
import json
from datetime import date


def test_index_without_parameters(client, seed):
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
def test_index_with_parameters(client, seed, params, expected):
    response = client.get("/halls/", query_string=params)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data["halls"]) == expected


@pytest.mark.parametrize("id", [1, 2, 3, 4, 5])
def test_show_with_existing_halls(client, seed, id):
    response = client.get(f"/halls/{id}")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert "hall" in data


def test_show_with_non_existing_hall(client, seed):
    response = client.get("/halls/6")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert "errors" in data


def test_delete_with_existing_hall(auth, client, seed):
    auth.login("jack@email.com", "Test1234")
    response = client.delete("/halls/5")

    assert response.status_code == 200


def test_delete_with_existing_hall_without_permissions(
        auth, client, seed):
    auth.login("jane@email.com", "Test1234")
    response = client.delete("/halls/5")

    assert response.status_code == 403


def test_create_with_valid_data(auth, client, hall_params):
    auth.login("jack@email.com", "Test1234")
    response = client.post("/halls/create", data=hall_params)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert "errors" not in data


def test_create_with_valid_data_without_permissions(auth, client, hall_params):
    auth.login("jane@email.com", "Test1234")
    response = client.post("/halls/create", data=hall_params)

    assert response.status_code == 403


def test_create_with_invalid_data(auth, client, hall_params):
    auth.login("jack@email.com", "Test1234")
    cp = hall_params.copy()
    cp["size"] = -1
    response = client.post("/halls/create", data=cp)
    data = json.loads(response.data)

    assert response.status_code == 422
    assert len(data["errors"]["hall"]["size"]) > 0
