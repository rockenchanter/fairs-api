from os import path


def test_create(auth, client, image_params, seed):
    auth.login("jack@email.com", "Test1234")
    dt = image_params.copy()
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/hall_img.jpg")
    dt["path"] = (open(image, "rb"), "image.jpg", "image/jpeg")
    dt["hall_id"] = 1

    response = client.post("/images/create", data=dt)
    assert response.status_code == 201


def test_update(auth, client, image_params, seed):
    auth.login("jack@email.com", "Test1234")
    dt = image_params.copy()
    image = path.join(path.dirname(path.abspath(__file__)),
                      "resources/face.jpg")
    dt["path"] = (open(image, "rb"), "face.jpg", "image/jpeg")
    dt["hall_id"] = 1
    dt["description"] = "new description"
    response = client.patch("/images/1", data=dt)
    assert response.status_code == 204


def test_destroy(auth, client, seed):
    auth.login("jack@email.com", "Test1234")
    response = client.delete("/images/6")
    assert response.status_code == 200
