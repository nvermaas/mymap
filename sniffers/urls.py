from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("sniffers/admin/", admin.site.urls),
    path("sniffers/markers/", include("markers.urls"),
    ),
]