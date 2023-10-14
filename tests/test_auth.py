from flask import session
import json
import pytest
from os import path

pytestmark = pytest.mark.usefixtures("clean_db")


def test_login_with_valid_credentials(auth, client, create_user):
    data = create_user({"role": "exhibitor"})
    with client:
        response = client.post("/login", data={
            "email": data["email"],
            "password": data["password"]
        })
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "user" in data
        assert "user_id" in session
    auth.logout()


def test_login_with_invalid_credentials(client):
    with client:
        response = client.post("/login", data={
            "email": "john.doe@email.com", "password": "Johnny12345"
        })

        data = json.loads(response.data)

        assert response.status_code == 401
        assert "errors" in data
        assert "user_id" not in session


def test_logout(client, auth, create_user):
    data = create_user({"role": "exhibitor"})
    auth.login(data["email"], data["password"])
    with client:
        response = client.get("/logout")

        assert response.status_code == 200
        assert "user_in" not in session


def test_authenticate(client, auth, create_user):
    data = create_user({"role": "exhibitor"})
    auth.login(data["email"], data["password"])
    with client:
        response = client.get("/authenticate", query_string={"locale": "pl"})
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "user" in data
        assert "user_id" in session
        assert session["locale"] == "pl"
    auth.logout()


def test_register_with_taken_email(client, auth, create_user):
    data = create_user({"role": "exhibitor"})
    with client:
        dat = data.copy()
        image = path.join(path.dirname(path.abspath(__file__)),
                          "resources/face.jpg")
        dat["image"] = (open(image, "rb"), "image.jpg", "image/jpeg")
        response = client.post("/register", data=dat)
        data = json.loads(response.data)

        assert response.status_code == 422
        assert "user" in data
        assert "errors" in data
        assert "user_id" not in session


def test_register_with_new_email(client, user_params):
    dat = user_params.copy()
    dat["email"] = "mario@gmail.com"
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/face.jpg")
    dat["image"] = (open(image, "rb"), "image.jpg", "image/jpeg")
    with client:
        response = client.post("/register", data=dat)
        data = json.loads(response.data)

        assert response.status_code == 201
        assert "user" in data
        assert "errors" not in data
        assert "user_id" in session
