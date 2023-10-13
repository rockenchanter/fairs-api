from os import path


def test_create(auth, client, stall_params, seed):
    auth.login("jack@email.com", "Test1234")
    dt = stall_params.copy()
    stall = path.join(path.dirname(path.abspath(__file__)),
                      "resources/hall_img.jpg")
    dt["image"] = (open(stall, "rb"), "stall.jpg", "image/jpeg")
    dt["hall_id"] = 1

    response = client.post("/stalls/create", data=dt)
    assert response.status_code == 201


def test_update(auth, client, stall_params, seed):
    auth.login("jack@email.com", "Test1234")
    dt = stall_params.copy()
    stall = path.join(path.dirname(path.abspath(__file__)),
                      "resources/face.jpg")
    dt["image"] = (open(stall, "rb"), "face.jpg", "image/jpeg")
    dt["hall_id"] = 1
    dt["size"] = 10
    response = client.patch("/stalls/1", data=dt)
    assert response.status_code == 204


def test_destroy(auth, client, seed):
    auth.login("jack@email.com", "Test1234")
    response = client.delete("/stalls/1")
    assert response.status_code == 200
