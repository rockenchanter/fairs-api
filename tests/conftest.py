import pytest

from fairs_api import create_app
import datetime


@pytest.fixture
def app():
    app = create_app("test")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# model fixtures
@pytest.fixture
def user_params():
    return {
        "name": "John", "surname": "Doe", "email": "john.doe@email.com",
        "password": "Johnny1234", "image": "dummydata"
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
