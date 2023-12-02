from django.urls import path

from . import views

app_name = "markers"

urlpatterns = [

    path("", views.IndexView.as_view()),
    path("map/<ip>", views.MarkersMapView.as_view()),
    path("latest", views.LatestHackerView.as_view()),
    path("latest_series", views.LatestSeriesHackerView.as_view(), name='latest_series'),
    path('sniff/<period>/<seconds>', views.SniffLastPeriod, name='sniff'),
]
