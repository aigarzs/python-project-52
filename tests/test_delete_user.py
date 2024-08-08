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


class UserDeleteTestCase(SimpleTestCase):
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

    def test_delete_get_without_login(self):
        client = Client()
        user_id = self.users[0].id
        url = "/users/%s/delete/" % user_id
        response = client.get(url)
        assert response.status_code == 302

    def test_delete_post_without_login(self):
        client = Client()
        user_id = self.users[0].id
        url = "/users/%s/delete/" % user_id
        response = client.post(url)
        assert response.status_code == 302

    def test_delete_get_with_login(self):
        client = Client()
        user = self.users[0]
        data = {"username": USERS[0]["username"],
                "password": USERS[0]["password"]}
        client.post("/login/", data)
        url = "/users/%s/delete/" % user.id
        response = client.get(url)
        assert response.status_code == 200
        templ_names = [t.name for t in response.templates]
        assert "user_delete.html" in templ_names

    def test_delete_post_with_login(self):
        client = Client()
        user = self.users[0]
        login_data = {"username": USERS[0]["username"],
                      "password": USERS[0]["password"]}
        client.post("/login/", login_data)
        url = "/users/%s/delete/" % user.id
        client.post(url)
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_post_with_invalid_login(self):
        client = Client()
        user = self.users[0]
        login_data = {"username": USERS[1]["username"],
                      "password": USERS[1]["password"]}
        client.post("/login/", login_data)
        url = "/users/%s/delete/" % user.id
        client.post(url)
        assert User.objects.filter(id=user.id).exists()

    def tearDown(self):
        for user in self.users:
            user.delete()
        super().tearDown()
