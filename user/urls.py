from django.urls import path

from user.views import CreateUserView, ManageUserView
from rest_framework_simplejwt import views as jwt_views

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ManageUserView.as_view(), name="profile"),
]
