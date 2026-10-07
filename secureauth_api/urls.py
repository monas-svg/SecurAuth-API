from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="web-home"), name="root"),
    path("admin/", admin.site.urls),
    path("api/", include("auth_app.urls")),
    path("app/", include("auth_app.web_urls")),
]
