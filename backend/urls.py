from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from offers.views import index
from django.conf.urls.static import static
from django.conf import settings
from registration.views import CustomAuthToken
from api.views import signup, LoginView, test_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("api/", include(("api.urls", "api"), namespace="api")),
    re_path("signup", signup),
    re_path("login", LoginView),
    re_path("test_token", test_token),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "My Daily Basket Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to MDB admin site"
