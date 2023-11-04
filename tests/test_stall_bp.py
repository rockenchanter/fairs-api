from os import path
import pytest

pytestmark = pytest.mark.usefixtures("clean_db")


def test_create(auth, client, stall_params, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    dt = stall_params.copy()
    stall = path.join(path.dirname(path.abspath(__file__)),
                      "resources/hall_img.jpg")
    dt["image"] = (open(stall, "rb"), "stall.jpg", "image/jpeg")
    dt["hall_id"] = 1

    response = client.post("/stalls", data=dt)
    assert response.status_code == 201


def test_update(auth, client, stall_params, create_user, create_stall):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    auth.login("jack@email.com", "Test1234")
    dt = stall_params.copy()
    stall = path.join(path.dirname(path.abspath(__file__)),
                      "resources/face.jpg")
    dt["image"] = (open(stall, "rb"), "face.jpg", "image/jpeg")
    dt["hall_id"] = 1
    dt["size"] = 10
    response = client.patch("/stalls/1", data=dt)
    assert response.status_code == 200


def test_destroy(auth, client, create_user, create_stall):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    auth.login("jack@email.com", "Test1234")
    response = client.delete("/stalls/1")
    assert response.status_code == 200
