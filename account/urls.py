from django.urls import path
from .views import UserRegistrationsView, UserLoginView, UserProfileView, UserChangePassword

urlpatterns = [
    path("register/", UserRegistrationsView.as_view(), name="register" ),
    path("login/", UserLoginView.as_view(), name="login" ),
    path("profile/", UserProfileView.as_view(), name="profile" ),
    path("changepassword/", UserChangePassword.as_view(), name="changepassword" ),
]
