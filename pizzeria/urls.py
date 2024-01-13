"""
URL configuration for pizzeria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # new
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('devices', FCMDeviceAuthorizedViewSet)
from home.admin import home_admin_site
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("", include("apps.authentication.urls")),  # new
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/", include("apps.user.urls")),  # new
    path("admin/", home_admin_site.urls),
    path("main/", include("apps.main.urls")),  # new
    path("api/", include("apps.api.urls")),  # new
    path('route/', include(router.urls)),
    path("payment/", include("apps.payment.urls")),  # new
    path("billing/", include("apps.billing.urls")),  # new
]
