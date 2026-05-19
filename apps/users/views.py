from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from apps.users.users_serializers import RegisterSerializer

class RegisterView (CreateAPIView):
    serializer_class = RegisterSerializer

    