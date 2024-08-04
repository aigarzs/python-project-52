from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.utils.translation import activate, deactivate
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class UsersView(View):

    def get(self, request, *args, **kwargs):
        context = {"users": User.objects.all()}
        return render(request, "users_list.html", context=context)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, _("You have logged in"))
            return redirect("home")
        else:
            context = {"error": _("Please enter valid user name and password. "
                                  + "Both fields might be register sensitive.")}
            return render(request, "login.html",
                          context=context, status=400)


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, _("You have logged out."))
        return redirect("home")


def validate_user(username, password1, password2):
    error_messages = {}

    try:
        User.username_validator(username)
    except ValidationError as err:
        error_messages["username"] = str(err)[2:-2]

    if password1 == password2:
        try:
            validate_password(password1)
        except ValidationError as err:
            error_messages["password"] = str(err)[2:-2]
    else:
        error_messages["password"] = _("Passwords do not match.")

    if error_messages:
        return error_messages
    else:
        return None


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        title = _("Registration")
        post_button = _("Register user")
        context = {"title": title, "post_button": post_button}
        return render(request, "user_edit.html", context=context)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        error_messages = validate_user(username, password1, password2)

        if not error_messages:
            try:
                User.objects.create_user(username=username,
                                         first_name=first_name,
                                         last_name=last_name,
                                         password=password1)
            except IntegrityError:
                msg = _("A user with that username already exists.")
                error_messages = {"username": msg}

        if error_messages:
            context = {
                "title": _("Registration"),
                "post_button": _("Register user"),
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "error_messages": error_messages
            }
            return render(request, "user_edit.html",
                          context=context, status=400)

        messages.success(request, _("User has successfully registered"))
        return redirect("login")


class UserUpdateView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")

        if not request.user.is_authenticated:
            msg = _("You are not authorized. Please log in!")
            messages.error(request, msg)
            return redirect("login")
        if request.user.id != user_id:
            msg = _("You have not rights to change other user.")
            messages.error(request, msg)
            return redirect("users")

        user = User.objects.get(id=user_id)
        title = _("Update user")
        post_button = _("Update")
        context = {"title": title,
                   "post_button": post_button,
                   "first_name": user.first_name,
                   "last_name": user.last_name,
                   "username": user.username}
        return render(request, "user_edit.html", context=context)

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")

        if not request.user.is_authenticated:
            msg = _("You are not authorized. Please log in!")
            messages.error(request, msg)
            return redirect("login")
        if request.user.id != user_id:
            msg = _("You have not rights to change other user.")
            messages.error(request, msg)
            return redirect("users")

        user = User.objects.get(id=user_id)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        error_messages = validate_user(username, password1, password2)

        if not error_messages:
            try:
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.set_password(password1)
                user.save()
            except IntegrityError:
                msg = _("A user with that username already exists.")
                error_messages = {"username": msg}

        if error_messages:
            context = {
                "title": _("Update user"),
                "post_button": _("Update"),
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "error_messages": error_messages
            }
            return render(request, "user_edit.html",
                          context=context, status=400)

        messages.success(request, _("User has successfully updated"))
        logout(request)
        return redirect("users")


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")

        if not request.user.is_authenticated:
            msg = _("You are not authorized. Please log in!")
            messages.error(request, msg)
            return redirect("login")
        if request.user.id != user_id:
            msg = _("You have not rights to change other user.")
            messages.error(request, msg)
            return redirect("users")

        user = User.objects.get(id=user_id)
        question = _("Are you sure you want to delete %(first_name)s "
                     "%(last_name)s?") % {"first_name": user.first_name,
                                          "last_name": user.last_name}
        context = {"question": question}
        return render(request, "user_delete.html", context=context)

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")

        if not request.user.is_authenticated:
            msg = _("You are not authorized. Please log in!")
            messages.error(request, msg)
            return redirect("login")
        if request.user.id != user_id:
            msg = _("You have not rights to change other user.")
            messages.error(request, msg)
            return redirect("users")

        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, _("User has successfully deleted."))
        logout(request)
        return redirect("users")
