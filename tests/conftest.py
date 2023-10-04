import pytest
import datetime
from werkzeug.security import generate_password_hash

from fairs_api import create_app
from fairs_api import models as md


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email: str, password: str):
        return self._client.post("/login", data={
            "email": email, "password": password
            })

    def register(self, name: str, surname: str, email: str, role: str,
                 image: str, password: str):
        fd = {
            "name": name, "password": password, "surname": surname,
            "email": email, "role": role, "image": image,
        }
        return self._client.post("/register", data=fd)

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture(scope="module")
def app():
    app = create_app("test")
    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="module")
def seed(app, user_params):
    users = [
        md.Exhibitor(**user_params),
        md.Organizer(**user_params),
        md.Administrator(**user_params)
    ]
    for us in users:
        us.make_password_hash()
    users[1].email = "jane@email.com"
    users[1].role = "organizer"
    users[2].role = "administrator"
    users[2].email = "jack@email.com"

    with app.app_context():
        md.db.session.add_all(users)
        md.db.session.commit()


# model fixtures
@pytest.fixture(scope="module")
def user_params():
    return {
        "name": "John", "surname": "Doe", "email": "john.doe@email.com",
        "password": "Test1234", "role": "exhibitor",
        "image": "dummy"
    }


@pytest.fixture(scope="module")
def fair_params():
    now = datetime.date.today()
    correct_sd = datetime.timedelta(days=31) + now
    return {
        "name": "Some Fair", "description": "x", "image": "aaa",
        "start": correct_sd, "end": correct_sd
    }


@pytest.fixture(scope="module")
def company_params():
    return {"name": "Some Fair", "description": "x", "image": "aaa"}


@pytest.fixture(scope="module")
def industry_params():
    return {"name": "IT", "icon": "computer", "color": "blue"}


@pytest.fixture(scope="module")
def address_params():
    return {"city": "IT", "street": "computer", "zipcode": "13333"}


@pytest.fixture(scope="module")
def image_params():
    return {"path": "aaa", "description": "sometext"}


@pytest.fixture(scope="module")
def hall_params():
    return {
        "name": "Arabasta", "description": "Very nice hall", "size": 500,
        "price": 1000, "city": "Warsaw", "street": "Mickiewicza 100",
        "zipcode": "13-333"
    }


@pytest.fixture(scope="module")
def stall_params():
    return {"size": 10, "image": "aaa", "amount": 0, "max_amount": 10}
