from flask import session
import json
from os import path


def test_login_with_valid_credentials(auth, client, user_params, seed):
    with client:
        response = client.post("/login", data={
            "email": user_params["email"],
            "password": user_params["password"]
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


def test_logout(client, auth):
    auth.login("john.doe@email.com", "Johnny12345")
    with client:
        response = client.get("/logout")

        assert response.status_code == 200
        assert "user_in" not in session


def test_authenticate(client, auth, user_params):
    auth.login(user_params["email"], user_params["password"])
    with client:
        response = client.get("/authenticate", query_string={"locale": "pl"})
        data = json.loads(response.data)

        assert response.status_code == 200
        assert "user" in data
        assert "user_id" in session
        assert session["locale"] == "pl"
    auth.logout()


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
