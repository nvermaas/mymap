from django.urls import path

from . import views

app_name = "markers"

urlpatterns = [
    path("map/<ip>", views.MarkersMapView.as_view()),
    path("latest", views.LatestHackerView.as_view()),
]
