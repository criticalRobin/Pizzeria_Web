from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics


# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
