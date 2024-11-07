from django.contrib import auth
from ninja.security import HttpBasicAuth


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            return user
