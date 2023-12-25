from django.urls import path
from .views import UserCreate


urlpatterns = [path("account/register", UserCreate.as_view())]
