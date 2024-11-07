from ninja.security import HttpBasicAuth
from django.contrib import auth


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            return user
