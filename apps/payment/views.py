from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="auth:login")
def temp(request):
    return render(request, "temp.html")
