import copy
from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase

NEW_USER = {"first_name": "John",
            "last_name": "Lennon",
            "username": "johnlennon",
            "password": "secret"}


class UserCreateTestCase(SimpleTestCase):
    databases = ['default']

    def test_create_user_form(self):
        client = Client()
        response = client.get("/users/create/")
        templ_names = [t.name for t in response.templates]
        assert "user_edit.html" in templ_names
        content = response.content
        assert b"id_first_name" in content
        assert b"id_last_name" in content
        assert b"id_username" in content
        assert b"id_password1" in content
        assert b"id_password2" in content

    def test_create_user_success(self):
        client = Client()
        new_user = copy.copy(NEW_USER)
        new_user["password1"] = NEW_USER["password"]
        new_user["password2"] = NEW_USER["password"]
        response = client.post("/users/create/", new_user)
        assert response.status_code == 302
        user = User.objects.get(username=new_user["username"])
        assert user
        user.delete()

    def test_create_user_duplicate(self):
        client = Client()
        new_user = copy.copy(NEW_USER)
        new_user["password1"] = NEW_USER["password"]
        new_user["password2"] = NEW_USER["password"]
        client.post("/users/create/", new_user)
        duplicate_response = client.post("/users/create/", new_user)
        assert duplicate_response.status_code == 400
        user = User.objects.get(username=new_user["username"])
        user.delete()

    # def tearDown(self):
    #     user = User.objects.get(username=NEW_USER["username"])
    #     if user:
    #         user.delete()
