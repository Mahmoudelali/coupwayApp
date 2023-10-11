from django.urls import path, include
from .views import CustomRegisterView

urlpatterns = [
    path("accounts/", include("rest_registration.api.urls")),
    path("register/", CustomRegisterView.as_view(), name="custom_register"),
]
