from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from .views import dashboard_stats_view
from apps.api.models import *
from apps.user.models import *
from apps.main.models import *


# Register your models here.
class HomeAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        context = dashboard_stats_view(request)
        if isinstance(context, dict):
            extra_context.update(context)
        return super().index(request, extra_context)

home_admin_site = HomeAdminSite(name='home_admin')

home_admin_site.register(User)
home_admin_site.register(Order)
home_admin_site.register(OrderDetails)
home_admin_site.register(Product)
home_admin_site.register(Table)
home_admin_site.register(Client)

