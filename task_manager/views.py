from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _
from django.utils.translation import activate, deactivate

class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

