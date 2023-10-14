from os import path
import pytest

pytestmark = pytest.mark.usefixtures("clean_db", "create_image")


def test_create(auth, client, create_user, image_params):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    dt = image_params.copy()
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/hall_img.jpg")
    dt["path"] = (open(image, "rb"), "image.jpg", "image/jpeg")
    dt["hall_id"] = 1

    response = client.post("/images/create", data=dt)
    assert response.status_code == 201


def test_update(auth, client, image_params, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    dt = image_params.copy()
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/face.jpg")
    dt["path"] = (open(image, "rb"), "face.jpg", "image/jpeg")
    dt["hall_id"] = 1
    dt["description"] = "new description"
    response = client.patch("/images/1", data=dt)
    assert response.status_code == 204


def test_destroy(auth, client, create_user):
    data = create_user({"role": "administrator"})
    auth.login(data["email"], data["password"])
    response = client.delete("/images/6")
    assert response.status_code == 200
