import pytest
import datetime
from datetime import date
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


@pytest.fixture()
def make_halls(app, hall_params, fair_params, image_params, create_user):
    halls = [
        md.Hall(**hall_params), md.Hall(**hall_params), md.Hall(**hall_params),
        md.Hall(**hall_params), md.Hall(**hall_params)
    ]
    fairs = [
        md.Fair(**fair_params), md.Fair(**fair_params), md.Fair(**fair_params),
        md.Fair(**fair_params), md.Fair(**fair_params)
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
        halls[i].images.append(md.Image(**image_params))
        fairs[i].organizer_id = 1

    with app.app_context():
        md.db.session.add_all(halls)
        md.db.session.add_all(fairs)
        md.db.session.commit()


@pytest.fixture
def make_industries(app):
    dset = [
        {"name": "Technologies & Software", "icon": "devices", "color": "blue"},
        {"name": "Healthcare", "icon": "medication", "color": "red"},
        {"name": "Financial Services", "icon": "monetization_on",
         "color": "amber-lighten-1"},
        {"name": "Retail & E-commerce", "icon": "storefront", "color": "black"},
        {"name": "Energy", "icon": "bolt", "color": "yellow"},
        {"name": "Automotive", "icon": "garage", "color": "grey-darken-1"},
        {"name": "Aerospace", "icon": "flight", "color": "blue-lighten-3"},
        {"name": "Food & Beverage", "icon": "restaurant", "color": "red"},
        {"name": "Entertainment & Media", "icon": "live_tv", "color": "purple"},
        {"name": "Transportation & Logistics",
         "icon": "local_shipping", "color": "grey-darken-1"},
        {"name": "Education & E-learning", "icon": "school", "color": "blue"},
        {"name": "Agriculture & Agribusiness",
         "icon": "agriculture", "color": "green"},
        {"name": "Legal Services", "icon": "gavel", "color": "brown-darken-1"},
        {"name": "Sports & Recreation",
         "icon": "fitness_center", "color": "red-lighten-1"},
        {"name": "Biotechnology", "icon": "biotech", "color": "green"},
        {"name": "Gaming & Entertainment", "icon": "sports_esports", "color": "red"},
        {"name": "Architecture", "icon": "architecture", "color": "green"},
        {"name": "Fashion", "icon": "diamond", "color": "pink-lighten-2"},
        {"name": "Environmental Services", "icon": "water_drop", "color": "blue"},
        {"name": "Real Estate", "icon": "apartment", "color": "grey-darken-1"}
    ]
    ind = [md.Industry(**par) for par in dset]
    with app.app_context():
        md.db.session.add_all(ind)
        md.db.session.commit()


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture(autouse=True)
def logout(auth):
    auth.logout()


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


@pytest.fixture()
def clean_db(app):
    meta = md.db.metadata
    with app.app_context():
        for table in reversed(meta.sorted_tables):
            md.db.session.execute(table.delete())
        md.db.session.commit()


# model fixtures
@pytest.fixture()
def user_params():
    return {
        "name": "John", "surname": "Doe", "email": "john.doe@email.com",
        "password": "Test1234", "role": "exhibitor",
        "image": "dummy"
    }


@pytest.fixture()
def create_user(app, user_params):
    par = user_params.copy()

    def _create_user(alter_params):
        par.update(alter_params)
        if par["role"] == "exhibitor":
            obj = md.Exhibitor(**par)
        elif par["role"] == "organizer":
            obj = md.Organizer(**par)
        elif par["role"] == "administrator":
            obj = md.Administrator(**par)

        pas = obj.password
        obj.password = generate_password_hash(obj.password)
        with app.app_context():
            md.db.session.add(obj)
            md.db.session.flush()
            ret = obj.serialize(False)
            ret["password"] = pas
            md.db.session.commit()
        return ret

    return _create_user


@pytest.fixture()
def create_image(app, image_params):
    par = image_params.copy()
    with app.app_context():
        md.db.session.add(md.Image(**par))
        md.db.session.commit()


@pytest.fixture()
def create_address(app, address_params):
    with app.app_context():
        md.db.session.add(md.Address(**address_params))
        md.db.session.commit()


@pytest.fixture()
def create_company(app, company_params):
    with app.app_context():
        md.db.session.add(md.Company(**company_params))
        md.db.session.commit()


@pytest.fixture()
def create_stall(app, stall_params):
    par = stall_params.copy()
    with app.app_context():
        md.db.session.add(md.Stall(**par))
        md.db.session.commit()


@pytest.fixture()
def create_hall(app, hall_params):
    par = hall_params.copy()
    with app.app_context():
        md.db.session.add(md.Hall(**par))
        md.db.session.commit()


@pytest.fixture()
def fair_params():
    now = datetime.date.today()
    correct_sd = datetime.timedelta(days=31) + now
    return {
        "name": "Some Fair", "description": "x", "image": "aaa",
        "start": correct_sd, "end": correct_sd, "organizer_id": 1,
        "hall_id": 1
    }


@pytest.fixture()
def company_params():
    return {"name": "Some Fair", "description": "x", "image": "aaa",
            "exhibitor_id": 1}


@pytest.fixture()
def industry_params():
    return {"name": "IT", "icon": "computer", "color": "blue"}


@pytest.fixture()
def address_params():
    return {"city": "IT", "street": "computer", "zipcode": "13333", "company_id": 1}


@pytest.fixture()
def image_params():
    return {"path": "aaa", "description": "sometext", "hall_id": 1}


@pytest.fixture()
def hall_params():
    return {
        "name": "Arabasta", "description": "Very nice hall", "size": 500,
        "price": 1000, "city": "Warsaw", "street": "Mickiewicza 100",
        "zipcode": "13-333", "public": True
    }


@pytest.fixture()
def stall_params():
    return {"size": 10, "image": "aaa", "amount": 0, "max_amount": 10,
            "hall_id": 1}
