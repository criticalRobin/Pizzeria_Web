from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


class LoginFormView(LoginView):
    template_name = "accounts/sign-in.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if user.employee_role == "chef":
            return redirect("api:orders_list")
        elif user.employee_role == "cashier":
            return redirect("payment:temp")
        else:
            return redirect("auth:login")


def logout_view(request):
    logout(request)
    return redirect("auth:login")
