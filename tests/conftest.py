import pytest

from fairs_api import create_app
from fairs_api.models import db
from fairs_api import models as md
import datetime
from os import path


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


@pytest.fixture(scope="module")
def app():
    app = create_app("test")
    return app


@pytest.fixture(scope="module")
def session(app):
    with app.app_context():
        with db.session() as sess:
            yield sess


@pytest.fixture(scope="module")
def seed_db(session):
    exh = md.Exhibitor(**{
        "name": "John", "surname": "Doe", "email": "john.doe@email.com",
        "password": "Johnny1234", "image": "dummydata"
    })
    exh.make_password_hash()
    session.add(exh)
    session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# model fixtures
@pytest.fixture
def user_params():
    image = path.join(path.dirname(path.abspath(__file__)), "resources/face.jpg")
    yield {
        "name": "John", "surname": "Doe", "email": "john.doe@email.com",
        "password": "Johnny1234", "role": "exhibitor",
        "image": (open(image, "rb"), "image.jpg", "image/jpeg")
    }


@pytest.fixture
def fair_params():
    now = datetime.date.today()
    correct_sd = datetime.timedelta(days=31) + now
    return {
        "name": "Some Fair", "description": "x", "image": "aaa",
        "start": correct_sd, "end": correct_sd
    }


@pytest.fixture
def company_params():
    return {"name": "Some Fair", "description": "x", "image": "aaa"}


@pytest.fixture
def industry_params():
    return {"name": "IT", "icon": "computer", "color": "blue"}


@pytest.fixture
def address_params():
    return {"city": "IT", "street": "computer", "zipcode": "13333"}


@pytest.fixture
def image_params():
    return {"path": "aaa", "description": "sometext"}


@pytest.fixture
def hall_params():
    return {
        "name": "aaa", "description": "sometext", "size": 50, "price": 1000,
        "city": "IT", "street": "computer", "zipcode": "13333"
    }


@pytest.fixture
def stall_params():
    return {"size": 10, "image": "aaa", "amount": 0, "max_amount": 10}


@pytest.fixture
def auth(client):
    return AuthActions(client)
