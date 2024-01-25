from django.urls import path

from user.views import CreateUserView, CreateTokenView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token")
]