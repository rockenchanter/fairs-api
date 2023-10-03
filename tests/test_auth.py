from flask import session
import json
from os import path


def test_login_with_valid_credentials(client, seed_db):
    with client:
        response = client.post("/login", data={
            "email": "john.doe@email.com", "password": "Johnny1234"
        })
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "user" in data
        assert "user_id" in session


def test_login_with_invalid_credentials(client):
    with client:
        response = client.post("/login", data={
            "email": "john.doe@email.com", "password": "Johnny12345"
        })

        data = json.loads(response.data)

        assert response.status_code == 401
        assert "errors" in data
        assert "user_id" not in session


def test_logout(client, auth):
    auth.login("john.doe@email.com", "Johnny12345")
    with client:
        response = client.get("/logout")

        assert response.status_code == 200
        assert "user_in" not in session


def test_authenticate(client, auth):
    auth.login("john.doe@email.com", "Johnny1234")
    with client:
        response = client.get("/authenticate", query_string={"locale": "pl"})
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "user" in data
        assert "user_id" in session
        assert session["locale"] == "pl"


def test_register_with_taken_email(client, user_params):
    with client:
        dat = user_params.copy()
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
