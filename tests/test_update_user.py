import copy

from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase

USERS = [{"first_name": "John",
          "last_name": "Lennon",
          "username": "johnlennon",
          "password": "secret1"},
         {"first_name": "Mark",
          "last_name": "Selby",
          "username": "markselby",
          "password": "secret2"},
         {"first_name": "Bruce",
          "last_name": "Willis",
          "username": "brucewillis",
          "password": "secret3"}
         ]


class UserUpdateTestCase(SimpleTestCase):
    databases = ['default']

    def setUp(self):
        super().setUp()
        self.users = []
        for u in USERS:
            user = User.objects.create_user(username=u["username"],
                                            password=u["password"],
                                            first_name=u["first_name"],
                                            last_name=u["last_name"])
            self.users.append(user)

    def test_update_get_without_login(self):
        client = Client()
        user_id = self.users[0].id
        url = "/users/%s/update" % user_id
        response = client.get(url)
        assert response.status_code == 301

    def test_update_post_without_login(self):
        client = Client()
        user_id = self.users[0].id
        user_data = USERS[0]
        url = "/users/%s/update" % user_id
        response = client.post(url, user_data)
        assert response.status_code == 301

    def test_update_get_with_login(self):
        client = Client()
        user = self.users[0]
        data = {"username": USERS[0]["username"],
                "password": USERS[0]["password"]}
        client.post("/login/", data)
        url = "/users/%s/update/" % user.id
        response = client.get(url)
        assert response.status_code == 200
        templ_names = [t.name for t in response.templates]
        assert "user_edit.html" in templ_names
        content = response.content
        assert b"id_first_name" in content
        assert b"id_last_name" in content
        assert b"id_username" in content
        assert b"id_password1" in content
        assert b"id_password2" in content

    def test_update_post_with_login(self):
        client = Client()
        user = self.users[0]
        login_data = {"username": USERS[0]["username"],
                      "password": USERS[0]["password"]}
        client.post("/login/", login_data)
        url = "/users/%s/update/" % user.id
        user_data = copy.copy(USERS[0])
        user_data["first_name"] = "Test"
        user_data["password1"] = user_data["password"]
        user_data["password2"] = user_data["password"]
        client.post(url, user_data)
        user = User.objects.get(id=user.id)
        assert user.first_name == "Test"

    def test_update_post_with_invalid_login(self):
        client = Client()
        user = self.users[0]
        login_data = {"username": USERS[1]["username"],
                      "password": USERS[1]["password"]}
        client.post("/login/", login_data)
        url = "/users/%s/update/" % user.id
        user_data = copy.copy(USERS[0])
        user_data["first_name"] = "Test"
        user_data["password1"] = user_data["password"]
        user_data["password2"] = user_data["password"]
        client.post(url, user_data)
        user = User.objects.get(id=user.id)
        assert user.first_name == USERS[0]["first_name"]

    def tearDown(self):
        for user in self.users:
            user.delete()
        super().tearDown()
