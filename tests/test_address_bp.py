import pytest

pytestmark = pytest.mark.usefixtures(
    "clean_db",
    "create_address",
    "create_address",
    "create_company"
)


def test_create(auth, client, create_user, address_params):
    data = create_user({"role": "exhibitor"})
    auth.login(data["email"], data["password"])
    dt = address_params.copy()
    dt["company_id"] = 1
    dt["exhibitor_id"] = data["id"]

    response = client.post("/addresses", data=dt)
    assert response.status_code == 201


def test_update(auth, client, address_params, create_user):
    data = create_user({"role": "exhibitor"})
    auth.login(data["email"], data["password"])
    dt = address_params.copy()
    dt["company_id"] = 1
    dt["description"] = "new description"
    dt["exhibitor_id"] = data["id"]
    response = client.patch("/addresses/1", data=dt)
    assert response.status_code == 200


def test_destroy(auth, client, create_user):
    data = create_user({"role": "exhibitor"})
    auth.login(data["email"], data["password"])
    response = client.delete("/addresses/6")
    assert response.status_code == 200
